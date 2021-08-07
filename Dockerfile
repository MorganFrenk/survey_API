# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /app_survey
COPY requirements.txt /app_survey/
RUN pip install -r requirements.txt
COPY . /app_survey/