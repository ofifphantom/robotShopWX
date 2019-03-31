#!usr/bin/python#coding=utf-8

import json,requests,traceback
from robotShop_WX import basic_log
from robotShop_WX.models import DoorInfoTable

def openDoor(branchID):
    try:
        doorTables = DoorInfoTable.objects.filter(branchID=branchID)
        if len(doorTables) > 0:
            doorTable = doorTables[0]
            doorID = doorTable.doorID
            url = u'http://39.107.24.82:8081/door/'
            res = requests.get(url,timeout=4).json()
            if res['status'] == 1:
                return True
            else:
                return False
        else:
            return False
    except Exception, e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        return False

def setStatus(status,message):
    setStatus = {}
    setStatus['status'] = status
    setStatus['message'] = message
    return setStatus


def getAppID():
    AppID = 'wx2c456d99ce2a2e86'
    return AppID


def getAppSecret():
    AppSecret = 'c12a27afa26718d5857fd12aef076870'
    return AppSecret