import hashlib
from datetime import datetime
from typing import List

from sqlmodel import (Field, Relationship, Session, SQLModel, create_engine,
                      select)


class Post(SQLModel, table=True):
    post_id: int = Field(default=None, primary_key=True)
    author: str
    title: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class User(SQLModel, table=True):
    user_id: str = Field(primary_key=True)
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


def insert(author: str, title: str, content: str):
    with Session(engine) as session:
        data = Post(author=author, title=title, content=content)
        session.add(data)
        session.commit()


def select_one(id: int):
    with Session(engine) as session:
        return session.get(Post, id)


def select_all(page: int) -> list[Post]:
    data = []
    with Session(engine) as session:
        offset = (page - 1) * 100
        results = session.exec(select(Post).offset(offset).limit(100)).all()
        for res in results:
            res_dict = {
                "post_id": res.post_id,
                "title": res.title,
                "author": res.author,
                "content": res.content,
                "created_at": res.created_at,
            }
            data.append(res_dict)
    return data


def update(id: int, author: str, title: str, content: str):
    with Session(engine) as session:
        res = session.get(Post, id)
        res.author = author
        res.title = title
        res.content = content
        session.add(res)
        session.commit()
        session.refresh(res)
    return session.get(Post, id)


def delete(id: int):
    with Session(engine) as session:
        res = session.get(Post, id)
        session.delete(res)
        session.commit()


def add_user(user_id: str, password: str, nickname: str):
    uppercase_count = sum(1 for word in password if word.isupper())
    if len(password) < 8 or uppercase_count == 0:
        raise ValueError
    with Session(engine) as session:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        data = User(user_id=user_id, password=hashed_password, nickname=nickname)
        session.add(data)
        session.commit()


def add_comment(author_id: str, post_id: str, content: str):
    with Session(engine) as session:
        data = Comment(author_id=author_id, post_id=post_id, content=content)
        session.add(data)
        session.commit()
