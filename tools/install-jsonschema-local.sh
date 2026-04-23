#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_DIR="${ROOT_DIR}/.tools/jsonschema-lib"

mkdir -p "${TARGET_DIR}"

python3 -m pip install \
  --disable-pip-version-check \
  --target "${TARGET_DIR}" \
  --upgrade \
  jsonschema \
  referencing \
  rpds-py \
  attrs \
  jsonschema-specifications

echo "Installed local jsonschema runtime to ${TARGET_DIR}"
