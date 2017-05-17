# -*- coding: utf-8 -*-
# ===================================
# ScriptName : 18_bridge_mode.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-05-17 14:02
# ===================================

"""
模式特点：将抽象部分与它的实现部分分离，使它们都可以独立地变化。

程序实例：两种品牌的手机，要求它们都可以运行游戏和通讯录两个软件，而不是为每个品牌的手机都独立编写不同的软件。

代码特点：虽然使用了object的新型类，不过在这里不是必须的，是对在Python2.2之后“尽量使用新型类”的建议的遵从示范。
"""


class HandsetSoft(object):
    def Run(self):
        pass

class HandsetGame(HandsetSoft):
    def Run(self):
        print "Game"

class HandsetAddressList(HandsetSoft):
    def Run(self):
        print "Address List"

class HandsetBrand(object):
    def __init__(self):
        self.m_soft = None
    def SetHandsetSoft(self,temp):
        self.m_soft= temp
    def Run(self):
        pass

class HandsetBrandM(HandsetBrand):
    def Run(self):
        if not (self.m_soft == None):
            print "BrandM"
            self.m_soft.Run()

class HandsetBrandN(HandsetBrand):
    def Run(self):
        if not (self.m_soft == None):
            print "BrandN"
            self.m_soft.Run()

if __name__ == "__main__":
    brand = HandsetBrandM()
    brand.SetHandsetSoft(HandsetGame())
    brand.Run()
    brand.SetHandsetSoft(HandsetAddressList())
    brand.Run()
    