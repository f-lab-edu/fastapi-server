import hashlib

from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from api.api_schema import (Content, RequestBody, RequestCommentBody,
                            RequestUserBody, ResponseListModel,
                            ResponseMessageModel, ResponseModel)
from database import Comment, Post, User, session

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
    data = Post(author=data.author, title=data.title, content=data.content)
    session.add(data)
    session.commit()
    return ResponseMessageModel(message="게시글 생성 성공")


@router.get(
    "/posts/{page}",
    response_model=ResponseListModel,
    status_code=status.HTTP_200_OK,
    tags=["posts"],
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
    "/posts/{post_id}",
    response_model=ResponseModel,
    status_code=status.HTTP_200_OK,
    tags=["posts"],
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
    "/posts/{post_id}",
    response_model=ResponseModel,
    status_code=status.HTTP_200_OK,
    tags=["posts"],
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
    "/posts/{post_id}",
    response_model=ResponseMessageModel,
    status_code=status.HTTP_200_OK,
    tags=["posts"],
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


@router.post(
    "/users",
    response_model=ResponseMessageModel,
    status_code=status.HTTP_201_CREATED,
    tags=["users"],
)
def create_user(data: RequestUserBody):
    """
    유저 생성
    """
    uppercase_count = sum(1 for word in data.password if word.isupper())
    if len(data.password) < 8 or uppercase_count == 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="유저 비밀번호가 최소 8자 이상, 대문자 1개 이상 포함되는지 확인해주세요.",
        )
    hashed_password = hashlib.sha256(data.password.encode()).hexdigest()
    data = User(user_id=data.user_id, password=hashed_password, nickname=data.nickname)
    session.add(data)
    session.commit()
    return ResponseMessageModel(message="유저 생성 성공")


@router.get(
    "/users/{page}",
    response_model=ResponseListModel,
    status_code=status.HTTP_200_OK,
    tags=["users"],
)
def get_user_posts(page: int) -> ResponseListModel:
    """
    게시글 목록 조회
    """
    data = page
    return ResponseListModel(message="게시글 목록 조회 성공", data=data)


@router.get(
    "/users/{user_id}/posts/{page}",
    response_model=ResponseListModel,
    status_code=status.HTTP_200_OK,
    tags=["users"],
)
def get_user_posts(page: int) -> ResponseListModel:
    """
    유저별로 작성한 게시글 목록 조회
    """
    data = page
    return ResponseListModel(message="게시글 목록 조회 성공", data=data)


@router.get(
    "/users/{user_id}/posts/{page}",
    response_model=ResponseListModel,
    status_code=status.HTTP_200_OK,
    tags=["users"],
)
def get_user_posts(page: int) -> ResponseListModel:
    """
    유저별로 작성한 게시글 목록 조회
    """
    data = page
    return ResponseListModel(message="게시글 목록 조회 성공", data=data)


@router.post(
    "/comments",
    response_model=ResponseMessageModel,
    status_code=status.HTTP_201_CREATED,
    tags=["comments"],
)
def create_comment(data: RequestCommentBody):
    """
    댓글 생성
    """
    data = Comment(author_id=data.author_id, post_id=data.post_id, content=data.content)
    session.add(data)
    session.commit()
    return ResponseMessageModel(message="댓글 생성 성공")
