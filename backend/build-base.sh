#!/bin/bash
# Build script for the base Docker image with liboqs pre-built
# This image only needs to be built once and can be reused for faster builds

set -e

PYTHON_VERSION=${PYTHON_VERSION:-3.13}
LIBOQS_REF=${LIBOQS_REF:-0.8.0}
LIBOQS_PYTHON_REF=${LIBOQS_PYTHON_REF:-v0.8.0}
IMAGE_NAME=${IMAGE_NAME:-pqc-messenger-base:0.8.0}

echo "Building base image: ${IMAGE_NAME}"
echo "  Python: ${PYTHON_VERSION}"
echo "  liboqs: ${LIBOQS_REF}"
echo "  liboqs-python: ${LIBOQS_PYTHON_REF}"
echo ""

docker build \
  -f Dockerfile.base \
  -t "${IMAGE_NAME}" \
  --build-arg PYTHON_VERSION="${PYTHON_VERSION}" \
  --build-arg LIBOQS_REF="${LIBOQS_REF}" \
  --build-arg LIBOQS_PYTHON_REF="${LIBOQS_PYTHON_REF}" \
  ./backend

echo ""
echo "✅ Base image built successfully: ${IMAGE_NAME}"
echo ""
echo "You can now use this base image for faster builds:"
echo "  docker compose build"
echo ""
echo "Or override the base image in docker-compose.yml:"
echo "  BASE_IMAGE=${IMAGE_NAME} docker compose build"

