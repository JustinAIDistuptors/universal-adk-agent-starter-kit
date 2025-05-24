#!/usr/bin/env python3
"""
Universal ADK Agent Starter Kit - Extraction Script

This script extracts files from official Google ADK repositories and
transforms them into configurable templates for the Universal ADK Starter Kit.

IMPORTANT: This script must be run after cloning all source repositories.
Every extracted file includes proper attribution to its source.
"""

import os
import re
import json
from pathlib import Path
import shutil
from typing import Dict, List, Tuple

# Define all extractions with source and destination
EXTRACTIONS = [
    # ========== Simple Agent Template (from llm-auditor) ==========
    {
        "source": "adk-samples/agents/llm-auditor/llm_auditor/agent.py",
        "dest": ".starter-kit/templates/simple_agent/agent.py",
        "transform": "make_configurable",
        "attribution": "google/adk-samples/agents/llm-auditor/"
    },
    {
        "source": "adk-samples/agents/llm-auditor/llm_auditor/prompt.py",
        "dest": ".starter-kit/templates/simple_agent/prompt.py",
        "transform": "make_configurable",
        "attribution": "google/adk-samples/agents/llm-auditor/"
    },
    {
        "source": "adk-samples/agents/llm-auditor/pyproject.toml",
        "dest": ".starter-kit/templates/simple_agent/pyproject.toml.template",
        "transform": "templatize_pyproject",
        "attribution": "google/adk-samples/agents/llm-auditor/"
    },
    {
        "source": "adk-samples/agents/llm-auditor/README.md",
        "dest": ".starter-kit/templates/simple_agent/README.md.template",
        "transform": "templatize_readme",
        "attribution": "google/adk-samples/agents/llm-auditor/"
    },
    {
        "source": "adk-samples/agents/llm-auditor/.env.example",
        "dest": ".starter-kit/templates/simple_agent/.env.example",
        "transform": "make_env_configurable",
        "attribution": "google/adk-samples/agents/llm-auditor/"
    },
    
    # ========== Multi-Agent Template (llm-auditor sub-agents) ==========
    {
        "source": "adk-samples/agents/llm-auditor/llm_auditor/sub_agents/critic/agent.py",
        "dest": ".starter-kit/templates/multi_agent/sub_agents/critic/agent.py",
        "transform": "make_configurable",
        "attribution": "google/adk-samples/agents/llm-auditor/sub_agents/"
    },
    {
        "source": "adk-samples/agents/llm-auditor/llm_auditor/sub_agents/reviser/agent.py",
        "dest": ".starter-kit/templates/multi_agent/sub_agents/reviser/agent.py",
        "transform": "make_configurable",
        "attribution": "google/adk-samples/agents/llm-auditor/sub_agents/"
    },
    
    # ========== RAG Agent Template ==========
    {
        "source": "adk-samples/agents/RAG/rag/agent.py",
        "dest": ".starter-kit/templates/rag_agent/agent.py",
        "transform": "make_configurable",
        "attribution": "google/adk-samples/agents/RAG/"
    },
    {
        "source": "adk-samples/agents/RAG/rag/tools/",
        "dest": ".starter-kit/templates/rag_agent/tools/",
        "transform": "copy_directory",
        "attribution": "google/adk-samples/agents/RAG/tools/"
    },
    
    # ========== Tool Agent Template (customer-service) ==========
    {
        "source": "adk-samples/agents/customer-service/customer_service/agent.py",
        "dest": ".starter-kit/templates/tool_agent/agent.py",
        "transform": "make_configurable",
        "attribution": "google/adk-samples/agents/customer-service/"
    },
    {
        "source": "adk-samples/agents/customer-service/customer_service/tools.py",
        "dest": ".starter-kit/templates/tool_agent/tools.py",
        "transform": "make_configurable",
        "attribution": "google/adk-samples/agents/customer-service/"
    },
    
    # ========== Testing Framework (from adk-python) ==========
    {
        "source": "adk-python/tests/matchers.py",
        "dest": "tests/core/matchers.py",
        "transform": "add_attribution_only",
        "attribution": "google/adk-python/tests/"
    },
    {
        "source": "adk-python/tests/fixtures.py",
        "dest": "tests/core/fixtures.py",
        "transform": "add_attribution_only",
        "attribution": "google/adk-python/tests/"
    },
    
    # ========== Deployment Infrastructure (from agent-starter-pack) ==========
    {
        "source": "agent-starter-pack/agents/adk_base/deployment/terraform/",
        "dest": "deployment/terraform/",
        "transform": "copy_terraform",
        "attribution": "GoogleCloudPlatform/agent-starter-pack/deployment/"
    },
    {
        "source": "agent-starter-pack/agents/adk_base/deployment/ci/",
        "dest": "deployment/ci/",
        "transform": "copy_directory",
        "attribution": "GoogleCloudPlatform/agent-starter-pack/deployment/"
    },
    {
        "source": "agent-starter-pack/agents/adk_base/Makefile",
        "dest": "Makefile.template",
        "transform": "templatize_makefile",
        "attribution": "GoogleCloudPlatform/agent-starter-pack/"
    },
]

def add_attribution(content: str, file_type: str, attribution: str) -> str:
    """Add attribution comment to file content based on file type."""
    if file_type == '.py':
        return f'''# Extracted from {attribution}
# Part of the Universal ADK Agent Starter Kit
# Original source: https://github.com/{attribution}

{content}'''
    elif file_type in ['.yaml', '.yml']:
        return f'''# Extracted from {attribution}
# Part of the Universal ADK Agent Starter Kit
# Original source: https://github.com/{attribution}

{content}'''
    elif file_type == '.md':
        return f'''<!-- Extracted from {attribution} -->
<!-- Part of the Universal ADK Agent Starter Kit -->
<!-- Original source: https://github.com/{attribution} -->

{content}'''
    elif file_type == '.toml':
        return f'''# Extracted from {attribution}
# Part of the Universal ADK Agent Starter Kit
# Original source: https://github.com/{attribution}

{content}'''
    else:
        return content

def make_configurable(content: str) -> str:
    """Replace hardcoded values with template variables."""
    replacements = [
        # Project IDs
        (r'project[_-]?id\s*=\s*["\'][\w-]+["\']', 'project_id = "{{project_id}}"'),
        (r'PROJECT_ID\s*=\s*["\'][\w-]+["\']', 'PROJECT_ID = "{{project_id}}"'),
        
        # Agent names
        (r'name\s*=\s*["\'][\w_-]+["\']', 'name = "{{agent_name}}"'),
        (r'agent_name\s*=\s*["\'][\w_-]+["\']', 'agent_name = "{{agent_name}}"'),
        
        # Model names (keep Gemini but make configurable)
        (r'model\s*=\s*["\']gemini-[\w.-]+["\']', 'model = "{{model_name|default:gemini-2.0-flash}}"'),
        
        # Locations
        (r'location\s*=\s*["\'][\w-]+["\']', 'location = "{{location|default:us-central1}}"'),
        
        # Package names in imports (for namespace configuration)
        (r'from llm_auditor', 'from {{namespace}}.agents.{{agent_name}}'),
        (r'from customer_service', 'from {{namespace}}.agents.{{agent_name}}'),
        (r'from rag', 'from {{namespace}}.agents.{{agent_name}}'),
    ]
    
    result = content
    for pattern, replacement in replacements:
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
    
    return result

def templatize_pyproject(content: str) -> str:
    """Convert pyproject.toml to template."""
    # Replace package name
    content = re.sub(r'name = "[\w-]+"', 'name = "{{agent_name}}"', content)
    # Replace description
    content = re.sub(r'description = ".*?"', 'description = "{{agent_description}}"', content)
    # Replace authors
    content = re.sub(r'authors = \[.*?\]', 'authors = ["{{author_name}} <{{author_email}}>"]', content, flags=re.DOTALL)
    return content

def templatize_readme(content: str) -> str:
    """Convert README.md to template."""
    # Replace agent-specific names with placeholders
    content = re.sub(r'# [\w\s-]+ Agent', '# {{agent_display_name}} Agent', content)
    content = re.sub(r'llm[_-]auditor', '{{agent_name}}', content, flags=re.IGNORECASE)
    content = re.sub(r'customer[_-]service', '{{agent_name}}', content, flags=re.IGNORECASE)
    return content

def make_env_configurable(content: str) -> str:
    """Make .env.example configurable."""
    # Add universal configuration at the top
    universal_config = '''# Universal ADK Starter Kit Configuration
# Project Configuration
PROJECT_ID={{project_id}}
LOCATION={{location|default:us-central1}}
NAMESPACE={{namespace}}
AGENT_NAME={{agent_name}}

# Model Configuration  
MODEL_NAME={{model_name|default:gemini-2.0-flash}}
GOOGLE_GENAI_USE_VERTEXAI={{use_vertex|default:true}}

# Original configuration from source agent:
'''
    return universal_config + content

def templatize_makefile(content: str) -> str:
    """Convert Makefile to template."""
    # Replace hardcoded values
    content = re.sub(r'PROJECT_ID\s*:?=\s*[\w-]+', 'PROJECT_ID := {{project_id}}', content)
    content = re.sub(r'AGENT_NAME\s*:?=\s*[\w-]+', 'AGENT_NAME := {{agent_name}}', content)
    return content

def copy_terraform(source_path: str, dest_path: str) -> None:
    """Copy Terraform files and templatize variables."""
    if os.path.isdir(source_path):
        shutil.copytree(source_path, dest_path, dirs_exist_ok=True)
        # Process all .tf files
        for tf_file in Path(dest_path).rglob('*.tf'):
            content = tf_file.read_text()
            # Make variables configurable
            content = re.sub(r'default\s*=\s*"[\w-]+"', 'default = "{{project_id}}"', content)
            tf_file.write_text(content)

def process_extraction(extraction: Dict[str, str], source_base: Path, dest_base: Path) -> None:
    """Process a single extraction."""
    source_path = source_base / extraction["source"]
    dest_path = dest_base / extraction["dest"]
    
    # Ensure destination directory exists
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    
    transform = extraction["transform"]
    attribution = extraction["attribution"]
    
    print(f"Extracting: {extraction['source']} -> {extraction['dest']}")
    
    try:
        if transform == "copy_directory":
            if source_path.is_dir():
                shutil.copytree(source_path, dest_path, dirs_exist_ok=True)
                # Add attribution to all Python files
                for py_file in dest_path.rglob('*.py'):
                    content = py_file.read_text()
                    content = add_attribution(content, '.py', attribution)
                    py_file.write_text(content)
        
        elif transform == "copy_terraform":
            copy_terraform(str(source_path), str(dest_path))
        
        else:
            # Read source file
            content = source_path.read_text()
            
            # Get file extension
            file_ext = source_path.suffix
            
            # Apply transformation
            if transform == "make_configurable":
                content = make_configurable(content)
            elif transform == "templatize_pyproject":
                content = templatize_pyproject(content)
            elif transform == "templatize_readme":
                content = templatize_readme(content)
            elif transform == "make_env_configurable":
                content = make_env_configurable(content)
            elif transform == "templatize_makefile":
                content = templatize_makefile(content)
            
            # Add attribution
            content = add_attribution(content, file_ext, attribution)
            
            # Write to destination
            dest_path.write_text(content)
            
        print(f"  ✓ Extracted successfully")
        
    except Exception as e:
        print(f"  ✗ Error: {e}")

def main():
    """Main extraction process."""
    print("Universal ADK Agent Starter Kit - Extraction Process")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("EXTRACTION_SCRIPT.md").exists():
        print("ERROR: Run this script from the universal-adk-agent-starter-kit directory")
        return
    
    # Source repositories base path
    source_base = Path("../")  # Assumes repos are cloned in parent directory
    dest_base = Path(".")
    
    # Check if source repositories exist
    required_repos = ["adk-samples", "agent-starter-pack", "adk-python", "A2A", "generative-ai"]
    missing_repos = []
    
    for repo in required_repos:
        if not (source_base / repo).exists():
            missing_repos.append(repo)
    
    if missing_repos:
        print(f"ERROR: Missing source repositories: {', '.join(missing_repos)}")
        print("\nPlease clone all repositories first:")
        print("cd ..")
        for repo in missing_repos:
            if repo == "adk-samples":
                print(f"git clone https://github.com/google/{repo}.git")
            elif repo == "A2A":
                print(f"git clone https://github.com/google/{repo}.git")
            elif repo == "adk-python":
                print(f"git clone https://github.com/google/{repo}.git")
            else:
                print(f"git clone https://github.com/GoogleCloudPlatform/{repo}.git")
        return
    
    print(f"Source repositories found in: {source_base.absolute()}")
    print(f"Extracting to: {dest_base.absolute()}")
    print()
    
    # Process each extraction
    successful = 0
    failed = 0
    
    for extraction in EXTRACTIONS:
        try:
            process_extraction(extraction, source_base, dest_base)
            successful += 1
        except Exception as e:
            print(f"Failed to extract {extraction['source']}: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Extraction complete: {successful} successful, {failed} failed")
    
    # Create configuration template
    print("\nCreating starter-kit.yaml configuration template...")
    config_template = {
        "project": {
            "project_id": "your-gcp-project-id",
            "location": "us-central1",
            "namespace": "mycompany",
            "author_name": "Your Name",
            "author_email": "your.email@example.com"
        },
        "agents": {
            "default_model": "gemini-2.0-flash",
            "use_vertex": True
        },
        "deployment": {
            "target": "cloud_run",  # or "agent_engine"
            "enable_ci": True,
            "enable_monitoring": True
        },
        "features": {
            "enable_rag": False,
            "enable_a2a": False,
            "enable_evaluation": True
        }
    }
    
    with open("starter-kit.yaml", "w") as f:
        import yaml
        yaml.dump(config_template, f, default_flow_style=False)
    
    print("✓ Created starter-kit.yaml configuration template")
    
    print("\nNext steps:")
    print("1. Review extracted files in .starter-kit/templates/")
    print("2. Configure starter-kit.yaml with your project settings")
    print("3. Run: python create_agent.py --type simple --name my_first_agent")

if __name__ == "__main__":
    main()
