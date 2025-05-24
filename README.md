# Universal ADK Agent Starter Kit

> 🚀 Build ANY Google ADK 1.0 agent in 30 minutes - from simple chatbots to complex multi-agent marketplaces

[![ADK Version](https://img.shields.io/badge/ADK-1.0%2B-blue)](https://github.com/google/adk-python)
[![Python](https://img.shields.io/badge/python-3.12-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green)](LICENSE)

## What is this?

A production-ready template repository that enables developers (and AI agents!) to rapidly build, test, deploy, and interconnect Google ADK 1.0 agents. Whether you're building a simple FAQ bot or a complex multi-agent marketplace like InstaBids, this kit has you covered.

## ✨ Features

- **🎯 Template-Based Architecture**: Pre-built templates for different agent types
  - `simple_agent` - Basic agent with tools
  - `a2a_agent` - Agent ready for mesh communication
  - `rag_agent` - Agent with knowledge base access

- **📈 Progressive Complexity**: Start simple, add features as needed
- **🔧 Production Ready**: Built-in budgets, tracing, testing, and CI/CD
- **🌐 Multi-Agent Support**: Optional A2A protocol for agent communication
- **🧠 Knowledge Base**: Optional RAG/Vector Search for shared knowledge
- **⚙️ Fully Configurable**: Works with any GCP project and namespace

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/JustinAIDistuptors/universal-adk-agent-starter-kit.git
cd universal-adk-agent-starter-kit

# Run interactive setup
make init

# Create your first agent
make new-agent TYPE=simple NAME=hello_world

# Deploy to staging
make deploy-staging
```

## 📚 Documentation

- [Quick Start Guide](docs/QUICKSTART.md)
- [Architecture Overview](docs/ARCHITECTURE.md)
- [Feature Guides](docs/features/)
  - [Multi-Agent Communication (A2A)](docs/features/a2a.md)
  - [Knowledge Base (RAG)](docs/features/rag.md)
  - [Production Deployment](docs/features/deployment.md)

## 🎭 Examples

- **[InstaBids](examples/instabids/)** - Complete marketplace with homeowner, contractor, and bidding agents
- **[Simple Bot](examples/simple_bot/)** - Basic customer service agent
- **[Research Team](examples/research_team/)** - Multi-agent research system

## 📦 What's Included

### Core Components
- **Agent Templates** - Pre-configured agent patterns from Google's official samples
- **Scaffolding CLI** - One-command agent generation
- **Evaluation Framework** - Automated testing with Example Store
- **CI/CD Pipeline** - Cloud Build integration with staging/prod workflows
- **Observability** - OpenTelemetry tracing to Cloud Trace
- **Budget Controls** - Stay within free tier credits

### Optional Features
- **Agent-to-Agent (A2A)** - Enable agents to communicate with each other
- **RAG/Vector Search** - Give agents access to a shared knowledge base
- **Multi-Environment** - Dev, staging, and production configurations

## 🛠️ Requirements

- Python 3.12+
- Google Cloud Platform account
- ADK 1.0+ (`pip install google-adk>=1.0`)
- Poetry for dependency management

## 🗺️ Repository Structure

```
.starter-kit/              # Templates and configuration
├── templates/             # Agent templates
└── config/               # Project configuration

src/
├── {namespace}/agents/    # Your agents live here
└── core/                 # Core utilities
    ├── a2a/              # Agent communication (optional)
    ├── rag/              # Knowledge base (optional)
    └── observability/    # Tracing and monitoring

deployment/               # Infrastructure as code
├── terraform/           # Terraform modules
└── ci/                  # CI/CD pipelines

examples/                # Full working examples
docs/                    # Documentation
tests/                   # Test templates and utilities
notebooks/               # Interactive guides
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](docs/CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Built using patterns and code from:
- [google/adk-samples](https://github.com/google/adk-samples)
- [GoogleCloudPlatform/agent-starter-pack](https://github.com/GoogleCloudPlatform/agent-starter-pack)
- [google/adk-python](https://github.com/google/adk-python)
- [GoogleCloudPlatform/vertex-ai-samples](https://github.com/GoogleCloudPlatform/vertex-ai-samples)
- [google/a2a-python](https://github.com/google/a2a-python)

---

*Built with ❤️ for the ADK community*
