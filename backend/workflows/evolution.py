import os
from typing import TypedDict, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from .supervisor import primary_llm

class EvolutionState(TypedDict):
    current_features: List[str]
    system_health: str
    suggested_upgrades: List[str]
    rationale: str

def evolver_agent(state: EvolutionState):
    """The Evolver: Analyzes AEGIS and suggests self-improvement features."""
    prompt = """You are the AEGIS Evolver. Your sole purpose is to make AEGIS the most powerful AI OS in existence.
    Analyze the current active features and suggest 3 'Black Mirror' level upgrades.
    
    Look for:
    - Recursive self-improvement (Can the AI write its own agents?)
    - Advanced UI/UX (Can we use Open Design patterns?)
    - Zero-latency memory mapping.
    - Autonomous GitHub harvesting (Pulling in top-tier open source tools).
    
    Current Features: {features}
    
    Reply with a technical blueprint for the next evolution.
    """
    response = primary_llm.invoke([
        SystemMessage(content=prompt.format(features=state['current_features'])),
        HumanMessage(content="What is the next step to becoming extremely powerful?")
    ])
    
    # In a real implementation, this would trigger a Forge PR to the codebase
    return {"suggested_upgrades": [response.content]}

from agents.specialists.forge_git import forge_git

async def run_evolution_cycle():
    """Autonomous Loop: Harvest -> Analyze -> Suggest."""
    # 1. Harvest trending AI patterns and Open Design systems
    external_intelligence = forge_git.harvest_trending_tools(query="topic:ai-os OR topic:mcp-server")
    
    # 2. Analyze via Evolver Agent
    evolution_state = {
        "current_features": ["Context-Compression", "Multi-Model-Debate"],
        "external_intelligence": external_intelligence
    }
    
    prompt = """You are the AEGIS Evolver.
    Below is a list of the most advanced AI OS repositories on GitHub right now:
    {intel}
    
    Analyze these and suggest 1 concrete feature we can 'harvest' and implement into AEGIS to make it superior.
    """
    response = primary_llm.invoke([
        SystemMessage(content=prompt.format(intel=external_intelligence)),
        HumanMessage(content="Evolve our system.")
    ])
    
    return {
        "discovery_log": external_intelligence,
        "evolution_plan": response.content
    }
