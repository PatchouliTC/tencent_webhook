from pydantic import BaseSettings
import logging

class AppSettings(BaseSettings):
    APP_NAME:str='WebHookApiServer'
    HOST:str='0.0.0.0'
    PORT:int=5005
    DEBUGMODE:bool=False
    DEVELOP:bool=False
    ROBOTHOOKURL:str=None
    SQL_URL:str=None
    GITSECRETKEY:str=None
    
    #FOR DEVELOP
    IDENTITYPWD:str=123456
    ACCESSTOKEN:str=None
    SENDTIME:str=None
    TEMPLATESTATSTR:str="""
-----PUSH STAT( %s )-----
```
%s
```"""
    TEMPLATEPUSHSTR:str="""# %s 提交（%s）

  WHAT'S NEW:

  ```
  %s
  ```"""

    #auto add unknown repo?
    AUTOADDUNKNOWNREPO:bool=False

    LOG_ROOT:str=APP_NAME
    LOG_LEVEL:int=logging.DEBUG
    LOG_FILE_ROOT_PATH:str='logs'

    class Config:
        case_sensitive=True
        env_file='AppSettings'
        env_encoding='utf-8'