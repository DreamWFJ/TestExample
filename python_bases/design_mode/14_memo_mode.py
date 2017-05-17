# -*- coding: utf-8 -*-
# ===================================
# ScriptName : 14_memo_mode.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-05-17 9:23
# ===================================

"""
模式特点：在不破坏封装性的前提下捕获一个对象的内部状态，并在该对象之外保存这个状态，以后可以将对象恢复到这个状态。

程序实例：将Originator对象的状态封装成Memo对象保存在Caretaker内

代码特点：无
"""

class Originator:
    def __init__(self):
        self.state = ""
    def Show(self):
        print self.state
    def CreateMemo(self):
        return Memo(self.state)
    def SetMemo(self,memo):
        self.state = memo.state

class Memo:
    state= ""
    def __init__(self,ts):
        self.state = ts

class Caretaker:
    memo = ""

if __name__ == "__main__":
    on = Originator()
    on.state = "on"
    on.Show()
    c = Caretaker()
    c.memo=on.CreateMemo()
    on.state="off"
    on.Show()
    on.SetMemo(c.memo)
    on.Show()