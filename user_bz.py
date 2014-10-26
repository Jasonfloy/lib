#!/usr/bin/env python
# -*- coding: utf-8 -*-

def login(user_name, password, pg):
    '''
    登录模块,如果不存在这个用户名,则注册
    '''
    user_infos = pg.getUserInfo(user_name)
    if user_infos:
        if user_infos[0].password == password:
            return user_infos[0]
        else:
            raise Exception('密码错误!')
    else:
        pg.db.insert(
            'user_info',
            user_name=user_name,
            password=password)
        return login(user_name, password)
if __name__ == '__main__':
    pass
