# -*- coding: utf-8 -*-
# ===================================
# ScriptName : user.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-03 16:52
# ===================================

from flask import Blueprint, abort
from jinja2 import TemplateNotFound

user_blueprint = Blueprint('user_blueprint', __name__,
                        template_folder='templates')

@user_blueprint.route('/<page>')
def show(page):
    try:
        pass
    except TemplateNotFound:
        abort(404)


if __name__ == '__main__':
    pass
    