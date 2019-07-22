FROM python:3.7-alpine

RUN apk add --no-cache make
RUN pip3 install pipenv

RUN mkdir /app
WORKDIR /app

COPY . /app

RUN make install-docker-deps

EXPOSE 5000

CMD ["make", "run"]
