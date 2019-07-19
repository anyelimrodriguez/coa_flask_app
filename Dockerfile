FROM python:3.7-alpine

RUN apk add --no-cache make
RUN pip3 install pipenv

RUN mkdir /app
WORKDIR /app

RUN make install-deps
CMD make run
