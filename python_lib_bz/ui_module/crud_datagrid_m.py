#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
create by bigzhu at 15/04/21 14:59:10 用来在页面上的datagrid,没有search
'''

from ui_module import my_ui_module
from tornado_bz import BaseHandler
from tornado_bz import ModuleHandler
import tornado_bz
import json
import public_bz
from webpy_db import SQLLiteral
from ui_module import crud_m
import db_bz


class crud_datagrid_m(my_ui_module.MyUIModule):

    '''
    create by bigzhu at 15/04/21 15:18:49 datagrid
    '''

    def render(self, table_name):
        self.table_name = table_name
        crud_oper = crud_m.CrudOper(self.pg)
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
        return self.render_string(self.html_name, table_name=table_name, fields=show_fields, all_fields=fields, table_desc=table_desc)

    def css_files(self):
        return ''

if __name__ == '__main__':
    pass
