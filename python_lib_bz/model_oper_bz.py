#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
create by bigzhu at 15/04/03 17:23:47 初始化数据库
create by bigzhu at 15/04/03 17:23:35 字段映射参见 http://peewee.readthedocs.org/en/latest/peewee/models.html
modify by bigzhu at 15/04/06 20:09:43 修改文件名称为 model_oper_bz.py
modify by bigzhu at 15/04/08 15:05:36 改用 PostgresqlExtDatabase 为了支持 json
'''
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import public_bz
#from peewee import *
from peewee import PostgresqlDatabase
from peewee import Model
from peewee import DateTimeField
from playhouse.postgres_ext import PostgresqlExtDatabase

import peewee


def dropTable(Model, db_name, user=None, password=None):
    '''
    create by bigzhu at 15/04/04 13:12:02 还是需要一个删除表的功能
    '''
    if user is None:
        user = db_name
    if password is None:
        password = db_name
    #db = PostgresqlDatabase(db_name, user=user, password=password, host='127.0.0.1')
    db = PostgresqlExtDatabase(db_name, user=user, password=password, host='127.0.0.1', register_hstore=False)
    Model._meta.database = db
    Model.drop_table()
    print 'drop table ' + Model.__name__


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
    db = PostgresqlExtDatabase(db_name, user=user, password=password, host='127.0.0.1', register_hstore=False)
    Model._meta.database = db
    try:
        if Model.table_exists():
            print 'table %s already exists' % Model.__name__
            return
        createBaseTable(db)
        Model.create_table()
        print 'create table ' + Model.__name__
    except peewee.OperationalError:
        print public_bz.getExpInfo()
        showDBCreate(db_name)
        exit(1)


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


def createAllTable(all_class, db_name):
    #all_class = globals().copy()
    for model in all_class:
        try:
            if issubclass(all_class[model], Model):
                createTable(all_class[model], db_name)
        except Exception:
            continue


class base(Model):
    created_date = DateTimeField(null=True)
    stat_date = DateTimeField(null=True)

if __name__ == '__main__':
    pass
    #createAllTable(pg_db)