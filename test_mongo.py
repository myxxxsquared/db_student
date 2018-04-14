
# Copyright (C) 2018 Wenjie Zhang (https://github.com/myxxxsquared) - All Rights Reserved

import dataloader
from utils import emptyshell, timer
import pymongo
from pymongo import MongoClient
import copy


def test_mongo(data, result):
    client = MongoClient()
    db = client.test
    student = db.student
    student.delete_many({})
    student.insert_many(copy.deepcopy(data))
    student.delete_many({})
    t = timer()

    # insert all (not supported for redis)
    t.tic()
    student.insert_many(copy.deepcopy(data))
    t.toc(result)

    student.delete_many({})

    # insert one by one
    t.tic()
    for item in data:
        student.insert_one(copy.deepcopy(item))
    t.toc(result)

    # delete by id
    t.tic()
    for item in data:
        student.delete_one({'id': item['id']})
    t.toc(result)

    student.insert_many(copy.deepcopy(data))

    # delete by value
    t.tic()
    student.delete_many({'schoolsup': 'yes'})
    t.toc(result)

    # delete all
    t.tic()
    student.delete_many({})
    t.toc(result)

    student.insert_many(copy.deepcopy(data))

    # modify by id
    t.tic()
    for item in data:
        student.update_one({'id': item['id']}, {'$set': {'reason': 'other'}})
    t.toc(result)

    # modify by item
    t.tic()
    student.update_many({'schoolsup': 'yes'}, {'$set': {'age': 15}})
    t.toc(result)

    # modify all
    t.tic()
    student.update_many({}, {'$set': {'age': 16}})
    t.toc(result)

    # search by id
    t.tic()
    for item in data:
        item = student.find_one({'id': item['id']})
        _ = item['famsize']
    t.toc(result)

    # search by value
    t.tic()
    it = student.find({'schoolsup': 'yes'})
    for i in it:
        _ = i['famsize']
    t.toc(result)

    # search all
    t.tic()
    it = student.find({})
    for i in it:
        _ = i['famsize']
    t.toc(result)

    student.delete_many({})

if __name__ == '__main__':
    data = dataloader.loaddata()
    result = []
    test_mongo(data, result)
    assert len(result) == 11
    print(result)
