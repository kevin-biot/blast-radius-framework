#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"
PY="${ROOT_DIR}/.tools/integration-env/bin/python"
RUN_DIR="$(mktemp -d "${ROOT_DIR}/.tools/alignment-check.XXXXXX")"

expect_status() {
  local expected="$1"
  shift
  local status=0
  "$@" || status=$?
  if [[ "${status}" -ne "${expected}" ]]
  then
    echo "Expected exit ${expected}, got ${status}: $*" >&2
    return 1
  fi
}

python3 -m unittest discover -s tests -v
"${PY}" -m unittest discover -s tests/integration -v
python3 tools/validate_json_schema.py --check-repository
expect_status 1 python3 tools/acs_trace_evidence.py .tools/acs-trace-v0.1.4/sample.jsonl --output "${RUN_DIR}/acs-trace.json"
expect_status 1 python3 tools/opa_comparison.py --output "${RUN_DIR}/opa-comparison.json"
"${PY}" tools/run_inspect_demo.py --log-dir "${RUN_DIR}/inspect-logs" --output "${RUN_DIR}/inspect-evidence.json"
python3 tools/run_acs_live.py --run-dir "${RUN_DIR}/acs-live"
python3 tools/run_async_boundary.py --run-dir "${RUN_DIR}/async-boundary"
"${PY}" tools/run_portability_demo.py --evidence "${RUN_DIR}/async-boundary/evidence.json" --run-dir "${RUN_DIR}/portability"
python3 tools/validate_json_schema.py spec/acs-trace-evidence.schema.json "${RUN_DIR}/acs-trace.json"
python3 tools/validate_json_schema.py spec/evaluation-evidence.schema.json "${RUN_DIR}/opa-comparison.json" "${RUN_DIR}/inspect-evidence.json"
python3 tools/validate_json_schema.py spec/execution-evidence.schema.json "${RUN_DIR}/acs-live/evidence.json" "${RUN_DIR}/async-boundary/evidence.json"
python3 tools/validate_json_schema.py spec/inventory-links.schema.json "${RUN_DIR}/portability/inventory-links.json"
python3 tools/validate_json_schema.py spec/dsse-envelope.schema.json "${RUN_DIR}/portability/evidence.dsse.json" "${RUN_DIR}/portability/inventory-links.dsse.json"
echo "Alignment checks passed. Generated evidence retained in ${RUN_DIR}"
