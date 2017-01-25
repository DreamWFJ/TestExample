# -*- coding: utf-8 -*-
# ===================================
# ScriptName : hello.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-01-24 15:08
# ===================================

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    raise
    return 'Hello world!'



if __name__ == '__main__':
    app.debug = True
    app.run()
    