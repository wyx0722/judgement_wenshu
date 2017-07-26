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
from config import app_data_source, field_dict, COLLECTION_NAME
from logger import Logger
from mongo import MongDb

log = Logger('judgement_wenshu.log').get_logger()


class ProcessWorker(object):
    # 属性未找到定义
    NOT_FOUND = 'not_found'

    # 工程根路径
    project_path = os.path.dirname(os.path.realpath(__file__))

    # 结果目录
    RESULT_FOLDER = 'result'

    def __init__(self, log):

        # 日志
        self.log = log

        # 数据库访问
        self.app_data_db = MongDb(app_data_source['host'], app_data_source['port'], app_data_source['db'],
                                  app_data_source['username'], app_data_source['password'], log=log)
        # 文件句柄
        self.file_handle = {}

        # 获取启动时间 用于计算还需要多少时间完成扫描
        self.start_time = time.time()
        self.log.info("当前启动时间: start_time = {}".format(self.start_time))

        # 当前分析到的位置
        self.current_num = 0
        # 获取当前要统计的数据个数
        self.total_num = self.app_data_db.db[COLLECTION_NAME].count()
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
            if config.Check.Compare.EQUAL in compare_info:
                judge_value = compare_info.get(config.Check.Compare.EQUAL)
                if field_value != judge_value:
                    self.file_handle[item_field][config.CHECK][config_field].write(
                        '{} {} not equal {}\r\n'.format(_id, field_value, judge_value))
                break

            # 如果是判断大于等于
            if config.Check.Compare.GREATERTHAN in compare_info:
                judge_value = compare_info.get(config.Check.Compare.GREATERTHAN)
                if field_value < judge_value:
                    self.file_handle[item_field][config.CHECK][config_field].write(
                        '{} {} less than {}\r\n'.format(_id, field_value, judge_value))
                break

            # 如果是小于等于
            if config.Check.Compare.LESSTHAN in compare_info:
                judge_value = compare_info.get(config.Check.Compare.LESSTHAN)
                if field_value > judge_value:
                    self.file_handle[item_field][config.CHECK][config_field].write(
                        '{} {} great than {}\r\n'.format(_id, field_value, judge_value))
                break
            break

    # 检测 数据是否正确
    def __process_check(self, _id, item_field, check_config, field_value):
        # 判断是否有数据类型判断
        if config.Check.TYPE in check_config:
            # 如果数据类型不正确则记录下来
            check_type = check_config.get(config.Check.TYPE)
            if not isinstance(field_value, check_type):
                self.file_handle[item_field][config.CHECK][config.Check.TYPE].write('{} type not {}\r\n'.format(
                    _id, check_type))
                # 如果类型都不正确则不需要进一步检查
                return

        # 是否需要对数值进行检测
        if config.Check.VALUE in check_config:
            self.detail_compare(_id, item_field, check_config, field_value, config.Check.VALUE)

        # 是否需要对长度进行检测
        if config.Check.LENGTH in check_config:
            self.detail_compare(_id, item_field, check_config, len(field_value), config.Check.LENGTH)

            # todo 是否需要对数组中的属性进行检测
            # if config.Check.ITEM in check_config:
            #     pass

    # 统计 数据topN
    def __process_statistics(self, _id, item_field, statistics_config, field_value):
        pass

    # 处理每一个document
    def __process_item(self, item):
        _id = item.get('_id')
        if _id is None:
            self.log.error('当前item没有_id属性: {}'.format(item))
            return
        _id = _id.__str__()
        for field, value in field_dict.iteritems():
            # 如果需要检测的字段没有在document
            if field not in item:
                # 把企业信息记录在not_found 中
                self.file_handle[field][self.NOT_FOUND].write(_id + '\r\n')
                continue

            field_value = item.get(field)

            # 判断是否由检测属性
            check = value.get(config.CHECK)
            if check is not None:
                self.__process_check(_id, field, check, field_value)

            # 判断是否由统计属性
            statistics = value.get(config.STATISTICS)
            if statistics is not None:
                self.__process_statistics(_id, field, statistics, field_value)

    # 执行程序
    def start_process(self):
        self.log.info("进入数据处理流程...")
        for item in self.app_data_db.traverse_batch(COLLECTION_NAME):
            self.current_num += 1

            # 处理每个document
            self.__process_item(item)

            if self.current_num % 10000 == 0:
                self.__predict_use_time()

    # 初始化
    def init_folder(self):

        self.log.info('初始化文件夹以及文件句柄...')

        result_path = self.project_path + "/" + self.RESULT_FOLDER
        # 创建结果目录
        if not os.path.exists(result_path):
            os.makedirs(result_path)

        for field_name, config_info in field_dict.iteritems():
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

                self.file_handle[field_name][key] = open(field_path + "/" + key + '.txt', 'w')

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
