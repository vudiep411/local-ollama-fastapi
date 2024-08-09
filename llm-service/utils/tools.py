import ollama
from tavily import TavilyClient
from langchain_community.chat_models import ChatOllama
from dotenv import load_dotenv
from langchain_community.chat_message_histories import RedisChatMessageHistory
import os 
from langchain_core.messages import SystemMessage
import logging
load_dotenv()

tavily_api_key = os.getenv("TAVILY_API_KEY")
tavily_client = TavilyClient(api_key=tavily_api_key)


"""Get redis client for session id"""
def history(session_id, redis_url):
    return RedisChatMessageHistory(session_id, redis_url)

def search_web(query):
    try:
        return tavily_client.get_search_context(query)
    except:
        return ""

def get_tools(query):
    response = ollama.chat(
        model='llama3.1',
        messages=[{'role': 'user', 'content': query
        }],

        tools=[
        {
        'type': 'function',
        'function': {
            'name': 'search_web',
            'description': 'Get context from web search',
            'parameters': {
            'type': 'object',
            'properties': {
                'query': {
                'type': 'string',
                'description': 'query for looking up web search',
                },
            },
            'required': ['query'],
            },
        },
        }
    ],
    )
    return response['message'].get('tool_calls', [])

def system_prompt(query, context):
    SYSTEM_PROMPT = """
    You are a helpful assistant. Use the following sources of information to answer the question IF NEEDED.
    Cite the sources in your answer if used.
    Question: {query}

    Context: {context}
    """.format(query=query, context=context)
    return SYSTEM_PROMPT


def get_search_context(query):
    tools = get_tools(query)
    if tools:
        for tool_call in tools:
            if tool_call['function']['name'] == 'search_web':
                logging.info(f"Tool call: {tool_call}")
                search_query = tool_call['function']['arguments']['query']
                context = search_web(search_query)
                return system_prompt(query, context)
    return ""
