# Universal ADK Agent Starter Kit - Extraction Progress Tracker
## Last Updated: 2024-01-24 06:57:00 UTC

This document tracks which files have been extracted from the 6 Google repositories.

## Extraction Progress

### From google/adk-samples
- [ ] ✅ python/agents/llm-auditor/llm_auditor/agent.py → .starter-kit/templates/simple_agent/agent.py
- [ ] ✅ python/agents/llm-auditor/llm_auditor/__init__.py → .starter-kit/templates/simple_agent/__init__.py
- [ ] ✅ python/agents/llm-auditor/pyproject.toml → .starter-kit/templates/simple_agent/pyproject.toml.template
- [ ] ❌ python/agents/llm-auditor/llm_auditor/prompt.py → .starter-kit/templates/simple_agent/prompt.py (NOT FOUND)
- [ ] ⏳ python/agents/llm-auditor/llm_auditor/sub_agents/critic/agent.py → .starter-kit/templates/multi_agent/sub_agents/critic/agent.py
- [ ] ⏳ python/agents/llm-auditor/llm_auditor/sub_agents/critic/prompt.py → .starter-kit/templates/multi_agent/sub_agents/critic/prompt.py
- [ ] ⏳ python/agents/llm-auditor/llm_auditor/sub_agents/reviser/agent.py → .starter-kit/templates/multi_agent/sub_agents/reviser/agent.py
- [ ] ⏳ python/agents/llm-auditor/llm_auditor/sub_agents/reviser/prompt.py → .starter-kit/templates/multi_agent/sub_agents/reviser/prompt.py
- [ ] ⏳ python/agents/RAG/rag/agent.py → .starter-kit/templates/rag_agent/agent.py
- [ ] ⏳ python/agents/RAG/rag/tools/ → .starter-kit/templates/rag_agent/tools/
- [ ] ⏳ python/agents/customer-service/customer_service/agent.py → .starter-kit/templates/tool_agent/agent.py
- [ ] ⏳ python/agents/customer-service/customer_service/tools.py → .starter-kit/templates/tool_agent/tools.py

### From google/adk-python
- [ ] ⏳ tests/matchers.py → tests/core/matchers.py
- [ ] ⏳ tests/fixtures.py → tests/core/fixtures.py

### From GoogleCloudPlatform/agent-starter-pack
- [ ] ⏳ agents/adk_base/deployment/terraform/ → deployment/terraform/
- [ ] ⏳ agents/adk_base/deployment/ci/ → deployment/ci/
- [ ] ⏳ agents/adk_base/Makefile → Makefile.template

### From google/A2A
- [ ] ⏳ samples/python/agents/google_adk/server.py → src/core/a2a/bridge_template.py
- [ ] ⏳ samples/python/agents/google_adk/agent.py → src/core/a2a/a2a_agent_example.py

### From GoogleCloudPlatform/generative-ai
- [ ] ⏳ gemini/rag-engine/rag_engine_vector_search.ipynb → (convert to) src/core/rag/vertex_ingest.py
- [ ] ⏳ gemini/agent-engine/tracing_agents_in_agent_engine.ipynb → (convert to) src/core/observability/trace_helpers.py

## Legend
- ✅ Completed
- ⏳ Pending
- ❌ Not Found/Skipped

## Next Steps
Continue with llm-auditor sub_agents extraction...
