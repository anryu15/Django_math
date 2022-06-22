FROM python:3
ENV PYTHONUNBUFFERED 1

RUN mkdir /code

WORKDIR /code

ADD requirements.txt /code/

COPY requirements.txt .

RUN pip install -r requirements.txt
ADD . /code/
COPY . /code/
