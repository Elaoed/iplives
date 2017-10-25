# -*- coding: utf-8 -*-

import sys
import argparse
from config.conf import conf
from config.conf import enviroment
from kits.log import get_logger
from kits.mysqlob import MySqlOB
from kits.redispool import Redispool

def initialize(modules: list) -> None:

    if "entrance" in modules:
        parser = argparse.ArgumentParser()
        parser.add_argument("-e", "--env", action="store", dest="env",
                            help="enviroment of server. prod|test|dev")
        parser.add_argument("-p", "--port", action="store", type=int, dest="port", default=6003,
                            help="port of running iplive node")
        if len(sys.argv) < 2:
            parser.print_help()
            sys.exit()

        args = parser.parse_args()
        if args.env not in ["dev", "test", "prod"]:
            print("enviroment not support")
            sys.exit()

        env = enviroment[args.env]
        conf['env'] = env
        conf['port'] = args.port

    # if "logger" in modules:
    #     conf['logger'] = get_logger('iplives', on_screen=True, level=env['level'])

    if "logger" in modules:
        conf['logger'] = get_logger('iplives', on_screen=True, level="info")

    # if "mysql" in modules:
    #     conf['mysql'] = MySqlOB(host=env['mysql']['host'], user=env['mysql']['user'],
    #                             passwd=env['mysql']['passwd'], port=env['mysql']['port'],
    #                             db=env['mysql']['db'])

    if "mysql" in modules:
        conf['mysql'] = MySqlOB()
    if "redis" in modules:
        conf['redis'] = Redispool()
