from enum import unique
import datetime
from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.types import TIMESTAMP

from app.utils import verifyUtil

from . import Base


class Repository(Base):
    __tablename__='repositories'
    id=Column(Integer,primary_key=True,index=True)

    identityid=Column(Integer,nullable=False,unique=True)

    name=Column(String(256),default="UnKnownRepo",nullable=False)
    displayname=Column(String(256),default="UndefinedRepo")

    visibility_level=Column(Integer,default=0) #0=private 10=public

    namespace=Column(String(512),index=True)
    url=Column(String)

    accesstoken=Column(String)
    verifytoken=Column(String)

    branches=relationship("Branch",backref="repo",cascade='all,delete-orphan')
    merges=relationship("MergeRecord",backref="repo",cascade='all,delete-orphan')

    watcher=relationship('NoticeReceiver',secondary='repos_recvs')
    submitters=relationship('Submitter',secondary='repos_subs')
    

    def verify_accesstoken(self,token) -> bool:
        if self.verifytoken and len(self.verifytoken)>0:
            return verifyUtil.verify_hook_token(token,self.accesstoken)
        return True

    def __repr__(self):
        return f"Repo:<{self.name}>({'Public' if self.visibility_level > 0 else 'Private'})\n[{self.url}]"

class Branch(Base):
    __tablename__='branches'
    id=Column(Integer,primary_key=True,index=True)

    repo_id=Column(Integer,ForeignKey('repositories.id',ondelete='CASCADE'))
    #repo

    name=Column(String)

    pushes=relationship("PushRecord",backref="branch",cascade='all,delete-orphan')
    merges=relationship("MergeRecord",backref="branch",cascade='all,delete-orphan')

    def __repr__(self):
        return f"Branch:{'[%s]' % self.repo.name if self.repo else ''} - {self.name}"

class Submitter(Base):
    __tablename__='submitters'
    id=Column(Integer,primary_key=True,index=True)

    identityid=Column(Integer,nullable=False)#locate remote

    displayname=Column(String(256),default="UnDefinedSubmitter")
    name=Column(String(256),nullable=False,index=True)

    pushes=relationship("PushRecord",backref="submitter",cascade='all,delete-orphan')
    merges=relationship("MergeRecord",backref="submitter",cascade='all,delete-orphan')

    associate_repos=relationship('Repository',secondary='repos_subs')

    def __repr__(self):
        return f"<{self.displayname}>[{self.name}]"



#push info
class PushRecord(Base):
    __tablename__='pushrecords'
    id=Column(Integer,primary_key=True,index=True)
    #操作人
    sub_id=Column(Integer,ForeignKey('submitters.id',ondelete='CASCADE'))
    #submitter

    #指向分支
    branch_id=Column(Integer,ForeignKey('branches.id',ondelete='CASCADE'))
    #branch

    #本次提交的hash
    current_hash=Column(String(64),index=True)
    #前一次提交的hash
    before_hash=Column(String(64))

    additions=Column(BigInteger,default=0)
    deletions=Column(BigInteger,default=0)


    push_at=Column(DateTime,nullable=False,default=datetime.datetime.now(),index=True)

    commits=relationship("Commit",backref="pushrecord",cascade='all,delete-orphan')

    def __repr__(self):
        return f"[{self.submitter.name}]-P->({self.branch.name})({self.push_at.strftime('%Y-%m-%d %H:%M:%S')})"
#push commit list
class Commit(Base):
    __tablename__='commits'
    id=Column(Integer,primary_key=True,index=True)

    push_id=Column(Integer,ForeignKey('pushrecords.id',ondelete='CASCADE'))
    #pushrecord

    remoteid=Column(String(64),nullable=False,index=True)

    message=Column(String)

    url=Column(String(256))

    commit_at=Column(DateTime)

class MergeRecord(Base):
    __tablename__='mergerecords'
    id=Column(Integer,primary_key=True,index=True)

    remoteid=Column(String(64),nullable=False,unique=True)
    url=Column(String(512))
    snap_source_branch_name=Column(String(256))
    snap_source_repo_namespace=Column(String(256))
    snap_sub_name=Column(String(256),index=True)

    sub_id=Column(Integer,ForeignKey('submitters.id',ondelete='CASCADE'))
    #submitter
    target_branch_id=Column(Integer,ForeignKey('branches.id',ondelete='CASCADE'))
    #branch
    happened_repo_id=Column(Integer,ForeignKey('repositories.id',ondelete='CASCADE'))
    #repo

    title=Column(String(256))

    current_merge_state=Column(String(64))
    current_state=Column(String(64))

    create_at=Column(DateTime,index=True)
    update_at=Column(DateTime)

    merges=relationship("MergeLog",backref="merge",cascade='all,delete-orphan')
class MergeLog(Base):
    __tablename__='mergelogs'
    id=Column(Integer,primary_key=True,index=True)

    merge_id=Column(Integer,ForeignKey('mergerecords.id',ondelete='CASCADE'))
    #merge

    current_merge_state=Column(String(64))
    current_state=Column(String(64))

    action=Column(String(32),index=True)
    extension_action=Column(String(32))

    record_at=Column(DateTime,index=True)

    __table_args__ = (Index('action_at_index', "action", "record_at"), )

class NoticeReceiver(Base):
    __tablename__='noticereceivers'
    id=Column(Integer,primary_key=True,index=True)

    name=Column(String(256),default='UndefinedReceiver',nullable=False,index=True)
    
    url=Column(String(256))

    stats_send_at=Column(String(64))

    token=Column(String(256))

    watchingrepos=relationship('Repository',secondary='repos_recvs')

class RepoRecv(Base):
    __tablename__='repos_recvs'
    id=Column(Integer,primary_key=True,index=True)

    repo_id=Column(Integer,ForeignKey('repositories.id',ondelete='CASCADE'))
    recv_id=Column(Integer,ForeignKey('noticereceivers.id',ondelete='CASCADE'))

    activate=Column(Boolean,default=True)

class RepoSub(Base):
    __tablename__='repos_subs'
    id=Column(Integer,primary_key=True,index=True)

    repo_id=Column(Integer,ForeignKey('repositories.id',ondelete='CASCADE'))
    sub_id=Column(Integer,ForeignKey('submitters.id',ondelete='CASCADE'))
