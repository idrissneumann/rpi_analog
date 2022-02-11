ARG BALENA_DEBIAN_TAG=buster
ARG BALENA_DEBIAN_DIGEST=sha256:b32c2579e735f8257211c9b2c2eeab6db199907e138380833dbe2515cc6878e3

FROM balenalib/raspberrypi3-debian:${BALENA_DEBIAN_TAG}@${BALENA_DEBIAN_DIGEST} AS base

COPY ./src ./requirements.txt ./manifest.json /

ENV PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8

RUN apt-get update -y && \
    apt-get install curl telnet net-tools wget python3 python3-pip -y && \
    pip3 install -r /requirements.txt

CMD [ "python3", "/main.py" ]
