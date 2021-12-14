FROM python:3.10

RUN pip install -U pip

RUN git clone -b pydantic_controller https://github.com/populse/soma-base /src/soma-base
RUN cd /src/soma-base && pip install -e .

COPY setup.py /src/bv-backend/setup.py
COPY bv_backend /src/bv-backend/bv_backend
RUN cd /src/bv_backend && pip install -e .

CMD ["uvicorn", "--host", "0.0.0.0", "bv_backend.main:app"]
