#!usr/bin/python#coding=utf-8

import datetime,requests,traceback,time
from robotShop_WX.models import AccessTokenTable
from robotShop_WX.public import setStatus,getAppID,getAppSecret
from robotShop_WX import basic_log

class AccessToken:
    def __init__(self):
        pass

    #获得有效access_token
    def getAccessTokenNow(self):
        try:
            logRecord = basic_log.Logger('record')
            accessTokens = AccessTokenTable.objects.all()
            if len(accessTokens) > 0:
                accessToken = accessTokens[0]
                nowTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                endTime = str(accessToken.endTime)
                if endTime > nowTime:
                    access_token = accessToken.access_token
                else:
                    for accessToken in accessTokens:
                        accessToken.delete()
                    getMessage = self.__getAccessTokenByWX()
                    if getMessage['status'] != 3:
                        access_token = getMessage['message']
                    else:
                        access_token = None
            else:
                getMessage = self.__getAccessTokenByWX()
                if getMessage['status'] != 3:
                    access_token = getMessage['message']
                else:
                    access_token = None
        except Exception,e:
            logErr = basic_log.Logger('error')
            logErr.log(traceback.format_exc())
            access_token = None
        return access_token

    #向微信请求access_token并存入数据库
    def __getAccessTokenByWX(self):
        try:
            getMessage = {}
            logRecord = basic_log.Logger('record')
            url = u'https://api.weixin.qq.com/cgi-bin/token'
            params = {
                'grant_type':'client_credential',
                'appid':getAppID(),
                'secret':getAppSecret()
            }
            res = requests.get(url, params=params).json()
            if 'access_token' in res:
                access_token = res['access_token']
                saveMessage = self.__saveAccessToken(access_token)
                if saveMessage['status'] == 0:
                    getMessage = setStatus(0, access_token)
                else:
                    getMessage = setStatus(2, access_token)
            else:
                getMessage = setStatus(3, str(res))
        except Exception,e:
            logErr = basic_log.Logger('error')
            logErr.log(traceback.format_exc())
            getMessage = setStatus(1,'get failed')
        return getMessage


    #保存access_token到数据库
    def __saveAccessToken(self,access_token):
        try:
            saveMessage = {}
            startTime = datetime.datetime.now()
            endTime = str(datetime.datetime.now() + datetime.timedelta(minutes=110))
            accessToken = AccessTokenTable(None,startTime,endTime,access_token)
            accessToken.save()
            saveMessage = setStatus(0, 'save success')
        except Exception,e:
            logErr = basic_log.Logger('error')
            logErr.log(traceback.format_exc())
            saveMessage = setStatus(1,'save failed')
        return saveMessage


