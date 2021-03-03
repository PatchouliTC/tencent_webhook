from app.models.db.models import Submitter
import requests
from app import logger
tencent_git_url="http://git.code.tencent.com"

#差异比较
diff_detail_url=f"{tencent_git_url}/api/v3/projects/:id/repository/compare"

#获取分支列表
get_branches_url=f"{tencent_git_url}/api/v3/projects/:id/repository/branches"

get_repo_events=f"{tencent_git_url}/api/v3/projects/:id/events"

def get_diff_info_reqest(repoid:int,old:str,new:str,accesstoken:str,timeout:int=3):
    if not accesstoken:
        return None,"No accesstoken"
    headers={'PRIVATE-TOKEN':accesstoken}
    params={"from":old,"to":new}
    try:
        req=requests.get(diff_detail_url.replace(":id",str(repoid),1),headers=headers,params=params,timeout=timeout)
        return req.json(),"success"
    except Exception as e:
        logger.error(f"Unable get diff info,{str(e)}")
        return None,str(e)

def get_branch_list(repoid:int,accesstoken:str,timeout:int=3):
    if not accesstoken:
        return None,"No accesstoken"
    headers={'PRIVATE-TOKEN':accesstoken}
    try:
        req=requests.get(get_branches_url.replace(":id",str(repoid),1),headers=headers,timeout=timeout)
        return req.json(),"success"
    except Exception as e:
        logger.error(f"Unable get branches list,{str(e)}")
        return None,str(e)


