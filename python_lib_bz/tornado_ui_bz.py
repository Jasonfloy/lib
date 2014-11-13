#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''利用Tornado 的 ui 模块,来对 html 和 js 做一些模块化处理
以利于复用
'''
import tornado
import time_bz


class Login(tornado.web.UIModule):

    '''登录的页面'''
    def css_files(self):
        '''
        Oauth2 按钮的样式
        '''
        return 'css_bz/Login.css'

    def javascript_files(self):
        '''
        登录的逻辑
        '''
        return 'js_bz/Login.js'

    def render(self):
        return self.render_string("template_bz/Login.html")


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


class Comment(tornado.web.UIModule):

    '''
    评论
    comments: 评论组, 包括评论内容,以及评论时间
    id: 评论附着于哪个东西, 这个东西的 id
    '''

    def javascript_files(self):
        '''
        '''
        return 'js_bz/Comment.js'

    def render(self, comments, id):
        return self.render_string("template_bz/Comment.html", comments=comments, timeLen=time_bz.timeLen, id=id)


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

if __name__ == '__main__':
    pass
