#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tornado.web import UIModule
action = ''
JS_PATH = "/lib_static/js/"
CSS_PATH = "/lib_static/css/"
LIB_PATH = "/lib_static/lib/"


class MyUIModule(UIModule):

    '''
    create by bigzhu at 15/03/07 21:12:30 改成 file 了,没法用模板了
    modify by bigzhu at 15/03/06 17:04:03 加入file
    modify by bigzhu at 15/06/13 14:13:39 加入version,以更新js,css
    modify by bigzhu at 15/06/19 15:40:48 支持有多个js 和 css 的情况
    modify by bigzhu at 15/06/27 22:07:41 把一些公用的依赖js/css加入到js/css list 中, 以避免潜规则依赖
    '''

    def __init__(self, handler):
        UIModule.__init__(self, handler)
        self.pg = self.handler.settings['pg']

        self.CSS_PATH = CSS_PATH
        self.JS_PATH = JS_PATH

        self.class_name = self.__class__.__name__
        self.css_name = self.class_name + '.css'
        self.js_name = self.class_name + '.js'
        self.html_name = self.class_name + '.html'

        self.js_file = JS_PATH + self.js_name
        self.css_file = CSS_PATH + self.css_name
        self.LIB_PATH = LIB_PATH

        self.version = None

        # 一些公用的文件
        self.all_js_files = [
            self.LIB_PATH + 'vue.min.js',
            self.LIB_PATH + 'underscore-min.js',
            self.LIB_PATH + 'jquery-2.1.1.min.js',
            #self.LIB_PATH + 'bootstrap-3.3.2-dist/js/bootstrap.min.js',
            #self.LIB_PATH + 'AdminLTE-2.0.2/dist/js/app.js',
            #self.LIB_PATH + 'AdminLTE-2.0.2/plugins/slimScroll/jquery.slimscroll.min.js',
            #self.LIB_PATH + 'jquery-toastmessage-plugin/src/main/javascript/jquery.toastmessage.js',
        ]
        self.all_css_files = [
            self.LIB_PATH + 'bootstrap-3.3.2-dist/css/bootstrap.min.css',
            self.LIB_PATH + 'Font-Awesome/css/font-awesome.min.css',
            self.LIB_PATH + 'ionicons-2.0.1/css/ionicons.min.css',
            self.LIB_PATH + 'AdminLTE-2.0.2/dist/css/AdminLTE.css',
            #self.LIB_PATH + 'AdminLTE-2.0.2/dist/css/skins/skin-blue.min.css',
            #self.LIB_PATH + 'jquery-toastmessage-plugin/src/main/resources/css/jquery.toastmessage.css',
        ]

    def javascript_files(self):
        if self.version:
            self.js_file += '?v=%s' % self.version
        self.all_js_files.append(self.js_file)
        return self.all_js_files

    def css_files(self):
        if self.version:
            self.css_file += '?v=%s' % self.version
        self.all_css_files.append(self.css_file)
        return self.all_css_files
    '''
    def embedded_css(self):
        return self.render_string(self.css_name)

    def embedded_javascript(self):
        return self.render_string(self.js_name, action_url=self.action_url)
    '''

    def render(self):
        return self.render_string(self.html_name)


class JsCssUIModule(UIModule):

    '''
    create by bigzhu at 15/02/22 03:40:44 用于只有 js 的 ui module
    modify by bigzhu at 15/02/22 21:30:12 public 还有 css 也得弄过去
    modify by bigzhu at 15/03/06 17:05:47 改为用 file
    '''

    def __init__(self, handler):
        UIModule.__init__(self, handler)
        self.pg = self.handler.settings['pg']

        self.class_name = self.__class__.__name__
        self.js_name = self.class_name + '.js'
        self.css_name = self.class_name + '.css'

        self.js_file = JS_PATH + self.js_name
        self.css_file = CSS_PATH + self.css_name

    def javascript_files(self):
        return self.js_file

    def css_files(self):
        return self.css_file

    '''
    def embedded_javascript(self):
        return self.render_string(self.js_name)

    def embedded_css(self):
        return self.render_string(self.css_name)
    '''

    def render(self):
        return ''


class HtmlUIModule(UIModule):

    '''
    create by bigzhu at 15/03/05 10:22:54 只要返回 html 就可以了
    '''

    def __init__(self, handler):
        UIModule.__init__(self, handler)
        self.pg = self.handler.settings['pg']

        self.class_name = self.__class__.__name__
        self.html_name = self.class_name + '.html'

    def embedded_javascript(self):
        return ''

    def embedded_css(self):
        return ''

    def render(self):
        return self.render_string(self.html_name)
