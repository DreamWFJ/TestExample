# -*- coding: utf-8 -*-
# ===================================
# ScriptName : multiprocessing_import_worker.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2016-09-02 9:37
# ===================================

import multiprocessing
import threading

def worker():
    print 'Worker', threading.currentThread().name, multiprocessing.current_process().name
    return