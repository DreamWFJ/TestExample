# -*- coding: utf-8 -*-
# ==================================
# Author        : WFJ
# ScriptName    : test_cookie.py
# CreateTime    : 2016-09-16 19:01
# ==================================

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import os.path

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class BaseHandler(tornado.web.RequestHandler):
    # 请求处理类有一个current_user属性,可以用来存储为当前请求进行用户验证的标识。其默认值为None。
    # 为了authenticated装饰器能够成功标识一个已认证用户，
    # 你必须覆写请求处理程序中默认的get_current_user()方法来返回当前用户
    def get_current_user(self):
        return self.get_secure_cookie("username")

class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        # 可以使用像self.redirect(self.get_argument('next', '/'))这样的行来重定向登录后用户回到的页面
        self.set_secure_cookie("username", self.get_argument("username"))
        self.redirect("/")

class WelcomeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('test2.html', user=self.current_user)

class LogoutHandler(BaseHandler):
    def get(self):
        if (self.get_argument("logout", None)):
            self.clear_cookie("username")
            self.redirect("/")

if __name__ == "__main__":
    tornado.options.parse_command_line()

    settings = {
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
        "xsrf_cookies": True,
        "login_url": "/login"
    }

    application = tornado.web.Application([
        (r'/', WelcomeHandler),
        (r'/login', LoginHandler),
        (r'/logout', LogoutHandler)
    ], **settings)

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
