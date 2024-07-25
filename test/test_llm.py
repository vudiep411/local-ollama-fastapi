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

app = FastAPI()
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
llm = ChatOllama(model="llama3.1", callbacks=callback_manager)
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
    chain.invoke(
        [HumanMessage(content=query)],
        config=config
    )

stop = False
while not stop:
    prompt = input(">>> ")
    config = {"configurable": {"session_id": "1"}}
    send_message(prompt, config)
    if prompt == "stop":
        stop = True
    print()

