# 기본 이미지
FROM python:3.12-alpine

# 애플리케이션 파일 복사
COPY . /app
COPY requirements.txt /app

# 작업 디렉토리 설정
WORKDIR /app

# 종속성 설치
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 실행
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "main:app"]