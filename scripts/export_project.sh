#!/usr/bin/env bash

set -e

PROJECT_NAME="thun-format-deckbuilder"
ZIP_NAME="${PROJECT_NAME}.zip"

echo "---------------------------------------"
echo "Exporting ${PROJECT_NAME}"
echo "---------------------------------------"

cd "$(dirname "$0")/.."

rm -f "../${ZIP_NAME}"

zip -r "../${ZIP_NAME}" . \
    -x ".git/*" \
    -x ".venv/*" \
    -x "__pycache__/*" \
    -x "**/__pycache__/*" \
    -x ".pytest_cache/*" \
    -x "**/.pytest_cache/*" \
    -x ".mypy_cache/*" \
    -x "**/.mypy_cache/*" \
    -x "*.pyc" \
    -x "*.pyo" \
    -x "data/cards.db" \
    -x "**/cards.db" \
    -x "*.zip"

echo ""
echo "Done!"
echo ""
echo "Created:"
echo "../${ZIP_NAME}"