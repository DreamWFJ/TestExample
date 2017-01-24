# -*- coding: utf-8 -*-
# ===================================
# ScriptName : threading_simple.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2016-09-01 16:22
# ===================================
import threading
import time
import logging
import random

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
)

def test_1():
    def worker(num):
        print 'Worker ', num
        return

    threads = []
    for i in range(5):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

def test_2():
    def worker():
        print threading.currentThread().getName(), 'Starting'
        time.sleep(2)
        print threading.currentThread().getName(), 'Exiting'
    def my_service():
        print threading.currentThread().getName(), 'Starting'
        time.sleep(3)
        print threading.currentThread().getName(), 'Exiting'
    t = threading.Thread(name='my_service', target=my_service)
    w = threading.Thread(name='worker', target=worker)
    w2 = threading.Thread(target=worker)
    w.start()
    w2.start()
    t.start()

# 在线程中一般不像test_2中那样用print输出信息，而是用logging
# 而且Logging是线程安全的，所以来自不同线程的消息在输出中会有所区分
def test_3():
    def worker():
        logging.debug('Starting')
        time.sleep(2)
        logging.debug('Exiting')

    def my_service():
        logging.debug('Starting')
        time.sleep(3)
        logging.debug('Exiting')

    t = threading.Thread(name='my_service', target=my_service)
    w = threading.Thread(name='worker', target=worker)
    w2 = threading.Thread(target=worker)
    w.start()
    w2.start()
    t.start()

def test_4():
    def worker(num):
        t = threading.currentThread()
        pause = random.randint(1, 5)
        logging.debug('[%s] %s sleeping %s', num, t.name, pause)
        time.sleep(pause)
        logging.debug('[%s] %s sleep ending', num, t.name)
        return
    for i in range(3):
        t = threading.Thread(target=worker, args=(i,))
        t.setDaemon(True)
        t.start()

    main_thread = threading.currentThread()
    for t in threading.enumerate():
        if t is main_thread:
            continue
        logging.debug('joining %s', t.getName())
        t.join()

def test_5():
    def delayed():
        logging.debug('worker running')
        return
    # Timer在一个延迟之后开始工作
    t1 = threading.Timer(3, delayed)
    t1.setName('t1')
    t2 = threading.Timer(3, delayed)
    t2.setName('t2')

    logging.debug('starting timers')
    t1.start()
    t2.start()
    logging.debug('waiting before canceling %s', t2.getName())
    time.sleep(2)
    logging.debug('canceling %s', t2.getName())
    # 这里t2不会执行，因为此时主进程已经退出了
    t2.cancel()
    logging.debug('done')



if __name__ == '__main__':
    # test_1()
    # test_2()
    # test_3()
    # test_4()
    test_5()