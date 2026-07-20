#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo "======================================"
echo "Running test suite"
echo "======================================"

python -m pytest
