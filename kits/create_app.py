# -*- coding: utf-8 -*-
import copy
import json
from functools import wraps

from flask import Flask, request
from config.conf import conf
from kits.apis import api_create
from kits.apis import api_update
from kits.apis import api_delete
from kits.custom_exception import CustomException
from kits.utils import key_exist
from kits.valids import newdun_dns_insert
from kits.valids import newdun_dns_update
from kits.apis import api_add_node

app = Flask(__name__)
param_valids = {
    "newdun_dns_insert": newdun_dns_insert,
    "newdun_dns_update": newdun_dns_update,
}
RET_OBJ = {
    'code': 1000,  # 1000+ means failed. 1000 means success
    'msg': "",     # 100\d means error type. 1001\d means error code
    'info': {
    }
}

IP_TOKEN = conf['tokens']

def try_except(orig_func):
    """simplest try except."""
    @wraps(orig_func)
    def wrapper(*args, **kwargs):
        ret_obj = copy.deepcopy(RET_OBJ)
        try:

            token = request.form.get('token', None)
            remote_ip = request.remote_addr
            if (remote_ip != "127.0.0.1") and \
               (not token or remote_ip not in IP_TOKEN or IP_TOKEN[remote_ip] != token):
                raise CustomException("Token not right", 1004)

            app_name = request.form.get('app_name', None)
            if not app_name:
                raise CustomException("app name is not exist", 1002)

            # params = {k: v for k, v in request.form.items()}
            params = request.form
            res = orig_func(params)
            return json.dumps(res)
        except CustomException as err:
            conf['logger'].error(err.msg)
            ret_obj['msg'] = err.msg
            ret_obj['code'] = err.code
            return json.dumps(ret_obj)
        except Exception:
            conf['logger'].critical("Exception Outermost", exc_info=True)
            ret_obj['msg'] = "Unknow Exceptions Please inform the Administrator"
            ret_obj['code'] = 1001
            return json.dumps(ret_obj)

    return wrapper

@app.route("/operate_monitor", methods=['POST'])
@try_except
def operate_monitor(params):
    """ different apps has different required params"""

    ret_obj = copy.deepcopy(RET_OBJ)

    group_id = params.get("group_id", type=int, default=None)
    app_name = params.get("app_name")
    operate = "update" if key_exist(group_id, app_name) else "insert"
    valid_key = "_".join([app_name, operate])
    if valid_key not in param_valids:
        raise CustomException("operate_monitor Not found corresponding valid function for %s" % app_name, 1005)

    params = param_valids[valid_key](params)
    api_create(params) if operate == "insert" else api_update(params)

    ret_obj['msg'] = operate + " monitor successfully."
    return ret_obj

@app.route("/stop_monitor", methods=["POST"])
@try_except
def stop_monitor(params):
    ret_obj = copy.deepcopy(RET_OBJ)

    group_id = params.get("group_id", type=int, default=None)
    app_name = params.get("app_name", type=str, default=None)
    if group_id is None or app_name is None:
        raise CustomException("lack of param. group_id or app_name in stop_monitor", 1002)

    api_delete(group_id, app_name)

    ret_obj['msg'] = "stop monitor successfully"
    return ret_obj

# @app.route("/modify_node_ips")
# @try_except
# def modify_node_ips():
#     pass

# ==================================== API For Frontend Above ============================

@app.route('/add_node', methods=['POST'])
def add_node():
    ret_obj = copy.deepcopy(RET_OBJ)
    ret_obj['msg'] = "add node successfully"
    node_ip = request.form.get("node_ip", type=str, default=None)
    passwd = request.form.get("passwd", type=str, default=None)

    if node_ip is None or passwd is None:
        conf['logger'].error("api - add_node: lack of param")
        ret_obj = copy.deepcopy(RET_OBJ)
        ret_obj['msg'] = "lack of param"
        ret_obj['code'] = 1002
        return json.dumps(ret_obj)

    if passwd != "passwd":
        pass

    api_add_node(node_ip)
    return json.dumps(ret_obj)

# @app.route('/remove_node', methods=['POST'])
# def remove_node():
#     ret_obj = copy.deepcopy(RET_OBJ)
#     ret_obj['msg'] = "add node successfully"
#     node_ip = request.form.get("node_ip", type=str, default=None)
#     passwd = request.form.get("passwd", type=str, default=None)

#     if node_ip is None or passwd is None:
#         conf['logger'].error("api - add_node: lack of param")
#         ret_obj = copy.deepcopy(RET_OBJ)
#         ret_obj['msg'] = "lack of param"
#         ret_obj['code'] = 1002
#         return json.dumps(ret_obj)

#     if passwd != "passwd":
#         pass

#     api_add_node(node_ip)
#     return json.dumps(ret_obj)

@app.route('/deal', methods=['POST'])
def deal():
    """ Deal with result that probe node detected. save it into redis only
        params:
            timestamp: 时间戳
            {
                res_time: 访问时间
                reason: 结果以及原因是什么 0(no result) 1(connection error) 2(timeout) 1xx-5xx(httpcode)
                server_id: server端唯一识别
            }
        因为是批量接收, 所以只有一个data = "server_id,res_time,reason:server_id,res_time,reason"
    """

    node_ip = request.remote_addr
    ret_obj = copy.deepcopy(RET_OBJ)
    ret_obj['msg'] = "server process successfully"

    data = request.form.get("data", type=str, default=None)
    timestamp = request.form.get("timestamp", type=int, default=None)
    if not data or not timestamp:
        conf['logger'].error('data not exist')
        ret_obj = copy.deepcopy(RET_OBJ)
        ret_obj['msg'] = "data not exist"
        ret_obj['code'] = 1002
        return json.dumps(ret_obj)

    jdata = json.loads(data)
    for record in jdata:  # {'server_id': 1, 'res_time': 5ms, 'last_status': 1}
        key = "iplive_cache:%d" % timestamp
        name = "%s:%s" % (node_ip, record['server_id'])
        conf['redis'].hset(key, name, ':'.join([str(record['res_time']), str(record['last_status'])]))
        conf['redis'].expire(key, 60)

    return json.dumps(ret_obj)
