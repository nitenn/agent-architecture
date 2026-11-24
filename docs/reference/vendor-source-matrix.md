# 大厂 Agent 架构来源矩阵

> 自动生成。更新时间：2026-11-23。

评级说明：`docs_maturity` 表示官方文档的覆盖程度；`open_source_signal` 表示官方开源实现/规范的活跃度；`enterprise_signal` 表示企业运行时、治理与部署信息密度。它们是信息覆盖度，不是产品质量评分。

## Tier 1 · 架构定义与前沿研究

持续定义 Agent 架构范式、协议、评测或大规模工程实践的头部基础模型实验室。

| 厂商 | 地区 | 优先级 | Agent 重点 | 文档 | 开源信号 | 企业信号 | 来源数 |
| --- | --- | --- | --- | --- | --- | --- | ---: |
| Anthropic | US | P0 | Claude Agent SDK、MCP、长任务 Harness、Agent 评测与可信 Agent | high | high | high | 5 |
| DeepSeek | CN | P0 | DeepSeek API、DeepSeek Harness 与 dsh-superagent 原型 | medium | high | medium | 3 |
| Google / Google DeepMind | US | P0 | Agent Development Kit、Gemini Enterprise Agent Platform、A2A 与 Agent Runtime | high | high | high | 3 |
| Microsoft | US | P0 | Microsoft Agent Framework、HarnessAgent、Foundry 与 Agent 365 | high | high | high | 6 |
| OpenAI | US | P0 | Agents API、Agents SDK、Codex Harness、AgentKit 与托管执行环境 | high | high | high | 6 |
| Meta AI | US | P1 | Muse 个人 Agent、Secure VM、跨应用任务执行与研究模型 | medium | high | medium | 2 |
| Mistral AI | FR | P1 | Managed Agents、Agents SDK、Studio、Workflow 与 MCP | high | high | high | 3 |
| xAI | US | P1 | Grok API 工具调用、多 Agent 研究、Grok Build 与 Grok Bot | medium | medium | medium | 4 |
| Cohere | CA | P2 | Command 工具调用、企业 RAG 与 Agent 构建路径 | medium | medium | high | 3 |

## Tier 1 · 企业与云 Agent 平台

提供 Agent Runtime、治理、沙箱、企业集成和规模化部署能力的云或企业软件厂商。

| 厂商 | 地区 | 优先级 | Agent 重点 | 文档 | 开源信号 | 企业信号 | 来源数 |
| --- | --- | --- | --- | --- | --- | --- | ---: |
| Amazon AWS | US | P0 | Amazon Bedrock AgentCore、Strands Agents、Agent Registry 与 Managed Agents | high | high | high | 5 |
| IBM | US | P1 | IBM watsonx Orchestrate、ReAct Core 默认 Agent 风格、AgentOps 与 A2A 连接管理 | high | medium | high | 5 |
| NVIDIA | US | P1 | NeMo Agent Toolkit、NIM、Blueprints 与企业 Agent 工具链 | medium | high | high | 4 |
| Salesforce | US | P1 | Agentforce、Atlas Reasoning Engine 与企业 Agentic Architecture | high | medium | high | 5 |

## Tier 1 · 中国 Agent 平台与模型厂商

在中国市场提供 Agent 开发、托管、工作流、模型服务和行业落地的核心厂商。

| 厂商 | 地区 | 优先级 | Agent 重点 | 文档 | 开源信号 | 企业信号 | 来源数 |
| --- | --- | --- | --- | --- | --- | --- | ---: |
| Alibaba Cloud / Qwen | CN | P0 | 阿里云百炼 Agent 2.0、Managed Agents、Flow Agent 与 Qwen-Agent | high | high | high | 4 |
| ByteDance / Volcengine | CN | P0 | 火山方舟 Managed Agents、Agent Toolkit、Skills、MCP 与多 Agent 协作 | high | medium | high | 3 |
| Huawei Cloud | CN | P0 | 智果 AgentArts、Managed Agents、工作流与记忆插件 | high | medium | high | 4 |
| Baidu | CN | P1 | 百度千帆 AppBuilder / Agent 开发平台、RAG、工作流与 Assistants API | high | medium | high | 3 |
| Tencent Cloud | CN | P1 | 腾讯云智能体开发平台 ADP、Multi-Agent、工作流与 Claw 模式 | high | medium | high | 3 |
| Zhipu AI / Z.AI | CN | P1 | Z Managed Agents 云端运行时、Agent/Environment/Session 模型与 AutoClaw 桌面 Agent | medium | high | medium | 3 |

## Tier 2 · 专项信号

在工具调用、多模态 Agent、长任务、桌面 Agent 或企业场景上具有独特信息的厂商。

| 厂商 | 地区 | 优先级 | Agent 重点 | 文档 | 开源信号 | 企业信号 | 来源数 |
| --- | --- | --- | --- | --- | --- | --- | ---: |
| MiniMax | CN | P2 | MiniMax Agent、全栈开发、多模态 Agent 与 API | medium | medium | medium | 3 |
| Moonshot AI / Kimi | CN | P2 | Kimi Hosted Agents、云/自托管沙箱、长上下文与 Agentic 编程工具链 | medium | medium | medium | 2 |
| iFlytek | CN | P2 | 讯飞星辰 Agent 开发平台、工作流、MCP Server 发布 | medium | low | high | 3 |

## 官方来源索引

### Anthropic

- **official-research** · [Anthropic Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) · `P0`
- **official-research** · [Demystifying evals for AI agents](https://www.anthropic.com/research/demystifying-evals-for-ai-agents) · `P0`
- **official-research** · [Trustworthy agents in practice](https://www.anthropic.com/research/trustworthy-agents) · `P0`
- **official-research** · [Effective harnesses for long-running agents](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents) · `P0`
- **official-releases** · [Claude Code Releases](https://github.com/anthropics/claude-code/releases.atom) · `P1`

### DeepSeek

- **official-docs** · [DeepSeek API Docs](https://api-docs.deepseek.com/zh-cn/) · `P0`
- **official-changelog** · [DeepSeek API Updates](https://api-docs.deepseek.com/zh-cn/updates/) · `P0`
- **official-releases** · [DeepSeek Harness Releases](https://github.com/deepseek-ai/deepseek-harness/releases.atom) · `P0`

### Google / Google DeepMind

- **official-docs** · [Google Agent Development Kit](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/adk) · `P0`
- **official-blog** · [Agent Development Kit: multi-agent applications](https://developers.googleblog.com/agent-development-kit-easy-to-build-multi-agent-applications/) · `P1`
- **official-releases** · [Google ADK Python Releases](https://github.com/google/adk-python/releases.atom) · `P0`
- **protocol** · [Agent2Agent Protocol Specification](https://a2a-protocol.org/latest/specification/) · `P0`

### Microsoft

- **official-docs** · [Microsoft Agent Framework Overview](https://learn.microsoft.com/en-us/agent-framework/overview/) · `P0`
- **official-docs** · [Microsoft Agent Harness](https://learn.microsoft.com/en-us/agent-framework/concepts/harness) · `P0`
- **official-docs** · [Microsoft Agent Pipeline Architecture](https://learn.microsoft.com/en-us/agent-framework/agents/agent-pipeline) · `P1`
- **official-blog** · [Microsoft Agent Framework Blog](https://devblogs.microsoft.com/agent-framework/) · `P0`
- **official-changelog** · [Microsoft Agent Framework Upgrade Guides](https://learn.microsoft.com/en-us/agent-framework/support/upgrade/) · `P0`

### OpenAI

- **official-docs** · [OpenAI Agents API Architecture](https://developers.openai.com/api/docs/guides/agents-api/architecture) · `P0`
- **official-docs** · [OpenAI Building Agents](https://developers.openai.com/tracks/building-agents) · `P0`
- **official-research** · [Harness Engineering](https://openai.com/index/harness-engineering/) · `P1`
- **official-releases** · [OpenAI Agents SDK Releases](https://github.com/openai/openai-agents-python/releases.atom) · `P0`

### Meta AI

- **official-product** · [Meta Muse personal AI agent](https://ai.meta.com/muse/) · `P1`
- **official-research** · [Meta AI Research](https://ai.meta.com/research/) · `P2`

### Mistral AI

- **official-docs** · [Mistral Managed Agents Overview](https://docs.mistral.ai/studio/agents/overview) · `P1`
- **official-docs** · [Mistral Agents API](https://docs.mistral.ai/studio/agents/agents-api) · `P1`
- **official-releases** · [Mistral Python Client Releases](https://github.com/mistralai/client-python/releases.atom) · `P1`

### xAI

- **official-docs** · [xAI API Overview](https://docs.x.ai/overview) · `P1`
- **official-docs** · [xAI Tools Overview](https://docs.x.ai/developers/tools/overview) · `P1`
- **official-docs** · [xAI Realtime Multi-Agent Research](https://docs.x.ai/developers/model-capabilities/text/multi-agent) · `P0`
- **official-product** · [Grok Build coding agent](https://docs.x.ai/build/overview) · `P1`

### Cohere

- **official-docs** · [Building an Agent with Cohere](https://docs.cohere.com/docs/building-an-agent-with-cohere) · `P1`
- **official-docs** · [Cohere Tool Use Quickstart](https://docs.cohere.com/docs/tool-use-quickstart) · `P1`
- **official-releases** · [Cohere Python Releases](https://github.com/cohere-ai/cohere-python/releases.atom) · `P2`

### Alibaba Cloud / Qwen

- **official-docs** · [阿里云百炼 Agent 服务概览](https://help.aliyun.com/zh/model-studio/agent-overview) · `P0`
- **official-docs** · [阿里云百炼 Managed Agents](https://help.aliyun.com/zh/model-studio/managed-agents-introduction) · `P0`
- **official-docs** · [阿里云百炼 Agent API](https://help.aliyun.com/zh/model-studio/agent-api/) · `P1`
- **official-releases** · [Qwen-Agent Releases](https://github.com/QwenLM/Qwen-Agent/releases.atom) · `P1`

### ByteDance / Volcengine

- **official-docs** · [火山方舟 Managed Agents](https://docs.volcengine.com/docs/ark/define-agent?lang=zh) · `P0`
- **official-docs** · [火山方舟 Managed Agents 概述](https://docs.volcengine.com/docs/ark/overview?lang=zh) · `P0`
- **official-toolkit** · [火山引擎 Agent Toolkit](https://docs.volcengine.com/docs/agent-toolkit/introduction?lang=zh) · `P1`

### Huawei Cloud

- **official-docs** · [华为云 AgentArts Managed Agents](https://support.huaweicloud.com/managedagents-agentarts/agentarts_13_0001.html) · `P0`
- **official-changelog** · [华为云 AgentArts 最新动态](https://support.huaweicloud.com/wtsnew-agentarts/index.html) · `P0`
- **official-docs** · [华为云 AgentArts 低代码单智能体](https://support.huaweicloud.com/lowcode-agentarts/agentarts_05_0017.html) · `P1`

### Baidu

- **official-docs** · [百度千帆 AppBuilder](https://cloud.baidu.com/doc/APPBUILDER/index.html) · `P1`
- **official-docs** · [百度千帆 Agent 创建方式](https://cloud.baidu.com/doc/qianfan/s/Lmh4stuli) · `P1`
- **official-docs** · [百度千帆 Agent 开发平台](https://cloud.baidu.com/doc/Qianfan/index.html) · `P1`

### Tencent Cloud

- **official-docs** · [腾讯云智能体开发平台 ADP 产品概述](https://cloud.tencent.com/document/product/1759/104193) · `P1`
- **official-docs** · [腾讯云 ADP 平台架构](https://cloud.tencent.com/document/product/1759/104194) · `P1`
- **official-docs** · [腾讯云 ADP 对话式应用开发与调优](https://cloud.tencent.com/document/product/1759/137902) · `P1`

### Zhipu AI / Z.AI

- **official-docs** · [智谱智能体开发平台（已下线）](https://docs.bigmodel.cn/cn/guide/platform/intelligent-agent) · `P1`
- **official-docs** · [Z Managed Agents](https://docs.bigmodel.cn/cn/managed-agents/overview) · `P0`
- **official-product** · [智谱 AutoClaw 桌面 Agent](https://autoclaw.zhipuai.cn/about/) · `P2`

### Amazon AWS

- **official-docs** · [Amazon Bedrock AgentCore Documentation](https://docs.aws.amazon.com/bedrock-agentcore/) · `P0`
- **official-docs** · [Amazon Bedrock AgentCore Harness](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness.html) · `P0`
- **official-docs** · [What is Amazon Bedrock AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html) · `P0`
- **official-releases** · [Strands Agents Releases](https://github.com/strands-agents/sdk-python/releases.atom) · `P1`

### IBM

- **official-product** · [IBM watsonx Agents](https://www.ibm.com/products/watsonx-orchestrate/ai-agents) · `P1`
- **official-docs** · [Introduction to AI agents in IBM watsonx Orchestrate](https://www.ibm.com/docs/en/watsonx/watson-orchestrate/base?topic=agents-introduction) · `P1`
- **official-docs** · [Building agents with IBM watsonx Orchestrate](https://www.ibm.com/docs/en/watsonx/watson-orchestrate/base?topic=agents-getting-started-building) · `P1`
- **official-changelog** · [IBM watsonx Orchestrate What's New](https://www.ibm.com/docs/en/watsonx/watson-orchestrate/base?topic=notes-whats-new) · `P0`
- **official-announcement** · [Agent Identity in IBM watsonx Orchestrate is now generally available](https://www.ibm.com/new/announcements/agent-identity-in-ibm-watsonx-orchestrate-is-now-generally-available) · `P0`

### NVIDIA

- **official-product** · [NVIDIA Agentic AI Solutions](https://www.nvidia.com/en-us/solutions/ai/agentic-ai/) · `P1`
- **official-reference** · [NVIDIA Agent Blueprints](https://build.nvidia.com/blueprints) · `P2`
- **official-docs** · [NVIDIA NIM for Agents](https://developer.nvidia.com/nim) · `P2`
- **official-releases** · [NeMo Agent Toolkit Releases](https://github.com/NVIDIA/NeMo-Agent-Toolkit/releases.atom) · `P1`

### Salesforce

- **official-docs** · [Enterprise Agentic Architecture](https://architect.salesforce.com/docs/architect/fundamentals/guide/enterprise-agentic-architecture) · `P1`
- **official-docs** · [The Agentic Enterprise - The IT Architecture for the AI-Powered Future](https://architect.salesforce.com/docs/architect/fundamentals/guide/agentic-enterprise-it-architecture) · `P1`
- **official-docs** · [Agentic Patterns on Salesforce](https://architect.salesforce.com/docs/architect/fundamentals/guide/agentic-patterns) · `P1`
- **official-docs** · [Agent Development Lifecycle](https://architect.salesforce.com/docs/architect/fundamentals/guide/agent-development-lifecycle) · `P2`
- **official-docs** · [The Building Blocks of Agentforce Agents](https://help.salesforce.com/s/articleView?id=ai.copilot_building_blocks.htm&language=en_US&type=5) · `P1`

### MiniMax

- **official-product** · [MiniMax M 系列 Agent 模型](https://www.minimaxi.com/models/text) · `P2`
- **official-docs** · [MiniMax API 对话文档](https://platform.minimaxi.com/document/ChatCompletion?key=667bdde33be2027f69b71d4c) · `P2`
- **official-blog** · [MiniMax Agent 新闻](https://www.minimaxi.com/news) · `P2`

### Moonshot AI / Kimi

- **official-docs** · [Moonshot / Kimi 开放平台文档](https://platform.moonshot.cn/docs) · `P2`
- **official-docs** · [Kimi Hosted Agents](https://platform.kimi.com/docs/hosted-agents/overview) · `P1`

### iFlytek

- **official-docs** · [讯飞星辰 Agent 开发平台介绍](https://www.xfyun.cn/doc/spark/Agent01-%E5%B9%B3%E5%8F%B0%E4%BB%8B%E7%BB%8D.html) · `P2`
- **official-docs** · [讯飞星辰 Agent 开发指南](https://www.xfyun.cn/doc/spark/Agent03-%E5%BC%80%E5%8F%91%E6%8C%87%E5%8D%97.html) · `P2`
- **official-docs** · [讯飞 Agent 平台 FAQ](https://www.xfyun.cn/doc/spark/Agent06-FAQ.html) · `P2`
