import os
from datetime import datetime, timezone
from typing import List

from dogpile.cache import make_region
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import Field, Relationship, SQLModel


class AuthToken(SQLModel, table=True):
    __tablename__ = "auth_token"
    idx: int = Field(primary_key=True)
    token: str


class Post(SQLModel, table=True):
    post_id: int = Field(default=None, primary_key=True)
    author: str = Field(foreign_key="user.user_id")
    title: str
    content: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )


class User(SQLModel, table=True):
    user_id: str = Field(default=None, primary_key=True)
    password: str
    nickname: str
    role: str = Field(default="member")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )


class Comment(SQLModel, table=True):
    com_id: int = Field(default=None, primary_key=True)
    author_id: str = Field(default=None, foreign_key="user.user_id")
    post_id: int = Field(default=None, foreign_key="post.post_id")
    content: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )


class Relationship(SQLModel):
    posts: List["Post"] = Relationship(back_populates="post", link_model=Post)
    users: List["User"] = Relationship(back_populates="user", link_model=User)
    comments: List["Comment"] = Relationship(
        back_populates="comment", link_model=Comment
    )


sqlite_url = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///post.db")

# 테스트 환경인지 확인하는 환경 변수를 추가합니다.
if os.getenv("TEST_ENV") == "true":
    sqlite_url = "sqlite+aiosqlite:///test.db"

# engine = create_async_engine(sqlite_url, echo=True, pool_size=10, max_overflow=20)
engine = create_async_engine(sqlite_url, echo=True)

cache_region = make_region().configure(
    "dogpile.cache.redis",
    arguments={
        "host": "localhost",  # Redis 서버 주소
        "port": 6379,  # Redis 서버 포트
        "db": 0,  # Redis 데이터베이스 번호
        "redis_expiration_time": 60 * 60 * 2,  # 캐시 만료 시간 (2시간)
        "distributed_lock": True,  # 분산 락 활성화
    },
)


async def get_cached_query_result(query):
    cache_key = str(query)  # 쿼리를 기반으로 고유 키 생성
    cached_result = cache_region.get(cache_key)

    if cached_result is not None:
        return cached_result  # 캐시된 결과 반환
    else:
        result = await execute_query(query)  # 데이터베이스 쿼리 실행
        cache_region.set(cache_key, result)  # 결과 캐싱
        return result


async def execute_query(query):
    async with engine.connect() as connection:
        result = await connection.execute(query)
        return result.fetchall()
