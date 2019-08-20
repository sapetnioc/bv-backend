FROM bv_rest

RUN pip install gunicorn

COPY setup.py /tmp
ADD bv_rest_example /tmp/bv_rest_example

COPY subjects.json /bv_rest_example/subjects.json
COPY centers.json /bv_rest_example/centers.json
COPY data.json /bv_rest_example/data.json
COPY visits.json /bv_rest_example/visits.json

RUN \
    cd /tmp && python setup.py develop # TODO modify to be compatible with local files


CMD gunicorn -b 0.0.0.0:80 bv_auth.wsgi

ENV FLASK_APP=bv_rest_example.wsgi
ENV FLASK_ENV=development
CMD flask run --host=0.0.0.0 --port 80

LABEL traefik.docker.network="web"
LABEL traefik.enable="true"
LABEL traefik.basic.frontend.rule="PathPrefixStrip: /example"
LABEL traefik.basic.port=80
LABEL traefik.basic.protocol="http"
