#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:         WFJ
Version:        0.1.0
FileName:       article.py
CreateTime:     2016-11-26 16:18
"""
import json
import tornado.web

class ToManageArticleHTML(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render("blog/manage_article.html")

class ManageArticleHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render("blog/manage_article.html")

    def post(self, *args, **kwargs):
        return_data = {
            "rows":[
                {
                    '_id': '123',
                    'name': 'title',
                    'ip': '192.168.10.123',
                    'auth':'root',
                    # 'auth_user': 'root',
                    # 'auth_passwd': 'root',
                    'node_status': 1,
                    'last_detect_time':1480318164.2178299
                },
                {
                    '_id': '124',
                    'name': 'title',
                    'ip': '10.100.10.135',
                    'auth':'root',
                    # 'auth_user': 'root',
                    # 'auth_passwd': 'root',
                    'node_status': 0,
                    'last_detect_time':1480318164.2178299
                }
            ],
            "total": 2
        }
        self.write(json.dumps(return_data))

    def delete(self, *args, **kwargs):
        pass
