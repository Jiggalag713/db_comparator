FROM ubuntu:22.04

ENV TZ=Europe/Moscow \
    DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y software-properties-common tzdata && \
    add-apt-repository ppa:deadsnakes/ppa -y && \
    apt-get update &&  \
    apt-get install -y curl make git python3.12 mysql-client pipx && \
    alias python3=python3.12 && \
    pipx install poetry
ENV PATH="/root/.local/bin:$PATH"
RUN poetry --version && \
    git config --global --add safe.directory '*' && \
    mkdir /db_comparator

COPY . /db_comparator/

WORKDIR /db_comparator

RUN poetry install --no-root

CMD ["poetry", "run", "python3", "headless.py", "--config", "./resources/properties/integration_tests"]