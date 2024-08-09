import redis
from langchain_community.chat_message_histories import RedisChatMessageHistory


r = redis.Redis(host='localhost', port=6379, decode_responses=True)
redis_url = "redis://localhost:6379"
def test_redis():
    for k in r.scan_iter():
        print(k)

def print_session_messages(session_id):
     print(r.lrange(session_id, 0, -1))

def delete_key(key):
    r.delete(key)

def history(session_id, redis_url):
    return RedisChatMessageHistory(session_id, redis_url)

hst = history("vu100", redis_url)
for msg in hst.messages:
    print(f"{msg.type}: {msg.content}")