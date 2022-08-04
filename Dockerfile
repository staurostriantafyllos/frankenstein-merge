FROM python:3.8

WORKDIR /usr/src/app

RUN apt-get update -y
RUN apt-get upgrade -y

COPY . .

ENTRYPOINT ["python", "./main.py"]
