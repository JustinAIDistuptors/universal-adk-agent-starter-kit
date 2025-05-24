# Extracted from google/adk-samples patterns
# Part of the Universal ADK Agent Starter Kit
# Template for creating custom tools

"""Custom tools for {{agent_name}} agent."""

from typing import Dict, Any, List
from google.adk.tools import FunctionTool
from pydantic import BaseModel, Field


class ProjectDetails(BaseModel):
    """Schema for project details."""
    project_type: str = Field(description="Type of project")
    description: str = Field(description="Detailed project description")
    budget_range: str = Field(description="Budget range for the project")
    timeline: str = Field(description="Expected timeline")


def get_example_data(query: str) -> Dict[str, Any]:
    """
    Example tool function that retrieves data.
    
    Args:
        query: Search query string
        
    Returns:
        Dictionary with example data
    """
    # This is a template - replace with actual implementation
    return {
        "status": "success",
        "data": f"Example data for query: {query}",
        "timestamp": "2025-05-24"
    }


def process_project_details(details: ProjectDetails) -> Dict[str, Any]:
    """
    Process project details and return structured data.
    
    Args:
        details: Project details using Pydantic model
        
    Returns:
        Processed project information
    """
    return {
        "project_id": "proj_" + str(hash(details.description))[:8],
        "type": details.project_type,
        "estimated_cost": "Based on " + details.budget_range,
        "duration": details.timeline,
        "status": "pending_review"
    }


def calculate_estimate(
    square_feet: int,
    project_type: str = "renovation"
) -> Dict[str, float]:
    """
    Calculate cost estimate for a project.
    
    Args:
        square_feet: Size of the area in square feet
        project_type: Type of project (renovation, new_build, etc.)
        
    Returns:
        Cost breakdown dictionary
    """
    base_rate = {
        "renovation": 150,
        "new_build": 200,
        "remodel": 175
    }.get(project_type, 150)
    
    subtotal = square_feet * base_rate
    tax = subtotal * 0.08
    total = subtotal + tax
    
    return {
        "subtotal": subtotal,
        "tax": tax,
        "total": total,
        "per_sqft": base_rate
    }


# Create FunctionTool instances
get_data_tool = FunctionTool(
    function=get_example_data,
    name="get_data",
    description="Retrieves relevant data based on query"
)

process_details_tool = FunctionTool(
    function=process_project_details,
    name="process_project",
    description="Process and structure project details"
)

estimate_tool = FunctionTool(
    function=calculate_estimate,
    name="calculate_estimate",
    description="Calculate cost estimates for projects"
)

# Export all tools
all_tools = [
    get_data_tool,
    process_details_tool,
    estimate_tool
]
