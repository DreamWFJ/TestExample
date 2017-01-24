# -*- coding: utf-8 -*-
# ===================================
# ScriptName : db_sqlite3.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2016-11-29 17:33
# ===================================
import os
import sqlite3

class Sqlite3DB(object):
    def __init__(self, path=None):
        self.path = path if path and len(path.strip())>1 else ':memory:'
        self.conn = self.get_conn()

    def __del__(self):
        self.conn.close()

    def nice_path(self):
        if not self.path.__eq__(':memory:'):
            if not self.path.endswith('.sqlite'):
                self.path = "%s%s"%(self.path, '.sqlite')
            if not os.path.dirname(self.path) or not (os.path.exists(self.path) and os.path.isfile(self.path)):
                self.path = os.path.join(os.path.dirname(os.path.realpath(__file__)), self.path)
                open(self.path,"w+").close()

    def get_conn(self):
        '''获取到数据库的连接对象，参数为数据库文件的绝对路径
        如果传递的参数是存在，并且是文件，那么就返回硬盘上面改
        路径下的数据库文件的连接对象；否则，返回内存中的数据接
        连接对象'''
        self.nice_path()
        if self.path.__eq__(':memory:'):
            return sqlite3.connect(':memory:')
        else:
            return sqlite3.connect(self.path)

    def get_cursor(self):
        '''该方法是获取数据库的游标对象，参数为数据库的连接对象
        如果数据库的连接对象不为None，则返回数据库连接对象所创
        建的游标对象；否则返回一个游标对象，该对象是内存中数据
        库连接对象所创建的游标对象'''
        if self.conn is not None:
            return self.conn.cursor()
        else:
            if self.path is not None:
                self.conn = self.get_conn()
                return self.conn.cursor()
            else:
                return self.get_conn().cursor()

    def drop_table(self, table):
        '''如果表存在,则删除表，如果表中存在数据的时候，使用该
        方法的时候要慎用！'''
        if table is not None and table != '':
            sql = 'DROP TABLE IF EXISTS ' + table

            cu = self.get_cursor()
            cu.execute(sql)
            self.conn.commit()
            cu.close()
        else:
            print('the [{}] is empty or equal None!'.format(table))

    def create_table(self, sql):
        '''创建数据库表：student'''
        if sql is not None and sql != '':
            cu = self.get_cursor()
            cu.execute(sql)
            self.conn.commit()
            cu.close()
        else:
            print('the [{}] is empty or equal None!'.format(sql))

    # 数据库 CRUD
    def save(self, sql, data):
        '''插入数据'''
        if sql is not None and sql != '':
            if data is not None:
                cu = self.get_cursor()
                for d in data:
                    cu.execute(sql, d)
                    self.conn.commit()
                cu.close()
        else:
            print('the [{}] is empty or equal None!'.format(sql))

    def find(self, sql):
        '''查询所有数据'''
        if sql is not None and sql != '':
            cu = self.get_cursor()
            cu.execute(sql)
            r = cu.fetchall()
            return list(r)
            # if len(r) > 0:
            #     for e in range(len(r)):
            #         print(r[e])
        else:
            print('the [{}] is empty or equal None!'.format(sql))
            return []

    def find_one(self, sql, data):
        '''查询一条数据'''
        if sql is not None and sql != '':
            if data is not None:
                #Do this instead
                d = (data,)
                cu = self.get_cursor()
                cu.execute(sql, d)
                r = cu.fetchall()
                return r
            else:
                print('the [{}] equal None!'.format(data))
                return None
        else:
            print('the [{}] is empty or equal None!'.format(sql))
            return None

    def update(self, sql, data):
        '''更新数据'''
        if sql is not None and sql != '':
            if data is not None:
                cu = self.get_cursor()
                for d in data:
                    cu.execute(sql, d)
                    self.conn.commit()
                cu.close()
        else:
            print('the [{}] is empty or equal None!'.format(sql))

    def raw_sql_execute(self, sql):
        if sql is not None and sql != '':
            cu = self.get_cursor()
            print "raw sql : ", sql
            cu.execute(sql)
            self.conn.commit()
            cu.close()
        else:
            print('the [{}] is empty or equal None!'.format(sql))

    def delete(self, sql, data):
        '''删除数据'''
        if sql is not None and sql != '':
            if data is not None:
                cu = self.get_cursor()
                for d in data:
                    cu.execute(sql, d)
                    self.conn.commit()
                cu.close()
        else:
            print('the [{}] is empty or equal None!'.format(sql))


def test_1():
    h = Sqlite3DB('abc')
    h.drop_table('test')
    sql = '''create table `test` (
        `_id` int(36) not null,
        `name` varchar(128) not null,
        `ip` varchar(36) default null,
        `auth_user` varchar(32) default null,
        `auth_passwd` varchar(64) default null,
        `node_status` int(1) default null,
        `last_detect_time` float(24) default null,
        `descriptor` varchar(128) default null,
        `last_detect_log` varchar(32) default null,
        primary key (`_id`)
    )'''
    h.create_table(sql)

    save_sql = '''insert into test values (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    data = [
        ('1', 'Hongten', '10.100.13.164', 'root', 'root', 1, 1480318164.2178299, 'test', 'tset.log'),
        ('2', 'Beijin', '20.100.13.164', 'root', 'root', 1, 1480318164.2178299, 'test', 'tset.log'),
        ('3', 'Shanghai', '30.100.13.164', 'root', 'root', 1, 1480318164.2178299, 'test', 'tset.log'),
    ]
    h.save(save_sql, data)

    print h.find('''select name, ip from test''')

    print h.find_one('''select * from test where _id= ?''', '1')

    h.update('''update test set name=? where _id=?''', [('test1', '1'),('test2', '2')])
    print h.find_one('''select * from test where _id= ?''', '1')
    h.delete('''delete from test where name=? and _id=?''', [('test1', '1'),('test2', '2')])
    print h.find('''select * from test''')

if __name__ == '__main__':
    test_1()
    