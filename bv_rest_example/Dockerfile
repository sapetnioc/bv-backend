FROM bv_rest

COPY setup.py /tmp
ADD bv_rest_example /tmp/bv_rest_example

RUN \
#     cd /tmp && python setup.py install && rm -R /tmp/setup.py /tmp/bv_auth
    cd /tmp && python setup.py develop # DEBUG

RUN pip install gunicorn

# CMD gunicorn -b 0.0.0.0:80 bv_auth.wsgi

COPY subjects.json /bv_rest_example/subjects.json
COPY centers.json /bv_rest_example/centers.json
COPY data.json /bv_rest_example/data.json
COPY visits.json /bv_rest_example/visits.json

ENV FLASK_APP=bv_rest_example.wsgi
ENV FLASK_ENV=development
CMD flask run --host=0.0.0.0 --port 80

LABEL traefik.docker.network="web"
LABEL traefik.enable="true"
LABEL traefik.basic.frontend.rule="PathPrefixStrip: /example"
LABEL traefik.basic.port=80
LABEL traefik.basic.protocol="http"
