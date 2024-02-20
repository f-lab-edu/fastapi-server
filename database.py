from sqlmodel import create_engine, SQLModel, Field, Session, select
from datetime import datetime


class Posts(SQLModel, table=True):
    post_id: int = Field(default=None, primary_key=True)
    author: str
    title: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

sqlite_file_name = "posts.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

def insert(author: str, title: str, content: str) -> bool:
    data = Posts(author=author, title=title, content=content)
    if not data:
        return False
    
    with Session(engine) as session:
        session.add(data)
        session.commit()
        return True

def select_one(id: int) -> dict:
    result_dict = {}
    with Session(engine) as session:
        result = session.exec(select(Posts).where(Posts.post_id == id))
        res = result.one()
        result_dict = {"post_id" : res.post_id, 
                        "title" : res.title,
                        "author" : res.author,
                        "content" : res.content,
                        "created_at" : res.created_at}
    return result_dict

def select_all() -> list:
    data = []
    with Session(engine) as session:
        results = session.exec(select(Posts)).all()
        for res in results:
            res_dict = {"post_id" : res.post_id, 
                "title" : res.title,
                "author" : res.author,
                "content" : res.content,
                "created_at" : res.created_at}
            data.append(res_dict)
    return data

def update(id: int, author: str, title: str, content: str) -> dict:
    result_dict = {}
    with Session(engine) as session:
        result = session.exec(select(Posts).where(Posts.post_id == id))
        res = result.one()
        res.author = author
        res.title = title
        res.content = content
        session.add(res)
        session.commit()
        session.refresh(res)

        result_dict = {"post_id" : res.post_id, 
                        "title" : res.title,
                        "author" : res.author,
                        "content" : res.content,
                        "created_at" : res.created_at}
    return result_dict

def delete(id: int) -> bool:
    result = False
    with Session(engine) as session:
        result = session.exec(select(Posts).where(Posts.post_id == id))
        res = result.one()
        
        session.add(res)
        session.commit()
        result = True
    return result