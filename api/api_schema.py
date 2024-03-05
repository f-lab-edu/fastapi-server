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

class UserBody(BaseModel):
    password: str
    nickname: str

class UserConent(BaseModel):
    user_id: str
    password: str
    nickname: str

class ResponseUser(BaseModel):
    message: str = Field(example="성공")
    data: UserConent

class Comment(BaseModel):
    com_id: int
    author_id: str
    post_id: int
    content: str
    created_at: datetime

class CommentBody(BaseModel):
    com_id: int
    author_id: str
    post_id: int
    content: str

class CommentConent(BaseModel):
    content: str


class ResponseComment(BaseModel):
    message: str = Field(example="성공")
    data: CommentConent


class ResponseComList(BaseModel):
    message: str = Field(example="성공")
    data: List[Comment]
