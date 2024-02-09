from pydantic import BaseModel

import datetime

class Item(BaseModel):
    post_id: int
    author: str
    title: str
    content: str
    created_at: datetime.datetime

class RequestBody(BaseModel):
    author: str
    title: str
    content: str

class ResponseModel(BaseModel):
    code: str
    data: str