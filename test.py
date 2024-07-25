from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import ConfigurableField
from langchain_core.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_experimental.llms.ollama_functions import OllamaFunctions
from langchain_core.tools import tool
from langchain.schema import Document
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()

web_search_tool = TavilySearchResults()

llm = OllamaFunctions(model="llama3.1", format="json")
prompt = ChatPromptTemplate.from_template("You are a helpful assistant tasked with answering user questions. "
            "You have access to one: web_search."
            "For any other questions, such as questions about current events, use the web_search tool to get information from the web."
            "{topic}"
            )


@tool
def web_search(query: str) -> str:
    """Run web search on the question."""
    web_results = web_search_tool.invoke({"query": query})
    return [
        Document(page_content=d["content"], metadata={"url": d["url"]})
        for d in web_results
    ]

tools = [
    {
        "name": "search_in_web",
        "description": "Use Tavily to search information in Internet.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "str",
                    "description": "The query used to search in Internet. " "e.g. what is the weather in San Francisco?",
                },
            },
            "required": ["query"],
        },
    }
]
chain = llm.bind_tools(tools=tools, function_call={"name": "web_search"}, functions=[{"name": web_search}])
res = chain.invoke("what is the weather in Boston?")
print(res)