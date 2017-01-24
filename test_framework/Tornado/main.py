# -*- coding: utf-8 -*-
# ===================================
# ScriptName : main.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2016-09-14 10:46
# ===================================
import os.path
import random

import tornado.httpserver
import tornado.web
import tornado.options
import tornado.ioloop

from tornado.options import define, options
define('port', default=8080, help='run on the given port', type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('main_index.html')

class MungedPageHandler(tornado.web.RequestHandler):
    def map_by_first_letter(self, text):
        mapped = dict()
        for line in text.split('\r\n'):
            for word in [x for x in line.split(' ') if len(x) > 0]:
                if word[0] not in mapped: mapped[word[0]] = []
                mapped[word[0]].append(word)

        return mapped
    def post(self):
        source_text = self.get_argument('source')
        text_to_change = self.get_argument('change')
        source_map = self.map_by_first_letter(source_text)
        change_lines = text_to_change.split('\r\n')
        self.render('munged.html', source_map=source_map, change_lines=change_lines,
                choice=random.choice)



if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[(r'/', IndexHandler), (r'/poem', MungedPageHandler)],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        # 这2行分别说明了模板路径和静态文件路径，在引用静态文件时，需要使用函数static_url()
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        # 开启调试模式
        debug=True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
    