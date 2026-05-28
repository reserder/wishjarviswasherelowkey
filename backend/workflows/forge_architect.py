import os
from langchain_core.messages import SystemMessage, HumanMessage
from .supervisor import reasoner

class ForgeArchitect:
    """Advanced capability allowing AEGIS to write its own agents."""
    
    def generate_agent_code(self, domain: str, purpose: str) -> str:
        prompt = f"""You are the AEGIS Forge Architect.
        Your task is to write a Python script for a new LangGraph specialist agent.
        
        Domain: {domain}
        Purpose: {purpose}
        
        Output MUST be valid Python code representing a function node for LangGraph.
        Include standard imports, LLM invocation, and a well-crafted persona prompt.
        DO NOT include markdown block backticks (```python) in your output, just the raw code.
        """
        
        response = reasoner.invoke([HumanMessage(content=prompt)])
        return response.content

    def spawn_agent(self, domain: str, purpose: str):
        """Generates, saves, and registers a new agent."""
        code = self.generate_agent_code(domain, purpose)
        filename = f"agents/specialists/{domain.lower().replace(' ', '_')}.py"
        
        with open(filename, "w") as f:
            f.write(code)
            
        return {"status": "success", "agent_file": filename, "message": f"Agent for '{domain}' created successfully."}

architect = ForgeArchitect()
