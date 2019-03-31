#!usr/bin/python#coding=utf-8

import datetime,requests,traceback,time,random,string,hashlib,json,base64
from robotShop_WX.models import MessageTable
from robotShop_WX.public import setStatus
from robotShop_WX import basic_log
from wechatpy.replies import ArticlesReply

class Message:
    
    def __init__(self):
        pass

    def sendArticlesReply(self,url,openID,imageURL,status):
        try:
            if status == 2:
                title = '还差一步，马上开门！点击完成身份验证！'
                description = '绑定手机，上传照片，即可开门购物！'
            elif status == 1:
                title = '开门失败！'
                description = '硬件故障，请联系客服！'
            else:
                title = '已开门！'
                description = '欢迎光临，小日子便利店！'
            reply = ArticlesReply()
            reply.source = 'gh_13a22430f791'
            reply.target =  openID
            # simply use dict as article
            reply.add_article({
                'title': title,
                'description' : description,
                'image': imageURL,
                'url': url
            })
            return reply
        except Exception, e:
            logErr = basic_log.Logger('error')
            logErr.log(traceback.format_exc())
            return None


    #发送短信
    def sendMessage(self,phoneNumber):
        try:
            logRecord = basic_log.Logger('record')
            sendMessage = {}
            identityCode = ''.join(random.choice(string.digits) for _ in range(4))
            startTime = datetime.datetime.now()
            endTime = str(datetime.datetime.now() + datetime.timedelta(minutes=2))
            messageCount = MessageTable.objects.filter(phoneNumber=phoneNumber).count()
            if messageCount > 0:
                MessageTable.objects.filter(phoneNumber=phoneNumber)[0].delete()
            messageTable = MessageTable(None,identityCode,phoneNumber,startTime,endTime)
            messageTable.save()
            statusCode = self.__send(phoneNumber,identityCode)
            if statusCode == 0:
                sendMessage = setStatus(0,'send success')
            else:
                sendMessage = setStatus(2, 'send failed')
        except Exception,e:
            logErr = basic_log.Logger('error')
            logErr.log(traceback.format_exc())
            sendMessage = setStatus(1,'send failed')
        return sendMessage

    #校验验证码
    def checkCode(self,phoneNumber,identityCode):
        messageTables = MessageTable.objects.filter(phoneNumber=phoneNumber)
        if len(messageTables) == 0:
            return False
        messageTable = messageTables[0]
        nowTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        endTime = str(messageTable.endTime)
        if endTime > nowTime and identityCode == messageTable.identityCode:
            return True
        else:
            return False
            
    def __send(self,phoneNumber,identityCode):
        logRecord = basic_log.Logger('record')
        sigParameter = self.__getSigParameter()
        authorization = self.__getAuthorization()
        url = u'https://app.cloopen.com:8883/2013-12-26/Accounts/8a48b5515493a1b701549d7bf8530b3d/SMS/TemplateSMS?sig=' + sigParameter
        data = json.dumps(
            {
                'to': phoneNumber,
                'appId': '8a216da85fe1c856015ff3320fbb08b5',
                'templateId': '219952',
                'datas': [identityCode, '1分钟']
            }
        )
        headers = {
            'content-length':139,
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=utf-8',
            'Authorization': authorization
        }
        res = requests.post(url, data=data, headers=headers).json()
        logRecord.log('message`s response:   ' + str(res))
        return res['statusCode']



    def __getSigParameter(self):
        nowTime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        sid = '8a48b5515493a1b701549d7bf8530b3d'
        token = '57303e9e979a466dbaca0ee9a48bf6ab'
        sigParameter = sid + token + nowTime
        sigParameter = hashlib.md5(sigParameter.encode('utf-8')).hexdigest()
        return sigParameter.upper()


    def __getAuthorization(self):
        nowTime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        sid = '8a48b5515493a1b701549d7bf8530b3d'
        authorization = sid + ':' + nowTime
        authorization = base64.b64encode(authorization)
        return authorization



