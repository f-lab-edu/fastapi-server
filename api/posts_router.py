from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
import datetime

from api.posts_schema import ResponseModel, ResponseListModel, Content, RequestBody

router = APIRouter(
    prefix="/api/posts",
    tags=["posts"]
)

store_data = []

@router.post("/", response_model=ResponseModel, status_code=status.HTTP_201_CREATED)
def create_post(data: RequestBody) -> ResponseModel:
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
        {"message" : "성공", "data" : content}
    )

@router.get("/", response_model=ResponseListModel, status_code=status.HTTP_200_OK)
def get_posts() -> ResponseListModel:
    """
    게시글 목록 조회
    """
    return JSONResponse(
        {"message" : "성공", "data" : store_data}
    )

@router.get("/{post_id}", response_model=ResponseModel, status_code=status.HTTP_200_OK)
def get_post(post_id: int) -> ResponseModel:
    """
    게시글 조회
    """
    global store_data
    for post in store_data:
        if post.get("post_id") == post_id:
            data = post
            return JSONResponse(
                {"message" : "성공", "data" : data}
            )
        else:
            data = {}
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=data
            )

@router.put("/{post_id}", response_model=ResponseModel, status_code=status.HTTP_200_OK)
def edit_post(data: Content) -> ResponseModel:
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
               {"message" : "성공", "data" : data}
            )
        else:
            data = {}
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=data
            )

@router.delete("/{post_id}", response_model=ResponseModel, status_code=status.HTTP_200_OK)
def delete_post(post_id: int) -> ResponseModel:
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