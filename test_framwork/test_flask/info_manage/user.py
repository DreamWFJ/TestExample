# -*- coding: utf-8 -*-
# ===================================
# ScriptName : user.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-03 16:52
# ===================================

from flask import jsonify, abort, Blueprint, request, url_for
from db import get_db

user_blueprint = Blueprint('user_blueprint', __name__,
                        template_folder='templates')

def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task


@user_blueprint.route('/users', methods=['GET'])
def get_users():
    db = get_db()
    cur = db.execute('select * from entries order by id desc')
    entries = cur.fetchall()
    return jsonify({'users': entries})


@user_blueprint.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

@user_blueprint.route('/users', methods=['POST'])
def create_user():
    db = get_db()
    db.execute('insert into entries (title, text) values (?, ?)',
               [request.form['title'], request.form['text']])
    db.commit()
    return jsonify({'task': task}), 201

@user_blueprint.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

@user_blueprint.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})