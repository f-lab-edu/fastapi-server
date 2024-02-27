import hashlib

from fastapi import APIRouter, HTTPException, status
from sqlmodel import Session, select

from api.api_schema import (CommentBody, CommentConent, Content, RequestBody,
                            ResponseComList, ResponseComment,
                            ResponseListModel, ResponseMessageModel,
                            ResponseModel, ResponseUser, UserBody, UserConent)
from database import Comment, Post, User, engine

session = Session(engine)

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
    "/posts/",
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


@router.get(
    "/posts/{post_id}/comments/",
    response_model=ResponseComList,
    status_code=status.HTTP_200_OK,
    tags=["posts"],
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


@router.post(
    "/users",
    response_model=ResponseMessageModel,
    status_code=status.HTTP_201_CREATED,
    tags=["users"],
)
def create_user(data: UserBody):
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


@router.put(
    "/users/{user_id}",
    response_model=ResponseUser,
    status_code=status.HTTP_200_OK,
    tags=["users"],
)
def edit_user(user_id: str, data: UserBody):
    """
    유저 정보 수정
    """

    uppercase_count = sum(1 for word in data.password if word.isupper())
    if len(data.password) < 8 or uppercase_count == 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="유저 비밀번호가 최소 8자 이상, 대문자 1개 이상 포함되는지 확인해주세요.",
        )
    hashed_password = hashlib.sha256(data.password.encode()).hexdigest()

    res = session.get(User, user_id)
    res.password = hashed_password
    res.nickname = data.nickname
    session.add(res)
    session.commit()
    session.refresh(res)
    data = session.get(User, user_id)

    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="유저 정보 수정 실패",
        )
    return ResponseUser(
        message=f"유저 아이디 {user_id} 수정 성공",
        data=UserConent(
            user_id=user_id,
            password=data.password,
            nickname=data.nickname,
        ),
    )


@router.delete(
    "/users/{user_id}",
    response_model=ResponseMessageModel,
    status_code=status.HTTP_200_OK,
    tags=["users"],
)
def delete_user(user_id: str):
    """
    유저 삭제
    """
    data = session.get(User, user_id)
    session.delete(data)
    session.commit()
    if data is False:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="유저 삭제 실패",
        )
    return ResponseMessageModel(message=f"유저 아이디 {user_id} 삭제 성공")


@router.get(
    "/users/{user_id}/posts/",
    response_model=ResponseListModel,
    status_code=status.HTTP_200_OK,
    tags=["users"],
)
def get_user_posts(user_id: str, page: int):
    """
    유저별로 작성한 게시글 목록 조회
    """
    data = []
    offset = (page - 1) * 100
    results = session.exec(select(Post).where(Post.author == user_id).offset(offset).limit(100)).all()
    for res in results:
        res_dict = {
            "post_id": res.post_id,
            "author": res.author,
            "title": res.title,
            "content": res.content,
            "created_at": res.created_at,
        }
        data.append(res_dict)
    return ResponseListModel(message="유저별 작성 게시글 목록 조회 성공", data=data)


@router.get(
    "/users/{user_id}/comments/",
    response_model=ResponseListModel,
    status_code=status.HTTP_200_OK,
    tags=["users"],
)
def get_user_comments(user_id: str, page: int) -> ResponseListModel:
    """
    유저별로 작성한 댓글 목록 조회
    """
    data = page
    return ResponseListModel(message="유저별 작성 댓글 조회 성공", data=data)


@router.post(
    "/comments",
    response_model=ResponseMessageModel,
    status_code=status.HTTP_201_CREATED,
    tags=["comments"],
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
    "/comments/{com_id}",
    response_model=ResponseComment,
    status_code=status.HTTP_200_OK,
    tags=["comments"],
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
    "/comments/{com_id}",
    response_model=ResponseMessageModel,
    status_code=status.HTTP_200_OK,
    tags=["comments"],
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
