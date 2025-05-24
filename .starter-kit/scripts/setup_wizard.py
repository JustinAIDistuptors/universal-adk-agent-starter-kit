#!/usr/bin/env python3
"""
Universal ADK Agent Starter Kit - Interactive Setup Wizard
Based on patterns from GoogleCloudPlatform/agent-starter-pack
"""

import os
import sys
import yaml
import subprocess
from pathlib import Path
from typing import Dict, Any

# ANSI color codes for pretty output
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
BOLD = '\033[1m'
RESET = '\033[0m'

def print_header():
    """Print welcome header"""
    print(f"""
{BLUE}{BOLD}═══════════════════════════════════════════════════════════════{RESET}
{BLUE}{BOLD}     Universal ADK Agent Starter Kit - Setup Wizard{RESET}
{BLUE}{BOLD}═══════════════════════════════════════════════════════════════{RESET}
    """)

def print_success(message: str):
    """Print success message"""
    print(f"{GREEN}✅ {message}{RESET}")

def print_error(message: str):
    """Print error message"""
    print(f"{RED}❌ {message}{RESET}")

def print_info(message: str):
    """Print info message"""
    print(f"{YELLOW}ℹ️  {message}{RESET}")

def prompt(question: str, default: str = None, required: bool = True) -> str:
    """Prompt user for input"""
    if default:
        question = f"{question} [{default}]"
    
    while True:
        answer = input(f"{BOLD}{question}: {RESET}").strip()
        
        if not answer and default:
            return default
        
        if answer or not required:
            return answer
            
        print_error("This field is required.")

def prompt_bool(question: str, default: bool = False) -> bool:
    """Prompt user for yes/no answer"""
    default_str = "Y/n" if default else "y/N"
    answer = prompt(f"{question} [{default_str}]", required=False)
    
    if not answer:
        return default
        
    return answer.lower() in ['y', 'yes', 'true', '1']

def check_prerequisites() -> bool:
    """Check if all prerequisites are installed"""
    print(f"\n{BOLD}Checking prerequisites...{RESET}")
    
    requirements = {
        "python3": "Python 3.12+",
        "gcloud": "Google Cloud SDK",
        "poetry": "Poetry (dependency management)",
        "terraform": "Terraform (infrastructure)",
    }
    
    all_good = True
    for cmd, name in requirements.items():
        try:
            subprocess.run([cmd, "--version"], capture_output=True, check=True)
            print_success(f"{name} found")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print_error(f"{name} not found - please install it first")
            all_good = False
    
    # Check ADK version
    try:
        import pkg_resources
        adk_version = pkg_resources.get_distribution('google-adk').version
        if adk_version >= "1.0":
            print_success(f"Google ADK {adk_version} found")
        else:
            print_error(f"Google ADK {adk_version} is too old - need 1.0+")
            all_good = False
    except:
        print_error("Google ADK not found - will install during setup")
    
    return all_good

def configure_project() -> Dict[str, Any]:
    """Configure project settings"""
    print(f"\n{BOLD}Project Configuration{RESET}")
    print("Let's set up your project details.\n")
    
    config = {
        "project": {
            "name": prompt("Project name", "my-adk-project"),
            "namespace": prompt("Namespace (used in imports)", "mycompany"),
            "description": prompt("Project description", "My ADK agent project"),
            "gcp": {},
            "region": prompt("Default GCP region", "us-central1"),
            "billing_account": prompt("GCP billing account ID", required=False),
        }
    }
    
    # GCP projects
    print(f"\n{BOLD}Google Cloud Projects{RESET}")
    print("Enter your GCP project IDs (or press enter to skip):\n")
    
    for env in ["dev", "staging", "prod"]:
        project_id = prompt(f"{env.capitalize()} project ID", required=False)
        if project_id:
            config["project"]["gcp"][env] = project_id
    
    if not config["project"]["gcp"]:
        print_error("Warning: No GCP projects configured. You'll need to add them later.")
    
    return config

def configure_features() -> Dict[str, Any]:
    """Configure optional features"""
    print(f"\n{BOLD}Feature Configuration{RESET}")
    print("Choose which features to enable:\n")
    
    features = {
        "a2a": {
            "enabled": prompt_bool("Enable Agent-to-Agent communication (A2A)?", False),
            "port": 8080
        },
        "rag": {
            "enabled": prompt_bool("Enable RAG/Vector Search for knowledge base?", False),
            "index_name": "agent-knowledge-base",
            "embedding_model": "textembedding-gecko@003",
            "chunk_size": 400
        },
        "budgets": {
            "enabled": prompt_bool("Enable budget controls?", True),
            "default_amount": 50,
            "alert_thresholds": [50, 80, 90, 100]
        },
        "tracing": {
            "enabled": prompt_bool("Enable OpenTelemetry tracing?", True),
            "sample_rate": 1.0
        },
        "cicd": {
            "provider": "cloudbuild",
            "auto_deploy_staging": prompt_bool("Auto-deploy to staging on commit?", True),
            "require_approval_prod": True
        }
    }
    
    return {"features": features}

def configure_agent_defaults() -> Dict[str, Any]:
    """Configure default agent settings"""
    print(f"\n{BOLD}Agent Defaults{RESET}")
    print("Configure default settings for new agents:\n")
    
    model = prompt("Default model", "gemini-2.0-flash")
    
    defaults = {
        "agent_defaults": {
            "model": model,
            "temperature": 0.7,
            "max_tokens": 2048,
            "timeout": 30,
            "default_tools": ["log_event"]
        }
    }
    
    return defaults

def save_configuration(config: Dict[str, Any]):
    """Save configuration to file"""
    config_path = Path(".starter-kit/config/project.yaml")
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    
    # Also update the root starter-kit.yaml
    with open("starter-kit.yaml", 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    
    print_success(f"Configuration saved to {config_path}")

def create_directory_structure(namespace: str):
    """Create the project directory structure"""
    print(f"\n{BOLD}Creating directory structure...{RESET}")
    
    directories = [
        f"src/{namespace}/agents",
        "src/core/a2a",
        "src/core/rag", 
        "src/core/observability",
        "deployment/terraform/modules",
        "deployment/terraform/environments",
        "deployment/ci",
        "tests/unit",
        "tests/integration",
        "tests/examples",
        "notebooks/quickstart",
        "notebooks/examples",
        "docs/features",
        "docs/api",
        "examples",
        ".starter-kit/templates/simple_agent",
        ".starter-kit/templates/a2a_agent",
        ".starter-kit/templates/rag_agent",
        ".starter-kit/scripts",
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        
    # Create __init__.py files
    init_files = [
        f"src/{namespace}/__init__.py",
        f"src/{namespace}/agents/__init__.py",
        "src/core/__init__.py",
        "src/core/a2a/__init__.py",
        "src/core/rag/__init__.py",
        "src/core/observability/__init__.py",
    ]
    
    for init_file in init_files:
        Path(init_file).touch(exist_ok=True)
    
    print_success("Directory structure created")

def install_dependencies():
    """Install project dependencies"""
    print(f"\n{BOLD}Installing dependencies...{RESET}")
    
    try:
        subprocess.run(["poetry", "install"], check=True)
        print_success("Dependencies installed")
    except subprocess.CalledProcessError:
        print_error("Failed to install dependencies")
        print_info("Run 'poetry install' manually to complete setup")

def main():
    """Main setup wizard"""
    print_header()
    
    # Check prerequisites
    if not check_prerequisites():
        print_error("\nPlease install missing prerequisites and run setup again.")
        sys.exit(1)
    
    # Gather configuration
    config = {}
    config.update(configure_project())
    config.update(configure_features())
    config.update(configure_agent_defaults())
    
    # Add remaining default configuration
    config.update({
        "development": {
            "hot_reload": True,
            "debug_mode": True,
            "local_port": 8000
        },
        "deployment": {
            "strategy": "blue-green",
            "health_check_path": "/health",
            "min_instances": 0,
            "max_instances": 10
        },
        "security": {
            "enable_vpc_sc": False,
            "enable_cmek": False,
            "allowed_domains": []
        }
    })
    
    # Save configuration
    save_configuration(config)
    
    # Create directory structure
    namespace = config["project"]["namespace"]
    create_directory_structure(namespace)
    
    # Install dependencies
    install_dependencies()
    
    # Success!
    print(f"\n{GREEN}{BOLD}✨ Setup complete!{RESET}")
    print(f"\nYour project '{config['project']['name']}' is ready.")
    print(f"\nNext steps:")
    print(f"  1. Run 'make new-agent TYPE=simple NAME=my_first_agent' to create your first agent")
    print(f"  2. Run 'make test' to verify everything is working")
    print(f"  3. Run 'make deploy-staging' when ready to deploy")
    print(f"\nHappy building! 🚀")

if __name__ == "__main__":
    main()
