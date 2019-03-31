#!usr/bin/python#coding=utf-8

from robotShop_WX import basic_log
from robotShop_WX.public import setStatus
import json,requests,traceback
from robotShop_WX.accessToken import AccessToken
from robotShop_WX.models import QRCodeTable


class QRCode:
    def __init__(self):
        pass

    def getQRCode(self,branchID):
        return self.__getgetQRCodeByWX(branchID)

    def __getgetQRCodeByWX(self,branchID):
        try:
            logRecord = basic_log.Logger('record')
            getMessage = {}
            accessToken = AccessToken()
            access_token = accessToken.getAccessTokenNow()
            url = u'https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token='+access_token
            data = json.dumps(
                {"action_name": "QR_LIMIT_STR_SCENE", "action_info": {"scene": {"scene_str": branchID}}}
            )
            res = requests.post(url, data=data).json()
            if 'ticket' in res:
                ticket = res['ticket']
                url = res['url']
                saveMessage = self.__saveQRCode(ticket,url)
                newURL = 'https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=' + ticket
                if saveMessage['status'] == 0:
                    getMessage = setStatus(0, newURL)
                else:
                    getMessage = setStatus(2, newURL)
            else:
                getMessage = setStatus(3, str(res))
        except Exception, e:
            logErr = basic_log.Logger('error')
            logErr.log(traceback.format_exc())
            getMessage = setStatus(1, 'get failed')
        return getMessage


    def __saveQRCode(self,ticket,url):
        try:
            saveMessage = {}
            qrCodeTable = QRCodeTable(None, ticket,url)
            qrCodeTable.save()
            saveMessage = setStatus(0, 'save success')
        except Exception, e:
            logErr = basic_log.Logger('error')
            logErr.log(traceback.format_exc())
            saveMessage = setStatus(1, 'save failed')
        return saveMessage
