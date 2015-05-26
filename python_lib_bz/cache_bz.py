#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
临时的 cache
'''
cache = {}


def put(data, key):
    '''
    create by bigzhu at 15/05/26 14:48:23 简化版本的缓存
    '''
    global cache
    cache[key] = data
    return data


def get(key):
    global cache
    return cache.get(key)


def test():
    global cache
    return cache

if __name__ == '__main__':
    print get('cpu_mem_io_top')
