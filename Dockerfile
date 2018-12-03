FROM python:3.7.1-alpine

WORKDIR /app

ADD main.py /app/
ADD ./src /app/src/

CMD ["python3", "main.py", "--all"]
