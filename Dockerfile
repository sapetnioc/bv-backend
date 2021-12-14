FROM python:3.10

RUN pip install -U pip

RUN git clone -b pydantic_controller https://github.com/populse/soma-base /src/soma-base
RUN cd /src/soma-base && pip install -e .

COPY setup.py /src/bv_services/setup.py
COPY bv_services /src/bv_services/bv_services
RUN cd /src/bv_services && pip install -e .

# /usr/bin/X11 is a symlink on .
# That makes uvicorn fails
# RUN rm /usr/bin/X11

CMD ["uvicorn", "--host", "0.0.0.0", "bv_services.main:app"]