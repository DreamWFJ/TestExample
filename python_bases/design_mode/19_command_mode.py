# -*- coding: utf-8 -*-
# ===================================
# ScriptName : 19_command_mode.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-05-17 14:06
# ===================================

"""
模式特点：将请求封装成对象，从而使可用不同的请求对客户进行参数化；对请求排队或记录请求日志，以及支持可撤消的操作。

程序实例：烧烤店有两种食物，羊肉串和鸡翅。客户向服务员点单，服务员将点好的单告诉大厨，由大厨进行烹饪。

代码特点：注意在遍历列表时不要用注释的方式删除，否则会出现bug。bug示例程序附在后面，我认为这是因为remove打乱了for迭代查询列表的顺序导致的。
"""

class Barbucer:
    def MakeMutton(self):
        print "Mutton"
    def MakeChickenWing(self):
        print "Chicken Wing"

class Command:
    def __init__(self,temp):
        self.receiver=temp
    def ExecuteCmd(self):
        pass

class BakeMuttonCmd(Command):
    def ExecuteCmd(self):
        self.receiver.MakeMutton()

class ChickenWingCmd(Command):
    def ExecuteCmd(self):
        self.receiver.MakeChickenWing()

class Waiter:
    def __init__(self):
        self.order =[]
    def SetCmd(self,command):
        self.order.append(command)
        print "Add Order"
    def Notify(self):
        for cmd in self.order:
            #self.order.remove(cmd)
            #lead to a bug
            cmd.ExecuteCmd()


if __name__ == "__main__":
    barbucer=Barbucer()
    cmd=BakeMuttonCmd(barbucer)
    cmd2=ChickenWingCmd(barbucer)
    girl=Waiter()
    girl.SetCmd(cmd)
    girl.SetCmd(cmd2)
    girl.Notify()
    