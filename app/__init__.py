import os

from fastapi import FastAPI,Request,responses
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi_sqlalchemy import db
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
import uvicorn

from utils import ConfigData as CD, config
from utils.logger import init_logging

from app.utils import respUtil

#记录server目录路径供未来使用
SERVER_ROOT_PATH:str=os.path.abspath(os.path.dirname(__file__))

#定义日志组件-非uvicorn
logger=init_logging(logname=__name__,level=CD.APP_CONFIG.LOG_LEVEL,filepath=os.path.join(CD.APP_CONFIG.LOG_FILE_ROOT_PATH,__name__,'log.log'))

#生产环境注销API接口文档
if CD.APP_CONFIG.DEVELOP:
    app=FastAPI()
else:
    app=FastAPI(docs_url=None,redoc_url=None)

#挂载static目录
app.mount("/static",StaticFiles(directory="app/static"),name='static')

#定义页面模板目录
templates=Jinja2Templates(directory='app/wtatic/templates')

#启动服务
def start_server():
    if CD.APP_CONFIG.DEBUGMODE:
        _app=create_server()
        logger.info(f'Note:Running at debug mode')
    else:
        _app=create_server()
    uvicorn.run(app=_app,host=CD.APP_CONFIG.HOST,port=CD.APP_CONFIG.PORT,debug=CD.APP_CONFIG.DEBUGMODE)

#创建APP，相关围绕APP关联内容处理
def create_server():

    app.add_middleware(DBSessionMiddleware,db_url=CD.APP_CONFIG.SQL_URL)
    from .routers import endpoints
    from .routers import hookend

    app.include_router(
        endpoints.router,
        responses={404: {'info':'Not Found'}}
    )
    app.include_router(
        hookend.router,
        tags=['WebHookCallbacks'],
        responses={404: {'info':'No such webhook endpoint'}}
    )
    return app

@app.on_event('startup')
async def startup_event():
    pass
    # from .models.db.models import Repository
    # repos=db.session.query(Repository).all()
    # for r in repos:
    #     print(r)


def global_exception_handler(app:FastAPI)->None:

    @app.exception_handler(Exception)
    async def basic_exception_handler(request:Request,exc:Exception):
        """全局异常捕获,其他细节异常捕获写在此捕获上方位置

        Args:
            request (Request): 关联请求
            exc (Exception): 异常信息
        """
        logger.error(f"Exception happened at {request.method} on {request.url}\nheaders:{request.headers}\nException info:{str(exc)}")
        return responsetemplate.resp_500()
