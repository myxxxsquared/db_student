
# Copyright (C) 2018 Wenjie Zhang (https://github.com/myxxxsquared) - All Rights Reserved

import dataloader
from utils import emptyshell, timer

from cassandra.cluster import Cluster  # pylint: disable=E0611


def test_cassandra(data, result):
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()
    session.execute(
        "create keyspace if not exists test with replication={'class':'SimpleStrategy', 'replication_factor': 1}")
    session.execute('use test')
    names = ['id varchar primary key']
    for k, v in data[0].items():
        if k != 'id':
            names.append('{} {}'.format(
                k, 'int' if isinstance(v, int) else 'varchar'))
    session.execute(
        'create table if not exists student ({})'.format(', '.join(names)))
    session.execute('truncate student')

    insertstr = 'insert into student ({}) values ({})'.format(', '.join(data[0].keys()), ', '.join(
        ['%s'] * len(data[0])
    ))
    insertprestr = 'insert into student ({}) values ({})'.format(', '.join(data[0].keys()), ', '.join(
        ['?'] * len(data[0])
    ))
    insertstat = session.prepare(insertprestr)
    for item in data:
        session.execute(insertstat, tuple(item.values()))
    session.execute('truncate student')

    t = timer()

    # insert all (not supported for redis)
    t.tic()
    for item in data:
        session.execute(insertstat, tuple(item.values()))
    t.toc(result)

    session.execute('truncate student')

    # insert one by one
    t.tic()
    for item in data:
        session.execute(insertstr, tuple(item.values()))
    t.toc(result)

    # delete by id
    t.tic()
    for item in data:
        session.execute('delete from student where id = %s', (item['id'],))
    t.toc(result)

    for item in data:
        session.execute(insertstat, tuple(item.values()))

    # delete by value
    t.tic()
    rows = session.execute("select id, schoolsup from student")
    delprepare = session.prepare("delete from student where id = ?")
    for i, s in rows:
        if s == 'yes':
            session.execute(delprepare, (i,))
    t.toc(result)

    # delete all
    t.tic()
    session.execute('truncate student')
    t.toc(result)

    for item in data:
        session.execute(insertstat, tuple(item.values()))

    # modify by id
    t.tic()
    for item in data:
        session.execute(
            "update student set reason='other' where id = %s", (item['id'],))
    t.toc(result)

    # modify by item
    t.tic()
    rows = session.execute("select id, schoolsup from student")
    modprepare = session.prepare("update student set age=15 where id = ?")
    for i, s in rows:
        if s == 'yes':
            session.execute(modprepare, (i,))
    t.toc(result)

    # modify all
    t.tic()
    rows = session.execute("select id from student")
    modprepare = session.prepare("update student set age=16 where id = ?")
    for (i,) in rows:
        session.execute(modprepare, (i,))
    t.toc(result)

    # search by id
    t.tic()
    for item in data:
        rows = session.execute(
            "select famsize from student where id = %s", (item['id'],))
        for (i,) in rows:
            pass
    t.toc(result)

    # search by value
    t.tic()
    rows = session.execute("select schoolsup, famsize from student")
    for s, i in rows:
        if s == 'yes':
            _ = i
    t.toc(result)

    # search all
    t.tic()
    rows = session.execute("select famsize from student")
    for (i,) in rows:
        pass
    t.toc(result)

    session.execute('truncate student')
    session.execute('drop table student')


if __name__ == '__main__':
    data = dataloader.loaddata()
    result = []
    test_cassandra(data, result)
    assert len(result) == 11
    print(result)
