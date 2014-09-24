#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import traceback
import json
import time
import datetime
import decimal


class ExtEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, datetime.datetime) or isinstance(o, datetime.date):
            return time.mktime(o.timetuple()) * 1000
        elif isinstance(o, decimal.Decimal):
            return int(o)
        # Defer to the superclass method
        return json.JSONEncoder(self, o)


def getExpInfoAll(just_info=False):
    '''得到Exception的异常'''
    if just_info:
        info = sys.exc_info()
        return str(info[1])
    else:
        return traceback.format_exc()


def getExpInfo():
    '''得到Exception的异常'''
    return getExpInfoAll(True)


class Storage(dict):

    """
    Storage 就是把 python 的字典的 get set 方法 override 了
    这样用起来比较方便
        >>> o = storage(a=1)
        >>> o.a
        1
        >>> o['a']
        1
        >>> o.a = 2
        >>> o['a']
        2
        >>> del o.a
        >>> o.a
        Traceback (most recent call last):
            ...
        AttributeError: 'a'

    """

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __repr__(self):
        return '<Storage ' + dict.__repr__(self) + '>'

storage = Storage


if __name__ == '__main__':
    pass
