import redis
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
import json
import requests


def test_chunk_stream():
    url = "http://127.0.0.1:8000/stream_chat"
    prompt = input(">>> ")
    data = {"content": prompt, "session_id": "test", "user_id": "vudiep411"}
    headers = {"Content-type": "application/json"}

    with requests.post(url, data=json.dumps(data), headers=headers, stream=True) as r:
        for chunk in r.iter_content(decode_unicode='utf-8'):
            print(chunk, end="")
    print()

def test_redis():
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    print(r.get("idv2"))


def main():
    test_chunk_stream()


if __name__ == '__main__':
    main()
