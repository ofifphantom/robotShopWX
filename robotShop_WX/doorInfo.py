#!usr/bin/python#coding=utf-8

from robotShop_WX.models import DoorInfoTable
import traceback
from robotShop_WX import basic_log

class DoorInfo:
    
    def __init__(self):
        pass
    
    def insertDoorInfo(self,branchID,doorID):
        try:
            branchIDCount = DoorInfoTable.objects.filter(branchID=branchID).count()
            doorIDCount = DoorInfoTable.objects.filter(doorID=doorID).count()
            if branchIDCount == 0 and doorIDCount == 0:
                doorInfoTable = DoorInfoTable(None,branchID, doorID)
                doorInfoTable.save()
                return 0
            else:
                return 2
        except Exception, e:
            logErr = basic_log.Logger('error')
            logErr.log(traceback.format_exc())
            return 1
        
        
    def getDoorID(self,branchID):
        try:
            doorInofs = DoorInfoTable.objects.filter(branchID=branchID)
            if len(doorInofs) > 0:
                doorInof = doorInofs[0]
                return doorInof.doorID
            return 0
        except Exception, e:
            logErr = basic_log.Logger('error')
            logErr.log(traceback.format_exc())
            return -1