FROM --platform=linux/amd64 python:3.10-bullseye

LABEL maintainer="makarudze.com"

ENV PYTHONUNBUFFERED 1

# Install dependencies.
COPY ./requirements.txt /tmp/requirements.txt
COPY ./dev-requirements.txt /tmp/dev-requirements.txt

COPY . /code
WORKDIR /code
EXPOSE 8000

RUN sudo apt update && \ 
    sudo apt upgrade -y && \
    sudo apt install nmap -y 

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    /py/bin/pip install -r /tmp/dev-requirements.txt && \
    rm -rf /tmp && \
    adduser \
    --disabled-password \
    --no-create-home \
    django-user

ENV PATH="/py/bin:$PATH"

USER django-user
