from fastapi import APIRouter, HTTPException, status

from api.api_schema import (
    Content,
    RequestBody,
    ResponseListModel,
    ResponseMessageModel,
    ResponseModel,
)
from database import delete, insert, select_all, select_one, update

router = APIRouter(prefix="/api")


@router.post(
    "/posts",
    response_model=ResponseMessageModel,
    status_code=status.HTTP_201_CREATED,
    tags=["posts"],
)
def create_post(data: RequestBody):
    """
    게시글 생성
    """
    data = insert(data.author, data.title, data.content)
    return ResponseMessageModel(message="게시글 생성 성공")


@router.get(
    "/posts",
    response_model=ResponseListModel,
    status_code=status.HTTP_200_OK,
    tags=["posts"],
)
def get_posts() -> ResponseListModel:
    """
    게시글 목록 조회
    """
    data = select_all()
    return ResponseListModel(message="게시글 목록 조회 성공", data=data)


@router.get(
    "/posts/{post_id}",
    response_model=ResponseModel,
    status_code=status.HTTP_200_OK,
    tags=["posts"],
)
def get_post(post_id: int):
    """
    게시글 조회
    """
    data = select_one(post_id)
    return ResponseModel(
        message="게시글 조회 성공",
        data=Content(
            post_id=data.post_id,
            author=data.author,
            title=data.title,
            content=data.content,
            created_at=data.created_at,
        ),
    )


@router.put(
    "/posts/{post_id}",
    response_model=ResponseModel,
    status_code=status.HTTP_200_OK,
    tags=["posts"],
)
def edit_post(post_id: int, data: RequestBody) -> ResponseModel:
    """
    게시글 수정
    """
    data = update(post_id, data.author, data.title, data.content)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글 수정 실패",
        )
    return ResponseModel(
        message=f"게시글 번호 {post_id} 수정 성공",
        data=Content(
            post_id=data.post_id,
            author=data.author,
            title=data.title,
            content=data.content,
            created_at=data.created_at,
        ),
    )


@router.delete(
    "/posts/{post_id}",
    response_model=ResponseMessageModel,
    status_code=status.HTTP_200_OK,
    tags=["posts"],
)
def delete_post(post_id: int):
    """
    게시글 삭제
    """
    data = delete(post_id)
    if data is False:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글 삭제 실패",
        )
    return ResponseMessageModel(message=f"게시글 번호 {post_id} 삭제 성공")


@router.post(
    "/users",
    response_model=ResponseMessageModel,
    status_code=status.HTTP_201_CREATED,
    tags=["users"],
)
def create_user(data: RequestBody):
    """
    유저 생성
    """
    data = insert(data.author, data.title, data.content)
    return ResponseMessageModel(message="유저 생성 성공")


@router.post(
    "/comments",
    response_model=ResponseMessageModel,
    status_code=status.HTTP_201_CREATED,
    tags=["comments"],
)
def create_comment(data: RequestBody):
    """
    댓글 생성
    """
    data = insert(data.author, data.title, data.content)
    return ResponseMessageModel(message="댓글 생성 성공")
