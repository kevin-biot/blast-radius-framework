#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_DIR="${ROOT_DIR}/.tools/integration-env"

python3 -c 'import sys; assert sys.version_info >= (3, 11), "Python 3.11+ required"'
python3 -m venv "${ENV_DIR}"
"${ENV_DIR}/bin/python" -m pip install --disable-pip-version-check \
  --requirement "${ROOT_DIR}/tools/requirements.txt" \
  --requirement "${ROOT_DIR}/tools/integration-requirements.txt"
echo "Installed optional integration runtime to ${ENV_DIR}"
