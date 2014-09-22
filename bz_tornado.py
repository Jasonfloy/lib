#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado


def getURLMap(the_globals):
    '''
        根据定义的tornado.web.RequestHandler,自动生成url map
    '''
    url_map = []
    for i in the_globals:
        try:
            if issubclass(the_globals[i], tornado.web.RequestHandler):
                url_map.append((r'/' + i, the_globals[i]))
                url_map.append((r"/%s/([0-9]+)" % i, the_globals[i]))
        except TypeError:
            continue
    return url_map


if __name__ == '__main__':
    pass
