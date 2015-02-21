#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ui_module import my_ui_module


class loading_m(my_ui_module.MyUIModule):

    '''create by bigzhu at 15/02/20 23:20:30 loading 的 module
    '''

    def render(self):
        return self.render_string(self.html_name)

if __name__ == '__main__':
    pass
