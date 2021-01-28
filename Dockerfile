FROM python:3.8.5-slim as web
WORKDIR /usr/src/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update
# General Tools
RUN apt-get -y install netcat git
# For SAML
RUN apt-get -y install xmlsec1
# For PostgreSQL
RUN apt-get -y install libpq-dev
# For Pyodbc
RUN apt-get -y install g++ gcc unixodbc-dev freetds-dev freetds-bin tdsodbc
# For LDAP
RUN apt-get -y install libsasl2-dev libldap2-dev libssl-dev
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
