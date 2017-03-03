# -*- coding: utf-8 -*-
# ===================================
# ScriptName : authentication.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-03 16:36
# ===================================
from flask_httpauth import HTTPBasicAuth


auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == 'ok':
        return 'python'
    return None


    