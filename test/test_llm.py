import os
from langchain_community.chat_models import ChatOllama
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.manager import CallbackManager
from langchain.prompts import BasePromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_message_histories import RedisChatMessageHistory
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from langchain_core.output_parsers import StrOutputParser
from langchain.callbacks import AsyncIteratorCallbackHandler
import json 
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import redis
from langchain_core.callbacks import StdOutCallbackHandler

app = FastAPI()
handler = StdOutCallbackHandler()
llm = ChatOllama(model="llama3.1", callbacks=[handler])
redis_url = "redis://localhost:6379"

def history(session_id, redis_url):
    return RedisChatMessageHistory(session_id, redis_url)

def send_message(query, config):
    chain = RunnableWithMessageHistory(
                llm, 
                lambda session_id: RedisChatMessageHistory(
                    session_id, url=redis_url
                )
    )
    for chunk in chain.stream([HumanMessage(content=query)], config=config):
            print(chunk.content, end="", flush=True)


def start():
    stop = False
    while not stop:
        prompt = input(">>> ")
        config = {"configurable": {"session_id": "3"}}
        send_message(prompt, config)
        if prompt == "stop":
            stop = True
        print()

start()
