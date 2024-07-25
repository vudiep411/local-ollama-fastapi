# from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
# from langchain.callbacks.manager import CallbackManager
# from langchain.prompts import BasePromptTemplate
# import os
# from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOllama
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_message_histories import RedisChatMessageHistory
from fastapi import FastAPI
from langchain.callbacks import AsyncIteratorCallbackHandler
import redis
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:3000",
    # Add other origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


callback_manager = AsyncIteratorCallbackHandler()
# system_prompt = """
# <|begin_of_text|><|start_header_id|>system<|end_header_id|>

# Environment: ipython
# Tools: brave_search, wolfram_alpha

# Cutting Knowledge Date: December 2023
# Today Date: 23 Jul 2024

# You are a helpful assistant<|eot_id|>
# <|start_header_id|>user<|end_header_id|>

# What is the current weather in Menlo Park, California?<|eot_id|><|start_header_id|>assistant<|end_header_id|>
# """
llm = ChatOllama(model="llama3.1")
redis_url = "redis://localhost:6379"

# Models
class Message(BaseModel):
    content: str
    session_id: str
    user_id: str

class DeleteMessageRequest(BaseModel):
    user_id: str
    session_id: str

# Calling LLM streaming function
async def send_message(query, config):
    try:
        chain = RunnableWithMessageHistory(
            llm, 
            lambda session_id: RedisChatMessageHistory(
                session_id, url=redis_url
            )
        )
        async for chunk in chain.astream([HumanMessage(content=query)], config=config):
            yield chunk.content
    except Exception as e:
        print(e)

# Get langchain redis message history
def history(session_id, redis_url):
    return RedisChatMessageHistory(session_id, redis_url)

async def save_user_session(user_id, session_id, message):
    r = redis.Redis.from_url(redis_url, decode_responses=True)
    r.hset(user_id, session_id, message)


# Endpoints
"""Stream the text generation from llm"""
@app.post("/stream_chat")
async def stream_chat(message: Message):
    config = {"configurable": {"session_id": message.session_id}}
    await save_user_session(message.user_id, message.session_id, message.content)
    generator = send_message(message.content, config)
    return StreamingResponse(generator, media_type="text/event-stream")


"""Get all messages from the session"""
@app.get("/messages/{session_id}")
def get_session_messages(session_id: str):
    messages = history(session_id, redis_url)
    res = []
    for msg in messages.messages:
        res.append({ "role": msg.type, "content": msg.content })
    return res


"""Get all sessions from a user's id"""
@app.get("/sessions/{user_id}")
def get_user_sessions(user_id: str):
    r = redis.Redis.from_url(redis_url, decode_responses=True)
    res = r.hgetall(user_id)
    return res


"""Delete messages from a session"""
@app.delete("/session")
async def delete_session(user: DeleteMessageRequest):
    messages = history(user.session_id, redis_url)
    await messages.aclear()
    r = redis.Redis.from_url(redis_url, decode_responses=True)
    r.srem(user.user_id, user.session_id)
    return {"session_id": user.session_id}



