#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ui_module import my_ui_module


class simditor_m(my_ui_module.MyUIModule):

    '''
    富文本编辑器
        create by bigzhu at 15/06/28 00:45:09 彩程出品, 目前能找到的最好的
    '''

    def __init__(self, handler):
        my_ui_module.MyUIModule.__init__(self, handler)

        simditor_path = self.LIB_PATH + 'simditor-2.1.14/'
        simditor_script = simditor_path + 'scripts/'
        simditor_styles = simditor_path + 'styles/'
        self.all_js_files += [
            simditor_script + 'module.js',
            simditor_script + 'hotkeys.js',
            simditor_script + 'uploader.js',
            simditor_script + 'simditor.js',
        ]
        self.all_css_files += [
            simditor_styles + 'simditor.css',
        ]

    def render(self, html=True):
        if html:
            return self.render_string(self.html_name)
        else:
            return ''
    def css_files(self):
        return self.all_css_files

if __name__ == '__main__':
    pass
