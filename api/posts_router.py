from fastapi import APIRouter, status, HTTPException
from fastapi.encoders import jsonable_encoder

from api.posts_schema import ResponseModel, ResponseListModel, RequestBody, ResponseBoolModel
from database import insert, select_one, select_all, update, delete

router = APIRouter(
    prefix="/api/posts",
    tags=["posts"]
)

@router.post("/", response_model=ResponseBoolModel, status_code=status.HTTP_201_CREATED)
def create_post(data: RequestBody) -> ResponseBoolModel:
    """
    게시글 생성
    """
    data = insert(data.author, data.title, data.content)
    if data is False:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글 생성 실패",
        )
    return jsonable_encoder(
        {"message" : "게시글 생성 성공", "data" : data}
    )

@router.get("/", response_model=ResponseListModel, status_code=status.HTTP_200_OK)
def get_posts() -> ResponseListModel:
    """
    게시글 목록 조회
    """
    data = select_all()
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글 목록 조회 실패",
        )
    return jsonable_encoder(
        {"message" : "성공", "data" : data}
    )

@router.get("/{post_id}", response_model=ResponseModel, status_code=status.HTTP_200_OK)
def get_post(post_id: int) -> ResponseModel:
    """
    게시글 조회
    """
    data = select_one(post_id)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글 조회 실패",
        )
    return jsonable_encoder(
                {"message" : "게시글 조회 성공", "data" : data}
            )

@router.put("/{post_id}", response_model=ResponseModel, status_code=status.HTTP_200_OK)
def edit_post(post_id: int, data: RequestBody) -> ResponseModel:
    """
    게시글 수정
    """
    data = update(post_id, data.author, data.title, data.content)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글 수정 실패",
        )
    return jsonable_encoder(
        {"message" : "성공", "data" : data}
    )

@router.delete("/{post_id}", response_model=ResponseBoolModel, status_code=status.HTTP_200_OK)
def delete_post(post_id: int) -> ResponseBoolModel:
    """
    게시글 삭제
    """
    data = delete(post_id)
    if data is False:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글 삭제 실패",
        )
    message = f"게시글 번호 {post_id} 삭제 성공"
    return jsonable_encoder(
        {"message" : message, "data" : data}
    )