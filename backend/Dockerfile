# syntax=docker/dockerfile:1.6
# Main application Dockerfile - uses inline multi-stage builds for liboqs
# No external base image required - everything is built inline

ARG PYTHON_VERSION=3.13
ARG LIBOQS_REF=0.12.0
ARG LIBOQS_PYTHON_REF=0.12.0

# Stage 1: Build liboqs and liboqs-python wheel
FROM python:${PYTHON_VERSION} AS liboqs-builder
ARG LIBOQS_REF
ARG LIBOQS_PYTHON_REF

ENV PATH="/root/.local/bin:${PATH}" \
    LIBOQS_INSTALL_PREFIX="/opt/liboqs"

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    git \
    libffi-dev \
    libssl-dev \
    ninja-build \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv package manager
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

WORKDIR /build

# Compile liboqs from source
RUN git clone --depth 1 --branch ${LIBOQS_REF} https://github.com/open-quantum-safe/liboqs.git
RUN cmake -S liboqs -B liboqs/build -G Ninja \
    -DCMAKE_INSTALL_PREFIX=${LIBOQS_INSTALL_PREFIX} \
    -DBUILD_SHARED_LIBS=ON \
    -DOQS_ENABLE_KEM_ml_kem_768=ON \
    -DOQS_ENABLE_KEM_ml_kem_1024=ON \
    -DOQS_ENABLE_KEM_BIKE=ON \
    -DOQS_ENABLE_KEM_CLASSIC_MCELIECE=ON \
    -DOQS_ENABLE_KEM_HQC=ON \
    -DOQS_ENABLE_SIG_dilithium_3=ON \
    && cmake --build liboqs/build \
    && cmake --install liboqs/build

# Compile liboqs-python wheel
RUN git clone --depth 1 --branch ${LIBOQS_PYTHON_REF} https://github.com/open-quantum-safe/liboqs-python.git
RUN LIBOQS_INSTALL_PATH=${LIBOQS_INSTALL_PREFIX} python -m pip wheel ./liboqs-python -w /tmp/wheels

# Stage 2: Base image with liboqs and wheel (no external dependency needed)
FROM python:${PYTHON_VERSION} AS base
ARG LIBOQS_REF
ARG LIBOQS_PYTHON_REF

LABEL maintainer="PQC Messenger"
LABEL description="Base image with liboqs and liboqs-python pre-built"
LABEL liboqs.ref="${LIBOQS_REF}"
LABEL liboqs-python.ref="${LIBOQS_PYTHON_REF}"

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv package manager for runtime
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin:${PATH}" \
    LIBOQS_INSTALL_PREFIX="/opt/liboqs" \
    LD_LIBRARY_PATH="/opt/liboqs/lib:${LD_LIBRARY_PATH}"

# Copy liboqs installation and wheel from builder
COPY --from=liboqs-builder ${LIBOQS_INSTALL_PREFIX} ${LIBOQS_INSTALL_PREFIX}
COPY --from=liboqs-builder /tmp/wheels/liboqs_python*.whl /opt/wheels/

# Create a script to install the wheel (can be called by derived images)
RUN echo '#!/bin/sh\n\
uv pip install --no-cache-dir /opt/wheels/liboqs_python*.whl' > /usr/local/bin/install-liboqs-python && \
    chmod +x /usr/local/bin/install-liboqs-python

WORKDIR /app

# Stage 3: Build Python dependencies
FROM base AS builder

ENV VIRTUAL_ENV="/opt/venv" \
    PATH="/opt/venv/bin:${PATH}"

RUN python -m venv ${VIRTUAL_ENV}
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

WORKDIR /app
COPY requirements.txt .

# Install Python dependencies
RUN uv pip install --no-cache-dir \
    fastapi \
    uvicorn[standard] \
    pydantic \
    pydantic-settings \
    email-validator \
    "pyjwt>=2.8.0" \
    "argon2-cffi>=23.1.0" \
    "sqlalchemy>=2.0.0"

# Install liboqs-python from pre-built wheel
RUN /usr/local/bin/install-liboqs-python

# Stage 4: Runtime - final application image
FROM python:${PYTHON_VERSION} AS runtime

RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Install uv package manager for runtime (needed for install-liboqs-python script)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV VIRTUAL_ENV="/opt/venv" \
    PATH="/root/.local/bin:/opt/venv/bin:${PATH}" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    LIBOQS_INSTALL_PREFIX="/opt/liboqs" \
    LD_LIBRARY_PATH="/opt/liboqs/lib:${LD_LIBRARY_PATH}"

WORKDIR /app

# Copy liboqs from base stage and virtual environment from builder stage
COPY --from=base ${LIBOQS_INSTALL_PREFIX} ${LIBOQS_INSTALL_PREFIX}
COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY app .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
