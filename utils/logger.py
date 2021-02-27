import os
import logging
from logging.handlers import TimedRotatingFileHandler
from . import ConfigData as CD

def init_logging(logname:str=CD.APP_CONFIG.LOG_ROOT,level:int=CD.APP_CONFIG.LOG_LEVEL,filepath:str=None):
    logger = logging.getLogger(logname)
    logger.setLevel(level)
    logger.handler=[]
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt='[%(asctime)s][%(levelname)s]<%(name)s> %(message)s',
        datefmt='%I:%M:%S'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    if filepath is not None:
        file_dir = os.path.split(filepath)[0]
        if not os.path.isdir(file_dir):
            os.makedirs(file_dir)
        fhandler=TimedRotatingFileHandler(filename=filepath,encoding='utf-8',when='d',interval=1,backupCount=90)
        fhandler.setFormatter(formatter)
        logger.addHandler(fhandler)
    return logger

def set_logger_level(logname:str=CD.APP_CONFIG.LOG_ROOT,level:int=CD.APP_CONFIG.LOG_LEVEL):

    logging.getLogger(logname).setLevel(level)

def get_logger(name:str=CD.APP_CONFIG.LOG_LEVEL):
    logger = logging.getLogger(name)
    return logger