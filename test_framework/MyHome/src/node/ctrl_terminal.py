# -*- coding: utf-8 -*-
# ===================================
# ScriptName : ctrl_terminal.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2016-12-02 15:16
# ===================================
import json
import paramiko
import tornado.web
from .node_ssh import NodeSSH
from .base import BaseHandler

class ToCtrlTerminalHTML(BaseHandler):
    def get(self, *args, **kwargs):
        self.render("node/node_terminal.html")

class CtrlTerminalHandler(BaseHandler):
    def get_task_script_name(self, _id):
        find_sql = "select download_script_file from time_task where _id=?"
        return self.db.find_one(find_sql, _id)[0][0]

    def get(self, *args, **kwargs):
        node_id = self.get_argument("_id", None)
        if node_id:
            task_lists = []
            query_node_sql = "select node_ip, node_name from node_manage where _id=?"
            node_info = self.db.find_one(query_node_sql, node_id)[0]
            node_dict = dict(zip(["node_ip", "node_name"], node_info))
            query_node_task_sql = "select task_id from node_time_task where node_id='%s'"%node_id
            node_task_info = self.db.find(query_node_task_sql)
            for task_id in node_task_info:
                query_task_sql = "select _id, task_name from time_task where _id = ?"
                task_info = self.db.find_one(query_task_sql, task_id[0])[0]
                print "task_info: ",task_info
                task_lists.append(dict(zip(["_id", "task_name"], task_info)))
            print task_lists
            self.write(json.dumps({"node":node_dict, "task_lists":task_lists}))

    def post(self, *args, **kwargs):
        node_id = self.get_argument("node_id", None)
        task_id = self.get_argument("task_id", None)
        ret_msg = ""
        if node_id and task_id:
            script_name = self.get_task_script_name(task_id)
            print script_name
            self.node_task = self.application.node_task
            ret_msg = self.node_task.execute_script(script_name, node_id)

        else:
            ret_msg = "Invalid node id or task id"
        print "msg: ", ret_msg
        self.write(json.dumps({"msg":ret_msg}))

class LoadHTMLStringModule(tornado.web.UIModule):
    def render(self, html_string):
        # html = tornado.template.Template(html_string)
        return html_string


class TerminalModule(tornado.web.UIModule):
    def render(self, author=''):
        return self.render_string("node/node_terminal.html", author=author)

    def css_files(self):
        return ["/static/css/jquery_terminal/jquery.terminal.min.css",
                "/static/module/css/node-terminal.css"]

    def javascript_files(self):
        return ["/static/js/jquery_terminal/jquery.terminal.min.js",
                "/static/js/jquery_terminal/jquery.mousewheel-min.js",
                "/static/module/js/node-terminal.js"]


class TerminalInteractHandler(BaseHandler):
    def get_node_info(self, _id):
        find_sql = "select node_ip, auth_user, auth_passwd, node_port from node_manage where _id=?"
        return self.db.find_one(find_sql, _id)[0]

    def get(self, *args, **kwargs):
        status = False
        message = "cmd execute failed"
        print "self.request.uri: ",self.request.uri
        print "self.request.body: ",self.request.body
        command = self.get_argument("command", None)
        _id = self.get_argument("_id", None)
        print "cmd: ", command
        if command == "init" and _id:
            self.clear_node_conn(_id)
            node_info = self.get_node_info(_id)
            node_ssh = NodeSSH(*node_info)
            error = node_ssh.init_ssh()
            if error:
                status = False
                message = error
                node_ssh.close_conn()
            else:
                self.node_ssh_conn_pools[_id] = node_ssh
                status = True
                message = "connect success"
        else:
            print self.node_ssh_conn_pools
            if self.node_ssh_conn_pools.has_key(_id):
                node_ssh_conn = self.node_ssh_conn_pools[_id]
                message = node_ssh_conn.input_cmd([command])
                status = True

        self.write(json.dumps({"status":status, "message": message}))


    def post(self, *args, **kwargs):
        print self.request.body
        # print self.request.headers
        # print self.request.uri
        # print self.request


        arguments = json.loads(self.request.body)
        cmd = arguments.get("method", None)
        print cmd
        self.write("you say what?")

    def clear_node_conn(self, _id):
        if self.node_ssh_conn_pools.has_key(_id):
            node_ssh_conn = self.node_ssh_conn_pools[_id]
            print "node_ssh_conn: ",node_ssh_conn
            node_ssh_conn.close_conn()
            del self.node_ssh_conn_pools[_id]

    def delete(self, *args, **kwargs):
        print self.request.body
        print self.request.uri
        _id = self.get_argument("_id", None)
        self.clear_node_conn(_id)

