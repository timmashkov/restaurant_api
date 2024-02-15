FROM python:3.10-slim

WORKDIR /food_app


COPY requirements.txt /food_app/
RUN pip install --upgrade pip; pip install  -r /food_app/requirements.txt

COPY . .
