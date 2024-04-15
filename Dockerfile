# 기본 이미지로 Python 3.12.0 이미지를 사용
FROM python:3.12-slim as builder

# 환경변수 설정
ENV PYTHONDONTWRITEBYTECODE 1
# 파이썬 출력 로그 설정
ENV PYTHONUNBUFFERED 1

# 시스템 의존성 설치
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libffi-dev

# poetry 설치
RUN pip install poetry
RUN poetry config virtualenvs.create false

# 작업 디렉토리 설정
WORKDIR /fastapi_server

# 프로젝트 의존성 파일 복사
COPY pyproject.toml poetry.lock ./

# 프로젝트 의존성 설치
RUN poetry install --no-dev

# 애플리케이션 코드를 이미지에 복사
COPY . .

EXPOSE 8000
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
