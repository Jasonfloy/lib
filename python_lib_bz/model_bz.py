#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
create by bigzhu at 15/04/06 20:13:37 存放公用的数据模型
'''
from peewee import TextField
from peewee import IntegerField
from peewee import DateTimeField
from peewee import BooleanField
from peewee import Model
from playhouse.postgres_ext import JSONField


class base(Model):
    created_date = DateTimeField(null=True)
    stat_date = DateTimeField(null=True)
    is_delete = BooleanField(null=True, default=False)
    user_id = IntegerField(null=True)


class user_info(base):

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


class comment(base):

    '''
    create by bigzhu at 15/04/06 20:34:12 通用的评论表模型
    '''
    key_type = TextField()  # 用于那个类型 比如一个系统有多个地方都要有评论,则用这个来区别, 站点可以填为 site'
    key = TextField()  # 比如填入 site_id, 使用这个评论的元素
    comment = TextField()  # 评论
    parent_id = IntegerField()  # 可空,父节点 id
    user_id = IntegerField()


class crud_conf(base):

    '''
    create by bigzhu at 15/04/17 13:22:53 curd模块用到的
    '''
    name = TextField()  # 字段的名字
    description = TextField()  # 字段的描述 用于显示在 form 的前面
    options = JSONField(null=True)  # select 类型的字段的 value 和 desc json 格式存储
    table_name = TextField()  # 表名 冗余,但是我不想用 id 了
    grid_show = IntegerField(null=True)  # 是否在 grid 显示
    c_type = TextField(null=True)  #
    seq = IntegerField(null=True)  # DEFAULT 0, -- 排列顺序
    sql_parm = TextField(null=True)  #
    is_search = IntegerField(null=True)  # 是否要在高级搜索里出现


class timeline(base):
    oper = TextField()  # 执行的动作
    target_type = TextField()  # 执行的目标对象
    target_id = IntegerField()  # 目标的 id, 用于表关联
    other_info = JSONField(null=True)  # 其他的附加信息, 使用 json 来存放
    user_id = IntegerField()

if __name__ == '__main__':
    pass
