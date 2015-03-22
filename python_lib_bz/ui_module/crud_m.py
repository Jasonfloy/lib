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

    def analysisSqlParm(self, sql_parm):
        '''
        create by bigzhu at 15/03/12 13:09:28 分析 sql_parm, 拆离出参数
        '''
        parm = sql_parm.split(',')
        what = parm[0]
        table_name = parm[1]
        if len(parm) == 3:
            where = parm[2]
        else:
            where = None
        return what, table_name, where

    def getOptions(self, sql_parm):
        '''
        create by bigzhu at 15/03/12 11:16:38 查询 options, 有两种方式:
            1 从配置表的 json 取出(这个不用做什么)
            2 从配置的 sql 取出: what as text,table,where
            优先 2
        '''
        if sql_parm:
            what, table_name, where = self.analysisSqlParm(sql_parm)
            what = "id as value," + what + " as text"
            options = list(self.pg.db.select(table_name, what=what, where=where))
            return options

    def getCrudConf(self, table_name, isTime=None):
        sql = '''
        select * from crud_conf where table_name='%s' and is_delete != 't'
        ''' % table_name
        if isTime:
            sql += " and c_type='timestamp' "
        sql += " order by seq desc, create_date"
        curd_confs = list(self.pg.db.query(sql))
        # 处理 Options
        for curd_conf in curd_confs:
            if curd_conf.sql_parm:
                print curd_conf.sql_parm
                curd_conf.options = self.getOptions(curd_conf.sql_parm)
        return curd_confs

    def getFileUploadCoulumn(self, table_name):
        sql = '''
        select name
        from crud_conf
        where table_name='three_post_cert'
            and is_delete != 't'
            and c_type='input-file'
            and table_name='%s'
        order by seq desc, create_date
        ''' % table_name
        return list(self.pg.db.query(sql))

    def getCrudListConf(self, table_name, isTime=None):
        sql = '''
        select * from crud_conf where table_name='%s' and grid_show=1 and is_delete != 't'
        ''' % table_name
        if isTime:
            sql += " and c_type='timestamp' "
        sql += " order by seq desc, create_date"
        return list(self.pg.db.query(sql))

    def getWhat(self, table_name, prefix=None):
        '''
        modify by bigzhu at 15/03/12 17:37:21 增加获取字段的前缀,用于组合查询区分是 a 表还是 b 表
        create by bigzhu at 15/03/09 14:22:37 查询出配置了哪些字段,用来 select 时候的 what
        '''
        fields = self.getCrudConf(table_name)

        field_list = []
        for field in fields:
            if prefix:
                field_list.append(prefix + field.name)
            else:
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
                if record.get(field.name) is None or record[field.name] == '':
                    record[field.name] = SQLLiteral("null")
                else:
                    record[field.name] = float(record[field.name]) / 1000
                    record[field.name] = SQLLiteral("to_timestamp(%s)" % record[field.name])
        return record

    def joinCrudListSql(self, table_name, sql, colum_name, sql_parm):
        '''
        create by bigzhu at 15/03/12 13:33:31 根据给定的条件迭代join组合出查询 list 的 sql
            sql:上一次迭代的 sql
            colum_name:配置了外键的字段名称
            sql_parm:配置的外键的sql 参数
        '''
        b_what, b_table_name, b_where = self.analysisSqlParm(sql_parm)
        # b 表默认查出 id, 并且让 name 字段和 a 表的 id 字段名字一样
        b_sql = '''
            select id, %s as %s from %s
        ''' % (b_what, colum_name,  b_table_name)
        if b_where:
            b_sql += ' where %s' % b_where

        # 组合 join
        what = self.getWhat(table_name, 'a.')
        # 剔除 a 表中和colum_name一样的字段查询...避免嵌套 sql 查询时候报不确定查哪个字段的错误
        what = what.replace(',a.' + colum_name, '')
        sql = '''
            select %s, b.%s, a.id from
                (%s) a
                    left join
                (%s) b
        on a.%s=b.id
        ''' % (what, colum_name, sql, b_sql, colum_name)
        return sql

    def getCrudListSql(self, table_name):
        '''
        modify by bigzhu at 15/03/12 13:57:43 需要添加 id
        create by bigzhu at 15/03/12 12:56:43 根据给定的条件组合出查询 list 的 sql
        '''
        what = self.getWhat(table_name)
        where = "is_delete='f'"
        order = "stat_date desc"
        sql = '''
            select %s,id from %s where %s order by %s
        ''' % (what, table_name, where, order)
        return sql


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
        if table_desc is None:
            raise Exception("需要设定修改维护的系统(biao)的说明")
        return self.render_string(self.html_name, fields=fields, table_desc=table_desc)

    def css_files(self):
        return ''


class crud_list(ModuleHandler):

    '''
    crud list 实现
    '''

    def get(self, table_name):
        self.myRender(table_name=table_name)


class crud_list_api(BaseHandler):

    @tornado_bz.handleError
    def post(self, table_name):
        self.set_header("Content-Type", "application/json")
        crud_oper = CrudOper(self.pg)
        sql = crud_oper.getCrudListSql(table_name)
        fields = crud_oper.getCrudConf(table_name)
        find_sql = self.request.body
        sql = sql.replace("order", find_sql + " order ")
        for field in fields:
            if field.sql_parm:
                sql = crud_oper.joinCrudListSql(table_name, sql, colum_name=field.name, sql_parm=field.sql_parm)
        isQueryCount = self.get_argument("queryCount", None)
        if not isQueryCount:
            limit = self.get_argument('limit', None)
            offset = self.get_argument('offset', None)
            if not limit:
                limit = 10
            if not offset:
                offset = 0
            else:
                offset = str(int(offset) - 1)
            sql = 'select * from (' + sql + ') tpage limit ' + limit + ' offset ' + offset
            print sql
            cert_array = list(self.pg.db.query(sql))
            self.write(json.dumps({'error': '0', "array": cert_array}, cls=public_bz.ExtEncoder))
        else:
            sql_where_parms = 'is_delete = false'
            if find_sql:
                sql_where_parms += find_sql
            count = self.pg.db.select(tables=table_name, what='count(id)', where=sql_where_parms)
            self.write(json.dumps(count[0], cls=public_bz.ExtEncoder))

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
        appedn by zhangrui 为了实现文件上传功能, 需要在这里查出c_type='input-file'的字段名 与 记录关联的文件
        '''
        self.set_header("Content-Type", "application/json")
        info = json.loads(self.request.body)
        table_name = info["table_name"]
        id = info.get("id")
        data = []
        all_files = []
        if id:
            crud_oper = CrudOper(self.pg)
            what = crud_oper.getWhat(table_name)
            data = list(self.pg.db.select(table_name, what=what, where="id=%s" % id))
            file_upload_columns = crud_oper.getFileUploadCoulumn(table_name)
            for column in file_upload_columns:
                sql = '''
                select r.id, f.file_name, f.file_path, f.file_type, f.suffix, 'false' as remove
                from uploaded_file_record_ref r left join uploaded_files f on r.uploaded_file_id = f.id
                where r.ref_table = '%s' and r.ref_column = '%s' and r.ref_record_id = '%s' and r.is_delete = '0'
                ''' % (table_name, column.name, id)
                files = self.pg.db.query(sql)
                all_files.append({
                    "column": column.name,
                    "files": files
                })
        table_desc = db_bz.getTableDesc(self.pg, table_name)
        if table_desc is None:
            raise Exception("需要设定修改维护的系统(biao)的说明")
        self.write(json.dumps({'error': '0', 'data': data, 'table_desc': table_desc, 'all_files': all_files}, cls=public_bz.ExtEncoder))


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
            id = self.pg.db.insert(table_name, seqname='id_base_seq', **record)

        self.write(json.dumps({'error': '0', 'id': id}))

if __name__ == '__main__':
    pass
