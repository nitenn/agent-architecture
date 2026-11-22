# 知识冲突与推翻记录

> 自动生成。更新时间：2026-11-22。

当新官方来源与旧结论冲突时，不删除历史，而是记录旧结论、新结论、变化日期、证据和推翻原因。

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
