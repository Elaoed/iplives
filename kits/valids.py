# -*- coding: utf-8 -*-
"""Various valid functions for various situation."""

from config.conf import conf
from config.conf import port_mapping
from config.conf import level_strategy
from kits.custom_exception import CustomException

def newdun_dns_insert(params):

    group_id = params.get("group_id", type=int)
    app_name = params.get("app_name", type=str)
    record_ids = params.get("record_ids", type=str, default=None)
    ips = params.get("ips", type=str, default=None)

    if not group_id or not record_ids or not ips:
        raise CustomException("insert - lack of param", 1002)

    ips = ips.split(":")
    record_ids = record_ids.split(":")

    if len(ips) is not len(record_ids):
        raise CustomException("len(main_ips) is not equals to len(record_ids)", 1006)

    # 测试backup_ip和main_ip是否有重合 或者和其他的main_ip是否有重合
    # if len(set(ips) & set(ips)) > 0:
    #     raise CustomException("main_ips have intersection with backup_ips", )

    # 4是最高级别、 数据会下发到所有的节点探测
    level = params.get("level", type=int, default=4)
    if level < 0 or level > 4:
        raise CustomException("level not valid ", 1006)

    if level is 4:
        sql = "SELECT node_ip FROM nodes WHERE status = 0"
        res = conf['mysql'].select(sql, [], one=False)
        node_ips = "" if not res else ':'.join([x['node_ip'] for x in res])
    else:
        node_ips = params.get("node_ips", type=str, default="")
        given = len(node_ips.split(":"))
        defined = level_strategy[str(level)]['total']
        if given != defined:
            conf['logger'].warning("Length of node_ips is not corresponding. defined:%d, given:%d " % (defined, given))
            raise CustomException("Length of node_ips is not corresponding to your level", 1006)

    protocol = params.get("protocol", type=str, default="http")
    if protocol not in ["http", "https", "tcp", "udp"]:
        raise CustomException("protocol not valid ", 1006)

    port = params.get("port", port_mapping[protocol])

    dparams = {
        'group_id': group_id,
        'app_name': app_name,
        'record_ids': record_ids,
        'ips': ips,
        'level': level,
        'protocol': protocol,
        'port': port,
        'node_ips': node_ips,
        'timeout': params.get("tmeout", type=int, default=3),
        'retry_count': params.get("retry_count", type=int, default=0),
        'interval': params.get("interval", type=int, default=60),
        'path': params.get("path", type=str, default="/"),
        'domain': params.get("domain", type=str, default=""),
        'cookies': params.get("cookies", type=str, default=""),
        'http_code': params.get("http_code", type=str, default="")
    }

    return dparams

def newdun_dns_update(params):
    pass
