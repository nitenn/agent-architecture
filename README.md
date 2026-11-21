# AI Agent / Harness 架构知识库

本仓库是「主流 Agent 架构 + Harness 相关知识」的版本化知识项目（仓库根 = 本目录）。

## 目录结构

| 路径 | 内容 |
| --- | --- |
| 主流Agent架构整理.md | 主文档（官方来源版 · 深度讲解，10 章） |
| 主流Agent架构·任务适配与搭建指南.md | 配套指南（适合任务/搭建细节/关键节点） |
| *·折叠版.html | 两份文档的可折叠网页版 |
| 主流Agent架构整理.pdf / .docx | 主文档导出物 |
| _research/ | 官方 README/规范存档（47 份） |
| docs-manifest.md | 官方文档库（28 个来源）清单 |
| 官方文档库/ | 本地官方文档归档（955MB，**不入库**，见 .gitignore） |
| build_collapsible.py / md_to_docx.py | 折叠版 HTML 与 DOCX 生成脚本 |

> 本仓库位于 D:\AI工具\02-本质层\04-知识库\08-人工智能与智能体\主流Agent架构；D:\AI\agent架构 仅保留壳与指针，不放正文副本。

## 文档再生成

```powershell
python build_collapsible.py
python md_to_docx.py
# PDF 使用 office-export-pdf 技能的 LibreOffice Kit 转换
```

## 官方文档库更新（稀疏克隆模板）

```powershell
git clone --depth 1 --filter=tree:0 --sparse <官方仓库URL> "官方文档库\<架构名>"
cd "官方文档库\<架构名>"
git sparse-checkout set --no-cone 'docs/' '/*.md'
```

## 约定

- 内容只来自官方仓库/官方文档/论文，不引入媒体或第三方整理；
- 官方文档库体积大，仅通过 docs-manifest.md 记录来源，不随仓库提交。
