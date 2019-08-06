FROM python:3.7-alpine

RUN pip install -U pip
RUN pip install -U ipython

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev libffi-dev && \
 pip install -U flask psycopg2-binary pyjwt[crypto] && \
 apk --purge del .build-deps


COPY setup.py /tmp
ADD bv_rest /tmp/bv_rest

RUN \
#     cd /tmp && python setup.py install && rm -R /tmp/setup.py /tmp/bv_rest
    cd /tmp && python setup.py develop && rm -R /tmp/setup.py # DEBUG

EXPOSE 80
