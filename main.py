from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from redis import asyncio as aioredis
from redis.asyncio import Redis

from api import comment, post, user
from database import SQLModel, engine

SQLModel.metadata.create_all(engine)
app = FastAPI()


@app.get("/", response_class=RedirectResponse)
async def index():
    return "/docs"


@app.on_event("startup")
async def startup_event() -> Redis:
    # aioredis 연결 생성
    app.redis = await aioredis.from_url("redis://localhost:6379")
    return app.redis


@app.on_event("shutdown")
async def shutdown_event():
    # aioredis 연결 종료
    app.redis.close()
    await app.redis.wait_closed()


async def get_cached_query_result(query):
    cache_key = str(query)  # 쿼리를 기반으로 고유 키 생성
    cached_result = await app.redis.get(cache_key)

    if cached_result is not None:
        return cached_result  # 캐시된 결과 반환
    else:
        result = await execute_query(query)  # 데이터베이스 쿼리 실행
        await app.redis.set(cache_key, result, ex=60 * 60 * 2)  # 결과를 2시간 동안 캐싱
        return result


async def execute_query(query):
    async with engine.connect() as connection:
        result = await connection.execute(query)
        return result.fetchall()


app.include_router(post.router)
app.include_router(user.router)
app.include_router(comment.router)
