#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
create by bigzhu at 15/04/06 20:13:37 存放公用的数据模型
'''
import db_init_bz
from peewee import TextField

class user_info(db_init_bz.base):

    '''
    create by bigzhu at 15/04/04 00:47:38 用户表
    '''
    user_type = TextField()  # 用户类型 google my twitter
    out_id = TextField(null=True)  # oauth2 的外部 id
    email = TextField(null=True)  # email 地址
    user_name = TextField()  # 用户名
    link = TextField(null=True)  # 链接
    picture = TextField(null=True)  # 头像地址
    gender = TextField(null=True)  # ?
    locale = TextField(null=True)  # 所在区域
    password = TextField(null=True)  # 密码
    original_json = TextField(null=True)  # ?
    slogan = TextField(null=True)  # 自定义头像
if __name__ == '__main__':
    pass
