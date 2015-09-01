from redis import StrictRedis
redis = StrictRedis()
import arrow
import random
import time
import itertools as it

redis.flushdb()
N = 10000
randtime = lambda: arrow.now().replace(minutes=random.random()*N)
times = [randtime().timestamp for i in range(N)]
ips = ["127.1.2.{}".format(i) for i in range(N)]
data = list(it.chain(*zip(times, ips)))

print "Adding 10,000 keys"
redis.zadd("lds:shf", *data)
print "Added 10,000 keys"

# This is fucking lovely
t1 = arrow.now().replace(hours=-1).timestamp
t2 = arrow.now().replace(hours=200).timestamp
#ips = len(redis.zrangebyscore("lds:shf", t1, t2))

t = time.clock()
print "Found {} keys in a 100 hour interval".format(redis.zcount("lds:shf", t1, t2))
print time.clock()-t
