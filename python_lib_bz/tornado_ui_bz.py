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


class CommentReply(tornado.web.UIModule):

    def render(self, comments, timeLen):
        return self.render_string("template_bz/CommentReply.html", comments=comments, timeLen=timeLen)

class Comment(tornado.web.UIModule):

    '''
    评论
    comments: 评论组, 包括评论内容,以及评论时间
    id: 评论附着于哪个东西, 这个东西的 id
    '''

    def embedded_css(self):
        return '''
.comment-list {
position: relative;
}
.comment-list:before {
position: absolute;
top: 0;
bottom: 100px;
left: 18px;
width: 1px;
background: #e0e4e8;
content: '';
}
.comment-list .comment-item {
margin-top: 0;
position: relative;
padding-left: 40px;
}
.comment-list .comment-item .comment-item {
padding-left: 46px;
}
.comment-list .thumb-sm {
width: 36px;
}
.avatar {
position: relative;
display: block;
border-radius: 5px;
white-space: nowrap;
margin-left: -40px;
}
.comment-list .arrow.left {
top: 20px;
left: 39px;
}
.comment-list .comment-item .comment-item .arrow.left {
left: 45px;
}
.comment-list .comment-reply .arrow.left {
top: 20px;
left: -1px;
}
.arrow.left {
top: 50%;
left: -8px;
margin-top: -8px;
border-left-width: 0;
border-right-color: #eee;
border-right-color: rgba(0,0,0,0.1);
}
.arrow:after {
border-width: 7px;
content: "";
}
.arrow, .arrow:after {
position: absolute;
display: block;
width: 0;
height: 0;
border-color: transparent;
border-style: solid;
}
.arrow.left:after {
content: " ";
left: 1px;
border-left-width: 0;
border-right-color: #fff;
bottom: -7px;
}
.arrow {
border-width: 8px;
z-index: 10;
}
.comment-list .comment-item .comment-body {
margin-left: 6px;
}
.comment-list .comment-reply .comment-body {
margin-left: 6px;
}
.panel.panel-default {
border-color: #eaeef1;
}
.panel {
border-radius: 2px;
}
.comment-list .comment-item .panel-heading, .comment-list .comment-item .panel-footer {
position: relative;
font-size: 12px;
background: #fff;
}
.bg-white a {
color: #545a5f;
}
.thumb img, .thumb-xs img, .thumb-sm img, .thumb-md img, .thumb-lg img, .thumb-btn img {
height: auto;
max-width: 100%;
vertical-align: middle;
}
.avatar img {
border-radius: 5px;
width: 100%;
}
.bg-info {
background-color: #4cb6cb;
color: #eaf6f9;
}
.bg-dark {
background-color: #5a6a7a;
color: #c9d0d7;
}
.bg-success {
background-color: #1ab667;
color: #a9f3ce;
}
.badge, .label {
font-weight: bold;
}
.label {
display: inline;
padding: .2em .6em .3em;
font-size: 75%;
font-weight: bold;
line-height: 1;
color: #fff;
text-align: center;
white-space: nowrap;
vertical-align: baseline;
border-radius: .25em;
}
.comment-list .comment-reply {
margin-left: 40px;
position: relative;
}
.comment-list .comment-item .comment-reply,.comment-list .comment-reply .comment-reply {
margin-left: 46px;
}
.input-group {
position: relative;
display: table;
border-collapse: separate;
}
.input-group-addon, .input-group-btn, .input-group .form-control {
display: table-cell;
}
.input-group .form-control {
position: relative;
z-index: 2;
float: left;
width: 100%;
margin-bottom: 0;
}
.comment-textarea{
    width: 100%;
    display: table-cell;
    box-sizing:border-box;
    resize: none;
    border: solid 1px #ccc;
    padding: 10px;
    outline: none;
    margin-bottom: 5px;
    border-radius: 3px;
    line-height: 24px;
}
.comment-textarea:focus{
    border: solid 1px #00a5fb;
}
.btn{
    outline: none;
}
.comment-list .comment-action{
    float: right;
    visibility: hidden;
}
.comment-list .comment-reply .comment-action{
    margin-right: 15px;
}
.comment-list .panel-body:hover .comment-action{
    visibility: visible;
}
    '''

    def javascript_files(self):
        '''
        '''
        return 'js_bz/Comment.js'

    def render(self, comments, key_type, key):
        return self.render_string("template_bz/Comment.html", comments=comments, timeLen=time_bz.timeLen, key_type=key_type, key=key)


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

    def render(self, menu_link):
        return self.render_string("template_bz/SubMenuLink.html", **menu_link)

if __name__ == '__main__':
    pass
