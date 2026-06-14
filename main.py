from __future__ import annotations

from fastapi import FastAPI

from ciel_agent.engine import CielTutorAgent
from ciel_agent.schemas import (
    AVAILABLE_ANIMATIONS,
    AVAILABLE_MODES,
    AttemptContext,
    CielDecisionResponse,
    CielStatusResponse,
)


app = FastAPI(
    title="ReaDirect Ciel Intelligent Tutor Agent",
    version=CielTutorAgent.version,
)
engine = CielTutorAgent()


@app.get("/health")
def health() -> dict:
    return {
        "status": "healthy",
        "service": "readirect-ia",
        "agent": "ciel",
        "engine_loaded": True,
        "deterministic": True,
        "llm_enabled": False,
        "version": engine.version,
    }


@app.get("/ia/ciel/status", response_model=CielStatusResponse)
def ciel_status() -> CielStatusResponse:
    return CielStatusResponse(
        service="readirect-ia",
        engine_loaded=True,
        available_modes=AVAILABLE_MODES,
        available_animations=AVAILABLE_ANIMATIONS,
        memory_backend=engine.memory.backend_name,
        version=engine.version,
        status="healthy",
    )


@app.post("/ia/ciel/decide", response_model=CielDecisionResponse)
def ciel_decide(context: AttemptContext) -> CielDecisionResponse:
    return CielDecisionResponse(ciel_agent=engine.decide(context))
