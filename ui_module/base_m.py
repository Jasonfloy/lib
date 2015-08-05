#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ui_module import my_ui_module


class base_m(my_ui_module.MyUIModule):

    '''
    create by bigzhu at 15/06/27 22:22:27 用来加载必要的js/css文件
    '''

    def render(self):
        return ''

    def javascript_files(self):
        return self.all_js_files

    def css_files(self):
        return self.all_css_files
