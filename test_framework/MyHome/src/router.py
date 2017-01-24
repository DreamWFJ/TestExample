#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:         WFJ
Version:        0.1.0
FileName:       router.py
CreateTime:     2016-11-26 15:38
"""
from tornado.web import url
from src.node.views import ManageNodeHandler, ToManageNodeHTML
from src.blog.article import ManageArticleHandler
from src.node.task import ToNodeTaskHTML, NodeBingTaskHandler, ToManageTaskHTML, ManageTaskHandler
from src.node.ctrl_terminal import ToCtrlTerminalHTML, CtrlTerminalHandler, TerminalModule, TerminalInteractHandler
from src.node.download_file import DownloadFileHandler

route_urls = [
    url(r'/manage/node', ToManageNodeHTML),
    url(r'/manage/node/data', ManageNodeHandler),

    url(r'/manage/timetask', ToManageTaskHTML),
    url(r'/manage/timetask/data', ManageTaskHandler),

    url(r'/node/timetask', ToNodeTaskHTML),
    url(r'/node/timetask/data', NodeBingTaskHandler),

    url(r'/node/terminal', ToCtrlTerminalHTML),
    url(r'/node/terminal/data', CtrlTerminalHandler),

    url(r'/terminal/interact', TerminalInteractHandler),
    url(r'/download/file', DownloadFileHandler),

    url(r'/manage/article', ManageArticleHandler)
]

ui_modules = {
    "Terminal": TerminalModule
}

if __name__ == '__main__':
    pass