#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from tornado_bz import UserInfoHandler
from ui_module import my_ui_module


class public_m(my_ui_module.JsCssUIModule):

    '''create by bigzhu at 15/02/21 18:34:46 就是为了提供 public.js 来用
    '''
    pass


class cascade(UserInfoHandler):
    '''
    根据参数取回数组[{"text": text, "value": value}]
    '''

    def get(self, str):
        print str
        parms = str.split("/")
        print parms
        self.write(json.dumps({'error': '0', 'options': None}))

if __name__ == '__main__':
    pass
