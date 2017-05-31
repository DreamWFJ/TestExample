# -*- coding: utf-8 -*-
# ===================================
# ScriptName : parser_config.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-05-31 15:51
# ===================================

import ConfigParser

"""
主要说明配置文件的高级写法，参考example.conf
"""

def test():
    conf = ConfigParser.ConfigParser()
    conf.read('example.conf')
    print conf.get('db1', "conn_str")
    print conf.get('db2', "conn_str")


if __name__ == '__main__':
    test()
    