#!/usr/bin/env bash

set -e

echo "======================================"
echo "Setting up development environment"
echo "======================================"

python -m pip install --upgrade pip
pip install -e .

echo ""
echo "Done."