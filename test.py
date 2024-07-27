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
from tavily import TavilyClient
import os

load_dotenv()

web_search_tool = TavilySearchResults(api_key=os.getenv("TAVILY_API_KEY"))

llm = OllamaFunctions(model="llama3.1", format="json")
prompt = ChatPromptTemplate.from_template("You are a helpful assistant tasked with answering user questions. "
            "You have access to one: web_search."
            "For any other questions, such as questions about current events, use the web_search tool to get information from the web."
            "{topic}"
            )


@tool
def web_search(query: str) -> str:
    """Run web search on the question."""
    try:
        web_results = web_search_tool.invoke({"query": query})
        print(web_results)
        return [
            Document(page_content=d["content"], metadata={"url": d["url"]})
            for d in web_results
        ]
    except:
        print("No search needed")
        return []
print(web_search("Hi"))
# print(web_search("Who is Leo Messi"))