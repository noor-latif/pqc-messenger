#!/usr/bin/env python3
"""
Cross-platform build orchestration script for PQC Messenger.

Builds the backend service using inline multi-stage builds.
Uses python-on-whales for all Docker operations.
"""

import argparse
import sys
from pathlib import Path

try:
    from python_on_whales import DockerClient
    from python_on_whales.exceptions import DockerException
except ImportError:
    print("ERROR: python-on-whales is not installed.", file=sys.stderr)
    print("Please install it with: pip install python-on-whales", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    """Main build orchestration."""
    parser = argparse.ArgumentParser(
        description="Build PQC Messenger backend using inline multi-stage builds"
    )
    parser.add_argument(
        "--python-version",
        default="3.13",
        help="Python version to use (default: 3.13)",
    )
    parser.add_argument(
        "--liboqs-ref",
        default="0.12.0",
        help="liboqs git ref/tag (default: 0.12.0)",
    )
    parser.add_argument(
        "--liboqs-python-ref",
        default="0.12.0",
        help="liboqs-python git ref/tag (default: 0.12.0)",
    )
    parser.add_argument(
        "--start",
        action="store_true",
        help="Start services after building (docker compose up)",
    )
    parser.add_argument(
        "--detach",
        action="store_true",
        help="Run containers in detached mode when using --start",
    )
    parser.add_argument(
        "--compose-file",
        default="docker-compose.yml",
        help="Path to docker-compose.yml file (default: docker-compose.yml)",
    )
    
    args = parser.parse_args()
    
    script_dir = Path(__file__).parent.resolve()
    compose_file = script_dir / args.compose_file
    
    if not compose_file.exists():
        print(f"ERROR: docker-compose.yml not found at {compose_file}", file=sys.stderr)
        sys.exit(1)
    
    # Initialize Docker client with compose file
    docker_client = DockerClient(compose_files=[str(compose_file)])
    
    # Build backend image using docker-compose
    print("Building backend service...")
    print(f"  Python: {args.python_version}")
    print(f"  liboqs: {args.liboqs_ref}")
    print(f"  liboqs-python: {args.liboqs_python_ref}")
    print()
    print("Note: This will build liboqs from source in a multi-stage build.")
    print("      This may take several minutes on first build.")
    print()
    
    try:
        # Build backend service using compose
        # Build args are defined in docker-compose.yml and can be overridden via environment
        # or by setting them here if python-on-whales supports it
        docker_client.compose.build(
            services=["backend"],
        )
        print("✅ Backend build completed successfully")
        print()
    except DockerException as e:
        error_msg = str(e)
        print(f"ERROR: Build failed: {error_msg}", file=sys.stderr)
        print("", file=sys.stderr)
        print("Troubleshooting:", file=sys.stderr)
        print("  - Ensure Docker is running: docker ps", file=sys.stderr)
        print("  - Check build logs above for specific errors", file=sys.stderr)
        print("  - Ensure you have at least 8 GB RAM available to Docker", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Unexpected error during build: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Optionally start services
    if args.start:
        print("Starting services...")
        try:
            docker_client.compose.up(detach=args.detach)
            if args.detach:
                print("✅ Services started in detached mode")
            else:
                print("✅ Services started (press Ctrl+C to stop)")
        except DockerException as e:
            print(f"ERROR: Failed to start services: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"ERROR: Unexpected error starting services: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print("Build complete. To start services, run:")
        print(f"  docker compose up")
        print()
        print("Or use this script with --start:")
        print(f"  python build.py --start")


if __name__ == "__main__":
    main()
