FROM python:3.10
ENV PYTHONNUNBUFFERED 1

ENV LANG C.UTF-8
ARG DEBIAN_FRONTEND=noninteractive
# Allow SECRET_KEY to be passed via arg so collectstatic can run during build time
ARG SECRET_KEY

RUN apt-get update \
  && apt-get clean all \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/webapp
COPY . .
RUN python3 -m pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --dev --system
# RUN pipenv install --deploy --system (Use this to deploy)
RUN adduser \
  --disabled-password \
  --no-create-home \
  django-user

USER django-user