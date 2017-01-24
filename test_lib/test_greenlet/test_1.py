# -*- coding: utf-8 -*-
# ===================================
# ScriptName : test_1.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2016-09-05 14:14
# ===================================
import greenlet
from greenlet import greenlet

def test_1():

    def read_next_char():
        g_self = greenlet.getcurrent()
        next_char = g_self.parent.switch()
        return next_char

    def process_commands(*args):
        while True:
            line = ''
            while not line.endswith('\n'):
                line += read_next_char()
            if line == 'quit\n':
                print 'are you sure?'
                if read_next_char() not in ['Y', 'y']:
                    continue
            process_commands(line)

    # g_processor = greenlet(process_commands)
    # g_processor.switch(*args)
    # gui.mainloop()

    # def event_keydown(key):
    #     g_processor.switch(key)

def test_2():
    # 协程
    def test1():
        print 12
        gr2.switch()
        print 34
    def test2():
        print 56
        gr1.switch()
        print 78

    gr1 = greenlet(test1)
    gr2 = greenlet(test2)
    gr1.switch()

def test_3():
    # 注意这里的切换
    def test1(x, y):
        print "x y",x, y
        # 将x+y的结果发送到gr2，即跳到test2中执行，然后将42发送过来，赋值给z，继续向下执行
        z = gr2.switch(x+y)
        print "test1: ", z
        gr2.switch(500)

    def test2(u):
        print "test2: ",u
        g = gr1.switch(42)
        print "test2 g: ",g

    gr1 = greenlet(test1)
    gr2 = greenlet(test2)
    gr1.switch("hello", " world")

if __name__ == '__main__':
    test_2()
    # test_3()
    