# Backend Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY ./app ./app
COPY ./datasets ./datasets
COPY requirements.txt ./
COPY .env ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
