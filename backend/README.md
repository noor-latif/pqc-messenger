# Backend Build Instructions

## Quick Start with Base Image (Recommended)

To speed up builds, use the pre-built base image with liboqs:

### 1. Build the base image (one-time setup, ~5-10 minutes)

**Linux/macOS:**
```bash
./build-base.sh
```

**Windows PowerShell:**
```powershell
.\build-base.ps1
```

**Or manually:**
```bash
docker build -f Dockerfile.base -t pqc-messenger-base:0.8.0 \
  --build-arg PYTHON_VERSION=3.13 \
  --build-arg LIBOQS_REF=0.8.0 \
  --build-arg LIBOQS_PYTHON_REF=v0.8.0 \
  ./backend
```

### 2. Build and run your app (now much faster!)

```bash
# From project root
docker compose build
docker compose up
```

## Build Without Base Image

If you prefer to build everything from scratch each time:

```bash
# Temporarily use a different base image
BASE_IMAGE=python:3.13 docker compose build --build-arg BASE_IMAGE=python:3.13
```

However, this will compile liboqs from source each time, which takes significantly longer.

## Customizing Base Image Versions

To use different versions of liboqs:

```bash
# Build base image with new versions
LIBOQS_REF=0.9.0 LIBOQS_PYTHON_REF=v0.9.0 ./build-base.sh

# Or with a custom image name
IMAGE_NAME=pqc-messenger-base:0.9.0 LIBOQS_REF=0.9.0 ./build-base.sh

# Use the new base image
BASE_IMAGE=pqc-messenger-base:0.9.0 docker compose build
```

## File Structure

- `Dockerfile.base` - Base image with liboqs and liboqs-python pre-compiled
- `Dockerfile` - Main application image that extends the base
- `build-base.sh` / `build-base.ps1` - Helper scripts to build the base image
- `requirements.txt` - Python dependencies (liboqs-python is installed from base image wheel)

