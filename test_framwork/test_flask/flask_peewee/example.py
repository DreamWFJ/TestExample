# -*- coding: utf-8 -*-
# ===================================
# ScriptName : example.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-21 15:16
# ===================================

import datetime
from flask import Flask
from flask_peewee.auth import Auth
from flask_peewee.db import Database
from peewee import *

# configure our database
DATABASE = {
    'name': 'example.db',
    'engine': 'peewee.SqliteDatabase',
}
DEBUG = True
SECRET_KEY = 'ssshhhh'

app = Flask(__name__)
app.config.from_object(__name__)

# instantiate the db wrapper
db = Database(app)


class Note(db.Model):
    message = TextField()
    created = DateTimeField(default=datetime.datetime.now)


# create an Auth object for use with our flask app and database wrapper
auth = Auth(app, db)


if __name__ == '__main__':
    auth.User.create_table(fail_silently=True)
    Note.create_table(fail_silently=True)

    app.run()