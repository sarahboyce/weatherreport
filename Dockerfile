FROM python:3.8.7-slim as web
WORKDIR /usr/src/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update
# General Tools
RUN apt-get -y install netcat git gcc
# For PostgreSQL
RUN apt-get -y install libpq-dev
RUN pip install --upgrade pip
COPY ./requirements.txt ./
RUN pip install -r requirements.txt
# Copy all files
COPY . .
EXPOSE 8000
RUN ["chmod", "+x", "./entrypoints/entrypoint.web.sh"]
# Collect Static Files
RUN SECRET_KEY=dummy python manage.py collectstatic --noinput --settings=weatherreport.settings.docker

ENTRYPOINT ["./entrypoints/entrypoint.web.sh"]
