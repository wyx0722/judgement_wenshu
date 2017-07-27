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
    'status': {
        # 时间格式 yyyy-MM-DD HH:mm:ss
        rules.CHECK: {
            rules.Check.TYPE: basestring,
        },
        rules.STATISTICS: rules.Statistics.FREQUENCY,
    },
    'province': {
        # 普通文本内容 允许为空 长度无限制 topN 统计
        rules.CHECK: {
            rules.Check.TYPE: basestring,
        },
        rules.STATISTICS: rules.Statistics.FREQUENCY,
    },
    'court': {
        # 时间格式 yyyy-MM-DD 固定格式，如果不符合规格则判定为错误 topN 统计
        rules.CHECK: {
            rules.Check.TYPE: basestring,
        },
        rules.STATISTICS: rules.Statistics.FREQUENCY,
    },
    'litigants': {
        rules.CHECK: {
            rules.Check.TYPE: basestring,
        },
        rules.STATISTICS: rules.Statistics.LENGTH,
    },
    'filing_date': {
        # 普通文本, 标题  长度topN 统计
        rules.CHECK: {
            rules.Check.TYPE: basestring,
        },
        rules.STATISTICS: rules.Statistics.LENGTH,
    },
    'case_id': {
        # 枚举类型
        rules.CHECK: {
            rules.Check.LENGTH: {
                rules.Check.Compare.LESSTHAN: 100
            },
            rules.Check.TYPE: basestring,
        },
        rules.STATISTICS: rules.Statistics.LENGTH,
    },
    'close_date': {
        # 数组 且item为字符串
        rules.CHECK: {
            rules.Check.LENGTH: {
                rules.Check.Compare.LESSTHAN: 50
            },
            rules.Check.TYPE: basestring,
        },
        rules.STATISTICS: rules.Statistics.LENGTH,
    },
    'judge': {
        # 暂时没有发现item数据
        rules.CHECK: {
            rules.Check.LENGTH: {
                rules.Check.Compare.LESSTHAN: 20
            },
            rules.Check.TYPE: basestring,
        },
        rules.STATISTICS: rules.Statistics.LENGTH,
    },
    'filing_people': {
        rules.CHECK: {
            rules.Check.LENGTH: {
                rules.Check.Compare.LESSTHAN: 20
            },
            rules.Check.TYPE: basestring,
        },
        rules.STATISTICS: rules.Statistics.LENGTH,
    },
    'original_collection': {
        rules.CHECK: {
            rules.Check.LENGTH: {
                rules.Check.Compare.LESSTHAN: 50
            },
            rules.Check.TYPE: basestring,
        },
        rules.STATISTICS: rules.Statistics.LENGTH,
    },
    'court_time': {
        rules.CHECK: {
            rules.Check.LENGTH: {
                rules.Check.Compare.LESSTHAN: 20
            },
            rules.Check.TYPE: basestring,
        },
        rules.STATISTICS: rules.Statistics.LENGTH,
    },
    'html': {
        rules.CHECK: {
            rules.Check.TYPE: basestring,
        },
    },
    'court_place': {
        # 普通文本 长度统计
        rules.CHECK: {
            rules.Check.TYPE: basestring,
        },
        rules.STATISTICS: rules.Statistics.LENGTH,
    },
    'plaintiff_list': {
        rules.CHECK: {
            rules.Check.TYPE: list,
            rules.Check.ITEM: {
                rules.Check.TYPE: basestring,
            }
        },

    },
    'defendant_list': {
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
    'case_cause': {
        # 普通文本 长度统计
        rules.CHECK: {
            rules.Check.TYPE: basestring,
        },
        rules.STATISTICS: rules.Statistics.LENGTH,

    },
    'procedure': {
        # 枚举类型
        rules.CHECK: {
            rules.Check.TYPE: basestring,
        },
        rules.STATISTICS: rules.Statistics.FREQUENCY,
    },
    'department': {
        # 枚举类型
        rules.CHECK: {
            rules.Check.TYPE: basestring,
        },
        rules.STATISTICS: rules.Statistics.LENGTH,
    },
    'clerk': {
        # 枚举类型
        rules.CHECK: {
            rules.Check.TYPE: basestring,
        },
        rules.STATISTICS: rules.Statistics.LENGTH,

    }
}
