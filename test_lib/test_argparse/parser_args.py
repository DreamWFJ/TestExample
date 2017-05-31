# -*- coding: utf-8 -*-
# ===================================
# ScriptName : parser_args.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-05-31 15:58
# ===================================


import os
import argparse

def handle_commandline():
    parser = argparse.ArgumentParser(prog='PROG')
    parser.add_argument("-s", "--size",
                        default=400, type=int,
                        help="make a scaled image that fits the given dimension [default: %s(default)d]")
    parser.add_argument("source",
                        help="the directory containing the original .xpm images")

    group1 = parser.add_argument_group('group1', 'group1 description')
    group1.add_argument('foo', help='foo help')
    args = parser.parse_args()
    source = os.path.abspath(args.source)
    return args.size, source, args.concurrency

if __name__ == '__main__':
    print handle_commandline()

