#!/usr/bin/env python3
"""Validate Agent knowledge records and cross-references."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE = ROOT / "knowledge"


def load_json(name: str) -> dict:
    return json.loads((KNOWLEDGE / name).read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []
    vendors_doc = load_json("vendors.json")
    sources_doc = load_json("sources.json")
    claims_doc = load_json("claims.json")
    conflicts_doc = load_json("conflicts.json")
    events = [
        json.loads(line)
        for line in (KNOWLEDGE / "timeline.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    vendors = vendors_doc["vendors"]
    sources = sources_doc["sources"]
    claims = claims_doc["claims"]
    conflicts = conflicts_doc["conflicts"]
    vendor_ids = {vendor["id"] for vendor in vendors}
    source_ids = {source["id"] for source in sources}
    claim_ids = {claim["id"] for claim in claims}
    event_ids = {event["id"] for event in events}

    for label, values in [
        ("vendor", [vendor["id"] for vendor in vendors]),
        ("source", [source["id"] for source in sources]),
        ("claim", [claim["id"] for claim in claims]),
        ("conflict", [conflict["id"] for conflict in conflicts]),
        ("timeline", [event["id"] for event in events]),
    ]:
        duplicates = sorted({value for value in values if values.count(value) > 1})
        if duplicates:
            errors.append(f"duplicate {label} ids: {duplicates}")

    for source in sources:
        if source.get("vendor_id") in {"standards", "research", "benchmarks"}:
            continue
        if source.get("vendor_id") not in vendor_ids:
            errors.append(f"source {source['id']} has unknown vendor {source.get('vendor_id')}")
        if not re.match(r"^https?://", source.get("url", "")):
            errors.append(f"source {source['id']} has invalid URL")

    for vendor in vendors:
        for source_id in vendor.get("source_ids", []):
            if source_id not in source_ids:
                errors.append(f"vendor {vendor['id']} references missing source {source_id}")

    for claim in claims:
        for source_id in claim.get("sources", []):
            if source_id not in source_ids:
                errors.append(f"claim {claim['id']} references missing source {source_id}")
        for old_claim in claim.get("supersedes", []):
            if old_claim == claim["id"]:
                errors.append(f"claim {claim['id']} supersedes itself")

    for conflict in conflicts:
        for source_id in conflict.get("sources", []):
            if source_id not in source_ids:
                errors.append(f"conflict {conflict['id']} references missing source {source_id}")
        for claim_id in conflict.get("affected_claims", []):
            if claim_id not in claim_ids:
                errors.append(f"conflict {conflict['id']} references missing claim {claim_id}")

    for event in events:
        for source_id in event.get("sources", []):
            if source_id not in source_ids:
                errors.append(f"timeline {event['id']} references missing source {source_id}")
        for claim_id in event.get("claims_added", []):
            if claim_id not in claim_ids:
                errors.append(f"timeline {event['id']} references missing claim {claim_id}")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", event.get("date", "")):
            errors.append(f"timeline {event['id']} has invalid date")

    if len(event_ids) != len(events):
        errors.append("timeline has duplicate ids")

    if errors:
        print("knowledge validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(
        f"knowledge ok: vendors={len(vendors)} sources={len(sources)} "
        f"claims={len(claims)} conflicts={len(conflicts)} events={len(events)}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
