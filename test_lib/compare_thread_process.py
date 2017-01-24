# -*- coding: utf-8 -*-
# ===================================
# ScriptName : compare_thread_process.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2016-09-05 15:10
# ===================================
import threading
import multiprocessing
import eventlet
import time

def count(s, d):
    print s, d
    r = 0
    while True:
        if r > d:
            break
        r = s + 1
    print 'result: ',r
    return r

def test_threading(n, s, d):
    l = [
        threading.Thread(target=count, args=(s, d))
        for i in range(n)
    ]
    for i in l:
        i.start()
    for i in l:
        i.join()

def test_eventlet(n, s, d):
    pool = eventlet.GreenPool(n)
    pool.imap(count, s, d)

def test_process(n, s, d):
    l = [
        multiprocessing.Process(target=count, args=(s, d))
        for i in range(n)
    ]
    for i in l:
        i.start()
    for i in l:
        i.join()

def test(num=1, start=1, end=100):
    t = time.clock()
    test_process(num, start, end)
    tp = time.clock()
    test_eventlet(num, start, end)
    te = time.clock()
    test_threading(num, start, end)
    tt = time.clock()
    print "process total time: ", tp-t
    print "eventlet total time: ", te - tp
    print "threading total time: ", tt- te

if __name__ == '__main__':
    test()
    # test(1, 1, 1000)
    # test(1, 1, 100000)
    # test(1, 1, 1000000)
    