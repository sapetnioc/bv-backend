FROM python:3.10

RUN pip install -U pip

RUN git clone -b pydantic_controller https://github.com/populse/soma-base /src/soma-base
RUN cd /src/soma-base && pip install -e .

RUN git clone https://github.com/sapetnioc/bv_services /src/bv_services
RUN cd /src/bv_services && pip install -e .

CMD []