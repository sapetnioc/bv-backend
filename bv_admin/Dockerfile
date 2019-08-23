FROM bv_rest

RUN mkdir /bv_admin
RUN apk add openssh-keygen
RUN ssh-keygen -t rsa -f /bv_admin/id_rsa -P '' -m PEM
RUN apk add docker

COPY setup.py /bv_services/src
ADD bv_admin /bv_services/src/bv_admin

RUN cd /bv_services/src && python setup.py develop && rm setup.py

ENV FLASK_APP=bv_admin.wsgi

CMD gunicorn -b 0.0.0.0:80 $FLASK_APP
# 
# ENV FLASK_ENV=development
# CMD flask run --host=0.0.0.0 --port 80
