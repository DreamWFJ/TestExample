# -*- coding: utf-8 -*-
# ===================================
# ScriptName : multiprocessing_mapreduce.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2016-09-02 18:20
# ===================================
import collections
import itertools
import multiprocessing

class SimpleMapReduce(object):
    def __init__(self, map_func, reduce_func, num_workers=None):
        self.map_func = map_func
        self.reduce_func = reduce_func
        self.pool = multiprocessing.Pool(num_workers)

    def partition(self, mapped_values):
        partitioned_data = collections.defaultdict(list)
        for key, value in mapped_values:
            partitioned_data[key].append(value)
        return partitioned_data.items()

    def __call__(self, inputs, chunksize=1):
        map_responses = self.pool.map(self.map_func,
                                      inputs,
                                      chunksize=chunksize)
        partitioned_data = self.partition(
            itertools.chain(*map_responses)
        )
        reduced_values = self.pool.map(self.reduce_func, partitioned_data)
        return reduced_values



if __name__ == '__main__':
    pass
    