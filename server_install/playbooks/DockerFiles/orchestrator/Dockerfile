FROM     ubuntu:focal
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update
RUN apt-get install -y python3 python3-pip postgresql-common libpq-dev docker

WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .
WORKDIR /app/orchestrator
CMD python3 main.py