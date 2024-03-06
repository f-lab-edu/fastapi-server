from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Header, HTTPException, status
from jose import jwt
from passlib.context import CryptContext
from sqlmodel import Session, select

from api.api_schema import (
    Content,
    ResponseAccessToken,
    ResponseListModel,
    ResponseMessageModel,
    ResponseUser,
    UserBody,
    UserConent,
)
from database import Post, User, engine

session = Session(engine)

router = APIRouter(prefix="/api/users", tags=["users"])

password_hashing = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "key01234567890"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 1
session_login = []


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password, hashed_password):
    return password_hashing.verify(plain_password, hashed_password)


@router.post(
    "/",
    response_model=ResponseMessageModel,
    status_code=status.HTTP_201_CREATED,
)
def create_user(data: UserConent):
    """
    유저 생성
    """
    uppercase_count = sum(1 for word in data.password if word.isupper())
    if len(data.password) < 8 or uppercase_count == 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="유저 비밀번호가 최소 8자 이상, 대문자 1개 이상 포함되는지 확인해주세요.",
        )
    hashed_password = password_hashing.hash(data.password)
    data = User(user_id=data.user_id, password=hashed_password, nickname=data.nickname)
    session.add(data)
    session.commit()
    return ResponseMessageModel(message="유저 생성 성공")


@router.put(
    "/{user_id}",
    response_model=ResponseUser,
    status_code=status.HTTP_200_OK,
)
def edit_user(user_id: str, data: UserBody) -> ResponseUser:
    """
    유저 정보 수정
    """
    res = session.get(User, user_id)
    if res == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="유저 아이디가 존재하지 않습니다.",
        )

    uppercase_count = sum(1 for word in data.password if word.isupper())
    if len(data.password) < 8 or uppercase_count == 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="유저 비밀번호가 최소 8자 이상, 대문자 1개 이상 포함되는지 확인해주세요.",
        )
    hashed_password = password_hashing.hash(data.password)

    res.password = hashed_password
    res.nickname = data.nickname
    session.add(res)
    session.commit()
    session.refresh(res)
    data = session.get(User, user_id)

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
def delete_user(user_id: str) -> ResponseMessageModel:
    """
    유저 삭제
    """
    data = session.get(User, user_id)
    if data == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="유저 삭제 실패. 유저 아이디가 존재하지 않습니다.",
        )
    session.delete(data)
    session.commit()
    return ResponseMessageModel(message=f"유저 아이디 {user_id} 삭제 성공")


@router.get(
    "/{user_id}/posts/",
    response_model=ResponseListModel,
    status_code=status.HTTP_200_OK,
)
def get_user_posts(user_id: str, page: int) -> ResponseListModel:
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


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
)
def post_user_login(user_id: str, password: str) -> ResponseAccessToken:
    """
    유저 로그인
    """
    db_data = session.get(User, user_id)
    if db_data == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="유저 아이디가 존재하지 않습니다.",
        )
    if not db_data or not verify_password(password, db_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="아이디 혹은 비밀번호가 맞지 않습니다.",
        )
    access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    access_token = create_access_token(
        data={"sub": user_id}, expires_delta=access_token_expires
    )
    session_login.append(access_token)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
)
def post_user_logout(token: str) -> ResponseMessageModel:
    """
    유저 로그아웃
    """
    if token not in session_login:
        return ResponseMessageModel(message="로그아웃 실패")
    token_idx = session_login.index(token)
    session_login.pop(token_idx)
    return ResponseMessageModel(message="로그아웃 성공")
