# -*- coding: utf-8 -*-

import requests
import json

class Ding(object):

    def __init__(self, access_token=None, content="test", atMobiles=None, isAtAll=False):
        self.url = "https://oapi.dingtalk.com/robot/send?"
        if not access_token:
            self.access_token = "224bf0490815ef03537acefba7d11f617977197991e0cb96b78a031b9c23e137"
            self.access_token = "ff5322aacfc4d7db3960de84487354f14fb901a6ef20187f4eedec825f384da4"
        else:
            self.access_token = access_token
        self.msgtype = "text"
        self.content = content
        self.atMobiles = [] if not atMobiles else atMobiles
        self.isAtAll = isAtAll

    def make_data(self):
        data = dict()
        data["msgtype"] = self.msgtype
        data["text"] = {
            "content": self.content
        }
        data["at"] = {
            "atMobiles": self.atMobiles,
            "isAtAll": self.isAtAll
        }
        return data

    def send(self):
        url = self.url + "access_token=" + self.access_token
        headers = {'Content-Type': 'application/json'}
        data = json.dumps(self.make_data())
        res = requests.post(url, data=data, headers=headers)
        jres = res.json()
        if jres['errcode'] is 0 and jres['errmsg'] == "ok":
            pass
        else:
            print(jres)

def send_ding_msg(content):

    msg = "[宕机监控] 告警:\n" + content
    dobject = Ding(content=msg)
    dobject.send()
