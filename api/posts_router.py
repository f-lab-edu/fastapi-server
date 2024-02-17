from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.responses import JSONResponse
import datetime

from api.posts_schema import ResponseModel, ResponseListModel, Content, RequestBody
from db.connection import get_session

router = APIRouter(
    prefix="/api/posts",
    tags=["posts"]
)

@router.post("/", response_model=ResponseModel, status_code=status.HTTP_201_CREATED)
def create_post(data: RequestBody, db: Depends(get_session)) -> ResponseModel:
    """
    게시글 생성
    """
    data = db
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글 생성 실패",
        )
    return JSONResponse(
        {"message" : "게시글 생성 성공", "data" : data}
    )

@router.get("/", response_model=ResponseListModel, status_code=status.HTTP_200_OK)
def get_posts(db: Depends(get_session)) -> ResponseListModel:
    """
    게시글 목록 조회
    """
    data = db
    if not data:
        raise
    return JSONResponse(
        {"message" : "성공", "data" : data}
    )

@router.get("/{post_id}", response_model=ResponseModel, status_code=status.HTTP_200_OK)
def get_post(post_id: int, db: Depends(get_session)) -> ResponseModel:
    """
    게시글 조회
    """
    data = db
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글 조회 실패",
        )
    return JSONResponse(
                {"message" : "게시글 조회 성공", "data" : data}
            )

@router.put("/{post_id}", response_model=ResponseModel, status_code=status.HTTP_200_OK)
def edit_post(data: Content, db: Depends(get_session)) -> ResponseModel:
    """
    게시글 수정
    """
    data = db
    if not data:
        raise
    return JSONResponse(
        {"message" : "성공", "data" : data}
    )

@router.delete("/{post_id}", response_model=ResponseModel, status_code=status.HTTP_200_OK)
def delete_post(post_id: int, db: Depends(get_session)) -> ResponseModel:
    """
    게시글 삭제
    """
    data = db
    if not data:
        raise
    message = f"게시글 번호 {post_id} 삭제 성공"
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"messaage" : message}
    )