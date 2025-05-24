# Quick Start Guide

Welcome to the Universal ADK Agent Starter Kit! This guide will help you build your first agent in under 30 minutes.

## Prerequisites

Before you begin, ensure you have:

- **Python 3.12+** installed
- **Google Cloud Platform account** with a project created
- **gcloud CLI** installed and configured
- **Poetry** for dependency management (`pip install poetry`)

## 🚀 5-Minute Setup

### 1. Clone and Install

```bash
# Clone the repository
git clone https://github.com/JustinAIDistuptors/universal-adk-agent-starter-kit.git
cd universal-adk-agent-starter-kit

# Install dependencies
poetry install

# Verify ADK installation
make verify-adk
```

### 2. Initialize Your Project

Run the interactive setup wizard:

```bash
make init
```

The wizard will ask for:
- Your project namespace (e.g., `mycompany`)
- GCP project IDs for dev/staging/prod
- Which features to enable (A2A, RAG, etc.)
- Default configurations

This creates a personalized `starter-kit.yaml` configuration file.

### 3. Create Your First Agent

```bash
# Create a simple agent
make new-agent TYPE=simple NAME=hello_agent
```

This generates:
```
src/{namespace}/agents/hello_agent/
├── __init__.py
├── agent.py         # Main agent logic
├── tools.py         # Agent tools/functions
├── config.yaml      # Agent-specific config
└── requirements.txt # Additional dependencies
```

### 4. Test Your Agent Locally

```bash
# Run tests
make test

# Start local development server
cd src/{namespace}/agents/hello_agent
poetry run python agent.py
```

Visit http://localhost:8000 to interact with your agent.

### 5. Deploy to Staging

```bash
# Deploy to Google Cloud
make deploy-staging
```

This will:
- Build your agent container
- Deploy to Cloud Run or Agent Engine
- Set up monitoring and tracing
- Apply budget controls
- Return your agent's public URL

## 📚 Next Steps

### Add More Features

**Enable Agent-to-Agent Communication:**
```bash
make enable-a2a
make new-agent TYPE=a2a NAME=coordinator_agent
```

**Enable Knowledge Base (RAG):**
```bash
make enable-rag
make ingest-docs
make new-agent TYPE=rag NAME=knowledge_agent
```

### Explore Examples

Check out the full examples:
- `examples/simple_bot/` - Basic customer service agent
- `examples/instabids/` - Multi-agent marketplace
- `examples/research_team/` - Collaborative research agents

### Production Deployment

When ready for production:

```bash
# Run comprehensive tests
make test

# Deploy to production (requires confirmation)
make deploy-prod
```

## 🎯 Common Patterns

### Simple Agent (FAQ Bot)

```python
from google.adk import Agent

agent = Agent(
    name="faq_bot",
    model="gemini-2.0-flash",
    instructions="You are a helpful FAQ assistant.",
    tools=[answer_question]
)
```

### A2A-Enabled Agent

```python
from google.adk import Agent
from src.core.a2a import A2AServer

agent = Agent(
    name="coordinator",
    model="gemini-2.0-flash",
    tools=[delegate_to_agent]
)

server = A2AServer(agent=agent, port=8080)
```

### RAG-Enabled Agent

```python
from google.adk import Agent
from src.core.rag import search_internal_docs

agent = Agent(
    name="knowledge_expert",
    model="gemini-2.0-flash",
    tools=[search_internal_docs]
)
```

## 🔧 Troubleshooting

### ADK Import Errors
```bash
# Ensure ADK 1.0+ is installed
pip install google-adk>=1.0
```

### GCP Authentication Issues
```bash
# Authenticate with Google Cloud
gcloud auth application-default login
```

### Deployment Failures
Check Cloud Build logs:
```bash
gcloud builds list --limit=5
gcloud builds log <BUILD_ID>
```

## 📖 Learn More

- [Architecture Overview](ARCHITECTURE.md)
- [Feature Guides](features/)
- [API Reference](api/)
- [Contributing Guide](CONTRIBUTING.md)

## 💬 Get Help

- Open an issue on [GitHub](https://github.com/JustinAIDistuptors/universal-adk-agent-starter-kit/issues)
- Check the [FAQ](FAQ.md)
- Join our [Discord community](#)

---

**Ready to build something amazing? Let's go! 🚀**
