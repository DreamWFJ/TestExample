# -*- coding: utf-8 -*-
# ==================================
# Author        : WFJ
# ScriptName    : threading_event.py
# CreateTime    : 2016-09-01 21:23
# ==================================

import logging
import threading
import time

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
)

def wait_for_event(e):
    logging.debug('wait_for_event starting')
    event_is_set = e.wait()
    logging.debug('event set: %s', event_is_set)


def wait_for_event_timeout(e, t):
    while not e.isSet():
        logging.debug('wait_for_event_timeout starting')
        event_is_set = e.wait(t)
        logging.debug('event set: %s', event_is_set)
        if event_is_set:
            logging.debug('processing event')
        else:
            logging.debug('doing other work')

def test_1():
    # 线程间的同步，通过Event管理一个内部标志，以set()和clear()方法控制这个标志
    # 使用wait()暂停，知道设置这个标志
    e = threading.Event()
    t1 = threading.Thread(
        name='block',
        target=wait_for_event,
        args=(e,)
    )
    t1.start()
    t2 = threading.Thread(
        name='nonblock',
        target=wait_for_event_timeout,
        args=(e, 2)
    )
    t2.start()
    logging.debug('waiting before calling Event.set()')
    time.sleep(3)
    e.set()
    logging.debug('event is set')


if __name__ == '__main__':
    test_1()
