#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
create by bigzhu at 15/07/06 18:01:26 用来向html加入基础的js和css, 一般放在base.html里, 避免因为没有使用 ui modules 导致没有js/css引入
'''

from ui_module import my_ui_module
from tornado_bz import BaseHandler
import tornado_bz


class world_map_m(my_ui_module.MyUIModule):

    '''
    create by bigzhu at 15/07/07 10:13:03
    '''

    def render(self, country_code_count, height=600, background_color="#66978A", fill_color="#e4e4e4", color_array='"#EEF3F1","#FFFAD0","#F2EE95","#F8CE59","#F9B700","#F5A02A","#CF801D","#BF7521","#732F01","#4F2102"'):
        '''
        country_code_count.country_code  #城市编码
        country_code_count.count  #数量
        '''
        parm = locals().copy()
        del parm['self']
        return self.render_string(self.html_name, **parm)


    def javascript_files(self):
        '''
        modify by bigzhu at 15/07/08 10:45:50 要用 jquery-jvectormap-2.0.2, 不能用 AdminLTE-2.0.4 带着的,会报找不到 jvm.Map 的错误
        '''
        my_js_files = [
            self.LIB_PATH + '/jquery-jvectormap-2.0.2/jquery-jvectormap-2.0.2.min.js',
            self.LIB_PATH + '/underscore-min.js',
            #self.LIB_PATH + 'AdminLTE-2.0.4/plugins/jvectormap/jquery-jvectormap-1.2.2.min.js',
            #'http://jvectormap.com/js/jquery-jvectormap-1.2.2.min.js',
            self.LIB_PATH + 'AdminLTE-2.0.4/plugins/jvectormap/jquery-jvectormap-world-mill-en.js',

        ]
        self.all_js_files += my_js_files

        return self.all_js_files

    def css_files(self):
        my_css_files = [
            self.LIB_PATH + '/jquery-jvectormap-2.0.2/jquery-jvectormap-2.0.2.css',
            #self.LIB_PATH + 'AdminLTE-2.0.4/plugins/jvectormap/jquery-jvectormap-1.2.2.css',
        ]
        self.all_css_files += my_css_files
        return self.all_css_files


class world_map(BaseHandler):

    '''
    create by bigzhu at 15/07/07 10:24:47 just for test
    '''

    def get(self):
        self.render(tornado_bz.getTName(self))
