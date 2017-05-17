# -*- coding: utf-8 -*-
# ===================================
# ScriptName : 22_flyweight_mode.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-05-17 14:40
# ===================================

"""
享元模式

模式特点：运用共享技术有效地支持大量细粒度的对象。

程序实例：一个网站工厂，根据用户请求的类别返回相应类别的网站。如果这种类别的网站已经在服务器上，那么返回这种网站并加上不同用户的独特的数据；如果没有，那么生成一个。

代码特点：为了展示每种网站的由用户请求的次数，这里为它们建立了一个引用次数的字典。

　　　　　　之所以不用Python的sys模块中的sys.getrefcount()方法统计引用计数是因为有的对象可能在别处被隐式的引用，从而增加了引用计数。
"""

import sys

class WebSite:
    def Use(self):
        pass

class ConcreteWebSite(WebSite):
    def __init__(self,strName):
        self.name = strName
    def Use(self,user):
        print "Website type:%s,user:%s" %(self.name,user)

class UnShareWebSite(WebSite):
    def __init__(self,strName):
        self.name = strName
    def Use(self,user):
        print "UnShare Website type:%s,user:%s" %(self.name, user)

class WebFactory:
    def __init__(self):
        test = ConcreteWebSite("test")
        self.webtype ={"test":test}
        self.count = {"test":0}
    def GetWeb(self,webtype):
        if webtype not in self.webtype:
            temp = ConcreteWebSite(webtype)
            self.webtype[webtype] = temp
            self.count[webtype] =1
        else:
            temp = self.webtype[webtype]
            self.count[webtype] = self.count[webtype]+1
        return temp
    def GetCount(self):
        for key in self.webtype:
            #print "type: %s, count:%d" %(key,sys.getrefcount(self.webtype[key]))
            print "type: %s, count:%d " %(key,self.count[key])

if __name__ == "__main__":
    f = WebFactory()
    ws=f.GetWeb("blog")
    ws.Use("Lee")
    ws2=f.GetWeb("show")
    ws2.Use("Jack")
    ws3=f.GetWeb("blog")
    ws3.Use("Chen")
    ws4=UnShareWebSite("TEST")
    ws4.Use("Mr.Q")
    print f.webtype
    f.GetCount()