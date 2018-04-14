
# Copyright (C) 2018 Wenjie Zhang (https://github.com/myxxxsquared) - All Rights Reserved

import csv

def process_data(data):
    return {k: v[1:-1] if v.startswith('"') and v.endswith('"') else int(v) for k, v in data.items()}

def loaddata():
    file = open('data/student.csv')
    file = csv.DictReader(file, delimiter=';', quotechar=None, quoting=csv.QUOTE_NONE)
    file = list(map(process_data, file))
    return file

if __name__ == '__main__':
    data = loaddata()
    for v in data:
        print(v['id'])
