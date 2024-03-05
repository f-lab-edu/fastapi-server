from fastapi import APIRouter, HTTPException, status
from sqlmodel import Session, select

from api.api_schema import (Content, RequestBody, ResponseComList,
                            ResponseListModel, ResponseMessageModel,
                            ResponseModel)
from database import Comment, Post, engine

session = Session(engine)

router = APIRouter(prefix="/api/posts", tags=["posts"])


@router.post(
    "/",
    response_model=ResponseMessageModel,
    status_code=status.HTTP_201_CREATED,
)
def create_post(data: RequestBody):
    """
    게시글 생성
    """
    data = Post(author=data.author, title=data.title, content=data.content)
    session.add(data)
    session.commit()
    return ResponseMessageModel(message="게시글 생성 성공")


@router.get(
    "/",
    response_model=ResponseListModel,
    status_code=status.HTTP_200_OK,
)
def get_posts(page: int) -> ResponseListModel:
    """
    게시글 목록 조회
    """
    data = []
    offset = (page - 1) * 100
    results = session.exec(select(Post).offset(offset).limit(100)).all()
    for res in results:
        res_dict = {
            "post_id": res.post_id,
            "title": res.title,
            "author": res.author,
            "content": res.content,
            "created_at": res.created_at,
        }
        data.append(res_dict)
    return ResponseListModel(message="게시글 목록 조회 성공", data=data)


@router.get(
    "/{post_id}",
    response_model=ResponseModel,
    status_code=status.HTTP_200_OK,
)
def get_post(post_id: int):
    """
    게시글 조회
    """
    data = session.get(Post, post_id)
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
def edit_post(post_id: int, data: RequestBody) -> ResponseModel:
    """
    게시글 수정
    """
    res = session.get(Post, post_id)
    res.author = data.author
    res.title = data.title
    res.content = data.content
    session.add(res)
    session.commit()
    session.refresh(res)
    data = session.get(Post, post_id)
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
    "/{post_id}",
    response_model=ResponseMessageModel,
    status_code=status.HTTP_200_OK,
)
def delete_post(post_id: int):
    """
    게시글 삭제
    """
    data = session.get(Post, post_id)
    session.delete(data)
    session.commit()
    if data is False:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글 삭제 실패",
        )
    return ResponseMessageModel(message=f"게시글 번호 {post_id} 삭제 성공")


@router.get(
    "/{post_id}/comments/",
    response_model=ResponseComList,
    status_code=status.HTTP_200_OK,
)
def get_post_comments(post_id: int, page: int):
    """
    게시글 별로 작성된 댓글 목록 조회
    """
    data = []
    offset = (page - 1) * 100
    results = session.exec(select(Comment).where(Comment.post_id == post_id).offset(offset).limit(100)).all()
    for res in results:
        res_dict = {
            "com_id": res.com_id,
            "author_id": res.author_id,
            "post_id": res.post_id,
            "content": res.content,
            "created_at": res.created_at,
        }
        data.append(res_dict)
    return ResponseComList(message="게시글 별로 작성된 댓글 목록 조회 성공", data=data)