# Universal ADK Agent Starter Kit

> 🚀 **Build ANY type of ADK agent** - from simple chatbots to complex multi-agent systems - using production-ready templates extracted from Google's official repositories.

## ⚠️ Current Status

**The extraction framework is complete, but the actual code extraction from Google repositories needs to be run.**

### What's Ready:
- ✅ Complete extraction plan documenting exactly which files to extract
- ✅ Scripts to automate the entire process (`setup.py`, `extract.py`, `create_agent.py`)
- ✅ Some template examples created with ADK 1.0 patterns
- ✅ Full documentation and examples

### What's Needed:
Run the extraction process to pull real code from the 6 official Google repositories.

## Quick Start

```bash
# 1. Clone this repository
git clone https://github.com/JustinAIDistuptors/universal-adk-agent-starter-kit.git
cd universal-adk-agent-starter-kit

# 2. Run the setup script (this will clone source repos and extract code)
python setup.py

# 3. Configure your project
# Edit starter-kit.yaml with your GCP project details

# 4. Create your first agent
python create_agent.py --type simple --name my_first_agent

# 5. Run your agent
cd src/[your-namespace]/agents/my_first_agent
adk run my_first_agent
```

## What is this?

The Universal ADK Agent Starter Kit is a comprehensive framework that enables anyone to build Google ADK 1.0+ agents quickly and correctly. It provides:

- ✅ **Extracted Templates** - Real code from google/adk-samples, not invented patterns
- ✅ **Production Infrastructure** - Terraform, CI/CD, monitoring from agent-starter-pack
- ✅ **Flexible Configuration** - Support any namespace, project, or deployment target
- ✅ **Optional Advanced Features** - RAG, A2A protocol, evaluation frameworks
- ✅ **ADK 1.0 Compatible** - Uses the latest `google.adk` imports

## Repository Structure

```
universal-adk-agent-starter-kit/
├── setup.py                    # One-command setup script
├── extract.py                  # Extracts code from official repos
├── create_agent.py             # Creates new agents from templates
├── starter-kit.yaml            # Your project configuration
│
├── .starter-kit/               # Extracted templates (after running extract.py)
│   └── templates/
│       ├── simple_agent/       # Basic single agent
│       ├── multi_agent/        # Multi-agent with sub-agents
│       ├── rag_agent/          # RAG-enabled agent
│       └── tool_agent/         # Agent with custom tools
│
├── src/                        # Your agents live here
│   ├── core/                   # Core utilities (RAG, A2A, etc.)
│   └── {namespace}/            # Your namespace
│       └── agents/             # Your agents
│
├── deployment/                 # Infrastructure as code
│   ├── terraform/              # Terraform modules
│   └── ci/                     # CI/CD pipelines
│
├── tests/                      # Testing framework
│   ├── core/                   # Test utilities from adk-python
│   └── agents/                 # Your agent tests
│
└── docs/                       # Documentation
```

## The 6 Source Repositories

All code is extracted from these official Google repositories:

1. **[google/adk-samples](https://github.com/google/adk-samples)** - ADK agent examples
2. **[GoogleCloudPlatform/agent-starter-pack](https://github.com/GoogleCloudPlatform/agent-starter-pack)** - Production scaffolding
3. **[google/adk-python](https://github.com/google/adk-python)** - Testing framework
4. **[google/a2a-python](https://github.com/google/a2a-python)** - Agent communication
5. **[GoogleCloudPlatform/generative-ai](https://github.com/GoogleCloudPlatform/generative-ai)** - RAG implementations
6. **[GoogleCloudPlatform/vertex-ai-samples](https://github.com/GoogleCloudPlatform/vertex-ai-samples)** - Deployment patterns

## Agent Types

### 1. Simple Agent
Basic agent with tools and LLM integration:
```python
python create_agent.py --type simple --name customer_helper
```

### 2. Multi-Agent System
Orchestrator with multiple sub-agents:
```python
python create_agent.py --type multi --name support_system
```

### 3. RAG Agent
Agent with Vertex AI Vector Search for knowledge retrieval:
```python
python create_agent.py --type rag --name knowledge_assistant
```

### 4. Tool Agent
Agent with extensive custom tool integration:
```python
python create_agent.py --type tool --name automation_agent
```

## Configuration

Edit `starter-kit.yaml` to configure your project:

```yaml
project:
  project_id: "your-gcp-project-id"
  location: "us-central1"
  namespace: "mycompany"           # Your code namespace
  author_name: "Your Name"
  author_email: "your.email@example.com"

agents:
  default_model: "gemini-2.0-flash"
  use_vertex: true                 # Use Vertex AI (false = AI Studio)

deployment:
  target: "cloud_run"              # or "agent_engine"
  enable_ci: true
  enable_monitoring: true

features:
  enable_rag: false                # Enable RAG features
  enable_a2a: false                # Enable agent-to-agent communication
  enable_evaluation: true          # Enable testing framework
```

## How It Works

### 1. Setup Phase
```bash
python setup.py
```
- Clones official Google repositories
- Runs `extract.py` to pull real code
- Sets up Python environment with ADK 1.0+
- Creates configuration template

### 2. Development Phase
```bash
python create_agent.py --type simple --name my_agent
```
- Uses extracted templates (not invented code)
- Applies your configuration (namespace, project, etc.)
- Creates agent structure with tests and deployment
- Generates proper ADK 1.0 imports

### 3. Testing Phase
```bash
# Run locally
adk run my_agent

# Run tests
pytest tests/agents/my_agent/

# Run evaluation
adk eval tests/agents/my_agent/my_agent_eval.json
```

### 4. Deployment Phase
```bash
# Deploy to Cloud Run
cd deployment/agents/my_agent
terraform apply

# Or deploy to Agent Engine
python deployment/deploy.py --agent my_agent
```

## Examples

See `examples/INSTABIDS_EXAMPLE.md` for a complete example of building a multi-agent marketplace.

## Source Attribution

Every file extracted includes attribution comments pointing to its source repository. The extraction process is documented in:
- `EXTRACTION_SCRIPT.md` - Detailed file mappings
- `extract.py` - Automated extraction script

## Requirements

- Python 3.9+
- Google Cloud Project (for deployment)
- ADK 1.0+ (installed automatically)

## Troubleshooting

### "Templates not found"
Run `python setup.py` to clone repositories and extract templates.

### "ADK command not found"
Activate your virtual environment: `source venv/bin/activate`

### "Import error: google.adk"
The setup script installs ADK 1.0+. If you installed manually, ensure you have the latest version.

## Contributing

This starter kit extracts code from official Google repositories. To contribute:
1. Identify the source repository and file
2. Update `extract.py` with the new extraction
3. Ensure proper attribution is included
4. Test with ADK 1.0+

## License

This project extracts code from various Google repositories, each with their own licenses. See the attribution comments in each file for the source repository and its license.

---

Built with ❤️ by the community for the community. Not an official Google product.
