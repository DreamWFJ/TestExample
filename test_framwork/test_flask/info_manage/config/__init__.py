# -*- coding: utf-8 -*-
# ===================================
# ScriptName : __init__.py.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-06 15:31
# ===================================

'''
加载config
def create_app():
    """创建Flask app"""
    app = Flask(__name__)

    # Load config
    config = load_config()
    app.config.from_object(config)


使用config
from flask import current_app

config = current_app.config
SITE_DOMAIN = config.get('SITE_DOMAIN')

'''
import os

def load_config():
    """加载配置类"""
    # 这里可以修改命令行传入
    mode = os.environ.get('MODE')
    try:
        if mode == 'PRODUCTION':
            from .production import ProductionConfig
            return ProductionConfig
        elif mode == 'TESTING':
            from .testing import TestingConfig
            return TestingConfig
        else:
            from .development import DevelopmentConfig
            return DevelopmentConfig
    except ImportError, e:
        from .default import Config
        return Config
    