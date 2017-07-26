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

from config import app_data_source, field_dict, COLLECTION_NAME
from logger import Logger
from mongo import MongDb

log = Logger('judgement_wenshu.log').get_logger()


class ProcessWorker(object):
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
        self.start_time = int(time.time())
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
        self.process()

        # 关闭文件信息
        self.close()

        self.log.info("结束 judgement_wenshu 数据分析程序.. ")

    # 执行程序
    def process(self):
        self.log.info("进入数据处理流程...")
        pass
        # for item in app_data_db.traverse_batch(DOCUMENT_NAME):
        #     pass

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
    worker = ProcessWorker(log)
    worker()


if __name__ == '__main__':
    main()
