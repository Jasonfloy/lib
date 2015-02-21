#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tornado.web import UIModule
action = ''


class MyUIModule(UIModule):
    action_url = ''

    def __init__(self, handler):
        UIModule.__init__(self, handler)

        self.class_name = self.__class__.__name__
        self.css_name = self.class_name + '.min.css'
        self.js_name = self.class_name + '.min.js'
        self.html_name = self.class_name + '.html'

    def embedded_css(self):
        return self.render_string(self.css_name)

    def embedded_javascript(self):
        return self.render_string(self.js_name, action_url=self.action_url)

    def render(self):
        return self.render_string(self.html_name)

class JsUIModule(UIModule):
    '''
    create by bigzhu at 15/02/22 03:40:44 用于只有 js 的 ui module
    '''

    def __init__(self, handler):
        UIModule.__init__(self, handler)

        self.class_name = self.__class__.__name__
        self.js_name = self.class_name + '.min.js'

    def embedded_javascript(self):
        return self.render_string(self.js_name)

    def render(self):
        return ''
