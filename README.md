# fastapi-server

## 아키텍처
```mermaid
flowchart LR
    A[main.py] --api 실행--> api["`post.py
    user.py
    comment.py`"]
    api --데이터 요청--> database.py
    database.py --데이터 조회--> id1[(post.db)]
```

## 버전 목록
- python : 3.12.0

## 환경 설정 방법
### 1. pyenv 설치 방법
```brew install pyenv```

### 2. pyenv로 파이썬 버전 설치
```pyenv install 3.12.0```

### 3. pyenv 실행
```pyenv shell 3.12.0```

### 4. poetry 설치 방법
```curl -sSL https://install.python-poetry.org | python3 -```

### 5. poetry 가상환경 실행
```poetry shell```

### 6. poetry로 필요한 패키지 일괄 설치
```poetry install```

### 7. poetry 종료 방법
```exit```

## fastAPI 서버 실행 및 종료 방법

### 1. 실행 방법
```uvicorn main:app --reload```

### 2. 종료 방법
```ctrl + c```

## 주의 사항 ##
- config.yaml를 직접 생성해서 추가해야 실행이 됩니다.

- config.yaml 위치
```
/config.yaml
```

### config.yaml 내용 예시 ###
```
secret_key: key01234567890
algorithm: HS256
access_token_expire_days: 1
```

## API 사용 방법 및 결과 예시
### 게시글 전체 목록 조회 API
- 사용 예시
```
curl -X 'GET' \
  'http://127.0.0.1:8000/api/posts/?page=1' \
  -H 'accept: application/json'
```

- 결과 예시
```
{
  "message": "게시글 목록 조회 성공",
  "data": [
    {
      "post_id": 1,
      "author": "admin",
      "title": "제목을 입력해주세요",
      "content": "내용을 입력해주세요",
      "created_at": "2024-03-06T16:49:59.694742"
    },
    {
      "post_id": 2,
      "author": "user0001",
      "title": "가입인사",
      "content": "안녕하세요",
      "created_at": "2024-03-10T04:07:31.244932"
    }
  ]
}
```

### 게시글 생성 API
- 사용 예시
```
curl -X 'POST' \
  'http://127.0.0.1:8000/api/posts/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "author": "user0001",
  "title": "가입인사",
  "content": "안녕하세요"
}'
```

- 결과 예시
```
{
  "message": "게시글 생성 성공"
}
```

### 게시글 조회 API
- 사용 예시
```
curl -X 'GET' \
  'http://127.0.0.1:8000/api/posts/2' \
  -H 'accept: application/json'
```

- 결과 예시
```
{
  "message": "게시글 조회 성공",
  "data": {
    "post_id": 2,
    "author": "admin",
    "title": "제목을 입력해주세요",
    "content": "내용을 입력해주세요",
    "created_at": "2024-03-06T16:49:59.694742"
  }
}
```

### 게시글 수정 API
- API 사용 시, 로그인 필요
- 게시글 작성한 본인 혹은 관리자(admin)가 아닐 시 수정 불가
- 사용 예시
```
curl -X 'PUT' \
  'http://127.0.0.1:8000/api/posts/2' \
  -H 'accept: application/json' \
  -H 'Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYWRtaW4wMiIsImV4cCI6MTcxMDEzMDc1MH0.JCIdSoqTm6hpxNFnu_vU_RxdZA4v7vChdl2AhiptQFE' \
  -H 'Content-Type: application/json' \
  -d '{
  "author": "admin02",
  "title": "제목 수정합니다",
  "content": "내용도 수정했습니다"
}'
```

- 결과 예시
```
{
  "message": "게시글 번호 2 수정 성공",
  "data": {
    "post_id": 2,
    "author": "admin",
    "title": "string",
    "content": "string",
    "created_at": "2024-03-06T16:49:59.694742"
  }
}
```

### 게시글 삭제 API
- API 사용 시, 로그인 필요
- 게시글 작성한 본인 혹은 관리자(admin)가 아닐 시 삭제 불가
- 사용 예시
```
curl -X 'DELETE' \
  'http://127.0.0.1:8000/api/posts/2' \
  -H 'accept: application/json' \
  -H 'Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYWRtaW4wMiIsImV4cCI6MTcxMDEzMDc1MH0.JCIdSoqTm6hpxNFnu_vU_RxdZA4v7vChdl2AhiptQFE'
```

- 결과 예시
```
{
  "message": "게시글 번호 2 삭제 성공"
}
```

### 게시글에 해당되는 댓글 목록 조회 API
- API 사용 시, 로그인 필요
- 사용 예시
```
curl -X 'DELETE'
    'http://127.0.0.1:8000/api/posts/1'
    -H 'accept: application/json'
```

### 유저 생성 API
- 1. 사용 예시 : 관리자 생성
```
curl -X 'POST' \
  'http://127.0.0.1:8000/api/users/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": "admin0001",
  "password": "A1234567890",
  "nickname": "관리자",
  "role": "admin"
}'
```

- 2. 사용 예시 : 유저 생성
```
curl -X 'POST' \
  'http://127.0.0.1:8000/api/users/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": "user0001",
  "password": "A1234567890",
  "nickname": "일반사용자",
  "role": "member"
}'
```

- 결과 예시
```
{
  "message": "유저 생성 성공"
}
```

### 유저 수정 API
- API 사용 시, 로그인 필요
- 유저 본인 혹은 관리자(admin)가 아닐 시 수정 불가
- 사용 예시
```
curl -X 'PUT' \
  'http://127.0.0.1:8000/api/users/admin02' \
  -H 'accept: application/json' \
  -H 'Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYWRtaW4wMiIsImV4cCI6MTcxMDEzMzc0NX0.0nGoAuuJuRs66sP2Mxox9RR-yeQHfidd8iDVWc4w4zo' \
  -H 'Content-Type: application/json' \
  -d '{
  "password": "A1234567890",
  "nickname": "닉네임수정",
  "role": "admin"
}'
```

- 결과 예시
```
{
  "message": "유저 아이디 admin02 수정 성공",
  "data": {
    "user_id": "admin02",
    "password": "$2b$12$XmFM8XLgBakzmNc/ZRjonO1.ebjhn5qrlbFOyEJ/PgkMP.SsdL1PW",
    "nickname": "닉네임수정",
    "role": "admin"
  }
}
```

### 유저 삭제 API
- API 사용 시, 로그인 필요
- 유저 본인 혹은 관리자(admin)가 아닐 시 삭제 불가
- 사용 예시
```
curl -X 'DELETE' \
  'http://127.0.0.1:8000/api/users/user0001' \
  -H 'accept: application/json' \
  -H 'Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYWRtaW4wMiIsImV4cCI6MTcxMDEzMzc0NX0.0nGoAuuJuRs66sP2Mxox9RR-yeQHfidd8iDVWc4w4zo'
```

- 결과 예시
```
{
  "message": "유저 아이디 user0001 삭제 성공"
}
```

### 유저가 작성한 게시글 조회 API
- API 사용 시, 로그인 필요
- 사용 예시
```
curl -X 'GET' \
  'http://127.0.0.1:8000/api/users/admin02/posts/?page=1' \
  -H 'accept: application/json' \
  -H 'Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYWRtaW4wMiIsImV4cCI6MTcxMDEzMDc1MH0.JCIdSoqTm6hpxNFnu_vU_RxdZA4v7vChdl2AhiptQFE'
```

- 결과 예시
```
{
  "message": "유저별 작성 게시글 목록 조회 성공",
  "data": [
    {
      "post_id": 4,
      "author": "admin02",
      "title": "첫 게시물",
      "content": "안녕하세요",
      "created_at": "2024-03-10T05:00:29.616600"
    }
  ]
}
```

### 유저가 작성한 댓글 조회 API
- API 사용 시, 로그인 필요
- 사용 예시
```
curl -X 'GET' \
  'http://127.0.0.1:8000/api/users/admin02/comments/?page=1' \
  -H 'accept: application/json' \
  -H 'Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYWRtaW4wMiIsImV4cCI6MTcxMDEzMDc1MH0.JCIdSoqTm6hpxNFnu_vU_RxdZA4v7vChdl2AhiptQFE'
```

- 결과 예시
```
{
  "message": "유저별 작성 댓글 조회 성공",
  "data": [
    {
      "com_id": 2,
      "author_id": "admin02",
      "post_id": 2,
      "content": "안녕하세요",
      "created_at": "2024-03-10T04:52:08.001156"
    },
    {
      "com_id": 3,
      "author_id": "admin02",
      "post_id": 2,
      "content": "반갑습니다",
      "created_at": "2024-03-10T04:52:31.157503"
    }
  ]
}
```

### 유저 로그인 API
- 사용 예시
```
curl -X 'POST' \
  'http://127.0.0.1:8000/api/users/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": "admin0001",
  "password": "A1234567890"
}'
```

- 결과 예시
```
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYWRtaW4wMiIsImV4cCI6MTcxMDEzMDc1MH0.JCIdSoqTm6hpxNFnu_vU_RxdZA4v7vChdl2AhiptQFE",
  "token_type": "bearer"
}
```

### 유저 로그아웃 API
- API 사용 시, 로그인 필요
- 사용 예시
```
curl -X 'POST' \
  'http://127.0.0.1:8000/api/users/logout' \
  -H 'accept: application/json' \
  -H 'Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYWRtaW4wMiIsImV4cCI6MTcxMDEzNDM4OX0.GdOIgLBqN5sW2Aic2AJJR47RH3shOJMQxsB1qsW6cwo' \
  -d ''
```

- 결과 예시
```
{
  "message": "로그아웃 성공"
}
```

### 댓글 생성 API
- 사용 예시
```
curl -X 'POST' \
  'http://127.0.0.1:8000/api/comments/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "com_id": 1,
  "author_id": "admin02",
  "post_id": 2,
  "content": "반갑습니다"
}'
```

- 결과 예시
```
{
  "message": "댓글 생성 성공"
}
```

### 댓글 수정 API
- API 사용 시, 로그인 필요
- 댓글 작성한 본인 혹은 관리자(admin)가 아닐 시 수정 불가
- 사용 예시
```
curl -X 'PUT' \
  'http://127.0.0.1:8000/api/comments/1' \
  -H 'accept: application/json' \
  -H 'Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYWRtaW4wMiIsImV4cCI6MTcxMDEzMDc1MH0.JCIdSoqTm6hpxNFnu_vU_RxdZA4v7vChdl2AhiptQFE' \
  -H 'Content-Type: application/json' \
  -d '{
  "content": "댓글 수정했어요"
}'
```

- 결과 예시
```
{
  "message": "댓글 아이디 1 내용 수정 성공",
  "data": {
    "content": "댓글 수정했어요"
  }
}
```

### 댓글 삭제 API
- API 사용 시, 로그인 필요
- 댓글 작성한 본인 혹은 관리자(admin)가 아닐 시 삭제 불가
- 사용 예시
```
curl -X 'DELETE' \
  'http://127.0.0.1:8000/api/comments/1' \
  -H 'accept: application/json' \
  -H 'Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYWRtaW4wMiIsImV4cCI6MTcxMDEzMDc1MH0.JCIdSoqTm6hpxNFnu_vU_RxdZA4v7vChdl2AhiptQFE'
```

- 결과 예시
```
{
  "message": "댓글 아이디 1 삭제 성공"
}
```
