# -*- coding: utf-8 -*-
# ===================================
# ScriptName : task.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2016-12-01 14:51
# ===================================
import os
import pprint
import json
import time
import uuid
from .base import BaseHandler, time2float

class ToNodeTaskHTML(BaseHandler):
    def get(self, *args, **kwargs):
        task_sql = "select _id, task_name from time_task "
        task_data_field = ['_id', 'task_name']
        task_list = [dict(zip(task_data_field, one)) for one in self.db.find(task_sql)]

        node_sql = "select _id, node_name from node_manage "
        node_data_field = ['_id', 'node_name']
        node_list = [dict(zip(node_data_field, one)) for one in self.db.find(node_sql)]
        self.render("node/node_task.html", task_list=task_list, node_list=node_list)

class NodeBingTaskHandler(BaseHandler):
    def get(self, *args, **kwargs):
        total_sql = """SELECT COUNT(*) FROM node_time_task WHERE 1=1 """
        query_sql = "select _id, node_id, task_id, is_period_execute, first_execute_time, time_task_period_num, " \
                   "time_task_period_unit from node_time_task WHERE 1=1 "
        # 查询域
        start_time = self.get_argument('start_time', None)
        sql = " and first_execute_time >={0} ".format(time2float(start_time)) if start_time else ""
        query_sql += sql
        total_sql += sql
        end_time = self.get_argument('end_time', None)
        sql = " and first_execute_time <={0} ".format(time2float(end_time)) if end_time else ""
        query_sql += sql
        total_sql += sql
        # id是模糊查询
        search_id = self.get_argument('search_id', None)
        sql = " and (_id like '%{0}%' or task_id like '%{0}%' or node_id like '%{0}%') ".format(search_id) if search_id else ""
        query_sql += sql
        total_sql += sql

        is_period_execute = self.get_argument('is_period_execute', None)
        sql = " and is_period_execute={0}".format(int(is_period_execute)) if is_period_execute and is_period_execute != '2' else ""
        query_sql += sql
        total_sql += sql

        order_type = self.get_argument("order", "asc")
        sort_name = self.get_argument('sort', "_id")
        query_sql += " ORDER BY %s %s "%(sort_name, order_type)

        offset = self.get_argument('offset', None)
        limit = self.get_argument('limit', None)
        query_sql += " LIMIT {limit} OFFSET {offset}".format(limit=limit, offset=offset) if offset is not None and limit is not None else ""


        last_data = []
        data_field = ['_id', 'node_id', 'task_id', 'is_period_execute','first_execute_time', 'time_task_period_num', 'time_task_period_unit']

        print query_sql
        for one in self.db.find(query_sql):
            last_data.append(dict(zip(data_field, one)))
        total = self.db.find(total_sql)
        return_data = {
            "rows": last_data,
            "total": total[0][0] if total and len(total) else 0
        }

        self.write(json.dumps(return_data))


    def post(self, *args, **kwargs):
        if self.get_query_argument("_id", None):
            self.put()
        else:
            node_ids = self.get_body_arguments("node_ids", None)
            if not isinstance(node_ids, list):
                node_ids = [node_ids]
            time_task_ids = self.get_body_arguments("time_task_ids", None)
            if not isinstance(time_task_ids, list):
                time_task_ids = [time_task_ids]
            first_execute_time = self.get_argument('first_execute_time', None)
            # 如果不填时间，默认5分钟之后执行
            first_execute_time = time.time() + 300 if first_execute_time or len(first_execute_time)<=0 or time2float(first_execute_time) < time.time() else time2float(first_execute_time)
            is_period_execute = self.get_argument('is_period_execute', None)
            is_period_execute = 1 if is_period_execute=='on' else 0

            time_task_period_num = self.get_argument('time_task_period_num', None) if is_period_execute else None
            time_task_period_unit = self.get_argument('time_task_period_unit', None) if is_period_execute else None


            data = []
            # '_id', 'node_id', 'task_id', 'is_period_execute', 'first_execute_time', 'time_task_period_num', 'time_task_period_unit', 'create_time'
            for node_id in node_ids:
                for task_id in time_task_ids:
                    data.append((str(uuid.uuid4()), node_id, task_id, int(is_period_execute), first_execute_time, time_task_period_num, time_task_period_unit, time.time()))

            save_sql = '''insert into node_time_task values (?, ?, ?, ?, ?, ?, ?, ?)'''
            self.db.save(save_sql, data)

            self.update_node_task()
        self.application.node_task.add_task()
        self.redirect("/node/timetask")

    def update_node_task(self):
        node_ids = self.get_body_arguments("node_ids", None)
        time_task_ids = self.get_body_arguments("time_task_ids", None)
        for node_id in node_ids:
            update_node_sql = "update node_manage set has_binding_task=1 WHERE _id = ?"
            self.db.update(update_node_sql, [(node_id,)])
        for task_id in time_task_ids:
            update_task_sql = "update time_task set has_binding_node=1 WHERE _id = ?"
            self.db.update(update_task_sql, [(task_id,)])

    def put(self, *args, **kwargs):
        _id = self.get_query_argument("_id")
        first_execute_time = self.get_argument('first_execute_time', None)
        first_execute_time = time2float(first_execute_time) if first_execute_time and len(first_execute_time)<=0 and time2float(first_execute_time) > time.time() else  time.time() + 300
        is_period_execute = self.get_argument('is_period_execute', None)
        is_period_execute = 1 if is_period_execute=='on' else 0
        time_task_period_num = self.get_argument('time_task_period_num', None)

        time_task_period_num = int(time_task_period_num) if is_period_execute and time_task_period_num and len(time_task_period_num)>0  else None
        time_task_period_unit = self.get_argument('time_task_period_unit', None)
        time_task_period_unit = time_task_period_unit if is_period_execute and time_task_period_unit and len(time_task_period_unit)>0  else None

        update_sql = '''update node_time_task set first_execute_time = ?, is_period_execute = ?, time_task_period_num = ?, time_task_period_unit = ?  where _id = ? '''
        data = [
            (first_execute_time, is_period_execute, time_task_period_num, time_task_period_unit, _id)
        ]
        self.db.update(update_sql, data)

    # 删除
    def delete(self, *args, **kwargs):
        ids = self.get_argument("_id", None)
        if ids:
            for _id in ids.split(','):
                query_sql = "select node_id, task_id from node_time_task WHERE _id=?"
                result = self.db.find_one(query_sql, _id)[0]
                print "node_id, task_id: ",result
                self.application.node_task.del_task(*result)
            self.db.delete('''delete from node_time_task where _id=?''', [(x,) for x in ids.split(',')])


class ToManageTaskHTML(BaseHandler):
    def get(self, *args, **kwargs):
        self.render("node/task_manage.html")

class ManageTaskHandler(BaseHandler):
    # 查询任务列表
    def get(self, *args, **kwargs):
        total_sql = "SELECT COUNT(*) FROM time_task WHERE 1=1 "
        query_sql = "select _id, task_name, task_function_description, interpreter, download_script_file, has_binding_node, create_time from time_task WHERE 1=1 "
        # 查询域
        start_time = self.get_argument('start_time', None)
        sql = " and create_time >={0} ".format(time2float(start_time)) if start_time else ""
        query_sql += sql
        total_sql += sql
        end_time = self.get_argument('end_time', None)
        sql = " and create_time <={0} ".format(time2float(end_time)) if end_time else ""
        query_sql += sql
        total_sql += sql
        task_name = self.get_argument('task_name', None)
        sql = " and task_name like '%{0}%'".format(task_name) if task_name else ""
        query_sql += sql
        total_sql += sql

        interpreter = self.get_argument('interpreter', None)
        sql = " and interpreter like '%{0}%'".format(interpreter) if interpreter else ""
        query_sql += sql
        total_sql += sql

        order_type = self.get_argument("order", "asc")
        sort_name = self.get_argument('sort', "_id")
        query_sql += " ORDER BY %s %s "%(sort_name, order_type)

        offset = self.get_argument('offset', None)
        limit = self.get_argument('limit', None)
        query_sql += " LIMIT {limit} OFFSET {offset}".format(limit=limit, offset=offset) if offset is not None and limit is not None else ""


        last_data = []
        data_field = ['_id', 'task_name', 'task_function_description', 'interpreter', 'download_script_file', 'has_binding_node', 'create_time']

        print "task_sql : ", query_sql

        for one in self.db.find(query_sql):
            last_data.append(dict(zip(data_field, one)))
        total = self.db.find(total_sql)

        # pprint.pprint(last_data)
        return_data = {
            "rows": last_data,
            "total": total[0][0] if total and len(total) else 0
        }

        self.write(json.dumps(return_data))

    def show_request(self):
        print "self.request: ",self.request
        print "self.request.headers: ",self.request.headers
        print "self.request.uri: ",self.request.uri
        print "self.request.body: ",self.request.body
        print "self.request.files: ",self.request.files
        print


    def post(self, *args, **kwargs):
        file_type = {
            "python":'.py',
            "bash": '.sh'
        }
        file_save_path = os.environ["DOWNLOAD_SCRIPT_PATH"]
        file_metas=self.request.files.get("upload_file_name")
        task_name = self.get_argument("task_name", None)
        task_function_description = self.get_argument("task_function_description", None)
        interpreter = self.get_argument("interpreter", None)
        is_upload_file = self.get_argument("is_upload_file", None)
        manual_input_cmd = self.get_argument("manual_input_cmd", None)
        upload_file_name = None
        if is_upload_file == "on":
            for meta in file_metas:
                upload_file_name=meta['filename']
                filepath=os.path.join(file_save_path,upload_file_name)
                #有些文件需要已二进制的形式存储，实际中可以更改
                with open(filepath,'wb') as up:
                    up.write(meta['body'])
        else:
            if manual_input_cmd and len(manual_input_cmd) > 0:
                current_time = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
                if file_type.has_key(interpreter.lower()):
                    upload_file_name = "%s%s"%(current_time, file_type[interpreter.lower()])
                else:
                    upload_file_name = "%s.txt"%current_time
                filepath=os.path.join(file_save_path,upload_file_name)
                with open(filepath,'wb') as up:
                    up.write(manual_input_cmd)

        # '_id', 'task_name', 'task_function_description', 'interpreter', 'download_script_file', 'has_binding_node', 'create_time'
        data = [(str(uuid.uuid4()), task_name, task_function_description, interpreter.lower(), upload_file_name, None, time.time())]

        save_sql = '''insert into time_task values (?, ?, ?, ?, ?, ?, ?)'''
        self.db.save(save_sql, data)


        self.redirect("/manage/timetask")



    # 删除
    def delete(self, *args, **kwargs):
        # 这里还需要补充删除上传的文件
        ids = self.get_argument("_id", None)
        if ids:
            download_path = os.environ["DOWNLOAD_SCRIPT_PATH"]
            query_sql = "select download_script_file from time_task WHERE _id=?"
            for x in ids.split(','):
                filename = self.db.find_one(query_sql, x)
                print "filename: ", filename
                if len(filename):
                    file_save_path = os.path.join(download_path, filename[0][0])
                    print file_save_path
                    if os.path.exists(file_save_path):
                        print "delete file: ",file_save_path
                        os.remove(file_save_path)
            task_ids = [(x,) for x in ids.split(',')]
            self.db.delete('''delete from time_task where _id=?''', task_ids)
            self.db.delete('''delete from node_time_task where task_id=?''', task_ids)
            self.application.node_task.restart()