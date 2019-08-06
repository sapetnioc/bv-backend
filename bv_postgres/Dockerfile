FROM postgres:11-alpine

COPY bv_postgres.sql /docker-entrypoint-initdb.d/

ENV POSTGRES_DB=bv_services
ENV POSTGRES_USER_FILE=/bv_services/postgres_user
ENV POSTGRES_PASSWORD_FILE=/bv_services/postgres_password
