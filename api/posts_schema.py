from typing import Dict, List
from pydantic import BaseModel, Field
from datetime import datetime

class RequestBody(BaseModel):
    author: str
    title: str
    content: str

class Content(BaseModel):
    post_id: int
    author: str
    title: str
    content: str
    created_at: datetime

class ResponseModel(BaseModel):
    message: str = Field(example="성공")
    data: Content

class ResponseListModel(BaseModel):
    message: str = Field(example="성공")
    data: List[Content]

class ResponseBoolModel(BaseModel):
    message: str = Field(example="성공")
    data: bool