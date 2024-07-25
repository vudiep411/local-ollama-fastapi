import redis

def test_redis():
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    # for k in r.scan_iter():
    #     print(k)
    print(r.lrange("message_store:c1d61fc1-2cce-4b14-81c6-491203275c4f", 0, -1))

test_redis()