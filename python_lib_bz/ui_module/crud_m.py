#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
create by bigzhu at 15/03/08 21:40:01 增删改查统一操作
'''

from ui_module import my_ui_module
from tornado_bz import BaseHandler
from tornado_bz import ModuleHandler
import tornado_bz
import json
import public_bz
from webpy_db import SQLLiteral
import db_bz


class CrudOper:

    '''
    对用户相关的操作
    '''

    def __init__(self, pg):
        self.pg = pg

    def getCrudConf(self, table_name, isTime=None):
        sql = '''
        select * from crud_conf where table_name='%s' and is_delete != 't'
        ''' % table_name
        if isTime:
            sql += " and c_type='timestamp' "
        sql += " order by seq desc, create_date"
        return list(self.pg.db.query(sql))

    def getCrudListConf(self, table_name, isTime=None):
        sql = '''
        select * from crud_conf where table_name='%s' and grid_show=1 and is_delete != 't'
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
        fields = self.getCrudConf(table_name, isTime=True)
        if fields:
            for field in fields:
                # 判断是否传了空的过来
                if record[field.name] is None or record[field.name] == '':
                    record[field.name] = SQLLiteral("null")
                else:
                    record[field.name] = float(record[field.name]) / 1000
                    record[field.name] = SQLLiteral("to_timestamp(%s)" % record[field.name])
        return record


class crud_m(my_ui_module.MyUIModule):

    '''
    create by bigzhu at 15/03/09 09:37:26 crud 的通用操作页面
    modify by bigzhu at 15/03/09 09:37:45 改用要传参数到 js 里面,因此不用 file 改用embedded 的方式
    '''

    def render(self, table_name):

        crud_oper = CrudOper(self.pg)
        fields = crud_oper.getCrudConf(table_name)
        return self.render_string(self.html_name, fields=fields)

    def css_files(self):
        return ''


class crud_list_m(my_ui_module.MyUIModule):

    '''
    create by bigzhu at 15/03/09 11:17:17 显示 list
    '''

    def render(self, table_name):

        crud_oper = CrudOper(self.pg)
        fields = crud_oper.getCrudListConf(table_name)
        table_desc = db_bz.getTableDesc(self.pg, table_name)
        return self.render_string(self.html_name, fields=fields, table_desc=table_desc)

    def css_files(self):
        return ''


class crud_list(ModuleHandler):

    '''
    crud list 实现
    '''

    def get(self, table_name, id=None):
        if id is None:
            self.myRender(table_name=table_name)


class crud_list_api(BaseHandler):

    @tornado_bz.handleError
    def get(self, table_name):
        self.set_header("Content-Type", "application/json")
        cert_array = list(self.pg.db.select(table_name, where="is_delete='f'", order="stat_date desc"))
        self.write(json.dumps({'error': '0', "array": cert_array}, cls=public_bz.ExtEncoder))

    def delete(self, table_name):
        self.set_header("Content-Type", "application/json")
        ids = self.request.body
        self.pg.db.update(table_name, where="id in (%s)" % ids, is_delete=True)
        self.write(json.dumps({'error': '0'}))


class crud(ModuleHandler):

    '''
    modify by bigzhu at 15/03/10 11:41:35 自行实现myRender,否则就会报错.
    crud 的实现方法
    '''
    def get(self, table_name):
        # 新建
        self.myRender(table_name=table_name)

    @tornado_bz.handleError
    def post(self):
        '''
        modify by bigzhu at 15/03/10 12:50:39 如果没有 id, 就只是查出 table_desc 返回去
        '''
        self.set_header("Content-Type", "application/json")
        info = json.loads(self.request.body)
        table_name = info["table_name"]
        id = info.get("id")
        data = []
        if id:
            crud_oper = CrudOper(self.pg)
            what = crud_oper.getWhat(table_name)

            data = list(self.pg.db.select(table_name, what=what, where="id=%s" % id))

        table_desc = db_bz.getTableDesc(self.pg, table_name)
        self.write(json.dumps({'error': '0', 'data': data, 'table_desc': table_desc}, cls=public_bz.ExtEncoder))


class crud_api(BaseHandler):
    '''
    modify by bigzhu at 15/03/10 15:56:15 update 时候也要更新 stat_date
    '''

    @tornado_bz.handleError
    def post(self):
        self.set_header("Content-Type", "application/json")
        info = json.loads(self.request.body)
        table_name = info["table_name"]
        record = info["record"]
        # 对于配置表自身的配置要做特殊处理
        if table_name.lower() == 'crud_conf':
            name = record['name']
            target_table_name = record['table_name']
            table_colums = db_bz.getTableColum(self.pg, target_table_name, name)
            if table_colums:
                pass
            else:
                raise Exception('%s表中没有字段%s' % (target_table_name, name))
        crud_oper = CrudOper(self.pg)
        record = crud_oper.preparedTimeData(table_name, record)

        id = record.get("id")
        if id:
            record['stat_date'] = SQLLiteral('now()')
            self.pg.db.update(table_name, where="id=%s" % id, **record)
        else:
            self.pg.db.insert(table_name, **record)

        self.write(json.dumps({'error': '0'}))

if __name__ == '__main__':
    pass
