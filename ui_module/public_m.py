#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import public_bz
from tornado_bz import UserInfoHandler
from ui_module import my_ui_module


class public_m(my_ui_module.MyUIModule):

    '''
    create by bigzhu at 15/02/21 18:34:46 就是为了提供 public.js 来用
    modify by bigzhu at 15/06/28 01:04:50 统一使用MyUIModule
    '''
    def render(self):
        return ''

class cascade(UserInfoHandler):
    '''
    create or update by: ZhangRui AT 2015-03-21 16:43
    根据参数取回数组[{"text": text, "value": value}]
    '''

    def get(self, str):
        self.set_header("Content-Type", "application/json")
        parms = str.split("/")
        cascade_type = parms[0]
        table_name = parms[1]
        column_name = parms[2]
        record_id = parms[3]
        if cascade_type == "options":
            options = list(self.pg.db.select(table_name, what="id as value, %s as text" % column_name, where="parent_id='%s'" % record_id))
        elif cascade_type == "value":
            options = list(self.pg.db.select(table_name, what="%s as value" % column_name, where="id='%s'" % record_id))
        else:
            raise Exception('无法识别操作类型: %s .' % cascade_type)
        self.write(json.dumps({'error': '0', 'options': options}, cls=public_bz.ExtEncoder))

if __name__ == '__main__':
    pass
