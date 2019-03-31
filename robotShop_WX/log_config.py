[loggers]
keys=record,root,error

[logger_record]
handlers=recordFile
level=NOTSET
qualname=record

[logger_error]
handlers=errorFile
level=NOTSET
qualname=error

[logger_root]
qualname=root
level=NOTSET
handlers=


[formatters]
keys=simple,normal,logtemps

[formatter_simple]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s

[formatter_normal]
format=%(asctime)s - %(name)s - %(levelname)s - %(module)s : %(lineno)d - %(message)s

[formatter_logtemps]
format=%(asctime)s %(name)s %(levelname)s %(message)s

[handlers]
keys=recordFile,errorFile

[handler_recordFile]
class=handlers.TimedRotatingFileHandler
backupCount=0
formatter=normal
level=INFO
args=('/home/work/log/records/record', 'midnight', 1)  
suffix='%Y_%m_%d_record.log'
interval=1

[handler_errorFile]
class=handlers.TimedRotatingFileHandler
backupCount=0
formatter=normal
level=INFO
args=('/home/work/log/errors/error', 'midnight', 1)
suffix='%Y_%m_%d_error.log'
interval=1