#!/usr/bin/env python
# -*- coding: utf-8 -*-


import tornado.web
import tornado_bz
import json
import hashlib
import user_bz
import public_bz
import tornado_auth_bz

import uuid
from email.MIMEText import MIMEText
from sendmail_bz import sendMail
from tornado_bz import UserInfoHandler
from tornado_bz import ModuleHandler
from tornado_bz import BaseHandler
from public_bz import storage
from ui_module import my_ui_module

salt = "hold is watching you"


class login_m(my_ui_module.MyUIModule):

    '''登录的页面'''

    def render(self, oauth2):
        return self.render_string(self.html_name, oauth2=oauth2)


class login(ModuleHandler, UserInfoHandler):

    '''
    登录后台的方法
    '''

    def initialize(self):
        '''
        针对 oauth2 ,需要你重载的时候来设置为你自己的参数, 以下是 google twitter douban 的例子

        # google 登录的参数
        CLIENT_ID = '413021385046-mgcrb8l8qnc3kdg8h9tq3857ae71idke.apps.googleusercontent.com'
        CLIENT_SECRET = 'hygluwSg-7L_WsifSC5-4OZ5'
        self.settings["google_oauth"] = {
            "key": CLIENT_ID,
            "secret": CLIENT_SECRET,
            "redirect_uri": "http://www.highwe.net/google",
        }
        # twitter
        self.settings["twitter_consumer_key"] = 'YmQK6YdczdtjMPLsHjoVs8QgH'
        self.settings["twitter_consumer_secret"] = 'ZM1fklU38SBQN5RBwvRH1yRttrrHjBS5uuOtqIqUObIGafgeRG'
        # douban
        self.settings["douban_api_key"] = '01be463aa2868092053ad2afe79381b6'
        self.settings["douban_api_secret"] = 'a957e7c9cc366f86'
        self.settings["redirect_uri"] = 'http://highwe.net/douban'
        '''
        UserInfoHandler.initialize(self)
        oauth2 = storage()
        oauth2.google = storage(enabled=False, url='/google')
        oauth2.twitter = storage(enabled=False, url='/twitter')
        oauth2.douban = storage(enabled=False, url='/douban')
        oauth2.github = storage(enabled=False, url='/github')
        self.oauth2 = oauth2

        # 用户操作相关的
        self.user_oper = user_bz.UserOper(self.pg)

    def get(self):
        self.myRender(oauth2=self.oauth2)

    @tornado_bz.handleError
    def post(self):
        self.set_header("Content-Type", "application/json")
        login_info = json.loads(self.request.body)
        form_type = login_info.get("type")
        if form_type == 'login':  # 如果是登录
            user_name = login_info.get("user_name")
            password = login_info.get("password")
            email = login_info.get("email")
            # 密码加密
            hashed_password = hashlib.md5(password + salt).hexdigest()
            user_info = self.user_oper.login(user_name, hashed_password, email)
            self.set_secure_cookie("user_id", str(user_info.id))
            self.write(json.dumps({'error': '0'}, cls=public_bz.ExtEncoder))
        elif form_type == 'forget':  # 如果是找回密码
            email = login_info.get("email")
            sql_token = "select forget_token from user_info where email = '%s' and user_type = 'my'" % email
            data_token = self.pg.db.query(sql_token)
            if len(data_token) < 1:
                self.write(json.dumps({'error': len(data_token)}, cls=public_bz.ExtEncoder))
                return
            forget_token = str(uuid.uuid4())
            # if len(data_token[0].forget_token) > 1:
            #     forget_token = data_token[0].forget_token

            sql_set_token = "update user_info set forget_token = '%s' where email = '%s' and user_type = 'my'" % (forget_token, email)
            self.pg.db.query(sql_set_token)
            url = 'http://' + self.request.host + self.request.uri + '#token/' + forget_token
            #content = MIMEText(loader.load("login_email_m.html").generate(user_name=email, url=url), 'html', 'utf-8')
            content = MIMEText('<a href="' + url + '">点此设置新密码</a><br><br>如果以上按钮点击无效，请将链接复制到浏览器地址栏中打开：<br>' + url, 'html', 'utf-8')
            content['From'] = 'hold@highwe.com'
            content['To'] = email

            content['Subject'] = '找回密码'
            sendMail(content['To'], content)

            self.write(json.dumps({'result': '成功'}, cls=public_bz.ExtEncoder))
        elif form_type == 'setPassword':  # 设置新密码
            password = login_info.get("password")
            hashed_password = hashlib.md5(password + salt).hexdigest()
            token = login_info.get("token")
            sql_verify = "select forget_token from user_info where forget_token = '%s' and user_type = 'my'" % token
            data_verify = self.pg.db.query(sql_verify)
            if len(data_verify) < 1:
                self.write(json.dumps({'error': len(data_verify)}, cls=public_bz.ExtEncoder))
                return
            sql_set_password = "update user_info set password = '%s' , forget_token = '' where forget_token = '%s' and user_type = 'my'" % (hashed_password, token)
            self.pg.db.query(sql_set_password)
            self.write(json.dumps({'result': '成功'}, cls=public_bz.ExtEncoder))

    @tornado_bz.handleError
    def put(self):
        self.set_header("Content-Type", "application/json")
        reset_data = json.loads(self.request.body)
        user_id = self.get_secure_cookie("user_id")
        old_password = reset_data.get("old_password")
        new_password = reset_data.get("new_password")
        # 加密
        hashed_old_pwd = hashlib.md5(old_password + salt).hexdigest()
        hashed_new_pwd = hashlib.md5(new_password + salt).hexdigest()
        error_msg = self.user_oper.resetPassword(user_id, hashed_old_pwd, hashed_new_pwd)
        self.write(json.dumps({'error': error_msg}, cls=public_bz.ExtEncoder))


class logout(BaseHandler):

    @tornado_bz.handleError
    def get(self):
        self.clear_cookie(name='user_id')
        self.redirect("/")


class google(BaseHandler, tornado.auth.GoogleOAuth2Mixin):

    '''
    显而易见, google 登录
    '''

    def initialize(self):
        BaseHandler.initialize(self)

    @tornado.gen.coroutine
    def get(self):
        redirect_uri = self.settings['google_oauth']['redirect_uri']
        if self.get_argument('code', False):
            user = yield self.get_authenticated_user(
                redirect_uri=redirect_uri,
                code=self.get_argument('code')
            )
            self.user = user
            user_info = self.getUserInfo()
            self.user_oper = user_bz.UserOper(self.pg)
            user_info = self.user_oper.googleLogin(user_info)
            self.set_secure_cookie("user_id", str(user_info.id))
            self.redirect("/")
            # Save the user with e.g. set_secure_cookie
        else:
            yield self.authorize_redirect(
                redirect_uri=redirect_uri,
                client_id=self.settings['google_oauth']['key'],
                scope=['profile', 'email'],
                response_type='code',
                extra_params={'approval_prompt': 'auto'})

    def getUserInfo(self):
        token = self.user.get('access_token')
        import requests

        response = requests.get('https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token=%s' % token)
        return response.json()


class twitter(BaseHandler, tornado.auth.TwitterMixin):
    _OAUTH_REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
    _OAUTH_ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"
    _OAUTH_AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize"
    _OAUTH_AUTHENTICATE_URL = "https://api.twitter.com/oauth/authenticate"
    _OAUTH_NO_CALLBACKS = False
    _TWITTER_BASE_URL = "https://api.twitter.com/1.1"

    def initialize(self):
        BaseHandler.initialize(self)

    @tornado.gen.coroutine
    def get(self):
        if self.get_argument("oauth_token", None):
            user_info = yield self.get_authenticated_user()

            self.user_oper = user_bz.UserOper(self.pg)
            user_info = self.user_oper.twitterLogin(user_info)
            self.set_secure_cookie("user_id", str(user_info.id))
            self.redirect("/")

            # Save the user using e.g. set_secure_cookie()
        else:
            yield self.authorize_redirect()


class github(BaseHandler, tornado_auth_bz.GithubOAuth2Mixin):

    def initialize(self):
        BaseHandler.initialize(self)

    @tornado.gen.coroutine
    def get(self):
        # if we have a code, we have been authorized so we can log in
        if self.get_argument("code", False):
            user = yield self.get_authenticated_user(
                redirect_uri=self.settings['github_oauth']['redirect_uri'],
                client_id=self.settings['github_oauth']['client_id'],
                client_secret=self.settings['github_oauth']['client_secret'],
                code=self.get_argument("code"),
                extra_fields="user:email"
            )

            self.user_oper = user_bz.UserOper(self.pg)
            user_info = self.user_oper.githubLogin(user)
            self.set_secure_cookie('user_id', str(user_info.id))
            self.redirect('/')

        else:
            yield self.authorize_redirect(
                redirect_uri=self.settings['github_oauth']['redirect_uri'],
                client_id=self.settings['github_oauth']['client_id'],
                extra_params={
                    "scope": "user:email",
                }
            )


class douban(BaseHandler, tornado_auth_bz.DoubanOAuth2Mixin):

    def initialize(self):
        BaseHandler.initialize(self)

    @tornado.gen.coroutine
    def get(self):
        if self.get_argument('code', False):
            # 获取到个人信息
            user = yield self.get_authenticated_user(
                redirect_uri=self.settings['redirect_uri'],
                code=self.get_argument('code')
            )
            if user:

                self.user_oper = user_bz.UserOper(self.pg)
                user_info = self.user_oper.doubanLogin(user)
                self.set_secure_cookie("user_id", str(user_info.id))
                self.redirect("/")

                # self.set_secure_cookie("user_id", str(user['uid']))
                # self.redirect(self.get_argument("next", "/"))
        else:
            yield self.authorize_redirect(
                redirect_uri=self.settings['redirect_uri'],
                client_id=self.settings['douban_api_key'],
                scope=None,  # 使用默认的scope权限
                response_type='code'
            )


if __name__ == '__main__':
    pass
