# OPA Boundary Comparison

This example uses a real, digest-pinned OPA binary and a small in-memory ledger. It does not depend on Lane2 services, invoke an LLM, grant legal authority or make external state changes.

## Workload

The same eight hand-authored cases run in each mode: allowed increment, wrong tenant, excessive amount, expired grant, wrong audience, accumulated budget, missing scope and malformed amount. `scenarios.json` supplies an explicit expected authorization for every proposal. The observer compares actual ledger receipts with those fixture expectations; it does not derive ground truth from OPA's answer.

| Mode | What it does | Observed fixture expectations matched | Cases with committed violations |
|---|---|---|---|
| `unmediated` | Direct dispatch to the fixture tool | 2 of 8 | 6 |
| `schema_only` | Validate the request shape before dispatch | 2 of 8 | 6 |
| `opa_enforced` | Validate shape, query OPA, dispatch only on explicit true | 8 of 8 | 0 |

These are deterministic fixture counts, **not estimated failure rates**. Shape validation is not a substitute for policy, but this fixture is not evidence that canonical A2A/MCP deployments lack policy enforcement. The tool itself rejects malformed amounts in every mode, which is why that case is not a committed violation in the unmediated mode.

The Rego policy checks action, principal, tenant, audience, scope, expiry, per-call amount and accumulated budget. Each case starts with a fresh ledger. The budget case is sequential; concurrency, revocation services, bypass routes and external side effects remain untested.

## Run

From the repository root:

```sh
bash tools/install-jsonschema-local.sh
python3 tools/install_opa_local.py
python3 tools/opa_comparison.py --output .tools/opa-example.json
python3 tools/validate_json_schema.py spec/evaluation-evidence.schema.json .tools/opa-example.json
```

The comparison deliberately includes unsafe baselines, so its overall result is `fail` and the CLI returns **1** while writing a valid evidence bundle. Exit 2 is an operational/input error. Inspect each mode separately; an overall failing comparison is not evidence that the OPA-gated mode failed. Use `--overwrite` only when intentionally replacing an old output.

For a real Inspect `.eval` log and export, install the optional runtime and run:

```sh
bash tools/install-integrations-local.sh
.tools/integration-env/bin/python tools/run_inspect_demo.py --log-dir .tools/opa-inspect-logs --output .tools/opa-inspect-evidence.json
```

This default run evaluates only the OPA-gated mode, scores eight cases and returns 0. Inspect uses the mock model identity; the solver performs no model generation. Here `task_success` means the ledger matches the fixture expectation, not human task utility. `--mode schema_only` or `--mode unmediated` produces the corresponding negative-control log and returns 1.

For all unit/native integration checks and fresh evidence artifacts, use `bash tools/check-alignment-local.sh` after fetching the ACS assets as described in [the utility guide](../../tools/README.md). The [alignment note](../../adoption/alignment-implementation.md) records scope, versions and remaining work.
