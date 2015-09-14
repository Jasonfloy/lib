#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
http 相关操作
'''
from urlparse import urlparse
import public_bz
import urllib2
import json


def getUrlLastPath(url):
    '''
    create by bigzhu at 15/07/10 11:47:28 获取url最后一个path,用于twiiter取用户名
    >>> getUrlLastPath("https://twitter.com/Cluvmmy")
    'Cluvmmy'
    '''
    path = urlparse(url).path
    last_path = path.split('/')
    return last_path[-1]


def removeUrlLastPath(url):
    '''
    create by bigzhu at 15/07/22 13:07:03 删除url最后一组的path,用来follow center的more上使用
    >>> removeUrlLastPath("http://follow.center/main/200")
    'http://follow.center/main/'
    '''
    last_path = getUrlLastPath(url)
    url = url.replace(last_path, '')
    return url


def getCountryCodeByIP(ip):
    '''
    根据 ip 地址取到所属的国家编码
    modify by bigzhu at 15/05/17 11:28:52 add test
    >>> getCountryCodeByIP('www.bigzhu.org')
    u'US'
    '''
    country_code = "not found"
    url = 'http://freegeoip.net/json/' + ip
    try:
        info = urllib2.urlopen(url, timeout=10).read()
        info = json.loads(info)
        if info.get('country_code') != '':
            country_code = info.get('country_code')
    except Exception:
        print public_bz.getExpInfoAll()
    return country_code

if __name__ == '__main__':
    print removeUrlLastPath("https://twitter.com/Cluvmmy/200")
