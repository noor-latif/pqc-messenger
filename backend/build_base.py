#!/usr/bin/env python3
"""
Cross-platform script to build the Docker base image with liboqs and liboqs-python.

Uses python-on-whales for programmatic Docker operations.
"""

import os
import sys
from pathlib import Path
from typing import Dict

try:
    from python_on_whales import docker
    from python_on_whales.exceptions import DockerException
except ImportError:
    print("ERROR: python-on-whales is not installed.", file=sys.stderr)
    print("Please install it with: pip install python-on-whales", file=sys.stderr)
    sys.exit(1)


def get_env_with_default(key: str, default: str) -> str:
    """Get environment variable with a default value."""
    return os.environ.get(key, default)


def main() -> None:
    """Build the Docker base image."""
    # Get script directory (backend/)
    script_dir = Path(__file__).parent.resolve()
    
    # Get build arguments from environment with defaults
    python_version = get_env_with_default("PYTHON_VERSION", "3.13")
    liboqs_ref = get_env_with_default("LIBOQS_REF", "0.12.0")
    liboqs_python_ref = get_env_with_default("LIBOQS_PYTHON_REF", "v0.12.0")
    image_name = get_env_with_default("IMAGE_NAME", "pqc-messenger-base:0.12.0")
    
    # Dockerfile path
    dockerfile_path = script_dir / "Dockerfile.base"
    
    if not dockerfile_path.exists():
        print(f"ERROR: Dockerfile.base not found at {dockerfile_path}", file=sys.stderr)
        sys.exit(1)
    
    # Build arguments
    buildargs: Dict[str, str] = {
        "PYTHON_VERSION": python_version,
        "LIBOQS_REF": liboqs_ref,
        "LIBOQS_PYTHON_REF": liboqs_python_ref,
    }
    
    print(f"Building base image: {image_name}")
    print(f"  Python: {python_version}")
    print(f"  liboqs: {liboqs_ref}")
    print(f"  liboqs-python: {liboqs_python_ref}")
    print()
    
    try:
        # Build the image with streaming output
        # python-on-whales docker.build() API: context is first positional arg
        docker.build(
            str(script_dir),
            tags=[image_name],
            file="Dockerfile.base",
            build_args=buildargs,
            stream_logs=True,
            progress="plain",
        )
        
        print()
        print(f"✅ Base image built successfully: {image_name}")
        print()
        print("You can now use this base image for faster builds:")
        print("  docker compose build")
        print()
        
    except DockerException as e:
        print()
        print(f"❌ Build failed: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print()
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

