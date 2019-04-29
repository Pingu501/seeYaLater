# FRONTEND
FROM node:10.15.0-alpine as frontend

WORKDIR /app

ADD /frontend /app

RUN yarn; yarn generate

# SERVER
FROM python:3.7-alpine

WORKDIR /app

ENV DJANGO_SETTINGS_MODULE seeYaLater.settings_production

RUN apk add mariadb mariadb-client mariadb-dev g++ nginx linux-headers

# install python dependencies
ADD /requirements.txt /app/
RUN pip install -r requirements.txt
RUN pip install uwsgi

RUN mkdir -p /app/static

# add compiled frontend to django
COPY --from=frontend /app/dist/ /app/static/

RUN mkdir /run/nginx/

COPY /api /app/api
COPY /miner /app/miner
COPY /seeYaLater /app/seeYaLater
COPY /manage.py /app/

RUN rm -rf /app/frontend

ADD /deployment/production/run.sh /
ADD /deployment/production/uwsgi.ini /app
ADD /deployment/production/uwsgi_params /
ADD /deployment/production/nginx.conf /etc/nginx/nginx.conf

EXPOSE 8000

CMD /run.sh
