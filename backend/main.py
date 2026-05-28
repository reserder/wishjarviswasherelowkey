import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from workflows.supervisor import app as orbit_app

api = FastAPI(title="AEGIS OS Backend")

class GoalRequest(BaseModel):
    goal: str

@api.get("/health")
def health():
    return {"status": "online", "system": "AEGIS OS"}

@api.post("/orbit/execute")
async def execute_goal(request: GoalRequest):
    try:
        inputs = {"messages": [HumanMessage(content=request.goal)]}
        result = await orbit_app.ainvoke(inputs)
        return {
            "agent": result.get("next_agent"),
            "response": result.get("final_response"),
            "approval_required": result.get("approval_required"),
            "instructions": result.get("instructions")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(api, host="0.0.0.0", port=8000)
