#!/usr/bin/env python
# encoding: utf-8
"""
@author: youfeng
@email: youfeng243@163.com
@license: Apache Licence
@file: config.py.py
@time: 2017/7/25 15:38
"""
# 最大需要检查统计的数据量
MAX_CHECK_NUM = 30000000

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

# 检查的表名称
COLLECTION_NAME = 'judgement_wenshu'

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


field_dict = {
    # '_record_id': {
    #     # 32位定长
    #     CHECK: {
    #         Check.LENGTH: {
    #             Check.Compare.EQUAL: 32
    #         },
    #         Check.TYPE: basestring,
    #     }
    # },
    # '_in_time': {
    #     # 时间格式 yyyy-MM-DD HH:mm:ss
    #     CHECK: {
    #         Check.TYPE: basestring,
    #     },
    #
    #     # 统计大小
    #     STATISTICS: Statistics.VALUE,
    #     # 'CHECK': {
    #     #     'format': ''
    #     # }
    # },
    # '_utime': {
    #     # 时间格式 yyyy-MM-DD HH:mm:ss
    #     CHECK: {
    #         Check.TYPE: basestring,
    #     },
    #     STATISTICS: Statistics.VALUE,
    # },
    'all_money': {
        # double类型 判断数值类型是否正确 不能为负数 最大值统计  topN 统计
        CHECK: {
            Check.VALUE: {
                Check.Compare.GREATERTHAN: 0
            },
            Check.TYPE: float,
        },
        STATISTICS: Statistics.VALUE,
    },
    'bulletin_date': {
        # 时间格式 yyyy-MM-DD HH:mm:ss
        CHECK: {
            Check.TYPE: basestring,
        },
        STATISTICS: Statistics.VALUE,
    },
    'case_cause': {
        # 普通文本内容 允许为空 长度无限制 topN 统计
        CHECK: {
            Check.TYPE: basestring,
        },
        STATISTICS: Statistics.LENGTH,
    },
    'case_date': {
        # 时间格式 yyyy-MM-DD 固定格式，如果不符合规格则判定为错误 topN 统计
        CHECK: {
            Check.TYPE: basestring,
            Check.LENGTH: {
                Check.Compare.LESSTHAN: 12,
            },
        },
        STATISTICS: Statistics.VALUE,
    },
    'case_id': {
        # 普通文本，长度小于100字符 长度topN统计

        CHECK: {
            Check.LENGTH: {
                Check.Compare.LESSTHAN: 100
            },
            Check.TYPE: basestring,
        },
        STATISTICS: Statistics.LENGTH,
    },
    'case_name': {
        # 普通文本, 标题  长度topN 统计
        CHECK: {
            Check.TYPE: basestring,
        },
        STATISTICS: Statistics.LENGTH,
    },
    'case_type': {
        # 枚举类型
        CHECK: {
            Check.TYPE: basestring,
        },
        STATISTICS: Statistics.FREQUENCY,
    },
    'chain_case_id': {
        # 数组 且item为字符串
        CHECK: {
            Check.TYPE: list,
            Check.ITEM: {
                Check.TYPE: basestring,
            }
        },
    },
    'company_list': {
        # 暂时没有发现item数据
        CHECK: {
            Check.TYPE: list,
        },

    },
    'court': {
        # 法院名称，普通字符串 长度topN统计

        CHECK: {
            Check.LENGTH: {
                Check.Compare.LESSTHAN: 100
            },
            Check.TYPE: basestring,
        },
        STATISTICS: Statistics.LENGTH,
    },
    'defendant_list': {
        # 数组 且item为字符串
        CHECK: {
            Check.TYPE: list,
            Check.ITEM: {
                Check.TYPE: basestring,
            }
        },

    },
    'doc_content': {
        # 文书  普通文本 长度统计
        CHECK: {
            Check.TYPE: basestring,
        },
        STATISTICS: Statistics.LENGTH,
    },
    'doc_id': {
        # 编号， 普通文本 长度统计

        CHECK: {
            Check.LENGTH: {
                Check.Compare.LESSTHAN: 1000
            },
            Check.TYPE: basestring,
        },
        STATISTICS: Statistics.LENGTH,
    },
    'judge_content': {
        # 普通文本 长度统计
        CHECK: {
            Check.TYPE: basestring,
        },
        STATISTICS: Statistics.LENGTH,
    },
    'judiciary_list': {
        CHECK: {
            Check.TYPE: list,
            Check.ITEM: {
                Check.TYPE: basestring,
            }
        },

    },
    'litigant_list': {
        CHECK: {
            Check.TYPE: list,
            Check.ITEM: {
                Check.TYPE: basestring,
            }
        },
    },
    'litigants': {
        CHECK: {
            Check.TYPE: basestring,
            Check.LENGTH: {
                Check.Compare.LESSTHAN: 100
            }
        },
        STATISTICS: Statistics.LENGTH,
    },
    'max_money': {
        # double类型 判断数值类型是否正确 不能为负数 最大值统计  topN 统计
        CHECK: {
            Check.TYPE: float,
            Check.VALUE: {
                Check.Compare.GREATERTHAN: 0
            }
        },
        STATISTICS: Statistics.VALUE,
    },
    'plaintiff_list': {
        CHECK: {
            Check.TYPE: list,
            Check.ITEM: {
                Check.TYPE: basestring,
            }
        },

    },
    'procedure': {
        # 枚举类型
        CHECK: {
            Check.TYPE: basestring,
        },
        STATISTICS: Statistics.FREQUENCY,
    },
    'province': {
        # 枚举类型
        CHECK: {
            Check.TYPE: basestring,
        },
        STATISTICS: Statistics.FREQUENCY,
    },
    'ref_ids': {
        # 数组 且item为字符串
        CHECK: {
            Check.TYPE: list,
            Check.ITEM: {
                Check.TYPE: basestring,
            }
        },

    },
    'litigant_info_list': {
        # 常规数组
        CHECK: {
            Check.TYPE: list,
        },
    }
}
