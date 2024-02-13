from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
import datetime

from domain.post_schema import Item, RequestBody

router = APIRouter(
    prefix="/api",
    tags=["post"]
)

store_data = []

@router.post("/posts", response_class=JSONResponse)
def create_post(data: RequestBody):
    """
    게시글 생성
    """
    global store_data
    if len(store_data) == 0:
        post_id = 1
        content = {"post_id" : post_id, "author" : data.author, "title" : data.title , "content" : data.content, "created_at" : str(datetime.datetime.now())}
        store_data.append(content)
    else:
        post_id = len(store_data) + 1
        content = {"post_id" : post_id, "author" : data.author, "title" : data.title , "content" : data.content, "created_at" : str(datetime.datetime.now())}
        store_data.append(content)

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
        status_code=status.HTTP_200_OK,
        content=store_data
    )

@router.get("/posts/{post_id}", response_class=JSONResponse)
def get_post(post_id: int):
    """
    게시글 조회
    """
    global store_data
    for post in store_data:
        if post.get("post_id") == post_id:
            data = post
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content=data
            )
        else:
            data = {}
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=data
            )

@router.put("/{post_id}", response_class=JSONResponse)
def edit_post(data: Item):
    """
    게시글 수정
    """
    global store_data
    for post in store_data:
        if post.get("post_id") == data.post_id:
            post["author"] = data.author
            post["title"] = data.title
            post["content"] = data.content
            data = {}
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content=data
            )
        else:
            data = {}
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=data
            )

@router.delete("/{post_id}", response_class=JSONResponse)
def delete_post(post_id: int):
    """
    게시글 삭제
    """
    global store_data
    for post in store_data:
        if post.get("post_id") == post_id:
            store_data.pop(store_data.index(post))
            message = f"게시글 번호 {post_id} 삭제 성공"
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"messaage" : message}
            )
        else:
            data = {}
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=data
            )