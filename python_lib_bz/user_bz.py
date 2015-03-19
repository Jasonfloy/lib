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
    def login(self, user_name, password, email=None):
        '''
        modify by bigzhu at 15/02/25 13:57:19 加入唯一约束
        modify by bigzhu at 15/03/08 14:24:57 加入 email; 根据 email 来判断是注册还是登录

        登录模块,如果不存在这个用户名,则注册
        数据模型:


        -- Table: user_info

        -- DROP TABLE user_info;

        CREATE TABLE user_info
        (
        -- 继承 from table base:  id integer NOT NULL DEFAULT nextval('base_id_seq'::regclass),
        -- 继承 from table base:  created_date timestamp without time zone DEFAULT now(),
        -- 继承 from table base:  stat_date timestamp without time zone DEFAULT now(),
          user_type text,
          out_id text,
          email text,
          user_name text,
          link text,
          picture text,
          gender text,
          locale text,
          password text,
          original_json text,
          CONSTRAINT user_info_out_id_key UNIQUE (out_id)
        )
        INHERITS (base)
        WITH (
          OIDS=FALSE
        );


        '''
        user_infos = self.getUserInfo(user_name=user_name)
        if user_infos:
            if user_infos[0].password == password:
                return user_infos[0]
            else:
                if email is None:
                    raise Exception('密码错误!')
                else:
                    raise Exception('用户已经存在!')
        else:
            self.pg.db.insert('user_info', user_type='my', user_name=user_name, password=password, email=email)
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
            self.pg.db.insert('user_info',
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
                              out_id=user_info.get('id'),
                              # email=user_info['email'],
                              user_name=user_info.get('name'),
                              link=user_info.get('alt'),
                              picture=user_info.get('avatar'),
                              # gender=user_info['gender'],
                              locale=user_info.get('loc_name')
                              )
            return self.doubanLogin(user_info)

    @daemonDB
    def githubLogin(self, user_info):
        '''
        github 登录信息存到 db 中
            {
             "id": "112340346785758313259",
             "email": "vermiliondun@gmail.com",
             "name": "朱一凡",
             "link": "https://plus.google.com/112340346785758313259",
             "picture": "https://lh5.googleusercontent.com/-E4rb72RaQHE/AAAAAAAAAAI/AAAAAAAAJzQ/p-tx9D78Mik/photo.jpg",
             "locale": "zh-CN"
            }
        '''
        user_infos = self.getUserInfo(user_type='github', out_id=user_info['id'])
        if user_infos:
            return user_infos[0]
        else:
            self.pg.db.insert('user_info',
                              user_type = 'github',
                              out_id = user_info['id'],
                              email = user_info['email'],
                              user_name = user_info['name'],
                              #link = user_info['html_url'],
                              picture = user_info['avatar_url'],
                              locale = user_info['location']
                              )
            return self.githubLogin(user_info)

    @daemonDB
    def resetPassword(self, user_id, old_password, new_password):
        users = self.getUserInfoById(user_id)
        if not users:
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
        users = list(self.pg.db.select("user_info", where="id=%s" % user_id, limit=1))
        return users


if __name__ == '__main__':
    pass
