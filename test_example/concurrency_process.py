# -*- coding: utf-8 -*-
# ===================================
# ScriptName : concurrency_process.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-05-27 10:47
# ===================================

"""
下面是一个简单的并发计算实现
思想：并发尽量不共享数据，--> 尽量不修改数据 --> 使用复制版本 --> 使用队列
"""

import sys
import math
import os
import Image
import multiprocessing
import argparse
import collections
import concurrent.futures

def handle_commandline():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--concurrency", type=int,
                        default=multiprocessing.cpu_count(),
                        help="specify the concurrency (for debugging and timing) [default: %(default)d]")
    parser.add_argument("-s", "--size",
                        default=400, type=int,
                        help="make a scaled image that fits the given dimension [default: %s(default)d]")
    parser.add_argument("-S", "--smooth", action="store_true",
                        help="use smooth scaling (slow but good for text)")
    parser.add_argument("source",
                        help="the directory containing the original .xpm images")
    parser.add_argument("target",
                        help="the directory for the scaled .xpm images")
    args = parser.parse_args()
    source = os.path.abspath(args.source)
    target = os.path.abspath(args.target)
    if source == target:
        args.error("source and target must be diffent")
    if not os.path.exists(args.target):
        os.makedirs(target)
    return args.size, args.smooth, source, target, args.concurrency

Result = collections.namedtuple("Result", "copied scaled name")
Summary = collections.namedtuple("Summary", "todo copied scaled canceled")

def report(message="", error=False):
    if len(message) >= 70 and not error:
        message = message[:67] + "..."
    sys.stdout.write("\r{:70}{}".format(message, "\n" if error else ""))
    sys.stdout.flush()

def scale(size, smooth, source, target, concurrency):
    canceled = False
    jobs = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()
    create_processes(size, smooth, jobs, results, concurrency)
    todo = add_jobs(source, target, jobs)
    try:
        jobs.join()
    except KeyboardInterrupt:
        report("canceling...")
        canceled = True
    copied = scaled = 0
    while not results.empty():
        result = results.get_nowait()
        copied += result.copied
        scaled += result.scaled
    return Summary(todo, copied, scaled, canceled)

def scale1(size, smooth, source, target, concurrency):
    futures = set()
    with concurrent.futures.ProcessPoolExecutor(max_workers=concurrency) as executor:
        for sourceImage, targetImage in get_jobs(source, target):
            future = executor.submit(scale_one, size, smooth, sourceImage, targetImage)
            futures.add(future)
        summary = wait_for(futures)
        if summary.canceled:
            executor.shutdown()
        return summary

def get_jobs(source, target):
    for name in os.listdir(source):
        yield os.path.join(source, name), os.path.join(target, name)

def wait_for(futures):
    canceled = False
    copied = scaled = 0
    try:
        # 这里as_completed会持续阻塞，直到有future完工或取消
        for future in concurrent.futures.as_completed(futures):
            err = future.exception()
            if err is None:
                result = future.result()
                copied += result.copied
                scaled += result.scaled
                report("{} {}".format("copied" if result.copied else "scaled", os.path.basename(result.name)))
            elif isinstance(err, Image.Error):
                report(str(err), True)
            else:
                raise err
    except KeyboardInterrupt:
        report("canceling...")
        canceled = True
        for future in futures:
            future.cancel()
    return Summary(len(futures), copied, scaled, canceled)


def create_processes(size, smooth, jobs, results, concurrency):
    for _ in range(concurrency):
        process = multiprocessing.Process(target=worker, args=(size, smooth, jobs, results))
        process.daemon = True
        process.start()

def worker(size, smooth, jobs, results):
    while True:
        try:
            sourceImage, targetImage = jobs.get()
            try:
                result = scale_one(size, smooth, sourceImage, targetImage)
                report("{} {}".format("copied" if result.copied else "scaled", os.path.basename(result.name)))
                results.put(result)
            except Image.Error as err:
                report(str(err), True)
        finally:
            jobs.task_done()

def add_jobs(source, target, jobs):
    for todo, name in enumerate(os.listdir(source), start=1):
        sourceImage = os.path.join(source, name)
        targetImage = os.path.join(target, name)
        jobs.put((sourceImage, targetImage))
    return todo

def scale_one(size, smooth, sourceImage, targetImage):
    oldImage = Image.from_file(sourceImage)
    if oldImage.width <= size and oldImage.height <= size:
        oldImage.save(targetImage)
        return Result(1, 0, targetImage)
    else:
        if smooth:
            scale = min(size / oldImage.width, size / oldImage.height)
            newImage = oldImage.scale(scale)
        else:
            stride = int(math.ceil(max(oldImage.width / size, oldImage.height / size)))
            newImage = oldImage.subsample(stride)
    newImage.save(targetImage)
    return Result(0, 1, targetImage)

def summarize(summary, concurrency):
    message = "copied {} scaled {}".format(summary.copied, summary.scaled)
    difference = summary.todo - (summary.copied + summary.scaled)
    if difference:
        message += "skipped {} ".format(difference)
    message += "using {} processes".format(concurrency)
    if summary.canceled:
        message += " [canceled]"
    report(message)
    print

if __name__ == '__main__':
    size, smooth, source, target, concurrency = handle_commandline()
    report("string...")
    summary = scale(size, smooth, source, target, concurrency)
    summarize(summary, concurrency)

    