# -*- coding: utf-8 -*-
# ===================================
# ScriptName : understand_look_around.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-01 8:48
# ===================================

import re

def test_1():
    print re.sub(r'(\d{4})-(\d{2})-(\d{2})', r'\2/\3/\1', '2016-01-11')
    # 输出：'01/11/2016'

def test_2():
    pattern = '(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})'
    print re.sub(pattern, r'\g<month>/\g<day>/\g<year>', '2016-01-11')
    # 输出：'01/11/2016'

def test_3():
    # (?=XX) 从左向右匹配，符合内容的字符串后面加空格
    print re.sub('(?=\d{3})', ' ', 'abc12345def')
    # 输出 'abc 1 2 345def'

def test_4():
    # (?!XX) 从左向右匹配，符合内容的字符串后面加空格
    print re.sub('(?!\d{3})', ' ', 'abc12345def')
    # 输出 ' a b c123 4 5 d e f '

def test_5():
    # (?<=XX) 从右向左匹配，符合内容的字符串前面加空格
    print re.sub('(?<=\d{3})', ' ', 'abc12345def')
    # 输出 'abc123 4 5 def'

def test_6():
    # (?<!XX) 从右向左匹配，符合内容的字符串前面加空格
    print re.sub('(?<!\d{3})', ' ', 'abc12345def')
    # 输出 ' a b c 1 2 345d e f '


if __name__ == '__main__':
    test_1()
    test_3()
    test_4()
    test_5()
    test_6()
    