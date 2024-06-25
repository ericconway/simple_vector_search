# Dockerfile
FROM python:3.9-slim

WORKDIR /app

ENV LOG_LEVEL=DEBUG

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY static/ ./static/
COPY document_corpus/ ./document_corpus/


CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]

