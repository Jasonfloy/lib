#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ui_module import my_ui_module
import comment_bz
import time_bz
import tornado_bz
from public_bz import storage
from tornado_bz import UserInfoHandler
import tree_bz
import json
import public_bz
import pg_bz
import tornado
OK = '0'
class comment_reply_m(tornado.web.UIModule):
    '''modify by bigzhu at 15/02/22 14:22:10 因为要递归,所以得单独独立出来
    '''

    def render(self, comments):
        return self.render_string("comment_reply_m.html", comments=comments)


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


class comment(UserInfoHandler):

    '''
    公用的评论系统
    key_type 评论的挂载类型
    key 评论的挂载 id
    modify by bigzhu at 15/02/22 12:22:45 放入公用库中
    '''
    @tornado_bz.handleError
    @tornado_bz.mustLogin
    def post(self):
        self.set_header("Content-Type", "application/json")
        data = json.loads(self.request.body)
        comment_content = data.get('comment')
        parent_id = data.get('parent_id')
        key_type = data.get('key_type')
        key = data.get('key')

        comment = comment_bz.Comment(self.pg)

        comment.addComment(comment_content, parent_id, self.current_user, key_type, key)

        self.write(json.dumps({'error': OK}))
if __name__ == "__main__":

    import sys
    if len(sys.argv) == 2:
        port = int(sys.argv[1])
    else:
        port = 8888
    print port

    url_map = tornado_bz.getURLMap(globals().copy())

    settings = tornado_bz.getSettings()

    settings["pg"] = pg_bz

    application = tornado.web.Application(url_map, **settings)

    application.listen(port)
    ioloop = tornado.ioloop.IOLoop().instance()
    tornado.autoreload.start(ioloop)
    ioloop.start()
