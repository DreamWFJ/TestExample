# -*- coding: utf-8 -*-
# ===================================
# ScriptName : example.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-17 17:23
# ===================================


from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)
    