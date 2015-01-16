#!/usr/bin/env python
# -*- coding: utf-8 -*-
import public_bz
import psycopg2
import functools
import time


def daemonDB(method):
    '''
    自动重连数据库的一个装饰器
    '''
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        try:
            return method(self, *args, **kwargs)
        except(psycopg2.OperationalError, psycopg2.InterfaceError):
            print public_bz.getExpInfo()
            self.pg.connect()
            time.sleep(5)
            return wrapper(self, *args, **kwargs)
            print '重新连接数据库'
    return wrapper
if __name__ == '__main__':
    pass
