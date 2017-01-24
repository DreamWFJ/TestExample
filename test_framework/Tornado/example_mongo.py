# -*- coding: utf-8 -*-
# ===================================
# ScriptName : example_mongo.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2016-09-14 17:31
# ===================================

import pymongo
from bson.objectid import ObjectId

# 连接对象可以访问你连接的服务器的任何数据库
conn = pymongo.MongoClient('localhost', 27017)
# conn = pymongo.MongoClient(
#     "mongodb://user:password@staff.mongohq.com:10066/your_mongohq_db"
# )
# 通过对象属性或者像字典一样使用对象来获得代表一个特定数据库的对象，数据库若不存在，则自动创建
db = conn.example
# or db = conn['example']

# 获取集合列表
print db.collection_names()
# 访问集合，同样适用对象属性或字典方式
collection_name = db.collection_name # or db['collection_name']

# 写入数据
# object_id =  collection_name.insert({"name": "flibnip", "description": "grade-A industrial flibnip", "quantity": 3})
# print "---------- ",object_id, type(object_id), isinstance(object_id, ObjectId)
# 输出 ----------  57d923e1a96b864a2874c3f0 <class 'bson.objectid.ObjectId'> True
# ObjectId('4eada3a4136fc4aa41000001')

# 读取数据，返回的结果为字典格式

description = collection_name.find_one({'name':"flibnip"})['description']
print description
print list(collection_name.find({'name':"flibnip"}))

# 移除数据
# print collection_name.remove({"name":"flibnip"})

import json
# 这里序列化是会报错，因为ObjectId，简单的处理办法是删除_id
# json.dumps(collection_name.find_one({'name':"flibnip"}))
# 或者使用bson去处理
'''
>>> from bson import Binary, Code
>>> from bson.json_util import dumps
>>> dumps([{'foo': [1, 2]},
...        {'bar': {'hello': 'world'}},
...        {'code': Code("function x() { return 1; }")},
...        {'bin': Binary("")}])
'[{"foo": [1, 2]}, {"bar": {"hello": "world"}}, {"code": {"$code": "function x() { return 1; }", "$scope": {}}}, {"bin": {"$binary": "AQIDBA==", "$type": "00"}}]'

>>> from bson.json_util import loads
>>> loads('[{"foo": [1, 2]}, {"bar": {"hello": "world"}}, {"code": {"$scope": {}, "$code": "function x() { return 1; }"}}, {"bin": {"$type": "00", "$binary": "AQIDBA=="}}]')
[{u'foo': [1, 2]}, {u'bar': {u'hello': u'world'}}, {u'code': Code('function x() { return 1; }', {})}, {u'bin': Binary('...', 0)}]

------------ 认证 -------------
>>> import urllib
>>> password = urllib.quote_plus('pass/word')
>>> password
'pass%2Fword'
>>> MongoClient('mongodb://user:' + password + '@127.0.0.1')
MongoClient('127.0.0.1', 27017)

>>> from pymongo import MongoClient
>>> client = MongoClient('example.com')
>>> client.the_database.authenticate('user', 'password', mechanism='SCRAM-SHA-1')
True
>>>
>>> uri = "mongodb://user:password@example.com/the_database?authMechanism=SCRAM-SHA-1"
>>> client = MongoClient(uri)

>>> from pymongo import MongoClient
>>> client = MongoClient('example.com')
>>> client.the_database.authenticate('user', 'password', mechanism='MONGODB-CR')
True
>>>
>>> uri = "mongodb://user:password@example.com/the_database?authMechanism=MONGODB-CR"
>>> client = MongoClient(uri)

>>> from pymongo import MongoClient
>>> client = MongoClient('example.com')
>>> db = client.the_database
>>> db.authenticate('user', 'password', source='source_database')
True

>>> uri = "mongodb://user:password@example.com/?authSource=source_database"
>>> db = MongoClient(uri).the_database

------------ ssl 认证 --------------
>>> import ssl
>>> from pymongo import MongoClient
>>> client = MongoClient('example.com',
...                       ssl=True,
...                       ssl_certfile='/path/to/client.pem',
...                       ssl_cert_reqs=ssl.CERT_REQUIRED,
...                       ssl_ca_certs='/path/to/ca.pem')
>>> client.the_database.authenticate("<X.509 derived username>",
...                                  mechanism='MONGODB-X509')
True
>>>


---------------- 操作 ---------------
from pymongo import MongoClient
from pymongo.collation import Collation, CollationStrength

contacts = MongoClient().test.contacts
result = contacts.update_many(
    {'first_name': 'jürgen'},
    {'$set': {'verified': 1}},
    collation=Collation(locale='de',
                        strength=CollationStrength.SECONDARY))


 复制数据库
 >>> client.admin.authenticate('administrator', 'pwd')
True
>>> client.admin.command('copydb',
                         fromdb='source_db_name',
                         todb='target_db_name',
                         fromhost='source.example.com')


块写操作
>>> import pymongo
>>> db = pymongo.MongoClient().bulk_example
>>> db.test.insert_many([{'i': i} for i in xrange(10000)]).inserted_ids
[...]
>>> db.test.count()
10000

>>> from pprint import pprint
>>>
>>> bulk = db.test.initialize_ordered_bulk_op()
>>> # Remove all documents from the previous example.
...
>>> bulk.find({}).remove()
>>> bulk.insert({'_id': 1})
>>> bulk.insert({'_id': 2})
>>> bulk.insert({'_id': 3})
>>> bulk.find({'_id': 1}).update({'$set': {'foo': 'bar'}})
>>> bulk.find({'_id': 4}).upsert().update({'$inc': {'j': 1}})
>>> bulk.find({'j': 1}).replace_one({'j': 2})
>>> result = bulk.execute()
>>> pprint(result)
{'nInserted': 3,
 'nMatched': 2,
 'nModified': 2,
 'nRemoved': 10000,
 'nUpserted': 1,
 'upserted': [{u'_id': 4, u'index': 5}],
 'writeConcernErrors': [],
 'writeErrors': []}



>>> from pymongo.errors import BulkWriteError
>>> bulk = db.test.initialize_ordered_bulk_op()
>>> bulk.find({'j': 2}).replace_one({'i': 5})
>>> # Violates the unique key constraint on _id.
...
>>> bulk.insert({'_id': 4})
>>> bulk.find({'i': 5}).remove_one()
>>> try:
...     bulk.execute()
... except BulkWriteError as bwe:
...     pprint(bwe.details)
...
{'nInserted': 0,
 'nMatched': 1,
 'nModified': 1,
 'nRemoved': 0,
 'nUpserted': 0,
 'upserted': [],
 'writeConcernErrors': [],
 'writeErrors': [{u'code': 11000,
                  u'errmsg': u'...E11000 duplicate key error...',
                  u'index': 1,
                  u'op': {'_id': 4}}]}

>>> bulk = db.test.initialize_unordered_bulk_op()
>>> bulk.insert({'_id': 1})
>>> bulk.find({'_id': 2}).remove_one()
>>> bulk.insert({'_id': 3})
>>> bulk.find({'_id': 4}).replace_one({'i': 1})
>>> try:
...     bulk.execute()
... except BulkWriteError as bwe:
...     pprint(bwe.details)
...
{'nInserted': 0,
 'nMatched': 1,
 'nModified': 1,
 'nRemoved': 1,
 'nUpserted': 0,
 'upserted': [],
 'writeConcernErrors': [],
 'writeErrors': [{u'code': 11000,
                  u'errmsg': u'...E11000 duplicate key error...',
                  u'index': 0,
                  u'op': {'_id': 1}},
                 {u'code': 11000,
                  u'errmsg': u'...E11000 duplicate key error...',
                  u'index': 2,
                  u'op': {'_id': 3}}]}
>>> bulk = db.test.initialize_ordered_bulk_op()
>>> bulk.insert({'a': 0})
>>> bulk.insert({'a': 1})
>>> bulk.insert({'a': 2})
>>> bulk.insert({'a': 3})
>>> try:
...     bulk.execute({'w': 3, 'wtimeout': 1})
... except BulkWriteError as bwe:
...     pprint(bwe.details)
...
{'nInserted': 4,
 'nMatched': 0,
 'nModified': 0,
 'nRemoved': 0,
 'nUpserted': 0,
 'upserted': [],
 'writeConcernErrors': [{u'code': 64,
                         u'errInfo': {u'wtimeout': True},
                         u'errmsg': u'waiting for replication timed out'}],
 'writeErrors': []}

----------- 操作 -------------
    replace_one(self, filter, replacement, upsert=False, bypass_document_validation=False)
    update_one(self, filter, update, upsert=False, bypass_document_validation=False)
    update_many(self, filter, update, upsert=False, bypass_document_validation=False)
    drop(self):
            Alias for :meth:`~pymongo.database.Database.drop_collection`.
            The following two calls are equivalent:
              >>> db.foo.drop()
              >>> db.drop_collection("foo")
    delete_one(self, filter)
    delete_many(self, filter)
    find_one(self, filter=None, *args, **kwargs)
    find(self, *args, **kwargs)
    count(self, filter=None, **kwargs)
    create_indexes(self, indexes)
    create_index(self, keys, **kwargs)
    drop_indexes(self):
        Drops all indexes on this collection.
    drop_index(self, index_or_name)
    reindex(self):
        Rebuilds all indexes on this collection.
    list_indexes(self)
    index_information(self)
    options(self)
    aggregate(self, pipeline, **kwargs)
    group(self, key, condition, initial, reduce, finalize=None, **kwargs)
    rename(self, new_name, **kwargs)
        Rename this collection
    distinct(self, key, filter=None, **kwargs)
        Get a list of distinct values for `key` among all documents in this collection.
    map_reduce(self, map, reduce, out, full_response=False, **kwargs):
        Perform a map/reduce operation on this collection.
    inline_map_reduce(self, map, reduce, full_response=False, **kwargs):
        Perform an inline map/reduce operation on this collection.
    find_one_and_delete(self, filter, projection=None, sort=None, **kwargs)
    find_one_and_replace(self, filter, replacement,
                                 projection=None, sort=None, upsert=False,
                                 return_document=ReturnDocument.BEFORE, **kwargs)
    find_one_and_update(self, filter, update,
                                projection=None, sort=None, upsert=False,
                                return_document=ReturnDocument.BEFORE, **kwargs)
    save(self, to_save, manipulate=True, check_keys=True, **kwargs)
    insert(self, doc_or_docs, manipulate=True,
                   check_keys=True, continue_on_error=False, **kwargs)
    update(self, spec, document, upsert=False, manipulate=False,
                   multi=False, check_keys=True, **kwargs)
    remove(self, spec_or_id=None, multi=True, **kwargs):
        Remove a document(s) from this collection.
    find_and_modify(self, query={}, update=None,
                            upsert=False, sort=None, full_response=False,
                            manipulate=False, **kwargs)


'''

def test_3():
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['test-database']
    post = {}
    posts = db.posts
    # 插入一条数据
    post_id = posts.insert_one(post).inserted_id
    # 查看当前不包括系统集合的集合名称
    db.collection_names(include_system_collections=False)
    # 查找一条数据
    posts.find_one()
    def get(post_id):
        # Convert from string to ObjectId:
        document = client.db.collection.find_one({'_id': ObjectId(post_id)})

    # 插入多条数据
    new_posts = [{}]
    result = posts.insert_many(new_posts)
    # 查询多条数据
    posts.find()
    # 统计查询数量
    posts.find({"author": "Mike"}).count()
    # 对查询结果进行排序
    posts.find({"author": "Mike"}).sort("author")

    # 创建索引
    result = db.profiles.create_index([('user_id', pymongo.ASCENDING)],unique=True)
    # 查看集合中的索引
    list(db.profiles.index_information())
    # 若插入唯一键重复的数据，将会抛出pymongo.errors.DuplicateKeyError异常

    '''
      聚合
        >>> from pymongo import MongoClient
        >>> db = MongoClient().aggregation_example
        >>> result = db.things.insert_many([{"x": 1, "tags": ["dog", "cat"]},
        ...                                 {"x": 2, "tags": ["cat"]},
        ...                                 {"x": 2, "tags": ["mouse", "cat", "dog"]},
        ...                                 {"x": 3, "tags": []}])
        >>> result.inserted_ids

        >>> from bson.son import SON
        >>> pipeline = [
        ...     {"$unwind": "$tags"},
        ...     {"$group": {"_id": "$tags", "count": {"$sum": 1}}},
        ...     {"$sort": SON([("count", -1), ("_id", -1)])}
        ... ]
        >>> list(db.things.aggregate(pipeline))
        [{u'count': 3, u'_id': u'cat'}, {u'count': 2, u'_id': u'dog'}, {u'count': 1, u'_id': u'mouse'}]

    '''

if __name__ == '__main__':
    pass
    