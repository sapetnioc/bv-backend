FROM bv_rest

RUN pip install gunicorn

RUN mkdir /src
COPY setup.py /src
ADD bv_rest_example /src/bv_rest_example
RUN cd /src && python setup.py develop


CMD gunicorn -b 0.0.0.0:80 bv_rest_example.wsgi


LABEL traefik.docker.network="web"
LABEL traefik.enable="true"
LABEL traefik.basic.frontend.rule="PathPrefixStrip: /example"
LABEL traefik.basic.port=80
LABEL traefik.basic.protocol="http"
