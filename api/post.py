from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import select

from api.api_schema import (
    CommentContent,
    Content,
    RequestBody,
    ResponseComList,
    ResponseListModel,
    ResponseMessageModel,
    ResponseModel,
)
from common import api_key_header, decode_access_token
from database import Comment, Post, User, engine

session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

router = APIRouter(prefix="/api/posts", tags=["posts"])


@router.post(
    "/",
    response_model=ResponseMessageModel,
    status_code=status.HTTP_201_CREATED,
)
async def create_post(
    data: RequestBody, token: str = Depends(api_key_header)
) -> ResponseMessageModel:
    """
    게시글 생성
    """
    token_user_id = decode_access_token(token)
    user_content = await session.get(User, token_user_id.get("user_id"))
    if user_content.user_id != data.author:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="유저 아이디가 다릅니다.",
        )
    post = Post(author=data.author, title=data.title, content=data.content)
    session.add(post)
    await session.commit()
    return ResponseMessageModel(message="게시글 생성 성공")


@router.get(
    "/",
    response_model=ResponseListModel,
    status_code=status.HTTP_200_OK,
)
async def get_posts(page: int = 1) -> ResponseListModel:
    """
    게시글 목록 조회
    """
    data = []
    offset = (page - 1) * 100
    results = await session.exec(select(Post).offset(offset).limit(100)).all()
    for res in results:
        res_dict = Content(
            post_id=res.post_id,
            author=res.author,
            title=res.title,
            content=res.content,
            created_at=res.created_at,
        )
        data.append(res_dict)
    return ResponseListModel(message="게시글 목록 조회 성공", data=data)


@router.get(
    "/{post_id}",
    response_model=ResponseModel,
    status_code=status.HTTP_200_OK,
)
async def get_post(post_id: int) -> ResponseModel:
    """
    게시글 조회
    """
    data = await session.get(Post, post_id)
    if data == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글이 존재하지 않습니다.",
        )
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
    "/{post_id}",
    response_model=ResponseModel,
    status_code=status.HTTP_200_OK,
)
async def edit_post(
    post_id: int, data: RequestBody, token: str = Depends(api_key_header)
) -> ResponseModel:
    """
    게시글 수정
    """
    post = await session.get(Post, post_id)
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글이 존재하지 않습니다.",
        )
    token_user_id = decode_access_token(token)
    user_content = await session.get(User, token_user_id.get("user_id"))
    if user_content.role != "admin" and token_user_id.get("user_id") != post.author:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="유저 아이디가 다릅니다.",
        )
    post.author = data.author
    post.title = data.title
    post.content = data.content
    session.add(post)
    await session.commit()
    session.refresh(post)
    post = await session.get(Post, post_id)
    return ResponseModel(
        message=f"게시글 번호 {post_id} 수정 성공",
        data=Content(
            post_id=post_id,
            author=data.author,
            title=data.title,
            content=data.content,
            created_at=datetime.now(timezone.utc),
        ),
    )


@router.delete(
    "/{post_id}",
    response_model=ResponseMessageModel,
    status_code=status.HTTP_200_OK,
)
async def delete_post(
    post_id: int, token: str = Depends(api_key_header)
) -> ResponseMessageModel:
    """
    게시글 삭제
    """
    data = await session.get(Post, post_id)
    if data == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글이 존재하지 않습니다.",
        )
    token_user_id = decode_access_token(token)
    user_role = await session.get(User, token_user_id.get("user_id"))
    if user_role.role != "admin" and token_user_id.get("user_id") != data.author:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="유저 아이디가 다릅니다.",
        )
    session.delete(data)
    await session.commit()
    return ResponseMessageModel(message=f"게시글 번호 {post_id} 삭제 성공")


@router.get(
    "/{post_id}/comments/",
    response_model=ResponseComList,
    status_code=status.HTTP_200_OK,
)
async def get_post_comments(post_id: int, page: int = 1) -> ResponseComList:
    """
    게시글 별로 작성된 댓글 목록 조회
    """
    data = []
    offset = (page - 1) * 100
    results = await session.exec(
        select(Comment).where(Comment.post_id == post_id).offset(offset).limit(100)
    ).all()
    for res in results:
        res_dict = CommentContent(
            com_id=res.com_id,
            author_id=res.author_id,
            post_id=res.post_id,
            content=res.content,
            created_at=res.created_at,
        )
        data.append(res_dict)
    return ResponseComList(message="게시글 별로 작성된 댓글 목록 조회 성공", data=data)
