#!usr/bin/python#coding=utf-8

import datetime,requests,traceback,time,os,stat
from robotShop_WX.models import UserTable,UserAuthTable
from robotShop_WX.public import setStatus,getAppID,getAppSecret
from robotShop_WX import basic_log
from robotShop_WX.accessToken import AccessToken
from robotShopWX.settings import BASE_DIR

class User:
    
    def __init__(self):
        pass
    
    def isRegister(self,openID):
            userAuthTables = UserAuthTable.objects.filter(openID=openID)
            if len(userAuthTables) > 0:
                userAuthTable = userAuthTables[0]
                if userAuthTable.registerTime == None:
                    return False
                else:
                    return True
            else:
                return False
        
    
    def getUserByPhone(self,phoneNumber):
        try:
            getUserByPhone = {}
            kwags = {}
            kwags['identityType'] = 'mobilePhone'
            kwags['identitfier'] = phoneNumber
            userAuthCount = UserAuthTable.objects.filter(**kwags).count()
            if userAuthCount == 0:
                getUserByPhone = setStatus(2,'the phoneNumber is invalid')
                return getUserByPhone
            userAuthTable = UserAuthTable.objects.filter(**kwags)[0]
            userTable = UserTable.objects.filter(authID=userAuthTable.id)[0]
            getUserByPhone = setStatus(0,userTable.id)
        except Exception,e:
            logErr = basic_log.Logger('error')
            logErr.log(traceback.format_exc())
            getUserByPhone = setStatus(1,'save failed')
        return getUserByPhone
    
    #保存user到数据库
    def updateUser(self,media_id,openID):
        try:
            logRecord = basic_log.Logger('record')
            updateUser = {}
            userTables = UserTable.objects.filter(openID=openID)
            userTable = userTables[0]
            accessToken = AccessToken()
            access_token = accessToken.getAccessTokenNow()
            url = u'https://api.weixin.qq.com/cgi-bin/media/get'
            params = {
                'access_token': access_token,
                'media_id': media_id
            }
            res = requests.get(url, params=params)
            uploadDate_str = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
            picture = self.__touchFile(res.content, uploadDate_str,openID)
            userTable.picture = picture
            userTable.save()
            updateUser = setStatus(0, 'save success')
        except Exception,e:
            logErr = basic_log.Logger('error')
            logErr.log(traceback.format_exc())
            updateUser = setStatus(1,'save failed')
        return updateUser

    
    def login(self,openID):
        try:
            loginAuthInfo = {}
            logRecord = basic_log.Logger('record')
            logRecord.log('openID : ' + openID)
            #loginAuth = self.__getUserToken(code)
            '''
            {
            u'openid': u'oZ1Klv0Cf5xzt_k-_CKpeB-1KYis',
            u'access_token': u'4_999KkDT-Em-W-3GXJOdOrUAVan2uXzhTs2U7pl_vZPc3U5zsyLUYCCnRxtwjQ6ut0l7d_zJq4Q3yURce4fhacB0aYCd-flu00DfvCkXjYyA',
            u'unionid': u'okGNQwSdG9S9iwR4afXTKcV0PKFI',
            u'expires_in': 7200,
            u'scope': u'snsapi_userinfo',
            u'refresh_token': u'4_k7fSn7aUvJzKRb12jHJEZrb8DWI3QTgc3YTDmNXfHg8O4IcaJMVar4nmX_e0-n4tyYO78paF_6WlUdPaAqoy_Q5zXafk-t5fag9L1WiA16I'
            }
            '''
            #openID = loginAuth['openid']
            userInfo = self.__getUserInfoByWX(openID)
            if userInfo['subscribe'] == 0:
                loginAuthInfo = setStatus(4, 'please subscribe us')
                return loginAuthInfo
            #access_token = loginAuth['access_token']
            #refresh_token = loginAuth['refresh_token']
            access_token = None
            refresh_token = None
            userAuthTables = UserAuthTable.objects.filter(openID=openID)
            if len(userAuthTables) > 0:
                userAuthTable = userAuthTables[0]
                if userAuthTable.registerTime != None:
                    #可以开门
                    userTables = UserTable.objects.filter(openID=userAuthTable.openID)
                    if len(userTables) == 0:
                        nickName = ''
                    else:
                        nickName = userTables[0].nickName
                    loginAuthInfo = setStatus(0,nickName)
                else:
                    logRecord.log('register step 2')
                    #用户关注公众号，未注册
                    registerStep = self.__registerStep2(userAuthTable,access_token,refresh_token)
                    if registerStep:
                        #让用户完成注册
                        loginAuthInfo = setStatus(2,openID)
                    else:
                        loginAuthInfo = setStatus(3,'login failed')
            else:
                logRecord.log('register step 1')
                registerStep = self.registerStep1(openID,access_token,refresh_token)
                if registerStep:
                    #让用户关注公众号并手机注册
                    loginAuthInfo = setStatus(2,openID)
                else:
                    loginAuthInfo = setStatus(3,'login failed')
        except Exception,e:
            logErr = basic_log.Logger('error')
            logErr.log(traceback.format_exc())
            loginAuthInfo = setStatus(1,'register failed')
        return loginAuthInfo
    
    
    def registerStep1(self,openID,access_token,refresh_token):
        try:
            registerStep = False
            identityType = None
            identitfier = None
            credential = None
            registerTime = None
            startTime = datetime.datetime.now()
            tokenEndTime = str(datetime.datetime.now() + datetime.timedelta(minutes=110))
            refreshTime = str(datetime.datetime.now() + datetime.timedelta(days=30))
            userAuthTable = UserAuthTable(None,openID,identityType,identitfier,credential,registerTime,access_token,tokenEndTime,refresh_token,refreshTime)
            userAuthTable.save()
            userInfo = self.__getUserInfoByWX(openID)
            nickname = userInfo['nickname'].encode('raw_unicode_escape')
            userTable = UserTable(None,openID,nickname,userInfo['headimgurl'],None)
            userTable.save()
            registerStep = True
        except Exception,e:
            logErr = basic_log.Logger('error')
            logErr.log(traceback.format_exc())
            registerStep = False
        return registerStep
    
    def __registerStep2(self,userAuthTable,access_token,refresh_token):
        try:
            registerStep = False
            userAuthTable.identityType = None
            userAuthTable.identitfier = None
            userAuthTable.credential = None
            userAuthTable.registerTime = None
            startTime = datetime.datetime.now()
            userAuthTable.tokenEndTime = str(datetime.datetime.now() + datetime.timedelta(minutes=110))
            userAuthTable.refreshTime = str(datetime.datetime.now() + datetime.timedelta(days=30))
            userAuthTable.save()
            userTables = UserTable.objects.filter(openID=userAuthTable.openID)
            userTable = userTables[0]
            userInfo = self.__getUserInfoByWX(userAuthTable.openID)
            userTable.nickName = userInfo['nickname'].encode('raw_unicode_escape')
            userTable.avatar = userInfo['headimgurl']
            userTable.save()
            registerStep = True
        except Exception,e:
            logErr = basic_log.Logger('error')
            logErr.log(traceback.format_exc())
            registerStep = False
        return registerStep
    
    def registerStep3(self,openID,phoneNumber):
        try:
            registerStep = False
            userAuthTables = UserAuthTable.objects.filter(openID=openID)
            userAuthTable = userAuthTables[0]
            userAuthTable.identityType = 'mobilePhone'
            userAuthTable.identitfier = phoneNumber
            userAuthTable.credential = None
            userAuthTable.registerTime = datetime.datetime.now()
            userAuthTable.save()
            registerStep = True
        except Exception,e:
            logErr = basic_log.Logger('error')
            logErr.log(traceback.format_exc())
            registerStep = False
        return registerStep


    #获取用户授权登录json
    def __getUserToken(self,code):
        
        url = u'https://api.weixin.qq.com/sns/oauth2/access_token'
        params = {
            'appid': getAppID(),
            'secret': getAppSecret(),
            'code' : code,
            'grant_type': 'authorization_code',
        }
        res = requests.get(url, params=params).json()
        return res


    #获取微信用户信息
    def __getUserInfoByWX(self,openID):
        userInfo = {}
        accessToken = AccessToken()
        access_token = accessToken.getAccessTokenNow()
        url = u'https://api.weixin.qq.com/cgi-bin/user/info'
        params = {
            'access_token': access_token,
            'openid': openID,
            'lang' : 'zh_CN'
        }
        res = requests.get(url, params=params).json()
        userInfo['nickname'] = res['nickname']
        userInfo['headimgurl'] = res['headimgurl']
        userInfo['subscribe'] = res['subscribe']
        return userInfo


    def __saveUserTable(self,userAtuthID):
        try:
            userTable = UserTable(None,userAtuthID,None,None,None)
            userTable.save()
        except Exception,e:
            logErr = basic_log.Logger('error')
            logErr.log(traceback.format_exc())
    


    def __touchFile(self,content, uploadDate_str,openID):
        pic = BASE_DIR + '/static/user/' + openID +'_' + uploadDate_str + '.jpg'
        picPath = '/static/user/' + openID +'_' + uploadDate_str + '.jpg'
        with open(pic, 'wb+') as destination:
            destination.write(content)
        os.chmod(pic, stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)
        return picPath
