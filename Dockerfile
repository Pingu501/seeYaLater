FROM node:10.15.0-alpine as frontend

WORKDIR /app

ADD frontend/ /app

RUN yarn
RUN yarn generate

FROM python:3.7.2-alpine

WORKDIR /app

ENV APACHE_CONFDIR /etc/apache2

RUN apk add mariadb mariadb-client mariadb-dev gcc g++ apache2 apache2-ctl apache2-mod-wsgi

ADD requirements.txt /app/
RUN pip install -r requirements.txt

COPY --from=frontend /app/dist/ /app/static/

RUN mkdir /app/logs

ADD / /app

RUN python manage.py collectstatic

RUN rm -rf /app/frontend

CMD ["apachectl", "-d", ".", "-f", "httpd.conf", "-e", "info", "-DFOREGROUND"]