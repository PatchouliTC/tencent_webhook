from typing import Dict,Any
from fastapi import APIRouter,Request
from fastapi.responses import HTMLResponse,FileResponse

from app import templates,logger 
from app.models.backend import HookItem,CommitsData
from app.const import robotmsgtemplate
from app.utils import respUtil

from utils import ConfigData
from utils.encrypt import encryption
from utils.logger import get_logger

router=APIRouter()

logger=get_logger(__name__)

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




