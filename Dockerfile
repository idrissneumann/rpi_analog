FROM balenalib/raspberrypi3-debian:latest

COPY ./src ./requirements.txt ./manifest.json /

ENV PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8

RUN apt-get update -y && \
    apt-get install curl telnet net-tools wget python3 python3-pip -y && \
    pip3 install -r /requirements.txt

CMD [ "python3", "/main.py" ]
