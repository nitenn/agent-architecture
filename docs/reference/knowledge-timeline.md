# Agent 架构知识时间线

> 自动生成。新事件按时间倒序排列；未来事件保留 `scheduled` 状态。

## 2026-11-30 · OpenAI Agent Builder 计划关闭

- 厂商/来源: `openai`
- 类型: `scheduled-change`
- 状态: `scheduled`
- 摘要: 过渡期结束后旧 Builder 入口失效，长期实现转向 Agents API / Agents SDK。
- 证据: [OpenAI Agent Builder and deprecation status](https://developers.openai.com/api/docs/guides/agent-builder) · [OpenAI Building Agents](https://developers.openai.com/tracks/building-agents)

## 2026-11-24 · Salesforce 首次观察 Agentic Enterprise 11 层 IT 架构

- 厂商/来源: `salesforce`
- 类型: `architecture-framework`
- 状态: `observed`
- 摘要: 首次观察官方架构文档：在传统 IT 层之外增加 Agentic、Semantic、AI/ML 与企业编排层；Agentic Layer 负责运行时、推理、记忆、工具与 Agent 注册，企业编排层采用集中治理与本地 MCP/A2A 编排相结合的 blended orchestration。页面未显示明确发布日期，日期采用首次观察日。
- 证据: [The Agentic Enterprise - The IT Architecture for the AI-Powered Future](https://architect.salesforce.com/docs/architect/fundamentals/guide/agentic-enterprise-it-architecture) · [Enterprise Agentic Architecture](https://architect.salesforce.com/docs/architect/fundamentals/guide/enterprise-agentic-architecture)

## 2026-11-23 · 智谱旧智能体开发平台下线，Z Managed Agents 成为当前入口

- 厂商/来源: `zhipu`
- 类型: `product-lifecycle`
- 状态: `published`
- 摘要: 官方文档标记旧平台已下线；首次观察 Z Managed Agents 以 Agent/Environment/Session/Events 提供云沙箱、工具权限、记忆和 Multi Agent。日期采用首次观察日，因未找到统一下线日。
- 证据: [Z Managed Agents](https://docs.bigmodel.cn/cn/managed-agents/overview) · [智谱智能体开发平台（已下线）](https://docs.bigmodel.cn/cn/guide/platform/intelligent-agent)

## 2026-11-23 · OpenAI Agents SDK v1.0.0-alpha.2 引入可恢复会话与工具执行钩子

- 厂商/来源: `openai`
- 类型: `runtime-preview`
- 状态: `preview`
- 摘要: ResumableSession 将对话历史与待审批动作一起持久化，允许替换 Worker 恢复；工具执行新增输入/输出钩子、声明过滤和 required PreToolUse 阻断，并提供文本脱敏与细粒度 tracing。恢复仍受同一工作区、权限、工具与 hooks 条件约束，外部副作用必须由应用核对，且新持久化格式要求先升级读取方。
- 证据: [OpenAI Agents SDK Releases](https://github.com/openai/openai-agents-python/releases.atom)

## 2026-11-23 · Kimi Hosted Agents 将 Agent Harness 作为托管服务提供

- 厂商/来源: `moonshot`
- 类型: `product-runtime`
- 状态: `published`
- 摘要: 首次观察 Kimi Hosted Agents 产品文档：平台负责 Agent loop、会话、记忆与编排，工具在云沙箱或企业自托管 Worker 执行。日期采用首次观察日。
- 证据: [Kimi Hosted Agents](https://platform.kimi.com/docs/hosted-agents/overview) · [Moonshot / Kimi 开放平台文档](https://platform.moonshot.cn/docs)

## 2026-11-22 · Agent 厂商情报系统建立初始基线

- 厂商/来源: `research`
- 类型: `system-baseline`
- 状态: `baseline`
- 摘要: 建立 20 家厂商、官方组件信号、协议、论文与评测来源的持续监测基线。
- 证据: [OpenAI Agents API Architecture](https://developers.openai.com/api/docs/guides/agents-api/architecture) · [Microsoft Agent Harness](https://learn.microsoft.com/en-us/agent-framework/concepts/harness) · [Anthropic Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) · [Google Agent Development Kit](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/adk) · [Amazon Bedrock AgentCore Harness](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness.html) · [阿里云百炼 Agent 服务概览](https://help.aliyun.com/zh/model-studio/agent-overview) · [火山方舟 Managed Agents](https://docs.volcengine.com/docs/ark/define-agent?lang=zh) · [腾讯云智能体开发平台 ADP 产品概述](https://cloud.tencent.com/document/product/1759/104193) · [百度千帆 AppBuilder](https://cloud.baidu.com/doc/APPBUILDER/index.html) · [华为云 AgentArts Managed Agents](https://support.huaweicloud.com/managedagents-agentarts/agentarts_13_0001.html)

## 2026-11-20 · 50 个 Agent Harness/Runtime 的恢复机制公开证据审计

- 厂商/来源: `research`
- 类型: `research-paper`
- 状态: `published`
- 摘要: 128 次真实使用报告仅 19 次完整恢复、54 次部分恢复、45 次失败；checkpoint/resume 与 rollback 均有高失败率，外部副作用补偿缺少产品级证据。
- 证据: [Exercised, Rarely Recovered](https://arxiv.org/abs/2611.27090v1) · [arXiv - Agent Harness](https://export.arxiv.org/api/query?search_query=all:%22agent%20harness%22&sortBy=submittedDate&sortOrder=descending&max_results=30)

## 2026-11-20 · Microsoft AutoGen 进入归档状态

- 厂商/来源: `microsoft`
- 类型: `lifecycle-change`
- 状态: `published`
- 摘要: GitHub 官方仓库横幅显示 AutoGen 于 2026-11-20 归档；官方不建议新项目继续以其为主框架，迁移到 MAF 或 AG2。
- 证据: [Microsoft AutoGen Repository Status](https://github.com/microsoft/autogen) · [Microsoft Agent Framework Overview](https://learn.microsoft.com/en-us/agent-framework/overview/)

## 2026-11-20 · ACP v2 进入 Preview

- 厂商/来源: `standards`
- 类型: `protocol-preview`
- 状态: `preview`
- 摘要: 新增前台/后台工作状态、child session 子 Agent、replay_complete 与幂等 prompt 重试；v2 与 v1 通过版本协商并存。
- 证据: [ACP v2 Preview](https://agentclientprotocol.com/announcements/acp-v2-preview) · [Agent Client Protocol](https://agentclientprotocol.com/)

## 2026-11-03 · IBM watsonx Orchestrate Agent Identity 正式 GA

- 厂商/来源: `ibm`
- 类型: `security-governance-release`
- 状态: `published`
- 摘要: 每个 Agent 可注册独立身份到 IBM Verify 或 Microsoft Entra；运行时以限定到用户与 Agent 的 OAuth token exchange 访问企业系统。GA 新增逐 Agent 审计日志与 kill switch，后者的单步操作会下线 Agent 并结束活动会话，同时提示可能受影响的协作 Agent。
- 证据: [Agent Identity in IBM watsonx Orchestrate is now generally available](https://www.ibm.com/new/announcements/agent-identity-in-ibm-watsonx-orchestrate-is-now-generally-available)

## 2026-09-11 · 澳大利亚网络安全中心发布 Agentic AI Harnesses 指南

- 厂商/来源: `standards`
- 类型: `security-guidance`
- 状态: `published`
- 摘要: 把 Harness 作为数据、工具、权限、记忆、计划与治理的软件层，并给出安全控制建议。
- 证据: [Agentic AI harnesses security guidance](https://www.cyber.gov.au/news/asd-releases-new-guidance-on-the-agentic-ai-harnesses)

## 2026-07-28 · MCP 2026-07-28 规范切换为无状态核心

- 厂商/来源: `standards`
- 类型: `protocol-release`
- 状态: `published`
- 摘要: 移除 initialize/initialized 与 Mcp-Session-Id，每个请求自包含版本与能力；引入 server/discover、Multi Round-Trip Requests、Extensions 与 Tasks。
- 证据: [Model Context Protocol Specification](https://modelcontextprotocol.io/specification/2026-07-28)

## 2026-07-16 · IBM watsonx Orchestrate 将 ReAct Core 设为默认 Agent 风格

- 厂商/来源: `ibm`
- 类型: `official-changelog`
- 状态: `published`
- 摘要: 2026-07 中期版本开始分批部署 ReAct Core 默认风格、AgentOps 评测优化部署循环与统一 A2A 连接管理；旧 Default/ReAct 被弃用。
- 证据: [IBM watsonx Orchestrate What's New](https://www.ibm.com/docs/en/watsonx/watson-orchestrate/base?topic=notes-whats-new)

## 2026-04-15 · OpenAI 发布 Agents SDK 演进

- 厂商/来源: `openai`
- 类型: `official-blog`
- 状态: `published`
- 摘要: 引入模型原生 Harness、原生沙箱执行、文件和工具运行时。
- 证据: [The next evolution of the Agents SDK](https://openai.com/index/the-next-evolution-of-the-agents-sdk/)

## 2026-03-10 · LangChain 发布 Agent Harness 解剖

- 厂商/来源: `research`
- 类型: `industry-research`
- 状态: `published`
- 摘要: 将 Harness 拆成文件系统、代码执行、沙箱、记忆和上下文管理等工程原语。
- 证据: [The Anatomy of an Agent Harness](https://www.langchain.com/blog/the-anatomy-of-an-agent-harness)

## 2026-02-15 · 华为云 ModelArts Studio Agent 开发模块下线

- 厂商/来源: `huawei`
- 类型: `lifecycle-change`
- 状态: `published`
- 摘要: Agent 开发能力迁移到 AgentArts；旧实现入口失效。
- 证据: [华为云 ModelArts Studio Agent 开发模块下线通知](https://www.huaweicloud.com/notice/2025/20260114164756418.html) · [华为云 AgentArts Managed Agents](https://support.huaweicloud.com/managedagents-agentarts/agentarts_13_0001.html)

## 2026-01-15 · OpenAI 发布 Practical Guide to Building Agents

- 厂商/来源: `openai`
- 类型: `official-research`
- 状态: `published`
- 摘要: 强调渐进式复杂度、单/多 Agent 选择、工具设计、护栏和人工审查。
- 证据: [OpenAI Building Agents](https://developers.openai.com/tracks/building-agents)

## 2026-01-09 · Anthropic 发布 Agent Evals 指南

- 厂商/来源: `anthropic`
- 类型: `official-research`
- 状态: `published`
- 摘要: 明确 task/trial/grader/transcript/outcome，以及 Evaluation Harness 的基础设施角色。
- 证据: [Demystifying evals for AI agents](https://www.anthropic.com/research/demystifying-evals-for-ai-agents)

## 2024-12-19 · Anthropic 发布 Building Effective Agents

- 厂商/来源: `anthropic`
- 类型: `official-research`
- 状态: `published`
- 摘要: 提出 workflow 与 agent 的工程分界、五种工作流模式和 ACI 原则。
- 证据: [Anthropic Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
