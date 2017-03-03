# -*- coding: utf-8 -*-
# ===================================
# ScriptName : error.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-03 16:39
# ===================================
from flask import make_response, jsonify
from authentication import auth
from run import app

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    pass
    