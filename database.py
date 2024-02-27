from datetime import datetime
from typing import List

from sqlmodel import Field, Relationship, SQLModel, create_engine


class Post(SQLModel, table=True):
    post_id: int = Field(default=None, primary_key=True)
    author: str = Field(foreign_key="user.user_id")
    title: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class User(SQLModel, table=True):
    user_id: str = Field(default=None, primary_key=True)
    password: str
    nickname: str
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class Comment(SQLModel, table=True):
    com_id: int = Field(default=None, primary_key=True)
    author_id: str = Field(default=None, foreign_key="user.user_id")
    post_id: str = Field(default=None, foreign_key="post.post_id")
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class Relationship(SQLModel):
    posts: List["Post"] = Relationship(back_populates="post", link_model=Post)
    users: List["User"] = Relationship(back_populates="user", link_model=User)
    comments: List["Comment"] = Relationship(
        back_populates="comment", link_model=Comment
    )


sqlite_file_name = "post.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)
