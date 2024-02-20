# fastapi-server

## 아키텍처
```mermaid
flowchart LR
    A[main.py] --api 실행--> posts_router.py
    posts_router.py --데이터 요청--> database.py
    database.py --데이터 조회--> id1[(post.db)]
```

## 버전 목록
- python : 3.12.0

## 사용 예시
### post
### update
### delete

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
