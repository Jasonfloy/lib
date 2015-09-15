#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ui_module import my_ui_module


class header_m(my_ui_module.MyUIModule):

    '''
    create by bigzhu at 15/04/12 14:32:51 通用的 header
        body  要加入 layout-top-nav 的 class 才能使用
    modify by bigzhu at 15/07/06 15:51:44 用need_login设定是否需要登录
    modify by bigzhu at 15/08/02 08:26:13 link.loading 决定是否要有loading出来
    modify by bigzhu at 15/08/02 08:26:59 link.target 决定是否在新页面打开
    '''

    def css_files(self):
        return ''

    def javascript_files(self):
        my_js_files = [
            self.LIB_PATH + 'bootstrap-3.3.2-dist/js/bootstrap.min.js',
            self.js_file
        ]
        self.all_js_files += my_js_files

        return self.all_js_files

    def render(self, user_info, header_name, links, need_login=True):
        return self.render_string(self.html_name, user_info=user_info, header_name=header_name, links=links, need_login=need_login)
if __name__ == '__main__':
    pass
