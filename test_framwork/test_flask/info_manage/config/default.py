# -*- coding: utf-8 -*-
# ===================================
# ScriptName : default.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-06 15:35
# ===================================
import os
from .. import BASE_DIR

class Config(object):
    DATABASE_URI = 'sqlite3:///' + os.path.join(BASE_DIR, 'app.db')