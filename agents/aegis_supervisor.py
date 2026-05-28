import os, sys
from typing import TypedDict, List
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.expanduser("~/aegis-ai-os/.env"))

from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama

llm = ChatOllama(model="qwen2.5:7b", base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"))

AGENTS = {
    "atlas":   "Amora Healthcare OS. RCM, billing, coding, denials, revenue, SOPs, hiring.",
    "mercury": "Research OS. Web research, citations, synthesis, competitor analysis, domain intelligence.",
    "velvet":  "Music and Brand OS. Amogh artist persona, lyrics, rollout strategy, content, visuals.",
    "pulse":   "Health and Wellness OS. Routines, habits, sleep, fitness, nutrition reminders.",
    "orbit":   "Executive OS. Calendar, inbox triage, priorities, daily briefing, meeting prep.",
    "wingman": "Social OS. Message drafts, dating context, follow-up reminders. HUMAN APPROVAL REQUIRED.",
    "forge":   "Infrastructure OS. Memory curation, RAG ingestion, workflow ops, routing monitor.",
    "scholar": "Learning OS. Academic notes, course summaries, study plans, concept explanations.",
}

class AegisState(TypedDict):
    goal: str
    assigned_agent: str
    response: str
    confidence: float
    needs_approval: bool
    history: List[str]

def supervisor_node(state: AegisState) -> AegisState:
    goal = state["goal"]
    descs = "\n".join([f"- {k}: {v}" for k, v in AGENTS.items()])
    prompt = f"""You are Aegis, the supreme AI operating system supervisor.
Agents available:
{descs}

User goal: {goal}

Pick ONE agent. Reply with ONLY the agent name in lowercase. No explanation."""
    r = llm.invoke(prompt)
    assigned = r.content.strip().lower().split()[0]
    if assigned not in AGENTS:
        assigned = "mercury"
    return {**state, "assigned_agent": assigned, "needs_approval": assigned == "wingman",
            "history": state.get("history", []) + [f"Aegis -> {assigned}"]}

def agent_node(state: AegisState) -> AegisState:
    agent = state["assigned_agent"]
    persona = AGENTS.get(agent, "General expert assistant")
    prompt = f"""You are {agent.capitalize()}, an elite specialist AI.
Role: {persona}
Task: {state['goal']}

Be specific, actionable, and expert-level. Use bullet points where helpful.
If you lack enough info to answer confidently, say LOW_CONFIDENCE at the start."""
    r = llm.invoke(prompt)
    content = r.content
    conf = 0.45 if content.startswith("LOW_CONFIDENCE") else 0.92
    return {**state, "response": content, "confidence": conf,
            "history": state.get("history", []) + [f"{agent} -> done"]}

def gate(state: AegisState) -> str:
    if state.get("needs_approval"): return "needs_approval"
    if state.get("confidence", 1.0) < 0.6: return "low_confidence"
    return "complete"

def approval_node(state: AegisState) -> AegisState:
    return {**state, "response": f"\n⚠️  APPROVAL REQUIRED BEFORE SENDING\nAgent: {state['assigned_agent'].upper()}\n\nDraft response:\n{state['response']}\n\nType 'yes send it' to confirm."}

def low_conf_node(state: AegisState) -> AegisState:
    return {**state, "response": f"\n⚠️  LOW CONFIDENCE — I need more context.\nHere is what I found so far:\n{state['response']}\n\nShall I do a deeper research pass?"}

g = StateGraph(AegisState)
g.add_node("supervisor", supervisor_node)
g.add_node("agent", agent_node)
g.add_node("approval", approval_node)
g.add_node("low_confidence", low_conf_node)
g.set_entry_point("supervisor")
g.add_edge("supervisor", "agent")
g.add_conditional_edges("agent", gate, {"needs_approval": "approval", "low_confidence": "low_confidence", "complete": END})
g.add_edge("approval", END)
g.add_edge("low_confidence", END)
aegis = g.compile()

def run(goal: str):
    print(f"\n🧠 AEGIS AI OS")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"Goal: {goal}\n")
    result = aegis.invoke({"goal": goal, "assigned_agent": "", "response": "", "confidence": 1.0, "needs_approval": False, "history": []})
    print(f"Agent Assigned : {result['assigned_agent'].upper()}")
    print(f"Flow           : {' → '.join(result['history'])}")
    print(f"Confidence     : {result['confidence']}")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"\n{result['response']}\n")
    return result

if __name__ == "__main__":
    goal = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Give me my morning briefing for Amora Healthcare and Amogh music"
    run(goal)
