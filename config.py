#!/usr/bin/env python
# encoding: utf-8
"""
@author: youfeng
@email: youfeng243@163.com
@license: Apache Licence
@file: config.py.py
@time: 2017/7/25 15:38
"""

# top数目
TOP_NUM = 10

# 数据库连接信息
app_data_source = {
    "host": "172.16.215.16",
    "port": 40042,
    "db": "app_data",
    "username": "read",
    "password": "read",
}

# 检查的表名称
DOCUMENT_NAME = 'judgement_wenshu'

field_dict = {
    '_record_id': {
        # 32位定长
        'check': {
            'length': {
                'equal': 32
            },
            'type': str,
        }
    },
    '_in_time': {
        # 时间格式 yyyy-MM-DD HH:mm:ss
        'check': {
            'type': str,
        },

        # 统计大小
        'statistics': 'value',
        # 'check': {
        #     'format': ''
        # }
    },
    '_utime': {
        # 时间格式 yyyy-MM-DD HH:mm:ss
        'check': {
            'type': str,
        },
        'statistics': 'value',
    },
    'all_money': {
        # double类型 判断数值类型是否正确 不能为负数 最大值统计  topN 统计
        'check': {
            'value': {
                'greaterthan': 0
            },
            'type': float,
        },
        'statistics': 'value',
    },
    'bulletin_date': {
        # 时间格式 yyyy-MM-DD HH:mm:ss
        'check': {
            'type': str,
        },
        'statistics': 'value',
    },
    'case_cause': {
        # 普通文本内容 允许为空 长度无限制 topN 统计
        'check': {
            'type': str,
        },
        'statistics': 'length',
    },
    'case_date': {
        # 时间格式 yyyy-MM-DD 固定格式，如果不符合规格则判定为错误 topN 统计
        'check': {
            'type': str,
        },
        'statistics': 'value',
    },
    'case_id': {
        # 普通文本，长度小于100字符 长度topN统计

        'check': {
            'length': {
                'lessthan': 100
            },
            'type': str,
        },
        'statistics': 'length',
    },
    'case_name': {
        # 普通文本, 标题  长度topN 统计
        'check': {
            'type': str,
        },
        'statistics': 'length',
    },
    'case_type': {
        # 枚举类型
        'check': {
            'type': str,
        },
        'statistics': 'frequency',
    },
    'chain_case_id': {
        # 数组 且item为字符串
        'check': {
            'type': list,
            'item': {
                'type': str,
            }
        },
    },
    'company_list': {
        # 暂时没有发现item数据
        'check': {
            'type': list,
        },

    },
    'court': {
        # 法院名称，普通字符串 长度topN统计

        'check': {
            'length': {
                'lessthan': 100
            },
            'type': str,
        },
        'statistics': 'length',
    },
    'defendant_list': {
        # 数组 且item为字符串
        'check': {
            'type': list,
            'item': {
                'type': str,
            }
        },

    },
    'doc_content': {
        # 文书  普通文本 长度统计
        'check': {
            'type': str,
        },
        'statistics': 'length',
    },
    'doc_id': {
        # 编号， 普通文本 长度统计

        'check': {
            'length': {
                'lessthan': 100
            },
            'type': str,
        },
        'statistics': 'length',
    },
    'judge_content': {
        # 普通文本 长度统计
        'check': {
            'type': str,
        },
        'statistics': 'length',
    },
    'judiciary_list': {
        'check': {
            'type': list,
            'item': {
                'type': str,
            }
        },

    },
    'litigant_list': {
        'check': {
            'type': list,
            'item': {
                'type': str,
            }
        },

    },
    'litigants': {

        'check': {
            'type': str,
            'length': {
                'lessthan': 100
            }
        },
        'statistics': 'length',
    },
    'max_money': {
        # double类型 判断数值类型是否正确 不能为负数 最大值统计  topN 统计
        'check': {
            'type': float,
            'value': {
                'greaterthan': 0
            }
        },
        'statistics': 'value',
    },
    'plaintiff_list': {
        'check': {
            'type': list,
            'item': {
                'type': str,
            }
        },

    },
    'procedure': {
        # 枚举类型
        'check': {
            'type': str,
        },
        'statistics': 'frequency',
    },
    'province': {
        # 枚举类型
        'check': {
            'type': str,
        },
        'statistics': 'frequency',
    },
    'ref_ids': {
        # 数组 且item为字符串
        'check': {
            'type': list,
            'item': {
                'type': str,
            }
        },

    },
    'litigant_info_list': {
        # 常规数组
        'check': {
            'type': list,
        },
    }
}
