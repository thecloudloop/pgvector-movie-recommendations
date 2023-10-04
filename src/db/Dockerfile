ARG POSTGRESQL_VERSION=15
ARG PGVECTOR_VERSION=v0.5.0

FROM postgres:${POSTGRESQL_VERSION}-bullseye

ARG POSTGRESQL_VERSION
ARG PGVECTOR_VERSION

LABEL maintainer="TheCloudloop - pgvector working example"

USER root

RUN apt-get update \
    && apt-get install -y ca-certificates \
    && apt-get install -y --no-install-recommends git

RUN apt-get install build-essential postgresql-server-dev-${POSTGRESQL_VERSION} -y --no-install-recommends

RUN cd /tmp \
    && git clone --branch ${PGVECTOR_VERSION} https://github.com/pgvector/pgvector.git \
    && cd /tmp/pgvector \
    && make && make install
 
