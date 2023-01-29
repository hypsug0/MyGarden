FROM python:3.11-slim-bullseye

ARG DEBIAN_FRONTEND=noninteractive
ARG USERNAME=app
ARG USER_UID=1000
ARG USER_GID=$USER_UID

ENV \
    # python:
    PYTHONDONTWRITEBYTECODE=1 \
    # pip:
    PIP_NO_CACHE_DIR=on \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100


RUN apt-get update -y \
    && apt-get install --no-install-recommends -y \
    libpq-dev gcc libgraphviz-dev \
    binutils libproj-dev gdal-bin postgresql-client \
    &&  apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /$USERNAME
COPY . /$USERNAME

COPY docker-entrypoint.sh /usr/bin/docker-entrypoint.sh

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

RUN mkdir /app/{static,media} && \
    chown -R app:app /app

USER $USERNAME

VOLUME ["/app/static","/app/media"]

EXPOSE 8000

ENTRYPOINT ["bash", "/usr/bin/docker-entrypoint.sh"]
