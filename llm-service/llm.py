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

app = FastAPI()

callback_manager = AsyncIteratorCallbackHandler()
llm = ChatOllama(model="llama3")
redis_url = "redis://localhost:6379"

# Models
class Message(BaseModel):
    content: str
    session_id: str
    user_id: str

class DeleteMessageRequest(BaseModel):
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

async def save_user_session(user_id, session_id):
    r = redis.Redis.from_url(redis_url, decode_responses=True)
    r.sadd(user_id, session_id)


# Endpoints
"""Stream the text generation from llm"""
@app.post("/stream_chat")
async def stream_chat(message: Message):
    config = {"configurable": {"session_id": message.session_id}}
    await save_user_session(message.user_id, message.session_id)
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
    res = r.smembers(user_id)
    return {user_id: res}


"""Delete messages from a session"""
@app.delete("/session")
async def delete_session(session_id: DeleteMessageRequest):
    messages = history(session_id.session_id, redis_url)
    await messages.aclear()
    return {"session_id": session_id.session_id}



