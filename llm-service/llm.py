from langchain_community.chat_models import ChatOllama
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_message_histories import RedisChatMessageHistory
from fastapi import FastAPI
import redis
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from langchain.schema import Document
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
# from langchain_community.tools.tavily_search import TavilySearchResults
# from dotenv import load_dotenv

# load_dotenv()
# web_search_tool = TavilySearchResults()


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
    key_type = r.type(user.user_id)
    # Delete key based on its type
    if key_type == 'set':
        r.srem(user.user_id, user.session_id)
    elif key_type == 'hash':
        r.hdel(user.user_id, user.session_id)
    elif key_type == 'list':
        r.lrem(user.user_id, 0, user.session_id)
    elif key_type == 'zset':
        r.zrem(user.user_id, user.session_id)
    else:
        return {"error": "Unsupported key type or key does not exist"}
    return {"session_id": user.session_id}



