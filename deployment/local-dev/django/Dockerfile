FROM python:3.7-stretch

RUN apt-get update && apt-get install -y supervisor

RUN mkdir -p /var/log/supervisord/ && touch /var/log/supervisord/supervisord.log

ADD entrypoint.sh /
ADD supervisord.conf /

WORKDIR /app
CMD ["/entrypoint.sh"]
