FROM python:3.9-alpine

WORKDIR /home

#variables de entorno
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0

#RUN apk update && apk add --no-cache gcc libc-dev make git libffi-dev openssl-dev python3-dev libxm12-dev libxslt-dev

COPY . .

RUN pip install -r /home/requirements.txt

#corro flask
CMD ["flask","run"]