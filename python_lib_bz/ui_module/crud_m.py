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


class CrudOper:

    '''
    对用户相关的操作
    '''

    def __init__(self, pg):
        self.pg = pg

    def getCrudConf(self, table_name):
        sql = '''
        select * from crud_conf where table_name='%s'
        ''' % table_name
        return list(self.pg.db.query(sql))


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
        fields = crud_oper.getCrudConf(table_name)
        return self.render_string(self.html_name, fields=fields)


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
        record = info["record"]
        id = record.get("id")
        if id:
            self.pg.db.update(table_name, where="id=%s" % id, **record)
        else:
            self.pg.db.insert(table_name, **record)

        self.write(json.dumps({'error': '0'}))


class crud_query(BaseHandler):

    @tornado_bz.handleError
    def post(self):
        self.set_header("Content-Type", "application/json")
        info = json.loads(self.request.body)
        table_name = info["table_name"]
        id = info["id"]

        what = self.pg.db.select('crud_conf', what='name', where="table_name='%s'" % table_name)
        l = []
        for i in what:
            l.append(i.name)

        data = list(self.pg.db.select(table_name, what=','.join(l), where="id=%s" % id))
        print data

        self.write(json.dumps({'error': '0', 'data': data}, cls=public_bz.ExtEncoder))
if __name__ == '__main__':
    pass
