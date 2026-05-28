from fastapi import APIRouter, HTTPException
from workflows.evolution import run_evolution_cycle

router = APIRouter(prefix="/evolution", tags=["Evolution"])

@router.post("/trigger")
async def trigger_evolution():
    """Manually triggers the Harvest -> Analyze -> Suggest cycle."""
    try:
        plan = await run_evolution_cycle()
        return plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status")
async def get_evolution_status():
    """Returns the current 'State of the OS' and pending upgrades."""
    return {
        "status": "Ready",
        "last_harvest": "2026-05-28T12:00:00Z",
        "pending_upgrades": ["Self-Healing-Endpoints", "Automated-PR-Reviewer"]
    }
