#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
create by bigzhu at 15/02/22 12:32:08 主要是用来测试
'''

import sys
import psycopg2
import time
reload(sys)
sys.setdefaultencoding('utf-8')
import webpy_db
import public_bz


db_ip = '0.0.0.0'
db_name= ''
db_user='yemai'
db_pw = 'yemai'
db = None


def daemonDB(f):
    def new_f(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except(psycopg2.OperationalError, psycopg2.InterfaceError):
            print public_bz.getExpInfo()
            connect()
            time.sleep(10)
            new_f(*args, **kwargs)
            print '重新连接数据库'
    return new_f


@daemonDB
def query(sql):
    return list(db.query(sql))


def connect():
    global db
    db = webpy_db.database(
        port=5432,
        host=db_ip,
        dbn='postgres',
        db=db_name,
        user=db_user,
        pw=db_pw)
    print '开始连接数据库 %s' % db_ip


connect()


if __name__ == '__main__':
    pass
