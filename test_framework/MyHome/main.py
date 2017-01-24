#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:         WFJ
Version:        0.1.0
FileName:       main.py
CreateTime:     2016-11-26 15:27
"""
import os
import signal
import uuid
import time
import tornado.log
import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
from tornado.options import options
from src.router import route_urls
from settings import global_settings
from src.db_sqlite3 import Sqlite3DB
from apscheduler.schedulers.tornado import TornadoScheduler
import logging
logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('debug_myhome.log')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter = tornado.log.LogFormatter()
ch.setFormatter(formatter)
fh.setFormatter(formatter)

logger.addHandler(ch)
logger.addHandler(fh)

class MyTornadoScheduler(TornadoScheduler):
    def __init__(self):
        self.global_task_job = {}
        super(TornadoScheduler, self).__init__()


from src.node.task_schedule import NodeTimeTask
app = tornado.web.Application(route_urls)
class MyHomeApp(tornado.web.Application):
    def __init__(self, scheduler, node_task):
        self.db = Sqlite3DB(os.environ["PROJECT_DATABASE_PATH"])
        self._init_db()
        self.logger = logger
        self.node_ssh_conn_pools = {}
        self.scheduler = scheduler
        self.node_task = node_task
        self._init_insert_data()
        tornado.web.Application.__init__(self, route_urls, **global_settings)

    def _init_db(self):
        handler = self.db
        handler.drop_table('node_manage')
        handler.drop_table('node_time_task')
        handler.drop_table('time_task')
        node_sql = '''create table `node_manage` (
            `_id` varchar(36) not null,
            `node_name` varchar(128) default null,
            `node_ip` varchar(36) default null,
            `node_port` varchar(36) default null,
            `auth_user` varchar(32) default null,
            `auth_passwd` varchar(64) default null,
            `node_status` int(1) default null,
            `last_detect_time` float(24) default null,
            `node_description` varchar(128) default null,
            `last_detect_log` varchar(32) default null,
            `has_binding_task` int(1) default null,
            `create_time` float(24) default null,
            primary key (`_id`)
        )'''


        handler.create_table(node_sql)

        node_time_task_sql = '''create table `node_time_task` (
            `_id` varchar(36) not null,
            `node_id` varchar(36) default null,
            `task_id` varchar(36) default null,
            `is_period_execute` int(1) default null,
            `first_execute_time` float(24) default null,
            `time_task_period_num` int(32) default null,
            `time_task_period_unit` varchar(32) default null,
            `create_time` float(24) default null,
            primary key (`_id`)
        )'''


        handler.create_table(node_time_task_sql)

        timetask_sql = '''create table `time_task` (
            `_id` varchar(36) not null,
            `task_name` varchar(128) default null,
            `task_function_description` varchar(256) default null,
            `interpreter` varchar(36) default null,
            `download_script_file` varchar(128) default null,
            `has_binding_node` int(1) default null,
            `create_time` float(24) default null,
            primary key (`_id`)
        )'''
        handler.create_table(timetask_sql)

    def get_uuid(self):
        return str(uuid.uuid4())

    def _init_insert_data(self):
        handler = self.db
        node1 = self.get_uuid()
        node2 = self.get_uuid()
        node3 = self.get_uuid()

        save_sql = '''insert into 'node_manage' values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        data = [
            (node1, 'test node 1', '192.168.217.138', 22, 'root', 'abc', 1, time.time(), 'this the description: test node 1', 'test.log', 1, time.time()),
            (node2, 'test node 2', '20.100.13.161', 22, 'root', 'root', 1, time.time(), 'this the description: test node 2', 'test1.log', None, time.time()),
            (node3, 'test node 3', '30.100.13.162', 3301, 'root', 'root', 0, None, 'this the description: test node 3', 'test2.log', 0, time.time()),
        ]
        handler.save(save_sql, data)

        save_sql = '''insert into 'time_task' values (?, ?, ?, ?, ?, ?, ?)'''
        task1 = self.get_uuid()
        task2 = self.get_uuid()
        task3 = self.get_uuid()
        task4 = self.get_uuid()
        data = [
            (task1, "task 1", "test host is alived", "bash", "20161202112203.sh", 1, time.time()),
            (task2, "task 2", "detected port is open by ip", "bash", "20161202150206.sh", 1, time.time()),
            (task3, "task 3", "just a test file", "python", "201612020630.py", 1, time.time()),
            (task4, "task 4", "I don't known what is it", "unknow", "201612020631", 0, time.time()),
        ]
        handler.save(save_sql, data)

        save_sql = '''insert into 'node_time_task' values (?, ?, ?, ?, ?, ?, ?, ?)'''
        a = self.get_uuid()
        data = [
            (self.get_uuid(), node1, task1, 1, time.time(), 12, 'Day', time.time()),
            (self.get_uuid(), node3, task1, 1, time.time(), 12, 'Day', time.time()),
            (self.get_uuid(), node2, task1, 1, time.time(), 12, 'Day', time.time()),
            (self.get_uuid(), node2, task2, 0, None, None, None, time.time()),
            (self.get_uuid(), node3, task3, 0, None, None, None, time.time()),
            (self.get_uuid(), node3, task3, 0, None, None, None, time.time()),
        ]
        handler.save(save_sql, data)



if __name__ == '__main__':
    scheduler = MyTornadoScheduler()
    node_task = NodeTimeTask(scheduler, logger)
    tornado.options.parse_command_line()
    server = tornado.httpserver.HTTPServer(MyHomeApp(scheduler, node_task))
    server.listen(options.port)
    node_task.start()
    # logging.info('start listen on port: %s', options.port)
    # signal.signal(signal.SIGTERM, sig_handler)
    # signal.signal(signal.SIGINT, sig_handler)
    try:
        tornado.ioloop.IOLoop.current().start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

