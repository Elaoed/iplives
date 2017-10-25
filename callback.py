# -*- coding: utf-8 -*-
"""Scheduled scan mysql. Send finished group information to php"""

import gevent

from config.conf import conf
from kits.iplive import iplive
from kits.utils import get_groups
from kits.ding import send_ding_msg
from kits.utils import get_sleep_time
from kits.utils import get_records
from kits.utils import get_all_nodes
from kits.data_dictionary import NOT_SYNC_TO_NODE

def vice_callback(_ts):

    groups = get_groups(_ts)
    ret_obj = dict()
    all_node_down_ips = []
    redis_key = "iplive_cache:%d" % _ts

    for group in groups:

        group_id = str(group['group_id'])
        app_name = group['app_name']
        records = get_records(group_id, app_name)
        ret_obj[group_id] = {}
        if group['level'] is 4:
            node_ips = get_all_nodes()
        else:
            node_ips = group["node_ips"].split(":")

        for record in records:
            _ip = record['ip']
            server_id = record['server_id']
            values = []

            for node_ip in node_ips:
                name = ":".join([node_ip, str(server_id)])
                value = conf['redis'].hget(redis_key, name)
                if value:
                    values.append(value)

            ip_status, res_time = iplive(values, group['level'], _ip)
            if ip_status is NOT_SYNC_TO_NODE:
                continue

            sql = "UPDATE records SET last_status = %s, res_time = %s WHERE server_id = %s"
            conf['mysql'].update(sql, [ip_status, res_time, server_id])

            ret_obj[str(group_id)][_ip] = {
                'status': ip_status,
                'res_time': res_time
            }

            if ip_status is not 0:
                all_node_down_ips.append(_ip)

    if all_node_down_ips:
        msg = "全部节点检测都宕机的 IP列表: [%s]" % ', '.join(all_node_down_ips)
        send_ding_msg(msg)
    print(ret_obj)

    # ==================== send this message back to php ========================


def callback_poller():

    # 把所有的node 存进redis 然后来一个结果拿出来比对接收到的数量是否已经达到要求
    # 致命缺陷就是 万一节点端超时或者少发了一个怎么办。 除非在服务端弄个定时器
    print("Starting callback poller to php .....")
    while True:
        sleep_time, _ts = get_sleep_time()
        gevent.sleep(sleep_time + 15)
        vice_callback(_ts)
