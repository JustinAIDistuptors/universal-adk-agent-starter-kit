# Deployment Directory

This directory will contain infrastructure and deployment code extracted from official repositories.

## Planned Structure (To Be Extracted):

### `/terraform/`
- **Source**: `GoogleCloudPlatform/agent-starter-pack/deployment/terraform/`
- Will contain Terraform modules for:
  - Cloud Run deployment
  - Agent Engine deployment
  - VPC and networking
  - IAM and security
  - Budget controls

### `/ci/`
- **Source**: `GoogleCloudPlatform/agent-starter-pack/deployment/ci/`
- Will contain CI/CD pipelines:
  - Cloud Build configurations
  - GitHub Actions workflows
  - Testing pipelines
  - Deployment automation

### `/environments/`
- Configuration for different environments:
  - `dev.tfvars`
  - `staging.tfvars`
  - `prod.tfvars`

## Key Features to Extract:

1. **Multi-environment support** - Dev, staging, prod
2. **Choice of deployment** - Cloud Run or Agent Engine
3. **Budget controls** - Cost management
4. **Monitoring** - Cloud Trace, Cloud Logging
5. **Security** - VPC-SC, IAM, Workload Identity

## Current Status: AWAITING EXTRACTION

No code has been added yet. All infrastructure code must be extracted from the official agent-starter-pack repository.
