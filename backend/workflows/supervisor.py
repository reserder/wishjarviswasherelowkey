import os
from typing import TypedDict, List, Annotated, Sequence
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv

load_dotenv()

# Configuration
LITELLM_URL = os.getenv("LITELLM_BASE_URL", "http://localhost:4000/v1")
LITELLM_KEY = os.getenv("LITELLM_API_KEY", "sk-aegis-local")

# LLM Clients
primary_llm = ChatOpenAI(
    model="gemma-primary",
    openai_api_base=LITELLM_URL,
    openai_api_key=LITELLM_KEY
)

reasoning_llm = ChatOpenAI(
    model="deepseek-reasoner",
    openai_api_base=LITELLM_URL,
    openai_api_key=LITELLM_KEY
)

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], lambda x, y: x + y]
    next_agent: str
    instructions: str
    approval_required: bool
    final_response: str

def orbit_supervisor(state: AgentState):
    """Orbit: The Executive OS Shell. Routes to specialists."""
    prompt = """You are Orbit, the Executive AI Operating System Supervisor.
Your job is to route the user's request to the correct specialist.

Available Specialists:
- Mercury: Research, web analysis, deep document synthesis.
- Atlas: Business operations, Amora Healthcare OS, SOPs, finance.
- Forge: Coding, architecture, GitHub, infrastructure.
- Echo: Memory retrieval, second brain management.
- Muse: Music, branding, artist persona.
- Operator: Automation, scheduling, workflows.

Instructions:
1. Identify the best specialist.
2. Provide specific instructions for that specialist.
3. Determine if the action requires human approval (Sentinel gate).

Reply in format:
AGENT: <agent_name>
INSTRUCTIONS: <instructions>
APPROVAL: <true/false>
"""
    last_message = state["messages"][-1].content
    response = primary_llm.invoke([HumanMessage(content=prompt + f"\nUser: {last_message}")])
    
    # Simple parsing
    lines = response.content.split("\n")
    agent = "mercury"
    instr = ""
    appr = False
    
    for line in lines:
        if line.startswith("AGENT:"): agent = line.replace("AGENT:", "").strip().lower()
        if line.startswith("INSTRUCTIONS:"): instr = line.replace("INSTRUCTIONS:", "").strip()
        if line.startswith("APPROVAL:"): appr = "true" in line.lower()
        
    return {
        "next_agent": agent,
        "instructions": instr,
        "approval_required": appr
    }

def specialist_node(state: AgentState):
    """Executes the specialist agent logic."""
    agent = state["next_agent"]
    instructions = state["instructions"]
    
    # Route to deepseek for Forge or Mercury
    llm = reasoning_llm if agent in ["forge", "mercury"] else primary_llm
    
    prompt = f"You are {agent.capitalize()}, an elite specialist. Task: {instructions}"
    response = llm.invoke([HumanMessage(content=prompt)])
    
    return {"final_response": response.content}

def sentinel_gate(state: AgentState):
    """Sentinel: Security & Approval Gate."""
    if state.get("approval_required"):
        return "approval_needed"
    return "complete"

# Graph Construction
workflow = StateGraph(AgentState)
workflow.add_node("orbit", orbit_supervisor)
workflow.add_node("specialist", specialist_node)

workflow.set_entry_point("orbit")
workflow.add_edge("orbit", "specialist")
workflow.add_conditional_edges("specialist", sentinel_gate, {
    "approval_needed": END, # In a real app, this would go to an approval node
    "complete": END
})

app = workflow.compile()

if __name__ == "__main__":
    inputs = {"messages": [HumanMessage(content="Help me analyze the latest competitors for Amora Healthcare.")]}
    for output in app.stream(inputs):
        print(output)
