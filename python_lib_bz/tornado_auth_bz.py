#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
基于 Oauth2 的登录
'''
import urllib
from core.options import options
from tornado import httpclient


class oAuth2Base:
    authurl = user_info_url = tokenurl = ''

    def get_params(self, params={}):
        """
        生成参数
        """
        def_params = {
            "client_id": self.client_id,
            "redirect_uri": options.oAuth2_redirect_url,
        }
        def_params.update(params)
        return urllib.urlencode(def_params)

    def request(self, HTTPRequest, callback):
        """
         异步请求数据
        """
        client = httpclient.AsyncHTTPClient()
        client.fetch(HTTPRequest, callback)

    def get_authorization_code(self, state, scope=None):
        """
        第一步：
        获取 authorization code
        得到一个URL，需要重定向到此地址
        """
        params = {
            "response_type": "code",
            "state": state
        }
        if scope:
            params.update({"scope": scope})
        return self.authurl + '?' + self.get_params(params)

    def get_access_token(self, code, callback):
        """
        第二步：
        返回到 redirect_uri之后会获取到一个code
        此方法可以根据code换取access_token，然后访问API
        """
        params = {
            "client_secret": self.client_secret,
            "grant_type": "authorization_code",
            "code": code,
        }
        request = httpclient.HTTPRequest(
            self.tokenurl,
            method='POST',
            body=self.get_params(params)
        )
        self.request(request, callback)


class douban(oAuth2Base):
    authurl = 'https://www.douban.com/service/auth2/auth'
    tokenurl = "https://www.douban.com/service/auth2/token"
    user_info_url = 'https://api.douban.com/v2/user/~me'

    @property
    def client_id(self):
        return options.oAuth2_douban_key

    @property
    def client_secret(self):
        return options.oAuth2_douban_secret

    @property
    def scope(self):
        return options.oAuth2_douban_scope

    def get_user_info(self, access_token, callback):
        """
        获取用户资料
        """
        request = httpclient.HTTPRequest(
            'https://api.douban.com/v2/user/~me',
            headers={"Authorization": "Bearer " + access_token}
        )
        self.request(request, callback)


class qq(oAuth2Base):
    authurl = "https://graph.qq.com/oauth2.0/authorize"
    tokenurl = "https://graph.qq.com/oauth2.0/token"
    user_info_url = "https://graph.qq.com/user/get_user_info"

    @property
    def client_id(self):
        return options.oAuth2_qq_appid

    @property
    def client_secret(self):
        return options.oAuth2_qq_key

    @property
    def scope(self):
        return options.oAuth2_qq_scope


if __name__ == '__main__':
    pass
