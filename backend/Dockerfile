# syntax=docker/dockerfile:1.6
# Main application Dockerfile - uses pre-built base image with liboqs
#
# Prerequisites:
#   Build the base image first: make build-base
#   Or use: docker build -f Dockerfile.base -t pqc-messenger-base:0.12.0 ./backend

ARG BASE_IMAGE=pqc-messenger-base:0.12.0
ARG PYTHON_VERSION=3.13

# Import base image as a stage
FROM ${BASE_IMAGE} AS base

FROM base AS builder

ENV VIRTUAL_ENV="/opt/venv" \
    PATH="/opt/venv/bin:${PATH}"

RUN python -m venv ${VIRTUAL_ENV}
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

WORKDIR /app
COPY requirements.txt .

# Install Python dependencies (remove liboqs-python from git install since we use wheel)
RUN uv pip install --no-cache-dir \
    fastapi \
    uvicorn[standard] \
    pydantic \
    pydantic-settings \
    email-validator \
    "pyjwt>=2.8.0" \
    "argon2-cffi>=23.1.0" \
    "sqlalchemy>=2.0.0"
# Install liboqs-python from pre-built wheel in base image
RUN /usr/local/bin/install-liboqs-python

FROM python:${PYTHON_VERSION} AS runtime

RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

ENV VIRTUAL_ENV="/opt/venv" \
    PATH="/opt/venv/bin:${PATH}" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    LIBOQS_INSTALL_PREFIX="/opt/liboqs" \
    LD_LIBRARY_PATH="/opt/liboqs/lib:${LD_LIBRARY_PATH}"

WORKDIR /app

# Copy liboqs from base image and virtual environment from builder
COPY --from=base ${LIBOQS_INSTALL_PREFIX} ${LIBOQS_INSTALL_PREFIX}
COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY app .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

