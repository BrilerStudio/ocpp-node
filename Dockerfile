FROM python:3.11.3-slim-bullseye

RUN apt-get update && apt-get install -y build-essential curl git

RUN mkdir -p /app

WORKDIR /app

COPY . /app

ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install -r requirements.txt --upgrade pip

CMD ["python", "/app/main.py"]
