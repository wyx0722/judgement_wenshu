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

from config import app_data_source, field_dict
from logger import Logger
from mongo import MongDb

log = Logger('judgement_wenshu.log').get_logger()


class ProcessWorker(object):
    # 工程根路径
    project_path = os.path.dirname(os.path.realpath(__file__))

    # 结果目录
    RESULT_FOLDER = 'result'

    def __init__(self):
        # 数据库访问
        self.app_data_db = MongDb(app_data_source['host'], app_data_source['port'], app_data_source['db'],
                                  app_data_source['username'], app_data_source['password'], log=log)
        # 文件句柄
        self.file_handle = {}

    def __call__(self, *args, **kwargs):
        log.info("启动 judgement_wenshu 数据分析程序.. ")

        # 目录信息初始化
        self.init_folder()

        # 处理过程
        self.process()

        # 关闭文件信息
        self.close()

        log.info("结束 judgement_wenshu 数据分析程序.. ")

    # 执行程序
    def process(self):
        pass
        # for item in app_data_db.traverse_batch(DOCUMENT_NAME):
        #     pass

    # 初始化
    def init_folder(self):
        result_path = self.project_path + "/" + self.RESULT_FOLDER
        # 创建结果目录
        if not os.path.exists(result_path):
            os.makedirs(result_path)

        for field_name, config_info in field_dict.iteritems():
            field_path = result_path + "/" + field_name
            if not os.path.exists(field_path):
                os.makedirs(field_path)

            if not isinstance(config_info, dict):
                log.error("配置信息错误: key = {} value 信息不是字典".format(field_name))
                raise Exception('终止检测...')

            # 遍历属性
            for key, value in config_info.iteritems():
                if isinstance(value, dict):
                    path = field_path + "/" + key
                    if not os.path.exists(path):
                        os.makedirs(path)

    # 关闭文件句柄
    def close(self):
        pass


def main():
    worker = ProcessWorker()
    worker()


if __name__ == '__main__':
    main()
