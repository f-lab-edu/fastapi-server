from datetime import datetime

from sqlmodel import Field, Session, SQLModel, create_engine, select


class Post(SQLModel, table=True):
    post_id: int = Field(default=None, primary_key=True)
    author: str
    title: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


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


def select_all() -> list[Post]:
    data = []
    with Session(engine) as session:
        results = session.exec(select(Post)).all()
        data = session.get(Post, id)
        print(data)
        print(type(data))
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
