# -*- coding: utf-8 -*-
# ===================================
# ScriptName : 15_combination_mode.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-05-17 9:47
# ===================================

"""
模式特点：将对象组合成成树形结构以表示“部分-整体”的层次结构

程序实例：公司人员的组织结构

代码特点：无
"""

class Component:
    def __init__(self,strName):
        self.m_strName = strName
    def Add(self,com):
        pass
    def Display(self,nDepth):
        pass

class Leaf(Component):
    def Add(self,com):
        print "leaf can't add"
    def Display(self,nDepth):
        strtemp = ""
        for i in range(nDepth):
            strtemp=strtemp+"-"
        strtemp=strtemp+self.m_strName
        print strtemp

class Composite(Component):
    def __init__(self,strName):
        self.m_strName = strName
        self.c = []
    def Add(self,com):
        self.c.append(com)
    def Display(self,nDepth):
        strtemp=""
        for i in range(nDepth):
            strtemp=strtemp+"-"
        strtemp=strtemp+self.m_strName
        print strtemp
        for com in self.c:
            com.Display(nDepth+2)

if __name__ == "__main__":
    p = Composite("Wong")
    p.Add(Leaf("Lee"))
    p.Add(Leaf("Zhao"))
    p1 = Composite("Wu")
    p1.Add(Leaf("San"))
    p.Add(p1)
    p.Display(1)