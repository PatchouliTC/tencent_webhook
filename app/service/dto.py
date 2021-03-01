from datetime import datetime as dtime

from sqlalchemy import func,case,inspect,and_,or_

from app.models.db import *


from fastapi_sqlalchemy import db

from utils import ConfigData

def get_or_add_repo(identityid:int=0,repodata:dict=None,add_when_not_exist:bool=False)->Repository:
    if identityid<=0 and not repodata:
        raise ValueError("no id and repodata give---can't find or add repo")
    _repo=None
    if identityid>0:
    #检查本地是否有该存储库记录
        _repo=db.session.query(Repository).filter(
            Repository.identityid==identityid
        ).first()
        if _repo:
            return _repo
    
    if add_when_not_exist:   
            _newrepo=Repository(**repodata)
            _newrepo.identityid=identityid
            db.session.add(_newrepo)
            db.session.commit()
            _repo=_newrepo
    return _repo

def get_or_add_branch(repo:Repository,name:str)->Branch:
    if not repo or not name:
        raise ValueError("Can't add no depend repo branch")
    _branch=None
    if name:
        _branch=db.session.query(Branch).filter(
            Branch.repo_id==repo.id,
            Branch.name==name
        ).first()
        if _branch:
            return _branch
    
    _newbranch=Branch(**{'name':name})
    repo.branches.append(_newbranch)
    db.session.commit()
    return _newbranch

def get_or_add_submitter(submitter:dict,identityid:int=0,name:str=None)->Submitter:
    if not name and identityid<=0 and not submitter:
        raise ValueError("Can't find or and submitter--no avilable data")

    if name or identityid>0:
        conditions=[]
        if identityid>0:
            conditions.append(or_(Submitter.identityid==identityid))
        if name:
            conditions.append(or_(Submitter.name==name))
        _submitter=db.session.query(Submitter).filter(*conditions).first()
        if _submitter:
            return _submitter
    
    _newsubmitter=Submitter(**submitter)
    if identityid>0:
        _newsubmitter.identityid=identityid
    if name:
        _newsubmitter.name=name
    _newsubmitter.displayname=_newsubmitter.name
    db.session.add(_newsubmitter)
    db.session.commit()
    return _newsubmitter

def add_pushrecord_with_commits(data:dict,submitter:Submitter,branch:Branch):
    if not data or not "current_hash" in data or not data['current_hash']:
        return ValueError("No enough data to add")

    resault=db.session.query(
        exists().where(PushRecord.current_hash==data['current_hash'])
    ).scalar()
    if not resault:
        _newpushrecord=PushRecord()
        _newpushrecord.current_hash=data['current_hash']
        _newpushrecord.before_hash=data['before_hash']
        _newpushrecord.push_at=dtime.now()
        submitter.pushes.append(_newpushrecord)
        branch.pushes.append(_newpushrecord)
        #add commits to this pushreocrd
        for commit in data['commits']:
            commit.pop("author",None)
            _newcommit=Commit(**commit)
            _newpushrecord.commits.append(_newcommit)
        
        db.session.commit()
        return _newpushrecord
    
    raise ValueError("target push already exists")
    

def get_stats_info(submitters:Submitter,date):
    stats=[]
    for sub in submitters:
        _stat=db.session.query(Repository.name.label("reponame"),
            func.sum(PushRecord.additions).label("additions"),
            func.sum(PushRecord.deletions).label("deletions"),
            func.count(PushRecord.id).label("subcount")).select_from(Repository).join(
                Repository.branches
            ).join(
                Branch.pushes
            ).join(
                Submitter,PushRecord.sub_id==Submitter.id
            ).filter(
                Submitter.identityid==sub.identityid,
                func.date(PushRecord.push_at) == date
            ).group_by(Repository.id)

        _statformat=[]
        for i in _stat:
            _statformat.append({ c: getattr(i, c) for c in i._fields })
        stats.append({'submitter':sub.name,'detail':_statformat})
    return stats
    



    