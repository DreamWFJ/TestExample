#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:         WFJ
Version:        0.1.0
FileName:       test.py
CreateTime:     2016-11-29 22:10
"""

def test():
    data_field = ['_id', 'name', 'ip']
    data = [
        ('1', 'a', '123'),
        ('2', 'b', '234'),
        ('3', 'c', '345'),
        ('4', 'd', '456')
    ]
    def test(x, y):
        return {x:y}
    l = []
    for one in data:
        l.append(dict(zip(data_field, one)))
    print l

if __name__ == '__main__':
    test()