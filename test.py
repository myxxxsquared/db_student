
# Copyright (C) 2018 Wenjie Zhang (https://github.com/myxxxsquared) - All Rights Reserved

from dataloader import loaddata
from test_redis import test_redis
from test_mongo import test_mongo
from test_cassandra import test_cassandra

import copy


def test(data, func, name):
    result = []
    func(copy.deepcopy(data), result)
    print("\033[94m{}\033[0m: {}".format(name, ', '.join(
        map(lambda x: '{:08.06f}'.format(x), result))))


def main():
    data = loaddata()

    print("\033[94mname     \033[0m:  I_one  ,  I_all  ,  D_id   , D_search,  D_all  ,  U_id   , U_search,  U_all  ,  S_id   , S_search,  S_all  ")

    test(data, test_redis, 'redis    ')
    test(data, test_mongo, 'mongo    ')
    test(data, test_cassandra, 'cassandra')


if __name__ == '__main__':
    main()
