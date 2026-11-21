# AI Agent / Harness 架构知识库

本仓库是「主流 Agent 架构 + Harness 相关知识」的版本化知识项目（仓库根 = 本目录）。

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
│  ├─ official-readmes/     # 官方 README/规范存档（47 份）
│  └─ notes/                # 调研笔记（预留）
├─ assets/                  # 图片/图表
├─ scripts/                 # 构建脚本
├─ exports/                 # 生成物（html/pdf/docx）
├─ official-docs/           # 955MB 官方文档库（git 忽略，清单见 docs/reference/official-sources.md）
└─ README.md / AGENTS.md
```

## 文档再生成

```powershell
python scripts/build_collapsible.py   # -> exports/html/
python scripts/md_to_docx.py          # -> exports/docx/
# PDF：使用 office-export-pdf 技能的 LibreOffice Kit 转换到 exports/pdf/
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
