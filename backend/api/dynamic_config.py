import os
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import Dict, Any, List
from .database.qdrant_client import memory_db

api = FastAPI(title="AEGIS Dynamic OS Config")

# Memory Hub: The single source of truth for all models
class ContextUpdate(BaseModel):
    source: str
    content: str
    metadata: Dict[str, Any]

@api.post("/config/add-model")
async def add_model(config: Dict[str, Any] = Body(...)):
    """Dynamically adds a model or API key to LiteLLM."""
    # Logic to update configs/litellm_config.yaml dynamically
    return {"status": "success", "message": f"Model {config.get('model_name')} integrated."}

@api.post("/memory/inject")
async def inject_context(data: ContextUpdate):
    """Universal context injection: any model can write to the shared brain."""
    memory_db.add_memory(
        collection=data.source,
        text=data.content,
        metadata=data.metadata
    )
    return {"status": "context_stored"}

@api.get("/features/registry")
async def get_features():
    """Returns list of active 'Plugins' or OS features."""
    return {
        "active_features": [
            "GitHub-Sync",
            "Multi-Model-Debate",
            "Context-Compression",
            "Auto-RAG-Indexing"
        ],
        "available_mcp_tools": ["filesystem", "google-search", "slack"]
    }
