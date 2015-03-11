#!/usr/bin/env python
# -*- coding: utf-8 -*-
import public_bz
import psycopg2
import functools
import time


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
    '''%table_name
    data = pg.db.query(sql)
    if data:
        return data[0].obj_description

def getTableColum(pg, table_name, name=None):
    '''
    获取表的字段名称
    modify by bigzhu at 15/03/11 11:31:48 如果传了 name, 就只取这个 colum, 可以用来检查是否存在
    '''
    sql = '''
        select format_type(a.atttypid,a.atttypmod) as type,a.attname as name
        from pg_class as c,pg_attribute as a
        where c.relname = '%s' and a.attrelid = c.oid and a.attnum>0 and a.atttypid<>0
    ''' % table_name
    if name:
        sql += " and a.attname='%s'" % name
    return list(pg.db.query(sql))

if __name__ == '__main__':
    pass
