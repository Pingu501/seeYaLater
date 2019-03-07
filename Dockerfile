FROM node:10.15.0-alpine as frontend

WORKDIR /app

ADD frontend/ /app

RUN yarn; yarn generate

FROM python:3.6.8-alpine

WORKDIR /app

RUN apk add mariadb mariadb-client mariadb-dev g++ uwsgi-python3 nginx

# install python dependencies
ADD requirements.txt /app/
RUN pip install -r requirements.txt

ADD seeYaLater_nginx.conf /etc/nginx/conf.d/

# add compiled frontend to django
COPY --from=frontend /app/dist/ /app/static/

# apache logs folder
RUN mkdir /app/logs

# create user for nginx
RUN addgroup seeYaLater
RUN adduser seeYaLater -D -H -G seeYaLater

COPY --chown=seeYaLater:seeYaLater / /app

# prepaire frontend for django
RUN python manage.py collectstatic

RUN rm -rf /app/frontend

# USER seeYaLater

CMD ["nginx", "–g", "'daemon off;'"]
