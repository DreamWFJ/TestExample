# -*- coding: utf-8 -*-
# ===================================
# ScriptName : exception.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2016-09-20 17:05
# ===================================


class InvalidJson(Exception):
    message = "invalid json data"

class InvalidRequestArgs(Exception):
    message = "invalid request parameters"

class InvalidUsername(Exception):
    message = "username is invalid"

class InvalidPhoneNum(Exception):
    message = "phone number is invalid"

class RWMongoDBError(Exception):
    message = "read or write mongodb error"