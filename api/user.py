from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import select

from api.api_schema import (
    CommentContent,
    Content,
    Login,
    ResponseAccessToken,
    ResponseComList,
    ResponseListModel,
    ResponseMessageModel,
    ResponseUser,
    UserBody,
    UserSign,
)
from common import (
    api_key_header,
    decode_access_token,
    encode_access_token,
    password_hashing,
    settings,
    verify_password,
)
from database import AuthToken, Comment, Post, User, engine

session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

router = APIRouter(prefix="/api/users", tags=["users"])


async def add_token_to_db(token: str) -> None:
    """db 토큰 저장소에 토큰 추가"""
    auth_token = AuthToken(
        token=token,
    )
    session.add(auth_token)
    await session.commit()


async def remove_token_from_db(token: str) -> None:
    """db 토큰 저장소에서 토큰 제거"""
    auth_token = await session.exec(
        select(AuthToken).where(AuthToken.token == token)
    ).first()
    if auth_token is not None:
        session.delete(auth_token)
        session.commit()


async def is_token_in_db(token: str) -> bool:
    """토큰이 db에 있는지 확인"""
    auth_token = await session.exec(
        select(AuthToken).where(AuthToken.token == token)
    ).first()
    if auth_token is not None:
        return True
    else:
        return False


@router.post(
    "/",
    response_model=ResponseMessageModel,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(data: UserSign) -> ResponseMessageModel:
    """
    유저 생성
    """
    cheacked_id = session.get(User, data.user_id)
    if cheacked_id != None and data.user_id == cheacked_id.user_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="유저 아이디가 이미 존재합니다.",
        )
    uppercase_count = sum(1 for word in data.password if word.isupper())
    if len(data.password) < 8 or uppercase_count == 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="유저 비밀번호가 최소 8자 이상, 대문자 1개 이상 포함되는지 확인해주세요.",
        )
    hashed_password = password_hashing.hash(data.password)
    data = User(
        user_id=data.user_id,
        password=hashed_password,
        nickname=data.nickname,
    )
    session.add(data)
    session.commit()
    return ResponseMessageModel(message="유저 생성 성공")


@router.put(
    "/{user_id}",
    response_model=ResponseUser,
    status_code=status.HTTP_200_OK,
)
async def edit_user(
    user_id: str, data: UserBody, token: str = Depends(api_key_header)
) -> ResponseUser:
    """
    유저 정보 수정
    """
    res = session.get(User, user_id)
    if res == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="유저 아이디가 존재하지 않습니다.",
        )
    token_user_id = decode_access_token(token)
    user_content = session.get(User, token_user_id.get("user_id"))
    if user_content.role != "admin" and token_user_id.get("user_id") != res.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="유저 아이디가 다릅니다.",
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
        data=UserSign(
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
async def delete_user(
    user_id: str, token: str = Depends(api_key_header)
) -> ResponseMessageModel:
    """
    유저 삭제
    """
    data = await session.get(User, user_id)
    if data == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="유저 삭제 실패. 유저 아이디가 존재하지 않습니다.",
        )
    token_user_id = decode_access_token(token)
    user_content = await session.get(User, token_user_id.get("user_id"))
    if user_content.role != "admin" and token_user_id.get("user_id") != data.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="유저 아이디가 다릅니다.",
        )
    session.delete(data)
    await session.commit()
    return ResponseMessageModel(message=f"유저 아이디 {user_id} 삭제 성공")


@router.get(
    "/{user_id}/posts/",
    response_model=ResponseListModel,
    status_code=status.HTTP_200_OK,
)
async def get_user_posts(
    user_id: str, page: int = 1, token: str = Depends(api_key_header)
) -> ResponseListModel:
    """
    유저별로 작성한 게시글 목록 조회
    """
    token_user_id = decode_access_token(token)
    user_content = await session.get(User, token_user_id.get("user_id"))
    if (
        user_content.role != "admin"
        and token_user_id.get("user_id") != user_content.user_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="유저 아이디가 다릅니다.",
        )
    data = []
    offset = (page - 1) * 100
    results = await session.exec(
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
    response_model=ResponseComList,
    status_code=status.HTTP_200_OK,
)
async def get_user_comments(
    user_id: str, page: int = 1, token: str = Depends(api_key_header)
) -> ResponseComList:
    """
    유저별로 작성한 댓글 목록 조회
    """
    token_user_id = decode_access_token(token)
    user_content = await session.get(User, token_user_id.get("user_id"))
    if (
        user_content.role != "admin"
        and token_user_id.get("user_id") != user_content.user_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="유저 아이디가 다릅니다.",
        )
    data = []
    offset = (page - 1) * 100
    results = await session.exec(
        select(Comment).where(Comment.author_id == user_id).offset(offset).limit(100)
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
    return ResponseComList(message="유저별 작성 댓글 조회 성공", data=data)


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
)
async def post_user_login(data: Login) -> ResponseAccessToken:
    """
    유저 로그인
    """
    db_data = await session.get(User, data.user_id)
    if db_data == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="유저 아이디가 존재하지 않습니다.",
        )
    if not db_data or not verify_password(data.password, db_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="아이디 혹은 비밀번호가 맞지 않습니다.",
        )
    access_token_expires = timedelta(days=settings.access_token_expire_days)
    access_token = encode_access_token(
        data={"user_id": data.user_id}, expires_delta=access_token_expires
    )
    add_token_to_db(access_token)
    return ResponseAccessToken(access_token=access_token, token_type="bearer")


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
)
async def post_user_logout(
    token: str = Depends(api_key_header),
) -> ResponseMessageModel:
    """
    유저 로그아웃
    """
    if is_token_in_db(token) != True:
        return ResponseMessageModel(message="로그아웃 성공")
    remove_token_from_db(token)
    return ResponseMessageModel(message="로그아웃 성공")
