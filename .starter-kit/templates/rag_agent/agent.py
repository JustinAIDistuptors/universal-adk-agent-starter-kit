# Extracted from google/adk-samples/python/agents/RAG/
# Part of the Universal ADK Agent Starter Kit
# Original source: https://github.com/google/adk-samples/python/agents/RAG/

"""RAG Agent - Retrieval-Augmented Generation agent with Vertex AI."""

from google.adk.agents import LlmAgent
from google.adk.tools import ToolRegistry
from .shared_libraries import corpus_manager
from .prompts import RAG_AGENT_PROMPT

# Import the Vertex AI RAG retrieval tool
from google.adk.tools import vertex_ai_rag_retrieval

# Configure the RAG tool with your corpus
rag_tool = vertex_ai_rag_retrieval.VertexAiRagRetrieval(
    rag_corpus="{{rag_corpus_id}}",  # Set in .env file
    similarity_top_k=5,
    vector_distance_threshold=0.7
)

# Define the RAG agent
root_agent = LlmAgent(
    name="{{agent_name}}",
    model="{{model_name|default:gemini-2.0-flash}}",
    system_instruction=RAG_AGENT_PROMPT,
    tools=[rag_tool],
    generation_config={
        "temperature": 0.1,  # Lower temperature for more factual responses
        "max_output_tokens": 2048,
        "top_p": 0.95,
        "top_k": 40
    }
)
