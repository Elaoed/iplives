# -*- coding:utf-8 -*-
""" A middle ware of DBUtils and program
    Example:
        m = MySqlOB()
        sql = "INSERT INTO table_name SET column = %s, column2 = %s"
        sql_param = [3, 4]
        m.insert(sql, sql_param)

    Notice: 1. only %s can be written in sql language
            2. you don't need to add '' or "" around %s like '%s' or "%s"
            3. any basic type can be use in sql_param
            4. when using in (%s). make sure using sql('%s' module) % sql_param(tuple). or it doesn't work
"""

from DBUtils.PooledDB import PooledDB
import pymysql as mysql
# import MySQLdb as mysql
# from MySQLdb.cursors import DictCursor
# from pymysql.err import MySQLError
from pymysql.cursors import DictCursor
from config.mysql_config import DB_HOST
from config.mysql_config import DB_PORT
from config.mysql_config import DB_USER
from config.mysql_config import DB_PASSWORD
from config.mysql_config import DB_DBNAME
from config.mysql_config import DB_BLOCKING
from config.mysql_config import DB_MAX_USAGE
from config.mysql_config import DB_CHARSET
from config.mysql_config import DB_AUTO_COMMIT
from config.mysql_config import DB_MAX_SHARED
from config.mysql_config import DB_MAX_CONNECYIONS


class MySqlOB(object):
    def __init__(self, host=None, port=None, user=None, passwd=None, db=None, charset=None,
                 autocommit=None, maxshared=None, maxconnections=None, blocking=None, maxusage=None,
                 cursorclass=DictCursor):

        if host is None:
            host = DB_HOST
        if port is None:
            port = DB_PORT
        if user is None:
            user = DB_USER
        if passwd is None:
            passwd = DB_PASSWORD
        if db is None:
            db = DB_DBNAME
        if charset is None:
            charset = DB_CHARSET
        if autocommit is None:
            autocommit = DB_AUTO_COMMIT
        if maxshared is None:
            maxshared = DB_MAX_SHARED
        if maxconnections is None:
            maxconnections = DB_MAX_CONNECYIONS
        if blocking is None:
            blocking = DB_BLOCKING
        if maxusage is None:
            maxusage = DB_MAX_USAGE

        self.__POOL = PooledDB(
            mysql,
            host=host,
            user=user,
            passwd=passwd,
            db=db,
            port=port,
            charset=charset,
            cursorclass=cursorclass,
            autocommit=autocommit,
            maxshared=maxshared,
            maxconnections=maxconnections,
            blocking=blocking,
            maxusage=maxusage
        )

    def get_connection(self):
        return self.__POOL.connection()

    def insert(self, sql, params):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, params)
            conn.commit()
        except Exception as err:
            conn.rollback()
            raise err
        finally:
            cursor.close()
            conn.close()

    def update(self, sql, params):
        self.insert(sql, params)

    def select(self, sql, params, one=True):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        if one:
            obj = cursor.fetchone()
        else:
            obj = cursor.fetchall()
        cursor.close()
        conn.close()
        return obj

    def delete(self, sql, params):
        self.insert(sql, params)

    # def exec_iu_conn(self, commands, conn, params):
    #     cursor = conn.cursor()
    #     try:
    #         cursor.execute(commands, params)
    #         conn.commit()
    #     except Exception as err:
    #         raise err
    #         conn.rollback()

    # def exec_query_conn(self, commands, conn, params, one=True):
    #     cursor = conn.cursor()
    #     cursor.execute(commands, params)
    #     if one:
    #         obj = cursor.fetchone()
    #     else:
    #         obj = cursor.fetchall()
    #     cursor.close()
    #     return obj
