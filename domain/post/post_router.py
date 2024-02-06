from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import datetime

from domain.post import post_schema

router = APIRouter(
    prefix="/api",
    tags=["post"]
)

@router.post("/post", response_class=JSONResponse)
def create_post(request: Request, data: post_schema.Item):
    """
    게시글 생성
    """
    global store_data 
    store_data = data
    return JSONResponse(
        status_code=200,
        content=data
    )

@router.get("/posts", response_class=JSONResponse)
def get_posts(request: Request):
    """
    게시글 목록 조회
    """
    return JSONResponse(
        status_code=200,
        content=store_data
    )

@router.get("/posts/{post_id}", response_class=JSONResponse)
def get_post(request: Request, post_id: int):
    """
    게시글 조회
    """
    data = store_data[post_id]
    return JSONResponse(
        status_code=200,
        content=data
    )

@router.post("/update/{post_id}", response_class=JSONResponse)
def edit_post(request: Request, data: post_schema.Item):
    """
    게시글 수정
    """
    global store_data 
    store_data = data
    return JSONResponse(
        status_code=200,
        content=store_data
    )

@router.post("/removal/{post_id}", response_class=JSONResponse)
def delete_post(request: Request, post_id: int):
    """
    게시글 삭제
    """
    return JSONResponse(
        status_code=200,
        content=post_id
    )