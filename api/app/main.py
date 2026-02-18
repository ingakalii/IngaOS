from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import os
from .router import IntentRouter
from .orchestrator import Orchestrator
from .infra.qdrant_client import QdrantClient
from .middleware.audit import AuditMiddleware
from .auth import get_current_user, require_role

app = FastAPI(title="Cognitive Enterprise Engine - Demo")

app.add_middleware(AuditMiddleware)

# Init components (singletons for demo)
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
router = IntentRouter()
orchestrator = Orchestrator()
qdrant = QdrantClient(QDRANT_URL)

class Query(BaseModel):
    user_id: str
    text: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/route")
def route(query: Query, user=Depends(get_current_user)):
    mode = router.classify(query.text)
    job = orchestrator.run(mode, query.dict())
    return {"mode": mode, "job_id": job}

@app.post("/api/strategic/market")
def strategic_market(query: Query, user=Depends(require_role(["admin", "analyst"]))):
    # direct call for demo: run synchronously
    from .agents.strategic.market_analyst import MarketAnalyst
    agent = MarketAnalyst(qdrant)
    result = agent.analyze(query.user_id, query.text)
    return {"result": result}

@app.post("/api/research/evaluate")
def research_evaluate(query: Query, user=Depends(require_role(["admin", "analyst", "auditor"]))):
    from .agents.research.evaluation_agent import EvaluationAgent
    agent = EvaluationAgent(qdrant)
    result = agent.evaluate_output(query.text, evidence=[])
    return {"result": result}

@app.post("/api/simulation/run")
def simulation_run(body: dict, user=Depends(require_role(["admin", "analyst"]))):
    # body expects: model, inputs, trials
    from .agents.simulation.simulation_engine import SimulationEngine
    engine = SimulationEngine()
    # for simplicity call orchestrator to process (synchronous)
    return engine.run_monte_carlo(lambda s: s.get("price",0)*s.get("users",0)*s.get("conv",0), body.get("inputs", {}), trials=body.get("trials", 200))

@app.post("/api/governance/check")
def governance_check(body: dict, user=Depends(require_role(["admin"]))):
    from .agents.governance.governance_agent import GovernanceAgent
    agent = GovernanceAgent()
    return agent.check(body.get("meta", {}))
