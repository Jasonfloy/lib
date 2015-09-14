#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado_bz
import json
import tornado
from tornado_bz import UserInfoHandler
from ui_module import my_ui_module


class user_info_m(my_ui_module.MyUIModule):

    '''
    create by bigzhu at 15/07/13 11:16:33
    '''

    def render(self, user_info, change_user_name=False):

        return self.render_string(self.html_name, user_info=user_info, change_user_name=change_user_name)


class user_info(UserInfoHandler):

    '''
    用户资料变更
    '''
    @tornado_bz.mustLogin
    def get(self):
        self.render(tornado_bz.getTName(self))

    @tornado_bz.mustLoginApi
    @tornado_bz.handleError
    def post(self):
        self.set_header("Content-Type", "application/json")
        data = json.loads(self.request.body)
        self.pg.db.update("user_info", where="id='%s'" % self.current_user, **data)
        self.write(json.dumps({'error': '0'}))


if __name__ == '__main__':
    pass
