# -*- coding: utf-8 -*-
# ===================================
# ScriptName : production.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-06 15:37
# ===================================
from .default import Config

class ProductionConfig(Config):
    DEBUG = False
    