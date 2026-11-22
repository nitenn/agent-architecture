# Knowledge Data Model

本目录是知识正文之前的机器可读事实层。

| 文件 | 作用 |
| --- | --- |
| `vendors.json` | 大厂分层、地区、Agent 重点、文档/开源/企业信号与优先级 |
| `sources.json` | 官方文档、研究、Release、协议、论文、评测与安全来源 |
| `claims.json` | 当前知识主张、置信度、证据和 supersedes 链 |
| `timeline.jsonl` | 按日期记录事件、产品变化、论文和生命周期 |
| `conflicts.json` | 新旧结论冲突、变化日期、推翻原因与受影响 claim |
| `state/source_state.json` | 页面或 Feed 的哈希、最近核验时间和最近变化时间 |
| `monitor/latest.json` | 最近一次扫描的结构化变化与人工复核队列 |
| `monitor/reports/` | 每日可读报告 |

## 更新顺序

```text
来源变化 → sources/timeline → claims/conflicts → Markdown 正文 → exports
```

禁止直接改写正文而跳过证据层。
