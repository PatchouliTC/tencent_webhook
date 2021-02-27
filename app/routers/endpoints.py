from typing import Dict,Any
from fastapi import APIRouter,Request
from fastapi.responses import HTMLResponse,FileResponse

from app import templates,logger 
from app.models.webhook import HookItem,commitsdata
from app.const import robotmsgtemplate
from app.helper import send_msg_to_robot
from app.utils import responsetemplate

from utils import ConfigData
from utils.encrypt import encryption

router=APIRouter()

@router.get("/",response_class=HTMLResponse,deprecated=False)
async def index(request:Request):
    return templates.TemplateResponse('index.html',{"request":request})

@router.post("/start",deprecated=True)
async def run_start(item:Dict[str,Any]):
    if 'comm'in item:
        return {'response':200,
        'text':item['comm']
        }
    else:
        return {'response':200,
        'text':'No Comm Find'}

@router.get("/assets/{filepath}",deprecated=True)
async def send_static_file(filepath:str):
    #return FileResponse(filepath)
    pass

@router.get("/__exit",deprecated=True)
async def exit():
    # cmd = "bash ~/{proj}boot.sh"
    # code = os.system(cmd)
    pass

@router.post("/webhook")
async def webhook_data_receiver(request:Request,item:HookItem):
    logger.debug(f"receive data:{item}")

    #验签
    # if ConfigData.APP_CONFIG.GITSECRETKEY:
    #     signature = request.headers.get('X-Gitlab-Token', '').split('=')[-1]
    #     token = encryption(request.body)
    #     if signature != token:
    #         logger.error('UnAuthorize hook request')
    #         return responsetemplate.resp_401()
    # if item.object_kind == 'merge_request':
    #   pass
    msg=''
    if item.object_kind=='push':
        comments_message = "\n".join([str(commit) for commit in item.commits])
        msg=robotmsgtemplate % (item.user_name,item.repository.name,comments_message)
        logger.debug(f"send msg=>{msg}")
        if not send_msg_to_robot(msg):
            logger.error("Unable send msg to robot")
        return {'response':msg}
    return {'response':'ok'}


