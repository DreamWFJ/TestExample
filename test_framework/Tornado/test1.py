# -*- coding: utf-8 -*-
# ===================================
# ScriptName : test1.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2016-09-14 14:28
# ===================================

import tornado.web
import tornado.httpserver
import tornado.options
import tornado.ioloop
import os.path

from tornado.options import options, define
define('port', default=8080, help='run on the given port', type=int)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
            "test1.html",
            page_title = "Burt't Books | Home",
            header_text = "Welcome to Burt's Books!",
        )

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),
        ]
        settings = dict(
            template_path = os.path.join(os.path.dirname(__file__), "templates"),
            static_path = os.path.join(os.path.dirname(__file__), "static"),
            debug = True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    # 该例子中不同的地方在于使用了类Application去初始化路由，配置文件信息
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
    