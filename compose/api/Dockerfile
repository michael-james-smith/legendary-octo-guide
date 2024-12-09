FROM python:3.13-bookworm AS builder

RUN pip install poetry==1.8.3

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /api

COPY ./pyproject.toml ./poetry.lock ./
RUN touch README.md

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --without dev --no-root

FROM python:3.13-slim-bookworm AS runtime

ARG UNAME=octo
ARG UID=520
ARG GID=520

ENV VIRTUAL_ENV=/api/.venv \
    PATH="/api/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY ./compose/api/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/api/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY api ./api
COPY alembic.ini ./
COPY main.py ./
COPY alembic ./alembic
RUN groupadd -g $GID -o $UNAME
RUN useradd -m -u $UID -g $GID -o -s /bin/bash $UNAME
USER $UNAME

ENTRYPOINT ["/entrypoint"]