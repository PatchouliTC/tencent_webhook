from logging import info
import re

from typing import Dict,Any, Union
from fastapi import APIRouter,Request,Header
 
from app.const import robotmsgtemplate
from app.utils import respUtil,verifyUtil

from app.models.webhook import *
from app.models.db import models as dbtable

from app.helper import send_push_msg_to_robot
from app.service import dto,txgitcall

from utils import ConfigData
from utils.encrypt import encryption
from utils.logger import get_logger

from fastapi_sqlalchemy import db

router=APIRouter()
logger=get_logger(__name__)


@router.post("/webhook")
async def webhook_data_receive(request:Request,payload:Union[PushData,MergeData],x_token:str=Header(None)):
    logger.debug(f"receive data:{payload}")

    #check repo
    _repoid=payload.project_id if payload.object_kind==HookKind.Push else payload.object_attributes.target_project_id

    _repodata=payload.repository if payload.object_kind==HookKind.Push else payload.object_attributes.target

    _localrepo=dto.get_or_add_repo(_repoid,_repodata.dict(),add_when_not_exist=ConfigData.APP_CONFIG.AUTOADDUNKNOWNREPO)
    
    if _localrepo:
        if not _localrepo.verify_accesstoken(x_token):
            return respUtil.resp_401()

    #check branch
    _refname=None
    if payload.object_kind==HookKind.Push:
        _refname=re.search("[^/]+(?!.*/)",payload.ref).group(0)
    elif payload.object_kind==HookKind.Merge:
        _refname=payload.object_attributes.target_branch

    _branch=dto.get_or_add_branch(_localrepo,_refname)

    

    #check subimtter

    _subid=payload.user_id if payload.object_kind==HookKind.Push else payload.object_attributes.author_id
    _subname=payload.user_name if payload.object_kind==HookKind.Push else payload.user.name

    _submitter=dto.get_or_add_submitter({'name':_subname,'identityid':_subid},_subid)

    logger.debug(f"{_localrepo}\n{_branch}\n{_submitter}")

    #check_finish,Add data
    #------------------------------------------------------
    #Add PUSH Data
    if payload.object_kind==HookKind.Push:
        _pushrecord=dto.add_pushrecord_with_commits(payload.dict(),_submitter,_branch)

        accesstoken=_localrepo.accesstoken if not ConfigData.APP_CONFIG.DEVELOP else ConfigData.APP_CONFIG.ACCESSTOKEN

        diffdata,info=txgitcall.get_diff_info_reqest(_repoid,_pushrecord.before_hash,_pushrecord.current_hash,accesstoken)
        if diffdata:
            additions=0
            deletions=0
            for difffile in diffdata['diffs']:
                additions+=difffile['additions']
                deletions+=difffile['deletions']
            
            _pushrecord.additions=additions
            _pushrecord.deletions=deletions
            db.session.commit()

        comments_message = "\n".join([str(commit) for commit in payload.commits])
        send_push_msg_to_robot(-1,payload.user_name,payload.repository.name,comments_message)

        return respUtil.resp_200()

    #Add Merge Data
    elif payload.object_kind==HookKind.Merge:

        pass

    return respUtil.resp_200(payload="Finish")



    #验签
    # if ConfigData.APP_CONFIG.GITSECRETKEY:
    #     signature = request.headers.get('X-Gitlab-Token', '').split('=')[-1]
    #     token = encryption(request.body)
    #     if signature != token:
    #         logger.error('UnAuthorize hook request')
    #         return responsetemplate.resp_401()
    # if item.object_kind == 'merge_request':
    #   pass
    # msg=''
    # if item.object_kind=='push':
    #     comments_message = "\n".join([str(commit) for commit in item.commits])
    #     msg=robotmsgtemplate % (item.user_name,item.repository.name,comments_message)
    #     logger.debug(f"send msg=>{msg}")
    #     if not send_msg_to_robot(msg):
    #         logger.error("Unable send msg to robot")
    #     return {'response':msg}
    return {'response':'ok'}
