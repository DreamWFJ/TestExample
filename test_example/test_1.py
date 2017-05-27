# -*- coding: utf-8 -*-
# ===================================
# ScriptName : test_1.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-05-26 10:21
# ===================================
import os
import multiprocessing
import argparse
import collections

def handle_commandline():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--concurrency", type=int,
                        default=multiprocessing.cpu_count(),
                        help="specify the concurrency (for debugging and timing) [default: %(default)d]")
    parser.add_argument("-s", "--size",
                        default=400, type=int,
                        help="make a scaled image that fits the given dimension [default: %s(default)d]")
    parser.add_argument("source",
                        help="the directory containing the original .xpm images")
    args = parser.parse_args()
    source = os.path.abspath(args.source)
    return args.size, source, args.concurrency

if __name__ == '__main__':
    print handle_commandline()
    Result = collections.namedtuple("Result", "copied scaled name")
    q = multiprocessing.JoinableQueue()
