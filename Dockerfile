ARG BASE_IMAGE=jfloff/alpine-python
ARG BASE_IMAGE_TAG=2.7-slim

FROM $BASE_IMAGE:$BASE_IMAGE_TAG

WORKDIR /usr/local/bin

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt && rm -f /tmp/requirements.txt

ENV LISTENPORT 8601
ENV IP 192.168.1.34
ENV FREQUENCY 1
ENV VERSION 0.48

ADD claymore-exporter.py .
ADD entrypoint.sh .
RUN chmod +x entrypoint.sh

EXPOSE 8601

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

