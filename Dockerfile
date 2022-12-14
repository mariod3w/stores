FROM python:3.8.15-slim-bullseye
RUN apt-get update && apt-get install nginx -y --no-install-recommends gcc python3-pip python3-dev libpq-dev curl libmariadb-dev
COPY scripts/nginx.default /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log
ADD requirements.txt /requirements/requirements.txt
RUN mkdir /code/
RUN pip install -r /requirements/requirements.txt --cache-dir /code/
WORKDIR /code/
ADD . /code/
COPY scripts/start-server.sh /code/start-server.sh
RUN chmod 755 /code/start-server.sh
RUN mkdir -p /code/stores_backend/static/
RUN python /code/manage.py collectstatic --settings=stores_backend.settings.prod --noinput
RUN chown -R www-data:www-data /code/stores_backend/static/
EXPOSE 80
STOPSIGNAL SIGTERM
CMD ["/code/start-server.sh"]