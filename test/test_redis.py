import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)
def test_redis():
    for k in r.scan_iter():
        print(k)

def print_session_messages(session_id):
     print(r.lrange(session_id, 0, -1))

def delete_key(key):
    r.delete(key)

test_redis()
