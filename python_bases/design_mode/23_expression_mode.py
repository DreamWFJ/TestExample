# -*- coding: utf-8 -*-
# ===================================
# ScriptName : 23_expression_mode.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-05-17 14:48
# ===================================

"""
解释器模式

模式特点：给定一个语言，定义它的文法的一种表示，并定义一个解释器，这个解释器使用该表示来解释语言中的句子。

程序实例：（只是模式特点的最简单示范）

代码特点：无
"""

class Context:
    def __init__(self):
        self.input=""
        self.output=""

class AbstractExpression:
    def Interpret(self,context):
        pass

class Expression(AbstractExpression):
    def Interpret(self,context):
        print "terminal interpret"

class NonterminalExpression(AbstractExpression):
    def Interpret(self,context):
        print "Nonterminal interpret"

if __name__ == "__main__":
    context= ""
    c = []
    c = c + [Expression()]
    c = c + [NonterminalExpression()]
    c = c + [Expression()]
    c = c + [Expression()]
    for a in c:
        a.Interpret(context)