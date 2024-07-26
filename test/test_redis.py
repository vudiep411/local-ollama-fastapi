import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)
def test_redis():
    for k in r.scan_iter():
        print(k)

def print_session_messages(session_id):
     print(r.lrange(session_id, 0, -1))

def delete_key(key):
    r.delete(key)

delete_key("message_store:3")
delete_key("message_store:2")
test_redis()
print_session_messages("message_store:1")