# Fartor
# version 1

FROM python:3.6-alpine

# init
ADD . /code
WORKDIR /code

# setup
RUN apk update
RUN apk upgrade
RUN apk --no-cache add \
    git \
    python3 \
    python3-dev \
    postgresql-client \
    postgresql-dev \
    build-base \
    gettext
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# clean
RUN apk del -r python3-dev postgresql

# prep
ENV PYTHONUNBUFFERED 1