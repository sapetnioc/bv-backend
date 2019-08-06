#! /bin/sh

docker-compose rm -f
docker rmi bv_postgres bv_rest bv_auth
docker volume rm bv_services_bv_services
docker volume prune -f
