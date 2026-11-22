# AI Agent 架构知识库

本仓库是「主流 Agent 架构」的版本化知识项目（仓库根 = 本目录）。

> GitHub：<https://github.com/nitenn/agent-architecture>
> Harness 专题已拆分为独立仓库：<https://github.com/nitenn/harness-architecture>

## 目录结构

```
├─ docs/
│  ├─ explanation/          # 解释型：机制与原理（主文档）
│  │  └─ agent-architecture.md
│  ├─ how-to/               # 操作型：搭建与选型（指南）
│  │  └─ task-fit-and-build.md
│  ├─ reference/            # 参考型：来源清单 / 交接文档
│  │  ├─ official-sources.md
│  │  └─ handover.md
│  └─ tutorials/            # 入门型（预留）
├─ research/
│  ├─ official-readmes/     # 官方 README/规范存档（23 份）
│  └─ notes/                # 调研笔记（预留）
├─ knowledge/               # 可持续更新的厂商源、主张、时间线与冲突账本
│  ├─ vendors.json          # 大厂分层与关注重点
│  ├─ sources.json          # 官方文档、博客、Release、论文与标准源
│  ├─ claims.json           # 当前知识主张与证据
│  ├─ timeline.jsonl        # 事件时间线
│  ├─ conflicts.json        # 新旧结论冲突和推翻原因
│  ├─ state/                # 页面哈希、最近核验时间、快照状态
│  └─ monitor/              # 每日监测报告与待处理变化
├─ assets/                  # 图片/图表
├─ scripts/                 # 构建脚本
├─ exports/                 # 生成物（html/pdf/docx）
├─ official-docs/           # 大体积官方文档库（git 忽略，清单见 docs/reference/official-sources.md）
└─ README.md / AGENTS.md
```

## 文档再生成

```powershell
python scripts/render_knowledge.py
python scripts/validate_knowledge.py
python scripts/check_links.py
python scripts/build_collapsible.py   # -> exports/html/
python scripts/md_to_docx.py          # -> exports/docx/
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/build_pdf.ps1
```

## 大厂 Agent 架构情报系统

- [大厂 Agent 架构版图](docs/explanation/agent-vendor-landscape.md)
- [大厂来源矩阵](docs/reference/vendor-source-matrix.md)
- [知识主张账本](docs/reference/claims-ledger.md)
- [知识时间线](docs/reference/knowledge-timeline.md)
- [冲突与推翻记录](docs/reference/conflict-log.md)
- [知识治理与每日更新规范](docs/reference/knowledge-governance.md)

每日扫描：

> 已在 Codex 中创建每日 `08:30` 的“Agent 厂商官方源每日监测”任务；无结论变化时不会制造知识更新。

```powershell
python scripts/monitor_sources.py
python scripts/render_knowledge.py
python scripts/validate_knowledge.py
python scripts/build_collapsible.py
python scripts/md_to_docx.py
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/build_pdf.ps1
```

## 官方文档库更新（稀疏克隆模板）

```powershell
git clone --depth 1 --filter=tree:0 --sparse <官方仓库URL> "official-docs\<架构名>"
cd "official-docs\<架构名>"
git sparse-checkout set --no-cone 'docs/' '/*.md'
```

## 约定

- 内容只来自官方仓库/官方文档/论文，不引入媒体或第三方整理；
- 官方文档库体积大，仅通过 docs/reference/official-sources.md 记录来源，不随仓库提交；
- 目录按 Diátaxis 四类组织：新增文档先归类（explanation / how-to / reference / tutorial）。
