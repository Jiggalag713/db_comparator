FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa -y && \
    apt-get update &&  \
    apt-get install -y curl make git python3.10 && \
    alias python3=python3.10 && \
    curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"
RUN poetry --version && \
    git config --global --add safe.directory '*' && \
    mkdir /db_comparator

# ENV PATH="${PATH}:/root/.poetry/bin"
# RUN printenv | grep PATH
#nRUN . ${HOME}/.profile

COPY . /db_comparator/

RUN cd /db_comparator && poetry install