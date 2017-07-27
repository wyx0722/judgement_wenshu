#!/usr/bin/env python
# encoding: utf-8
"""
@author: youfeng
@email: youfeng243@163.com
@license: Apache Licence
@file: main.py
@time: 2017/7/25 20:47
"""
import os
import time

import config
import rules
from logger import Logger
from mongo import MongDb
from topN import TopMaxHeap

log = Logger('data_analyse.log').get_logger()


class ProcessWorker(object):
    # 最大需要检查统计的数据量
    MAX_CHECK_NUM = 80000000

    # top数目
    TOP_NUM = 1000

    # 数据库连接信息
    app_data_source = {
        "host": "172.16.215.16",
        "port": 40042,
        "db": "app_data",
        "username": "read",
        "password": "read",
    }

    # 属性未找到定义
    NOT_FOUND = 'not_found'

    # 工程根路径
    project_path = os.path.dirname(os.path.realpath(__file__))

    def __init__(self, log):

        # 日志
        self.log = log

        # 数据库访问
        self.app_data_db = MongDb(self.app_data_source['host'], self.app_data_source['port'],
                                  self.app_data_source['db'], self.app_data_source['username'],
                                  self.app_data_source['password'], log=log)
        # 文件句柄
        self.file_handle = {}

        # 最大堆
        self.max_heap_manage = {}

        # 最小堆
        # self.min_heap_manage = {}

        # 频率管理
        self.hz_manage = {}

        # 获取启动时间 用于计算还需要多少时间完成扫描
        self.start_time = time.time()
        self.log.info("当前启动时间: start_time = {}".format(self.start_time))

        # 当前分析到的位置
        self.current_num = 0

        # 获取当前要统计的数据个数
        self.total_num = self.app_data_db.db[config.COLLECTION_NAME].count()
        if self.total_num > self.MAX_CHECK_NUM:
            self.total_num = self.MAX_CHECK_NUM

        self.log.info("当前需要统计的数据总数目为: {}".format(self.total_num))

    def __call__(self, *args, **kwargs):
        self.log.info("启动 judgement_wenshu 数据分析程序.. ")

        # 目录信息初始化
        self.init_folder()

        # 处理过程
        self.start_process()

        # 关闭文件信息
        self.close()

        self.log.info("结束 judgement_wenshu 数据分析程序.. ")

    # 计算预计需要多长时间完成..
    def __predict_use_time(self):
        end_time = time.time()

        use_time = end_time - self.start_time

        if use_time <= 0:
            return

        total_time = int(self.total_num * use_time / self.current_num)
        self.log.info('已耗费时间: {}s'.format(int(use_time)))
        self.log.info('预计还需要耗时: {}s'.format(total_time - int(use_time)))

    # 详细比较
    def detail_compare(self, _id, item_field, check_config, field_value, config_field):
        # 是否需要对数值进行检测

        compare_info = check_config.get(config_field)
        if not isinstance(compare_info, dict):
            raise Exception('属性比较配置信息错误: _id = {} field = {} check_config = {}'.format(
                _id, item_field, check_config))

        while True:
            # 如果是判等，但是数值不相等 则记录下来
            if rules.Check.Compare.EQUAL in compare_info:
                judge_value = compare_info.get(rules.Check.Compare.EQUAL)
                if field_value != judge_value:
                    self.file_handle[item_field][rules.CHECK][config_field].write(
                        '{} {} not equal {}\r\n'.format(_id, field_value, judge_value))
                break

            # 如果是判断大于等于
            if rules.Check.Compare.GREATERTHAN in compare_info:
                judge_value = compare_info.get(rules.Check.Compare.GREATERTHAN)
                if field_value < judge_value:
                    self.file_handle[item_field][rules.CHECK][config_field].write(
                        '{} {} less than {}\r\n'.format(_id, field_value, judge_value))
                break

            # 如果是小于等于
            if rules.Check.Compare.LESSTHAN in compare_info:
                judge_value = compare_info.get(rules.Check.Compare.LESSTHAN)
                if field_value > judge_value:
                    self.file_handle[item_field][rules.CHECK][config_field].write(
                        '{} {} great than {}\r\n'.format(_id, field_value, judge_value))
                break
            break

    # 检测 数据是否正确
    def __process_check(self, _id, item_field, check_config, field_value):
        # 判断是否有数据类型判断
        if rules.Check.TYPE in check_config:
            # 如果数据类型不正确则记录下来
            check_type = check_config.get(rules.Check.TYPE)
            if not isinstance(field_value, check_type):
                self.file_handle[item_field][rules.CHECK][rules.Check.TYPE].write('{} type not {}\r\n'.format(
                    _id, check_type))
                # 如果类型都不正确则不需要进一步检查
                return

        # 是否需要对数值进行检测
        if rules.Check.VALUE in check_config:
            self.detail_compare(_id, item_field, check_config, field_value, rules.Check.VALUE)

        # 是否需要对长度进行检测
        if rules.Check.LENGTH in check_config:
            self.detail_compare(_id, item_field, check_config, len(field_value), rules.Check.LENGTH)

            # todo 是否需要对数组中的属性进行检测
            # if rules.Check.ITEM in check_config:
            #     pass

    # 统计 数据topN
    def __process_statistics(self, _id, item_field, statistics_config, field_value):

        # 统计频率
        if statistics_config == rules.Statistics.FREQUENCY:
            if field_value not in self.hz_manage[item_field]:
                self.hz_manage[item_field][field_value] = 1
            else:
                self.hz_manage[item_field][field_value] += 1
            return

        # 统计长度
        if statistics_config == rules.Statistics.LENGTH:
            self.max_heap_manage[item_field].push([len(field_value), _id])
            # self.min_heap_manage[item_field].push([len(field_value), _id])
            return

        # 统计数值
        if statistics_config == rules.Statistics.VALUE:
            self.max_heap_manage[item_field].push([field_value, _id])
            # self.min_heap_manage[item_field].push([field_value, _id])
            return

    # 处理每一个document
    def __process_item(self, item):
        _id = item.get('_id')
        if _id is None:
            self.log.error('当前item没有_id属性: {}'.format(item))
            return
        _id = _id.__str__()
        for field, value in config.field_dict.iteritems():
            # 如果需要检测的字段没有在document
            if field not in item:
                # 把企业信息记录在not_found 中
                self.file_handle[field][self.NOT_FOUND].write(_id + '\r\n')
                continue

            field_value = item.get(field)

            # 判断是否由检测属性
            check = value.get(rules.CHECK)
            if check is not None:
                self.__process_check(_id, field, check, field_value)

            # 判断是否由统计属性
            statistics = value.get(rules.STATISTICS)
            if statistics is not None:
                self.__process_statistics(_id, field, statistics, field_value)

    # 输出频率结果
    def hz_result(self, field_name, statistics):
        sort_list = sorted(self.hz_manage[field_name].iteritems(), key=lambda a: a[1])
        self.file_handle[field_name][statistics].write('数据频率统计: \r\n')
        for item in sort_list:
            self.file_handle[field_name][statistics].write('{} {}\r\n'.format(item[0], item[1]))

    # 输出最大统计结果
    def max_heap_result(self, field_name, statistics, _type):
        sort_list = self.max_heap_manage[field_name].topk()
        if _type == rules.Statistics.LENGTH:
            self.file_handle[field_name][statistics].write('最大长度排序: \r\n')
        if _type == rules.Statistics.VALUE:
            self.file_handle[field_name][statistics].write('最大值排序: \r\n')
        for item in sort_list:
            self.file_handle[field_name][statistics].write('{} {}\r\n'.format(item[0], item[1]))

    # 输出统计结果
    def statistics_result(self):
        self.log.info('开始输出统计结果: ')
        for field_name, config_info in config.field_dict.iteritems():

            # 遍历属性
            for key, value in config_info.iteritems():
                if isinstance(value, dict):
                    continue

                if value == rules.Statistics.FREQUENCY:
                    self.hz_result(field_name, key)
                    continue

                # 统计值
                self.max_heap_result(field_name, key, value)
                # self.max_heap_manage[field_name] = TopMaxHeap(rules.TOP_NUM)
                # self.min_heap_manage[field_name] = TopMinHeap(rules.TOP_NUM)
        self.log.info('输出统计结果完成...')

    # 执行程序
    def start_process(self):
        self.log.info("进入数据处理流程...")
        for item in self.app_data_db.traverse_batch(config.COLLECTION_NAME):
            self.current_num += 1

            # 处理每个document
            self.__process_item(item)

            if self.current_num % 10000 == 0:
                self.__predict_use_time()

            # 如果达到最大需要统计的数目 则退出
            if self.current_num >= self.total_num:
                break

        # 输出统计信息
        self.statistics_result()

    # 初始化
    def init_folder(self):

        self.log.info('初始化文件夹以及文件句柄...')

        result_path = self.project_path + "/" + config.COLLECTION_NAME
        # 创建结果目录
        if not os.path.exists(result_path):
            os.makedirs(result_path)

        for field_name, config_info in config.field_dict.iteritems():
            field_path = result_path + "/" + field_name
            if not os.path.exists(field_path):
                os.makedirs(field_path)

            if not isinstance(config_info, dict):
                self.log.error("配置信息错误: key = {} value 信息不是字典".format(field_name))
                raise Exception('终止检测...')

            self.file_handle[field_name] = {}

            # 没有找到属性记录文件..
            self.file_handle[field_name][self.NOT_FOUND] = open(field_path + "/" + self.NOT_FOUND + '.txt', 'w')

            # 遍历属性
            for key, value in config_info.iteritems():
                if isinstance(value, dict):
                    path = field_path + "/" + key
                    if not os.path.exists(path):
                        os.makedirs(path)

                    self.file_handle[field_name][key] = {}
                    for key1, value1 in value.iteritems():
                        self.file_handle[field_name][key][key1] = open(path + "/" + key1 + '.txt', 'w')

                    continue

                if key != rules.STATISTICS:
                    raise Exception('新加属性无法识别: key = {}'.format(key))

                self.file_handle[field_name][key] = open(field_path + "/" + key + '.txt', 'w')
                if value == rules.Statistics.FREQUENCY:
                    self.hz_manage[field_name] = {}
                    continue

                # 统计值
                self.max_heap_manage[field_name] = TopMaxHeap(self.TOP_NUM)
                # self.min_heap_manage[field_name] = TopMinHeap(config.TOP_NUM)

    # 关闭文件句柄
    def close(self):
        self.log.info('开始关闭文件句柄...')

        def close_handle(file_handle):
            if not isinstance(file_handle, dict):
                return

            for key, value in file_handle.iteritems():
                if isinstance(value, dict):
                    close_handle(value)
                    continue
                if isinstance(value, file):
                    value.close()
                    continue
                log.error("关闭文件异常未知类型: type = {}".format(type(value)))

        close_handle(self.file_handle)
        self.log.info('关闭文件句柄完成...')


def main():
    try:
        worker = ProcessWorker(log)
        worker()
    except Exception as e:
        log.error("异常退出...")
        log.exception(e)


if __name__ == '__main__':
    main()
