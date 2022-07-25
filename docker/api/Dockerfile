FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1



RUN apt-get update \
  && apt-get -y install netcat gcc postgresql \
  && apt-get clean


WORKDIR /app

COPY . /app

RUN pip install pipenv
COPY Pipfile Pipfile.lock /app/
RUN pipenv install --system --dev


EXPOSE 8000