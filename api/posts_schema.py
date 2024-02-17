from typing import Dict, List
from pydantic import BaseModel, Field
from sqlmodel import Field, SQLModel
from datetime import datetime

class RequestBody(BaseModel):
    author: str
    title: str
    content: str

class ResponseModel(BaseModel):
    message: str = Field(example="성공")
    data: BaseModel

class Content(BaseModel, SQLModel, table=True):
    post_id: int = Field(default=None, primary_key=True)
    author: str
    title: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

class ContentDict(ResponseModel):
    data: Content

class ResponseListModel(BaseModel):
    message: str = Field(example="성공")
    data: BaseModel

class ContentList(ResponseListModel):
    data: List[Content]