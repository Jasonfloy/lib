#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ui_module import my_ui_module


class check_ie_m(my_ui_module.MyUIModule):

    '''create by ywq at 15/03/06 判断低于ie9版本，则显示提示升级浏览器的页面
    '''
    def javascript_files(self):
        return ''

    def css_files(self):
        return ''

if __name__ == '__main__':
    pass
