#!/usr/bin/env python3
"""Read pinned ACS OTLP/JSON traces without mistaking verdicts for enforcement."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from uuid import UUID

try:
    from .evidence_common import digest, now, write_evidence
    from .fetch_acs_trace_assets import CACHE, COMMIT, FILES
    from .validate_json_schema import decode_json, load_json
except ImportError:
    from evidence_common import digest, now, write_evidence
    from fetch_acs_trace_assets import CACHE, COMMIT, FILES
    from validate_json_schema import decode_json, load_json


def trace_assets():
    manifest = load_json(CACHE / "manifest.json")
    if manifest.get("upstream_commit") != COMMIT:
        raise ValueError("wrong ACS trace cache revision")
    for name in FILES:
        if digest((CACHE / name).read_bytes()) != manifest["files"][name]["sha256"]:
            raise ValueError(f"ACS trace asset digest mismatch: {name}")
    return load_json(CACHE / "otel-mapping.json"), manifest


def any_value(value):
    if not isinstance(value, dict) or len(value) != 1:
        raise ValueError("invalid OTLP AnyValue")
    kind, item = next(iter(value.items()))
    if kind in {"stringValue", "bytesValue"} and isinstance(item, str):
        return item
    if kind == "boolValue" and type(item) is bool:
        return item
    if kind == "intValue" and (type(item) is int or isinstance(item, str) and re.fullmatch(r"-?\d+", item)):
        return int(item)
    if kind == "doubleValue" and type(item) in {int, float}:
        return item
    if kind == "arrayValue":
        return [any_value(v) for v in item.get("values", [])]
    if kind == "kvlistValue":
        return attributes(item.get("values", []))
    raise ValueError(f"unsupported or malformed OTLP value: {kind}")


def attributes(items):
    if not isinstance(items, list):
        raise ValueError("OTLP attributes must be a list")
    result = {}
    for item in items:
        key = item["key"]
        if not isinstance(key, str) or key in result:
            raise ValueError("invalid or duplicate OTLP attribute key")
        result[key] = any_value(item["value"])
    return result


def documents(raw):
    text = raw.decode("utf-8")
    try:
        return [decode_json(text)]
    except json.JSONDecodeError:
        return [decode_json(line) for line in text.splitlines() if line.strip()]


def read_trace(paths, mapping):
    names = {entry["span_name"] for entry in mapping["properties"]["step_to_span"]["default"].values()}
    groups, seen, sources = {}, {}, []
    ignored = 0
    for path in paths:
        raw = path.read_bytes()
        sources.append({"path": path.name, "sha256": digest(raw)})
        for document in documents(raw):
            if not isinstance(document, dict) or not isinstance(document.get("resourceSpans"), list):
                raise ValueError("expected OTLP ExportTraceServiceRequest.resourceSpans")
            for resource in document["resourceSpans"]:
                service = attributes(resource.get("resource", {}).get("attributes", [])).get("service.name", "unknown")
                if not isinstance(resource.get("scopeSpans"), list) or not isinstance(service, str):
                    raise ValueError("invalid OTLP scope or service name")
                for scope in resource["scopeSpans"]:
                    for span in scope.get("spans", []):
                        supported = span.get("name") in names
                        if not supported and not any(e.get("name") in {"acs.decision", "acs.decision.failure"} for e in span.get("events", [])):
                            ignored += 1
                            continue
                        span_key = (span["traceId"], span["spanId"])
                        if not re.fullmatch(r"[0-9a-fA-F]{32}", span_key[0]) or not re.fullmatch(r"[0-9a-fA-F]{16}", span_key[1]):
                            raise ValueError("invalid OTLP trace/span ID")
                        if span_key in seen:
                            if seen[span_key] != (span, service):
                                raise ValueError("conflicting exports for the same trace/span ID")
                            continue
                        seen[span_key] = (span, service)
                        attrs = attributes(span.get("attributes", []))
                        pair = tuple(str(UUID(attrs[key])) for key in ("acs.session.id", "acs.request_id"))
                        group = groups.setdefault(pair, {"span_names": set(), "services": set(), "verdicts": set(),
                            "chain_hashes": set(), "policy_references": [], "failures": [], "results": [], "findings": set()})
                        group["span_names"].add(span["name"])
                        group["services"].add(service)
                        if not supported:
                            group["findings"].add("unsupported span name carrying ACS events")
                        if (resource.get("resource", {}).get("droppedAttributesCount", 0)
                                or scope.get("scope", {}).get("droppedAttributesCount", 0)
                                or any(span.get(key, 0) for key in ("droppedAttributesCount", "droppedEventsCount", "droppedLinksCount"))):
                            group["findings"].add("dropped telemetry")
                        if span["name"] == "gen_ai.tool.result" and "acs.request_id_ref" not in attrs:
                            group["findings"].add("tool result has no request reference; outcome cannot be linked")
                        if span["name"] == "gen_ai.tool.result" and "acs.request_id_ref" in attrs:
                            group["results"].append({"request_id_ref": str(UUID(attrs["acs.request_id_ref"])),
                                "tool": attrs.get("gen_ai.tool.name", "unknown"), "exit_status": attrs.get("acs.exit_status", "unknown")})
                        for event in span.get("events", []):
                            values = attributes(event.get("attributes", []))
                            if event.get("droppedAttributesCount", 0):
                                group["findings"].add("dropped telemetry")
                            if event["name"] == "acs.decision":
                                verdict = values.get("acs.decision")
                                if verdict not in {"allow", "deny", "modify", "ask", "defer"}:
                                    raise ValueError("unknown ACS disposition")
                                group["verdicts"].add(verdict)
                                if "acs.chain_hash" in values:
                                    if not isinstance(values["acs.chain_hash"], str) or not values["acs.chain_hash"]:
                                        raise ValueError("invalid reported chain hash")
                                    group["chain_hashes"].add(values["acs.chain_hash"])
                                keys = ("acs.policy.ids", "acs.policy.versions", "acs.policy.rule_ids")
                                if any(key in values for key in keys):
                                    arrays = [values.get(key) for key in keys]
                                    if any(not isinstance(a, list) or any(not isinstance(v, str) for v in a) for a in arrays) or len({len(a) for a in arrays}) != 1:
                                        raise ValueError("ACS policy arrays must be parallel string arrays")
                                    for policy_id, version, rule in zip(*arrays):
                                        ref = {"policy_id": policy_id, "policy_version": version, "rule_id": rule}
                                        if ref not in group["policy_references"]:
                                            group["policy_references"].append(ref)
                            elif event["name"] == "acs.decision.failure":
                                enums = mapping["properties"]["decision_failure_event"]["properties"]["attribute_values"]["default"]
                                failure = {}
                                for suffix in ("class", "posture", "reported_by"):
                                    key = "acs.failure." + suffix
                                    if values.get(key) not in enums[key]:
                                        raise ValueError(f"invalid {key}")
                                    failure[suffix] = values[key]
                                if failure["class"] == "other" and (not isinstance(values.get("acs.failure.detail"), str) or not values["acs.failure.detail"].strip()):
                                    raise ValueError("other failure class requires detail")
                                if failure not in group["failures"]:
                                    group["failures"].append(failure)
    if not groups:
        raise ValueError("no supported ACS step spans found")
    failed_sessions = {pair[0] for pair, group in groups.items()
                       if any(f["class"] == "handshake_failure" for f in group["failures"])}
    results_by_request = {}
    for pair, group in groups.items():
        for result in group["results"]:
            target = (pair[0], result["request_id_ref"])
            if target not in groups or "gen_ai.tool.call" not in groups[target]["span_names"]:
                group["findings"].add("tool result references a missing tool-call request")
            results_by_request.setdefault(target, []).append(dict(result, result_request_id=pair[1]))
    records = []
    for (session, request), group in sorted(groups.items()):
        if len(group["span_names"]) > 1:
            group["findings"].add("conflicting step names for one request pair")
        if len(group["verdicts"]) > 1:
            group["findings"].add("conflicting verdicts")
        if len(group["chain_hashes"]) > 1:
            group["findings"].add("conflicting reported chain hashes; integrity investigation required")
        if session in failed_sessions:
            group["findings"].add("session handshake failure reported")
        if any(f["posture"] == "fail_open" for f in group["failures"]):
            group["findings"].add("fail-open posture reported; actual effects not verified")
        results = results_by_request.get((session, request), [])
        records.append({"session_id": session, "request_id": request,
            "span_names": sorted(group["span_names"]), "claimed_services": sorted(group["services"]),
            "verdicts": sorted(group["verdicts"]), "reported_chain_hashes": sorted(group["chain_hashes"]),
            "policy_references": group["policy_references"], "failures": group["failures"],
            "reported_tool_results": results, "tool_result_request_refs": sorted({r["request_id_ref"] for r in group["results"]}),
            "findings": sorted(group["findings"]),
            "decision_usable_as_reported": len(group["verdicts"]) == 1 and not group["failures"] and not group["findings"],
            "enforcement_status": "not_verified"})
    return {"bundle_version": "0.1", "source_format": "ACS-OTLP-JSON", "upstream_commit": COMMIT,
        "created_at": now(), "sources": sources, "records": records, "ignored_span_count": ignored,
        "failure_pair_count": sum(bool(g["failures"]) for g in groups.values()),
        "analysis_status": "findings" if any(r["findings"] for r in records) else "consistent",
        "limits": ["Trace-only analysis; verdicts and tool-result events never prove enforcement or actual effects.",
                   "Service names, policy references, chain hashes and failure postures are self-reported, not authenticated.",
                   "No full ACS-Trace/OCSF conformance, signature, anchor or production-boundary verification.",
                   "Missing events and missing host streams may conceal failures; counts are observed lower bounds."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("traces", nargs="+", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    try:
        if args.output.resolve() in {path.resolve() for path in args.traces}:
            raise ValueError("output must not replace an input trace")
        mapping, manifest = trace_assets()
        bundle = read_trace(args.traces, mapping)
        bundle["mapping_sha256"] = manifest["files"]["otel-mapping.json"]["sha256"]
        write_evidence(bundle, "acs-trace-evidence.schema.json", args.output, args.overwrite)
        print(f"{bundle['analysis_status'].upper()}: {len(bundle['records'])} request pairs; enforcement not verified")
        return int(bundle["analysis_status"] == "findings")
    except Exception as exc:
        print(f"ERROR: {exc}; fetch pinned assets with python3 tools/fetch_acs_trace_assets.py", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
