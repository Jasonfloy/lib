#!/usr/bin/env python
# -*- coding: utf-8 -*-


from ui_module import my_ui_module


class solar404_m(my_ui_module.MyUIModule):

    '''
    create by bigzhu at 15/03/18 11:13:35 太阳系
    这里的 css 必须要用embedded的方式,否则不会生效
    '''

    def css_files(self):
        return ''
    def embedded_css(self):
        return self.render_string('../static/css/'+self.css_name)
if __name__ == '__main__':
    pass
