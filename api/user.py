import hashlib

from fastapi import APIRouter, HTTPException, status
from sqlmodel import Session, select

from api.api_schema import (
    Content,
    ResponseListModel,
    ResponseMessageModel,
    ResponseUser,
    UserBody,
    UserConent,
)
from database import Post, User, engine

session = Session(engine)

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post(
    "/",
    response_model=ResponseMessageModel,
    status_code=status.HTTP_201_CREATED,
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
    "/{user_id}",
    response_model=ResponseUser,
    status_code=status.HTTP_200_OK,
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
    "/{user_id}",
    response_model=ResponseMessageModel,
    status_code=status.HTTP_200_OK,
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
    "/{user_id}/posts/",
    response_model=ResponseListModel,
    status_code=status.HTTP_200_OK,
)
def get_user_posts(user_id: str, page: int):
    """
    유저별로 작성한 게시글 목록 조회
    """
    data = []
    offset = (page - 1) * 100
    results = session.exec(
        select(Post).where(Post.author == user_id).offset(offset).limit(100)
    ).all()
    for res in results:
        res_dict = Content(
            post_id=res.post_id,
            author=res.author,
            title=res.title,
            content=res.content,
            created_at=res.created_at,
        )
        data.append(res_dict)
    return ResponseListModel(message="유저별 작성 게시글 목록 조회 성공", data=data)


@router.get(
    "/{user_id}/comments/",
    response_model=ResponseListModel,
    status_code=status.HTTP_200_OK,
)
def get_user_comments(user_id: str, page: int) -> ResponseListModel:
    """
    유저별로 작성한 댓글 목록 조회
    """
    data = page
    return ResponseListModel(message="유저별 작성 댓글 조회 성공", data=data)
