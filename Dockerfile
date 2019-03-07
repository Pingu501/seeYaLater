FROM node:10.15.0-alpine as frontend

WORKDIR /app

ADD frontend/ /app

RUN yarn; yarn generate

FROM python:3.6.8-alpine

WORKDIR /app

ENV APACHE_CONFDIR /etc/apache2

RUN apk add mariadb mariadb-client mariadb-dev g++

# install python dependencies
ADD requirements.txt /app/
RUN pip install -r requirements.txt

RUN apk add make apache2 apache2-ctl apache2-dev

# add compiled frontend to django
COPY --from=frontend /app/dist/ /app/static/

# apache logs folder
RUN mkdir /app/logs

# create user for apache
RUN addgroup seeYaLater
RUN adduser seeYaLater -D -H -G seeYaLater

COPY --chown=seeYaLater:seeYaLater / /app

RUN wget https://github.com/GrahamDumpleton/mod_wsgi/archive/4.6.5.tar.gz; \
    tar xfz 4.6.5.tar.gz; \
    cd mod_wsgi-4.6.5; \
    ./configure --with-python=/usr/local/bin/python; \
    make install; \
    rm -rf mod_wsgi-4.6.5 4.6.5.tar.gz;

# prepaire frontend for django
RUN python manage.py collectstatic

RUN rm -rf /app/frontend

# USER seeYaLater

CMD apachectl -d . -f httpd.conf -e info -DFOREGROUND
