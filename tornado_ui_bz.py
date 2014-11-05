#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''利用Tornado 的 ui 模块,来对 html 和 js 做一些模块化处理
以利于复用
'''
import tornado
import time_bz


class Login(tornado.web.UIModule):

    '''登录的页面'''

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
        menu_links = [
            storage(title='每日发现', active='', href='/recommend', icon='mail'),
            storage(title='我的收藏', active='active', href='/haha', icon='home')
        ]
    '''

    # def javascript_files(self):
    #    '''
    #    高亮当前选中的这个 menu link
    #    '''
    #    return 'js_bz/MenuLink.js'

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

if __name__ == '__main__':
    pass
