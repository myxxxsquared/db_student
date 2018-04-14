
# Copyright (C) 2018 Wenjie Zhang (https://github.com/myxxxsquared) - All Rights Reserved

import redis
import dataloader
import itertools
from utils import timer, emptyshell


def test_redis(data, result):
    r = redis.Redis()
    r.flushall()
    for item in data:
        i = item['id']
        r.hmset(i, item)
    r.delete(*[item['id'] for item in data])
    r.flushall()
    t = timer()

    # insert all (not supported for redis)
    t.toc(result)

    # insert one by one
    t.tic()
    for item in data:
        i = item['id']
        r.hmset(i, item)
    t.toc(result)

    # delete by id
    t.tic()
    for item in data:
        r.delete(item['id'])
    t.toc(result)

    for item in data:
        i = item['id']
        r.hmset(i, item)

    # delete by value
    t.tic()
    keys = r.keys()
    for key in keys:
        if r.hmget(key, ['schoolsup'])[0] == b'yes':
            r.delete(key)
    t.toc(result)

    # delete all
    t.tic()
    r.flushall()
    t.toc(result)

    for item in data:
        i = item['id']
        r.hmset(i, item)

    # modify by id
    t.tic()
    for item in data:
        r.hmset(item['id'], {'reason': 'other'})
    t.toc(result)

    # modify by item
    t.tic()
    keys = r.keys()
    for key in keys:
        if r.hmget(key, 'schoolsup') == b'yes':
            r.hmset(key, {'age': 15})
    t.toc(result)

    # modify all
    t.tic()
    keys = r.keys()
    for key in keys:
        if r.hmget(key, 'schoolsup') == b'yes':
            r.hmset(key, {'age': 16})
    t.toc(result)

    # search by id
    t.tic()
    for item in data:
        r.hmget(item['id'], ['famsize'])
    t.toc(result)

    # search by value
    t.tic()
    for key in keys:
        if r.hmget(key, 'schoolsup') == b'yes':
            r.hmget(key, 'famsize')
    t.toc(result)

    # search all
    t.tic()
    keys = r.keys()
    for key in keys:
        r.hmget(key, 'famsize')
    t.toc(result)

    r.flushall()


if __name__ == '__main__':
    data = dataloader.loaddata()
    result = []
    test_redis(data, result)
    assert len(result) == 11
    print(result)
