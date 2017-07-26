#!/usr/bin/env python
# encoding: utf-8
"""
@author: youfeng
@email: youfeng243@163.com
@license: Apache Licence
@file: topN.py
@time: 2017/7/26 14:19
"""
import heapq
import random


class TopMaxHeap(object):
    def __init__(self, k):
        self.k = k
        self.data = []

    def push(self, item):
        if len(self.data) < self.k:
            heapq.heappush(self.data, item)
        else:
            topk_small = self.data[0]
            if item[0] > topk_small[0]:
                heapq.heapreplace(self.data, item)

    def topk(self):
        # return [x for x in reversed([heapq.heappop(self.data) for _ in xrange(len(self.data))])]
        return sorted(self.data, reverse=True, cmp=lambda x, y: cmp(x[0], y[0]))


class TopMinHeap(object):
    def __init__(self, k):
        self.k = k
        self.data = []

    def push(self, item):
        # Reverse item to convert to max-heap
        item[0] = -item[0]
        # Using heap algorighem
        if len(self.data) < self.k:
            heapq.heappush(self.data, item)
        else:
            topk_small = self.data[0]
            if item[0] > topk_small[0]:
                heapq.heapreplace(self.data, item)

    def btmk(self):
        sort_list = []
        for item in self.data:
            sort_list.append([-item[0], item[1]])
        return sorted(sort_list, cmp=lambda x, y: cmp(x[0], y[0]))


if __name__ == "__main__":
    list_rand = random.sample(xrange(1000000), 100)
    th = TopMaxHeap(10)
    for i in list_rand:
        th.push([i, 'fasd'])
    print th.topk()
    print sorted(list_rand, reverse=True)[0:10]

    list_rand = random.sample(xrange(1000000), 100)
    th = TopMinHeap(10)
    for i in list_rand:
        th.push([i, 'fasd'])
    print th.btmk()
    print sorted(list_rand)[0:10]
