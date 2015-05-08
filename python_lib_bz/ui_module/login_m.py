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
from hashlib import md5
import urllib2

salt = "hold is watching you"
captcha_id = "a90c68898a94d4bca5825facf40d07d7"
private_key = "ff897f66927e005f30a654c782cdd0e7"


class geetest(object):

    """docstring for gt 极验证"""

    def __init__(self, id, key):
        self.PRIVATE_KEY = key
        self.CAPTCHA_ID = id
        self.PY_VERSION = "2.15.4.1.1"

    def geetest_register(self):
        apireg = "http://api.geetest.com/register.php?"
        regurl = apireg + "gt=%s" % self.CAPTCHA_ID
        try:
            result = urllib2.urlopen(regurl, timeout=2).read()
        except:
            result = ""
        return result

    def geetest_validate(self, challenge, validate, seccode):
        apiserver = "http://api.geetest.com/validate.php"
        if validate == self.md5value(self.PRIVATE_KEY + 'geetest' + challenge):
            query = 'seccode=' + seccode + "&sdk=python_" + self.PY_VERSION
            print query
            backinfo = self.postvalues(apiserver, query)
            if backinfo == self.md5value(seccode):
                return 1
            else:
                return 0
        else:
            return 0

    def postvalues(self, apiserver, data):
        req = urllib2.Request(apiserver)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        response = opener.open(req, data)
        backinfo = response.read()
        return backinfo

    def md5value(self, values):
        m = md5()
        m.update(values)
        return m.hexdigest()


class login_m(my_ui_module.MyUIModule):

    '''登录的页面'''

    def render(self, oauth2, user_types=[]):
        gt = geetest(captcha_id, private_key)
        challenge = gt.geetest_register()
        BASE_URL = "api.geetest.com/get.php?gt="
        if len(challenge) == 32:
            url = "http://%s%s&challenge=%s" % (BASE_URL, captcha_id, challenge)
            print url
            #httpsurl = "https://%s%s&challenge=%s" % (BASE_URL, captcha_id, challenge)
        return self.render_string(self.html_name, oauth2=oauth2, user_types=user_types, url=url)


class login(ModuleHandler, UserInfoHandler):

    '''
    登录后台的方法
    '''

    def initialize(self):
        '''
        针对 oauth2 ,需要你重载的时候来设置为你自己的参数, 以下是 google twitter douban 的例子
        modify by bigzhu at 15/04/26 21:56:09 对应的oauth登录的参数,应该在对应的oauth里面来设置,这里不用再设置了
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
        #是否要验证
        self.validate = False

    def get(self):
        self.myRender(oauth2=self.oauth2)

    @tornado_bz.handleError
    def post(self):
        self.set_header("Content-Type", "application/json")
        login_info = json.loads(self.request.body)
        form_type = login_info.get("type")
        if form_type == 'login':
            user_name = login_info.get("user_name")
            password = login_info.get("password")
            if self.validate:
                #验证码
                geetest_challenge = login_info.get("geetest_challenge")
                geetest_validate = login_info.get("geetest_validate")
                geetest_seccode = login_info.get("geetest_seccode")
                gt = geetest(captcha_id, private_key)
                result = gt.geetest_validate(geetest_challenge, geetest_validate, geetest_seccode)
                if not result:
                    raise Exception('验证码不正确!')
            # 密码加密
            hashed_password = hashlib.md5(password + salt).hexdigest()
            user_info = self.user_oper.login(user_name, hashed_password)
            self.set_secure_cookie("user_id", str(user_info.id))
        elif form_type == 'signup':
            user_name = login_info.get("user_name")
            password = login_info.get("password")
            email = login_info.get("email")
            # 用户是否存在应该注册提交前判断,这里再次判断
            user_info = self.user_oper.getUserInfo(user_name=user_name)
            if user_info:
                raise Exception('用户已经存在!可能是那一瞬间被抢注了.真遗憾,换一个吧')
            hashed_password = hashlib.md5(password + salt).hexdigest()

            user_type = login_info.get("user_type", 'my')

            self.user_oper.signup(user_name, hashed_password, email, user_type)
            user_info = self.user_oper.login(user_name, hashed_password, "'%s'" % user_type)
            self.set_secure_cookie("user_id", str(user_info.id))
        elif form_type == 'forget':  # 如果是找回密码
            email = login_info.get("email")
            user_info = self.user_oper.getUserInfo(email=email)
            if not user_info:
                raise Exception('没有邮箱为%s的用户!' % email)
            forget_token = str(uuid.uuid4())
            # if len(data_token[0].forget_token) > 1:
            #     forget_token = data_token[0].forget_token

            sql_set_token = "update user_info set forget_token = '%s' where email = '%s' and user_type = 'my'" % (forget_token, email)
            self.pg.db.query(sql_set_token)
            send_mail = 'safe@highwe.com'
            url = 'http://' + self.request.host + self.request.uri + '#token/' + forget_token
            #content = MIMEText(loader.load("login_email_m.html").generate(user_name=email, url=url), 'html', 'utf-8')
            content = MIMEText('<a href="' + url + '">点此设置新密码</a><br><br>如果以上按钮点击无效，请将链接复制到浏览器地址栏中打开：<br>' + url, 'html', 'utf-8')
            content['From'] = send_mail
            content['To'] = email

            content['Subject'] = '找回密码'
            send_mail = self.settings.get('send_mail', 'hold@highwe.com')
            sendMail(email, content, send_mail, 'highwe123')
        elif form_type == 'setPassword':  # 设置新密码
            password = login_info.get("password")
            hashed_password = hashlib.md5(password + salt).hexdigest()
            token = login_info.get("token")
            count = self.pg.db.update('user_info', where="forget_token = '%s'" % token, password=hashed_password, forget_token='')
            if count == 0:
                raise Exception('token 已经失效,请不要重复提交!')
        self.write(json.dumps({'error': '0'}, cls=public_bz.ExtEncoder))

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
    import doctest
    doctest.testmod()
