# -*- coding: utf-8 -*-
# ===================================
# ScriptName : poemmaker.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2016-09-14 10:02
# ===================================
import os.path
import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver

from tornado.options import define, options
define('port', default=8080, help='run on the give port', type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class PoemPageHandler(tornado.web.RequestHandler):
    def post(self):
        noun1 = self.get_argument('noun1')
        noun2 = self.get_argument('noun2')
        verb = self.get_argument('verb')
        noun3 = self.get_argument('noun3')
        self.render('poem.html', roads=noun1, wood=noun2, made=verb, difference=noun3)

'''
模板语法
    填充表达式
        可以将任何python表达式放在双大括号中,注意模板中取字典的变量是用dict['key']的方式
        >>> from tornado.template import Template
        >>> print Template("{{ 1+1 }}").generate()   ---> 2
        >>> print Template("{{ 'scrambled eggs'[-4:] }}").generate()   ---> eggs
        >>> print Template("{{ ', '.join([str(x*x) for x in range(10)]) }}").generate()   ---> 0, 1, 4, 9, 16, 25, 36, 49, 64, 81

    控制流语句
        {% if page is None %}
        或
        {% if len(entries) == 3 %}

        {% for book in books %}
            <li>{{ book }}</li>
        {% end %}
        使用{% set foo = 'bar' %}来设置变量

    在模板中使用函数
        escape(s)
        替换字符串s中的&、<、>为他们对应的HTML字符。
        url_escape(s)
        使用urllib.quote_plus替换字符串s中的字符为URL编码形式。
        json_encode(val)
        将val编码成JSON格式。（在系统底层，这是一个对json库的dumps函数的调用。查阅相关的文档以获得更多关于该函数接收和返回参数的信息。）
        squeeze(s)
        过滤字符串s，把连续的多个空白字符替换成一个空格。

        编写自己的函数传入模板
            >>> from tornado.template import Template
            >>> def disemvowel(s):
            ...     return ''.join([x for x in s if x not in 'aeiou'])
            ...
            >>> disemvowel("george")
            'grg'
            >>> print Template("my name is {{d('mortimer')}}").generate(d=disemvowel)
            my name is mrtmr
    块和替换
        通过extends和block语句支持模板继承
            {% extends "filename.html" %}
            {% block header %}{% end %}
    自动转义
        {% set mailLink = "<a href="mailto:contact@burtsbooks.com">Contact Us</a>" %}
        {{ mailLink }}'

        {% autoescape None %}
        {{ mailLink }}
        默认是开启转义，使用{% raw %}指令不转义
        {% raw mailLink %}

'''

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r'/', IndexHandler),
            (r'/poem', PoemPageHandler)
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates")
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()