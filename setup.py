#!/usr/bin/env python3
"""
Universal ADK Agent Starter Kit - Setup Script

This script sets up the Universal ADK Agent Starter Kit by:
1. Cloning required repositories
2. Running the extraction process
3. Setting up the development environment
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import yaml

REQUIRED_REPOS = [
    {
        "name": "adk-samples",
        "url": "https://github.com/google/adk-samples.git",
        "org": "google"
    },
    {
        "name": "agent-starter-pack", 
        "url": "https://github.com/GoogleCloudPlatform/agent-starter-pack.git",
        "org": "GoogleCloudPlatform"
    },
    {
        "name": "adk-python",
        "url": "https://github.com/google/adk-python.git",
        "org": "google"
    },
    {
        "name": "A2A",
        "url": "https://github.com/google/A2A.git",
        "org": "google"
    },
    {
        "name": "generative-ai",
        "url": "https://github.com/GoogleCloudPlatform/generative-ai.git",
        "org": "GoogleCloudPlatform"
    }
]

def run_command(cmd, cwd=None):
    """Run a shell command and return success status."""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    return True

def check_prerequisites():
    """Check if required tools are installed."""
    print("Checking prerequisites...")
    
    # Check Python version
    if sys.version_info < (3, 9):
        print("ERROR: Python 3.9+ is required")
        return False
    print("✓ Python version:", sys.version)
    
    # Check git
    if not shutil.which("git"):
        print("ERROR: git is not installed")
        return False
    print("✓ git is installed")
    
    # Check if ADK is installed
    try:
        import google.adk
        print("✓ Google ADK is installed")
    except ImportError:
        print("⚠ Google ADK not installed. Will install during setup.")
    
    return True

def clone_repositories():
    """Clone all required repositories."""
    print("\n" + "="*60)
    print("Cloning source repositories...")
    print("="*60)
    
    parent_dir = Path("..").absolute()
    all_cloned = True
    
    for repo in REQUIRED_REPOS:
        repo_path = parent_dir / repo["name"]
        if repo_path.exists():
            print(f"✓ {repo['name']} already exists")
        else:
            print(f"\nCloning {repo['name']}...")
            if run_command(f"git clone {repo['url']}", cwd=str(parent_dir)):
                print(f"✓ Cloned {repo['name']}")
            else:
                print(f"✗ Failed to clone {repo['name']}")
                all_cloned = False
    
    return all_cloned

def setup_python_environment():
    """Set up Python virtual environment and install dependencies."""
    print("\n" + "="*60)
    print("Setting up Python environment...")
    print("="*60)
    
    # Create virtual environment if it doesn't exist
    venv_path = Path("venv")
    if not venv_path.exists():
        print("Creating virtual environment...")
        if not run_command(f"{sys.executable} -m venv venv"):
            return False
        print("✓ Virtual environment created")
    
    # Determine pip path based on OS
    if sys.platform == "win32":
        pip_path = "venv\\Scripts\\pip"
        activation_cmd = "venv\\Scripts\\activate.bat"
    else:
        pip_path = "venv/bin/pip"
        activation_cmd = "source venv/bin/activate"
    
    print(f"\nTo activate the virtual environment, run:")
    print(f"  {activation_cmd}")
    
    # Install dependencies
    print("\nInstalling dependencies...")
    dependencies = [
        "google-adk>=1.0.0",
        "pyyaml",
        "agent-starter-pack",
        "a2a-sdk",
    ]
    
    for dep in dependencies:
        print(f"Installing {dep}...")
        if not run_command(f"{pip_path} install {dep}"):
            print(f"⚠ Failed to install {dep}")
    
    return True

def run_extraction():
    """Run the extraction script."""
    print("\n" + "="*60)
    print("Running extraction process...")
    print("="*60)
    
    if not Path("extract.py").exists():
        print("ERROR: extract.py not found")
        return False
    
    # Run extraction script
    if sys.platform == "win32":
        python_cmd = "venv\\Scripts\\python"
    else:
        python_cmd = "venv/bin/python"
    
    return run_command(f"{python_cmd} extract.py")

def create_example_config():
    """Create an example configuration if starter-kit.yaml doesn't exist."""
    config_file = Path("starter-kit.yaml")
    if config_file.exists():
        print("✓ starter-kit.yaml already exists")
        return True
    
    print("Creating example configuration...")
    
    config = {
        "project": {
            "project_id": "my-gcp-project",
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
            "target": "cloud_run",
            "enable_ci": True,
            "enable_monitoring": True
        },
        "features": {
            "enable_rag": False,
            "enable_a2a": False,
            "enable_evaluation": True
        }
    }
    
    with open(config_file, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)
    
    print("✓ Created starter-kit.yaml")
    print("\n⚠ IMPORTANT: Edit starter-kit.yaml with your actual project settings")
    
    return True

def create_example_agents():
    """Create example agents to demonstrate the system."""
    print("\n" + "="*60)
    print("Creating example agents...")
    print("="*60)
    
    # Check if templates exist
    if not Path(".starter-kit/templates/simple_agent").exists():
        print("⚠ Templates not found. Skipping example creation.")
        print("  Run the extraction process first.")
        return
    
    print("\nTo create your first agent, run:")
    print("  python create_agent.py --type simple --name my_first_agent")
    print("\nAvailable agent types:")
    print("  - simple: Basic single agent with tools")
    print("  - multi: Multi-agent system with sub-agents")
    print("  - rag: RAG-enabled agent with vector search")
    print("  - tool: Agent with custom tools")

def main():
    """Main setup process."""
    print("Universal ADK Agent Starter Kit - Setup")
    print("="*60)
    
    # Check prerequisites
    if not check_prerequisites():
        print("\nPlease install missing prerequisites and try again.")
        sys.exit(1)
    
    # Clone repositories
    if not clone_repositories():
        print("\nRepository cloning failed. Please check your internet connection.")
        sys.exit(1)
    
    # Set up Python environment
    if not setup_python_environment():
        print("\nPython environment setup failed.")
        sys.exit(1)
    
    # Run extraction
    if run_extraction():
        print("\n✓ Extraction completed successfully!")
    else:
        print("\n⚠ Extraction failed. You may need to run it manually:")
        print("  python extract.py")
    
    # Create example configuration
    create_example_config()
    
    # Show next steps
    print("\n" + "="*60)
    print("Setup Complete!")
    print("="*60)
    print("\nNext steps:")
    print("1. Edit starter-kit.yaml with your GCP project settings")
    print("2. Activate the virtual environment:")
    if sys.platform == "win32":
        print("   venv\\Scripts\\activate.bat")
    else:
        print("   source venv/bin/activate")
    print("3. Create your first agent:")
    print("   python create_agent.py --type simple --name my_first_agent")
    print("4. Run your agent:")
    print("   cd src/[namespace]/agents/my_first_agent")
    print("   adk run my_first_agent")
    print("\nFor more information, see README.md")

if __name__ == "__main__":
    main()
