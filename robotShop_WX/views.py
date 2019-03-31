#!usr/bin/python#coding=utf-8

from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from robotShop_WX import basic_log
from robotShop_WX.forms import RegisterForm
from robotShop_WX.sign import Sign
from robotShop_WX.qrCode import QRCode
from robotShop_WX.public import setStatus,openDoor
from robotShop_WX.message import Message
from robotShop_WX.doorInfo import DoorInfo
from robotShop_WX.user import User
import hashlib,json,traceback
from wechatpy import parse_message
import re,sys,math,os,stat,time,subprocess,chardet,docx
from docx import Document

DOMAIN = 'http://shop.wuliwuli.cn'

reload(sys)
sys.setdefaultencoding('utf-8')

@csrf_exempt
def wechat(request):
    try:
        logRecord = basic_log.Logger('record')
        if request.method == 'GET':
            signature = request.GET['signature']
            timestamp = request.GET['timestamp']
            nonce = request.GET['nonce']
            wxtoken = 'xrzbld_xrzbld'
            echostr = request.GET['echostr']
            list = [wxtoken,timestamp,nonce]
            list.sort()
            list = ''.join(list)
            sha1 = hashlib.sha1()
            sha1.update(list.encode('utf-8'))
            hashcode = sha1.hexdigest()
            if hashcode == signature:
                return HttpResponse(echostr)
        elif request.method == 'POST':
            logRecord.log('POST method')
            msg = parse_message(request.body)
            global DOMAIN
            imageURL = DOMAIN + '/static/images/openDoor1.png'
            logRecord.log('msg.event : ' + msg.event)
            if msg.event == 'subscribe_scan':
                logRecord.log('subscribe_scan')
                branchID = msg.scene_id
                user = User()
                message = Message()
                isRegister = user.isRegister(msg.source)
                if isRegister:
                    openMessage = openDoor(branchID)
                    newUrl = ''
                    if openMessage == False:
                        reply = message.sendArticlesReply(newUrl, msg.source, imageURL, 1)
                    else:
                        reply = message.sendArticlesReply(newUrl, msg.source, imageURL, 0)
                    return HttpResponse(reply.render(), content_type="application/xml")
                user.registerStep1(msg.source,None,None)
                newUrl = DOMAIN + '/wx/registerByPhone?openID=' + msg.source + '&branchID=' + branchID
                reply = message.sendArticlesReply(newUrl,msg.source,imageURL,2)
                return HttpResponse(reply.render(), content_type="application/xml")
            elif msg.event == 'scan':
                branchID = msg.scene_id
                logRecord.log('branchID: ' + branchID)
                user = User()
                openInfo = user.login(msg.source)
                if openInfo['status'] == 0:
                    logRecord.log('scan  0')
                    newUrl = ''
                    message = Message()
                    openMessage = openDoor(branchID)
                    if openMessage == False:
                        reply = message.sendArticlesReply(newUrl, msg.source, imageURL, 1)
                    else:
                        reply = message.sendArticlesReply(newUrl, msg.source, imageURL, 0)
                    return HttpResponse(reply.render(), content_type="application/xml")
                elif openInfo['status'] == 2:
                    logRecord.log('scan  2')
                    newUrl = DOMAIN + '/wx/registerByPhone?openID=' + msg.source + '&branchID=' + branchID
                    message = Message()
                    reply = message.sendArticlesReply(newUrl, msg.source, imageURL, 2)
                    return HttpResponse(reply.render(), content_type="application/xml")
            else:
                logRecord.log('success')
                return HttpResponse('success')
    except Exception, e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        return HttpResponse('error')

@csrf_exempt
def openDoor(request):
    try:
        branchID = request.GET['branchID']
        doorID = request.GET['doorID']
        doorInfo = DoorInfo()
        doorMsg = doorInfo.insertDoorInfo(branchID,doorID)
        if doorMsg == 0:
            qrCode = QRCode()
            getMessage = qrCode.getQRCode(branchID)
            return HttpResponse(getMessage['message'])
        else:
            return HttpResponse(doorMsg)
    except Exception, e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        return render(request, 'error.html')
        

@csrf_exempt
def sendCode(request):
    try:
        logRecord = basic_log.Logger('record')
        sendCode = {}
        json2Dict = json.loads(request.body)
        phoneNumber = json2Dict['phoneNumber']
        message = Message()
        message.sendMessage(phoneNumber)
        sendCode = setStatus(0,'send success')
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        sendCode = setStatus(1,'send failed')
    logRecord.log('sendCode: ' + str(sendCode))
    return HttpResponse(json.dumps(sendCode), content_type='application/json')
    

@csrf_exempt
def registerByPhone(request):
    try:
        logRecord = basic_log.Logger('record')
        if request.method == 'POST':
            registerByPhone = {}
            phoneNumber = request.POST['phoneNumber']
            identityCode = request.POST['identityCode']
            openID = request.POST['openID']
            branchID = request.POST['branchID']
            doorInfo = DoorInfo()
            doorID = doorInfo.getDoorID(branchID)
            message = Message()
            flag = message.checkCode(phoneNumber,identityCode)
            if flag:
                user = User()
                isSuccess = user.registerStep3(openID,phoneNumber)
                if isSuccess:
                    global DOMAIN
                    url = DOMAIN + request.get_full_path()
                    sign = Sign(url)
                    WXconfig = sign.sign()
                    return render(request, 'uploadPic.html', {'WXconfig' : WXconfig,'openID': openID,'doorID' : doorID})
                else:
                    registerByPhone = setStatus(3,phoneNumber)
            else:
                registerByPhone = setStatus(2,phoneNumber)
            return render(request, 'registerHome.html', {'branchID' : branchID ,'openID': openID,'registerMessage':registerByPhone})
        else:
            openID = request.GET['openID']
            user = User()
            isRegister = user.isRegister(openID)
            if isRegister:
                logRecord.log('already register')
                return render(request, 'alreadyRegister.html')
            branchID = request.GET['branchID']
            form = RegisterForm()
            return render(request, 'registerHome.html', {'branchID' : branchID ,'openID': openID,'registerMessage':None})
    except Exception, e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        return render(request, 'error.html')


@csrf_exempt
def saveUserInfo(request):
    try:
        saveUserInfo = {}
        if request.method == 'POST':
            logRecord = basic_log.Logger('record')
            logRecord.log('request.body: ' + str(request.body))
            json2Dict = json.loads(request.body)
            mediaID = json2Dict['mediaID']
            openID = json2Dict['openID']
            user = User()
            userByPhone = user.updateUser(mediaID,openID)
            if userByPhone['status'] == 0:
                #开门API
                saveUserInfo = setStatus(0,'success')
            else:
                saveUserInfo = setStatus(2,userByPhone['message'])
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        saveUserInfo = setStatus(1,'save failed')
    logRecord.log('saveUserInfo: ' + str(saveUserInfo))
    return HttpResponse(json.dumps(saveUserInfo), content_type='application/json')


def registerSuccess(request):
    doorID = request.GET['doorID']
    return render(request, 'registerSuccess.html',{'doorID' : doorID})
    
    
def registerFailed(request):
    openID = request.GET['openID']
    doorID = request.GET['doorID']
    if 'reUpload' in request.GET:
        global DOMAIN
        url = DOMAIN + request.get_full_path()
        sign = Sign(url)
        WXconfig = sign.sign()
        return render(request, 'uploadPic.html',{'WXconfig' : WXconfig,'openID': openID,'doorID':doorID})
    else:
        return render(request, 'registerFailed.html',{'openID': openID,'doorID':doorID})


@csrf_exempt
def uploadFile(request):
    if request.method == 'GET':
        htmlTexts = []
        return render(request, 'ttt.html', {'htmlTexts': htmlTexts})
    elif request.method == 'POST':
        logRecord = basic_log.Logger('record')
        changNum = 45
        file = request.FILES['file']
        fileNameList = file.name.split('.')
        extendsName = fileNameList[len(fileNameList) - 1]
        uploadDate = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        filePath = __touchFile(file,str(uploadDate),extendsName)
        if extendsName == 'docx':
            doc = docx.Document(filePath)
            docTexts = ''.join([paragraph.text for paragraph in doc.paragraphs])
            docTexts = str(docTexts.replace(' ','').replace('\n',''))
            #docTexts = docTexts.decode('utf-8','ignore').encode('utf-8')
            docTexts = transformCodec(docTexts,'docx')
            htmlTexts = analyze(docTexts, changNum)
        elif extendsName == 'doc':
            docTexts = str(subprocess.check_output(['antiword', filePath]))
            docTexts = docTexts.replace(' ','').replace('\n','')
            docTexts = transformCodec(docTexts,None)
            htmlTexts = analyze(docTexts, changNum)
        else:
            pass
        result = {'htmlTexts':htmlTexts}
        return HttpResponse(json.dumps(result), content_type='application/json')


def analyze(docTexts,changNum):
    if (len(docTexts) < changNum):
        line = 1
    else:
        if (len(docTexts) % changNum == 0):
            line = len(docTexts) / changNum
        else:
            line = math.ceil(len(docTexts) / changNum)
    i = 0
    newTexts = []
    for docText in docTexts:
        if i >= line:
            break
        else:
            if i == 0:
                newTexts.append(docTexts[0:changNum])
            else:
                newTexts.append(docTexts[changNum * i:changNum * i + changNum - 1])
        i += 1
    return newTexts


def transformCodec(re_data,fileType):
    try:
        if fileType == 'doc':
            re_data = re_data.decode('utf-8','ignore')
        elif fileType == 'docx':
            re_data = re_data.decode('utf-8','ignore').encode('utf-8')
        else:
            re_data = re_data.decode('gb2312','ignore').encode('utf-8')
    except Exception as error:
        pos = re.findall(r'decodebytesinposition([\d]+)-([\d]+):illegal',str(error).replace(' ',''))
        if len(pos)==1:
            re_data = re_data[0:int(pos[0][0])]+re_data[int(pos[0][1]):]
            re_data = transformCodec(re_data,fileType)
    return re_data


def __touchFile(docFile,uploadDate,extendsName):
    filePath = '/home/work/temp/' + uploadDate + '.' + extendsName
    with open(filePath, 'wb+') as destination:
        for chunk in docFile.chunks():
            destination.write(chunk)
    os.chmod(filePath, stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)
    return filePath

def __removeFile(filePath):
    if filePath != None:
        if os.path.isfile(filePath):
            os.remove(filePath)
            return True
        else:
            return False