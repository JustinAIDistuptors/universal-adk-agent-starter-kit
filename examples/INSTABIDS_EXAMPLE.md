# Example: Building InstaBids with Universal ADK Agent Starter Kit

This example demonstrates how to build a complete multi-agent marketplace (InstaBids) using the Universal ADK Agent Starter Kit. InstaBids connects homeowners with contractors for home improvement projects.

## Overview

InstaBids consists of 4 interconnected agents:
1. **Homeowner Agent** - Helps homeowners describe their projects
2. **Contractor Finder** - Matches projects with qualified contractors  
3. **Bid Coordinator** - Manages the bidding process
4. **Knowledge Base** - RAG-powered agent for home improvement advice

## Step 1: Initial Setup

```bash
# Clone and setup the starter kit
git clone https://github.com/JustinAIDistuptors/universal-adk-agent-starter-kit.git
cd universal-adk-agent-starter-kit
python setup.py
```

## Step 2: Configure for InstaBids

Edit `starter-kit.yaml`:

```yaml
project:
  project_id: "instabids-prod"
  location: "us-central1"
  namespace: "instabids"
  author_name: "InstaBids Team"
  author_email: "dev@instabids.ai"

agents:
  default_model: "gemini-2.0-flash"
  use_vertex: true

deployment:
  target: "agent_engine"       # Use Agent Engine for production
  enable_ci: true
  enable_monitoring: true

features:
  enable_rag: true            # For knowledge base
  enable_a2a: true            # For agent communication
  enable_evaluation: true
```

## Step 3: Create the Agents

### 3.1 Homeowner Agent
```bash
python create_agent.py --type tool --name homeowner_agent \
  --description "Helps homeowners describe their home improvement projects"
```

Customize `src/instabids/agents/homeowner_agent/agent.py`:
```python
# Extracted from google/adk-samples/agents/customer-service/
# Modified for InstaBids homeowner use case

from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from .tools import (
    capture_project_details,
    upload_project_photos,
    estimate_project_scope,
    save_to_database
)

root_agent = LlmAgent(
    name="homeowner_agent",
    model="gemini-2.0-flash",
    instruction="""You are a helpful home improvement assistant. 
    Help homeowners describe their projects clearly and completely.
    Ask about:
    - Type of project (kitchen, bathroom, landscaping, etc.)
    - Current condition and desired outcome
    - Budget range
    - Timeline preferences
    - Any specific requirements or constraints
    """,
    tools=[
        capture_project_details,
        upload_project_photos,
        estimate_project_scope,
        save_to_database
    ]
)
```

### 3.2 Contractor Finder Agent
```bash
python create_agent.py --type multi --name contractor_finder \
  --description "Matches projects with qualified contractors"
```

This creates a multi-agent system with sub-agents for:
- Qualification checking
- Geographic matching
- Specialty matching
- Availability verification

### 3.3 Bid Coordinator Agent
```bash
python create_agent.py --type simple --name bid_coordinator \
  --description "Manages the bidding process between homeowners and contractors"
```

### 3.4 Knowledge Base Agent (RAG)
```bash
python create_agent.py --type rag --name knowledge_base \
  --description "Provides home improvement advice and cost estimates"
```

## Step 4: Set Up RAG for Knowledge Base

1. Prepare your data:
```bash
# Create a CSV with home improvement data
cat > data/home_improvement_knowledge.csv << EOF
title,content,category,typical_cost
"Kitchen Remodel","Full kitchen remodels typically include...","kitchen","$15000-50000"
"Bathroom Update","Bathroom updates can range from...","bathroom","$5000-25000"
EOF
```

2. Ingest into Vertex AI Vector Search:
```bash
cd src/instabids/agents/knowledge_base
python ingest_knowledge.py --csv ../../../data/home_improvement_knowledge.csv
```

## Step 5: Enable Agent-to-Agent Communication

The A2A protocol allows agents to communicate. With `enable_a2a: true`, each agent gets an A2A bridge automatically.

Update `a2a_manifest.yaml`:
```yaml
agents:
  - name: homeowner_agent
    identity: instabids.homeowner
    endpoint: https://homeowner-agent-instabids-prod.a.run.app
    capabilities: ["project_capture", "photo_upload"]
    
  - name: contractor_finder
    identity: instabids.contractor_finder
    endpoint: https://contractor-finder-instabids-prod.a.run.app
    capabilities: ["contractor_search", "qualification_check"]
    
  - name: bid_coordinator
    identity: instabids.bid_coordinator
    endpoint: https://bid-coordinator-instabids-prod.a.run.app
    capabilities: ["bid_management", "negotiation"]
    
  - name: knowledge_base
    identity: instabids.knowledge
    endpoint: https://knowledge-base-instabids-prod.a.run.app
    capabilities: ["cost_estimation", "advice"]
```

## Step 6: Create the Orchestration Flow

Create a main orchestrator that coordinates all agents:

```python
# src/instabids/orchestrator.py
from google.adk.agents import LlmAgent
from google.adk.tools import AgentTool
from a2a import A2AClient

# Create A2A clients for each agent
homeowner_client = A2AClient("https://homeowner-agent-instabids-prod.a.run.app")
contractor_client = A2AClient("https://contractor-finder-instabids-prod.a.run.app")
bid_client = A2AClient("https://bid-coordinator-instabids-prod.a.run.app")
knowledge_client = A2AClient("https://knowledge-base-instabids-prod.a.run.app")

# Create agent tools
homeowner_tool = AgentTool(
    agent=homeowner_client,
    name="homeowner_agent",
    description="Helps homeowners describe their projects"
)

main_orchestrator = LlmAgent(
    name="instabids_orchestrator",
    model="gemini-2.0-flash",
    instruction="""You orchestrate the InstaBids platform.
    
    Workflow:
    1. Use homeowner_agent to capture project details
    2. Use knowledge_base for cost estimates and advice
    3. Use contractor_finder to find matching contractors
    4. Use bid_coordinator to manage the bidding process
    """,
    tools=[
        homeowner_tool,
        # ... other agent tools
    ]
)
```

## Step 7: Testing

Test each agent individually:
```bash
# Test homeowner agent
cd src/instabids/agents/homeowner_agent
adk run homeowner_agent

# Test with evaluation
pytest tests/agents/homeowner_agent/
adk eval tests/agents/homeowner_agent/homeowner_eval.json
```

Test the complete flow:
```bash
python -m instabids.orchestrator
```

## Step 8: Deployment

### Deploy Individual Agents
```bash
# Deploy each agent to Agent Engine
cd deployment/agents/homeowner_agent
terraform apply

cd ../contractor_finder
terraform apply

# ... deploy others
```

### Set Up CI/CD
The starter kit includes Cloud Build pipelines:
```yaml
# deployment/ci/instabids_pipeline.yaml
steps:
  # Test all agents
  - name: 'python:3.11'
    entrypoint: 'pytest'
    args: ['tests/']
    
  # Deploy to staging
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: 'bash'
    args:
      - '-c'
      - |
        for agent in homeowner_agent contractor_finder bid_coordinator knowledge_base; do
          cd deployment/agents/$agent
          terraform apply -auto-approve
          cd ../../..
        done
```

## Step 9: Monitoring

With `enable_monitoring: true`, you get:
- Cloud Trace for request tracking
- Cloud Logging for all agent interactions
- Looker dashboard for business metrics

Access traces:
```bash
gcloud trace traces list --project=instabids-prod
```

## Complete Example Interaction

```python
# User interaction with InstaBids
user_request = "I need to remodel my kitchen. It's about 200 sq ft and looks like it's from the 1980s."

# The orchestrator coordinates all agents:
# 1. Homeowner agent captures details
project_details = await homeowner_agent.capture_project_details(user_request)

# 2. Knowledge base provides estimates
estimate = await knowledge_base.estimate_cost(project_details)

# 3. Contractor finder locates matches  
contractors = await contractor_finder.find_matches(project_details)

# 4. Bid coordinator manages bidding
bids = await bid_coordinator.request_bids(project_details, contractors)

# Result returned to user
return {
    "project_id": "proj_12345",
    "estimated_cost": "$25,000 - $45,000",
    "contractors_found": 5,
    "bids_received": 3,
    "next_steps": "Review bids and select a contractor"
}
```

## Production Considerations

1. **Security**: Use VPC Service Controls and IAM
2. **Scaling**: Agent Engine auto-scales, but monitor costs
3. **Data**: Store all interactions in BigQuery for analytics
4. **Compliance**: Ensure contractor verification and licensing
5. **Payments**: Integrate with payment providers for bid deposits

## Summary

Using the Universal ADK Agent Starter Kit, we built a complete multi-agent marketplace with:
- ✅ 4 specialized agents working together
- ✅ RAG-powered knowledge base
- ✅ Agent-to-agent communication via A2A
- ✅ Production-ready deployment with monitoring
- ✅ CI/CD pipeline for continuous deployment

Total time from setup to deployed system: < 1 day (vs weeks of custom development)

The same pattern can be applied to build:
- E-commerce platforms
- Customer service systems
- Educational platforms
- Healthcare coordinators
- Financial advisors
- Any multi-agent application!
