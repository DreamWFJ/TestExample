# -*- coding: utf-8 -*-
# ===================================
# ScriptName : test_1.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2016-10-19 17:38
# ===================================

"""
1. 封装数据库操作(INSERT,FIND,UPDATE)
2. 函数执行完MONGODB操作后关闭数据库连接
"""
import pymongo
import time
import traceback
from bson import ObjectId
from functools import wraps
from pymongo.database import Database

try:
    from pymongo import MongoClient
except ImportError:
    # 好像2.4之前的pymongo都没有MongoClient,现在官网已经把Connection抛弃了
    import warnings
    warnings.warn("Strongly recommend upgrading to the latest version pymongo version,"
                  "Connection is DEPRECATED: Please use mongo_client instead.")
    from pymongo import Connection as MongoClient


class Tools(object):
    def __init__(self):
        pass
    def get_str_time(self):
        return time.strftime('%Y-%m-%d %X', time.localtime())
    def get_float_time(self):
        return time.time()
    def get_int_time(self):
        return int(time.time())

    def convert_to_object(self, id_list):
        try:
            ret_list = []
            for temp_id in id_list:
                if isinstance(temp_id, ObjectId):
                    ret_list.append(temp_id)
                    continue
                else:
                    ret_list.append(ObjectId(temp_id))
            return ret_list
        except:
            traceback.print_exc()

    def convert_to_list(self, cursor):
        ret_list = []
        for temp_dict in cursor:
            ret_list.append(temp_dict)
        return ret_list

    def convert_object_to_str(self, cursor):
        ret_list = []
        if isinstance(cursor, list):
            for one in cursor:
                if isinstance(one, ObjectId):
                    ret_list.append(str(one))
        else:
            ret_list.append(str(cursor))
        return ret_list

class ParserParam(object):
    def __init__(self):
        self.conditions = {}
    def parser_update(self, param_dict={}):
        dbname = param_dict.get('dbname', '')
        tablename = param_dict.get('tablename', '')
        conditions = param_dict.get('param', {})
        contents = param_dict.get('contents', {})
        upsert = bool(param_dict.get('upsert', False))
        multi = param_dict.get('multi', False)
        return dbname, tablename, conditions, contents, upsert, multi


    def parser_find(self, param_dict={}):
        dbname = param_dict.get('dbname', '')
        tablename = param_dict.get('tablename', '')
        conditions = param_dict.get('param', {})
        contents = param_dict.get('contents', {})
        sort_dict = param_dict.get('sort', {'_id':-1})
        limit_nums = param_dict.get('limit', 0)
        skip_nums = param_dict.get('skip', 0)
        return dbname, tablename, conditions, contents, sort_dict, limit_nums, skip_nums

    def parser_find_one(self, param_dict={}):
        dbname = param_dict.get('dbname', '')
        tablename = param_dict.get('tablename', '')
        conditions = param_dict.get('param', {})
        contents = param_dict.get('contents', {})
        return dbname, tablename, conditions, contents

    def parser_remove(self, param_dict={}):
        dbname = param_dict.get('dbname', '')
        tablename = param_dict.get('tablename', '')
        conditions = param_dict.get('param', {})
        return dbname, tablename, conditions

    def parser_drop(self, param_dict={}):
        dbname = param_dict.get('dbname', '')
        tablename = param_dict.get('tablename', '')
        return dbname,tablename

    def parser_insert(self, param_dict={}):
        dbname = param_dict.get('dbname', '')
        tablename = param_dict.get('tablename', '')
        contents = param_dict.get('contents', {})
        return dbname, tablename, contents

class MongodbHandle(Tools, ParserParam):

    '''封装数据库操作'''

    def __init__(self, host='localhost', port=27017, dbname='test', tablename='', max_pool_size=10, timeout=10):
        self.host = host
        self.port = port
        self.max_pool_size = max_pool_size
        self.timeout = timeout
        self.dbname = dbname
        self.tablename = tablename

    def connect(self):
        return MongoClient(self.host, self.port, self.max_pool_size, connectTimeoutMS=60 * 60 * self.timeout)

    def init_conn(self, host, port, user, passwd):
        self.set_right(host, port, user, passwd)
        self.conn = self.connect()

    def set_right(self, host, port, user, passwd):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd

    def auth_right(self):
        self.change_dbname('admin')
        self.db_conn.authenticate(self.user, self.passwd)

    def get_new_conn(self, host='', port=27017, user='', passwd=''):
        if host == '':
            host = self.host
        port = self.port
        if user == '':
            user = self.user
        if passwd == '':
            passwd = self.passwd
        self.init_conn(host, port, user, passwd)
        self.auth_right()

    def close_conn(self):
        self.conn.close()

    def show_conn_info(self):
        print "--------------------------- db connection info ---------------------------"
        print "conn             = ", self.conn
        print "db_conn          = ", self.db_conn
        print "db_table_conn    = ", self.db_table_conn

    def show_info(self):
        print "--------------------------- right info ---------------------------"
        print "info : ip=%s | port=%d | user=%s | passwd=%s | dbname=%s | tablename=%s" %(self.host, self.port, self.user, self.passwd, self.dbname, self.tablename)


    def change_dbname(self, dbname):
        self.dbname = dbname
        self.db_conn = self.conn[dbname]

    def change_tablename(self, tablename):
        self.tablename = tablename
        self.db_table_conn = self.db_conn[tablename]

    def change_db_table(self, dbname, tablename):
        self.change_dbname(dbname)
        self.change_tablename(tablename)

    def add_user(self, user, passwd):
        self.change_dbname('admin')
        self.conn.add_user(user, passwd)

    def db_insert(self, param_dict={}):
        try:
            cursor = None
            dbname, tablename, contents = self.parser_insert(param_dict)
            if dbname and tablename:
                self.change_db_table(dbname, tablename)
            if contents:
                cursor = self.db_table_conn.insert(contents, manipulate=True, safe=True, check_keys=True, continue_on_error=False)
                return self.convert_object_to_str(cursor)
            else:
                raise ValueError("insert argument 'contents' cannot be null")
        except:
            traceback.print_exc()

    def db_update(self, param_dict={}):
        try:
            cursor = None
            dbname, tablename, conditions, contents, upsert_flag, multi_flag = self.parser_update(param_dict)
            if dbname and tablename:
                self.change_db_table(dbname, tablename)
            if conditions and contents:
                cursor = self.db_table_conn.update(conditions, contents, upsert=upsert_flag, manipulate=True, safe=True, multi=multi_flag)
                print cursor
                if cursor.get('err') == None:
                    return 1 #update success
                else:
                    return 0 #update failed
            else:
                raise ValueError("update argument 'param or contents' cannot be null")
        except:
            traceback.print_exc()

    def db_remove(self, param_dict={}):
        try:
            cursor = None
            dbname, tablename, conditions = self.parser_remove(param_dict)
            if dbname and tablename:
                self.change_db_table(dbname, tablename)
            if conditions:
                cursor = self.db_table_conn.remove(conditions, safe=True)
                print cursor
                if cursor.get('err') == None:
                    return 1 #update success
                else:
                    return 0 #update failed
                return cursor
            else:
                raise ValueError("remove argument 'param' cannot be null")
        except:
            traceback.print_exc()

    def db_drop(self, param_dict={}):
        try:
            cursor = None
            dbname, tablename = self.parser_drop(param_dict)
            if dbname and tablename:
                self.change_db_table(dbname, tablename)
                cursor = self.db_table_conn.drop()
#                print cursor
#                if cursor.get('err') == None:
#                    return 1 #update success
#                else:
#                    return 0 #update failed
                return cursor
            else:
                raise ValueError("drop argument 'dbname or tablename' cannot be null")
        except:
            traceback.print_exc()

    def db_find(self, param_dict={}):
        cursor = None
        dbname, tablename, conditions, contents, sort_dict, limit_nums, skip_nums = self.parser_find(param_dict)
        if dbname and tablename:
            self.change_db_table(dbname, tablename)
        if contents:
            cursor = self.db_table_conn.find(conditions, contents).sort(sort_dict.keys()[0], sort_dict.values()[0]).limit(limit_nums).skip(skip_nums)
        else:
            cursor = self.db_table_conn.find(conditions).sort(sort_dict.keys()[0], sort_dict.values()[0]).limit(limit_nums).skip(skip_nums)
        return self.convert_to_list(cursor)

    def db_find_one(self, param_dict={}):
        dbname, tablename, conditions, contents = self.parser_find_one(param_dict)
        if dbname and tablename:
            self.change_db_table(dbname, tablename)
        if contents:
            return self.db_table_conn.find_one(conditions, contents)
        else:
            return self.db_table_conn.find_one(conditions)



class Collection(object):

    def __init__(self, db, collection):
        self.collection = getattr(db, collection)

    def __getattr__(self, operation):
        # 我这个封装只是为了拦截一部分操作,不符合的就直接raise属性错误
        control_type = ['disconnect', 'insert', 'update', 'find', 'find_one']
        if operation in control_type:
            return getattr(self.collection, operation)
        raise AttributeError(operation)


def close_db(dbs=['db']):
    '''
    关闭mongodb数据库连接
    db : 在执行函数里面使用的db的名字(大部分是db，也会有s_db)
        Usage::
            >>>s_db = Mongo()
            >>>@close_db(['s_db'])
            ...: def test():
            ...:     print s_db.test.insert({'a': 1, 'b': 2})
            ...:
    '''
    def _deco(func):
        @wraps(func)
        def _call(*args, **kwargs):
            result = func(*args, **kwargs)
            for db in dbs:
                try:
                    func.func_globals[db].connection.disconnect()
                except KeyError:
                    pass
            return result
        return _call
    return _deco




def test():
    a = MongodbHandle()
    a.get_new_conn(host='192.168.10.46', port=27017, user='root', passwd='aodun')
#    a.init_conn()
#    a.change_dbname('idcadm_main')
#    a.change_tablename('domain_filter')
#    temp_result =  a.db_find({"dbname":"isms_daily_20150526", "tablename":"active_log_192.168.10.46", "content":{"src_ip":1, "url":1, "_id":0}, "skip":3001, "limit":100})
#    print temp_result
#    a.get_new_conn(host='192.168.10.46', port=27017, user='root', passwd='aodun')
#    print a.db_find({"dbname":"isms_daily_20150527", "tablename":"active_log_192.168.10.46", "content":{"src_ip":1, "url":1, "_id":0}, "sort":{"access_time":1}})
##    a.change_db_table('idcadm_main', 'domain_filter')
#    print a.db_find_one({"dbname":"isms_daily_20150527", "tablename":"active_log_192.168.10.46", "param":{"src_ip":"192.168.10.182"}})
#    a.show_conn_info()
#    a.show_info()
#    print a.db_update({"dbname":"idcadm_main", "tablename":"domain_filter", "param":{"_id":{"$in":[ObjectId("5565664be138233e4b11d89f"), ObjectId("5566db16e138233e4b11ed31")]}}, "contents":{"$set":{"status":456}}, "multi":1})
#    a.close_conn()
    print a.db_remove({"dbname":"idcadm_main", "tablename":"domain_filter","param":{"domain" : "www.test6.com.cn"}})

#    print a.db_insert({"dbname":"idcadm_main", "tablename":"domain_filter","contents":{"status" : 1,
#  "domain" : "www.test6.com.cn",
#  "c_date" : "2015-05-28 14:38:03",
#  "c_name" : "admintest",
#  "c_ip" : "192.168.10.185"}})

if __name__ == '__main__':
    test()


    