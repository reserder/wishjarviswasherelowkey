import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from api.dynamic_config import api as config_router
from api.ui_evolution import router as ui_router
from api.evolution_api import router as evolution_router
from api.voice_gateway import router as voice_router
from api.connectors_hub import router as connectors_router
from workflows.supervisor import app as orbit_app
from fastapi.middleware.cors import CORSMiddleware

api = FastAPI(title="AEGIS OS Backend")

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api.include_router(ui_router)
api.include_router(evolution_router)
api.include_router(voice_router)
api.include_router(connectors_router)
api.mount("/config", config_router)

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
    uvicorn.run(api, host="0.0.0.0", port=8001)
