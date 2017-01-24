#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:         WFJ
Version:        0.1.0
FileName:       settings.py
CreateTime:     2016-11-26 15:39
"""
import os
import sys
from tornado.options import options, define
MAIN_PATH = sys.path[0]
sys.path.append(MAIN_PATH)
from src.router import ui_modules
DOWNLOAD_PATH = os.path.join(MAIN_PATH, "download")
# 设置下载文件的路径环境变量
os.environ["DOWNLOAD_LOG_PATH"] = os.path.join(DOWNLOAD_PATH, "log")
os.environ["DOWNLOAD_SCRIPT_PATH"] = os.path.join(DOWNLOAD_PATH, "script")
os.environ["PROJECT_MAIN_PATH"] = MAIN_PATH
os.environ["PROJECT_DATABASE_PATH"] = os.path.join(MAIN_PATH, "test.sqlite")

define('port', default=8080, help='run on the given port', type=int)
define('debug', default=True, help='run on the give debug', type=bool)

global_settings = {
    'template_path': os.path.join(os.path.dirname(__file__), "templates"),
    'static_path': os.path.join(os.path.dirname(__file__), "static"),
    'cookie_secret': "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
    'debug': options.debug,
    # 'xsrf_cookies': True,
    'login_url': "/login",
    "ui_modules":ui_modules
}

