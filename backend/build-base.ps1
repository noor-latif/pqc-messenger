# Build script for the base Docker image with liboqs pre-built (PowerShell)
# This image only needs to be built once and can be reused for faster builds

$ErrorActionPreference = "Stop"

$PythonVersion = if ($env:PYTHON_VERSION) { $env:PYTHON_VERSION } else { "3.13" }
$LibOqsRef = if ($env:LIBOQS_REF) { $env:LIBOQS_REF } else { "0.8.0" }
$LibOqsPythonRef = if ($env:LIBOQS_PYTHON_REF) { $env:LIBOQS_PYTHON_REF } else { "v0.8.0" }
$ImageName = if ($env:IMAGE_NAME) { $env:IMAGE_NAME } else { "pqc-messenger-base:0.8.0" }

Write-Host "Building base image: $ImageName" -ForegroundColor Cyan
Write-Host "  Python: $PythonVersion"
Write-Host "  liboqs: $LibOqsRef"
Write-Host "  liboqs-python: $LibOqsPythonRef"
Write-Host ""

docker build `
  -f Dockerfile.base `
  -t "$ImageName" `
  --build-arg PYTHON_VERSION="$PythonVersion" `
  --build-arg LIBOQS_REF="$LibOqsRef" `
  --build-arg LIBOQS_PYTHON_REF="$LibOqsPythonRef" `
  ./backend

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Base image built successfully: $ImageName" -ForegroundColor Green
    Write-Host ""
    Write-Host "You can now use this base image for faster builds:"
    Write-Host "  docker compose build"
    Write-Host ""
    Write-Host "Or override the base image in docker-compose.yml:"
    Write-Host "  `$env:BASE_IMAGE='$ImageName'; docker compose build"
} else {
    Write-Host "❌ Build failed!" -ForegroundColor Red
    exit $LASTEXITCODE
}

