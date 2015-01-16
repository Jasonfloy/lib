#!/usr/bin/env python
# -*- coding: utf-8 -*-
from db_bz import daemonDB


class UserOper:

    '''
    对用户相关的操作
    '''

    def __init__(self, pg):
        self.pg = pg

    @daemonDB
    def login(self, user_name, password):
        '''
        登录模块,如果不存在这个用户名,则注册
        数据模型:

        CREATE TABLE user_info
        (
          user_type text, -- google or other
          out_id text, -- google id or other
          email text,
          user_name text,
          link text,
          picture text,
          gender text, -- mail?
          locale text, --zh-CN
          password text,
          original_json text --用来存放原始返回的 json 字段,避免有内容没存到
        -- 继承 from table base:  user_id integer
        )
        INHERITS (base)



        '''
        user_infos = self.getUserInfo(user_name=user_name)
        if user_infos:
            if user_infos[0].password == password:
                return user_infos[0]
            else:
                raise Exception('密码错误!')
        else:
            self.pg.db.insert('user_info', user_type='my', user_name=user_name, password=password)
            return self.login(user_name, password)

    @daemonDB
    def getUserInfo(self, user_type='my', user_name=None, out_id=None):
        sql = "select * from user_info where user_type='%s' " % user_type
        if user_name:
            sql += " and user_name='%s' " % user_name
        if out_id:
            sql += " and out_id='%s' " % out_id
        return list(self.pg.db.query(sql))

    @daemonDB
    def googleLogin(self, user_info):
        '''
        google 登录信息存到 db 中
            {
             "id": "112340346785758313259",
             "email": "vermiliondun@gmail.com",
             "verified_email": true,
             "name": "朱一凡",
             "given_name": "一凡",
             "family_name": "朱",
             "link": "https://plus.google.com/112340346785758313259",
             "picture": "https://lh5.googleusercontent.com/-E4rb72RaQHE/AAAAAAAAAAI/AAAAAAAAJzQ/p-tx9D78Mik/photo.jpg",
             "gender": "male",
             "locale": "zh-CN"
            }
        '''
        user_infos = self.getUserInfo(user_type='google', out_id=user_info['id'])
        if user_infos:
            return user_infos[0]
        else:
            pg.db.insert('user_info',
                         user_type='google',
                         out_id=user_info['id'],
                         email=user_info['email'],
                         user_name=user_info['name'],
                         link=user_info['link'],
                         picture=user_info['picture'],
                         gender=user_info['gender'],
                         locale=user_info['locale']
                         )
            return self.googleLogin(user_info)

    @daemonDB
    def twitterLogin(self, user_info):
        '''
        twitter 登录信息存到 db 中
        '''
        user_infos = self.getUserInfo(user_type='twitter', out_id=user_info['id'])
        if user_infos:
            return user_infos[0]
        else:
            self.pg.db.insert('user_info',
                              user_type='twitter',
                              out_id=user_info['id'],
                              # email=user_info['email'],
                              user_name=user_info['username'],
                              # link=user_info['link'],
                              picture=user_info['profile_image_url_https'],
                              # gender=user_info['gender'],
                              locale=user_info['profile_location']
                              )
            return self.twitterLogin(user_info)

    @daemonDB
    def doubanLogin(self, user_info):
        '''
        douban 登录信息存到 db 中
        '''
        user_infos = self.getUserInfo(user_type='douban', out_id=user_info['id'])
        if user_infos:
            return user_infos[0]
        else:
            self.pg.db.insert('user_info',
                         user_type='douban',
                         out_id=user_info['id'],
                         # email=user_info['email'],
                         user_name=user_info['name'],
                         link=user_info['alt'],
                         picture=user_info['avatar'],
                         # gender=user_info['gender'],
                         locale=user_info['loc_name']
                         )
            return self.doubanLogin(user_info)

    @daemonDB
    def resetPassword(self, user_id, old_password, new_password):
        users = self.getUserInfoById(user_id)
        if users:
            return "该用户不存在，请重新登录"
        else:
            user = users[0]
            if user.get('password') == old_password:
                self.pg.db.update("user_info", where="id=%s" % user_id, password=new_password)
                return "0"
            else:
                return "密码错误"

    @daemonDB
    def getUserInfoById(self, user_id):
        sql = "select * from user_info where id=%s " % user_id
        return list(self.pg.db.query(sql))


if __name__ == '__main__':
    pass
