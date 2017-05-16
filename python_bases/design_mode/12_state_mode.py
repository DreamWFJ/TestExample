# -*- coding: utf-8 -*-
# ===================================
# ScriptName : 12_state_mode.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-05-16 16:25
# ===================================

"""
模式特点：当一个对象的内在状态改变时允许改变其行为，这个对象看起来像是改变了其类。

程序实例：描述一个程序员的工作状态，当需要改变状态时发生改变，不同状态下的方法实现不同

代码特点：无
"""

class State:
    def WirteProgram(self):
        pass

class Work:
    def __init__(self):
        self.hour = 9
        self.current = ForenoonState()
    def SetState(self,temp):
        self.current = temp
    def WriteProgram(self):
        self.current.WriteProgram(self)

class NoonState(State):
    def WriteProgram(self,w):
        print "noon working"
        if (w.hour<13):
            print "fun."
        else:
            print "need to rest."

class ForenoonState(State):
    def WriteProgram(self,w):
        if (w.hour<12):
            print "morning working"
            print "energetic"
        else:
            w.SetState(NoonState())
            w.WriteProgram()

if __name__ == "__main__":
    mywork = Work()
    mywork.hour = 9
    mywork.WriteProgram()
    mywork.hour =14
    mywork.WriteProgram()