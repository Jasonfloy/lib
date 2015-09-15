#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''利用Tornado 的 ui 模块,来对 html 和 js 做一些模块化处理
以利于复用
'''
import tornado
import tornado.web
import time_bz
from public_bz import storage


class MenuLink(tornado.web.UIModule):

    '''menu 上的 link, 自己去循环生成内容
    似乎有些多余的样子
    在模板里这样来用:
        {% for menu_link in menu_links %}
        {% module MenuLink(menu_link) %}
        {% end %}
    需要的参数是这样:
        menu_link = storage(title='每日发现', active='', href='/recommend', icon='mail')
    '''

    def render(self, menu_link):
        return self.render_string("template_bz/MenuLink.html", **menu_link)


class CommentReply(tornado.web.UIModule):

    def render(self, comments, timeLen):
        return self.render_string("template_bz/CommentReply.html", comments=comments, timeLen=timeLen)


class SubMenuLink(tornado.web.UIModule):

    '''子菜单的menu 上的 link, 自己去循环生成内容
    在模板里这样来用:
        {% for menu_link in menu_links %}
        {% module SubMenuLink(menu_link) %}
        {% end %}
    需要的参数是这样:
        items = [
            storage(title='每日发现', items=active='', href='/recommend', icon='mail'),
            storage(title='我的收藏', active='active', href='/haha', icon='home')
        ]
        menu_link = storage(title='我是父节点', items=items)
    '''

    def css_files(self):
        '''
        sidebar的样式
        '''
        return 'css_bz/Submenu.css'

    def render(self, menu_link):
        return self.render_string("template_bz/SubMenuLink.html", **menu_link)


class MenuLink_zxy(tornado.web.UIModule):

    '''子菜单的menu 上的 link, 自己去循环生成内容
    在模板里这样来用:
        {% for menu_link in menu_links %}
        {% module MenuLink(menu_link) %}
        {% end %}
    需要的参数是这样:
        items = [
            storage(title='每日发现', items=active='', href='/recommend', icon='mail'),
            storage(title='我的收藏', active='active', href='/haha', icon='home')
        ]
        menu_link = storage(title='我是父节点', items=items)
    '''

    def render(self, menu_link):
        return self.render_string("template_bz/MenuLink_zxy.html", **menu_link)


if __name__ == '__main__':
    pass
