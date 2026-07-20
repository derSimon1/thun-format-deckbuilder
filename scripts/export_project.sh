#!/usr/bin/env bash
set -euo pipefail

PROJECT_NAME="thun-format-deckbuilder"
ZIP_NAME="${PROJECT_NAME}.zip"

cd "$(dirname "$0")/.."

echo "---------------------------------------"
echo "Exporting ${PROJECT_NAME}"
echo "---------------------------------------"

rm -f "../${ZIP_NAME}"

zip -r "../${ZIP_NAME}" . \
    -x ".git/*" \
    -x ".venv/*" \
    -x "__pycache__/*" \
    -x "*/__pycache__/*" \
    -x ".pytest_cache/*" \
    -x "*/.pytest_cache/*" \
    -x ".mypy_cache/*" \
    -x "*/.mypy_cache/*" \
    -x "*.pyc" \
    -x "*.pyo" \
    -x "*.egg-info/*" \
    -x "data/cards.db" \
    -x "data/cards.db-wal" \
    -x "data/cards.db-shm" \
    -x "*/cards.db" \
    -x "*/cards.db-wal" \
    -x "*/cards.db-shm" \
    -x "*.zip"

echo ""
echo "Done!"
echo "Created: ../${ZIP_NAME}"
