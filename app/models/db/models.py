import datetime
from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.types import TIMESTAMP

from . import Base

#repo
class Repository(Base):
    __tablename__='repositories'
    id=Column(Integer,primary_key=True,index=True)

    name=Column(String(256),default="UnKnownRepo")
    description=Column(String,default="")
    visable_level=Column(Integer,default=10) #0=private 10=public
    repoid=Column(Integer,nullable=False)
    reponamespace=Column(String)
    url=Column(String)
    accesstoken=Column(String)

    branches=relationship("RepoBranch",backref="repo",cascade='all,delete-orphan')
    
    def __repr__(self):
        return f"Repo{self.name}({'Public' if self.visable_level > 0 else 'Private'})\n[{self.url}]"

#repo-branch
class RepoBranch(Base):
    __tablename__='repobranches'
    id=Column(Integer,primary_key=True,index=True)

    repo_id=Column(Integer,ForeignKey('repositories.id',ondelete='CASCADE'))
    #repo

    name=Column(String)

    pushes=relationship("PushInfo",backref="branch",cascade='all,delete-orphan')

    def __repr__(self):
        return f"{'[%s]' % self.repo.name if self.repo else ''} - {self.name}"

#hook user data save
class Operator(Base):
    __tablename__='operators'
    id=Column(Integer,primary_key=True,index=True)
    userid=Column(Integer,nullable=False)#locate remote
    name=Column(String,default="Unknown")

    pushes=relationship("PushInfo",backref="operator",cascade='all,delete-orphan')


    def __repr__(self):
        return f"<{self.name}>"



#push info
class PushInfo(Base):
    __tablename__='pushinfos'
    id=Column(Integer,primary_key=True,index=True)
    #操作人
    op_id=Column(Integer,ForeignKey('operators.id',ondelete='CASCADE'))
    #operator

    #指向分支
    branch_id=Column(Integer,ForeignKey('repobranches.id',ondelete='CASCADE'))
    #branch

    #本次提交的hash
    currnet_hash=Column(String(64),nullable=False)
    #前一次提交的hash
    before_hash=Column(String(64),nullable=False)

    additions=Column(BigInteger,default=-1)
    deletions=Column(BigInteger,default=-1)

    push_at=Column(DateTime,nullable=False,default=datetime.datetime.now())

    commits=relationship("Commit",backref="pushinfo",cascade='all,delete-orphan')

    def __repr__(self):
        return f"[{self.operator.name}]-P->({self.branch.name})({self.push_at.strftime('%Y-%m-%d %H:%M:%S')})"

#push commit list
class Commit(Base):
    __tablename__='commits'
    id=Column(Integer,primary_key=True,index=True)

    push_id=Column(Integer,ForeignKey('pushinfos.id',ondelete='CASCADE'))
    #pushinfo

    remoteid=Column(String(128),nullable=False)
    message=Column(String)

    commit_at=Column(DateTime)

# class MergeInfo(Base):
#     __tablename__='mergeinfos'
#     id=Column(Integer,primary_key=True,index=True)
#     repo_id=Column(Integer,ForeignKey('repositories.id',ondelete='CASCADE'))
#     #repo