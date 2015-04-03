#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
create by bigzhu at 15/04/03 17:23:47 初始化数据库
create by bigzhu at 15/04/03 17:23:35 字段映射参见 http://peewee.readthedocs.org/en/latest/peewee/models.html
'''
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import datetime
import public_bz
from peewee import *
import peewee

def createTable(Model, db_name, user=None, password=None):
    '''
    create by bigzhu at 15/04/04 01:08:30 建立数据库表; peewee 要在定义时候指定 db 相当不人性化,修正
    modify by bigzhu at 15/04/04 01:32:46 没有这个数据库的时候,直接返回建立数据的语句
    modify by bigzhu at 15/04/04 01:45:43 如果表已经存在,不能往下继续了
    '''
    if user is None:
        user = db_name
    if password is None:
        password = db_name
    db = PostgresqlDatabase(db_name, user=user, password=password)
    Model._meta.database = db
    try:
        if Model.table_exists():
            print 'table %s already exists' % Model.__name__
            return
        createBaseTable(db)
        Model.create_table()
    except peewee.OperationalError:
        print public_bz.getExpInfo()
        showDBCreate(db_name)
        return
    table_name = Model.__name__
    if table_name != 'base':
        sql = '''
            alter table %s inherit base;
            ''' % table_name
        db.execute_sql(sql)
        resetBaseDefault(db)


def resetBaseDefault(db):
    '''
    create by bigzhu at 15/04/04 01:25:45 强制重新设置的 base 的 default, 保证新建立的表也是 default
    '''
    sql = '''
        alter table base
           alter column created_date set default now();
        alter table base
           alter column stat_date set default now();
    '''
    db.execute_sql(sql)


def showDBCreate(db_name):
    '''
    create by bigzhu at 15/04/04 01:20:33 根据名字拼装出建立数据库及用户的语句
    '''
    sql = '''
        create role %s login encrypted password '%s' noinherit valid until 'infinity';
        create database %s with encoding='utf8' owner=%s;
    ''' % (db_name, db_name, db_name, db_name)
    print sql


def createBaseTable(db):
    '''
    create by bigzhu at 15/04/04 01:39:26 建立 base 表
    '''
    base._meta.database = db
    base.create_table(True)


class base(Model):
    created_date = DateTimeField(null=True)
    stat_date = DateTimeField(null=True)

if __name__ == '__main__':
    createAllTable(pg_db)
