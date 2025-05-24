# Universal ADK Agent Starter Kit - Makefile
# Built from patterns in GoogleCloudPlatform/agent-starter-pack

.PHONY: help init new-agent test deploy-staging deploy-prod enable-rag enable-a2a ingest-docs clean

# Default namespace and project (overridden by starter-kit.yaml after init)
NAMESPACE ?= mycompany
PROJECT ?= myproject-dev
AGENT_TYPE ?= simple
AGENT_NAME ?= demo_agent

help:
	@echo "Universal ADK Agent Starter Kit"
	@echo ""
	@echo "Setup Commands:"
	@echo "  make init                    - Run interactive setup wizard"
	@echo ""
	@echo "Agent Commands:"
	@echo "  make new-agent TYPE=simple NAME=my_agent  - Create a new agent"
	@echo "  make test                    - Run all tests"
	@echo "  make deploy-staging          - Deploy to staging environment"
	@echo "  make deploy-prod             - Deploy to production"
	@echo ""
	@echo "Optional Features:"
	@echo "  make enable-rag              - Enable Vector Search/RAG"
	@echo "  make enable-a2a              - Enable Agent-to-Agent communication"
	@echo "  make ingest-docs             - Update knowledge base"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean                   - Clean build artifacts"
	@echo "  make verify-adk              - Verify ADK 1.0+ installation"

init:
	@echo "🚀 Starting Universal ADK Agent Starter Kit Setup..."
	@python3 .starter-kit/scripts/setup_wizard.py

new-agent:
	@echo "📦 Creating new $(AGENT_TYPE) agent: $(AGENT_NAME)..."
	@if [ -f ".starter-kit/config/project.yaml" ]; then \
		python3 .starter-kit/scripts/create_agent.py --type $(AGENT_TYPE) --name $(AGENT_NAME); \
	else \
		echo "❌ Error: Please run 'make init' first to configure your project"; \
		exit 1; \
	fi

test:
	@echo "🧪 Running tests..."
	@poetry run pytest tests/ -v
	@echo "✅ Running ADK evaluation..."
	@poetry run adk eval tests/examples/*.evalset.json

deploy-staging:
	@echo "🚀 Deploying to staging..."
	@cd deployment && terraform workspace select staging || terraform workspace new staging
	@cd deployment && terraform apply -var-file=environments/staging.tfvars

deploy-prod:
	@echo "🚀 Deploying to production..."
	@read -p "⚠️  Are you sure you want to deploy to production? [y/N] " confirm && \
	if [ "$$confirm" = "y" ]; then \
		cd deployment && terraform workspace select prod || terraform workspace new prod && \
		terraform apply -var-file=environments/prod.tfvars; \
	fi

enable-rag:
	@echo "🧠 Enabling RAG/Vector Search..."
	@python3 .starter-kit/scripts/enable_feature.py --feature rag

enable-a2a:
	@echo "🔗 Enabling Agent-to-Agent communication..."
	@python3 .starter-kit/scripts/enable_feature.py --feature a2a

ingest-docs:
	@echo "📚 Ingesting documentation into knowledge base..."
	@if [ -f "src/core/rag/vertex_ingest.py" ]; then \
		poetry run python -m src.core.rag.vertex_ingest --source docs/; \
	else \
		echo "❌ Error: RAG not enabled. Run 'make enable-rag' first"; \
		exit 1; \
	fi

verify-adk:
	@echo "🔍 Verifying ADK installation..."
	@python3 -c "import pkg_resources; v = pkg_resources.get_distribution('google-adk').version; print(f'✅ ADK version {v} installed')" || \
		(echo "❌ ADK not found. Installing..." && pip install google-adk>=1.0)

clean:
	@echo "🧹 Cleaning build artifacts..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@rm -rf .pytest_cache .coverage htmlcov

# Development helpers
lint:
	@poetry run ruff check src/ tests/
	@poetry run black --check src/ tests/

format:
	@poetry run black src/ tests/
	@poetry run ruff check --fix src/ tests/

# CI/CD helpers
ci-test:
	@make lint
	@make test

# Installation helper
install:
	@echo "📦 Installing dependencies..."
	@poetry install
	@make verify-adk
