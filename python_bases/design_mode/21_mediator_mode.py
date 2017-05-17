# -*- coding: utf-8 -*-
# ===================================
# ScriptName : 21_mediator_mode.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-05-17 14:31
# ===================================

"""
中介者模式

模式特点：用一个对象来封装一系列的对象交互，中介者使各对象不需要显示地相互引用，从而使耦合松散，而且可以独立地改变它们之间的交互。

程序实例：两个对象通过中介者相互通信

代码特点：无
"""

class Mediator:
    def Send(self,message,col):
        pass

class Colleague:
    def __init__(self,temp):
        self.mediator = temp

class Colleague1(Colleague):
    def Send(self,message):
        self.mediator.Send(message,self)
    def Notify(self,message):
        print "Colleague1 get a message:%s" %message

class Colleague2(Colleague):
    def Send(self,message):
        self.mediator.Send(message,self)
    def Notify(self,message):
        print "Colleague2 get a message:%s" %message

class ConcreteMediator(Mediator):
    def Send(self,message,col):
        if(col==col1):
            col2.Notify(message)
        else:
            col1.Notify(message)

if __name__ == "__main__":
    m =ConcreteMediator()
    col1 = Colleague1(m)
    col2 = Colleague2(m)
    m.col1=col1
    m.col2=col2
    col1.Send("How are you?")
    col2.Send("Fine.")