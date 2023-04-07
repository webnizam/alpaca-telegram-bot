FROM python:3.10-slim-buster

# Install dependencies
RUN apt-get update \
    && apt-get install -y \
    build-essential \
    curl \
    g++ \
    git \
    make \
    python3-venv \
    software-properties-common

WORKDIR /root/bot

COPY ./requirements.txt ./

RUN pip3 install -r requirements.txt

COPY main.py ./
CMD python3 main.py

