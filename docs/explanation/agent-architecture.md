# 主流 Agent 架构整理（官方来源版 · 深度讲解）

> **变更注记（2026-11-09，外部会话修订）**：按用户委托并经官方来源核验，本版补充 5.3 AG-UI / 5.4 ACP 协议节，修正 0.1（归纳框架标注）、1.2（并入第 2 章）、3.6（中性措辞）。修改清单与原因见《交接文档.md》第 0 节「外部修改记录」。

> **本版说明**：本版在官方来源版基础上，为**每一个架构**补充深度讲解（核心机制、工作原理、官方数据、设计取舍、相邻对比）。所有内容仍严格来自官方仓库/官方文档/论文原文，媒体与第三方信息已全部清除。GitHub 数据为 2026-11-03 经官方 API 抓取。

## 0. 全景图与统一心智模型

### 0.1 一切 Agent 的内核：一条循环

**本文归纳**：一切 Agent 系统的内核都可归为同一条循环（官方无此统一表述，官方口径见第 2 章）：

**记忆/上下文 → 思考(Thought) → 行动(Action，调用工具) → 观察(Observation) → 反思 → 回到思考**

一个 AI Agent 系统 = **模型（推理核心）+ 工具 + 记忆 + 规划 + 环境反馈循环**。所谓"架构"，就是对这条循环的三个维度做放大：

| 维度 | 回答的问题 | 代表架构 |
| --- | --- | --- |
| 推理深度 | 一步思考不够怎么办 | ReAct → ReWOO / LLMCompiler（规划分离）、Self-Refine / Reflexion（反思）、ToT / GoT / LATS（搜索） |
| 协作拓扑 | 一个模型不够怎么办 | 角色流水线、对话群组、层级 Manager-Worker、图工作流、常驻事件驱动 |
| 工程可靠性 | 循环跑崩了怎么办 | durable execution、HITL、guardrails、工单状态机、MCP/A2A/AG-UI/ACP 协议 |

> **标注**：本节「一条循环 + 三个放大维度」是本文档的归纳框架，并非任一官方定义；Anthropic 官方口径是 workflow/agent 二分与 augmented LLM（见 2.1 / 2.3）。

### 0.2 本文结构

第 1 章逐讲单智能体认知架构；第 2 章讲 Anthropic 官方工作流模式；第 3 章逐讲多智能体拓扑；第 4 章讲工程框架哲学；第 5 章讲协议；第 6–8 章为数据、能力矩阵与选型组合思维。每个架构一节，节内固定包含：官方出处 → 核心机制 → 工作原理 → 官方数据 → 取舍与对比。

---

## 1. 单智能体认知架构（逐一深度讲解）

### 1.1 ReAct（ICLR 2023 · 官方仓库 [ysymyth/ReAct](https://github.com/ysymyth/ReAct)）

**论文**：[ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)（Yao et al.）。

**解决什么问题**：纯 CoT 是"闭门思考"——模型只能推理，不能获取外部信息，也无法采取行动；纯行动式调用是"无脑操作"——能调工具但缺乏多步推理的连贯性。ReAct 把两者交织：**每一步先推理、再行动、用观察到的环境事实修正下一步推理**。

**工作原理**（逐步）：
1. 输入任务，模型输出第一段推理（Thought），并决定调用哪个工具（Action）；
2. 环境执行工具，返回结果（Observation），追加进上下文；
3. 模型带着完整轨迹继续推理，决定下一步；
4. 循环直到模型认为可以给出最终答案。

**机制关键点**：每一轮决策都基于"推理 + 行动 + 观察"的**完整历史轨迹**回放——推理始终被环境事实（ground truth）锚定，因此比纯 CoT 更抗幻觉、比纯行动更有规划性。

**官方数据**（仓库 README）：HotpotQA EM：GPT-3 30.4 / PaLM 29.4；FEVER EM：54.0 / 62.2；AlfWorld 成功率：78.4 / 70.9；WebShop：35.8 / 40.0。

**设计取舍**：两个原生代价——① 每轮全量回放历史导致 token 冗余；② 推理与工具调用串行交织导致延迟。后续所有单智能体架构（1.5–1.10）本质上都是在治理这两个代价。官方 README 指向其工程化后继：[LangChain zero-shot ReAct Agent](https://python.langchain.com/docs/modules/agents/agent_types/react.html)。

### 1.2 （本节已并入第 2 章）

> 本节原为 Anthropic 官方博客总纲，已并入第 2 章（2.1 workflow/agent 分界、2.3 augmented LLM），此处不再重复。该官方博客同时是第 2 章五种工作流模式的唯一来源。

### 1.3 Self-Refine（官方仓库 [madaan/self-refine](https://github.com/madaan/self-refine)）

**论文**：[Self-Refine: Iterative Refinement with Self-Feedback](https://arxiv.org/abs/2303.17651)。

**核心机制**：同一个模型依次扮演三个角色——生成者（产出初稿）→ 反馈者（给自己的产出写批评）→ 精炼者（按批评重写），循环迭代直到满足停止条件。**不需要外部反馈信号、不需要额外训练、不需要多模型**。

**工作原理**：每轮把"初稿 + 反馈"拼进提示词，让模型自我修正；反馈是即用即弃的，不跨任务沉淀。

**官方覆盖**：7 类任务——首字母缩写生成、对话回复、代码可读性改进、Commongen、GSM-8k、Yelp 情感迁移、PIE 程序修复；仓库含全部复现脚本与 GPT4-V 视觉版自精炼示例（如迭代生成 TikZ 图）。

**取舍与对比**：代价是每次迭代一次完整 LLM 调用，且自反馈质量依赖模型自身批评能力。与 Reflexion（1.4）的区别：Self-Refine 是**同一次尝试内**的反复打磨；Reflexion 是**跨尝试**的经验积累。

### 1.4 Reflexion（NeurIPS 2023 · 官方仓库 [noahshinn/reflexion](https://github.com/noahshinn/reflexion)）

**论文**：[Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366)。

**核心机制**：语言智能体的"口头强化学习"——任务执行失败后，模型生成**自我反思**（verbal self-reflection，一段文字而非标量奖励），存入**情景记忆**（episodic memory）；下一轮尝试时把记忆作为上下文加载，指导行为修正。num_trials 控制迭代轮数，use_memory 可关闭以做对照。

**RL 类比**（官方思路）：反思文本 ≈ 奖励信号，情景记忆 ≈ 经验回放缓存——整套"学习"过程完全用自然语言实现，无需梯度更新。

**官方实验矩阵**：3 种基础 Agent（ReAct / CoT_context / CoT_no_context）× 4 种反思策略（NONE / LAST_ATTEMPT / REFLEXION / LAST_ATTEMPT_AND_REFLEXION），逐层叠加可精确量化每部分增益；任务覆盖 HotpotQA 推理、AlfWorld 决策、LeetcodeHardGym 编程。

**取舍与对比**：反思质量依赖模型的自我诊断能力；记忆无限增长会稀释上下文。它是 ReAct 的自然增强——官方的基础 Agent 之一就是 ReAct。

### 1.5 Plan-and-Execute（LangGraph 官方文档模式）

**出处**：LangGraph 官方文档（docs.langchain.com；官方教程原址 langchain-ai.github.io/langgraph/tutorials/plan-and-execute）。

**核心机制**：三段式——**Planner** 先制定步骤计划 → **Executor** 逐步执行 → 执行中发现计划失效时由 **Replanner** 依据新观察修订计划、继续执行。LangGraph 官方以状态机实现该模式（PlanExecute 状态：计划、上一步结果、重规划次数）。

**工作原理**：相比 ReAct 的"每步都全量重读历史再决策"，该模式把"想"与"做"分相；相比 ReWOO（1.6）的"一次规划永不回头"，它允许**中间修订**——是"规划分离"与"观察反馈"的折中。

**适用**：步骤较多、可先规划再执行的任务；尤其是执行阶段相对确定、只需周期性检查计划是否仍有效的场景。

### 1.6 ReWOO（官方仓库 [billxbf/ReWOO](https://github.com/billxbf/ReWOO)）

**论文**：[ReWOO: Decoupling Reasoning from Observations](https://arxiv.org/abs/2305.18323)。

**核心机制**：**推理与观察彻底解耦**——Planner 一次性生成完整工具调用计划，每个步骤的结果用占位符（#E1、#E2…）引用；Worker 按顺序执行全部工具；Solver 在最后把占位符替换为真实结果、一次性作答。

**为什么省 token**：规划阶段不需要任何观察结果，模型不必像 ReAct 那样在每步之间反复重读历史；提示词只进入一次，工具结果只消费一次。

**官方数据**：HotpotQA 上 **5× token 效率 + 4% 精度提升**；工具故障下更鲁棒；官方展示把 175B GPT-3.5 的规划能力经指令微调蒸馏到 7B LLaMA（官方开源 planner_7B），证明"规划"与"执行"可彻底分家。官方后续实现并入 [Gentopia](https://github.com/Gentopia-AI/Gentopia)。

**取舍**：中间发生意外无法即时改计划——不适合需要边做边决策的开放式任务；适合步骤可预测、执行确定的任务。

### 1.7 LLMCompiler（官方仓库 [SqueezeAILab/LLMCompiler](https://github.com/SqueezeAILab/LLMCompiler)）

**论文**：[An LLM Compiler for Parallel Function Calling](https://arxiv.org/abs/2312.04511)。

**核心机制**：三组件流水线——
1. **Planner**：把问题拆成多个任务，生成**带依赖标注的 DAG**（每个任务显式声明"我的参数来自哪个任务的输出"）；
2. **Task Fetching Unit（TFU）**：调度器——任务依赖一旦就绪立即下发，互不依赖的任务自然并行；
3. **Executor**：并行执行工具调用。

--stream 模式下任务边生成边下发，不等 Planner 画完整个 DAG，进一步压延迟。

**官方数据**：HotpotQA、Movie Recommendation、ParallelQA 上一致的延迟降低、成本节省与精度提升；官方宣布已进入 LangGraph 与 LlamaIndex 生态。

**取舍与对比**：与 ReWOO 相比，它把"顺序计划"升级为"依赖图"，把可并行性显式化；但 DAG 标注本身要求模型更精确的结构化输出，出错面更大。适合多路检索、多数据源聚合类任务。

### 1.8 Tree of Thoughts（NeurIPS 2023 · 官方仓库 [princeton-nlp/tree-of-thought-llm](https://github.com/princeton-nlp/tree-of-thought-llm)）

**论文**：[Tree of Thoughts: Deliberate Problem Solving with LLMs](https://arxiv.org/abs/2305.10601)。

**核心机制**：把中间推理组织成树，每步四个动作——
1. **propose / sample**：生成 k 个候选思路；
2. **evaluate**：两种评估模式——value（对每个思路独立打分）或 vote（让思路互相投票）；
3. **select**：greedy 保留最好的 b 个状态；
4. 继续展开；Game of 24 用 **BFS**，填字游戏用 **DFS**。

**工作原理**：关键在"多分支探索 + 回溯"——一条思路走到死路就回到上级节点换支路，而不是像 CoT 那样一条链走到黑。官方仓库把生成器/评估器/选择器全部参数化（--method_generate / --method_evaluate / --n_generate_sample 等）。

**官方数据**：Game of 24 达 74%（官方注明复现为 69%，差异来自 GPT 解码随机性）；论文报告 CoT 仅约 4%。Creative Writing 与 Mini Crosswords 亦有显著提升。

**取舍**：评估环节是纯 token 消耗（每个候选状态都要多次 LLM 调用打分），成本随树宽近似平方级膨胀——"想得多"的直接账单。适合推理瓶颈型任务（谜题、规划），不适合工具密集型任务。

### 1.9 Graph of Thoughts（AAAI 2024 · 官方仓库 [spcl/graph-of-thoughts](https://github.com/spcl/graph-of-thoughts)，ETH SPCL）

**论文**：[Graph of Thoughts: Solving Elaborate Problems](https://arxiv.org/abs/2308.09687)。

**核心机制**：把问题建模为**操作图（Graph of Operations）**——节点是 LLM 操作（Generate、Score、**Aggregate 合并**、Improve、GroundTruth 校验等），边是思想之间的依赖；一个 Controller 解释执行该图，LLM 作为引擎，Prompter/Parser 负责进出格式转换。

**相对 ToT 的增量**：树只能分叉，图允许**多条思路合并（Aggregate）成一条**；官方实现把 CoT（链）与 ToT（树）都表达为 GoT 的特例——同一框架内可自由选择拓扑。

**官方数据**（论文）：32 数字排序任务上，成本比 ToT 降低 31% 以上且质量更高。

**取舍**：拓扑自由度带来的是设计负担——你必须自己设计操作图；相比 ToT 的固定流程，GoT 更适合有明确可合并结构的任务（排序、关键词计数等）。

### 1.10 LATS（论文 [arXiv:2310.04406](https://arxiv.org/abs/2310.04406)）

**论文**：Language Agent Tree Search Unifies Reasoning, Acting, and Planning in Language Models（Zhou et al.）。

**核心机制**：思维树 + **蒙特卡洛树搜索**（按 UCB 决定扩展哪一支）+ 环境反馈 + 自我反思的统一框架——像 AlphaGo 那样"搜索 + 评估 + 反哺"。

**说明**：论文未提供公开官方实现仓库，本整理以论文原文为准，不再展开未经验证的实现细节。

> **清理说明**：早期版本中的 PEV、Mental Loop、Dry-Run、Metacognitive、Graph World-Model、双记忆系统等条目源自第三方整理、无法在官方/学术来源核实，已全部移除。

---

## 2. Anthropic 官方工作流模式（官方博客深度讲解）

来源：[Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)（Anthropic 官方，2024-12-19；页面顶部官方注明工具生态已变化，现指向 Claude Managed Agents）。

### 2.1 最重要的分界：Workflow vs Agent

官方把所有"智能体系统"（agentic systems）分成两类：

- **Workflows**：LLM 与工具沿**代码预定义的路径**编排——图长什么样由开发者提前决定；
- **Agents**：LLM **动态决定自己的流程与工具使用**——图是模型在运行中自己画的。

这条分界是后文所有选型判断的地基：**能预定义路径就用 workflow（可预测、易测试、便宜）；只有"连你自己都不知道要改几个文件"的场景才需要自主 agent。**

### 2.2 官方原则（原文要点）

- 从最简单方案开始：很多应用优化单次 LLM 调用（检索 + 上下文示例）就够；
- 复杂确有必要时：well-defined 任务用 workflow（可预测性与一致性），大规模灵活决策用 agent；
- 框架只是起步工具：官方建议先用 LLM API 直写，用框架就必须理解其底层；
- 增加复杂度**必须**有可测收益（measurably improves outcomes）。

### 2.3 基座：augmented LLM

LLM + 检索 + 工具 + 记忆；模型主动生成检索查询、选择工具、决定保留什么。官方建议经 MCP 接入第三方工具生态。工程要点：增强能力要贴合用例，且为模型提供简单、文档良好的接口。

### 2.4 五种工作流模式逐一讲解

**① Prompt chaining（提示链）**
- 结构：线性 A→B→C，每步输出喂给下一步；中间可加程序化 gate 检查（如大纲是否符合标准）。
- 官方适用条件：任务可干净地拆成固定子步骤。
- 官方示例：营销文案生成→翻译；先写大纲（过检查）→按大纲写正文。
- 本质：把一个大任务拆成多个"更容易的小任务"，用延迟换准确率。

**② Routing（路由）**
- 结构：先分类输入，再分发到专用处理链。
- 官方适用条件：输入有清晰类别、分类可准确完成（LLM 或传统分类器）。
- 官方示例：客服问题分类（咨询/退款/技术支持）分到不同下游；易/难题路由到不同成本模型（官方举例 Haiku/Sonnet 分级）。
- 本质：关注点分离——避免"为一个输入优化的提示词伤害其他输入"。

**③ Parallelization（并行化）**
- 两种变体：sectioning（拆成互不依赖的子任务并行执行）与 voting（同一任务跑多次、聚合投票）。
- 官方适用条件：子任务可并行提速；或需要多视角/多次尝试提高置信度。
- 官方示例：sectioning——护栏模型与主模型并行（比单调用同时干两件事更好）、多维度自动评测；voting——代码漏洞多提示词并行评审、内容合规多阈值投票。
- 本质：官方观察——"多个考量点交给多个独立 LLM 调用分别专注处理，效果更好"。

**④ Orchestrator-workers（协调者-工作者）**
- 结构：中心 LLM 动态拆解任务 → 派发给 worker LLM → 综合结果。
- 与并行化的关键区别（官方原文）：**子任务不可预知**——例如改代码时"要改哪些文件、每个文件怎么改"取决于任务本身；并行化的子任务是预先定义的。
- 官方示例：多文件代码修改；多源信息搜集分析。
- 本质：这是"层级式多智能体"在单工作流层面的雏形。

**⑤ Evaluator-optimizer（评估器-优化器）**
- 结构：一个 LLM 生成、另一个评估并给反馈、循环迭代。
- 官方适用条件：有明确评估标准；且"人能写出有效反馈"与"LLM 也能给出此类反馈"两者成立——类似人类作家的打磨过程。
- 官方示例：文学翻译（译者 LLM 漏掉的韵味由评估 LLM 指出）；需要多轮搜索的复杂检索任务。
- 本质：Self-Refine（1.3）的工程化落地形态。

### 2.5 何时用 Agent + 三条核心原则

**Agent 适用**（官方原文）：开放性问题、所需步数难以预测、无法硬编码固定路径；执行中每步都要从环境获取 ground truth 评估进展；可设检查点暂停等人反馈；必须设停止条件（如最大迭代数）；成本更高、错误会复合，需沙箱测试与护栏。

**三条核心原则**：① 简单性；② 透明性——显式展示 Agent 的规划步骤；③ 精心设计 ACI（agent-computer interface）——工具格式要少格式开销、贴近模型在互联网上见过的自然形态、给模型足够 token 思考。

**官方附录实践**：客服（会话 + 查单/退款工具 + 可测的成功标准）与编码 Agent（SWE-bench 按 PR 描述改真实 issue；computer use 参考实现）——两者共同点：有清晰成功标准、有反馈环、有人工监督。

---

## 3. 多智能体协作拓扑（官方仓库逐一深度讲解）

### 3.1 MetaGPT：SOP 流水线（ICLR 2024 · 官方仓库 [FoundationAgents/MetaGPT](https://github.com/FoundationAgents/MetaGPT)）

**官方定位**：一行需求 → 用户故事 / 竞品分析 / 需求 / 数据结构 / API / 文档；内建产品经理、架构师、项目经理、工程师角色。

**核心哲学**：**Code = SOP(Team)**——把软件公司的标准作业流程物化，施加到由 LLM 组成的团队上。

**机制深度**：
- 协作不靠自由对话，而是**角色序列 + 结构化产出传递**：每个角色的输出是正式文档（PRD、设计文档、任务清单），不是聊天记录——下游角色拿到的是"规格"而非"口水话"，信息密度高、可复用；
- 为什么这很重要：自由多智能体对话的两个顽疾是信息稀释与产出不可复用，SOP 化一次性解决两者；
- 论文：MetaGPT: Meta Programming for a Multi-Agent Collaborative Framework（ICLR 2024）。

**官方生态**：MGX（自然语言编程产品）；AFlow（自动生成 Agentic 工作流，ICLR 2025 Oral）；Data Interpreter（数据分析 + 写码 + 画图）；Debate 等多智能体用例。

**取舍**：SOP 越严格，越适合"流程已知"的领域（软件研发、报告生产）；对开放探索类任务反而僵化。

### 3.2 ChatDev：从剧本式到零代码平台（官方仓库 [OpenBMB/ChatDev](https://github.com/OpenBMB/ChatDev)）

**ChatDev 1.0（legacy 分支）**：虚拟软件公司——CEO/CTO/程序员等角色按 **ChatChain**（相位化的流水线剧本）参加"功能研讨会"，走完设计→编码→测试→文档全流程。本质是把"双智能体对话"（导师-助手）推广成多角色、多相位的对话剧本。

**ChatDev 2.0 DevAll**（官方 2026-01 发布）：零代码多智能体编排平台——用户只配置 agent、工作流、任务即可编排数据可视化、3D 生成、深度研究等场景；经典 1.x 转入 chatdev1.0 分支维护。

**官方学术谱系**（仓库 News）：
- MacNet：DAG 拓扑的多智能体协作网络，官方称可支撑上千 agent、不受上下文限制；
- Puppeteer（NeurIPS 2025）：**可学习的中央编排器**——用 RL 优化"何时激活哪个 agent、按什么顺序"，把编排本身变成可训练对象；
- Experiential Co-Learning：导师-助手跨任务积累"捷径经验"，含经验的获取、利用、传播与淘汰。

**取舍**：ChatDev 谱系的价值在于把"协作拓扑"本身当成研究变量（链→DAG→可学习编排），适合需要定制协作结构的场景。

### 3.3 AutoGen → MAF / AG2：消息式群聊（官方仓库 [microsoft/autogen](https://github.com/microsoft/autogen)）

**官方现状**：微软官方 README 明确 AutoGen **已归档、不再维护**；企业级继任者是 [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)（MAF 1.0：生产可用、企业级多智能体编排、多厂商模型、经 A2A/MCP 跨运行时互操作，官方提供迁移指南）；社区继任者 [AG2](https://github.com/ag2ai/ag2)（官方自述 The Open-Source AgentOS，Apache-2.0）。

**AutoGen 官方分层设计**（历史上最重要的"对话式多智能体"框架）：
- **Core API**：事件驱动的**消息传递** + 本地/分布式运行时；智能体即消息处理器，跨 Python/.NET；
- **AgentChat API**：在 Core 上封装常见模式——双智能体对话、**GroupChat 群聊**（群管理器决定下一个发言者）；
- **Extensions**：LLM 客户端（OpenAI/Azure 等）、代码执行等扩展；
- 开发者工具：AutoGen Studio（无代码原型，官方声明非生产用途）、AutoGen Bench（评测）；旗舰示例 Magentic-One（网页浏览 + 代码执行 + 文件处理的多智能体团队）。

**机制评价**：消息式设计优雅——任何协作都归结为"谁给谁发什么消息"；但群聊的**收敛性没有保证**（谁来叫停、何时停止没有确定答案），这正是微软官方转向 MAF（确定性编排 + 协议互操作）的动因，也是 3.4/3.5/3.8 各条"确定性"路线的反面教材。

### 3.4 CrewAI：Crews + Flows 双原语（官方仓库 [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI)）

**官方定位**：高抽象 + 低层 API 并存的多智能体自动化框架。两大原语：
- **Crews**：角色（role/goal/backstory）驱动的自主协作团队——代理之间自然决策、动态委托；
- **Flows**：事件驱动、状态精确可控的确定性工作流——显式控制执行路径、任务间状态一致、可混入普通 Python 代码与条件分支。

**官方机制**：
- JSON-first 项目：agents/*.jsonc 定义每个 agent 的角色/目标/LLM/工具，crew.jsonc 定义任务、进程与输入；占位符 + inputs 提供参数化；
- 进程两种：**sequential**（任务链）与 **hierarchical**（自动产生 manager，负责规划、任务委托与结果校验）——层级式被官方做成开箱即用；
- 能力矩阵（官方 Key Features）：工具、memory、knowledge、checkpointing、异步执行、MCP/A2A、human input、结构化输出；
- 商业 AMP Suite：托管部署、可观测、治理、安全与支持。

**机制评价**：Crews 是"自主"，Flows 是"控制"，官方明说**两者嵌套使用才是完整形态**——这恰好是 Anthropic"workflow 与 agent 互补"原则在框架层的体现。

### 3.5 LangGraph：状态图编排（官方仓库 [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph)）

**官方定位**：为构建、管理、部署**长期运行的有状态 Agent** 而生的低层编排框架；受 Pregel 与 Apache Beam 启发，接口风格借鉴 NetworkX；可不依赖 LangChain 单独使用。

**机制深度**：
- **状态图模型**：节点（计算）+ 边（控制流）+ 全局共享状态；支持循环、条件分支、并行扇出；任意多智能体拓扑（含 supervisor）都能画成图；
- **Durable execution**：持久化执行——失败/重启后**精确从断点恢复**，长期运行的任务不必从头重跑（官方专页）；
- **Human-in-the-loop**：interrupts 机制允许在任意节点暂停、人工检查并**修改状态**后再放行；
- **Memory**：短期工作记忆（进行中推理）+ 跨会话长期记忆，官方把记忆做成一等公民；
- 可观测：LangSmith 全程追踪执行路径、状态迁移与运行时指标；
- 上层包 Deep Agents：规划、子代理、文件系统（官方 README 指向）。

**机制评价**：LangGraph 的价值在"把 ReAct 族与多智能体拓扑**编译成可预测、可恢复的状态机**"——它不规定你用哪种认知架构，而是给所有架构一个可靠的执行底座。

### 3.6 OpenAI Agents SDK：委托原语（官方仓库 [openai/openai-agents-python](https://github.com/openai/openai-agents-python)）

**官方定位**：轻量但强大的多智能体工作流框架；provider-agnostic（OpenAI Responses/Chat Completions + 100+ LLM）。

**核心概念逐一**（官方文档）：
- **Agents**：LLM + instructions + tools + guardrails + handoffs 的封装；
- **Handoffs / Agents-as-tools**：把另一个 Agent 当工具委托——多智能体协作降级为"一次工具调用"，简单但可控（官方对比页将 handoffs 与图式方法并列展示，两者各有适用面）；
- **Guardrails**：输入/输出两侧的可配置安全校验；
- **Human in the loop**：内建的人工介入机制；
- **Sessions**：跨运行自动管理会话历史（SQLite 内建，Redis 可选）；
- **Tracing**：内建运行追踪；
- **Sandbox agents**：容器内执行长时任务（文件检查、命令执行、打补丁、保状态）；Realtime/Voice agents：语音流水线。

**机制评价**：哲学是"多智能体 = 智能体 + 交接"的极简模型，把从零到可用压缩到最短路径；复杂控制流交给图式框架（如 LangGraph）补位。

### 3.7 Google ADK 2.0：图运行时 + 任务委托（官方仓库 [google/adk-python](https://github.com/google/adk-python)）

**官方定位**：code-first、把软件工程原则用于 Agent 构建的模块化框架；模型无关、部署无关、可与其他框架互操作；多语言版：Java / Kotlin / Go / TypeScript。

**核心机制逐一**（官方 README）：
- **Agent**：定义指令、工具与行为的最小单元；
- **Workflow**：图执行引擎——routing、fan-out/fan-in、loops、retry、状态管理、动态节点、HITL、**嵌套工作流**都是内建原语；
- **Task API**：结构化的 agent 间委托——多轮任务模式、单轮受控输出、混合委托模式、任务 Agent 可作为工作流节点；
- **Tool Confirmation**：HITL 确认流，可守卫工具执行并要求自定义输入；
- **Agent Config**：无代码定义 Agent；
- 工程配套：adk eval（评估）、adk web（开发 UI）、部署到 Cloud Run / Vertex AI Agent Engine；工具生态：预置工具、自定义函数、OpenAPI 规格、MCP。

**机制评价**：ADK 把"确定性图编排"与"自主 Agent"做成同一框架的两类一等公民（Workflow 与 Agent 可互嵌），与 Anthropic 的 workflow/agent 分界完全对齐。

### 3.8 xAI Grok Bot：常驻式个人 Bot 团队（官方文档 [docs.x.ai/grok-bot](https://docs.x.ai/grok-bot/overview)）

**官方定位**：Grok Bot 是"主动式 AI 队友"（proactive AI teammate）——每个 Bot 拥有云电脑，可在你的应用与网站上干活，笔记本合上后仍继续工作；多个 Bot 可以像真实团队一样协作，你的 primary Bot 负责协调。

**Bot 模型**（官方 bots 页）：
- 每个 Bot = 名字 + 一份职责 + 自己的对话 + 持续积累的工作上下文；一个 Bot 一个职责能积累更有用的记忆；
- **primary Bot** 是你的主要联系人，会主动向你汇报并协调其他 Bot；
- **记忆**：每个 Bot 独立记忆（偏好、长期规则、带日期的工作日志）；仅少数事实（姓名、时区）跨 Bot 共享；Bot 自主决定记什么，用户可要求它记住/修正/忘掉；
- 同一类请求反复出现且有自己的来源、规则或日程时，给它单独开一个 Bot。

**云电脑**（官方 computer-and-apps 页）：
- 所有 Bot 共享**同一台持久云电脑**：浏览器（含登录态）、命令行、文件系统，跨任务保留；笔记本合上工作不中断；
- 每个 Bot 有独立"屏幕"，可并行执行，但**屏幕只是工作台、不是安全边界**——文件、登录态、命令行凭据在 Bot 之间共享；
- 用户之间严格隔离（每人一台、硬件隔离）；
- 敏感步骤可"接管电脑"由人完成（SSO、passkey、CAPTCHA、银行卡验证等）。

**审批与安全**（官方 approvals / vault 页）：
- **Auto Review** 默认开启：执行命令、使用已连接应用、使用电脑前逐动作检查；多数放行，需要人工时弹审批卡并等待；
- **Custom Rules**：Ask first（命中必停）/ Allow automatically；审批卡三分支 Allow once / Always allow / Deny；
- **只有用户本人消息算指令**——网页、邮件里的文字一律不算（官方明确的提示注入防线）；
- **Vault**：登录与银行卡在页面内直接填入，Bot 从不接触明文；也可接 1Password、Secure Form、secure secret card；
- Bot 以你的身份行动、无自有凭据（团队管理的连接器除外），每条动作都可追溯到你。

**技能与例程**（官方 skills-routines 页）：
- **skill** = 可复用的任务指令（何时用、输入与权限、步骤、校验、输出、审批边界）；
- **routine** = 告诉某个 Bot 何时运行工作流：定时，或事件触发（Slack 消息、GitHub/Linear/Sentry/PagerDuty 事件、邮件、webhook）；
- 可"演示教学"：记录浏览器操作（最长 10 分钟）生成技能草稿，先在小例子上验证再接例程。

**扩展方式**：Apps 目录（Gmail、Google Calendar、Drive、Slack、Notion、Teams 等）、任意 **MCP 服务器**、自定义 API（官方 marketplace 的 tinkabot 可把 API 封装成 MCP+技能）；编码任务可移交 **Cursor Cloud Agents** 并把结果附回回复。

**边界**：Grok Bot 是产品级个人 Bot 团队，不等同于通用多智能体拓扑；本节关注其角色、上下文、工具与审批模型。

---

## 4. 单智能体工程框架（官方仓库深度讲解）

### 4.1 Smolagents：用代码思考（官方仓库 [huggingface/smolagents](https://github.com/huggingface/smolagents)）

**官方定位**：barebones、"用代码思考"的 Agent 库；核心逻辑约 1000 行（agents.py）。

**核心机制（CodeAgent）**：ReAct 循环的变体——区别是**行动以 Python 代码片段表达**：模型写一段代码，其中包含一个或多个工具调用（还能用循环、条件一次表达多次调用），执行环境运行它、把日志回填记忆，直到模型调用 final_answer 结束。官方绘制的流程：任务进 memory → 模型生成 → 解析出代码动作 → 执行 → 执行日志回 memory 循环。

**为什么代码表达更优（官方引用研究）**：比 JSON 工具调用少 30% 步骤（即少 30% LLM 调用），困难基准上分数更高——因为一次代码块可组合多步操作，而 JSON 一次只能声明一步。

**其他官方能力**：经典 ToolCallingAgent（JSON 式，二选一）；模型无关（transformers/Ollama/Hub 推理供应商/LiteLLM/OpenAI/Anthropic/Bedrock 等）；工具无关（MCP、LangChain、Hub Space 都能当工具）；模态无关（文本/视觉/视频/音频）；多智能体层级；Hub 分享（push_to_hub/from_hub）；CLI（smolagent / webagent）。

**官方安全声明**：代码执行 = 任意代码执行，官方要求使用 E2B / Blaxel / Modal / Docker 沙箱；官方明确 LocalPythonExecutor 只是尽力缓解、**不是安全边界**，不可运行不可信代码。

**取舍**：极简换来的是"自己管生产化"——部署、观测、护栏都要自己拼；适合研究、原型与嵌入式场景。

### 4.2 Pydantic AI：类型化的 Agent 循环（官方仓库 [pydantic/pydantic-ai](https://github.com/pydantic/pydantic-ai)）

**官方定位**：Python AI SDK——类型安全、可扩展的 Agent 循环；"Every model, every interface, typed end to end"；同一 Agent 定义可跑在 CLI / Web / 实时语音 / 后台队列 / GitHub Actions / ACP / AG-UI 等任何界面。

**核心机制逐一**：
- **类型契约**：output_type 声明返回类型（Pydantic 模型），每次运行返回验证过的对象；工具入参由签名自动生成 schema 并先验证——把整类运行时错误提前到写时；
- **capability 原语**：把工具 + 指令 + hooks + 模型设置打包成可复用单元；核心自带 MCP、WebSearch；支持按需延迟加载；
- **durable execution**：官方支持八引擎——Temporal、DBOS、Prefect、Restate、AWS Lambda、Airflow、Absurd、pgtask（前五与厂商联合维护），每个模型/工具调用成为持久活动，重启与长等待后仍可恢复；另有 StepPersistence（无需引擎的检查点式快照）；
- **Pydantic Graph**：类型化的图控制流，当"一个 Agent 循环不够用"时补位；
- **可观测**：OpenTelemetry 原生插桩，Logfire 一键点亮；Pydantic Evals 评估最终输出与工具调用轨迹（含线上流量抽样）。

**取舍**：类型系统的收益在工程团队最大化；官方提供与 LangChain/ADK/MAF/Claude Agent SDK 的对比页与迁移技能。

### 4.3 LlamaIndex：数据框架（官方仓库 [run-llama/llama_index](https://github.com/run-llama/llama_index)）

**官方定位**：data framework——数据连接器摄取（API/PDF/SQL…）、索引与图结构化、检索查询接口（输入提示、返回检索上下文与知识增强输出）；core + 300+ 集成包。

**官方生态**：LlamaParse 文档智能平台——Parse（agentic OCR，130+ 格式）、Extract（结构化抽取）、Index（摄取与 RAG）、Split（大文档拆分）、Agents（Workflows + Agent Builder 的端到端文档 Agent）。

**取舍**：官方自认 Agent 循环不是其主线——它的价值在检索基础设施，Agent 是建在其上的编排层；适合"Agent 的主体工作是查询文档与数据源"的场景。

---

## 5. 协议层（官方规范深度讲解）

### 5.1 MCP：模型上下文协议（官方规范 2025-06-18 · [modelcontextprotocol](https://modelcontextprotocol.io/specification/2025-06-18)）

**官方定义**：连接 LLM 应用与外部数据/工具的开放协议；灵感来自 Language Server Protocol——LSP 标准化了"开发工具如何接语言支持"，MCP 标准化了"AI 应用如何接上下文与工具"。

**数据流三方**：Hosts（发起连接的 LLM 应用）→ 内嵌 Clients（连接器）→ 连接多个 Servers（提供上下文与能力的服务）。基座是 JSON-RPC 2.0、有状态连接、能力协商。

**服务器三类特性**：Resources（上下文数据，供用户或模型使用）、Prompts（模板化消息与工作流）、Tools（模型可执行的函数）。
**客户端三类特性**：Sampling（服务器发起的递归 LLM 交互——让工具端也能"问模型"）、Roots（服务器询问允许操作的文件系统边界）、Elicitation（服务器向用户索取额外信息）。
**实用机制**：配置、进度跟踪、取消、错误上报、日志。

**官方安全四原则**（规范原文）：① 用户同意与控制（明确同意并理解所有数据访问与操作）；② 数据隐私（暴露用户数据给服务器前必须取得同意）；③ 工具安全（工具描述应视为不可信，调用前必须取得用户同意）；④ 采样控制（用户批准是否采样、看得到实际提示、控制服务器可见范围）。规范同时明言：**协议本身无法强制这些安全原则，实现者 SHOULD 落实**。

### 5.2 A2A：智能体互操作协议（官方仓库 [a2aproject/A2A](https://github.com/a2aproject/A2A)，Linux Foundation）

**官方定义**：让"不透明"的智能体应用互相通信与协作的开放协议——解决不同公司、不同框架、不同服务器上的 Agent 如何以"Agent 的身份"协作。

**四项官方能力**：发现彼此能力（Agent Card 声明能力与连接信息）、协商交互模态（文本/表单/媒体）、安全协作用于长时任务、**不暴露内部状态/记忆/工具**（保留不透明性 = 保护安全与知识产权）。

**技术形态**：JSON-RPC 2.0 over HTTP(S)；同步请求/响应 + SSE 流式 + 异步推送通知；文本/文件/结构化 JSON；企业级安全、认证与可观测设计；官方 SDK 六语言：Python / Go / JS / Java / .NET / Rust。

**官方路线图**：AgentCard 内嵌授权方案与凭据、QuerySkill() 动态技能查询、任务内动态 UX 协商（如对话中途加音视频）、客户端主动方法、流式可靠性改进。

**与 MCP 的关系**（官方 DeepLearning.AI 课程原话）：A2A 让 Agent 与 Agent 协作，MCP 让 Agent 接工具，二者互补——一个管"横向的智能体网络"，一个管"纵向的能力接入"。

### 5.3 AG-UI：前端交互协议（官方文档 [docs.ag-ui.com](https://docs.ag-ui.com/)）

**官方定义**：Agent User Interaction Protocol——标准化 Agent 与面向用户的前端应用之间的通信（官方架构页：AG-UI connects front-end applications to AI agents）。

**机制**：事件驱动的协议——以 events 为原语（官方 concepts/events），流式传递消息、工具调用状态与界面快照；官方提供三条快速上手路径：Server（实现 AG-UI 兼容服务端）、Middleware（把既有协议、进程内 Agent 或自定义方案桥接入 AG-UI）、Clients（前端消费端）。

**官方定位**：官方专页「MCP, A2A, and AG-UI」说明三者互补——AG-UI 管「用户与 Agent 的交互层」，MCP 管工具/上下文接入，A2A 管 Agent 间协作。

**版本与支持**：官方含 Migrating to 1.0 迁移指南（AG-UI 1.0），并明示提供可选商业生产支持。

**取舍**：只约束前端交互事件流，不规定 Agent 内部实现与工具协议；复用既有协议时走官方 Middleware。

### 5.4 ACP：编辑器客户端协议（官方文档 [agentclientprotocol.com](https://agentclientprotocol.com/)）

**官方定义**：Agent Client Protocol——标准化代码编辑器与 Agent 之间的通信（官方原文：a protocol that standardizes communication between code editors）。

**机制**：官方 v1 协议按分节规范组织：初始化（Initialization）、认证（Authentication）、会话建立（Session Setup）、会话列表（Session List）、会话删除（Session Delete）、提示词（Prompt）等；官方提供 Architecture 总览、ACP Registry（查找并安装 ACP 兼容 Agent 的入口），以及 Agents / Clients 两侧实现清单。

**官方定位**：面向「编辑器类客户端 ↔ 本地或远程 Agent」的接入标准化，客户端与 Agent 解耦、可插拔。

**取舍**：聚焦编辑器会话交互（会话管理、提示词、认证），不规定 Agent 内部认知架构；与 MCP/A2A/AG-UI 互补。

---

## 6. 官方项目数据一览（GitHub 官方 API，2026-11-03 实测）

| 项目 | 官方仓库 | Stars | 最近推送 | License | 官方一句话定位 |
| --- | --- | --- | --- | --- | --- |
| LangGraph | langchain-ai/langgraph | 44.4K | 2026-11-03 | MIT | Build resilient agents（低层有状态编排） |
| AutoGen（已归档） | microsoft/autogen | 61.7K | 2026-10-28 | MIT(代码) | 多智能体框架；官方建议迁移 MAF |
| AG2 | ag2ai/ag2 | 5.0K | 2026-11-03 | Apache-2.0 | The Open-Source AgentOS |
| CrewAI | crewAIInc/crewAI | 60.4K | 2026-11-03 | MIT | 角色扮演自主智能体编排 |
| LlamaIndex | run-llama/llama_index | 52.8K | 2026-10-26 | MIT | 面向 AI 的文档处理平台 |
| OpenAI Agents SDK | openai/openai-agents-python | 30.5K | 2026-11-03 | MIT | 轻量多智能体工作流框架 |
| Google ADK | google/adk-python | 22.1K | 2026-11-03 | Apache-2.0 | code-first Agent 工具包 |
| Smolagents | huggingface/smolagents | 30.2K | 2026-10-29 | Apache-2.0 | 用代码思考的 barebones 库 |
| Pydantic AI | pydantic/pydantic-ai | 21.0K | 2026-11-03 | MIT | How Python does AI |
| A2A | a2aproject/A2A | 26.4K | 2026-11-02 | Apache-2.0 | 智能体互操作开放协议 |
| MCP | modelcontextprotocol/modelcontextprotocol | 9.6K | 2026-11-03 | MIT | MCP 规范与文档 |

---

## 7. 生产化能力清单（各官方文档明确提供）

| 能力 | 官方提供方 |
| --- | --- |
| 持久化执行/断点恢复 | LangGraph durable execution；Pydantic AI 八引擎 durable；CrewAI checkpointing；OpenAI Agents SDK sessions |
| 人机协同 | LangGraph interrupts；ADK Tool Confirmation；Agents SDK HITL；CrewAI human input |
| 安全护栏 | Agents SDK guardrails；MCP 规范安全原则；Smolagents 沙箱强制 |
| 可观测与评估 | LangSmith；Agents SDK 内置 tracing；Pydantic Logfire（OTel）/ Evals；ADK eval；AutoGen Bench |
| 协议互操作 | MCP（各框架普遍支持）；A2A（CrewAI、MAF、Strands 等官方支持）；AG-UI（前端交互事件流，官方 Middleware + 1.0 迁移指南）；ACP（编辑器客户端协议，官方 Registry + v1 分节规范） |

---

## 8. 选型与组合思维（基于官方定位归纳）

**单智能体认知层**：任务路径确定、步骤可预测 → ReWOO / LLMCompiler（省 token、可并行）；需要边做边修正 → ReAct 或 Plan-and-Execute；错误会重复出现、可跨尝试学习 → 加 Reflexion；推理是瓶颈、值得花 token 探索 → ToT / GoT；同轮打磨输出 → Self-Refine。

**编排层**：
- 路径可预定义 → Workflow（Anthropic 五模式：链/路由/并行/协调者-工作者/评估器-优化器）；
- 需要长时运行、断点恢复、人工检查点 → LangGraph（durable + interrupts + 双记忆）；
- 角色团队直觉匹配、要快速原型 → CrewAI（Crews + Flows）；
- 极简上手 + 多智能体委托 → OpenAI Agents SDK；图工作流 + Google 生态 → ADK；
- 软件研发 SOP → MetaGPT / ChatDev；对话式多智能体研究 → AutoGen 已归档，改用 MAF / AG2；
- 个人/团队日常（云电脑操作、审批、技能例程）→ Grok Bot 模式。

**工具与输出层**：类型契约优先 → Pydantic AI；代码即行动 → Smolagents（务必沙箱）；检索/文档智能 → LlamaIndex。外部工具统一走 MCP，Agent 间协作走 A2A。

**2026 生产系统参考拼装**：

A2A 对接外部 Agent 网络 → [LangGraph 状态图：durable + interrupts + 双记忆] → Supervisor 节点（层级派单，采用显式授权与工单化边界）→ Worker 节点（ReAct + Reflexion 记忆；规划用 LLMCompiler 并行 DAG）→ MCP 工具层 → LangSmith/Logfire 可观测 + guardrails + 预算上限 + 沙箱。

**官方总原则（Anthropic）**：从最简单方案开始，workflow 优先于 agent，只在"流程无法预先确定"时引入自主决策，且每增加复杂度必须有可测收益。

---

## 9. 参考资料（全部官方来源）

- ReAct：[ysymyth/ReAct](https://github.com/ysymyth/ReAct) · [arXiv:2210.03629](https://arxiv.org/abs/2210.03629)
- Self-Refine：[madaan/self-refine](https://github.com/madaan/self-refine) · [arXiv:2303.17651](https://arxiv.org/abs/2303.17651)
- Reflexion：[noahshinn/reflexion](https://github.com/noahshinn/reflexion) · [arXiv:2303.11366](https://arxiv.org/abs/2303.11366)
- Plan-and-Execute：LangGraph 官方文档 [docs.langchain.com](https://docs.langchain.com/oss/python/langgraph/overview)
- ReWOO：[billxbf/ReWOO](https://github.com/billxbf/ReWOO) · [arXiv:2305.18323](https://arxiv.org/abs/2305.18323)
- LLMCompiler：[SqueezeAILab/LLMCompiler](https://github.com/SqueezeAILab/LLMCompiler) · [arXiv:2312.04511](https://arxiv.org/abs/2312.04511)
- ToT：[princeton-nlp/tree-of-thought-llm](https://github.com/princeton-nlp/tree-of-thought-llm) · [arXiv:2305.10601](https://arxiv.org/abs/2305.10601)
- GoT：[spcl/graph-of-thoughts](https://github.com/spcl/graph-of-thoughts) · [arXiv:2308.09687](https://arxiv.org/abs/2308.09687)
- LATS：[arXiv:2310.04406](https://arxiv.org/abs/2310.04406)
- Anthropic：[Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
- MetaGPT：[FoundationAgents/MetaGPT](https://github.com/FoundationAgents/MetaGPT)
- ChatDev：[OpenBMB/ChatDev](https://github.com/OpenBMB/ChatDev)
- AutoGen/MAF：[microsoft/autogen](https://github.com/microsoft/autogen) · [microsoft/agent-framework](https://github.com/microsoft/agent-framework) · [ag2ai/ag2](https://github.com/ag2ai/ag2)
- CrewAI：[crewAIInc/crewAI](https://github.com/crewAIInc/crewAI)
- LangGraph：[langchain-ai/langgraph](https://github.com/langchain-ai/langgraph)
- OpenAI Agents SDK：[openai/openai-agents-python](https://github.com/openai/openai-agents-python)
- Google ADK：[google/adk-python](https://github.com/google/adk-python)
- Smolagents：[huggingface/smolagents](https://github.com/huggingface/smolagents)
- Pydantic AI：[pydantic/pydantic-ai](https://github.com/pydantic/pydantic-ai)
- LlamaIndex：[run-llama/llama_index](https://github.com/run-llama/llama_index)
- Grok Bot：[官方文档 docs.x.ai/grok-bot](https://docs.x.ai/grok-bot/overview) · [官方公告](https://x.ai/news/introducing-grok-bot)
- MCP：[官方规范 2025-06-18](https://modelcontextprotocol.io/specification/2025-06-18)
- A2A：[a2aproject/A2A](https://github.com/a2aproject/A2A) · [a2a-protocol.org](https://a2a-protocol.org)
- AG-UI：[官方文档 docs.ag-ui.com](https://docs.ag-ui.com) · [官方仓库 ag-ui-protocol/ag-ui](https://github.com/ag-ui-protocol/ag-ui)
- ACP：[官方文档 agentclientprotocol.com](https://agentclientprotocol.com) · [官方仓库 agentclientprotocol/agent-client-protocol](https://github.com/agentclientprotocol/agent-client-protocol)

---

### 附录：官方文档库（本地完整归档）

自 2026-11-07 起，每个主流架构的官方文档已按独立文件夹完整归档于 **official-docs/**（git 稀疏克隆：README + docs 树；小型学术仓库为全量），当前共 27 个文件夹：

| 文件夹 | 归档内容 |
| --- | --- |
| ReAct / Self-Refine / Reflexion / ReWOO / LLMCompiler / Tree-of-Thoughts / Graph-of-Thoughts | 官方仓库全量（论文代码与实验） |
| LATS | 说明文件：论文 arXiv:2310.04406（官方未公开实现仓库） |
| Plan-and-Execute | 说明文件：LangGraph 官方文档模式（文档见 LangGraph 文件夹） |
| Anthropic-Building-Effective-Agents | 官方博客全文 Markdown + 说明 |
| MetaGPT / ChatDev / AutoGen / Microsoft-Agent-Framework / AG2 | README + docs 树（AutoGen 含官方归档声明） |
| CrewAI | README + docs 树（官方完整文档站） |
| LangGraph | 官方仓库 + docs-site（langchain-ai/docs 的 LangGraph 官方文档与示例） |
| OpenAI-Agents-SDK / Google-ADK / Smolagents / Pydantic-AI / LlamaIndex | README + docs 树 |
| Grok-Bot | 28 页官方文档（docs.x.ai/grok-bot 全套 + 订阅页，Markdown 原文） |
| MCP / A2A | README + docs 树（官方协议规范） |
| AG-UI / ACP | README + docs 树（官方协议规范） |

归档完成后，已用新下载的官方文档对本文全部关键论断逐一核验（LangGraph durable execution / interrupts、ADK fan-out/fan-in、AutoGen 归档声明、Pydantic AI Temporal durable、MCP 规范等，均与正文一致）。

### 附录：本地取证资料存档说明

官方原始文档摘录存档于 `research/official-readmes/`；大体积完整归档位于 `official-docs/`。此前媒体/第三方资料文件已全部删除。

> **配套文档**：每个架构的【适合任务类型 / 不适合场景 / 官方搭建细节 / 关键节点】四维分析，见 [task-fit-and-build.md](../how-to/task-fit-and-build.md)。


