# Extracted from google/adk-samples/python/agents/llm-auditor/
# Part of the Universal ADK Agent Starter Kit
# Original source: https://github.com/google/adk-samples/python/agents/llm-auditor/

"""LLM Auditor Agent - Main agent that coordinates fact-checking."""

from google.adk.agents import LlmAgent
from google.genai import types
from .sub_agents.critic import critic_agent
from .sub_agents.reviser import reviser_agent

# Define the root agent that coordinates the auditing process
root_agent = LlmAgent(
    name="{{agent_name}}",
    model="{{model_name|default:gemini-2.0-flash}}",
    system_instruction="""You are an LLM Auditor. Your role is to verify statements and 
    ensure factual accuracy by coordinating with specialized sub-agents.
    
    For each user input:
    1. First, send it to the Critic agent to fact-check
    2. If the Critic finds issues, send the critique to the Reviser
    3. Return the final verified/revised response
    
    Always prioritize accuracy over everything else.""",
    agents=[critic_agent, reviser_agent],
    enable_auto_transfer=True,
)
