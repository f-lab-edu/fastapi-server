from fastapi import APIRouter, HTTPException, status
from sqlmodel import Session, select

from api.api_schema import (
    CommentBody,
    CommentConent,
    ResponseComment,
    ResponseMessageModel,
)
from database import Comment, engine

session = Session(engine)

router = APIRouter(prefix="/api/comments", tags=["comments"])


@router.post(
    "/",
    response_model=ResponseMessageModel,
    status_code=status.HTTP_201_CREATED,
)
def create_comment(data: CommentBody):
    """
    댓글 생성
    """
    data = Comment(author_id=data.author_id, post_id=data.post_id, content=data.content)
    session.add(data)
    session.commit()
    return ResponseMessageModel(message="댓글 생성 성공")


@router.put(
    "/{com_id}",
    response_model=ResponseComment,
    status_code=status.HTTP_200_OK,
)
def edit_comment(com_id: int, data: CommentConent):
    """
    댓글 내용 수정
    """
    res = session.get(Comment, com_id)
    res.content = data.content
    session.add(res)
    session.commit()
    session.refresh(res)
    data = session.get(Comment, com_id)

    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="댓글 내용 수정 실패",
        )
    return ResponseComment(
        message=f"댓글 아이디 {com_id} 내용 수정 성공",
        data=CommentConent(
            content=data.content,
        ),
    )


@router.delete(
    "/{com_id}",
    response_model=ResponseMessageModel,
    status_code=status.HTTP_200_OK,
)
def delete_comment(com_id: int):
    """
    댓글 삭제
    """
    data = session.get(Comment, com_id)
    session.delete(data)
    session.commit()
    if data is False:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="댓글 삭제 실패",
        )
    return ResponseMessageModel(message=f"댓글 아이디 {com_id} 삭제 성공")
