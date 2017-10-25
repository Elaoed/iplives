# -*- coding: utf-8 -*-
"""Utility functions"""

import time
import requests
from requests import Session
from requests import Request

from config.conf import conf

def compose_url(protocol, _ip, port, uri):

    url = ''.join([protocol, "://", _ip, ":", str(port), uri])
    return url

def get_nodes(task_id):

    sql = """select node_ips
             from vip_node_setting
             where id = (select vip_level
                         from records
                         where id = %s);
          """ % task_id
    nodes = conf['mysql'].select(sql, one=True)['node_ips']
    nodes = nodes.split(":")
    return nodes

def get_times(timestamp=None):

    if timestamp is None:
        timestamp = int(time.time())

    return time.strftime('%Y-%m-%d %X', time.localtime(timestamp))

def self_requests(method, url, logger=None, **kwargs):

    ret_value = -1
    try:
        session = Session()
        if method == "POST":
            data = session.pop("data")
            data = data if data else {}
        elif method == "GET":
            pass

        req = Request(method, url, **kwargs)
        prepped = req.prepare()

        res = session.send(prepped)
        return res.status_code
    except requests.exceptions.ConnectTimeout:
        pass
    except requests.exceptions.ReadTimeout:
        ret_value = 2
    except requests.exceptions.ConnectionError:
        ret_value = 1
    except requests.exceptions.Timeout:
        ret_value = 2
    except Exception:
        ret_value = -1

    return ret_value

def get_sleep_time():
    """get sleep time to next minutes"""
    now = int(time.time())
    next_ts = now - now % 60 + 60
    sleep_time = 60 - now % 60
    return sleep_time, next_ts

# def write_user_log(params):
#     sql = """insert into user_log set
#           task_id = %s,
#           user_id = %s,
#           trouble_reason = '%s',
#           start_time = '%s',
#           switch_to_backup = '%s'
#       """ % (params['task_id'],
#              params['user_id'],
#              REDIS.hget("up_to_email:" + params['task_id'], 'reason'),
#              get_time(int(params['timestamp'])),
#              params['switch_result'])
#     exec_iu(sql)

def key_exist(group_id, app_name):
    sql = "select group_id from groups where group_id = %s and app_name = %s"
    res = conf['mysql'].select(sql, [group_id, app_name], one=True)
    return True if res else False

def get_groups(_ts):

    sql = """SELECT group_id, app_name, level, node_ips
         FROM groups
         WHERE del_flag = 0 AND (`interval` = 60
      """

    for interval in conf['scan_strategy']:
        if interval != '60' and _ts % int(interval) == 0:
            sql += " OR  `interval` = %s" % interval
    sql += ")"
    groups = conf['mysql'].select(sql, [], one=False)
    return groups

def get_records(group_id, app_name):
    sql = """SELECT server_id, record_id, ip
             FROM records
             WHERE group_id = %s AND app_name = %s
          """
    records = conf['mysql'].select(sql, [group_id, app_name], one=False)
    return records

def get_all_nodes():
    sql = """SELECT node_ip FROM nodes WHERE status = 0"""
    nodes = conf['mysql'].select(sql, [], one=False)
    return [n['node_ip'] for n in nodes]
