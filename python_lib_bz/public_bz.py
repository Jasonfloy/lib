#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import traceback
import json
import time
import datetime
import decimal
import urllib2

import os


class ExtEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, datetime.datetime) or isinstance(o, datetime.date):
            return time.mktime(o.timetuple()) * 1000
        elif isinstance(o, decimal.Decimal):
            return float(o)
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


def analyzeStrTable(str_table, title_list, start_with, end_with=None):
    '''
    解析抓取回来的 str table
    转换为 storage 列表,类似从数据库中查出的 data list

    :str_table 需要拆分的 str
    :title_list title 指定切片的对应的 title, 对并表的列名
    :start_with 从哪一行开始,一般会自己带着一列 title, 那么要从1行开始
    :end_with 一些末尾会有多余的空行,需要抛弃
    '''
    title_len = len(title_list)
    li = str_table.split('\n')
    li = li[start_with:end_with]
    li = [i.split() for i in li]
    table = []
    for i in li:
        d = storage()
        for n, v in enumerate(i):
            if n >= title_len:
                d[title_list[title_len - 1]] += ' ' + v
            else:
                d[title_list[n]] = v
        table.append(d)
    return table


def getExecutingPathFile():
    '''
    返回当前执行的 python 文件,带路径
    '''
    # return inspect.getfile(inspect.currentframe()) # script filename
    # (usually with path)
    return os.path.abspath(sys.argv[0])


def getExecutingPath():
    '''
    返回当前执行的 python 文件所在路径
    '''
    # return
    # os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    # script directory
    dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
    return dirname


def runCommand(command):
    '''
    运行命令
    '''
    try:
        p = os.popen(command)
        content = p.read()
        p.close()
    except Exception:
        content = 'djoin_error:' + getExpInfo(True)
    return content


def getCountryCodeByIP(ip):
    '''
    根据 ip 地址取到所属的国家编码
    '''
    country_code = "not found"
    url = 'http://freegeoip.net/json/' + ip
    try:
        info = urllib2.urlopen(url, timeout=10).read()
        info = json.loads(info)
        if info.get('country_code') != '':
            country_code = info.get('country_code')
    except Exception:
        print getExpInfoAll()
    return country_code

if __name__ == '__main__':
    getCountryCodeByIP('www.douban.com')
