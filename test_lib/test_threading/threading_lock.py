# -*- coding: utf-8 -*-
# ==================================
# Author        : WFJ
# ScriptName    : threading_lock.py
# CreateTime    : 2016-09-01 21:36
# ==================================

import logging
import random
import threading
import time

# python内置数据结构（列表，字典等等）是线程安全的，这是python使用原子字节码
# 来管理这些数据结构的一个副作用（更新过程中不会释放GIL）

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
)

class Counter(object):
    def __init__(self, start=0):
        self.lock = threading.Lock()
        self.value = start
    def increment(self):
        logging.debug('Waiting for lock')
        self.lock.acquire()
        try:
            logging.debug('Acquired lock')
            self.value = self.value + 1
            logging.debug('Value is : %d', self.value)
        finally:
            self.lock.release()



def test_1():
    def worker(c):
        for i in range(2):
            pause = random.random()
            logging.debug('Sleeping %0.02f', pause)
            time.sleep(pause)
            c.increment()
        logging.debug('Done')

    counter = Counter()
    for i in range(2):
        t = threading.Thread(target=worker, args=(counter, ))
        t.start()
    logging.debug('Waiting for worker threads')
    main_thread = threading.currentThread()
    for t in threading.enumerate():
        if t is not main_thread:
            t.join()
    logging.debug('Counter: %d', counter.value)

def lock_holder(lock):
    logging.debug('Starting')
    while True:
        lock.acquire()
        try:
            logging.debug('Holding')
            time.sleep(0.5)
        finally:
            logging.debug('Not holding')
            lock.release()
        time.sleep(0.5)
    return

def test_2():
    # 模拟负载，查看请求次数
    def worker(lock):
        logging.debug('Starting')
        num_tries = 0
        num_acquires = 0
        while num_acquires < 3:
            time.sleep(0.5)
            logging.debug('Trying to acquire')
            # 设置超时时间为0，即请求一次，没有则离开，设置为1则表示1s内重复请求
            have_it = lock.acquire(0)
            try:
                num_tries += 1
                if have_it:
                    logging.debug('Iteration %d: Acquired', num_tries)
                    num_acquires += 1
                else:
                    logging.debug('Iteration %d: Not acqaured', num_tries)
            finally:
                if have_it:
                    lock.release()
        logging.debug('Done after %d iterations', num_tries)

    lock = threading.Lock()
    holder = threading.Thread(target=lock_holder,
                              args=(lock,),
                              name='LockHolder')
    holder.setDaemon(True)
    holder.start()
    worker = threading.Thread(target=worker,
                              args=(lock,),
                              name='Worker')
    worker.start()
    lock.acquire()

def test_3():
    # 如果同一个线程的不同代码需要'重新获得'锁，在这种情况下则要使用RLock
    lock = threading.RLock()
    print 'First try :', lock.acquire()
    print 'Second try:', lock.acquire(0)


def test_4():
    def work_with(lock):
        with lock:
            logging.debug('Lock acquired via with')

    def work_no_with(lock):
        lock.acquire()
        try:
            logging.debug('Lock acquired directly')
        finally:
            lock.release()

    lock = threading.Lock()
    w = threading.Thread(target=work_with, args=(lock,))
    nw = threading.Thread(target=work_no_with, args=(lock,))
    w.start()
    nw.start()

def test_5():
    # 同步线程
    def consumer(cond):
        logging.debug('Starting consumer thread')
        t = threading.currentThread()
        with cond:
            cond.wait()
            logging.debug('Resource is available to consumer')

    def producer(cond):
        logging.debug('Starting producer thread')
        with cond:
            logging.debug('Marking resource available')
            cond.notifyAll()

    condition = threading.Condition()
    c1 = threading.Thread(name='c1', target=consumer, args=(condition,))
    c2 = threading.Thread(name='c2', target=consumer, args=(condition,))
    p = threading.Thread(name='p', target=producer, args=(condition,))

    c1.start()
    time.sleep(2)
    c2.start()
    time.sleep(2)
    p.start()

class ActivePool(object):
    def __init__(self):
        super(ActivePool, self).__init__()
        self.active = []
        self.lock = threading.Lock()

    def makeActive(self, name):
        with self.lock:
            self.active.append(name)
            logging.debug('makeActive Running: %s', self.active)

    def makeInactive(self, name):
        with self.lock:
            self.active.remove(name)
            logging.debug('makeInactive Running: %s', self.active)

def test_6():
    # 限制资源的并发访问，连接池支持同时连接，但数目是固定的，使用Semaphore来管理
    def worker(s, pool):
        logging.debug('Waiting to join the pool')
        with s:
            name = threading.currentThread().getName()
            pool.makeActive(name)
            time.sleep(0.1)
            pool.makeInactive(name)

    pool = ActivePool()
    s = threading.Semaphore(3)
    for i in range(10):
        t = threading.Thread(target=worker, name=str(i),
                             args=(s, pool))
        t.start()

def test_7():
    def show_value(data):
        try:
            val = data.value
        except AttributeError:
            logging.debug('No value yet')
        else:
            logging.debug('value=%s', val)

    def worker(data):
        show_value(data)
        data.value = random.randint(1, 100)
        show_value(data)
    # local_data属性value对所有线程都不可见，除非它在某个线程中设置才能被该线程看到
    local_data = threading.local()
    show_value(local_data)
    local_data.value = 1000
    show_value(local_data)

    for i in range(2):
        t = threading.Thread(target=worker, args=(local_data, ))
        t.start()
    time.sleep(1)

    class MyLocal(threading.local):
        def __init__(self, value):
            logging.debug('id(self) = %d %d', id(self), value)
            logging.debug('Initializing %r', self)
            self.value = value
    local_data1 = MyLocal(1000)
    show_value(local_data1)

    for i in range(2):
        t = threading.Thread(target=worker, args=(local_data1, ))
        t.start()

if __name__ == '__main__':
    # test_1()
    # test_2()
    # test_3()
    # test_4()
    # test_5()
    # test_6()
    test_7()