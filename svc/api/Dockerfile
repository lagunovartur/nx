FROM python:3.12-slim AS builder
ENV PYTHONUNBUFFERED=1
WORKDIR /src

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

ARG BE_INSTALL_DEV='false'
RUN bash -c "if [ $BE_INSTALL_DEV == 'true' ] ; \
    then poetry install --no-root ;  \
    else poetry install --no-root --only main ; fi"

FROM python:3.12-slim

WORKDIR /src

COPY --from=builder /opt/poetry /opt/poetry
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

COPY ./ .

ENV PYTHONPATH=.

CMD ["bash", "-c", "python ./nx_api/main.py"]

