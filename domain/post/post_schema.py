import datetime

from pydantic import BaseModel

class Item(BaseModel):
    post_id: int
    author: str
    title: str
    content: str
    created_at: datetime.datetime