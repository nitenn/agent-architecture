# Agent 架构知识时间线

> 自动生成。新事件按时间倒序排列；未来事件保留 `scheduled` 状态。

## 2026-11-30 · OpenAI Agent Builder 计划关闭

- 厂商/来源: `openai`
- 类型: `scheduled-change`
- 状态: `scheduled`
- 摘要: 过渡期结束后旧 Builder 入口失效，长期实现转向 Agents API / Agents SDK。
- 证据: [OpenAI Agent Builder and deprecation status](https://developers.openai.com/api/docs/guides/agent-builder) · [OpenAI Building Agents](https://developers.openai.com/tracks/building-agents)

## 2026-11-22 · Agent 厂商情报系统建立初始基线

- 厂商/来源: `research`
- 类型: `system-baseline`
- 状态: `baseline`
- 摘要: 建立 20 家厂商、官方组件信号、协议、论文与评测来源的持续监测基线。
- 证据: [OpenAI Agents API Architecture](https://developers.openai.com/api/docs/guides/agents-api/architecture) · [Microsoft Agent Harness](https://learn.microsoft.com/en-us/agent-framework/concepts/harness) · [Anthropic Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) · [Google Agent Development Kit](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/adk) · [Amazon Bedrock AgentCore Harness](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness.html) · [阿里云百炼 Agent 服务概览](https://help.aliyun.com/zh/model-studio/agent-overview) · [火山方舟 Managed Agents](https://docs.volcengine.com/docs/ark/define-agent?lang=zh) · [腾讯云智能体开发平台 ADP 产品概述](https://cloud.tencent.com/document/product/1759/104193) · [百度千帆 AppBuilder](https://cloud.baidu.com/doc/APPBUILDER/index.html) · [华为云 AgentArts Managed Agents](https://support.huaweicloud.com/managedagents-agentarts/agentarts_13_0001.html)

## 2026-10-28 · Microsoft AutoGen 进入归档状态

- 厂商/来源: `microsoft`
- 类型: `lifecycle-change`
- 状态: `published`
- 摘要: 官方不建议新项目继续以 AutoGen 为主框架，迁移到 MAF 或 AG2。
- 证据: [Microsoft AutoGen Repository Status](https://github.com/microsoft/autogen) · [Microsoft Agent Framework Overview](https://learn.microsoft.com/en-us/agent-framework/overview/)

## 2026-09-11 · 澳大利亚网络安全中心发布 Agentic AI Harnesses 指南

- 厂商/来源: `standards`
- 类型: `security-guidance`
- 状态: `published`
- 摘要: 把 Harness 作为数据、工具、权限、记忆、计划与治理的软件层，并给出安全控制建议。
- 证据: [Agentic AI harnesses security guidance](https://www.cyber.gov.au/news/asd-releases-new-guidance-on-the-agentic-ai-harnesses)

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
