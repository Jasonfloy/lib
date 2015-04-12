#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ui_module import my_ui_module

class header_m(my_ui_module.MyUIModule):
    '''
    create by bigzhu at 15/04/12 14:32:51 通用的 header
    '''
    def css_files(self):
        return ''
    def render(self, user_info, header_name, links):
        return self.render_string(self.html_name, user_info=user_info, header_name=header_name, links=links)
if __name__ == '__main__':
    pass
