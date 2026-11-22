# 交接文档（仓库版）

> 本目录是项目 git 仓库根（2026-11-21 初始化，2026-11-21 按 Diátaxis 目录重构）：知识正文与交付物均在仓库内；官方文档库在 official-docs/，仅以 official-sources.md 记录来源、不入库。

## 关键事实

- 仓库根：D:\AI工具\02-本质层\04-知识库\08-人工智能与智能体\主流Agent架构（main）
- GitHub：https://github.com/nitenn/agent-architecture
- 文档：docs/explanation/agent-architecture.md（主文档）+ docs/how-to/task-fit-and-build.md（指南）
- 参考：docs/reference/official-sources.md（27 个官方来源）、docs/reference/handover.md（本文）
- 官方文档库：official-docs/（git 忽略）
- D:\AI\agent架构 仅保留壳与指针，不放正文副本
- Harness 专题：D:\AI\harness架构；GitHub：https://github.com/nitenn/harness-architecture

## 再生成

python scripts/build_collapsible.py → exports/html/
python scripts/md_to_docx.py → exports/docx/
PDF：LibreOffice Kit → exports/pdf/

## 接手第一步

1. 读 README.md 与本文；
2. 查证官方原文：official-docs/ 或 official-sources.md 中的官方站点；
3. 改动后 git add -A && git commit（main）。
