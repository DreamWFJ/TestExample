# -*- coding: utf-8 -*-
# ===================================
# ScriptName : multiprocessing_simple.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2016-09-02 9:30
# ===================================
import os
import sys
import logging
import random
import time
import threading
import multiprocessing
"""
    跟管理线程类似管理进程
"""

def worker(num):
    print 'Worker', num, threading.currentThread().name, multiprocessing.current_process().name
    sys.stdout.flush()
    return

def test_1():
    jobs = []
    for i in range(5):
        # 这里要求传入的参数是能够使用pickle串行化
        p = multiprocessing.Process(target=worker, args=(i,))
        jobs.append(p)
        p.start()

def daemon():
    p = multiprocessing.current_process()
    print 'Starting:',p.name, p.pid
    sys.stdout.flush()
    time.sleep(2)
    print 'Exiting :', p.name, p.pid
    sys.stdout.flush()

def non_daemon():
    p = multiprocessing.current_process()
    print 'Starting:',p.name, p.pid
    sys.stdout.flush()
    time.sleep(2)
    print 'Exiting :', p.name, p.pid
    sys.stdout.flush()

def test_2():
    # def daemon():
    #     p = multiprocessing.current_process()
    #     print 'Starting:',p.name, p.pid
    #     sys.stdout.flush()
    #     time.sleep(2)
    #     print 'Exiting :', p.name, p.pid
    #     sys.stdout.flush()
    d = multiprocessing.Process(name='daemon', target=daemon,)
    # ???????????? 这里不知道为什么在__main__下面设置就能成功运行，否则报错
    # 不是上面的原因，原来是target函数定义在test_2下面，而默认是在__main__下面寻找
    d.daemon = True
    n = multiprocessing.Process(name='non-daemon', target=non_daemon,)
    n.daemon = False
    d.start()
    time.sleep(1)
    n.start()
    d.join(1)
    print 'd.is_alive()',d.is_alive()
    n.join()

def show_worker():
    print 'Starting worker'
    time.sleep(0.1)
    print 'Finished worker'

def test_3():
    p = multiprocessing.Process(target=show_worker)
    print 'BEFORE: ', p, p.is_alive()

    p.start()
    print 'DURING: ', p, p.is_alive()

    p.terminate()
    print 'TERMINATERD: ', p, p.is_alive()

    p.join()
    print 'JOINED: ', p, p.is_alive()

def exit_error():
    sys.exit(1)

def exit_ok():
    return

def return_value():
    return 1

def raises():
    raise RuntimeError('There was an error!')

def terminated():
    time.sleep(3)

def test_4():
    jobs = []
    for f in [exit_error, exit_ok, return_value, raises, terminated]:
        print 'Starting process for', f.func_name
        j = multiprocessing.Process(target=f, name=f.func_name)
        jobs.append(j)
        j.start()
    jobs[-1].terminate()
    for j in jobs:
        j.join()
        print '%15s.exitcode = %s ' %(j.name, j.exitcode)

def test_5():
    # 修改默认消息输出格式
    multiprocessing.log_to_stderr(logging.DEBUG)
    p = multiprocessing.Process(target=worker, args=("test_5",))
    p.start()
    p.join()

def test_6():
    # 默认等级是NOTSET，即不产生任何消息
    multiprocessing.log_to_stderr()
    logger = multiprocessing.get_logger()
    logger.setLevel(logging.INFO)
    p = multiprocessing.Process(target=worker, args=("test_5",))
    p.start()
    p.join()


class Worker(multiprocessing.Process):
    def run(self):
        print 'In %s ' % self.name
        return

def test_7():
    jobs = []
    for i in range(5):
        p = Worker()
        jobs.append(p)
        p.start()
    for j in jobs:
        j.join()


class MyFancyClass(object):
    def __init__(self, name):
        self.name = name

    def do_something(self):
        proc_name = multiprocessing.current_process().name
        print 'Doing something fancy in %s for %s!' %(proc_name, self.name)


def worker_1(q):
    obj = q.get()
    obj.do_something()

def test_8():
    # 向进程传递消息
    queue = multiprocessing.Queue()
    p = multiprocessing.Process(target=worker_1, args=(queue,))
    p.start()
    queue.put(MyFancyClass('Fancy Dan'))
    # 等待worker_1结束
    queue.close()
    queue.join_thread()
    p.join()

class Consumer(multiprocessing.Process):
    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        proc_name = self.name
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                print '%s: Exiting' % proc_name
                self.task_queue.task_done()
                break
            print '%s : %s' %(proc_name, next_task)
            answer = next_task()
            print 'answer: ',answer
            self.task_queue.task_done()
            self.result_queue.put(answer)
        return

class Task(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __call__(self):
        time.sleep(0.1)

    def __str__(self):
        return '---- %s * %s' %(self.a, self.b)

def test_9():
    tasks = multiprocessing.JoinableQueue()
    # tasks.task_done()
    results = multiprocessing.Queue()
    num_consumers = multiprocessing.cpu_count() * 2
    print 'Creating %d consumers' % num_consumers
    consumers = [Consumer(tasks, results) for i in xrange(num_consumers)]
    for w in consumers:
        w.start()
    print "============================="
    num_jobs = 10
    for i in xrange(num_jobs):
        print "== ",i
        tasks.put(Task(i, i))
    for i in xrange(num_consumers):
        tasks.put(None)
    print "111111111111111111"
    while num_jobs:
        result = results.get()
        print 'Result:',result
        num_jobs -= 1

class ActivePool(object):
    def __init__(self):
        super(ActivePool, self).__init__()
        self.mgr = multiprocessing.Manager()
        self.active = self.mgr.list()
        self.lock = multiprocessing.Lock()

    def makeActive(self, name):
        with self.lock:
            self.active.append(name)
    def makeInactive(self, name):
        with self.lock:
            self.active.remove(name)
    def __str__(self):
        with self.lock:
            return str(self.active)

def worker_2(s, pool):
    name = multiprocessing.current_process().name
    with s:
        pool.makeActive(name)
        print 'Now running: %s' % str(pool)
        time.sleep(random.random)
        pool.makeInactive(name)

def test_10():
    pool = ActivePool()
    s = multiprocessing.Semaphore(3)
    jobs = [
        multiprocessing.Process(target=worker_2,
                                name=str(i),
                                args=(s, pool),
                                )
        for i in range(10)
    ]
    for j in jobs:
        j.start()
    for j in jobs:
        j.join()
        print 'Now running : %s' % str(pool)

def worker_3(d, key, value):
    d[key] = value

def test_11():
    # 管理共享状态
    mgr = multiprocessing.Manager()
    d = mgr.dict()
    jobs = [
        multiprocessing.Process(target=worker_3, args=(d, i, i*2))
        for i in range(10)
    ]
    for j in jobs:
        j.start()
    for j in jobs:
        j.join()
    print 'Results:',d

def producer(ns, event):
    ns.value = 'This is the value'
    # 注意，对于可变值内容的更新不会自动传播，下面consumer中打印的my_list为[]
    ns.my_list = []
    ns.my_list.append('This the value')
    event.set()

def consumer(ns, event):
    try:
        value = ns.value
    except Exception, err:
        print 'Before event, error:', str(err)
    try:
        value = ns.my_list
    except Exception, err:
        print 'Before event, error:', str(err)

    event.wait()
    print 'After event:', ns.value
    print 'After event:', ns.my_list

def test_12():
    mgr = multiprocessing.Manager()
    namespace = mgr.Namespace()
    # namespace.my_list = []
    event = multiprocessing.Event()
    p = multiprocessing.Process(target=producer, args=(namespace, event))
    c = multiprocessing.Process(target=consumer, args=(namespace, event))
    c.start()
    p.start()
    c.join()
    p.join()

def do_calculation(data):
    return data * 2

def start_process():
    print 'Starting', multiprocessing.current_process().name

def test_13():
    inputs = list(range(10))
    print 'Input    :',inputs
    builtin_outputs = map(do_calculation, inputs)
    print 'builtin_outputs :',builtin_outputs
    pool_size = multiprocessing.cpu_count() * 2
    pool = multiprocessing.Pool(processes=pool_size,
                                # 设置该参数告诉池在完成一些任务后要重启一个工作进程
                                maxtasksperchild=2,
                                initializer=start_process,)
    pool_outputs = pool.map(do_calculation, inputs)
    pool.close()
    pool.join()
    print 'Pool     :',pool_outputs


if __name__ == '__main__':
    # test_1()
    # test_2()
    # test_3()
    # test_4()
    # test_5()
    # test_6()
    # test_7()
    # test_8()
    # test_9()
    # test_10()
    # test_11()
    # test_12()
    test_13()