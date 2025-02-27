# 1. Python 3.10 베이스 이미지 사용
FROM python:3.10

# 2. 작업 디렉토리 생성
WORKDIR /app

# 3. FastAPI 및 필요한 라이브러리 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. FastAPI 앱 코드 및 프롬프트 파일 복사
COPY . .

# 5. FastAPI 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]