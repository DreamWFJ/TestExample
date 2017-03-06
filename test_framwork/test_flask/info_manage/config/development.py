# -*- coding: utf-8 -*-
# ===================================
# ScriptName : development.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-06 15:37
# ===================================

from .default import Config

class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URI = 'sqlite://:memory:'
    