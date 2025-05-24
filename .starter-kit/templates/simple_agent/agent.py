# Extracted from google/adk-samples/python/agents/llm-auditor/
# Part of the Universal ADK Agent Starter Kit
# Original source: https://github.com/google/adk-samples/python/agents/llm-auditor/

# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""{{agent_description}}"""

from google.adk.agents import SequentialAgent

from .sub_agents.critic import critic_agent
from .sub_agents.reviser import reviser_agent


{{agent_name}} = SequentialAgent(
    name='{{agent_name}}',
    description=(
        '{{agent_long_description|default:Evaluates LLM-generated answers, verifies actual accuracy using the'
        ' web, and refines the response to ensure alignment with real-world'
        ' knowledge.}}'
    ),
    sub_agents=[critic_agent, reviser_agent],
)

root_agent = {{agent_name}}
