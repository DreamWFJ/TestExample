# -*- coding: utf-8 -*-
# ===================================
# ScriptName : test_2.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2016-09-01 14:40
# ===================================

import signal
import os
import time



def receive_signal(signum, stack):
    print 'Received:',signum

def alarm_received(n, stack):
    return

def test_1():
    # 注册信号句柄
    signal.signal(signal.SIGUSR1, receive_signal)
    signal.signal(signal.SIGUSR2, receive_signal)

    print 'My PID is :', os.getpid()

    while True:
        print 'Waiting...'
        time.sleep(3)

def test_2():
    signal.signal(signal.SIGALRM, alarm_received)
    signals_to_names = dict(
        (getattr(signal, n), n)
        for n in dir(signal)
        if n.startswith('SIG') and '_' not in n

    )
    for s, name in sorted(signals_to_names.items()):
        # 查看信号注册了哪些处理程序
        handler = signal.getsignal(s)
        if handler is signal.SIG_DFL:
            handler = 'SIG_DFL'
        elif handler is signal.SIG_IGN:
            handler = 'SIG_IGN'
        print '%-10s (%2d):' % (name, s), handler

def receive_alarm(signum, stack):
    print 'Alarm :', time.ctime()


def test_3():
    # 2s 后接受闹铃信号
    signal.signal(signal.SIGALRM, receive_alarm)
    signal.alarm(2)
    # sleep不会完全持续4s
    print 'Before: ', time.ctime()
    time.sleep(4)
    print 'After : ', time.ctime()


def do_exit(sig, stack):
    raise SystemExit('Exiting')

def test_4():
    # 忽略信号，SIGINT是中断信号，Ctrl-C
    # 首先将SIGINT信号替换为SIG_IGN信号，然后注册SIGUSR1信号
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    signal.signal(signal.SIGUSR1, do_exit)
    print 'My PID is :', os.getpid()
    signal.pause()

import threading
def signal_handler(num, stack):
    print 'in [signal_handler] Current pid %d and ThreadName %s' % (os.getpid(), threading.currentThread().name)
    print 'Received signal %d in %s' % (num, threading.currentThread().name)

def wait_for_signal():
    print 'in [wait_for_signal] Current pid %d and ThreadName %s' % (os.getpid(), threading.currentThread().name)
    print 'Waiting for signal in', threading.currentThread().name
    signal.pause()
    print 'Done waiting'

def send_signal():
    print 'in [send_signal] Current pid %d and ThreadName %s' % (os.getpid(), threading.currentThread().name)
    print 'Sinding signal in', threading.currentThread().name
    os.kill(os.getpid(), signal.SIGUSR1)

def test_5():
    # 信号在进程与线程之间不能很好的结合，只有进程的主线程才可以接收信号
    # 因此主线程发的信号，其它线程不能收到，这里调用alarm信号避免无限阻塞，因为接收者永不退出
    signal.signal(signal.SIGUSR1, signal_handler)
    receiver = threading.Thread(target=wait_for_signal, name='receiver')
    receiver.start()
    time.sleep(0.1)
    sender = threading.Thread(target=send_signal, name='sender')
    sender.start()
    sender.join()
    print 'Waiting for ',receiver.name
    signal.alarm(4)
    receiver.join()




if __name__ == '__main__':
    # test_1()
    # test_2()
    # test_3()
    # test_4()
    test_5()