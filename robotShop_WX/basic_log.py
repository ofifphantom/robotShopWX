import logging
import logging.config
import os
import datetime
import time
from logging.handlers import TimedRotatingFileHandler

class Logger:
    def __init__(self, logName):
        logging.config.fileConfig('/home/work/robotShopWX/robotShop_WX/log_config.py')
        self.logName = logName
        if logName == "error":
            self.__logger = logging.getLogger('error')
        elif logName == "record":
            self.__logger = logging.getLogger('record')

    def log(self, msg):
        if self.__logger is not None:
            self.__logger.info(msg)

    def normalLog(self, msg):
        if self.__logger is not None:
            self.__logger.info(msg)

    def errorLog(self, msg):
        if self.__logger is not None:
            self.__logger.exception('msg:%s', msg)

