#! /bin/sh
docker build -t bv_rest bv_rest
docker volume create bv_services_bv_services
docker run -v bv_services_bv_services:/bv_services --rm python:3.7-alpine python -c 'import secrets, os; os.path.exists("/bv_services/postgres_password") or open("/bv_services/postgres_password", "w").write(secrets.token_urlsafe())'
docker run -v bv_services_bv_services:/bv_services --rm python:3.7-alpine sh -c 'echo bv_services > /bv_services/postgres_user && chmod a+r /bv_services/postgres_user /bv_services/postgres_password'
docker-compose build
docker-compose up
