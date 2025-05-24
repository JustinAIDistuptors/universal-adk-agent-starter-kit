#!/usr/bin/env python3
"""
Universal ADK Agent Starter Kit - Agent Creation Script

This script creates new ADK agents from extracted templates.
It uses the configuration from starter-kit.yaml to customize the agent.
"""

import os
import sys
import argparse
import yaml
import shutil
from pathlib import Path
from string import Template
import re

AGENT_TYPES = {
    "simple": {
        "template_path": ".starter-kit/templates/simple_agent",
        "description": "Basic single agent with tools"
    },
    "multi": {
        "template_path": ".starter-kit/templates/multi_agent",
        "description": "Multi-agent system with sub-agents"
    },
    "rag": {
        "template_path": ".starter-kit/templates/rag_agent",
        "description": "RAG-enabled agent with vector search"
    },
    "tool": {
        "template_path": ".starter-kit/templates/tool_agent",
        "description": "Agent with custom tools"
    }
}

class AgentCreator:
    def __init__(self, config_file="starter-kit.yaml"):
        """Initialize the agent creator with configuration."""
        self.config = self.load_config(config_file)
        self.template_vars = self.build_template_vars()
    
    def load_config(self, config_file):
        """Load configuration from YAML file."""
        if not Path(config_file).exists():
            print(f"ERROR: Configuration file {config_file} not found.")
            print("Please run extract.py first to create the configuration template.")
            sys.exit(1)
        
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)
    
    def build_template_vars(self):
        """Build template variables from configuration."""
        return {
            "project_id": self.config["project"]["project_id"],
            "location": self.config["project"]["location"],
            "namespace": self.config["project"]["namespace"],
            "author_name": self.config["project"]["author_name"],
            "author_email": self.config["project"]["author_email"],
            "model_name": self.config["agents"]["default_model"],
            "use_vertex": str(self.config["agents"]["use_vertex"]).lower(),
        }
    
    def process_template(self, content, agent_name, agent_description=""):
        """Process template content with variables."""
        # Add agent-specific variables
        vars = self.template_vars.copy()
        vars.update({
            "agent_name": agent_name,
            "agent_display_name": agent_name.replace("_", " ").title(),
            "agent_description": agent_description or f"ADK agent for {agent_name}"
        })
        
        # Process {{variable}} style templates
        def replace_var(match):
            var_expr = match.group(1)
            if "|" in var_expr:
                # Handle default values: {{var|default:value}}
                var_name, default_expr = var_expr.split("|", 1)
                if default_expr.startswith("default:"):
                    default_value = default_expr[8:]
                    return vars.get(var_name.strip(), default_value)
            return vars.get(var_expr.strip(), match.group(0))
        
        content = re.sub(r'\{\{([^}]+)\}\}', replace_var, content)
        return content
    
    def create_agent(self, agent_type, agent_name, agent_description=""):
        """Create a new agent from template."""
        if agent_type not in AGENT_TYPES:
            print(f"ERROR: Unknown agent type '{agent_type}'")
            print(f"Available types: {', '.join(AGENT_TYPES.keys())}")
            return False
        
        # Validate agent name
        if not re.match(r'^[a-z][a-z0-9_]*$', agent_name):
            print(f"ERROR: Agent name must be lowercase with underscores only (e.g., my_agent)")
            return False
        
        template_info = AGENT_TYPES[agent_type]
        template_path = Path(template_info["template_path"])
        
        if not template_path.exists():
            print(f"ERROR: Template directory {template_path} not found.")
            print("Please run extract.py first to extract templates from source repositories.")
            return False
        
        # Create destination path
        dest_path = Path(f"src/{self.config['project']['namespace']}/agents/{agent_name}")
        
        if dest_path.exists():
            print(f"ERROR: Agent {agent_name} already exists at {dest_path}")
            return False
        
        print(f"Creating {agent_type} agent: {agent_name}")
        print(f"Destination: {dest_path}")
        
        # Copy template files
        self._copy_template(template_path, dest_path, agent_name, agent_description)
        
        # Create additional files
        self._create_init_file(dest_path)
        self._create_deployment_files(agent_name)
        self._create_test_files(agent_name)
        
        # Update A2A manifest if enabled
        if self.config["features"].get("enable_a2a", False):
            self._update_a2a_manifest(agent_name)
        
        print(f"\n✓ Agent {agent_name} created successfully!")
        print(f"\nNext steps:")
        print(f"1. cd src/{self.config['project']['namespace']}/agents/{agent_name}")
        print(f"2. Review and customize agent.py and prompt.py")
        print(f"3. Add any custom tools in tools.py")
        print(f"4. Run: adk run {agent_name}")
        
        return True
    
    def _copy_template(self, template_path, dest_path, agent_name, agent_description):
        """Copy and process template files."""
        dest_path.mkdir(parents=True, exist_ok=True)
        
        for item in template_path.iterdir():
            if item.is_file():
                # Read template file
                content = item.read_text()
                
                # Process template variables
                content = self.process_template(content, agent_name, agent_description)
                
                # Determine destination filename
                dest_name = item.name
                if dest_name.endswith('.template'):
                    dest_name = dest_name[:-9]  # Remove .template suffix
                
                # Write processed file
                dest_file = dest_path / dest_name
                dest_file.write_text(content)
                print(f"  Created: {dest_file}")
            
            elif item.is_dir():
                # Recursively copy directories
                dest_subdir = dest_path / item.name
                self._copy_template(item, dest_subdir, agent_name, agent_description)
    
    def _create_init_file(self, agent_path):
        """Create __init__.py file for the agent package."""
        init_content = f'''# Agent package initialization
# Extracted and configured by Universal ADK Agent Starter Kit

from .agent import root_agent

__all__ = ["root_agent"]
'''
        init_file = agent_path / "__init__.py"
        init_file.write_text(init_content)
        print(f"  Created: {init_file}")
    
    def _create_deployment_files(self, agent_name):
        """Create deployment configuration for the agent."""
        deploy_dir = Path(f"deployment/agents/{agent_name}")
        deploy_dir.mkdir(parents=True, exist_ok=True)
        
        # Create deployment configuration
        deploy_config = {
            "agent_name": agent_name,
            "deployment_target": self.config["deployment"]["target"],
            "project_id": self.config["project"]["project_id"],
            "location": self.config["project"]["location"],
            "enable_monitoring": self.config["deployment"]["enable_monitoring"]
        }
        
        deploy_file = deploy_dir / "deploy.yaml"
        with open(deploy_file, 'w') as f:
            yaml.dump(deploy_config, f, default_flow_style=False)
        print(f"  Created: {deploy_file}")
    
    def _create_test_files(self, agent_name):
        """Create test files for the agent."""
        test_dir = Path(f"tests/agents/{agent_name}")
        test_dir.mkdir(parents=True, exist_ok=True)
        
        # Create test file
        test_content = f'''# Test suite for {agent_name} agent
# Generated by Universal ADK Agent Starter Kit

import pytest
from {self.config['project']['namespace']}.agents.{agent_name} import root_agent
from google.adk.runners import InMemoryRunner
from google.genai.types import Part, UserContent

def test_{agent_name}_basic():
    """Test basic functionality of {agent_name} agent."""
    runner = InMemoryRunner(agent=root_agent)
    session = runner.session_service.create_session(
        app_name=runner.app_name,
        user_id="test_user"
    )
    
    # Test with a simple message
    content = UserContent(parts=[Part(text="Hello, test message")])
    events = list(runner.run(
        user_id=session.user_id,
        session_id=session.id,
        new_message=content
    ))
    
    assert len(events) > 0
    assert any(event.content.parts for event in events)

def test_{agent_name}_tools():
    """Test that agent has access to configured tools."""
    assert hasattr(root_agent, 'tools')
    # Add specific tool tests based on agent type
'''
        
        test_file = test_dir / f"test_{agent_name}.py"
        test_file.write_text(test_content)
        print(f"  Created: {test_file}")
        
        # Create evalset file if evaluation is enabled
        if self.config["features"].get("enable_evaluation", True):
            evalset = {
                "eval_name": f"{agent_name}_basic_eval",
                "display_name": f"Basic evaluation for {agent_name}",
                "description": f"Tests basic functionality of {agent_name} agent",
                "test_cases": [
                    {
                        "id": "test_1",
                        "inputs": {"text": "Hello, how can you help me?"},
                        "expected_events": [
                            {
                                "event_type": "agent_response",
                                "has_content": True
                            }
                        ]
                    }
                ]
            }
            
            evalset_file = test_dir / f"{agent_name}_eval.json"
            import json
            with open(evalset_file, 'w') as f:
                json.dump(evalset, f, indent=2)
            print(f"  Created: {evalset_file}")
    
    def _update_a2a_manifest(self, agent_name):
        """Update A2A manifest with new agent."""
        manifest_file = Path("a2a_manifest.yaml")
        
        if manifest_file.exists():
            with open(manifest_file, 'r') as f:
                manifest = yaml.safe_load(f) or {"agents": []}
        else:
            manifest = {"agents": []}
        
        # Add new agent
        manifest["agents"].append({
            "name": agent_name,
            "identity": f"{self.config['project']['namespace']}.{agent_name}",
            "endpoint": f"https://{agent_name}-{self.config['project']['project_id']}.a.run.app",
            "status": "pending_deployment"
        })
        
        with open(manifest_file, 'w') as f:
            yaml.dump(manifest, f, default_flow_style=False)
        print(f"  Updated: {manifest_file}")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Create a new ADK agent from templates"
    )
    parser.add_argument(
        "--type",
        choices=list(AGENT_TYPES.keys()),
        required=True,
        help="Type of agent to create"
    )
    parser.add_argument(
        "--name",
        required=True,
        help="Name of the agent (lowercase with underscores)"
    )
    parser.add_argument(
        "--description",
        default="",
        help="Description of the agent"
    )
    parser.add_argument(
        "--config",
        default="starter-kit.yaml",
        help="Configuration file (default: starter-kit.yaml)"
    )
    
    args = parser.parse_args()
    
    # Create agent
    creator = AgentCreator(args.config)
    success = creator.create_agent(args.type, args.name, args.description)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
