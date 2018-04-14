# NoSQL 的基本使用

张文杰 (wenjiez696_at_gmail.com)

## 测试内容

- 批量插入
- 逐个插入
- 按主键删除
- 筛选删除
- 全部删除
- 按主键修改
- 筛选修改
- 全部修改
- 按主键查询属性
- 按条件查询属性
- 遍历

## 运行环境

```
OS: Ubuntu 18.04 Bionic Beaver (development branch)
CPU: Intel(R) Core(TM) i5-5200U CPU @ 2.20GHz
Memory: 8G
```

## 安装与配置

1. Miniconda 安装

```
$ wget https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-4.4.10-Linux-x86_64.sh
$ ./Miniconda3-4.4.10-Linux-x86_64.sh
```

2. 数据库软件安装

```
# echo "deb http://www.apache.org/dist/cassandra/debian 311x main"
# curl https://www.apache.org/dist/cassandra/KEYS | sudo apt-key add -
# sudo apt-key adv --keyserver pool.sks-keyservers.net --recv-key A278B781FE4B2BDA
# apt install redis-server cassandra mongodb
```

3. conda环境配置

```
$ conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
$ conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
$ conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
$ conda config --set show_channel_urls yes
$ conda create -n db
$ conda install pymongo redis-py cassandra-driver -n db
```

## 程序运行

```
$ source activate db
$ python test.py
```

## 运行结果

name     |  I_one  |  I_all  |  D_id   | D_search|  D_all  |  U_id   | U_search|  U_all  |  S_id   | S_search|  S_all
-|-|-|-|-|-|-|-|-|-|-|-
redis    | 0.000000| 0.331573| 0.062058| 0.083081| 0.013847| 0.064913| 0.074324| 0.082713| 0.076591| 0.076914| 0.082175
mongo    | 0.101084| 0.398549| 0.354701| 0.002577| 0.006087| 0.917833| 0.002887| 0.009799| 1.055133| 0.004754| 0.016752
cassandra| 0.917867| 1.094512| 0.737409| 0.110348| 0.107526| 0.800503| 0.121632| 0.859821| 1.722984| 0.021034| 0.022636
