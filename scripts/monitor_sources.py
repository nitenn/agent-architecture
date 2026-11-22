#!/usr/bin/env python3
"""Poll official agent sources and produce a review report.

Only standard-library dependencies are used so the job can run without a venv.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE = ROOT / "knowledge"
STATE_PATH = KNOWLEDGE / "state" / "source_state.json"
SNAPSHOT_DIR = KNOWLEDGE / "state" / "snapshots"
REPORT_DIR = KNOWLEDGE / "monitor" / "reports"
LATEST_PATH = KNOWLEDGE / "monitor" / "latest.json"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/131.0 Safari/537.36 CodexKnowledgeMonitor/1.0"
)


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_skip = 0
        self.title = ""
        self._in_title = False
        self.parts: list[str] = []
        self.meta_description = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "noscript", "svg"}:
            self.in_skip += 1
        if tag == "title":
            self._in_title = True
        if tag == "meta":
            values = {key.lower(): (value or "") for key, value in attrs}
            if values.get("name", "").lower() == "description":
                self.meta_description = values.get("content", "")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript", "svg"} and self.in_skip:
            self.in_skip -= 1
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_skip:
            return
        if self._in_title:
            self.title += data
        else:
            value = data.strip()
            if value:
                self.parts.append(value)

    def text(self) -> str:
        return normalize_text(" ".join(self.parts))


def normalize_text(value: str) -> str:
    value = html.unescape(value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def fetch(url: str, timeout: int) -> tuple[bytes, str]:
    request = Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/atom+xml,application/xml,text/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        },
    )
    with urlopen(request, timeout=timeout) as response:
        return response.read(), response.headers.get_content_type()


def extract_html(body: bytes) -> tuple[str, str]:
    text = body.decode("utf-8", errors="replace")
    parser = TextExtractor()
    parser.feed(text)
    title = normalize_text(parser.title)
    content = parser.text()
    if parser.meta_description:
        content = normalize_text(parser.meta_description + " " + content)
    return title, content


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1].lower()


def extract_feed(body: bytes) -> tuple[str, list[dict[str, str]]]:
    root = ET.fromstring(body)
    feed_title = ""
    entries: list[dict[str, str]] = []

    for node in root.iter():
        if local_name(node.tag) == "title" and not feed_title and node.text:
            feed_title = normalize_text(node.text)
            break

    for item in root.iter():
        if local_name(item.tag) not in {"entry", "item"}:
            continue
        values: dict[str, str] = {}
        for child in list(item):
            name = local_name(child.tag)
            if name == "link":
                href = child.attrib.get("href") or (child.text or "")
                if href and "url" not in values:
                    values["url"] = href
            elif name in {"id", "guid", "title", "updated", "published", "pubdate", "summary", "content"}:
                key = "id" if name in {"id", "guid"} else name
                if key not in values:
                    values[key] = normalize_text("".join(child.itertext()))
        entry_id = values.get("id") or values.get("url") or values.get("title", "")
        if entry_id:
            entries.append(
                {
                    "id": entry_id,
                    "title": values.get("title", ""),
                    "url": values.get("url", ""),
                    "published": values.get("published") or values.get("pubdate") or values.get("updated", ""),
                    "summary": values.get("summary") or values.get("content", ""),
                }
            )
    return feed_title, entries[:100]


def extract_github_commits(body: bytes) -> tuple[str, list[dict[str, str]]]:
    payload = json.loads(body.decode("utf-8"))
    entries = []
    for item in payload:
        commit = item.get("commit", {})
        message = (commit.get("message") or "").splitlines()[0]
        entries.append(
            {
                "id": item.get("sha", ""),
                "title": message,
                "url": item.get("html_url", ""),
                "published": (commit.get("author") or {}).get("date", ""),
                "summary": message,
            }
        )
    return "GitHub commits", entries


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def poll_source(source: dict[str, Any], timeout: int) -> dict[str, Any]:
    result: dict[str, Any] = {
        "source_id": source["id"],
        "vendor_id": source.get("vendor_id", "unknown"),
        "source_title": source.get("title", source["id"]),
        "url": source["url"],
        "priority": source.get("priority", "P2"),
        "kind": source.get("kind", "html"),
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "ok": False,
        "error": "",
    }
    try:
        body, content_type = fetch(source["url"], int(source.get("timeout", timeout)))
        kind = source.get("kind", "html")
        if kind == "atom":
            title, entries = extract_feed(body)
            text = "\n".join(
                f"{entry['published']} | {entry['title']} | {entry['url']} | {entry['summary']}"
                for entry in entries
            )
            result.update(
                {
                    "ok": True,
                    "page_title": title or result["source_title"],
                    "text": text,
                    "hash": digest(text),
                    "entries": entries,
                    "content_type": content_type,
                }
            )
        elif kind == "github_commits":
            title, entries = extract_github_commits(body)
            text = "\n".join(
                f"{entry['published']} | {entry['title']} | {entry['url']}"
                for entry in entries
            )
            result.update(
                {
                    "ok": True,
                    "page_title": title,
                    "text": text,
                    "hash": digest(text),
                    "entries": entries,
                    "content_type": content_type,
                }
            )
        else:
            title, text = extract_html(body)
            result.update(
                {
                    "ok": True,
                    "page_title": title or result["source_title"],
                    "text": text,
                    "hash": digest(text),
                    "entries": [],
                    "content_type": content_type,
                }
            )
    except (HTTPError, URLError, TimeoutError, ET.ParseError, ValueError) as exc:
        result["error"] = f"{type(exc).__name__}: {exc}"
    return result


def render_report(
    run_date: str,
    changes: list[dict[str, Any]],
    errors: list[dict[str, Any]],
    manual_review: list[dict[str, Any]],
    baseline: bool,
) -> str:
    lines = [
        f"# Agent 官方源监测报告 · {run_date}",
        "",
        f"> 生成时间：{datetime.now(timezone.utc).isoformat()}",
        "",
        "## 摘要",
        "",
        f"- 模式：{'初始基线' if baseline else '增量扫描'}",
        f"- 内容变化源：{len(changes)}",
        f"- 抓取失败源：{len(errors)}",
        f"- 需人工/搜索复核源：{len(manual_review)}",
        "",
    ]
    if changes:
        lines.extend(["## 内容变化", ""])
        for change in changes:
            lines.extend(
                [
                    f"### {change['source_title']}",
                    "",
                    f"- source_id: `{change['source_id']}`",
                    f"- vendor: `{change['vendor_id']}`",
                    f"- priority: `{change['priority']}`",
                    f"- type: `{change['change_type']}`",
                    f"- URL: {change['url']}",
                ]
            )
            if change.get("new_items"):
                lines.append("- 新增条目：")
                for item in change["new_items"][:20]:
                    lines.append(f"  - {item.get('published', '')} · [{item.get('title', '')}]({item.get('url', '')})")
            lines.append("")
    else:
        lines.extend(["## 内容变化", "", "无新增或变化。", ""])

    if errors:
        lines.extend(["## 抓取失败", ""])
        for error in errors:
            lines.append(f"- `{error['source_id']}` · {error['url']} · {error['error']}")
        lines.append("")

    if manual_review:
        lines.extend(["## 需人工/搜索复核", ""])
        for source in manual_review:
            lines.append(f"- `{source['id']}` · {source['title']} · {source['url']}")
        lines.append("")

    lines.extend(
        [
            "## 下一步",
            "",
            "1. 逐条打开变化来源，确认它是否属于官方 Agent 架构信号。",
            "2. 对照 `knowledge/claims.json` 判断是新增、补充还是冲突。",
            "3. 若冲突，写入 `knowledge/conflicts.json`，说明新证据为何推翻旧结论，并更新 claim 状态。",
            "4. 追加 `knowledge/timeline.jsonl`，运行 `python scripts/render_knowledge.py`。",
            "5. 重建 HTML/DOCX/PDF，并提交 Git。",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--only-p0", action="store_true")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--init", action="store_true", help="Treat all sources as baseline.")
    args = parser.parse_args()

    config = load_json(KNOWLEDGE / "sources.json", {"sources": []})
    all_sources = config["sources"]
    manual_review = [
        source
        for source in all_sources
        if source.get("manual_review") and not source.get("monitor", True)
    ]
    sources = [
        source
        for source in all_sources
        if source.get("monitor", True)
    ]
    if args.only_p0:
        sources = [source for source in sources if source.get("priority") == "P0"]
    if args.limit > 0:
        sources = sources[: args.limit]

    previous = load_json(STATE_PATH, {"sources": {}})
    previous_sources = previous.get("sources", {})
    results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as executor:
        futures = {executor.submit(poll_source, source, args.timeout): source for source in sources}
        for future in as_completed(futures):
            results.append(future.result())

    baseline_mode = args.init or not previous_sources
    changes: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    next_sources: dict[str, Any] = {} if args.init else dict(previous_sources)
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)

    for result in sorted(results, key=lambda item: (item["priority"], item["source_id"])):
        source_id = result["source_id"]
        old = previous_sources.get(source_id, {})
        if not result["ok"]:
            errors.append(result)
            next_sources[source_id] = {**old, "last_checked": result["checked_at"], "last_error": result["error"]}
            continue

        snapshot = SNAPSHOT_DIR / f"{source_id}.txt"
        snapshot.write_text(result["text"], encoding="utf-8")
        old_hash = old.get("hash")
        old_entry_ids = set(old.get("entry_ids", []))
        new_entry_ids = [entry["id"] for entry in result.get("entries", [])]
        new_items = [entry for entry in result.get("entries", []) if entry["id"] not in old_entry_ids]

        changed = False
        change_type = ""
        if not baseline_mode and old_hash and old_hash != result["hash"]:
            changed = True
            change_type = "content_changed"
        if not baseline_mode and result.get("entries") and new_items:
            changed = True
            change_type = "new_feed_items"

        if changed:
            changes.append(
                {
                    **{key: result[key] for key in ("source_id", "vendor_id", "source_title", "url", "priority", "kind")},
                    "change_type": change_type,
                    "old_hash": old_hash,
                    "new_hash": result["hash"],
                    "new_items": new_items,
                    "snapshot_path": str(snapshot.relative_to(ROOT)),
                }
            )

        next_sources[source_id] = {
            "hash": result["hash"],
            "entry_ids": new_entry_ids,
            "title": result.get("page_title", ""),
            "last_checked": result["checked_at"],
            "last_changed": result["checked_at"] if changed else old.get("last_changed", ""),
            "last_error": "",
        }

    state = {
        "schema_version": 1,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "sources": dict(sorted(next_sources.items())),
    }
    write_json(STATE_PATH, state)

    report = render_report(args.date, changes, errors, manual_review, baseline_mode)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORT_DIR / f"{args.date}.md"
    report_path.write_text(report, encoding="utf-8")
    write_json(
        LATEST_PATH,
        {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "date": args.date,
            "baseline": baseline_mode,
            "report_path": str(report_path.relative_to(ROOT)),
            "changes": changes,
            "errors": errors,
            "manual_review": manual_review,
        },
    )
    print(
        f"sources={len(sources)} changes={len(changes)} errors={len(errors)} "
        f"manual_review={len(manual_review)} baseline={baseline_mode}"
    )
    print(f"report={report_path.relative_to(ROOT)}")
    return 0

if __name__ == "__main__":
    sys.exit(main())

