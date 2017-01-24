# -*- coding: utf-8 -*-
# ===================================
# ScriptName : definitions_readonly.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2016-09-14 18:20
# ===================================
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os.path
import pymongo

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
            "index.html",
            page_title = "Burt's Books | Home",
            header_text = "Welcome to Burt's Books!",
        )

class RecommendedHandler(tornado.web.RequestHandler):
    def get(self):
        coll = self.application.db.books
        books = coll.find()
        self.render(
            "recommended.html",
            page_title = "Burt's Books | Recommended Reading",
            header_text = "Recommended Reading",
            books = books
        )

class BookModule(tornado.web.UIModule):
    def render(self, book):
        return self.render_string(
            "modules/book.html",
            book=book,
        )
    def css_files(self):
        return "/static/css/recommended.css"
    def javascript_files(self):
        return "/static/js/recommended.js"


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/(\w+)", WordHandler),
            (r"/", MainHandler),
            (r"/recommended/", RecommendedHandler),
            (r"/edit/([0-9Xx\-]+)", BookEditHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            ui_modules={"Book": BookModule},
            debug=True,
        )
        conn = pymongo.MongoClient("localhost", 27017)
        self.db = conn["example"]
        tornado.web.Application.__init__(self, handlers, **settings)

class BookEditHandler(tornado.web.RequestHandler):
    def get(self, isbn=None):
        book = dict()
        if isbn:
            coll = self.application.db.books
            book = coll.find_one({"isbn": isbn})
        self.render("book_edit.html",
            page_title="Burt's Books",
            header_text="Edit book",
            book=book)

    def post(self, isbn=None):
        import time
        book_fields = ['isbn', 'title', 'subtitle', 'image', 'author',
            'date_released', 'description']
        coll = self.application.db.books
        book = dict()
        if isbn:
            book = coll.find_one({"isbn": isbn})
        for key in book_fields:
            book[key] = self.get_argument(key, None)

        if isbn:
            coll.save(book)
        else:
            book['date_added'] = int(time.time())
            coll.insert(book)
        self.redirect("/recommended/")

class WordHandler(tornado.web.RequestHandler):
    # 一旦我们在Application对象中添加了db属性，我们就可以在任何RequestHandler对象中使用self.application.db访问它
    def get(self, word):
        coll = self.application.db.words
        word_doc = coll.find_one({"word": word})
        if word_doc:
            del word_doc["_id"]
            self.write(word_doc)
        else:
            self.set_status(404)
            self.write({"error": "word not found"})

    def post(self, word):
        definition = self.get_argument("definition")
        coll = self.application.db.words
        word_doc = coll.find_one({"word": word})
        if word_doc:
            word_doc['definition'] = definition
            coll.save(word_doc)
        else:
            word_doc = {'word': word, 'definition': definition}
            coll.insert(word_doc)
        del word_doc["_id"]
        self.write(word_doc)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
    