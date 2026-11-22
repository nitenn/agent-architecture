# 本仓库约定（AI 会话必读）

## 定位

「主流 Agent 架构」知识库；仓库根即本目录，git 分支 main。

## 硬性规则

1. 内容只来自官方仓库 / 官方文档 / 论文原文；不得引入媒体或第三方整理；
2. 官方文档库（official-docs/）不提交，来源以 docs/reference/official-sources.md 为准；
3. 修改 docs/ 后必须同步重建 exports/（scripts/build_collapsible.py、scripts/md_to_docx.py、scripts/build_pdf.ps1）；
4. 目录遵循 Diátaxis：explanation（为什么）/ how-to（怎么做）/ reference（查什么）/ tutorials（入门）。
5. 厂商动态与冲突必须写入 `knowledge/`：先更新 sources / timeline / claims / conflicts，再改正文；
6. 新结论与旧结论冲突时不得静默覆盖：必须写清旧结论、新结论、官方证据和推翻原因；
7. 日常监测只信 A 级来源（官方文档、官方研究、官方仓库/Release、标准与论文）；社区信息只能作为线索。

## 常用命令

```powershell
python scripts/build_collapsible.py
python scripts/md_to_docx.py
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/build_pdf.ps1
python scripts/monitor_sources.py
python scripts/render_knowledge.py
python scripts/validate_knowledge.py
python scripts/check_links.py
git add -A; git commit -m "..."
```
