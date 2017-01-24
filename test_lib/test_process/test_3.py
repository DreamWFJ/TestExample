# -*- coding: utf-8 -*-
# ===================================
# ScriptName : test_3.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2016-09-01 16:11
# ===================================

import signal
import time
import threading

def signal_handler(num, stack):
    print time.ctime(), 'Alarm in', threading.currentThread().name

def use_alarm():
    t_name = threading.currentThread().name
    print time.ctime(), 'Setting alarm in', t_name
    signal.alarm(1)
    print time.ctime(), 'Sleeping in', t_name
    time.sleep(3)
    print time.ctime(), 'Done with sleep in', t_name

def test_1():
    # 闹铃信号可以由任意线程设置，但是只能被主线程接收，并且闹铃信号不能终止除主线程外的其它线程的休眠
    signal.signal(signal.SIGALRM, signal_handler)
    alarm_thread = threading.Thread(target=use_alarm,
                                    name='alarm_thread')
    alarm_thread.start()
    time.sleep(0.1)
    print time.ctime(), 'Waiting for ', alarm_thread.name
    alarm_thread.join()
    print time.ctime(), 'Exiting normally'

if __name__ == '__main__':
    test_1()