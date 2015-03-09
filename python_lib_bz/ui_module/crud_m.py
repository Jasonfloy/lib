#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
create by bigzhu at 15/03/08 21:40:01 增删改查统一操作
'''

from ui_module import my_ui_module
from tornado_bz import BaseHandler
import tornado_bz
import json
import public_bz
from webpy_db import SQLLiteral


class CrudOper:

    '''
    对用户相关的操作
    '''

    def __init__(self, pg):
        self.pg = pg

    def getCrudConf(self, table_name, isTime=None):
        sql = '''
        select * from crud_conf where table_name='%s'
        ''' % table_name
        if isTime:
            sql += " and c_type='timestamp' "
        return list(self.pg.db.query(sql))

    def getCrudListConf(self, table_name, isTime=None):
        sql = '''
        select * from crud_conf where table_name='%s' and grid_show=1
        ''' % table_name
        if isTime:
            sql += " and c_type='timestamp' "
        return list(self.pg.db.query(sql))

    def getWhat(self, table_name):
        '''
        create by bigzhu at 15/03/09 14:22:37 查询出配置了哪些字段,用来 select 时候的 what
        '''
        fields = self.getCrudConf(table_name)

        field_list = []
        for field in fields:
            field_list.append(field.name)
        return ','.join(field_list)

    def preparedTimeData(self, table_name, record):
        '''
        取出字段类型是时间的,来加工处理要 insert 的数据
        '''
        # 取出字段是时间类型的
        fields = self.getCrudConf(table_name, True)
        if fields:
            for field in fields:
                record[field.name] = SQLLiteral("to_timestamp(%s)" % record[field.name])
        return record


class crud_m(my_ui_module.MyUIModule):

    '''
    create by bigzhu at 15/03/09 09:37:26 crud 的通用操作页面
    modify by bigzhu at 15/03/09 09:37:45 改用要传参数到 js 里面,因此不用 file 改用embedded 的方式
    '''

    def render(self, table_name):

        pg = self.handler.settings['pg']
        crud_oper = CrudOper(pg)
        fields = crud_oper.getCrudConf(table_name)
        return self.render_string(self.html_name, fields=fields)


class crud_list_m(my_ui_module.MyUIModule):

    '''
    create by bigzhu at 15/03/09 11:17:17 显示 list
    '''

    def render(self, table_name):

        pg = self.handler.settings['pg']
        crud_oper = CrudOper(pg)
        fields = crud_oper.getCrudListConf(table_name)
        return self.render_string(self.html_name, fields=fields)


class crud_list(BaseHandler):
    '''
    crud list 实现
    '''
    def get(self, table_name, id=None):
        if id is None:
            self.render(tornado_bz.getTName(self), table_name=table_name)


class crud_list_api(BaseHandler):

    @tornado_bz.handleError
    def get(self, table_name):
        self.set_header("Content-Type", "application/json")
        cert_array = list(self.pg.db.select(table_name, where="is_delete='f'"))
        self.write(json.dumps({'error': '0', "array": cert_array}, cls=public_bz.ExtEncoder))

    def delete(self, table_name):
        self.set_header("Content-Type", "application/json")
        ids = self.request.body
        self.pg.db.update(table_name, where="id in (%s)" % ids, is_delete=True)
        self.write(json.dumps({'error': '0'}))


class crud(BaseHandler):
    '''
    crud 的实现方法
    '''
    def get(self, table_name, id=None):
        # 新建
        if id is None:
            self.render(tornado_bz.getTName(self), table_name=table_name)

    @tornado_bz.handleError
    def post(self):
        self.set_header("Content-Type", "application/json")
        info = json.loads(self.request.body)
        table_name = info["table_name"]
        id = info["id"]

        crud_oper = CrudOper(self.pg)
        what = crud_oper.getWhat(table_name)

        data = list(self.pg.db.select(table_name, what=what, where="id=%s" % id))

        self.write(json.dumps({'error': '0', 'data': data}, cls=public_bz.ExtEncoder))


class crud_api(BaseHandler):

    @tornado_bz.handleError
    def post(self):
        self.set_header("Content-Type", "application/json")
        info = json.loads(self.request.body)
        table_name = info["table_name"]
        record = info["record"]

        crud_oper = CrudOper(self.pg)
        record = crud_oper.preparedTimeData(table_name, record)

        id = record.get("id")
        if id:
            self.pg.db.update(table_name, where="id=%s" % id, **record)
        else:
            self.pg.db.insert(table_name, **record)

        self.write(json.dumps({'error': '0'}))

if __name__ == '__main__':
    pass
