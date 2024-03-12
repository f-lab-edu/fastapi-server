from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from api.api_schema import (
    CommentBody,
    CommentConent,
    ResponseComment,
    ResponseMessageModel,
)
from common import api_key_header, check_access_token
from database import Comment, User, engine

session = Session(engine)

router = APIRouter(prefix="/api/comments", tags=["comments"])


@router.post(
    "/",
    response_model=ResponseMessageModel,
    status_code=status.HTTP_201_CREATED,
)
def create_comment(data: CommentBody) -> ResponseMessageModel:
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
def edit_comment(
    com_id: int, data: CommentConent, token: str = Depends(api_key_header)
) -> ResponseComment:
    """
    댓글 내용 수정
    """
    res = session.get(Comment, com_id)
    if res == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="댓글이 존재하지 않습니다.",
        )
    token_user_id = check_access_token(token)
    user_content = session.get(User, token_user_id.get("user_id"))
    if user_content.role != "admin" and token_user_id.get("user_id") != res.author_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="유저 아이디가 다릅니다.",
        )
    res.content = data.content
    session.add(res)
    session.commit()
    session.refresh(res)
    data = session.get(Comment, com_id)
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
def delete_comment(
    com_id: int, token: str = Depends(api_key_header)
) -> ResponseMessageModel:
    """
    댓글 삭제
    """
    data = session.get(Comment, com_id)
    if data == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="댓글이 존재하지 않습니다.",
        )
    token_user_id = check_access_token(token)
    user_content = session.get(User, token_user_id.get("user_id"))
    if user_content.role != "admin" and token_user_id.get("user_id") != data.author:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="유저 아이디가 다릅니다.",
        )
    session.delete(data)
    session.commit()
    return ResponseMessageModel(message=f"댓글 아이디 {com_id} 삭제 성공")
