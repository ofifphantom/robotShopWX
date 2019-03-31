from django.db import models

# Create your models here.
class AccessTokenTable(models.Model):
    
    startTime = models.DateTimeField('startTime',null=True)
    endTime = models.DateTimeField('endTime',null=True)
    access_token = models.CharField('access_token',max_length=600,null=True)
    
    def create(self,startTime,endTime,access_token,tokenType):
        accessToken = self.create(startTime=startTime,endTime=endTime,access_token=access_token)
        return accessToken

    def __unicode__(self):
        aaa = ['startTime','endTime','access_token']
        xz = ''
        for a in aaa:
            value = getattr(self, a)
            xz = a + ':' + str(value) + '\n' +xz
        return xz

    class Meta:
        db_table = "accessTokenTable"
        verbose_name = "accessTokenTable"
        verbose_name_plural = "accessTokenTable"
        

class JsapiTicketTable(models.Model):
    
    startTime = models.DateTimeField('startTime',null=True)
    endTime = models.DateTimeField('endTime',null=True)
    jsapi_ticket = models.CharField('jsapi_ticket',max_length=600,null=True)
    
    def create(self,startTime,endTime,jsapi_ticket):
        accessToken = self.create(startTime=startTime,endTime=endTime,jsapi_ticket=jsapi_ticket)
        return accessToken

    def __unicode__(self):
        aaa = ['startTime','endTime','jsapi_ticket']
        xz = ''
        for a in aaa:
            value = getattr(self, a)
            xz = a + ':' + str(value) + '\n' +xz
        return xz

    class Meta:
        db_table = "jsapiTicketTable"
        verbose_name = "jsapiTicketTable"
        verbose_name_plural = "jsapiTicketTable"

        
class UserTable(models.Model):
    
    openID = models.CharField('openID',max_length=50,null=True)
    nickName = models.CharField('nickName',max_length=100,null=True)
    avatar = models.CharField('avatar',max_length=200,null=True)
    picture = models.CharField('picture',max_length=200,null=True)
    
    def create(self,openID,nickName,avatar,picture):
        user = self.create(openID=openID,nickName=nickName,avatar=avatar,picture=picture)
        return user

    def __unicode__(self):
        aaa = ['openID','nickName','avatar','picture']
        xz = ''
        for a in aaa:
            value = getattr(self, a)
            xz = a + ':' + str(value) + '\n' +xz
        return xz

    class Meta:
        db_table = 'user'
        verbose_name = 'user'
        verbose_name_plural = 'user'
        
       
class UserAuthTable(models.Model):

    openID = models.CharField('openID',max_length=50,null=True)
    identityType = models.CharField('identityType',max_length=50,null=True)
    identitfier = models.CharField('identitfier',max_length=100,null=True)
    credential = models.CharField('credential',max_length=50,null=True)
    registerTime = models.DateTimeField('registerTime',null=True)
    access_token = models.CharField('access_token',max_length=600,null=True)
    tokenEndTime = models.DateTimeField('tokenEndTime',null=True)
    refresh_token = models.CharField('refresh_token',max_length=600,null=True)
    refreshTime = models.DateTimeField('refreshTime',null=True)
    
    def create(self,openID,identityType,identitfier,credential,registerTime,access_token,tokenEndTime,refresh_token,refreshTime):
        user = self.create(openID=openID,identityType=identityType,identitfier=identitfier,credential=credential,registerTime=registerTime,access_token=access_token,tokenEndTime=tokenEndTime,refresh_token=refresh_token,refreshTime=refreshTime)
        return user

    def __unicode__(self):
        aaa = ['openID','identityType','identitfier','credential','registerTime','access_token','tokenEndTime','refresh_token','refreshTime']
        xz = ''
        for a in aaa:
            value = getattr(self, a)
            xz = a + ':' + str(value) + '\n' +xz
        return xz

    class Meta:
        db_table = 'userAuth'
        verbose_name = 'userAuth'
        verbose_name_plural = 'userAuth'


class MessageTable(models.Model):
    
    identityCode = models.CharField('identityCode',max_length=10,null=True)
    phoneNumber = models.CharField('phoneNumber',max_length=20,unique=True,null=True)
    startTime = models.DateTimeField('startTime',null=True)
    endTime = models.DateTimeField('endTime',null=True)
    
    def create(self,identityCode,phoneNumber,startTime,endTime):
        message = self.create(identityCode=identityCode,phoneNumber=phoneNumber,startTime=startTime,endTime=endTime)
        return message

    def __unicode__(self):
        aaa = ['identityCode','phoneNumber','startTime','endTime']
        xz = ''
        for a in aaa:
            value = getattr(self, a)
            xz = a + ':' + str(value) + '\n' +xz
        return xz

    class Meta:
        db_table = 'message'
        verbose_name = 'message'
        verbose_name_plural = 'message'

class QRCodeTable(models.Model):

    ticket = models.CharField('ticket',max_length=600,null=True)
    url = models.CharField('url',max_length=100,null=True)

    def create(self, ticket, url):
        qrCode = self.create(ticket=ticket, url=url)
        return qrCode

    def __unicode__(self):
        aaa = ['ticket', 'url']
        xz = ''
        for a in aaa:
            value = getattr(self, a)
            xz = a + ':' + str(value) + '\n' + xz
        return xz

    class Meta:
        db_table = 'qrCode'
        verbose_name = 'qrCode'
        verbose_name_plural = 'qrCode'
        
        
class DoorInfoTable(models.Model):

    branchID = models.CharField('ticket',max_length=50,null=True)
    doorID = models.CharField('url',max_length=50,null=True)

    def create(self, branchID, doorID):
        door = self.create(branchID=branchID, doorID=doorID)
        return door

    def __unicode__(self):
        aaa = ['branchID', 'doorID']
        xz = ''
        for a in aaa:
            value = getattr(self, a)
            xz = a + ':' + str(value) + '\n' + xz
        return xz

    class Meta:
        db_table = 'doorInfo'
        verbose_name = 'doorInfo'
        verbose_name_plural = 'doorInfo'        
