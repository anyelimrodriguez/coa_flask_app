FROM python:3.7-alpine

RUN apk add --no-cache \
    make \
    python3-dev \
    build-base \
    linux-headers \
    pcre-dev \
    nginx \
    supervisor

RUN mkdir -p /run/nginx
RUN rm /etc/nginx/conf.d/default.conf
COPY deployment/app.conf /etc/nginx/conf.d

RUN mkdir /app
WORKDIR /app/

RUN pip3 install pipenv
COPY Pipfile Pipfile.lock /app/
RUN pipenv install --system --deploy --ignore-pipfile

COPY deployment/uwsgi.ini /etc/uwsgi/
COPY deployment/supervisord.ini /etc/supervisor.d/
COPY . /app/

EXPOSE 80

CMD /usr/bin/supervisord
