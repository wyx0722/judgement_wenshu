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

from config import app_data_source, DOCUMENT_NAME
from logger import Logger
from mongo import MongDb

log = Logger('judgement_wenshu.log').get_logger()

app_data_db = MongDb(app_data_source['host'], app_data_source['port'], app_data_source['db'],
                     app_data_source['username'], app_data_source['password'], log=log)

# 工程根路径
project_path = os.path.dirname(os.path.realpath(__file__))


# 执行程序
def process():
    for item in app_data_db.traverse_batch(DOCUMENT_NAME):
        pass


def main():
    log.info("启动 judgement_wenshu 数据分析程序.. ")

    process()

    log.info("结束 judgement_wenshu 数据分析程序.. ")


if __name__ == '__main__':
    main()
