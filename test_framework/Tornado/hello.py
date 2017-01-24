# -*- coding: utf-8 -*-
# ===================================
# ScriptName : hello.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2016-09-13 16:32
# ===================================

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import textwrap
import os.path
'''
textwrap
    wrap(text, width = 70, **kwargs):这个函数可以把一个字符串拆分成一个序列，每个元素的长度是一样的
    fill(text, width=70, **kwargs) :该方法可以根据指定的长度，进行拆分字符串，然后逐行显示
    dedent()方法->文本进行不缩进显示，相应的indent()方法 -> 进行缩进显示
'''

from tornado.options import define, options
# options可以从命令行中解析参数，并作为属性存在于实例中，如果没有输入该参数，则使用默认值，type是对类型校验
define('port', default=8091, help='run on the given port', type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        # 从查询字符串中获取参数
        greeting = self.get_argument('greeting', 'Hello')
        self.write(greeting + ', Friendly user!')
    def write_error(self, status_code, **kwargs):
        self.write('Gosh darnit, user! You caused a %d error.' %status_code)

class ReverseHandler(tornado.web.RequestHandler):
    def get(self, input):
        print "input: ",input
        self.write(input[::-1])

class WrapHandler(tornado.web.RequestHandler):
    def post(self):
        text = self.get_argument('text')
        width = self.get_argument('width', 40)
        self.write(textwrap.fill(text, int(width)))

    def write_error(self, status_code, **kwargs):
        self.write('Gosh darnit, user! You caused a %d error.' %status_code)

# Tornado支持任何合法的HTTP请求（GET、POST、PUT、DELETE、HEAD、OPTIONS）
class WidgetHandler(tornado.web.RequestHandler):
    def get(self, widget_id):
        widget = retrieve_from_db(widget_id)
        self.write(widget.serialize())

    def post(self, widget_id):
        widget = retrieve_from_db(widget_id)
        widget['foo'] = self.get_argument('foo')
        save_to_db(widget)

def retrieve_from_db(widget_id):
    return widget_id

def save_to_db(widget):
    pass

class HelloHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('hello.html')

class HelloModule(tornado.web.UIModule):
    def render(self):
        return '<h1>Hello World!</h1>'

class BookModule(tornado.web.UIModule):
    def render(self, book):
        return self.render_string('modules/book.html', book=book)

    # 嵌入JavaScript
    def embedded_javascript(self):
        return "document.write(\"embedded_javascript()\")"

    # 嵌入CSS
    def embedded_css(self):
        return ".book {background-color:#F5F5F5}"

    # 在闭合</body>标签前添加完整的HTML标记
    def html_body(self):
        return "<script>document.write(\"html_body\")</script>"

    def html_head(self):
        return "<script>document.write(\"html_head\")</script>"

    # 添加样式表和JS
    def css_files(self):
        return "/static/css/newreleases.css"
    def javascript_files(self):
        return "https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.14/jquery-ui.min.js"

class RecommendedHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
            "recommended.html",
            page_title="Burt's Books | Recommended Reading",
            header_text="Recommended Reading",
            books=[
                {
                    "title":"Programming Collective Intelligence",
                    "subtitle": "Building Smart Web 2.0 Applications",
                    "image":"/static/images/collective_intelligence.jpg",
                    "author": "Toby Segaran",
                    "date_added":1310248056,
                    "date_released": "August 2007",
                    "isbn":"978-0-596-52932-1",
                    "description":"<p>This fascinating book demonstrates how you "
                        "can build web applications to mine the enormous amount of data created by people "
                        "on the Internet. With the sophisticated algorithms in this book, you can write "
                        "smart programs to access interesting datasets from other web sites, collect data "
                        "from users of your own applications, and analyze and understand the data once "
                        "you've found it.</p>"
                }
            ]
        )


if __name__ == '__main__':
    # 解析命令行
    tornado.options.parse_command_line()
    # 创建一个app,其中handler是处理句柄，指定uri对应的处理方法
    app = tornado.web.Application(
        handlers=[
            (r"/", IndexHandler),
            (r"/reverse/(\w+)", ReverseHandler),
            (r"/wrap", WrapHandler),
            (r"/hello", HelloHandler),
            (r"/book", RecommendedHandler)
        ],
        # 指定模板路径
        template_path = os.path.join(os.path.dirname(__file__), 'templates'),
        # 指定渲染html的module
        ui_modules={
            'Hello': HelloModule,
            'Book': BookModule,
        },
        # 这2行分别说明了模板路径和静态文件路径，在引用静态文件时，需要使用函数static_url()
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        # 开启调试模式
        debug=True
    )

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()