from pydantic import BaseModel
from typing import List

class CommitsData(BaseModel):
    message:str
    url:str
    def __str__(self):
        return f"{self.message}\n({self.url})\n"

class repository(BaseModel):
    name:str

class HookItem(BaseModel):
    user_name:str
    object_kind:str
    repository:repository
    commits:List[CommitsData]
