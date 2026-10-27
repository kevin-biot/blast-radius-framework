# CycloneDX to BRF Component Cards

This is a fictional CycloneDX 1.7 inventory, not an SBOM for this repository or proof of a deployed system. It links one service to the existing legal-database component card without changing that card or its historical profile rating.

```sh
bash tools/install-jsonschema-local.sh
python3 tools/fetch_cyclonedx_schemas.py
python3 tools/cyclonedx_inventory.py examples/cyclonedx/bom.json --mapping examples/cyclonedx/card-map.json --card spec/examples/example-component-card-tool-legal-db.json --profile spec/examples/example-profile-closed-world-br2.json --output .tools/cyclonedx-links.json
python3 tools/validate_json_schema.py spec/inventory-links.schema.json .tools/cyclonedx-links.json
```

Use a fresh output path; the importer refuses overwrites. The pinned upstream full schema, not a simplified BOM shape, validates the input. Other JSON spec versions and XML are unsupported and rejected.

Expected projection: four entries, one `declared_unverified` card link, two `unmapped` entries and one `not_addressable` entry. The service version `1.0` must exactly match the card. Card and profile digests identify the documents checked. A supplied card with unresolved profile IDs fails, as do duplicate `bom-ref` values, dangling local dependency references, unknown mappings and version mismatches.

To use your own inventory, create reviewed `links` entries in the same form as `card-map.json`, supply every linked card and its referenced profiles, and inspect all remaining gaps. Do not infer matches from names. Entries without `bom-ref` remain visible but cannot be mapped by this utility. An empty `links` list supports inventory-only inspection; it does not assert complete documentation.

The dependency graph is retained as declarations, with missing graphs and unlisted entries marked explicitly. An external BOM-Link is reported but never fetched. Edges and `provides` declarations do not establish deployed coupling, runtime reachability, authorization or a corporate mandate. CycloneDX signatures are not cryptographically verified. The [portability guide](../../adoption/evidence-portability-and-inventory.md) covers scope and optional DSSE packaging.
