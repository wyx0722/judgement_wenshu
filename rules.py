#!/usr/bin/env python
# encoding: utf-8
"""
@author: youfeng
@email: youfeng243@163.com
@license: Apache Licence
@file: rules.py
@time: 2017/7/27 18:32
"""

# 检测
CHECK = 'check'


class Check(object):
    def __int__(self):
        pass

    # 文本长度
    LENGTH = 'length'

    class Compare(object):
        def __init__(self):
            pass

        # 相等
        EQUAL = 'equal'

        # 大于等于
        GREATERTHAN = 'greaterthan'

        # 小于等于
        LESSTHAN = 'lessthan'

    # 数据类型
    TYPE = 'type'
    # 数值大小
    VALUE = 'value'
    # 数组属性
    ITEM = 'item'


# 统计
STATISTICS = 'statistics'


class Statistics(object):
    def __init__(self):
        pass

    # 数值大小
    VALUE = 'value'

    # 文本长度
    LENGTH = 'length'

    # 出现频率
    FREQUENCY = 'frequency'
