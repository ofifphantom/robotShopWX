#!usr/bin/python#coding=utf-8

import datetime,requests,traceback,time
from robotShop_WX.models import JsapiTicketTable
from robotShop_WX.accessToken import AccessToken
from robotShop_WX.public import setStatus
from robotShop_WX import basic_log

class JsapiTicket:
    
    def __init__(self):
        self.jsapi_ticket = None

    #获得有效jsapi_ticket
    def getJsapiTicketNow(self):
        try:
            logRecord = basic_log.Logger('record')
            jsapiTickets = JsapiTicketTable.objects.all()
            if len(jsapiTickets) > 0:
                jsapiTicket = jsapiTickets[0]
                nowTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                endTime = str(jsapiTicket.endTime)
                if endTime > nowTime:
                    self.jsapi_ticket = jsapiTicket.jsapi_ticket
                else:
                    for jsapiTicket in jsapiTickets:
                        jsapiTicket.delete()
                    getMessage = self.__getJsapiTicketByWX()
                    if getMessage['status'] != 3:
                        self.jsapi_ticket = getMessage['message']
                    else:
                        self.jsapi_ticket = None
            else:
                getMessage = self.__getJsapiTicketByWX()
                if getMessage['status'] != 3:
                    self.jsapi_ticket = getMessage['message']
                else:
                    self.jsapi_ticket = None
        except Exception,e:
            logErr = basic_log.Logger('error')
            logErr.log(traceback.format_exc())
            self.jsapi_ticket = None
        return self.jsapi_ticket


    #向微信请求jsapi_ticket并存入数据库
    def __getJsapiTicketByWX(self):
        try:
            logRecord = basic_log.Logger('record')
            getMessage = {}
            accessToken = AccessToken()
            access_token = accessToken.getAccessTokenNow()
            url = u'https://api.weixin.qq.com/cgi-bin/ticket/getticket'
            params = {
                'access_token':access_token,
                'type':'jsapi'
            }
            res = requests.get(url, params=params).json()
            if 'ticket' in res:
                jsapi_ticket = res['ticket']
                saveMessage = self.__saveJsapiTicket(jsapi_ticket)
                if saveMessage['status'] == 0:
                    getMessage = setStatus(0,jsapi_ticket)
                else:
                    getMessage = setStatus(2,jsapi_ticket)
            else:
                getMessage = setStatus(3,str(res))
        except Exception,e:
            logErr = basic_log.Logger('error')
            logErr.log(traceback.format_exc())
            getMessage = setStatus(1,'get failed')
        logRecord.log('getJsapiTicketByWX: ' + str(getMessage))
        return getMessage


    #保存jsapi_ticket到数据库
    def __saveJsapiTicket(self,jsapi_ticket):
        try:
            saveMessage = {}
            startTime = datetime.datetime.now()
            endTime = str(datetime.datetime.now() + datetime.timedelta(minutes=110))
            jsapiTicket = JsapiTicketTable(None,startTime,endTime,jsapi_ticket)
            jsapiTicket.save()
            saveMessage = setStatus(0, 'save success')
        except Exception,e:
            logErr = basic_log.Logger('error')
            logErr.log(traceback.format_exc())
            saveMessage = setStatus(1,'save failed')
        return saveMessage
    
    
    