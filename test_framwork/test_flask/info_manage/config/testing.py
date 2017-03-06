# -*- coding: utf-8 -*-
# ===================================
# ScriptName : testing.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-06 15:36
# ===================================

from .default import Config

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    PROPAGATE_EXCEPTIONS = True
    PRESERVE_CONTEXT_ON_EXCEPTION = True
    SECRET_KEY = 'test'
    LOGGER_NAME = 'test'
    TRAP_HTTP_EXCEPTIONS = True
    TRAP_BAD_REQUEST_ERRORS = True