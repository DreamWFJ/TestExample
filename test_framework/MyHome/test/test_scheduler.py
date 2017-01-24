# -*- coding: utf-8 -*-
# ===================================
# ScriptName : test_scheduler.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2016-12-08 13:31
# ===================================


import tornado
from apscheduler.schedulers.tornado import TornadoScheduler
sched = TornadoScheduler()


def job1(a, b, c):
    print "job1:", a,b,c


def job2(a, b, c):
    print "job2:", a,b,c

a_job = sched.add_job(job1, 'interval', seconds=1, minutes=0, next_run_time='2016-12-08 14:50:00', args=["a", "b", "c"])

# sched.add_job(job2, 'interval', seconds=1, kwargs={"a": "a", "b": "b", "c": "c"})
print a_job
sched.start()

a_job.reschedule('interval', minutes=5, seconds=1)


tornado.ioloop.IOLoop.instance().start()