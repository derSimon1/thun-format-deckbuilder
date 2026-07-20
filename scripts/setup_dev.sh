#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo "======================================"
echo "Setting up development environment"
echo "======================================"

python -m pip install --upgrade pip
python -m pip install -e ".[dev]"

echo ""
echo "Done."
