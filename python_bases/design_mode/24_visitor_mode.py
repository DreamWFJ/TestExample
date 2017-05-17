# -*- coding: utf-8 -*-
# ===================================
# ScriptName : 24_visitor_mode.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-05-17 14:51
# ===================================

"""
访问者模式

模式特点：表示一个作用于某对象结构中的各元素的操作。它使你可以在不改变各元素的类的前提下定义作用于这些元素的新操作。

程序实例：对于男人和女人（接受访问者的元素，ObjectStructure用于穷举这些元素），不同的遭遇（具体的访问者）引发两种对象的不同行为。

代码特点：无
"""

class Person:
    def Accept(self,visitor):
        pass

class Man(Person):
    def Accept(self,visitor):
        visitor.GetManConclusion(self)

class Woman(Person):
    def Accept(self,visitor):
        visitor.GetWomanConclusion(self)

class Action:
    def GetManConclusion(self,concreteElementA):
        pass
    def GetWomanConclusion(self,concreteElementB):
        pass

class Success(Action):
    def GetManConclusion(self,concreteElementA):
        print "男人成功时，背后有个伟大的女人"
    def GetWomanConclusion(self,concreteElementB):
        print "女人成功时，背后有个不成功的男人"

class Failure(Action):
    def GetManConclusion(self,concreteElementA):
        print "男人失败时，闷头喝酒，谁也不用劝"
    def GetWomanConclusion(self,concreteElementB):
        print "女人失败时，眼泪汪汪，谁也劝不了"


class ObjectStructure:
    def __init__(self):
        self.plist=[]
    def Add(self,p):
        self.plist=self.plist+[p]
    def Display(self,act):
        for p in self.plist:
            p.Accept(act)

if __name__ == "__main__":
    os = ObjectStructure()
    os.Add(Man())
    os.Add(Woman())
    sc = Success()
    os.Display(sc)
    fl = Failure()
    os.Display(fl)
    