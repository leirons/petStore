FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1



RUN apt-get update \
  && apt-get -y install netcat gcc postgresql \
  && apt-get clean


WORKDIR /edvantis/src

COPY . /edvantis/

RUN python -m pip install pipenv==2021.5.29
COPY Pipfile Pipfile.lock /edvantis/
RUN pipenv  install --system --dev

EXPOSE 8000
