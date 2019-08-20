FROM python:3.7-alpine

RUN apk add --no-cache make python3-dev build-base linux-headers pcre-dev
RUN pip3 install pipenv

RUN mkdir /app
WORKDIR /app/

COPY Makefile Pipfile Pipfile.lock /app/

RUN make install-docker-deps

COPY . /app/

EXPOSE 5000

CMD ["make", "run"]
