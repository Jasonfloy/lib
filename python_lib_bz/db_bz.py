#!/usr/bin/env python
# -*- coding: utf-8 -*-
import public_bz
import psycopg2
import functools
import time
from webpy_db import SQLLiteral

def daemonDB(method):
    '''
    自动重连数据库的一个装饰器
    '''
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        try:
            return method(self, *args, **kwargs)
        except(psycopg2.OperationalError, psycopg2.InterfaceError):
            print public_bz.getExpInfo()
            self.pg.connect()
            time.sleep(5)
            return wrapper(self, *args, **kwargs)
            print '重新连接数据库'
    return wrapper


def getTableDesc(pg, table_name):
    '''
    create by bigzhu at 15/03/10 10:05:45 查询表的描述
    '''
    sql = '''
        select obj_description('public.%s'::regclass)
    ''' % table_name
    data = pg.db.query(sql)
    if data:
        return data[0].obj_description


def getTableColum(pg, table_name, name=None, just_time=None):
    '''
    获取表的字段名称
    modify by bigzhu at 15/03/11 11:31:48 如果传了 name, 就只取这个 colum, 可以用来检查是否存在
    modify by bigzhu at 15/04/24 14:19:25 可以只查timestamp出来
    '''
    sql = '''
        select format_type(a.atttypid,a.atttypmod) as type,a.attname as name
        from pg_class as c,pg_attribute as a
        where c.relname = '%s' and a.attrelid = c.oid and a.attnum>0 and a.atttypid<>0
    ''' % table_name
    if name:
        sql += " and a.attname='%s'" % name
    if just_time:
        sql += " and format_type(a.atttypid,a.atttypmod)='timestamp without time zone' "
    return list(pg.db.query(sql))


def transTimeValueByTable(pg, table_name, v):
    '''
    create by bigzhu at 15/04/24 14:14:52 为了让time能 insert/update 数据库
    modify by bigzhu at 15/04/24 16:10:51 自动除以1000以应对js
    '''
    time_colums = getTableColum(pg, table_name, just_time=True)
    for time_colum in time_colums:
        name = time_colum.name
        if v.get(name):
            v[name] = SQLLiteral("to_timestamp(%s)" % v[name]/1000)
    return v


if __name__ == '__main__':
    import test_pg as pg
    transValueByTable(pg, 'user_info', 'haha')
