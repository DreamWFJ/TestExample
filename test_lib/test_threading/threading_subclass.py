# -*- coding: utf-8 -*-
# ===================================
# ScriptName : threading_subclass.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2016-09-01 16:57
# ===================================
import threading
import logging

logging.basicConfig(
        level=logging.DEBUG,
        format='[%(levelname)s] (%(threadName)-10s) %(message)s',
    )


def test_1():
    # Thread完成一些基本初始化，然后调用run方法，这会调用传递到构造函数的目标函数
    class MyThread(threading.Thread):
        def run(self):
            logging.debug('running')
            return

    for i in range(5):
        t = MyThread()
        t.start()

def test_2():
    class MyThreadWithArgs(threading.Thread):
        def __init__(self, group=None, target=None, name=None,
                     args=(), kwargs=None, verbose=None):
            threading.Thread.__init__(self, group=group,
                                      target=target,
                                      name=name,
                                      verbose=verbose)
            self.args = args
            self.kwargs = kwargs
            return
        def run(self):
            logging.debug('running with %s and %s',
                          self.args, self.kwargs)
            return

    for i in range(5):
        t = MyThreadWithArgs(args=(i,),
                             kwargs={'a':'A', 'b':'B'})
        t.start()


if __name__ == '__main__':
    # test_1()
    test_2()
