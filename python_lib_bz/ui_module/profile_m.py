#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado_bz
import json
import tornado
from tornado_bz import UserInfoHandler
from ui_module import my_ui_module


class profile_m(my_ui_module.MyUIModule):

    '''
    create by bigzhu at 15/03/03 10:43:04 用户的 profile, 需要传入 user_info 对象
    '''

    def render(self, user_info):

        return self.render_string(self.html_name, user_info=user_info)


class profile(UserInfoHandler):

    '''
    用户资料变更
    '''
    @tornado_bz.mustLogin
    def get(self):
        self.render(tornado_bz.getTName(self))

    @tornado_bz.mustLogin
    @tornado_bz.handleError
    def post(self):
        self.set_header("Content-Type", "application/json")
        if self.request.files:
            f = self.request.files["img"][0]
            if "image" not in f.content_type:
                raise Exception('上传的文件应该是一个图片')
            file_type = f.get("filename")[f.get("filename").index("."):]
            file_path = "static/upload/%s%s" % (self.current_user, file_type)
            img = open(file_path, 'w')
            img.write(f["body"])
            img.close()
            self.pg.db.update("user_info", where="id='%s'" % self.current_user, picture="/" + file_path)
            self.write(json.dumps({'error': 0}))
        else:
            data = json.loads(self.request.body)
            self.pg.db.update("user_info", where="id='%s'" % self.current_user, slogan=tornado.escape.xhtml_escape(data.get("slogan")), email=tornado.escape.xhtml_escape(data.get("email")))
            self.write(json.dumps({'error': 0}))
if __name__ == '__main__':
    pass
