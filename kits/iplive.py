# -*- coding: utf-8 -*-
""" Aiming at using received node callback. Determine current ip status.
    1 means website is working with http statuses they want.
    2 means connection error when node tries to connect to target.
    3 means tiemout when node tries to connect to target.
    1xx-5xx means http code error after node successfully connect to target

    return this to caller
"""

from config.conf import conf
from config.conf import level_strategy
from kits.ding import send_ding_msg
from kits.data_dictionary import NOT_SYNC_TO_NODE

def iplive(values, level, _ip):

    if level is 4:

        sql = "SELECT COUNT(*) as count FROM nodes"
        count = conf['mysql'].select(sql, [], one=True)
        strategy = {
            'total': count['count'],
            'as_down': count['count']
        }
    else:
        strategy = level_strategy[str(level)]

    if len(values) is not strategy['total']:
        msg = ("Node number error, ip:%s get:%s, total:%s, level:%s" %
               (_ip, len(values), strategy['total'], level))
        conf['logger'].error(msg)
        send_ding_msg("收到结果的检测节点的数量和默认不匹配: " + msg)

        if not values:
            return (NOT_SYNC_TO_NODE, 0)

    if len(values) is 0:
        return 2, 0

    reason = None
    down_count = 0
    res_times = []
    for value in values:
        res_time, last_status = value.decode('utf-8').split(":")
        res_times.append(int(res_time))
        if int(last_status) is not 1:
            reason = last_status
            down_count += 1

    res_time = sum(res_times) / len(res_times)

    as_down = strategy['as_down'] - (strategy['total'] - len(values))
    if as_down is 0:
        return (0, res_time) if reason is None else (reason, res_time)

    return (0, res_time) if (reason is None or down_count < as_down) else (reason, res_time)
