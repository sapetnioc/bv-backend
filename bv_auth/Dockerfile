FROM bv_rest

RUN mkdir /bv_auth
RUN apk add openssh-keygen
RUN ssh-keygen -t rsa -f /bv_auth/id_rsa -P '' -m PEM
RUN apk add docker

COPY setup.py /tmp
ADD bv_auth /tmp/bv_auth

RUN \
#     cd /tmp && python setup.py install && rm -R /tmp/setup.py /tmp/bv_auth
    cd /tmp && python setup.py develop # DEBUG

RUN pip install gunicorn

# CMD gunicorn -b 0.0.0.0:80 bv_auth.wsgi

ENV FLASK_APP=bv_auth.wsgi
ENV FLASK_ENV=development
CMD flask run --host=0.0.0.0 --port 80
