# -*- coding: utf-8 -*-
# ==================================
# Author        : WFJ
# ScriptName    : example.py
# CreateTime    : 2016-09-17 10:22
# ==================================

from tornado.httpclient import HTTPClient
from tornado.httpclient import AsyncHTTPClient
from tornado.concurrent import Future

# 同步模式
def synchronous_fetch(url):
    http_client = HTTPClient()
    response = http_client.fetch(url)
    return response.body

# 异步模式
def asynchronous_fetch(url, callback):
    http_client = AsyncHTTPClient()
    def handle_response(response):
        callback(response.body)
    http_client.fetch(url, callback=handle_response)

# 使用Future的异步模式，内部为协程
def async_fetch_future(url):
    http_client = AsyncHTTPClient()
    my_future = Future()
    fetch_future = http_client.fetch(url)
    fetch_future.add_done_callback(
        lambda f: my_future.set_result(f.result()))
    return my_future


from tornado import gen

@gen.coroutine
def fetch_coroutine(url):
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(url)
    raise gen.Return(response.body)


if __name__ == '__main__':
    pass
