# 知识冲突与推翻记录

> 自动生成。更新时间：2026-11-23。

当新官方来源与旧结论冲突时，不删除历史，而是记录旧结论、新结论、变化日期、证据和推翻原因。

## Microsoft AutoGen 归档日期

- ID: `conflict-autogen-archive-date-correction`
- 变化日期: 2026-11-20
- 观察日期: 2026-11-23
- 旧结论: AutoGen 的归档日期记录为 2026-10-28。
- 新结论: GitHub 官方仓库横幅显示 AutoGen 于 2026-11-20 归档。
- 推翻原因: 官方仓库页面直接显示归档日期，优先于此前未保留完整证据的日期记录；归档状态本身不变。
- 证据: [Microsoft AutoGen Repository Status](https://github.com/microsoft/autogen)
- 处理: `corrected`

## MCP 传输与会话模型

- ID: `conflict-mcp-stateless-2026`
- 变化日期: 2026-07-28
- 观察日期: 2026-11-23
- 旧结论: MCP 基座是 JSON-RPC 2.0、有状态连接与 initialize/initialized 能力协商（2025-06-18 规范）。
- 新结论: MCP 2026-07-28 规范改为无状态、自包含请求核心，移除 initialize/initialized 与 Mcp-Session-Id，并要求请求自行携带协议版本与能力。
- 推翻原因: 官方 2026-07-28 规范与 changelog 明确移除协议级 session 和初始化握手；继续把 2025-06-18 的有状态连接描述为当前模型会误导实现。
- 证据: [Model Context Protocol Specification](https://modelcontextprotocol.io/specification/2026-07-28)
- 处理: `superseded`

## 智谱 Agent 平台代际

- ID: `conflict-zhipu-managed-agents`
- 变化日期: 2026-11-23
- 观察日期: 2026-11-23
- 旧结论: 智谱智能体开发平台是当前可继续使用的 Agent 构建入口。
- 新结论: 原智能体开发平台已下线；当前官方入口是 Z Managed Agents。
- 推翻原因: 官方页面标题和正文均标记旧平台已下线，并明确引导迁移到 Managed Agents；未找到统一下线日期，change_date 暂采用首次观察日。
- 证据: [智谱智能体开发平台（已下线）](https://docs.bigmodel.cn/cn/guide/platform/intelligent-agent) · [Z Managed Agents](https://docs.bigmodel.cn/cn/managed-agents/overview)
- 处理: `superseded`

## Microsoft AutoGen 生命周期

- ID: `conflict-autogen-archive-2026`
- 变化日期: 2026-10-28
- 观察日期: 2026-11-22
- 旧结论: AutoGen 是可继续用于新项目的对话式多智能体框架。
- 新结论: AutoGen 已归档，新项目应迁移 Microsoft Agent Framework 或 AG2。
- 推翻原因: 微软官方仓库状态和迁移说明取代旧教程、旧框架介绍；继续把 AutoGen 作为新项目默认选项会引入维护与安全风险。
- 证据: [Microsoft AutoGen Repository Status](https://github.com/microsoft/autogen) · [Microsoft Agent Framework Overview](https://learn.microsoft.com/en-us/agent-framework/overview/)
- 处理: `superseded`

## Amazon Bedrock Agents 产品代际

- ID: `conflict-aws-bedrock-agents-classic`
- 变化日期: 2026-11-22
- 观察日期: 2026-11-22
- 旧结论: Bedrock Agents Classic 是 AWS Agent 构建的主要入口。
- 新结论: Agents Classic 已进入维护模式，迁移目标是 Amazon Bedrock AgentCore harness。
- 推翻原因: 官方维护模式页面明确说明迁移路径；新架构提供 runtime、identity、gateway、memory 和 observability 等独立运行层能力。
- 证据: [Amazon Bedrock Agents Classic Maintenance Mode](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-classic-maintenance-mode.html) · [Amazon Bedrock AgentCore Harness](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness.html) · [What is Amazon Bedrock AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html)
- 处理: `superseded`

## Huawei ModelArts Studio Agent 模块

- ID: `conflict-huawei-modelarts-agent-offline`
- 变化日期: 2026-02-15
- 观察日期: 2026-11-22
- 旧结论: ModelArts Studio 可作为华为云 Agent 开发入口。
- 新结论: ModelArts Studio Agent 开发模块已下线，当前入口是 AgentArts。
- 推翻原因: 华为云官方公告给出下线时间，并指向 AgentArts 全生命周期平台。
- 证据: [华为云 ModelArts Studio Agent 开发模块下线通知](https://www.huaweicloud.com/notice/2025/20260114164756418.html) · [华为云 AgentArts Managed Agents](https://support.huaweicloud.com/managedagents-agentarts/agentarts_13_0001.html)
- 处理: `superseded`

## OpenAI Agent Builder 生命周期

- ID: `conflict-openai-agent-builder-sunset`
- 变化日期: 2026-11-30
- 观察日期: 2026-11-22
- 旧结论: Agent Builder 可作为长期 Agent 工作流构建入口。
- 新结论: Agent Builder 计划于 2026-11-30 关闭，长期入口是 Agents API / Agents SDK。
- 推翻原因: OpenAI 官方页面给出计划关闭日期，并建议下载 Agents SDK 代码自部署；保留 Builder 作为当前默认会产生时间线上必然失效的知识。
- 证据: [OpenAI Agent Builder and deprecation status](https://developers.openai.com/api/docs/guides/agent-builder) · [OpenAI Building Agents](https://developers.openai.com/tracks/building-agents)
- 处理: `superseded`
