# -*- coding: utf-8 -*-
# ===================================
# ScriptName : task_schedule.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2016-12-08 11:16
# ===================================

import os
import time
from .node_ssh import NodeSSH
from src.db_sqlite3 import Sqlite3DB
def time2string(t):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))

class NodeTimeTask(object):
    def __init__(self, schedule, logger):
        self.db = Sqlite3DB(os.environ["PROJECT_DATABASE_PATH"])
        self.logger = logger
        self.schedule = schedule

    def start(self):
        self.add_task()
        self.logger.debug("start scheduler ...")
        if not self.schedule.running:
            self.schedule.start()

    def stop(self):
        self.logger.debug("stop scheduler ...")
        self.schedule.shutdown(wait=False)

    def restart(self):
        self.logger.debug("restart scheduler ...")
        # self.stop()
        self.start()


    def add_task(self):
        self.logger.debug("add task to scheduler ...")
        query_time_task_sql = "select task_id, first_execute_time, time_task_period_num, time_task_period_unit, node_id from " \
                              "node_time_task where is_period_execute = 1"
        query_task_sql = "select download_script_file from time_task where _id=?"
        time_task_lists = self.db.find(query_time_task_sql)
        self.logger.info("need schedule task list: %s"%time_task_lists)
        node_task_history = dict()
        for time_task in time_task_lists:
            task_id = time_task[0]
            first_execute_time = time_task[1]
            first_execute_time = time2string(first_execute_time) if first_execute_time > time.time() else time2string(time.time() + 300)
            print "first_execute_time: ",first_execute_time
            time_task_period_num = time_task[2]
            time_task_period_unit = time_task[3]
            node_id = time_task[4]
            script_file_name = self.db.find_one(query_task_sql, task_id)[0][0]
            if node_task_history.has_key(node_id):
                if script_file_name in node_task_history[node_id]:
                    continue
                else:
                    node_task_history[node_id].append(script_file_name)
            else:
                node_task_history[node_id] = [script_file_name]


            self.logger.debug("node_id: %s, script name: %s, first_execute_time:%s, time_task_period_num: %s, time_task_period_unit :%s"%(node_id,
                                                                script_file_name, first_execute_time, time_task_period_num, time_task_period_unit))
            seconds = 0
            minutes = 0
            hours = 0
            days = 0
            months = 0
            years = 0
            if time_task_period_unit.lower() == "hour":
                hours = int(time_task_period_num)
            elif time_task_period_unit.lower() == "minute":
                minutes = int(time_task_period_num)
            elif time_task_period_unit.lower() == "second":
                seconds = int(time_task_period_num)
            elif time_task_period_unit.lower() == "day":
                days = int(time_task_period_num)

            self.logger.debug("start schedule job, script name: %s, first_excute_time: %s, period: %s%s"%(script_file_name,
                                                    first_execute_time, time_task_period_num, time_task_period_unit) )
            if self.schedule.global_task_job.has_key(node_id):
                if self.schedule.global_task_job[node_id].has_key(script_file_name):
                    job = self.schedule.global_task_job[node_id][script_file_name]
                    job.reschedule('interval', seconds=seconds,
                                      minutes=minutes, hours=hours, days=days)
                else:
                    self.schedule.global_task_job[node_id] = {}
                    job =self.schedule.add_job(self.execute_script, 'interval', name=script_file_name, seconds=seconds, replace_existing=True,
                                      minutes=minutes, hours=hours, days=days, next_run_time=first_execute_time, args=[script_file_name, node_id])
                    self.schedule.global_task_job[node_id][script_file_name] = job
            else:
                self.schedule.global_task_job[node_id] = {}
                job =self.schedule.add_job(self.execute_script, 'interval', name=script_file_name, seconds=seconds, replace_existing=True,
                                      minutes=minutes, hours=hours, days=days, next_run_time=first_execute_time, args=[script_file_name, node_id])
                self.schedule.global_task_job[node_id][script_file_name] = job
                print job
                print script_file_name
                print self.schedule.global_task_job[node_id]
        self.logger.info("current job: %s"%self.schedule.global_task_job)

    def del_task(self, node_id, task_id):
        # 移除废弃的定时任务
        self.logger.debug("start stop scheduler node_id: %s,  task_id: %s "%(node_id, task_id))
        query_task_sql = "select download_script_file from time_task where _id=?"
        script_file_name = self.db.find_one(query_task_sql, task_id)[0][0]
        error_status = False
        if self.schedule.global_task_job.has_key(node_id):
            node_task_history = self.schedule.global_task_job[node_id]
            if node_task_history.has_key(script_file_name):
                job = node_task_history[script_file_name]
                job.remove()
                del self.schedule.global_task_job[node_id][script_file_name]
                self.logger.info("stop scheduler: %s ( task_id: %s, node_id: %s )"%(job, task_id, node_id))
            else:
                error_status = True
        else:
            error_status = True

        if error_status:
            self.logger.error("not found running task( task_id: %s, node_id: %s )"%(task_id, node_id))



    def execute_script(self, script_name, node_id):
        try:
            script_path = os.path.join(os.environ["DOWNLOAD_SCRIPT_PATH"], script_name)
            self.logger.info("in node: %s, start execute script: %s "%(node_id, script_path))
            db = Sqlite3DB(os.environ["PROJECT_DATABASE_PATH"])
            find_sql = "select node_ip, auth_user, auth_passwd, node_port from node_manage where _id=?"
            node_info = db.find_one(find_sql, node_id)[0]
            node_ssh = NodeSSH(*node_info)
            error = node_ssh.init_ssh()
            status = True
            message = "None"
            if error:
                status = False
                message = error
                self.logger.error("init connnect error: %s -- %s"%(error, node_info))
                node_ssh.close_conn()
            else:
                message = node_ssh.execute_script(script_path)
                node_ssh.close_conn()
                self.logger.debug("script execute result = %s"%message)
                log_name = "%s_%s.log"%(node_id, time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())))
                log_path = os.path.join(os.environ["DOWNLOAD_LOG_PATH"], log_name)
                # 保存脚本执行日志
                with open(log_path,'w') as up:
                    up.write(message)
                self.logger.debug("node id: '%s', update log filename: '%s' to db"%(node_id, log_name))
                # 更新日志文件到数据
                update_sql = "update node_manage set last_detect_time=%f, last_detect_log='%s' where _id=?"%(time.time(), log_name)
                print update_sql
                data = [(node_id,)]
                db.update(update_sql, data)
            return message
        except Exception, e:
            return str(e)
        finally:
            del db




