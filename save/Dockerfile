FROM python:3.11.3-slim-bullseye

RUN apt-get update && apt-get install -y build-essential curl git

RUN mkdir -p /usr/src/csms

WORKDIR /usr/src/csms

COPY .. /usr/src/csms

ENV PYTHONPATH=/usr/src/csms
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ARG GITHUB_TOKEN
ENV GITHUB_TOKEN=$GITHUB_TOKEN

RUN pip install -r requirements.txt --upgrade pip