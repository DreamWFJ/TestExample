# -*- coding: utf-8 -*-
# ===================================
# ScriptName : flaskr.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-01-24 17:31
# ===================================

import sqlite3
# 内容管理工具，实现with xxx as xx
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash

# configuration
DATABASE = 'flaskr.db'
DEBUG = True
SECRET_KEY = 'Development key'
USERNAME = 'Admin'
PASSWORD = 'Default'

app = Flask(__name__)
# 这一行中，from_object() 会查看给定的对象（如果该对象是一个字符串就会 直接导入它），搜索对象中所有变量名均为大字字母的变量。
app.config.from_object(__name__)
# 通常，从一个配置文件中导入配置是比较好的做法，我们使用 from_envvar() 来完成这个工作，把上面的 from_object() 一行替换为
# app.config.from_envvar('FLASKR_SETTINGS', silent=True)， 这样做就可以设置一个 FLASKR_SETTINGS 的环境变量来指定一个配置文件，并 根据该文件来重载缺省的配置。 silent 开关的作用是告诉 Flask 如果没有这个环境变量 不要报错


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    # init_db()
    # 运行服务器后，会发现只有你自己的电脑可以使用服务，而网络中的其他电脑却不行。 缺省设置就是这样的，因为在调试模式下该应用的用户可以执行你电脑中的任意 Python 代码
    # 如果你关闭了 调试 或信任你网络中的用户，那么可以让服务器被公开访问, 修改host='0.0.0.0'即可
    app.run(host='0.0.0.0', port=10101)
    