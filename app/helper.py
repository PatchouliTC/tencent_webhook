import requests
from utils import ConfigData
from . import logger
from app.models.db.models import *
from fastapi_sqlalchemy import db
from app.service import dto

def send_stat_msg_to_robot(receiverid:int):
    msgtemplate=ConfigData.APP_CONFIG.TEMPLATESTATSTR
    if ConfigData.APP_CONFIG.DEVELOP:
        targeturl=ConfigData.APP_CONFIG.ROBOTHOOKURL
        
    else:
        receiver=db.session.query(NoticeReceiver).filter(NoticeReceiver.id==receiverid).first()
        if not receiver or not receiver.url:
            return False

        targeturl=receiver.url

    logger.debug(f'start plan for {receiverid}...')
    #For develop , default get all sub data
    today=datetime.date.today() 
    oneday=datetime.timedelta(days=1) 
    yesterday=today-oneday  
    data=None
    with db():
        _submitters=db.session.query(Submitter).all()
        data=dto.get_stats_info(_submitters,yesterday)
    logger.debug(data)
    
    format_message=""

    for sub in data:
        format_message+=f"\nSubmitter[{sub['submitter']}]=>\n"
        if len(sub['detail'])>0:
            format_message+="\n".join([f"--Repo:<{item['reponame']}>: +{item['additions']} lines -{item['deletions']} lines {item['subcount']} submits\n" for item in sub['detail']])
        else:
            format_message+="--No Push--\n"

    sendmsg={'msgtype': 'text', 'text': {'content': msgtemplate % (yesterday.strftime("%Y-%m-%d"),format_message)}}
    logger.debug(sendmsg)
    #print(msgtemplate % (yesterday.strftime("%Y-%m-%d"),format_message))
    try:
        req=requests.post(targeturl,json=sendmsg,timeout=3)
        logger.debug(f"state:{req.status_code},info:{req.reason},data:{req.text}")
        return True
    except Exception as e:
        logger.error(f"post msg to robot failed,{str(e)}")
        return False      



def send_push_msg_to_robot(receiverid:int,subname,reponame,msg):

    msgtemplate=ConfigData.APP_CONFIG.TEMPLATEPUSHSTR
    if ConfigData.APP_CONFIG.DEVELOP:
        targeturl=ConfigData.APP_CONFIG.ROBOTHOOKURL
        
    else:
        receiver=db.session.query(NoticeReceiver).filter(NoticeReceiver.id==receiverid).first()
        if not receiver or not receiver.url:
            return False

        targeturl=receiver.url


    if msg and ConfigData.APP_CONFIG.ROBOTHOOKURL:
        sendmsg={'msgtype': 'text', 'text': {'content': msgtemplate % (subname,reponame,msg)}}
        logger.debug(f"send push msg{sendmsg}")
        #print(msgtemplate % (subname,reponame,msg))
        try:
            req=requests.post(targeturl,json=sendmsg,timeout=3)
            logger.debug(f"state:{req.status_code},info:{req.reason},data:{req.text}")
            return True
        except Exception as e:
            logger.error(f"post msg to robot failed,{str(e)}")
            return False



