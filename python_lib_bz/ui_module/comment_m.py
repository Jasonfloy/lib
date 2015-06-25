#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ui_module import my_ui_module
import comment_bz
import tornado_bz
from public_bz import storage
from tornado_bz import UserInfoHandler
import json
import tornado
from ui_module import my_ui_module
OK = '0'


def createTable(db_name):
    '''
    create by bigzhu at 15/04/13 13:13:48 建立 comment 数据模型库(依赖)
    '''
    import model_oper_bz
    import model_bz
    model_oper_bz.createTable(model_bz.comment, db_name)


class comment_reply_m(my_ui_module.MyUIModule):

    '''
    modify by bigzhu at 15/02/22 14:22:10 因为要递归,所以得单独独立出来
    modify by bigzhu at 15/06/19 15:15:21 use self.html_name
    '''

    def render(self, comments):
        return self.render_string(self.html_name, comments=comments)


class comment_m(my_ui_module.MyUIModule):

    '''
    评论,需要传入参数
    comments: 评论组, 包括评论内容,以及评论时间,具体参见 comment 表
    key_type: 一个网站有多个地方有评论时候,用于区分哪个模块,可空
    key: 关键字,一般就是 id, 比如 site_id,定位是哪个东西的评论
    user_info:用户信息,发评论的人的信息
    modify by bigzhu at 15/02/22 21:16:39 去掉发评论的人的信息,应该是默认带在 template 里面了
    '''

    def render(self, comments, key_type, key):
        parm = storage()
        parm.comments = comments
        parm.key_type = key_type
        parm.key = key

        return self.render_string(self.html_name, parm=parm)

    def javascript_files(self):
        return [self.js_file,
                self.LIB_PATH + '/flexText/jquery.flexText.min.js',
                ]

    def css_files(self):
        return [self.LIB_PATH + '/flexText/style.css',
                self.css_file,
                ]


class comment(UserInfoHandler):

    '''
    公用的评论系统
    key_type 评论的挂载类型
    key 评论的挂载 id
    modify by bigzhu at 15/02/22 12:22:45 放入公用库中
    '''

    def initialize(self):
        UserInfoHandler.initialize(self)

    @tornado_bz.handleError
    @tornado_bz.mustLogin
    def post(self):
        self.set_header("Content-Type", "application/json")
        data = json.loads(self.request.body)
        comment_content = data.get('comment')

        comment_content = tornado.escape.xhtml_escape(comment_content)
        parent_id = data.get('parent_id')
        key_type = data.get('key_type')
        key = data.get('key')

        comment = comment_bz.Comment(self.pg)

        comment.addComment(comment_content, parent_id, self.current_user, key_type, key)

        self.write(json.dumps({'error': OK}))
if __name__ == "__main__":
    pass
