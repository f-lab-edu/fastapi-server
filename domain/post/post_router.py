from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
import datetime

from domain.post import post_schema

router = APIRouter(
    prefix="/api",
    tags=["post"]
)

store_data = []

@router.post("/post", response_class=JSONResponse)
def create_post(data: post_schema.RequestBody):
    """
    게시글 생성
    """
    global store_data
    if len(store_data) == 0:
        post_id = 1
        content = {"post_id" : post_id, "author" : data.author, "title" : data.title , "content" : data.content, "created_at" : str(datetime.datetime.now())}
        store_data.append(content)
        print(store_data)
    else:
        post_id = len(store_data) + 1
        content = {"post_id" : post_id, "author" : data.author, "title" : data.title , "content" : data.content, "created_at" : str(datetime.datetime.now())}
        store_data.append(content)
        print(store_data)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=store_data
    )

@router.get("/posts", response_class=JSONResponse)
def get_posts():
    """
    게시글 목록 조회
    """
    return JSONResponse(
        status_code=200,
        content=store_data
    )

@router.get("/posts/{post_id}", response_class=JSONResponse)
def get_post(post_id: int):
    """
    게시글 조회
    """
    data = store_data[post_id]
    return JSONResponse(
        status_code=200,
        content=data
    )

@router.put("/{post_id}", response_class=JSONResponse)
def edit_post(data: post_schema.Item):
    """
    게시글 수정
    """
    global store_data 
    store_data = data
    return JSONResponse(
        status_code=200,
        content=store_data
    )

@router.delete("/{post_id}", response_class=JSONResponse)
def delete_post(post_id: int):
    """
    게시글 삭제
    """
    return JSONResponse(
        status_code=200,
        content=post_id
    )