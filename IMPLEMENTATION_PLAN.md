# Universal ADK Agent Starter Kit - Implementation Plan

## 🚨 CRITICAL REQUIREMENT
**Every file must be extracted from source repositories - NO invented code**

## Discovered Repositories (Verified via Search)

### 1. Core ADK Repositories
- **google/adk-samples** - Sample agents with ADK 1.0 patterns
- **google/adk-python** - ADK SDK with evaluation framework  
- **GoogleCloudPlatform/agent-starter-pack** - Production scaffolding & CLI

### 2. Supporting Infrastructure
- **google/a2a-python** - Agent-to-Agent protocol SDK
- **GoogleCloudPlatform/generative-ai** - RAG implementations, tracing
- **GoogleCloudPlatform/vertex-ai-samples** - Agent Engine deployment

## Phase 1: Repository Extraction Plan

### Step 1.1: Agent Templates
**Source**: google/adk-samples
```bash
# Extract from /python/agents/
- data-science/ → Complex multi-agent template
- brand-search-optimization/ → Tool-using agent template
- Look for simpler agents for basic template
```

### Step 1.2: Scaffolding Infrastructure  
**Source**: GoogleCloudPlatform/agent-starter-pack
```bash
# Extract:
- CLI tool (agent-starter-pack create command)
- Terraform modules from deployment/
- CI/CD templates from deployment/ci/
- Makefile patterns
```

### Step 1.3: Evaluation Framework
**Source**: google/adk-python
```bash
# Extract from /tests/:
- matchers.py
- fixtures.py  
- test_llm_auditor.py
- .evalset.json examples
```

### Step 1.4: A2A Protocol
**Source**: google/a2a-python
```bash
# Extract:
- examples/helloworld/server.py → Bridge template
- examples/langgraph/ → Advanced A2A patterns
- Core A2A client/server implementations
```

### Step 1.5: RAG Implementation
**Source**: GoogleCloudPlatform/generative-ai
```bash
# Extract from notebooks:
- gemini/rag-engine/rag_engine_vector_search.ipynb
- Convert to vertex_ingest.py module
- Extract search patterns
```

### Step 1.6: Deployment Patterns
**Source**: GoogleCloudPlatform/vertex-ai-samples
```bash
# Extract:
- Agent Engine deployment scripts
- Cloud Run patterns
- Monitoring setup
```

## Phase 2: Template Structure

Based on discovered patterns, create three agent templates:

### 1. Simple Agent Template
```
simple_agent/
├── agent.py          # From adk-samples basic agent
├── tools.py          # Tool patterns
├── config.yaml       # Configuration
└── test_agent.py     # Test patterns
```

### 2. A2A Agent Template  
```
a2a_agent/
├── agent.py          # Agent with A2A capability
├── bridge.py         # From a2a-python examples
├── tools.py          
└── test_agent.py
```

### 3. RAG Agent Template
```
rag_agent/
├── agent.py          # Agent with RAG tools
├── tools.py          # Including search_internal_docs
├── ingest.py         # From generative-ai notebooks
└── test_agent.py
```

## Phase 3: Core Infrastructure

### From agent-starter-pack:
- `Makefile` commands
- `pyproject.toml` with proper dependencies
- Terraform modules for GCP resources
- CI/CD pipelines (Cloud Build)

### From adk-python:
- Test harness
- Evaluation framework
- Example Store patterns

### From generative-ai:
- RAG pipeline (vertex_ingest.py)
- Tracing setup
- Vector Search configuration

## Phase 4: Configuration System

Create flexible configuration:
```yaml
project:
  name: "{configurable}"
  namespace: "{configurable}"
  gcp:
    dev: "{configurable}"
    staging: "{configurable}"
    prod: "{configurable}"
features:
  a2a: false  # Optional
  rag: false  # Optional
  budgets: true
  tracing: true
```

## Next Steps

1. **Clone all repositories locally**
2. **Extract specific files following this plan**
3. **Adapt extracted code for universal use**
4. **Test with multiple configurations**

## Key Principles

1. **No invented code** - Every function traces to a source
2. **ADK 1.0 compatibility** - Verify all imports use `google.adk`
3. **Progressive complexity** - Simple → A2A → RAG
4. **Configuration over hardcoding** - Support any namespace/project

## Validation Checklist

- [ ] All agent templates extracted from adk-samples
- [ ] CLI scaffolding from agent-starter-pack  
- [ ] Evaluation from adk-python
- [ ] A2A from a2a-python
- [ ] RAG from generative-ai
- [ ] Deployment from vertex-ai-samples

This plan ensures we build from REAL, CURRENT code, not assumptions.
