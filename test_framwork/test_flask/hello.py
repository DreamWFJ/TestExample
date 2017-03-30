# -*- coding: utf-8 -*-
# ===================================
# ScriptName : models.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-23 16:42
# ===================================
import os
import hashlib
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

basedir = os.path.abspath(os.path.dirname(__file__))

_db = SQLAlchemy()

db = _db



# 角色表
class Role(db.Model):
    __tablename__ = 'roles'
    _id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    enabled = db.Column(db.Boolean, default = True, index = True)
    users = db.relationship('User', backref='role')
    create_at = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    # 用户名名称
    name = db.Column(db.String(64), unique = True, index = True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.name


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite').replace('\\', '\/')
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    db.init_app(app)
    return app