$ErrorActionPreference = 'Continue'
$root = 'D:\AI\agent架构\官方文档库'
New-Item -ItemType Directory -Force -Path $root | Out-Null
Write-Output ('git version: ' + (git --version))

$repos = @(
  @{name='ReAct';url='https://github.com/ysymyth/ReAct.git'},
  @{name='Self-Refine';url='https://github.com/madaan/self-refine.git'},
  @{name='Reflexion';url='https://github.com/noahshinn/reflexion.git'},
  @{name='ReWOO';url='https://github.com/billxbf/ReWOO.git'},
  @{name='LLMCompiler';url='https://github.com/SqueezeAILab/LLMCompiler.git'},
  @{name='Tree-of-Thoughts';url='https://github.com/princeton-nlp/tree-of-thought-llm.git'},
  @{name='Graph-of-Thoughts';url='https://github.com/spcl/graph-of-thoughts.git'},
  @{name='MetaGPT';url='https://github.com/FoundationAgents/MetaGPT.git'},
  @{name='ChatDev';url='https://github.com/OpenBMB/ChatDev.git'},
  @{name='AutoGen';url='https://github.com/microsoft/autogen.git'},
  @{name='Microsoft-Agent-Framework';url='https://github.com/microsoft/agent-framework.git'},
  @{name='AG2';url='https://github.com/ag2ai/ag2.git'},
  @{name='CrewAI';url='https://github.com/crewAIInc/crewAI.git'},
  @{name='LangGraph';url='https://github.com/langchain-ai/langgraph.git'},
  @{name='OpenAI-Agents-SDK';url='https://github.com/openai/openai-agents-python.git'},
  @{name='Google-ADK';url='https://github.com/google/adk-python.git'},
  @{name='Smolagents';url='https://github.com/huggingface/smolagents.git'},
  @{name='Pydantic-AI';url='https://github.com/pydantic/pydantic-ai.git'},
  @{name='LlamaIndex';url='https://github.com/run-llama/llama_index.git'},
  @{name='dsh-superagent';url='https://github.com/deepseek-ai/dsh-superagent-prototype.git'},
  @{name='MCP';url='https://github.com/modelcontextprotocol/modelcontextprotocol.git'},
  @{name='A2A';url='https://github.com/a2aproject/A2A.git'}
)

foreach($r in $repos){
  $dest = Join-Path $root $r.name
  Write-Output ('=== CLONE ' + $r.name + ' ===')
  if(Test-Path (Join-Path $dest '.git')){
    Write-Output 'exists, skip'
    continue
  }
  if(Test-Path $dest){ Remove-Item -Recurse -Force $dest }
  git clone --depth 1 --filter=blob:none --sparse $r.url $dest 2>&1 | Out-String | Write-Output
  if(Test-Path (Join-Path $dest '.git')){
    $patterns = @('docs/','/*.md')
    if($r.name -eq 'dsh-superagent'){ $patterns = @('docs/','prompts/','skills/','/*.md') }
    git -C $dest sparse-checkout set --no-cone @($patterns) 2>&1 | Out-String | Write-Output
    $count = (Get-ChildItem -Recurse -File $dest -ErrorAction SilentlyContinue | Measure-Object).Count
    Write-Output ('files checked out: ' + $count)
  } else {
    Write-Output ('CLONE FAILED: ' + $r.name)
  }
}
Write-Output '=== ALL DONE ==='
