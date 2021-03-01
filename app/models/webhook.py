"""
    面向HOOK的数据模型验证
"""
from pydantic import BaseModel,ValidationError, validator,Field
from datetime import datetime
from typing import List, Optional

from .commontype import *

class CommonData(BaseModel):
    object_kind:HookKind

    @validator("object_kind")
    def valid_operator_can_be_used(cls, v):
        return HookKind.from_str(v)

    def __str__(self):
        return f"Hook_Mode:{self.object_kind}"
    
    class Config:
        use_enum_values = True
        allow_population_by_field_name=True


class Author(BaseModel):
    name:str

class Repository(BaseModel):
    name:str
    url:Optional[str]=Field(..., alias="homepage")
    visibility_level:int
    namespace:Optional[str]

    @validator('namespace', pre=True, always=True, whole=True)
    def check_homepage_or_namespace(cls, namespace, values):
        if not values.get('url') and not namespace:
            raise ValueError('either homepage(url) or namespace is required')
        return namespace

class Commit(BaseModel):
    remoteid:str=Field(..., alias="id")
    message:str
    url:str
    author:Author
    commit_at:datetime=Field(..., alias="timestamp")

class MergeInfo(BaseModel):
    id:int

    target_branch:str
    source_branch:str
    source_project_id:int
    target_project_id:int

    author_id:int
    title:str

    create_at:datetime
    update_at:datetime

    state:str
    merge_status:str

    source:Repository
    target:Repository

    url:str

    action:str
    extension_action:str

class PushData(CommonData):
    """
        PUSH操作数据模型
    """
    operation_kind:str
    action_kind:str
    before_hash:str=Field(..., alias="before")
    current_hash:str=Field(..., alias="after")
    ref:str
    user_name:str
    user_id:int
    project_id:int
    repository:Repository
    commits:List[Commit]
    total_commits_count:int

class MergeData(CommonData):
    """
        Merge操作数据模型
    """
    user:Author
    object_attributes:MergeInfo