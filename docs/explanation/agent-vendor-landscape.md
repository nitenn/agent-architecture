# 大厂 Agent 架构版图

> 初始基线：2026-11-22；最近核验：2026-11-24。厂商能力和产品状态会变化，动态结果以 [大厂来源矩阵](../reference/vendor-source-matrix.md) 和时间线为准。

## 比较方法

本版图不按模型跑分排序，而按厂商「对 Agent 架构的可复用贡献」比较：

- 是否提出稳定的架构范式或协议；
- 是否提供可落地的 SDK、Runtime 或托管平台；
- 是否公开长任务、沙箱、记忆、上下文、权限、评估与观测细节；
- 是否持续更新官方文档、Release 和弃用公告；
- 是否存在可运行的参考实现或源码。

## 一、架构定义与前沿研究

### OpenAI

关注重点：

- Agents API、Agents SDK、Codex Harness；
- 控制面与执行环境分离；
- Sessions、tools、handoffs、guardrails、tracing、evals；
- Agents SDK v1.0.0-alpha.2 的 ResumableSession、跨 Worker 待审批恢复、工具执行钩子与文本脱敏；
- MCP 与多 Agent 协作。

OpenAI 的文档对「托管 Harness」「Agent 循环」「执行环境」的边界描述较清晰，适合作为生产平台架构参考。alpha.2 把会话、待审批状态和工具钩子写入运行时契约，但仍要求应用在恢复后核对部分编辑与外部副作用。

### Anthropic

关注重点：

- workflow 与 agent 的分界；
- 五种工作流模式；
- MCP；
- 长任务 Harness；
- Agent Evals、可信 Agent、权限与容器隔离。

Anthropic 的优势是工程原则与架构边界，尤其适合防止“一上来就做全自主 Agent”。

### Google / DeepMind

关注重点：

- Agent Development Kit（ADK）；
- Gemini Enterprise Agent Platform / Agent Runtime；
- A2A；
- 多语言、图工作流、评估与部署。

Google 的价值主要在开放协议、跨语言工具链和企业运行时。

### Microsoft

关注重点：

- Microsoft Agent Framework（MAF）；
- Agent Harness / Pipeline；
- multi-agent workflows；
- Microsoft Foundry、Agent 365、企业身份与治理。

Microsoft 强调把 Harness 组合到既有 Agent Framework 和上下文提供者之上，而不是另造黑盒运行时。

### Meta AI

关注重点：

- Muse 个人 Agent；
- Secure VM 与持久电脑；
- 跨应用、后台任务和人在关键步骤接管；
- 工具生成。

Meta 更接近“个人 Agent + 持久执行环境”的产品路线。

### xAI

关注重点：

- Grok API 工具调用；
- Realtime Multi-Agent Research；
- Grok Build 终端 Coding Agent；
- Grok Bot 云电脑团队。

xAI 的产品线同时覆盖 API、多 Agent 研究、终端 Agent 和长期 Bot，适合观察“模型 + 工具 + 云端执行面”的组合。

### Mistral AI

关注重点：

- Managed Agents；
- Agents API / SDK；
- Studio、Workflow、Evaluation、Deploy；
- MCP、Connector 与工具调用。

Mistral 把 Agent 产品与模型、工作流、评估、部署组织成较完整的应用平台，适合观察欧洲企业市场的 Agent 工程路线。

### Cohere

关注重点：

- Command 模型的工具计划与工具调用；
- 企业 RAG、检索和私有部署；
- Agent 构建示例与 SDK。

Cohere 的架构信号更偏企业 RAG 与工具调用基础能力，而不是完整自主 Agent Runtime。

### DeepSeek

关注重点：

- DeepSeek API；
- DeepSeek Harness 的插件化架构；
- dsh-superagent 的 Trigger、Gate、Mandate、Ticket 与恢复机制。

DeepSeek 的案例对“长期常驻 Agent 如何被授权和收敛”特别有价值。Harness 细节维护在独立的 [Harness 架构知识库](https://github.com/nitenn/harness-architecture)。

## 二、云与企业 Agent 平台

### AWS

- Amazon Bedrock AgentCore；
- 托管 Harness；
- Runtime、Gateway、Identity、Memory、Registry；
- Strands Agents；
- MCP / A2A 互操作。

AWS 的架构重点已经从“单一 Agent 产品”转向“Agent 基础设施套件”。

### Microsoft

除 MAF 外，Microsoft 还在 Agent 身份、企业治理、Foundry 和多语言托管方面形成企业层信号。

### NVIDIA

- NeMo Agent Toolkit；
- NIM；
- Agent Blueprints；
- 企业内、云、边缘的部署。

NVIDIA 的重点是模型服务、工具链和行业参考蓝图。

### IBM

- watsonx Orchestrate；
- ReAct Core 已成为推荐默认 Agent 风格，旧 Default/ReAct 被弃用；
- AgentOps 把评测、提示词优化与部署组织为闭环；
- Agent Identity 已 GA：独立 Agent 身份注册到 IBM Verify 或 Microsoft Entra，按用户与 Agent 限定的 OAuth token exchange、逐 Agent 审计日志与 kill switch；
- 企业 Agent、预置 Agent、A2A 连接管理、发现与评估。

IBM 适合观察传统企业软件中的 Agent 生命周期治理与“默认执行风格”迁移；Agent Identity 进一步把身份、委托、审计和紧急停用拆成可治理的控制面能力。

### Salesforce

- Agentforce；
- Atlas Reasoning Engine；
- Agentic Enterprise 11 层 IT 架构；
- blended orchestration：集中式企业编排与本地 Agent 通过 MCP/A2A 自主协作并存；
- MCP/A2A、Data 360、Trust Layer。

Salesforce 的强项是把 Agent 嵌入 CRM、业务流程和企业数据边界，并把 Agent Runtime、语义层、AI/ML 层与企业编排层显式分层。

## 三、中国 Agent 平台与模型厂商

### 阿里云 / Qwen

- 百炼 Agent 2.0；
- Managed Agents；
- Flow Agent；
- MCP；
- Agent API 与 IaC；
- Qwen-Agent 开源生态。

阿里云覆盖零代码、托管运行时和开源 Agent 工具链，是当前国内资料最完整的平台之一。

### 字节跳动 / 火山引擎

- 火山方舟 Managed Agents；
- Skills、Tools、MCP；
- 多 Agent 协作；
- 上下文压缩；
- 长时任务与会话产物。

其托管 Agent 架构对长时、有状态、异步任务描述较具体。

### 腾讯云

- 腾讯云 ADP；
- 标准、单工作流、Multi-Agent、Claw 模式；
- 知识库、工具、评测和私有化。

腾讯云更强调企业级应用全生命周期与业务落地。

### 百度

- 千帆 AppBuilder / Agent 开发平台；
- RAG、工作流、UI Builder；
- 零代码、低代码、高代码。

百度的主线是搜索与知识增强、应用构建效率和企业集成。

### 华为云

- AgentArts；
- Managed Agents；
- IAM 执行委托；
- 记忆插件；
- OBS 运行时会话存储。

华为云的架构信号集中在托管运行时、权限、存储和企业生命周期。

### 智谱

- 原智能体开发平台已下线，不再是当前实现入口；
- Z Managed Agents：Agent、Environment、Session、Events；
- 云沙箱、版本化 Agent、Skills、MCP、工具权限、Vault、记忆与 Multi Agent；
- AutoClaw 桌面 Agent。

智谱现已同时覆盖云端托管 Agent Runtime 与桌面 Agent，适合观察“平台 Agent”和“个人电脑 Agent”两条执行面。

### Moonshot / Kimi、MiniMax、讯飞

作为专项信号跟踪：

- Kimi：Hosted Agents 将 Harness 作为服务提供；平台负责 Agent loop、编排、会话与记忆，工具在云沙箱或企业自托管 Worker 执行；
- Kimi 仍保留长上下文、工具调用与 Agentic 编程能力；
- MiniMax：Agentic Coding、多模态、并行专业 Agent；
- 讯飞：工作流 Agent、发布渠道、MCP Server。

## 四、除了官方产品文档还应记录什么

### 1. 官方研究论文与技术报告

论文先于产品文档暴露新架构，例如记忆、反思、搜索、长任务、Agent 评测和上下文压缩。

### 2. 官方工程博客与事故复盘

工程博客通常解释真实生产约束、性能数字、失败模式和架构演变；事故复盘能揭示产品文档看不到的风险。

### 3. Release、Changelog 与弃用公告

它们决定“旧知识何时失效”。任何关于 API、Agent Builder、Runtime 或协议的生命周期变化都应进入时间线。

### 4. 参考实现与 SDK

观察 Agent Loop、工具接口、状态模型、沙箱权限和持久化机制的真实实现，而不是只看产品宣传页。

### 5. 协议与标准

- MCP：工具与上下文接入；2026-07-28 规范已转为无状态请求核心；
- A2A：Agent 间互操作；
- AG-UI：Agent 与前端事件流，1.0 已稳定；
- ACP：编辑器与 Agent 会话协议，v1 稳定并已有 v2 Preview。

### 6. 基准与评测

关注任务、trial、grader、trace、outcome，以及 Harness 本身对结果的影响，而不是只抄排行榜。

### 7. 安全与治理

HITL、最小权限、沙箱、网络出口、提示注入、工具审批、审计、数据边界和 Agent 身份。

### 8. 成本与运营

步数、token、工具调用、缓存、并发、沙箱启动、失败重试和每次成功任务的成本。

### 9. 参考架构与生产案例

尤其是长运行 Coding Agent、企业知识库、客服、数据分析、SRE 和跨系统工作流。

### 10. 路线图与产品生命周期

旧入口下线、框架归档、API 合并、默认参数变化，往往比新增功能更能影响架构选择。

## 维护结论

一个“最前沿 Agent 知识库”不能只存摘要。它至少要同时维护：

1. 来源；
2. 时间；
3. 证据等级；
4. 当前主张；
5. 冲突与推翻原因；
6. 受影响的架构建议；
7. 下一次核验条件。

本项目通过 `knowledge/` 的机器可读账本和每日自动扫描实现这七项。
