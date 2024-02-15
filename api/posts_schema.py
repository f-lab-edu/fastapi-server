from typing import Dict, List
from pydantic import BaseModel, Field
import datetime

class RequestBody(BaseModel):
    author: str
    title: str
    content: str

class ResponseModel(BaseModel):
    message: str = Field(example="성공")
    data: BaseModel

class Content(BaseModel):
    post_id: int
    author: str
    title: str
    content: str
    created_at: datetime.datetime

class ContentDict(ResponseModel):
    data: Content

class ResponseListModel(BaseModel):
    message: str = Field(example="성공")
    data: BaseModel

class ContentList(ResponseListModel):
    data: List[Content]