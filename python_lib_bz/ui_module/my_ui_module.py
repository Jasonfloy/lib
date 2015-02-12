#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.web
action = ''


class MyUIModule(tornado.web.UIModule):
    action_url = ''

    def __init__(self, handler):
        tornado.web.UIModule.__init__(self, handler)

        self.class_name = self.__class__.__name__
        self.css_name = self.class_name + '.css'
        self.js_name = self.class_name + '.js'
        self.html_name = self.class_name + '.html'

    def embedded_css(self):
        return self.render_string(self.css_name)

    def embedded_javascript(self):
        return self.render_string(self.js_name, action_url=self.action_url)

    def render(self):
        return self.render_string(self.html_name)
