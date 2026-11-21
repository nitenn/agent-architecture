# 本仓库约定（AI 会话必读）

## 定位

「主流 Agent 架构 + Harness」知识库；仓库根即本目录，git 分支 main。

## 硬性规则

1. 内容只来自官方仓库 / 官方文档 / 论文原文；不得引入媒体或第三方整理；
2. 官方文档库（official-docs/，955MB）不提交，来源以 docs/reference/official-sources.md 为准；
3. 修改 docs/ 后必须同步重建 exports/（scripts/build_collapsible.py、scripts/md_to_docx.py，PDF 用 LibreOffice Kit）；
4. 目录遵循 Diátaxis：explanation（为什么）/ how-to（怎么做）/ reference（查什么）/ tutorials（入门）。

## 常用命令

```powershell
python scripts/build_collapsible.py
python scripts/md_to_docx.py
git add -A; git commit -m "..."
```
