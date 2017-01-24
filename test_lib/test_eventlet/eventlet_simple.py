# -*- coding: utf-8 -*-
# ===================================
# ScriptName : eventlet_simple.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2016-09-05 14:01
# ===================================

import thread
from eventlet import tpool

def test_1():
    def my_func(starting_ident):
        print 'starting_ident: ',starting_ident
        print 'running in new thread: ', starting_ident != thread.get_ident()
    tpool.execute(my_func, thread.get_ident())


if __name__ == '__main__':
    test_1()
    