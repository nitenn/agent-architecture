# 知识主张账本

> 自动生成。更新时间：2026-11-23。

本账本是当前可维护的说法集合。`status=active` 表示当前采用；`superseded` 只在历史追溯时保留。

## Harness 设计

### 工具接口、上下文预算、状态持久化、权限和验证应作为一等设计对象，而不是提示词之外的事后补丁。

- ID: `claim-tool-context-first-class`
- 状态: `active`
- 置信度: `high`
- 首次观察: 2026-11-22
- 最近核验: 2026-11-23
- 来源: [Anthropic Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) · [Microsoft Agent Harness](https://learn.microsoft.com/en-us/agent-framework/concepts/harness) · [Effective harnesses for long-running agents](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents) · [Enterprise Agentic Architecture](https://architect.salesforce.com/docs/architect/fundamentals/guide/enterprise-agentic-architecture) · [Z Managed Agents](https://docs.bigmodel.cn/cn/managed-agents/overview) · [Kimi Hosted Agents](https://platform.kimi.com/docs/hosted-agents/overview)
- 说明: 来自多厂商文档与工程实践的归纳；托管平台把沙箱、会话、记忆和权限策略显式产品化。

## 协议分层

### MCP 主要解决模型/Agent 与工具和上下文之间的接入，A2A 主要解决 Agent 与 Agent 之间的互操作；两者是互补层，不是替代关系。

- ID: `claim-mcp-a2a-layers`
- 状态: `active`
- 置信度: `high`
- 首次观察: 2026-11-22
- 最近核验: 2026-11-23
- 来源: [Model Context Protocol Specification](https://modelcontextprotocol.io/specification/2026-07-28) · [Agent2Agent Protocol Specification](https://a2a-protocol.org/latest/specification/) · [Google Agent Development Kit](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/adk)
- 说明: AG-UI 负责前端交互，ACP 负责编辑器客户端接入；MCP 2026-07-28 已把协议核心改为无状态请求模型。

## 协议架构

### ACP v2 Preview 把会话扩展为可同时运行前台与后台工作的长期执行单元，将子 Agent 暴露为 child session，并定义 replay_complete 与幂等 prompt 重试；v2 与 v1 通过版本协商并存。

- ID: `claim-acp-v2-preview`
- 状态: `active`
- 置信度: `high`
- 首次观察: 2026-11-20
- 最近核验: 2026-11-23
- 来源: [ACP v2 Preview](https://agentclientprotocol.com/announcements/acp-v2-preview) · [Agent Client Protocol](https://agentclientprotocol.com/)
- 说明: v2 仍是 Preview，官方承诺尽量少做大破坏性变更但尚未冻结。

### 自 2026-07-28 规范起，MCP 使用无状态、自包含请求核心：移除 initialize/initialized 与 Mcp-Session-Id；每个请求携带协议版本和客户端能力，跨调用状态由服务器显式签发 handle。

- ID: `claim-mcp-stateless-2026`
- 状态: `active`
- 置信度: `high`
- 首次观察: 2026-07-28
- 最近核验: 2026-11-23
- 来源: [Model Context Protocol Specification](https://modelcontextprotocol.io/specification/2026-07-28)
- Supersedes: `claim-mcp-stateful-2025`
- 说明: server/discover 可选，Multi Round-Trip Requests 用 input_required 结果替代旧的服务端发起请求模式。

## 持久化与恢复

### 公开报告审计显示，恢复机制普遍存在且会被使用，但完整恢复仍少：50 个 runtime/harness 的 128 次真实报告中仅 19 次完整恢复，54 次部分恢复、45 次失败。

- ID: `claim-recovery-not-guaranteed`
- 状态: `active`
- 置信度: `medium`
- 首次观察: 2026-11-20
- 最近核验: 2026-11-23
- 来源: [Exercised, Rarely Recovered](https://arxiv.org/abs/2611.27090v1) · [arXiv - Agent Harness](https://export.arxiv.org/api/query?search_query=all:%22agent%20harness%22&sortBy=submittedDate&sortOrder=descending&max_results=30)
- 说明: 证据来自公开使用报告的系统审计，不等同于受控故障注入实验；外部副作用补偿尤其缺少产品级证据。

## 架构选择

### 当任务路径可以预定义时，应优先使用 workflow；只有步骤不可预测、需要运行中依据环境动态决策时，才引入自主 Agent。

- ID: `claim-workflow-before-agent`
- 状态: `active`
- 置信度: `high`
- 首次观察: 2024-12-19
- 最近核验: 2026-11-22
- 来源: [Anthropic Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) · [OpenAI Building Agents](https://developers.openai.com/tracks/building-agents)
- 说明: Anthropic 的核心工程原则；OpenAI 的实际指南也强调渐进式复杂度。

## 概念边界

### Agent Harness 是模型之外的运行时支架，负责驱动模型与工具循环、维护会话和上下文、施加审批与停止条件，并支持多步任务持续推进。

- ID: `claim-harness-runtime-scaffold`
- 状态: `active`
- 置信度: `high`
- 首次观察: 2026-11-22
- 最近核验: 2026-11-23
- 来源: [Microsoft Agent Harness](https://learn.microsoft.com/en-us/agent-framework/concepts/harness) · [OpenAI Agents API Architecture](https://developers.openai.com/api/docs/guides/agents-api/architecture) · [Trustworthy agents in practice](https://www.anthropic.com/research/trustworthy-agents) · [Z Managed Agents](https://docs.bigmodel.cn/cn/managed-agents/overview) · [Kimi Hosted Agents](https://platform.kimi.com/docs/hosted-agents/overview)
- 说明: 跨厂商共同要素；托管平台进一步把 Harness 本身作为服务提供，具体能力范围仍因产品而异。

### “Agent = Model + Harness”适合作为工程分解，但它是行业归纳，不是所有厂商共同发布的正式标准定义。

- ID: `claim-model-plus-harness-synthesis`
- 状态: `active`
- 置信度: `high`
- 首次观察: 2026-11-22
- 最近核验: 2026-11-22
- 来源: [OpenAI Agents API Architecture](https://developers.openai.com/api/docs/guides/agents-api/architecture) · [Microsoft Agent Harness](https://learn.microsoft.com/en-us/agent-framework/concepts/harness) · [Anthropic Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
- 说明: 文档中必须区分官方定义与本文归纳。

## 评测

### Agent Harness 与 Evaluation Harness 是两个层次：前者运行生产 Agent，后者负责并发运行评测任务、记录轨迹、评分和聚合结果。

- ID: `claim-eval-harness-distinct`
- 状态: `active`
- 置信度: `high`
- 首次观察: 2026-01-09
- 最近核验: 2026-11-22
- 来源: [Demystifying evals for AI agents](https://www.anthropic.com/research/demystifying-evals-for-ai-agents)
- 说明: 用于避免把测试底座与 Agent 运行时混为一谈。

## 运行时架构

### 生产级 Agent 系统正在把控制面（会话、策略、编排、审计）与执行面（沙箱、文件、网络、工具）分离，以支持托管、自托管和混合部署。

- ID: `claim-control-execution-separation`
- 状态: `active`
- 置信度: `medium`
- 首次观察: 2026-11-22
- 最近核验: 2026-11-23
- 来源: [OpenAI Agents API Architecture](https://developers.openai.com/api/docs/guides/agents-api/architecture) · [What is Amazon Bedrock AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html) · [Microsoft Agent Harness](https://learn.microsoft.com/en-us/agent-framework/concepts/harness) · [Z Managed Agents](https://docs.bigmodel.cn/cn/managed-agents/overview) · [Kimi Hosted Agents](https://platform.kimi.com/docs/hosted-agents/overview)
- 说明: 跨厂商架构归纳；智谱与 Kimi 的托管 Agent 进一步验证控制面/执行面分离，具体分界仍不同。

### IBM watsonx Orchestrate 在 2026-07 更新中将 ReAct Core 设为推荐默认 Agent 风格，旧 Default/ReAct 被弃用，并把 evaluation、optimization、deployment 组织为 AgentOps 循环。

- ID: `claim-ibm-react-core-default`
- 状态: `active`
- 置信度: `high`
- 首次观察: 2026-07-16
- 最近核验: 2026-11-23
- 来源: [IBM watsonx Orchestrate What's New](https://www.ibm.com/docs/en/watsonx/watson-orchestrate/base?topic=notes-whats-new)
- 说明: 同一版本还提供统一 A2A 连接管理；区域自 2026-07-16 起分批部署。

### Kimi Hosted Agents 将 Agent Harness 作为托管服务提供，把模型、编排、会话与记忆留在平台控制面，并支持云沙箱或企业自托管环境执行工具。

- ID: `claim-moonshot-hosted-agents`
- 状态: `active`
- 置信度: `high`
- 首次观察: 2026-11-23
- 最近核验: 2026-11-23
- 来源: [Kimi Hosted Agents](https://platform.kimi.com/docs/hosted-agents/overview)
- 说明: 官方定位为 Harness as a Service；自托管环境只把沙箱工具放到企业主机，Agent loop 仍在云端。

## 项目生命周期

### Microsoft AutoGen 已归档，不再作为新生产项目的主框架；官方迁移路径是 Microsoft Agent Framework，社区替代包括 AG2。

- ID: `claim-autogen-archived`
- 状态: `active`
- 置信度: `high`
- 首次观察: 2026-11-20
- 最近核验: 2026-11-23
- 来源: [Microsoft AutoGen Repository Status](https://github.com/microsoft/autogen) · [Microsoft Agent Framework Overview](https://learn.microsoft.com/en-us/agent-framework/overview/)
- Supersedes: `claim-autogen-active`
- 说明: GitHub 官方仓库横幅显示归档日期为 2026-11-20；此前 2026-10-28 的记录已由冲突日志纠正。

### Amazon Bedrock Agents Classic 已进入维护模式，官方提供迁移到 AgentCore harness 的路径。

- ID: `claim-bedrock-classic-maintenance`
- 状态: `active`
- 置信度: `high`
- 首次观察: 2026-11-22
- 最近核验: 2026-11-22
- 来源: [Amazon Bedrock Agents Classic Maintenance Mode](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-classic-maintenance-mode.html) · [Amazon Bedrock AgentCore Harness](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness.html)
- Supersedes: `claim-bedrock-agents-classic-active`
- 说明: 新项目应评估 AgentCore 与 Strands。

### 华为云 ModelArts Studio 的 Agent 开发模块已下线，Agent 开发能力迁移到 AgentArts/Versatile。

- ID: `claim-huawei-agentarts-migration`
- 状态: `active`
- 置信度: `high`
- 首次观察: 2026-02-15
- 最近核验: 2026-11-22
- 来源: [华为云 ModelArts Studio Agent 开发模块下线通知](https://www.huaweicloud.com/notice/2025/20260114164756418.html) · [华为云 AgentArts Managed Agents](https://support.huaweicloud.com/managedagents-agentarts/agentarts_13_0001.html)
- Supersedes: `claim-huawei-modelarts-agent-active`
- 说明: 旧文档不能继续作为当前实现入口。

### OpenAI Agent Builder 计划于 2026-11-30 关闭；长期实现应迁移到 Agents API / Agents SDK。

- ID: `claim-openai-agent-builder-sunset`
- 状态: `active`
- 置信度: `high`
- 首次观察: 2026-11-22
- 最近核验: 2026-11-22
- 来源: [OpenAI Agent Builder and deprecation status](https://developers.openai.com/api/docs/guides/agent-builder) · [OpenAI Building Agents](https://developers.openai.com/tracks/building-agents)
- Supersedes: `claim-agent-builder-default`
- 说明: 过渡期内旧用户仍可使用。

### 智谱原智能体开发平台已下线；当前官方入口是 Z Managed Agents，以 Agent、Environment、Session、Events 四元组提供云端 Agent 循环、沙箱、权限、记忆与 Multi Agent。

- ID: `claim-zhipu-managed-agents-migration`
- 状态: `active`
- 置信度: `high`
- 首次观察: 2026-11-23
- 最近核验: 2026-11-23
- 来源: [Z Managed Agents](https://docs.bigmodel.cn/cn/managed-agents/overview) · [智谱智能体开发平台（已下线）](https://docs.bigmodel.cn/cn/guide/platform/intelligent-agent)
- Supersedes: `claim-zhipu-agent-platform-active`
- 说明: 官方未在页面给出统一下线日期；首次观察日期采用 2026-11-23，避免猜测。
