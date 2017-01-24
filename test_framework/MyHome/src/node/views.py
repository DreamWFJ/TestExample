# -*- coding: utf-8 -*-
# ===================================
# ScriptName : views.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2016-11-28 17:47
# ===================================
import uuid
import time
import os
import json
from .base import BaseHandler, time2float



class ToManageNodeHTML(BaseHandler):
    def get(self, *args, **kwargs):
        self.render("node/node_manage.html")

class ManageNodeHandler(BaseHandler):
    # 查询
    def get(self, *args, **kwargs):
        total_sql = """SELECT COUNT(*) FROM node_manage WHERE 1=1 """
        query_sql = """SELECT _id, node_name, node_ip, node_port, auth_user, auth_passwd, node_status,
last_detect_time, node_description, last_detect_log, has_binding_task, create_time FROM node_manage WHERE 1=1 """

        # 查询域
        start_time = self.get_argument('start_time', None)
        sql = " and last_detect_time >={0}".format(time2float(start_time)) if start_time else ""
        query_sql += sql
        total_sql += sql
        end_time = self.get_argument('end_time', None)
        sql = " and last_detect_time <={0}".format(time2float(end_time)) if end_time else ""
        query_sql += sql
        total_sql += sql
        node_ip = self.get_argument('node_ip', None)
        sql = " and  node_ip like '%{0}%'".format(node_ip) if node_ip else ""
        query_sql += sql
        total_sql += sql
        node_status = self.get_argument('node_status', None)
        sql = " and node_status={0}".format(int(node_status)) if node_status and node_status != '2' else ""
        query_sql += sql
        total_sql += sql
        order_type = self.get_argument("order", "asc")
        sort_name = self.get_argument('sort', "_id")
        sql = " ORDER BY %s %s "%(sort_name, order_type)
        query_sql += sql
        total_sql += sql
        offset = self.get_argument('offset', None)
        limit = self.get_argument('limit', None)
        sql = " LIMIT {limit} OFFSET {offset}".format(limit=limit, offset=offset) if offset is not None and limit is not None else ""
        query_sql += sql
        last_data = []
        data_field = ['_id', 'node_name', 'node_ip', 'node_port', 'auth_user', 'auth_passwd', 'node_status', 'last_detect_time',
                      'node_description', 'last_detect_log', 'has_binding_task', 'create_time']
        print query_sql
        for one in self.db.find(query_sql):
            last_data.append(dict(zip(data_field, one)))
        total = self.db.find(total_sql)
        return_data = {
            "rows": last_data,
            "total": total[0][0] if total and len(total) else 0
        }

        self.write(json.dumps(return_data))

    # 新增
    def post(self, *args, **kwargs):
        if self.get_query_argument("_id", None):
            self.put()
        else:
            node_name = self.get_argument('node_name', None)
            node_ip = self.get_argument('node_ip', None)
            node_port = self.get_argument('node_port', None)
            auth_user = self.get_argument('auth_user', None)
            auth_passwd = self.get_argument('auth_passwd', None)
            node_description = self.get_argument('node_description', None)
            # '_id', 'node_name', 'node_ip', 'auth_user', 'auth_passwd', 'node_status', 'last_detect_time', 'node_description', 'last_detect_log', 'create_time'
            save_sql = '''insert into node_manage values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
            data = [
                (str(uuid.uuid4()), node_name, node_ip, int(node_port), auth_user, auth_passwd, 0, None, node_description, None, None, time.time())
            ]
            self.db.save(save_sql, data)
            self.redirect("/manage/node")



    # 修改
    def put(self, *args, **kwargs):
        _id = self.get_query_argument("_id")
        node_name = self.get_argument('node_name', None)
        node_ip = self.get_argument('node_ip', None)
        node_port = self.get_argument('node_port', None)
        auth_user = self.get_argument('auth_user', None)
        auth_passwd = self.get_argument('auth_passwd', None)
        node_description = self.get_argument('node_description', None)


        update_sql = '''update node_manage set node_name = ?, node_ip = ?, node_port = ?, auth_user = ?, auth_passwd = ?, node_description = ? where _id = ?'''
        data = [
            (node_name, node_ip, node_port, auth_user, auth_passwd, node_description, _id)
        ]
        self.db.update(update_sql, data)
        self.redirect("/manage/node")

    # 删除
    def delete(self, *args, **kwargs):
        # 这里还需要删除产生的日志文件
        ids = self.get_argument("_id", None)
        if ids:
            node_ids = [(x,) for x in ids.split(',')]
            delete_log_file(ids.split(','))
            self.db.delete('''delete from node_manage where _id=?''', node_ids)
            self.db.delete('''delete from node_time_task where node_id=?''', node_ids)
            self.application.node_task.restart()

def delete_log_file(ids):
    log_path = os.environ["DOWNLOAD_LOG_PATH"]
    for f in os.listdir(log_path):
        file_path = os.path.join(log_path, f)
        [os.remove(file_path) for _id in ids if f.startswith(_id)]
