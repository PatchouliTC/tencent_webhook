import requests
from utils import ConfigData
from . import logger

def send_msg_to_robot(msg,timeout:int=5):
    """发送消息给目标机器人

    Args:
        msg (str): 消息内容
        timeout (int, optional): 连接超时时间. Defaults to 5.

    Returns:
        bool: 发送是否成功
    """
    if msg and ConfigData.APP_CONFIG.ROBOTHOOKURL:
        sendmsg={'msgtype': 'text', 'text': {'content': msg}}
        try:
            req=requests.post(ConfigData.APP_CONFIG.ROBOTHOOKURL,json=sendmsg,timeout=timeout)
            logger.debug(f"state:{req.status_code},info:{req.reason},data:{req.text}")
            return True
        except Exception as e:
            logger.error(f"post msg to robot failed,{str(e)}")
            return False

