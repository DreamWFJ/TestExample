# -*- coding: utf-8 -*-
# ==================================
# Author        : WFJ
# ScriptName    : tweet_rate.py
# CreateTime    : 2016-09-16 11:36
# ==================================

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.httpclient
import tornado.options
import tornado.gen

import urllib
import json
import datetime
import time

from tornado.options import define, options
define('port', default=8000, help='run on the given port', type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        query = self.get_argument('q')
        client = tornado.httpclient.HTTPClient()
        # fetch方法返回的HTTPResponse对象允许你访问HTTP响应的任何部分，不只是body
        response = client.fetch("http://search.twitter.com/search.json?" +\
                                urllib.urlencode({'query':query, 'result_type':'recent', 'rpp':100}))
        body = json.loads(response.body)
        result_count = len(body['results'])
        now = datetime.datetime.utcnow()
        raw_oldest_tweet_at = body['results'][-1]['created_at']
        oldest_tweet_at = datetime.datetime.strptime(raw_oldest_tweet_at,
                        "%a, %d %b %Y %H:%M:%S +0000")
        seconds_diff = time.mktime(now.timetuple()) - \
                time.mktime(oldest_tweet_at.timetuple())
        tweets_per_second = float(result_count) / seconds_diff
        self.write("""
        <div style="text-align: center">
            <div style="font-size: 72px">%s</div>
            <div style="font-size: 144px">%.02f</div>
            <div style="font-size: 24px">tweets per second</div>
        </div>""" % (query, tweets_per_second))

    # 添加异步请求的装饰
    # 记住当你使用@tornado.web.asynchonous装饰器时，Tornado永远不会自己关闭连接。
    # 你必须在你的RequestHandler对象中调用finish方法来显式地告诉Tornado关闭连接。
    # （否则，请求将可能挂起，浏览器可能不会显示我们已经发送给客户端的数据。）
    @tornado.web.asynchronous
    def get(self):
        query = self.get_argument('q')
        client = tornado.httpclient.AsyncHTTPClient()
        client.fetch("http://search.twitter.com/search.json?" + \
                urllib.urlencode({"q": query, "result_type": "recent", "rpp": 100}),
                callback=self.on_response)

    def on_response(self, response):
        body = json.loads(response.body)
        result_count = len(body['results'])
        now = datetime.datetime.utcnow()
        raw_oldest_tweet_at = body['results'][-1]['created_at']
        oldest_tweet_at = datetime.datetime.strptime(raw_oldest_tweet_at,
                "%a, %d %b %Y %H:%M:%S +0000")
        seconds_diff = time.mktime(now.timetuple()) - \
                time.mktime(oldest_tweet_at.timetuple())
        tweets_per_second = float(result_count) / seconds_diff
        self.write("""
<div style="text-align: center">
    <div style="font-size: 72px">%s</div>
    <div style="font-size: 144px">%.02f</div>
    <div style="font-size: 24px">tweets per second</div>
</div>""" % (self.get_argument('q'), tweets_per_second))
        self.finish()


class IndexHandler1(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        query = self.get_argument('q')
        client = tornado.httpclient.AsyncHTTPClient()
        # 在同一个函数中实现异步，不像上面例子，分别需要管理请求和回调函数
        response = yield tornado.gen.Task(client.fetch,
                "http://search.twitter.com/search.json?" + \
                urllib.urlencode({"q": query, "result_type": "recent", "rpp": 100}))
        body = json.loads(response.body)
        result_count = len(body['results'])
        now = datetime.datetime.utcnow()
        raw_oldest_tweet_at = body['results'][-1]['created_at']
        oldest_tweet_at = datetime.datetime.strptime(raw_oldest_tweet_at,
                "%a, %d %b %Y %H:%M:%S +0000")
        seconds_diff = time.mktime(now.timetuple()) - \
                time.mktime(oldest_tweet_at.timetuple())
        tweets_per_second = float(result_count) / seconds_diff
        self.write("""
<div style="text-align: center">
    <div style="font-size: 72px">%s</div>
    <div style="font-size: 144px">%.02f</div>
    <div style="font-size: 24px">tweets per second</div>
</div>""" % (query, tweets_per_second))
        self.finish()

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", IndexHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()