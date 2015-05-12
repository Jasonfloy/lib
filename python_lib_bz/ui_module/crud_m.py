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


def createTable(db_name):
    '''
    create by bigzhu at 15/04/22 18:19:38 create table
    '''
    import model_oper_bz
    import model_bz
    model_oper_bz.createTable(model_bz.crud_conf, db_name)


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
        select * from crud_conf where table_name='%s' and is_delete != 1
        ''' % table_name
        if isTime:
            sql += " and c_type='timestamp' "
        sql += " order by seq desc, created_date"
        curd_confs = list(self.pg.db.query(sql))
        # 处理 Options
        for curd_conf in curd_confs:
            if curd_conf.sql_parm:
                curd_conf.options = self.getOptions(curd_conf.sql_parm)
        return curd_confs

    def getFileUploadCoulumn(self, table_name):
        sql = '''
        select name
        from crud_conf
        where is_delete != 1
            and c_type='input-file'
            and table_name='%s'
        order by seq desc, created_date
        ''' % table_name
        return list(self.pg.db.query(sql))

    def getCrudListConf(self, table_name, isTime=None):
        sql = '''
        select * from crud_conf where table_name='%s' and grid_show=1 and is_delete != 1
        ''' % table_name
        if isTime:
            sql += " and c_type='timestamp' "
        sql += " order by seq desc, created_date"
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
                    s = "to_timestamp(%s)" % str(float(record[field.name]) / 1000)
                    record[field.name] = SQLLiteral(s)
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

    def getCrudListSql(self, table_name, user_id=None):
        '''
        modify by bigzhu at 15/03/12 13:57:43 需要添加 id
        create by bigzhu at 15/03/12 12:56:43 根据给定的条件组合出查询 list 的 sql
        '''
        what = self.getWhat(table_name)
        where = "is_delete != 1"
        if user_id:
            where += " and user_id=%s" % user_id
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
        return self.render_string(self.html_name, fields=fields, table_name=table_name)

    def css_files(self):
        return ''


class crud_check_m(my_ui_module.MyUIModule):

    '''
    create by zhangwh at 15/05/11 21:15
    审核detail模块
    '''

    def render(self, table_name):
        crud_oper = CrudOper(self.pg)
        fields = crud_oper.getCrudConf(table_name)
        return self.render_string(self.html_name, fields=fields, table_name=table_name)

    def css_files(self):
        return ''


class crud_list_m(my_ui_module.MyUIModule):

    '''
    create by bigzhu at 15/03/09 11:17:17 显示 list
    '''

    def render(self, table_name):
        crud_oper = CrudOper(self.pg)
        #fields = crud_oper.getCrudListConf(table_name)
        fields = crud_oper.getCrudConf(table_name)
        show_fields = []
        more_fields = []
        for field in fields:
            if field.grid_show == 1:
                show_fields.append(field)
            elif field.is_search == 1:
                more_fields.append(field)
        table_desc = db_bz.getTableDesc(self.pg, table_name)
        if table_desc is None:
            raise Exception("需要设定修改维护的系统(biao)的说明")
        return self.render_string(self.html_name, fields=show_fields, more_search=more_fields, table_desc=table_desc)

    def css_files(self):
        return ''


class crud_check_list_m(my_ui_module.MyUIModule):

    '''
    create by zhangwh at 15/05/11 21:18
    显示list
    '''

    def render(self, table_name):
        crud_oper = CrudOper(self.pg)
        fields = crud_oper.getCrudConf(table_name)
        show_fields = []
        show_fields = [field for field in fields if field.grid_show == 1]

        return self.render_string(self.html_name, fields=show_fields)

    def css_files(self):
        return ''


class crud_list(ModuleHandler):

    '''
    crud list 实现
    '''

    def get(self, table_name):
        self.myRender(table_name=table_name)


class crud_check_list(ModuleHandler):

    '''
    审核模块list显示
    '''

    def get(self, table_name):
        self.myRender(table_name=table_name)


class crud_list_api(BaseHandler):

    @tornado_bz.handleError
    def post(self, table_name):
        self.set_header("Content-Type", "application/json")
        crud_oper = CrudOper(self.pg)
        sql = crud_oper.getCrudListSql(table_name, self.current_user)
        fields = crud_oper.getCrudConf(table_name)
        find_sql = ""
        isFind = self.get_argument("find", None)
        flag = False  # 开关，判断是否有关联查询
        option_fields = []
        option_dict = {}
        for field in fields:
            if field.sql_parm:
                sql = crud_oper.joinCrudListSql(table_name, sql, colum_name=field.name, sql_parm=field.sql_parm)
                if isFind:
                    sql = "select * from (" + sql + ")c where 1=1 "  # 如果是查找，并且有关联时，
                    flag = True
            if field.options:
                option_fields.append(field.name)
                option_dict[field.name] = field.options

        if isFind:
            find_data = json.loads(self.request.body)
            search_parms = find_data["search_parms"]
            for sp in search_parms:
                find_sql += " and (%s)::text like '%%%s%%'" % (sp["name"], sp["value"])  # 先测试，不对用子查询
        isQueryCount = self.get_argument("queryCount", None)
        if not isQueryCount:
            if flag:
                sql += find_sql
            else:
                sql = sql.replace("order", find_sql + " order ")  # load时拼条件
            limit = self.get_argument('limit', None)
            offset = self.get_argument('offset', None)
            if not limit:
                limit = 10
            if not offset:
                offset = 0
            else:
                offset = str(int(offset) - 1)
            sql = 'select * from (' + sql + ') tpage limit ' + str(int(limit)) + ' offset ' + str(int(offset))
            cert_array = list(self.pg.db.query(sql))

            # 解决crud_list页面select显示为value的问题
            result_array = []
            for row in cert_array:
                for key in row:
                    if key in option_fields:
                        for select in option_dict[key]:
                            if row[key] == select['value']:
                                row[key] = select['text']
                result_array.append(row)

            self.write(json.dumps({'error': '0', "array": result_array}, cls=public_bz.ExtEncoder))
        else:
            sql_where_parms = ' is_delete != 1'
            if find_sql:
                sql_where_parms += find_sql
            if flag:
                sql += find_sql
                sql = "select count(*) from (" + sql + ") d"
                count = self.pg.db.query(sql)
            else:
                count = self.pg.db.select(tables=table_name, what='count(id)', where=sql_where_parms)
            self.write(json.dumps(count[0], cls=public_bz.ExtEncoder))

    def delete(self, table_name):
        self.set_header("Content-Type", "application/json")
        ids = self.request.body
        self.pg.db.update(table_name, where="id in (%s)" % ids, is_delete=1)
        self.write(json.dumps({'error': '0'}))


class crud_check_list_api(BaseHandler):

    '''
    create by zhangwh at 15/05/11 22:19
    '''

    def get(self, table):
        self.set_header("Content-Type", "application/json")

        limit = self.get_argument('limit', 10)
        offset = self.get_argument('offset', 1)
        checked = self.get_argument('checked', 'nocheck')
        if int(offset) > 0:
            offset = int(offset) - 1

        sql = "select * from %s where checked='%s' order by created_date desc limit %d offset %d" % (table, str(checked), int(limit), int(offset))
        records = list(self.pg.db.query(sql))

        sql = "select count(*) from %s" % table
        count = list(self.pg.db.query(sql))

        data = json.dumps({'error': '0', 'records': records, 'count': count[0].count}, cls=public_bz.ExtEncoder)
        self.write(data)


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
        append by zhangrui 为了实现文件上传功能, 需要在这里查出c_type='input-file'的字段名 与 记录关联的文件
        '''
        self.set_header("Content-Type", "application/json")
        info = json.loads(self.request.body)
        table_name = info["table_name"]
        id = info.get("id")
        data = []
        crud_oper = CrudOper(self.pg)
        file_columns = crud_oper.getFileUploadCoulumn(table_name)
        if id:
            what = crud_oper.getWhat(table_name)
            data = list(self.pg.db.select(table_name, what=what, where="id=%s" % id))
        table_desc = db_bz.getTableDesc(self.pg, table_name)
        if table_desc is None:
            raise Exception("需要设定修改维护的系统(biao)的说明")
        self.write(json.dumps({'error': '0', 'data': data, 'table_desc': table_desc, 'file_columns': file_columns}, cls=public_bz.ExtEncoder))


class crud_check(ModuleHandler):

    '''
    审核功能的crud
    created by zhangwh at 2015-5-11 16:30
    '''

    def get(self, table_name):
        self.myRender(table_name=table_name)

    @tornado_bz.handleError
    def post(self):
        self.set_header("Content-Type", "application/json")

        data = []
        info = json.loads(self.request.body)
        table_name = info["table_name"]
        id = info.get("id")
        crud_oper = CrudOper(self.pg)
        if id:
            what = crud_oper.getWhat(table_name)
            data = list(self.pg.db.select(table_name, what=what, where="id=%s" % id))

        self.write(json.dumps({'error': '0', 'data': data}, cls=public_bz.ExtEncoder))


class crud_api(BaseHandler):

    '''
    modify by bigzhu at 15/03/10 15:56:15 update 时候也要更新 stat_date
    modify by bigzhu at 15/04/22 17:27:16 自动插入 user_id
    '''

    @tornado_bz.handleError
    def post(self):
        self.set_header("Content-Type", "application/json")
        info = json.loads(self.request.body)
        table_name = info["table_name"]
        record = info["record"]
        if self.current_user:
            if record.get('user_id') is None:
                record['user_id'] = self.current_user
        else:
            raise Exception('请登录系统')
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
            seq = table_name + '_id_seq'
            id = self.pg.db.insert(table_name, seqname=seq, **record)

        self.write(json.dumps({'error': '0', 'id': id}))

if __name__ == '__main__':
    pass
