# syntax=docker/dockerfile:1.6

ARG PYTHON_VERSION=3.13

FROM python:${PYTHON_VERSION} AS builder

ENV PATH="/root/.local/bin:${PATH}" \
    VIRTUAL_ENV="/opt/venv" \
    LIBOQS_INSTALL_PREFIX="/opt/liboqs"

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

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

WORKDIR /build

# Compile liboqs from source
RUN git clone --depth 1 https://github.com/open-quantum-safe/liboqs.git
RUN cmake -S liboqs -B liboqs/build -G Ninja \
    -DCMAKE_INSTALL_PREFIX=${LIBOQS_INSTALL_PREFIX} \
    -DBUILD_SHARED_LIBS=ON \
    -DOQS_ENABLE_KEM_BIKE=ON \
    -DOQS_ENABLE_KEM_CLASSIC_MCELIECE=ON \
    -DOQS_ENABLE_KEM_HQC=ON \
    && cmake --build liboqs/build \
    && cmake --install liboqs/build

# Compile liboqs-python wheel to install later
RUN git clone --depth 1 https://github.com/open-quantum-safe/liboqs-python.git
RUN LIBOQS_INSTALL_PATH=${LIBOQS_INSTALL_PREFIX} python -m pip wheel ./liboqs-python -w /tmp/wheels

RUN python -m venv ${VIRTUAL_ENV}
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

WORKDIR /app
COPY requirements.txt .

RUN uv pip install --no-cache-dir -r requirements.txt
RUN uv pip install --no-cache-dir /tmp/wheels/liboqs_python*.whl

FROM python:${PYTHON_VERSION} AS runtime

RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

ENV VIRTUAL_ENV="/opt/venv" \
    PATH="/opt/venv/bin:${PATH}" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    LIBOQS_INSTALL_PREFIX="/opt/liboqs" \
    LD_LIBRARY_PATH="/opt/liboqs/lib:${LD_LIBRARY_PATH}"

WORKDIR /app

COPY --from=builder ${LIBOQS_INSTALL_PREFIX} ${LIBOQS_INSTALL_PREFIX}
COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

