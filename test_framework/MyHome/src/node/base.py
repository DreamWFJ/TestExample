# -*- coding: utf-8 -*-
# ===================================
# ScriptName : base.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2016-12-01 14:54
# ===================================
import time
import tornado.web

class BaseHandler(tornado.web.RequestHandler):
    def prepare(self):
        self.db = self.application.db
        self.node_ssh_conn_pools = self.application.node_ssh_conn_pools


def time2float(s):
    return time.mktime(time.strptime(s,'%Y-%m-%d %H:%M:%S'))