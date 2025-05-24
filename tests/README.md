# Tests Directory

This directory will contain testing utilities and patterns extracted from official repositories.

## Planned Structure (To Be Extracted):

### `/core/`
Testing utilities to be extracted from:
- **Source**: `google/adk-python/tests/`
- `matchers.py` - Test matching utilities
- `fixtures.py` - Test fixtures
- `test_llm_auditor.py` - Example test patterns

### `/templates/`
Test templates for each agent type:
- `test_simple_agent.py`
- `test_a2a_agent.py`
- `test_rag_agent.py`

### `/examples/`
Example Store files:
- **Source**: `google/adk-python` evalset examples
- `.evalset.json` files for evaluation
- Expected outputs and test cases

### `/integration/`
Integration tests for:
- Multi-agent communication
- RAG functionality
- Deployment verification

## Key Testing Features to Extract:

1. **ADK Evaluation Framework** - From adk-python
2. **Example Store** - Deterministic testing
3. **pytest Integration** - Standard Python testing
4. **CI/CD Integration** - Automated testing in pipelines

## Current Status: AWAITING EXTRACTION

No test code has been added yet. All testing utilities must be extracted from the official adk-python repository.
