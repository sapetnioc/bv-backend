FROM python:3.7-alpine

RUN pip install -U pip
RUN pip install -U ipython

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev libffi-dev && \
 pip install -U flask psycopg2-binary pyjwt[crypto] && \
 apk --purge del .build-deps


COPY setup.py /bv_services/src/setup.py
ADD bv_rest /bv_services/src/bv_rest

RUN cd /bv_services/src && python setup.py develop && rm setup.py

EXPOSE 80
