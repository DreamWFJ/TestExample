# -*- coding: utf-8 -*-
# ===================================
# ScriptName : threading_daemon.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2016-09-01 16:37
# ===================================
import threading
import time
import logging


def test_1():
    # 输出结果不会有守护线程的'Exiting'消息，因为在守护线程从2s睡眠唤醒之前，主线程和非守护线程以及退出
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(levelname)s] (%(threadName)-10s) %(message)s',
    )

    def daemon():
        logging.debug('Starting')
        time.sleep(2)
        logging.debug('Exiting')

    def non_daemon():
        logging.debug('Starting')
        logging.debug('Exiting')

    d = threading.Thread(name='daemon', target=daemon)
    d.setDaemon(True)
    t = threading.Thread(name='non-daemon', target=non_daemon)
    d.start()
    t.start()


def test_2():
    # 同test_1比较，会等待守护进程退出，主进程才会退出
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(levelname)s] (%(threadName)-10s) %(message)s',
    )
    def daemon():
        logging.debug('Starting')
        time.sleep(2)
        logging.debug('Exiting')

    def non_daemon():
        logging.debug('Starting')
        logging.debug('Exiting')

    d = threading.Thread(name='daemon', target=daemon)
    d.setDaemon(True)
    t = threading.Thread(name='non-daemon', target=non_daemon)
    d.start()
    t.start()
    # 可以设置等待时间，超过时间后，就不阻塞了
    d.join(1)
    logging.debug('d.isAlive() %s', d.isAlive())
    t.join()

if __name__ == '__main__':
    # test_1()
    test_2()
