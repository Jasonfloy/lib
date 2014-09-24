#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
jinja2 模板相关的公用代码
'''
from jinja2 import Environment, FileSystemLoader
import os
path = os.getcwd()
env = Environment(loader=FileSystemLoader(path + '/template'))


def getTemplate(file_name):
    '''
    返回 jinja2 template 模板
    模板放在当前目录的 /template 目录
    必须是.html 后缀
    '''
    template = env.get_template(file_name + '.html')
    return template

if __name__ == '__main__':
    pass
