from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


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


class ResponseMessageModel(BaseModel):
    message: str = Field(example="성공")


class RequestUserBody(BaseModel):
    user_id: str
    password: str
    nickname: str
