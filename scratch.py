from redis import StrictRedis
redis = StrictRedis()
import arrow
import random
import time
import itertools as it

redis.flushdb()
randtime = lambda: arrow.now().replace(minutes=random.random()*N)
times = [randtime().timestamp for i in range(N)]
ips = ["127.1.2.{}".format(i) for i in range(N)]
data = list(it.chain(*zip(times, ips)))

t = time.clock()
redis.zadd("lds:shf", *data)
print "Added {} keys in {}ms".format(N, (time.clock()-t)*1000)
print redis.zcard("lds:shf")

# Time interval
t1 = arrow.now().replace(hours=-1).timestamp
t2 = arrow.now().replace(hours=200).timestamp

# Oh yeah baby
t = time.clock()
redis.zremrangebyscore("lds:shf", 0, t2)
print redis.zcard("lds:shf")
print "Deleted {} keys deemed to be too old in {}ms".format(N, (time.clock()-t)*1000)
redis.zadd("lds:shf", *data)
print redis.zcard("lds:shf")
print "Replaced those {} keys".format(N)

t = time.clock()
print "Found {} keys in a given interval".format(redis.zcount("lds:shf", t1, t2))
print "Time elapsed was {}ms".format((time.clock()-t)*1000)

