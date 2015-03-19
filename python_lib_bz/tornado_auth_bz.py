#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
基于 Oauth2 的登录
'''
import tornado.httputil
import tornado.httpclient
import tornado.web
import tornado.gen
import urllib
import logging
import functools

from tornado.auth import AuthError
from tornado.auth import OAuth2Mixin
from tornado.auth import _auth_return_future
from tornado.concurrent import return_future
from tornado import escape


class DoubanMixin(object):

    @return_future
    def authorize_redirect(self, redirect_uri=None, client_id=None,
                           client_secret=None, extra_params=None,
                           callback=None, scope=None, response_type="code"):
        args = {
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'response_type': response_type
        }
        if scope:
            args['scope'] = ' '.join(scope)

        self.redirect(
            tornado.httputil.url_concat(self._OAUTH_AUTHORIZE_URL, args))  # 跳转到认证页面
        callback()

    def _oauth_request_token_url(self, redirect_uri=None, client_id=None, client_secret=None, code=None):
        url = self._OAUTH_ACCESS_TOKEN_URL
        args = dict(
            client_id=client_id,
            redirect_uri=redirect_uri,
            client_secret=client_secret,
            grant_type="authorization_code",
            code=code
        )
        return tornado.httputil.url_concat(url, args)


class DoubanOAuth2Mixin(DoubanMixin):
    _OAUTH_ACCESS_TOKEN_URL = 'https://www.douban.com/service/auth2/token'
    _OAUTH_AUTHORIZE_URL = 'https://www.douban.com/service/auth2/auth?'

    def get_auth_http_client(self):
        return tornado.httpclient.AsyncHTTPClient()

    @_auth_return_future
    def get_authenticated_user(self, redirect_uri, code, callback):
        http = self.get_auth_http_client()
        body = urllib.urlencode({
            'redirect_uri': redirect_uri,
            'code': code,
            'client_id': self.settings['douban_api_key'],
            'client_secret': self.settings['douban_api_secret'],
            "grant_type": "authorization_code",
        })

        http.fetch(self._OAUTH_ACCESS_TOKEN_URL, functools.partial(self._on_access_token, callback),
                   method="POST", body=body)

    def _on_access_token(self, future, response):
        if response.error:
            future.set_exception(AuthError('Douban Auth Error: %s' % str(response)))
            return
        args = escape.json_decode(response.body)
        # future.set_result(args)
        self.get_user_info(access_token=args['access_token'],
                           callback=functools.partial(self._on_get_user_info, future))

    def _on_get_user_info(self, future, user):
        if user is None:
            future.set_result(None)
            return
        future.set_result(user)

    @_auth_return_future
    def get_user_info(self, access_token, callback):
        url = 'https://api.douban.com/v2/user/~me'
        http = tornado.httpclient.AsyncHTTPClient()
        req = tornado.httpclient.HTTPRequest(url, headers={"Authorization": "Bearer " + access_token})
        http.fetch(req, functools.partial(self._on_get_user_request, callback))

    def _on_get_user_request(self, future, response):
        if response.error:
            future.set_exception(AuthError('Error response fetching',
                                           response.error, response.request.url))
            return
        future.set_result(escape.json_decode(response.body))


class GithubOAuth2Mixin(OAuth2Mixin):
    """ Github OAuth Mixin, based on FacebookGraphMixin
    """
 
    _OAUTH_AUTHORIZE_URL = 'https://github.com/login/oauth/authorize'
    _OAUTH_ACCESS_TOKEN_URL = 'https://github.com/login/oauth/access_token'
    _API_URL = 'https://api.github.com'
 
    def get_authenticated_user(self, redirect_uri, client_id, client_secret,
                              code, callback, extra_fields=None):
        """ Handles the login for Github, queries /user and returns a user object
        """
        logging.debug('gau ' + redirect_uri)
        http = tornado.httpclient.AsyncHTTPClient()
        args = {
          "redirect_uri": redirect_uri,
          "code": code,
          "client_id": client_id,
          "client_secret": client_secret,
        }
 
        http.fetch(self._oauth_request_token_url(**args),
            self.async_callback(self._on_access_token, redirect_uri, client_id,
                                client_secret, callback, fields))
 
    def _on_access_token(self, redirect_uri, client_id, client_secret,
                        callback, fields, response):
        """ callback for authentication url, if successful get the user details """
        if response.error:
            logging.warning('Github auth error: %s' % str(response))
            callback(None)
            return
 
        args = tornado.escape.parse_qs_bytes(
                tornado.escape.native_str(response.body))
 
        if 'error' in args:
            logging.error('oauth error ' + args['error'][-1])
            raise Exception(args['error'][-1])
 
        session = {
            "access_token": args["access_token"][-1],
        }
 
        self.github_request(
            method="/user",
            callback=self.async_callback(
                self._on_get_user_info, callback, session),
            access_token=session["access_token"],
            )
 
    def _on_get_user_info(self, callback, session, user):
        """ callback for github request /user to create a user """
        logging.debug('user data from github ' + str(user))
        if user is None:
            callback(None)
            return
        callback({
            "login": user["login"],
            "name": user["name"],
            "email": user["email"],
            "access_token": session["access_token"],
        })
 
    def github_request(self, path, callback, access_token=None,
                method='GET', body=None, **args):
        """ Makes a github API request, hands callback the parsed data """
        args["access_token"] = access_token
        url = tornado.httputil.url_concat(self._API_URL + path, args)
        logging.debug('request to ' + url)
        http = tornado.httpclient.AsyncHTTPClient()
        if body is not None:
            body = tornado.escape.json_encode(body)
            logging.debug('body is' +  body)
        http.fetch(url, callback=self.async_callback(
                self._parse_response, callback), method=method, body=body)
 
    def _parse_response(self, callback, response):
        """ Parse the JSON from the API """
        if response.error:
            logging.warning("HTTP error from Github: %s", response.error)
            callback(None)
            return
        try:
            json = tornado.escape.json_decode(response.body)
        except Exception:
            logging.warning("Invalid JSON from Github: %r", response.body)
            callback(None)
            return
        if isinstance(json, dict) and json.get("error_code"):
            logging.warning("Facebook error: %d: %r", json["error_code"],
                            json.get("error_msg"))
            callback(None)
            return
        callback(json)

if __name__ == '__main__':
    pass
