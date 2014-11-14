#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''利用Tornado 的 ui 模块,来对 html 和 js 做一些模块化处理
以利于复用
'''
import tornado
import tornado.web
import time_bz
from public_bz import storage


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

    def render(self, oauth2):
        return self.render_string("template_bz/Login.html", oauth2=oauth2)


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
    评论,需要传入参数
    comments: 评论组, 包括评论内容,以及评论时间,具体参见 comment 表
    key_type: 一个网站有多个地方有评论时候,用于区分哪个模块,可空
    key: 关键字,一般就是 id, 比如 site_id,定位是哪个东西的评论
    user_info:用户信息,发评论的人的信息



    -- Table: comment

    -- DROP TABLE comment;

    CREATE TABLE comment
    (
    -- 继承 from table base:  id integer NOT NULL DEFAULT nextval('base_id_seq'::regclass),
    -- 继承 from table base:  created_date timestamp without time zone DEFAULT now(),
    -- 继承 from table base:  stat_date timestamp without time zone DEFAULT now(),
      user_id integer, -- 填写的用户 id
      key_type text, -- 用于那个类型....
      key text, -- 比如填入 site_id,...
      user_name text, -- 用户名...
      user_picture text, -- 用户头像...
      comment text, -- 评论
      parent_id integer -- 可空,父节点 id
    )
    INHERITS (base)
    WITH (
      OIDS=FALSE
    );
    ALTER TABLE comment
      OWNER TO monitor;
    COMMENT ON COLUMN comment.user_id IS '填写的用户 id';
    COMMENT ON COLUMN comment.key_type IS '用于那个类型.

    比如一个系统有多个地方都要有评论,则用这个来区别

    为了站点可以填为 site';
    COMMENT ON COLUMN comment.key IS '比如填入 site_id,
    使用这个评论的元素';
    COMMENT ON COLUMN comment.user_name IS '用户名
    可以为空,如果你用 user_id 去关联其他表的话';
    COMMENT ON COLUMN comment.user_picture IS '用户头像

    可空';
    COMMENT ON COLUMN comment.comment IS '评论';
    COMMENT ON COLUMN comment.parent_id IS '可空,父节点 id';


    '''

    def css_files(self):
        return 'css_bz/Comment.css'

    def javascript_files(self):
        '''
        '''
        return 'js_bz/Comment.js'

    def render(self, comments, key_type, key, user_info):
        parm = storage()
        parm.comments = comments
        parm.key_type = key_type
        parm.key = key
        parm.user_info = user_info

        return self.render_string("template_bz/Comment.html", parm=parm, timeLen=time_bz.timeLen)


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
