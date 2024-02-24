from fastapi import APIRouter, HTTPException, status

from api.posts_schema import (Content, RequestBody, ResponseListModel,
                              ResponseMessageModel, ResponseModel)
from database import delete, insert, select_all, select_one, update

router = APIRouter(prefix="/api/posts", tags=["posts"])


@router.post(
    "/", response_model=ResponseMessageModel, status_code=status.HTTP_201_CREATED
)
def create_post(data: RequestBody):
    """
    게시글 생성
    """
    data = insert(data.author, data.title, data.content)
    return ResponseMessageModel(message="게시글 생성 성공")


@router.get("/", response_model=ResponseListModel, status_code=status.HTTP_200_OK)
def get_posts() -> ResponseListModel:
    """
    게시글 목록 조회
    """
    data = select_all()
    return ResponseListModel(message="게시글 목록 조회 성공", data=data)


@router.get("/{post_id}", response_model=ResponseModel, status_code=status.HTTP_200_OK)
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


@router.put("/{post_id}", response_model=ResponseModel, status_code=status.HTTP_200_OK)
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
    "/{post_id}", response_model=ResponseMessageModel, status_code=status.HTTP_200_OK
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
