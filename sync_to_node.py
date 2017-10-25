# -*- coding: utf-8 -*-
""" Sync server database with nodes
    1. insert
    2. update
    3. delete
"""
import gevent
import requests
from config.conf import conf
from kits.ding import send_ding_msg
from kits.utils import compose_url

def sync_to_node(server_id, node_ip):
    sql = """SELECT server_id, app_name, group_id, record_id, ip
             FROM records
             WHERE server_id = %s
          """
    data = conf['mysql'].select(sql, [server_id], one=True)

    sql = """SELECT protocol, port, `path`, domain, cookies, http_code, retry_count, `interval`, timeout
             FROM groups
             WHERE group_id = %s AND app_name = %s AND del_flag = 0"""
    data.update(conf['mysql'].select(sql, [data['group_id'], data['app_name']], one=True))

    # send request
    url = compose_url("http", node_ip, 8877, "/operate")

    try:
        res = requests.post(url, data=data, timeout=3)
        if res.status_code is 200:

            if res.json()['code'] == 1000:
                sql = """UPDATE relation
                         SET sync = 1
                         WHERE node_ip = %s AND server_id = %s
                      """
                conf['mysql'].update(sql, [node_ip, server_id])
                conf['logger'].info("sync to node successfully...")
            else:
                msg = "code not right. 1000 desired %d get" % res.json()['code']
                conf['logger'].info(msg)
                send_ding_msg(msg)
        else:
            msg = "Sync to node status code error: %d " % res.status_code
            conf['logger'].info(msg)
            send_ding_msg(msg)
    except requests.exceptions.RequestException as err:
        # conf['logger'].critical("Node error", exc_info=True)
        conf['logger'].critical(err.__str__())
        send_ding_msg("向节点同步数据出现异常: " + err.__str__())

def sync_poller():

    print("Start sync to node poller ......")
    while True:
        sql = """SELECT server_id, node_ip
                 FROM relation
                 WHERE sync = 0
              """
        res = conf['mysql'].select(sql, [], one=False)
        [sync_to_node(task['server_id'], task['node_ip']) for task in res]
        gevent.sleep(20)

if __name__ == "__main__":
    from kits import initialize
    initialize(["mysql", "logger"])
    sync_poller()
