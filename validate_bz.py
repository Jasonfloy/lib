#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
一些验证
'''
import re
VALID_ADDRESS_REGEXP = "^([a-z0-9]*[-_]?[a-z0-9]+)*@([a-z0-9]*[-_]?[a-z0-9]+)+[\.][a-z]{2,3}([\.][a-z]{2})?$"
def validateEmail(email):
    '''
    create by bigzhu at 15/07/03 14:08:12
        如果 return None, 那么验证不通过
    '''
    return re.match(VALID_ADDRESS_REGEXP, email)
if __name__ == '__main__':
    print 'bigzhu'
    assert re.match(VALID_ADDRESS_REGEXP, 'bigzhu@1') is not None
