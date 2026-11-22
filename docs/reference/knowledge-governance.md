# 知识治理与每日更新规范

## 目标

把“大厂 Agent 架构信息”维护成可追溯、可更新、可推翻、可比较的长期知识系统，而不是一次性链接清单。

## 来源分级

### A 级：事实正源

- 厂商官方产品文档；
- 厂商官方研究论文/技术报告；
- 官方工程博客、发布说明、弃用公告；
- 官方 GitHub 仓库、Release 与协议规范；
- 标准化组织、政府安全机构和顶级学术论文。

A 级来源可以直接改变 `claims.json` 中的事实判断。

### B 级：结构参考

- 行业技术博客；
- Awesome List；
- 源码拆解或案例研究；
- 社区基准榜单。

B 级来源只能用于发现问题、补充解释或提出待验证假设，不能单独推翻 A 级结论。

### C 级：弱信号

- 社媒、访谈、会议演讲问答；
- 二手报道；
- 未版本化的截图或摘要。

C 级必须标记为 `low confidence`，只进入时间线或监控候选，不直接进入正文。

## 时间线

每个事件至少记录：

- `date`：官方发布日期，不知道时用首次观察日期并在 `summary` 中说明；
- `vendor_id`；
- `type`：文档、论文、协议、发布、弃用、事故、基准等；
- `title` / `summary`；
- `sources`：可点击来源；
- `claims_added`；
- `status`：`published`、`baseline`、`scheduled`、`withdrawn`。

## 冲突与推翻

当新内容与旧结论冲突时：

1. 不删除旧记录；
2. 新建 `conflict` 条目；
3. 写清旧结论、新结论、变化日期、观察日期和官方证据；
4. 写清“新内容为什么推翻旧结论”，例如官方归档、下线、API 弃用、能力边界变化；
5. 更新 `claims.json` 中受影响 claim 的 `status`、`supersedes`、`last_verified`；
6. 重新生成时间线和冲突日志。

## 每日自动任务

每日任务只做四类动作：

1. **扫描**：运行 `scripts/monitor_sources.py`；
2. **核验**：只打开变化来源及其关联官方页面；
3. **更新**：更新 sources、timeline、claims、conflicts 与受影响的 Markdown；
4. **重建**：生成 HTML、DOCX、PDF 并提交 Git。

没有明确官方证据时，任务只能把条目放入待确认状态，不能凭空更新事实。

## 来源健康

- 抓取失败连续 3 天：在 `sources.json` 中标记 `monitor_health: broken`；
- 页面长期 404：查找迁移入口并记录冲突；
- 动态页面无法稳定比较：改用官方 `llms.txt`、Markdown、RSS、Release Atom 或 API；
- 官方内容存在版本号时，将版本写入来源备注或时间线摘要。
