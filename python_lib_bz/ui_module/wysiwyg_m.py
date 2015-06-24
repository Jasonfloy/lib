#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ui_module import my_ui_module


class wysiwyg_m(my_ui_module.MyUIModule):

    '''
    富文本编辑器
    create by bigzhu at 15/06/19 15:15:55 http://www.bootcss.com/p/bootstrap-wysiwyg/
    '''

    def __init__(self, handler):
        my_ui_module.MyUIModule.__init__(self, handler)
        self.all_js_files = [self.LIB_PATH+'bootstrap3-wysiwyg/dist/bootstrap3-wysihtml5.all.js',
                             self.LIB_PATH+'bootstrap3-wysiwyg/dist/locales/bootstrap-wysihtml5.zh-CN.js',
                             ]
        self.all_css_files = [self.LIB_PATH+'bootstrap3-wysiwyg/dist/bootstrap3-wysihtml5.min.css',
                              self.CSS_PATH+'file_upload_m.css',
                              ]


    def render(self):
        return self.render_string(self.html_name)



if __name__ == '__main__':
    pass
