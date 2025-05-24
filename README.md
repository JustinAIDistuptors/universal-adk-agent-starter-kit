# Universal ADK Agent Starter Kit

> 🚀 **Build ANY type of ADK agent** - from simple chatbots to complex multi-agent systems - using production-ready templates extracted from Google's official repositories.

## What is this?

The Universal ADK Agent Starter Kit is a comprehensive framework that enables anyone to build Google ADK 1.0+ agents quickly and correctly. It provides:

- ✅ **Extracted Templates** - Real code from google/adk-samples, not invented patterns
- ✅ **Production Infrastructure** - Terraform, CI/CD, monitoring from agent-starter-pack
- ✅ **Flexible Configuration** - Support any namespace, project, or deployment target
- ✅ **Optional Advanced Features** - RAG, A2A protocol, evaluation frameworks
- ✅ **ADK 1.0 Compatible** - Uses the latest `google.adk` imports

## Quick Start

```bash
# 1. Clone this repository
git clone https://github.com/JustinAIDistuptors/universal-adk-agent-starter-kit.git
cd universal-adk-agent-starter-kit

# 2. Run the setup script
python setup.py

# 3. Configure your project
# Edit starter-kit.yaml with your GCP project details

# 4. Create your first agent
python create_agent.py --type simple --name my_first_agent

# 5. Run your agent
cd src/[your-namespace]/agents/my_first_agent
adk run my_first_agent
```

## Repository Structure

```
universal-adk-agent-starter-kit/
├── setup.py                    # One-command setup script
├── extract.py                  # Extracts code from official repos
├── create_agent.py             # Creates new agents from templates
├── starter-kit.yaml            # Your project configuration
│
├── .starter-kit/               # Extracted templates (after setup)
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
- Extracts agent templates and infrastructure code
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

## Advanced Features

### Enable RAG (Retrieval-Augmented Generation)
1. Set `enable_rag: true` in starter-kit.yaml
2. Create a RAG agent: `python create_agent.py --type rag --name doc_expert`
3. Configure Vertex AI Vector Search in the agent

### Enable A2A (Agent-to-Agent Communication)
1. Set `enable_a2a: true` in starter-kit.yaml
2. Agents automatically get A2A bridge code
3. See `a2a_manifest.yaml` for agent registry

### Production CI/CD
1. Set `enable_ci: true` in starter-kit.yaml
2. Push to GitHub
3. Cloud Build automatically tests and deploys

## Source Attribution

All code in this repository is extracted from official Google repositories:

- **Agent Templates**: [google/adk-samples](https://github.com/google/adk-samples)
- **Infrastructure**: [GoogleCloudPlatform/agent-starter-pack](https://github.com/GoogleCloudPlatform/agent-starter-pack)
- **Testing Framework**: [google/adk-python](https://github.com/google/adk-python)
- **A2A Protocol**: [google/A2A](https://github.com/google/A2A)
- **RAG Implementation**: [GoogleCloudPlatform/generative-ai](https://github.com/GoogleCloudPlatform/generative-ai)

Every extracted file includes attribution comments pointing to its source.

## Requirements

- Python 3.9+
- Google Cloud Project (for deployment)
- ADK 1.0+ (installed automatically)

## Troubleshooting

### "Templates not found"
Run `python extract.py` to extract templates from source repositories.

### "ADK command not found"
Activate your virtual environment: `source venv/bin/activate`

### "Import error: google.adk"
Install ADK 1.0+: `pip install google-adk>=1.0.0`

### Deployment Issues
Check that your GCP project has the required APIs enabled:
- Vertex AI API
- Cloud Run API (if using Cloud Run)
- Cloud Build API (if using CI/CD)

## Examples

### Example 1: Simple Customer Service Bot
```bash
# Create the agent
python create_agent.py --type simple --name customer_bot \
  --description "Handles customer inquiries"

# Customize the agent
cd src/mycompany/agents/customer_bot
# Edit agent.py to add your business logic

# Test locally
adk run customer_bot

# Deploy to production
cd deployment/agents/customer_bot
terraform apply
```

### Example 2: Multi-Agent Research System
```bash
# Create multi-agent system
python create_agent.py --type multi --name research_system \
  --description "Coordinates multiple research agents"

# The system includes:
# - Orchestrator agent
# - Web search sub-agent  
# - Summary sub-agent
# - Citation sub-agent
```

### Example 3: RAG-Powered Documentation Assistant
```bash
# Enable RAG in config
# Edit starter-kit.yaml: enable_rag: true

# Create RAG agent
python create_agent.py --type rag --name doc_assistant \
  --description "Answers questions using company documentation"

# Configure vector search
# Follow setup in src/mycompany/agents/doc_assistant/README.md
```

## Contributing

This starter kit is built by extracting code from official Google repositories. To contribute:

1. Identify the source repository and file
2. Update `extract.py` with the new extraction
3. Ensure proper attribution is included
4. Test with ADK 1.0+

## License

This project extracts code from various Google repositories, each with their own licenses. See the attribution comments in each file for the source repository and its license.

---

Built with ❤️ by the community for the community. Not an official Google product.
