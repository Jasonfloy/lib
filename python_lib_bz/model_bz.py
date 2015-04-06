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

class comment(db_init_bz.base):
    '''
    create by bigzhu at 15/04/06 20:34:12 通用的评论表模型
    '''
    key_type  = TextField()  # 用于那个类型 比如一个系统有多个地方都要有评论,则用这个来区别, 站点可以填为 site'
    key   = TextField()  # 比如填入 site_id, 使用这个评论的元素
    comment   = TextField()  # 评论
    parent_id  = IntegerField() # 可空,父节点 id
    user_id = IntegerField()

if __name__ == '__main__':
    pass
