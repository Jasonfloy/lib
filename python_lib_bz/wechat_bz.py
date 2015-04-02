#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
create by bigzhu at 15/04/01 13:30:11  微信相关的操作和接口
modify by bigzhu at 15/04/01 16:18:35  修改为依赖 pip install wechat-sdk 的版本,简化代码
'''

import requests
from wechat_sdk import WechatBasic


class WeChat():

    '''
    '''

    def __init__(self, app_id, app_secret, token):
        self.app_id = app_id
        self.app_secret = app_secret

    def getAccessToken(self):
        """
        create by bigzhu at 15/04/01 14:05:44 获取 accesstoken, 根据时效性缓存的以后再做
        """
        params = {
            "appid": self.app_id,
            "secret": self.app_secret,
            "grant_type": "client_credential"
        }
        result = requests.get("https://api.weixin.qq.com/cgi-bin/token", params=params).json()
        access_token = result['access_token']
        return {'access_token': access_token}

    def getWeChatIP(self):
        '''
        create by bigzhu at 15/04/01 14:34:08 获取微信的 server 的 ip
        '''
        return requests.get("https://api.weixin.qq.com/cgi-bin/getcallbackip", params=self.getAccessToken()).json()

    def addKF(self, acct, name, passwd):
        '''
        create by bigzhu at 15/04/01 14:34:29 添加客服   客服账号,客服名称,客服密码 (参数错误)
        '''
        kf = {
            "kf_account": acct,
            "nickname": name,
            "password": passwd,
        }
        return requests.post("https://api.weixin.qq.com/customservice/kfaccount/add", params=self.getAccessToken(), data=kf).json()

if __name__ == '__main__':
    wechat = WechatBasic(token='JbBqbzuji22PF2db1K381Z2JdcdbUIBF', appid='wxb853fa08cbc04938', appsecret='01a74260fd9db2460a5ef3052a8aa830')
    #print wechat.get_access_token()
    print wechat.get_menu()
    # print we_chat.getAccessToken()
    # print we_chat.getWeChatIP()
    #print we_chat.addKF('bigzhu','大猪', '123')
