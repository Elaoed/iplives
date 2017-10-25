# -*- conding: utf-8 -*-

import requests
import unittest

class TestAPI(unittest.TestCase):

    def setUp(self):
        self.url = "http://127.0.0.1:6003"

    def test_add(self):
        path = "/operate_monitor"
        data = {
            'token': "",
            'app_name': "newdun_dns",
            'group_id': "1",
            'protocol': "http",
            'port': "80",
            'timeout': 3,
            'retry_count': 0,
            'interval': 60,
            'level': 1,
            'node_ips': "127.0.0.1",
            'domain': "www.jackeriss.com",
            'path': "/",
            'cookies': "",
            'http_code': "200,301",
            'ips': "115.159.192.237",
            'record_ids': "5"
        }
        res = requests.post(self.url + path, data=data)
        assert(res.status_code is 200)
        assert(res.json()['code'] == 1000)

if __name__ == "__main__":
    unittest.main()
