# -*- coding: utf-8 -*-
# ===================================
# ScriptName : test_1.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2016-09-18 14:59
# ===================================

import re

def test_1():
    # s = r"/version/user((?P<bracket>/)(?(bracket)(?P<user_id>\w+)|\s*))?"
    s = r"/version/user((?P<bracket>/)(?(bracket)(?P<user_id>[\da-f]{8}(-[\da-f]{4}){3}-[\da-f]{12})|\s*))?"
    pattern = re.compile(s)
    print '\t', pattern.groupindex
    print '\t', pattern.groups
    for num, i in enumerate(['/version/user/4d3c47c6-4b66-4daf-bb4a-e0a67619cb83',
              '/version/user/fsa',
              '/version/users',
              '/version/user',
              '/version/user/',
              '/version/user//']):
        print '%s - re: %s' % (num, i)
        # match会从字符串最前面进行匹配，开始不一样，则匹配失败
        match = pattern.match(i)
        if match:
            print '\t', match.groups()
            print '\t', match.group(0)
            print '\t', match.group(1)
            print '\t', match.group(2)
            print '\t', match.group(3)
            print '\t',match.groupdict()

def test_2():
    text = '4d3c47c6-4b66-4daf-bb4a-e0a67619cb83'
    s = r'[\da-f]{8}(-[\da-f]{4}){3}-[\da-f]{12}'
    pattern = re.compile(s)
    match  = pattern.match(text)
    if match:
        print match.group()

if __name__ == '__main__':
    test_1()
    # test_2()
    