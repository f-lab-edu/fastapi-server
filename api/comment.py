from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from api.api_schema import (
    CommentBody,
    CommentConent,
    ResponseComment,
    ResponseMessageModel,
)
from common import api_key_header, decode_access_token
from database import Comment, Post, User, engine

session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

router = APIRouter(prefix="/api/comments", tags=["comments"])


@router.post(
    "/",
    response_model=ResponseMessageModel,
    status_code=status.HTTP_201_CREATED,
)
async def create_comment(data: CommentBody) -> ResponseMessageModel:
    """
    댓글 생성
    """
    post_id = await session.get(Post, data.post_id)
    if post_id == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시물이 존재하지 않습니다.",
        )
    comment = Comment(
        author_id=data.author_id, post_id=data.post_id, content=data.content
    )
    session.add(comment)
    await session.commit()
    return ResponseMessageModel(message="댓글 생성 성공")


@router.put(
    "/{com_id}",
    response_model=ResponseComment,
    status_code=status.HTTP_200_OK,
)
async def edit_comment(
    com_id: int, data: CommentConent, token: str = Depends(api_key_header)
) -> ResponseComment:
    """
    댓글 내용 수정
    """
    res = await session.get(Comment, com_id)
    if res == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="댓글이 존재하지 않습니다.",
        )
    token_user_id = decode_access_token(token)
    user_content = await session.get(User, token_user_id.get("user_id"))
    if user_content.role != "admin" and token_user_id.get("user_id") != res.author_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="유저 아이디가 다릅니다.",
        )
    res.content = data.content
    session.add(res)
    await session.commit()
    session.refresh(res)
    data = await session.get(Comment, com_id)
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
async def delete_comment(
    com_id: int, token: str = Depends(api_key_header)
) -> ResponseMessageModel:
    """
    댓글 삭제
    """
    data = await session.get(Comment, com_id)
    if data == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="댓글이 존재하지 않습니다.",
        )
    token_user_id = decode_access_token(token)
    user_content = await session.get(User, token_user_id.get("user_id"))
    if user_content.role != "admin" and token_user_id.get("user_id") != data.author_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="유저 아이디가 다릅니다.",
        )
    session.delete(data)
    await session.commit()
    return ResponseMessageModel(message=f"댓글 아이디 {com_id} 삭제 성공")
