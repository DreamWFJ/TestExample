# -*- coding: utf-8 -*-
# ===================================
# ScriptName : example.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-30 10:40
# ===================================
from pprint import pprint
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper



def test_1():
    with file('config.yaml') as stream:
        data = load(stream, Loader=Loader)
        print "data: ",data
        output = dump(data, Dumper=Dumper)
        print "output: ",output

def test_2():
     with file('config.yaml') as stream:
        data = load(stream)
        pprint(data)
if __name__ == '__main__':
    test_2()
    