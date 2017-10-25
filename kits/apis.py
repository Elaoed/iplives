# -*- coding: utf-8 -*-
""" Putting all the mysql operation on this module
    Reducing the code numbers on route module
"""
from config.conf import conf
from kits.utils import get_times

def api_create(params: dict) -> None:

    sql_param = [params['group_id'], params['app_name'], params['protocol'], params['port'],
                 params['timeout'], params['retry_count'], params['interval'], params['level'],
                 params['node_ips'], get_times(), params['domain'], params['path'],
                 params['cookies'], params['http_code']]
    sql = """INSERT INTO groups
             SET group_id = %s, app_name = %s, protocol = %s, port = %s, timeout = %s, retry_count = %s,
                 `interval` = %s, level = %s, node_ips = %s, gmt_create = %s, domain = %s,
                 `path` = %s, cookies = %s, http_code = %s
          """
    conf['mysql'].insert(sql, sql_param)

    record_ids = params['record_ids']
    ips = params['ips']
    node_ips = params['node_ips'].split(":")

    for index, _ip in enumerate(ips):

        sql_param = (params['group_id'], params['app_name'], record_ids[index], _ip, get_times())
        sql = """INSERT INTO records
                 SET group_id = %s, app_name = %s, record_id = %s, ip = %s, gmt_create = %s, ext = 0
              """

        conf['mysql'].insert(sql, sql_param)

        sql = "SELECT LAST_INSERT_ID();"
        server_id = conf['mysql'].select(sql, [], one=True)['LAST_INSERT_ID()']

        for node_ip in node_ips:
            sql_param = [server_id, node_ip, get_times()]
            sql = """INSERT INTO relation
                     SET server_id = %s, node_ip = %s, gmt_create = %s
                  """

            conf['mysql'].insert(sql, sql_param)


def api_update(params: dict):

    pass

def api_delete(group_id: int, app_name: str) -> None:

    # 后期 改成让定时任务来删除。 api只负责把del_flag置1

    sql = """SELECT server_id FROM records WHERE group_id = %s AND app_name = %s"""
    res = conf['mysql'].select(sql, [group_id, app_name], one=False)
    if not res:
        return

    server_ids = ', '.join([str(x['server_id']) for x in res] + ["-2"])

    sql = """DELETE FROM relation WHERE server_id in (%s)""" % server_ids
    conf['mysql'].delete(sql, [])

    sql = """DELETE FROM records WHERE group_id = %s AND app_name = %s"""
    conf['mysql'].delete(sql, [group_id, app_name])

    sql = """DELETE FROM groups WHERE group_id = %s AND app_name = %s"""
    conf['mysql'].delete(sql, [group_id, app_name])

def api_add_node(node_ip: str) -> None:
    """Aimed at adding group into new node_ip if node is highest level"""
    sql = "INSERT INTO nodes SET node_ip = %s, gmt_create = %s"
    conf['mysql'].insert(sql, [node_ip, get_times()])

    sql = "SELECT group_id, app_name FROM groups WHERE level = 4"
    res = conf['mysql'].select(sql, [], one=False)
    if not res:
        return

    # condition = (group_id, 'app_name'), (group_id, 'app_name')
    condition = ', '.join(['(' + ', '.join([str(con['group_id']), "'" + con['app_name'] + "'"]) + ')' for con in res])
    sql = "SELECT server_id FROM records WHERE (group_id, app_name) in (%s)" % condition
    server_ids = conf['mysql'].select(sql, [], one=False)
    if not server_ids:
        return

    content = ', '.join(['(' + ', '.join([str(x['server_id']), "'" + node_ip + "'"]) + ')' for x in server_ids])
    sql = "INSERT INTO relation(server_id, node_ip) VALUES%s" % content
    conf['mysql'].insert(sql, [])
