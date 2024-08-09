from typing import List
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.runnables import ConfigurableField
from langchain_core.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_experimental.llms.ollama_functions import OllamaFunctions
from langchain_core.tools import tool
from langchain.schema import Document
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from tavily import TavilyClient
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.retrievers import BaseRetriever
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.runnables.history import RunnableWithMessageHistory
import os
from langchain_community.chat_models import ChatOllama
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
load_dotenv()



def test_1():
    class WebSearch(BaseRetriever):
        q: str
        def _get_relevant_documents(
            self, query: str, *, run_manager: CallbackManagerForRetrieverRun
        ) -> List[Document]:
            """Run web search on the question."""
            try:
                if len(self.q) < 5:
                    return []
                web_results = web_search_tool.invoke({"query": self.q})
                return [
                    Document(page_content=d["content"], metadata={"url": d["url"]})
                    for d in web_results
                ]
            except Exception as e:
                print(e)
                return []



    def messages_hist(session_id):
        history = RedisChatMessageHistory(url=redis_url, key_prefix="", session_id=session_id)
        return history



    retriever = WebSearch(q="What is the weather in SF?")

    contextualize_q_system_prompt = """Given a chat history and the latest user question \
    which might reference context in the chat history, formulate a standalone question \
    which can be understood without the chat history."""

    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )

    ### Answer question ###
    qa_system_prompt = """You are an assistant for question-answering tasks. \
    Use the following pieces of retrieved context to answer the question. \
    If the question is not relevant with the document ignore the document and give a normal \
    response. Do NOT return empty response.

    {context}"""

    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    convo_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        lambda session_id: RedisChatMessageHistory(
                    session_id, url=redis_url
        ),
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )

    config = {"configurable": {"session_id": "vu7"}}

    # for chunk in convo_rag_chain.stream({"input": "What is the weather in SF"}, config=config):
    #     print(chunk, end="")

    res = convo_rag_chain.invoke({"input": "Hi, what's your name"}, config=config)
    print(res["answer"])


############################################################################################################################
web_search_tool = TavilySearchResults(api_key=os.getenv("TAVILY_API_KEY"))
redis_url = "redis://localhost:6379"
llm = ChatOllama(model="llama3.1")
tools = [web_search_tool]
prompt = """
You run in a loop of Thought, Action, Pause, Observation.
At the end of the loop you will output an Answer.
Use Thought to describe your thoughts about a question you have been asked.
Use Action to run one of the action available to you then STOP AND RETURN.
Observation will be provided after the result of the output action.

Your available actions are:

web_search(query):
e.g. web_search("Current weather in San Francisco")
return search result of the query.

Follow the format below:

Example:
Question: What is the elevation range for the area that the eastern sector of the Colorado orogeny extends into?
Thought: I need to search Colorado orogeny, find the area that the eastern sector of the Colorado orogeny extends into, then find the elevation range of the area.
Action: web_search(Colorado orogeny)
STOP AND RETURN

Observation: The Colorado orogeny was an episode of mountain building (an orogeny) in Colorado and surrounding areas.
Thought: It does not mention the eastern sector. So I need to look up eastern sector.
Action: web_search(Colorado orogeny)
STOP AND RETURN

Observation: (Result 1 / 1) The eastern sector extends into the High Plains and is called the Central Plains orogeny.
Thought: The eastern sector of Colorado orogeny extends into the High Plains. So I need to search High Plains and find its elevation range.
Action: web_search(Colorado orogeny)
STOP AND RETURN

Observation: High Plains refers to one of two distinct land regions
Thought: I need to instead search High Plains (United States).
Action: web_search(Colorado orogeny)
STOP AND RETURN

Observation: The High Plains are a subregion of the Great Plains. From east to west, the High Plains rise in elevation from around 1,800 to 7,000 ft (550 to 2,130 m).[3]
Thought: High Plains rise in elevation from around 1,800 to 7,000 ft, so the answer is 1,800 to 7,000 ft.
Action: Finish[1,800 to 7,000 ft]
STOP AND RETURN
"""


config = {"configurable": {"session_id": "vu200"}}

def web_search(q):
    try:
        if len(q) < 5:
            return []
        web_results = web_search_tool.invoke({"query": q})
        return [
            Document(page_content=d["content"], metadata={"url": d["url"]})
            for d in web_results
        ]
    except Exception as e:
        print(e)
        return []


class Agent:
    def __init__(self, system="") -> None:
        self.system = system
        self.messages = []
        if self.system:
            self.messages.append(SystemMessage(content=system))

    def invoke(self, message):
        self.messages.append(HumanMessage(content=message))
        result = self.execute()
        self.messages.append(SystemMessage(content=result))
        return result
    
    def execute(self):
        ...









# agent = create_react_agent(llm, tools, prompt)
# agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
# agent_with_chat_history = RunnableWithMessageHistory(
#     agent_executor,
#     lambda session_id: RedisChatMessageHistory(
#                 session_id, url=redis_url
#     ),
#     input_messages_key="input",
#     history_messages_key="chat_history"
# )
