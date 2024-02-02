from fastapi import APIRouter

from domain.post import post_schema

router = APIRouter(
    prefix="/api",
    tags=["post"]
)

@router.post("/post")
def create_post(post_id: int, author: str, title: str, content: str, created_at: str):
    """
    게시글 생성
    """
    # DB에 데이터 추가
    return {"code" : "200", 
            "message" : "성공"}

@router.get("/posts")
def get_posts():
    """
    게시글 목록 조회
    """
    # DB에서 데이터 가져오기
    post_id = 1
    author = 'author1'
    title = 'title1'
    content = 'content1'
    created_at = '2024-01-01'
    return {"code" : "200", 
            "message" : "성공", 
            "data" : [{"post_id": post_id, "author": author, "title": title, "content": content, "created_at": created_at}]}

@router.get("/{post_id}")
def get_post(post_id: int):
    """
    게시글 조회
    """
    post_id = 1
    author = 'author1'
    title = 'title1'
    content = 'content1'
    created_at = '2024-01-01'
    return {"code" : "200", 
            "message" : "성공", 
            "data" : {"post_id": post_id, 
                      "author": author, 
                      "title": title, 
                      "content": content, 
                      "created_at": created_at}}