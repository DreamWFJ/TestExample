# -*- coding: utf-8 -*-
# ===================================
# ScriptName : run.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-03 15:10
# ===================================

from flask import Flask
from user import user_blueprint
from example import example_blueprint
app = Flask(__name__)

app.register_blueprint(user_blueprint, url_prefix='/api/v1.0')
app.register_blueprint(example_blueprint, url_prefix='/api/v1.0')

if __name__ == '__main__':
    app.run(debug=True)
    