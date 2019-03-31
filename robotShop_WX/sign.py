#!usr/bin/python#coding=utf-8

import time
import random
import string
import hashlib
from robotShop_WX import basic_log
from robotShop_WX.jsapiTicket import JsapiTicket

class Sign:
    def __init__(self, url):
        jaspiTicket = JsapiTicket()
        jsapi_ticket = jaspiTicket.getJsapiTicketNow()
        self.ret = {
            'nonceStr': self.__create_nonce_str(),
            'jsapi_ticket': jsapi_ticket,
            'timestamp': self.__create_timestamp(),
            'url': url
        }

    def __create_nonce_str(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))

    def __create_timestamp(self):
        return int(time.time())

    def sign(self):
        logRecord = basic_log.Logger('record')
        string1 = '&'.join(['%s=%s' % (key.lower(), self.ret[key]) for key in sorted(self.ret)])
        logRecord.log('string1: ' + string1)
        self.ret['signature'] = hashlib.sha1(string1).hexdigest()
        return self.ret

