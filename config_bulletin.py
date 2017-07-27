#!/usr/bin/env python
# encoding: utf-8
"""
@author: youfeng
@email: youfeng243@163.com
@license: Apache Licence
@file: config.py.py
@time: 2017/7/25 15:38
"""
import rules

COLLECTION_NAME = 'bulletin'

field_dict = {
    'all_money': {
        # double类型 判断数值类型是否正确 不能为负数 最大值统计  topN 统计
        rules.CHECK: {
            rules.Check.VALUE: {
                rules.Check.Compare.GREATERTHAN: 0
            },
            rules.Check.TYPE: float,
        },
        rules.STATISTICS: rules.Statistics.VALUE,
    },
    'bulletin_date': {
        # 时间格式 yyyy-MM-DD HH:mm:ss
        rules.CHECK: {
            rules.Check.TYPE: basestring,
        },
        rules.STATISTICS: rules.Statistics.VALUE,
    },
    'case_cause': {
        # 普通文本内容 允许为空 长度无限制 topN 统计
        rules.CHECK: {
            rules.Check.TYPE: basestring,
        },
        rules.STATISTICS: rules.Statistics.LENGTH,
    },
    'case_date': {
        # 时间格式 yyyy-MM-DD 固定格式，如果不符合规格则判定为错误 topN 统计
        rules.CHECK: {
            rules.Check.TYPE: basestring,
            rules.Check.LENGTH: {
                rules.Check.Compare.LESSTHAN: 12,
            },
        },
        rules.STATISTICS: rules.Statistics.VALUE,
    },
    'case_id': {
        # 普通文本，长度小于100字符 长度topN统计

        rules.CHECK: {
            rules.Check.LENGTH: {
                rules.Check.Compare.LESSTHAN: 100
            },
            rules.Check.TYPE: basestring,
        },
        rules.STATISTICS: rules.Statistics.LENGTH,
    },
    'case_name': {
        # 普通文本, 标题  长度topN 统计
        rules.CHECK: {
            rules.Check.TYPE: basestring,
        },
        rules.STATISTICS: rules.Statistics.LENGTH,
    },
    'case_type': {
        # 枚举类型
        rules.CHECK: {
            rules.Check.TYPE: basestring,
        },
        rules.STATISTICS: rules.Statistics.FREQUENCY,
    },
    'chain_case_id': {
        # 数组 且item为字符串
        rules.CHECK: {
            rules.Check.TYPE: list,
            rules.Check.ITEM: {
                rules.Check.TYPE: basestring,
            }
        },
    },
    'company_list': {
        # 暂时没有发现item数据
        rules.CHECK: {
            rules.Check.TYPE: list,
        },

    },
    'court': {
        # 法院名称，普通字符串 长度topN统计

        rules.CHECK: {
            rules.Check.LENGTH: {
                rules.Check.Compare.LESSTHAN: 100
            },
            rules.Check.TYPE: basestring,
        },
        rules.STATISTICS: rules.Statistics.LENGTH,
    },
    'defendant_list': {
        # 数组 且item为字符串
        rules.CHECK: {
            rules.Check.TYPE: list,
            rules.Check.ITEM: {
                rules.Check.TYPE: basestring,
            }
        },

    },
    'doc_content': {
        # 文书  普通文本 长度统计
        rules.CHECK: {
            rules.Check.TYPE: basestring,
        },
        rules.STATISTICS: rules.Statistics.LENGTH,
    },
    'doc_id': {
        # 编号， 普通文本 长度统计

        rules.CHECK: {
            rules.Check.LENGTH: {
                rules.Check.Compare.LESSTHAN: 1000
            },
            rules.Check.TYPE: basestring,
        },
        rules.STATISTICS: rules.Statistics.LENGTH,
    },
    'judge_content': {
        # 普通文本 长度统计
        rules.CHECK: {
            rules.Check.TYPE: basestring,
        },
        rules.STATISTICS: rules.Statistics.LENGTH,
    },
    'judiciary_list': {
        rules.CHECK: {
            rules.Check.TYPE: list,
            rules.Check.ITEM: {
                rules.Check.TYPE: basestring,
            }
        },

    },
    'litigant_list': {
        rules.CHECK: {
            rules.Check.TYPE: list,
            rules.Check.ITEM: {
                rules.Check.TYPE: basestring,
            }
        },
    },
    'litigants': {
        rules.CHECK: {
            rules.Check.TYPE: basestring,
            rules.Check.LENGTH: {
                rules.Check.Compare.LESSTHAN: 100
            }
        },
        rules.STATISTICS: rules.Statistics.LENGTH,
    },
    'max_money': {
        # double类型 判断数值类型是否正确 不能为负数 最大值统计  topN 统计
        rules.CHECK: {
            rules.Check.TYPE: float,
            rules.Check.VALUE: {
                rules.Check.Compare.GREATERTHAN: 0
            }
        },
        rules.STATISTICS: rules.Statistics.VALUE,
    },
    'plaintiff_list': {
        rules.CHECK: {
            rules.Check.TYPE: list,
            rules.Check.ITEM: {
                rules.Check.TYPE: basestring,
            }
        },

    },
    'procedure': {
        # 枚举类型
        rules.CHECK: {
            rules.Check.TYPE: basestring,
        },
        rules.STATISTICS: rules.Statistics.FREQUENCY,
    },
    'province': {
        # 枚举类型
        rules.CHECK: {
            rules.Check.TYPE: basestring,
        },
        rules.STATISTICS: rules.Statistics.FREQUENCY,
    },
    'ref_ids': {
        # 数组 且item为字符串
        rules.CHECK: {
            rules.Check.TYPE: list,
            rules.Check.ITEM: {
                rules.Check.TYPE: basestring,
            }
        },

    },
    'litigant_info_list': {
        # 常规数组
        rules.CHECK: {
            rules.Check.TYPE: list,
        },
    }
}
