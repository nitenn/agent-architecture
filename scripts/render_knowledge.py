#!/usr/bin/env python3
"""Render machine-readable knowledge records into reference Markdown."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE = ROOT / "knowledge"
DOCS = ROOT / "docs" / "reference"


def load(name: str) -> dict:
    return json.loads((KNOWLEDGE / name).read_text(encoding="utf-8"))


def source_link(source: dict) -> str:
    return f"[{source.get('title', source['id'])}]({source['url']})"


def main() -> int:
    vendors_doc = load("vendors.json")
    sources_doc = load("sources.json")
    claims_doc = load("claims.json")
    conflicts_doc = load("conflicts.json")
    vendors = {vendor["id"]: vendor for vendor in vendors_doc["vendors"]}
    sources = {source["id"]: source for source in sources_doc["sources"]}
    tiers = {tier["id"]: tier for tier in vendors_doc["tiers"]}
    source_counts = Counter(source["vendor_id"] for source in sources_doc["sources"])

    DOCS.mkdir(parents=True, exist_ok=True)
    vendor_lines = [
        "# 大厂 Agent 架构来源矩阵",
        "",
        f"> 自动生成。更新时间：{vendors_doc['updated_at']}。",
        "",
        "评级说明：`docs_maturity` 表示官方文档的覆盖程度；`open_source_signal` 表示官方开源实现/规范的活跃度；`enterprise_signal` 表示企业运行时、治理与部署信息密度。它们是信息覆盖度，不是产品质量评分。",
        "",
    ]
    for tier_id, tier in tiers.items():
        members = [vendor for vendor in vendors.values() if vendor["tier"] == tier_id]
        if not members:
            continue
        vendor_lines.extend(
            [
                f"## {tier['label']}",
                "",
                tier["description"],
                "",
                "| 厂商 | 地区 | 优先级 | Agent 重点 | 文档 | 开源信号 | 企业信号 | 来源数 |",
                "| --- | --- | --- | --- | --- | --- | --- | ---: |",
            ]
        )
        for vendor in sorted(members, key=lambda item: (item["watch_priority"], item["name"])):
            vendor_lines.append(
                f"| {vendor['name']} | {vendor['country']} | {vendor['watch_priority']} | "
                f"{vendor['agent_positioning']} | {vendor['docs_maturity']} | "
                f"{vendor['open_source_signal']} | {vendor['enterprise_signal']} | "
                f"{source_counts[vendor['id']]} |"
            )
        vendor_lines.append("")

    vendor_lines.extend(["## 官方来源索引", ""])
    for vendor in sorted(vendors.values(), key=lambda item: (item["tier"], item["watch_priority"], item["name"])):
        vendor_lines.extend([f"### {vendor['name']}", ""])
        for source_id in vendor.get("source_ids", []):
            source = sources.get(source_id)
            if source:
                vendor_lines.append(f"- **{source['category']}** · {source_link(source)} · `{source['priority']}`")
        vendor_lines.append("")
    (DOCS / "vendor-source-matrix.md").write_text("\n".join(vendor_lines), encoding="utf-8")

    claim_lines = [
        "# 知识主张账本",
        "",
        f"> 自动生成。更新时间：{claims_doc['updated_at']}。",
        "",
        "本账本是当前可维护的说法集合。`status=active` 表示当前采用；`superseded` 只在历史追溯时保留。",
        "",
    ]
    for topic in sorted({claim["topic"] for claim in claims_doc["claims"]}):
        claim_lines.extend([f"## {topic}", ""])
        for claim in sorted(
            [item for item in claims_doc["claims"] if item["topic"] == topic],
            key=lambda item: item["id"],
        ):
            links = [source_link(sources[source_id]) for source_id in claim["sources"] if source_id in sources]
            claim_lines.extend(
                [
                    f"### {claim['statement']}",
                    "",
                    f"- ID: `{claim['id']}`",
                    f"- 状态: `{claim['status']}`",
                    f"- 置信度: `{claim['confidence']}`",
                    f"- 首次观察: {claim['first_observed']}",
                    f"- 最近核验: {claim['last_verified']}",
                    f"- 来源: {' · '.join(links) if links else '—'}",
                ]
            )
            if claim.get("supersedes"):
                claim_lines.append(f"- Supersedes: {', '.join(f'`{value}`' for value in claim['supersedes'])}")
            if claim.get("notes"):
                claim_lines.append(f"- 说明: {claim['notes']}")
            claim_lines.append("")
    (DOCS / "claims-ledger.md").write_text("\n".join(claim_lines), encoding="utf-8")

    events = []
    for line in (KNOWLEDGE / "timeline.jsonl").read_text(encoding="utf-8").splitlines():
        if line.strip():
            events.append(json.loads(line))
    timeline_lines = [
        "# Agent 架构知识时间线",
        "",
        "> 自动生成。新事件按时间倒序排列；未来事件保留 `scheduled` 状态。",
        "",
    ]
    for event in sorted(events, key=lambda item: (item["date"], item["id"]), reverse=True):
        links = [source_link(sources[source_id]) for source_id in event.get("sources", []) if source_id in sources]
        timeline_lines.extend(
            [
                f"## {event['date']} · {event['title']}",
                "",
                f"- 厂商/来源: `{event['vendor_id']}`",
                f"- 类型: `{event['type']}`",
                f"- 状态: `{event['status']}`",
                f"- 摘要: {event['summary']}",
                f"- 证据: {' · '.join(links) if links else '—'}",
                "",
            ]
        )
    (DOCS / "knowledge-timeline.md").write_text("\n".join(timeline_lines), encoding="utf-8")

    conflict_lines = [
        "# 知识冲突与推翻记录",
        "",
        f"> 自动生成。更新时间：{conflicts_doc['updated_at']}。",
        "",
        "当新官方来源与旧结论冲突时，不删除历史，而是记录旧结论、新结论、变化日期、证据和推翻原因。",
        "",
    ]
    for conflict in sorted(conflicts_doc["conflicts"], key=lambda item: item["observed_date"], reverse=True):
        links = [source_link(sources[source_id]) for source_id in conflict["sources"] if source_id in sources]
        conflict_lines.extend(
            [
                f"## {conflict['topic']}",
                "",
                f"- ID: `{conflict['id']}`",
                f"- 变化日期: {conflict['change_date']}",
                f"- 观察日期: {conflict['observed_date']}",
                f"- 旧结论: {conflict['old_claim']}",
                f"- 新结论: {conflict['new_claim']}",
                f"- 推翻原因: {conflict['reason']}",
                f"- 证据: {' · '.join(links) if links else '—'}",
                f"- 处理: `{conflict['resolution']}`",
                "",
            ]
        )
    (DOCS / "conflict-log.md").write_text("\n".join(conflict_lines), encoding="utf-8")
    print("rendered: vendor-source-matrix.md, claims-ledger.md, knowledge-timeline.md, conflict-log.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
