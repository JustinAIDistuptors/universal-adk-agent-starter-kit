# Universal ADK Agent Starter Kit - Extraction Script

This script documents the exact files to extract from official Google repositories.

## Phase 1: Agent Templates from google/adk-samples

### Simple Agent Template
**Source**: `google/adk-samples/agents/llm-auditor/`
```bash
# Files to extract:
agents/llm-auditor/llm_auditor/agent.py → .starter-kit/templates/simple_agent/agent.py
agents/llm-auditor/llm_auditor/prompt.py → .starter-kit/templates/simple_agent/prompt.py
agents/llm-auditor/llm_auditor/__init__.py → .starter-kit/templates/simple_agent/__init__.py
agents/llm-auditor/pyproject.toml → .starter-kit/templates/simple_agent/pyproject.toml.template
agents/llm-auditor/README.md → .starter-kit/templates/simple_agent/README.md.template
agents/llm-auditor/.env.example → .starter-kit/templates/simple_agent/.env.example
```

### Multi-Agent Template (with sub-agents)
**Source**: `google/adk-samples/agents/llm-auditor/`
```bash
# Files to extract:
agents/llm-auditor/llm_auditor/sub_agents/critic/agent.py → .starter-kit/templates/multi_agent/sub_agents/critic/agent.py
agents/llm-auditor/llm_auditor/sub_agents/critic/prompt.py → .starter-kit/templates/multi_agent/sub_agents/critic/prompt.py
agents/llm-auditor/llm_auditor/sub_agents/reviser/agent.py → .starter-kit/templates/multi_agent/sub_agents/reviser/agent.py
agents/llm-auditor/llm_auditor/sub_agents/reviser/prompt.py → .starter-kit/templates/multi_agent/sub_agents/reviser/prompt.py
```

### RAG Agent Template
**Source**: `google/adk-samples/agents/RAG/`
```bash
# Files to extract:
agents/RAG/rag/agent.py → .starter-kit/templates/rag_agent/agent.py
agents/RAG/rag/tools/ → .starter-kit/templates/rag_agent/tools/
agents/RAG/README.md → .starter-kit/templates/rag_agent/README.md.template
```

### Customer Service Template (with tools)
**Source**: `google/adk-samples/agents/customer-service/`
```bash
# Files to extract:
agents/customer-service/customer_service/agent.py → .starter-kit/templates/tool_agent/agent.py
agents/customer-service/customer_service/tools.py → .starter-kit/templates/tool_agent/tools.py
agents/customer-service/customer_service/config.py → .starter-kit/templates/tool_agent/config.py
```

## Phase 2: Scaffolding from GoogleCloudPlatform/agent-starter-pack

### CLI Tool
**Source**: `GoogleCloudPlatform/agent-starter-pack`
```bash
# The CLI is installed via pip, but we need to extract:
# - The command patterns
# - The template structure it creates
# - The configuration it uses
```

### Deployment Infrastructure
**Source**: `GoogleCloudPlatform/agent-starter-pack/agents/*/deployment/`
```bash
# Files to extract:
deployment/terraform/ → deployment/terraform/
deployment/ci/pr_checks.yaml → deployment/ci/pr_checks.yaml
deployment/ci/staging_deployment.yaml → deployment/ci/staging_deployment.yaml
deployment/ci/prod_deployment.yaml → deployment/ci/prod_deployment.yaml
Makefile → Makefile.template
```

## Phase 3: Evaluation Framework from google/adk-python

### Testing Utilities
**Source**: `google/adk-python/tests/`
```bash
# Files to extract:
tests/matchers.py → tests/core/matchers.py
tests/fixtures.py → tests/core/fixtures.py
tests/test_llm_auditor.py → tests/templates/test_agent_template.py
```

### Example Store Format
**Source**: `google/adk-python/samples_for_testing/`
```bash
# Files to extract:
samples_for_testing/hello_world/hello_world_eval_set_001.evalset.json → tests/examples/evalset_template.json
```

## Phase 4: A2A Protocol from google/a2a-python

### Bridge Template
**Source**: `google/A2A/samples/python/agents/google_adk/`
```bash
# Files to extract:
samples/python/agents/google_adk/server.py → src/core/a2a/bridge_template.py
samples/python/agents/google_adk/agent.py → src/core/a2a/a2a_agent_example.py
```

## Phase 5: RAG Implementation from GoogleCloudPlatform/generative-ai

### Vector Search Implementation
**Source**: `GoogleCloudPlatform/generative-ai/gemini/rag-engine/`
```bash
# Notebooks to convert:
gemini/rag-engine/rag_engine_vector_search.ipynb → (convert to) src/core/rag/vertex_ingest.py
```

### Tracing Implementation
**Source**: `GoogleCloudPlatform/generative-ai/gemini/agent-engine/`
```bash
# Notebooks to convert:
gemini/agent-engine/tracing_agents_in_agent_engine.ipynb → (convert to) src/core/observability/trace_helpers.py
```

## Extraction Commands

### Step 1: Clone all repositories
```bash
mkdir ~/adk-extraction && cd ~/adk-extraction

# Clone all source repositories
git clone https://github.com/google/adk-samples.git
git clone https://github.com/GoogleCloudPlatform/agent-starter-pack.git
git clone https://github.com/google/adk-python.git
git clone https://github.com/google/A2A.git
git clone https://github.com/GoogleCloudPlatform/generative-ai.git
```

### Step 2: Run extraction script
```python
#!/usr/bin/env python3
"""
Extract files from official Google ADK repositories
Each file copied includes attribution comment
"""

import shutil
import os
from pathlib import Path

EXTRACTIONS = [
    # Simple agent template
    {
        "source": "adk-samples/agents/llm-auditor/llm_auditor/agent.py",
        "dest": ".starter-kit/templates/simple_agent/agent.py",
        "attribution": "Extracted from google/adk-samples/agents/llm-auditor/"
    },
    # Add all other files...
]

def extract_with_attribution(source, dest, attribution):
    """Copy file and add attribution comment"""
    dest_path = Path(dest)
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(source, 'r') as f:
        content = f.read()
    
    # Add attribution
    if dest.endswith('.py'):
        attributed_content = f'# {attribution}\n# Original file: {source}\n\n{content}'
    else:
        attributed_content = content
    
    with open(dest, 'w') as f:
        f.write(attributed_content)
    
    print(f"Extracted: {source} → {dest}")

# Run extractions
for extraction in EXTRACTIONS:
    extract_with_attribution(
        extraction["source"],
        extraction["dest"],
        extraction["attribution"]
    )
```

## Important Notes

1. **ADK 1.0 Compatibility**: All imports must use `from google.adk` (not older imports)
2. **Attribution**: Every extracted file must include attribution comment
3. **Configurability**: Replace hardcoded values with template variables:
   - Project names → `{{project_id}}`
   - Agent names → `{{agent_name}}`
   - Namespaces → `{{namespace}}`
4. **Testing**: Each extracted component must be tested with ADK 1.0

## Verification Checklist

- [ ] All Python files import from `google.adk` (ADK 1.0)
- [ ] No hardcoded project IDs or agent names
- [ ] Attribution comments in all extracted files
- [ ] Templates are configurable via starter-kit.yaml
- [ ] Evaluation framework works with ADK 1.0
- [ ] A2A bridges are compatible with latest protocol
- [ ] RAG implementation uses Vertex AI Vector Search GA APIs
