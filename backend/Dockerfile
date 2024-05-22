FROM python:3.9

ENV PYTHONUNBUFFERED 1

RUN apt-get update

COPY Pipfile /src/
COPY Pipfile.lock /src/
WORKDIR /src

RUN pip install --upgrade pip && pip install pipenv
RUN pipenv install --system

COPY . /src/
WORKDIR /src
