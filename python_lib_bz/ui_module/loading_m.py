#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ui_module import my_ui_module


class loading_m(my_ui_module.MyUIModule):

    '''create by bigzhu at 15/02/20 23:20:30 loading 的 module
    create by bigzhu at 15/04/10 21:55:37 改回继承MyUIModule,加入版本号
    '''

    def render(self):
        return ''

    def javascript_files(self):
        return self.js_file + '?v=6.1'

    def css_files(self):
        return self.css_file + '?v=1'

if __name__ == '__main__':
    pass
