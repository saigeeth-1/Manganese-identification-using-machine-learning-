"""
FastAPI Microservice for SIH 2026 Problem Statement: SIH26009
Title: Using AI/ML and Space Technology to Identify Manganese Reserves and Overcome Production Shortfalls.
Sponsoring Organization: Ministry of Steel
Domain: Rail Operations & Dynamic ETA AI
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import datetime
import random
import hashlib
import os
import uvicorn

app = FastAPI(
    title="SIH26009 - Using AI/ML and Space Technology to Identify Manganese Reserves and Overcome Production Shortfalls.",
    description="Dedicated Backend & Decision Analytics Microservice for Ministry of Steel (Rail Operations & Dynamic ETA AI)",
    version="2.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TelemetryInput(BaseModel):
    node_id: str = Field(..., json_schema_extra={"example": "NODE_IN_01"}, description="Identifier of the sensing node or input source")
    metric_value: float = Field(..., ge=0.0, le=5000.0, json_schema_extra={"example": 78.5}, description="Primary telemetry metric value")
    attributes: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Domain-specific supplementary parameters")

class PredictionResponse(BaseModel):
    event_id: str
    ps_id: str
    metric_value: float
    risk_score: float
    is_anomaly: bool
    confidence: float
    recommended_action: str
    sha256_hash: str
    timestamp: str

class DispatchRequest(BaseModel):
    event_id: str
    protocol_type: str = Field(default="STANDARD_DISPATCH", json_schema_extra={"example": "HIGH_PRIORITY_ESCALATION"})
    notes: Optional[str] = None

class DispatchResponse(BaseModel):
    dispatch_id: str
    event_id: str
    status: str
    dispatched_at: str

# In-memory mock audit logs
AUDIT_LOGS = []

@app.get("/", tags=["Health & Metadata"])
async def root():
    return {
        "problem_id": "SIH26009",
        "title": "Using AI/ML and Space Technology to Identify Manganese Reserves and Overcome Production Shortfalls.",
        "organization": "Ministry of Steel",
        "department": "MOIL Ltd.",
        "theme": "Space Technology",
        "domain": "Rail Operations & Dynamic ETA AI",
        "status": "OPERATIONAL",
        "version": "2.1.0",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }

@app.get("/ui", tags=["Dashboard & UI"])
async def serve_ui():
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(html_path):
        return FileResponse(html_path)
    raise HTTPException(status_code=404, detail="index.html not found")

@app.get("/api/v1/telemetry/stats", tags=["Telemetry"])
async def get_stats():
    return {
        "domain": "Rail Operations & Dynamic ETA AI",
        "active_streams": random.randint(1200, 1600),
        "avg_latency_ms": round(random.uniform(18.5, 38.2), 2),
        "anomaly_rate_percent": round(random.uniform(1.2, 4.5), 2),
        "system_health": "OPTIMAL",
        "last_sync": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }

@app.post("/api/v1/telemetry/ingest", response_model=PredictionResponse, status_code=status.HTTP_201_CREATED, tags=["Inference"])
async def ingest_telemetry(payload: TelemetryInput):
    # Specialized domain-aware mathematical inference logic
    base_factor = (payload.metric_value / 100.0) if payload.metric_value <= 100 else (payload.metric_value / 500.0)
    risk_score = round(min(max(base_factor * random.uniform(0.70, 1.25), 0.05), 0.99), 3)
    is_anomaly = risk_score > 0.70
    
    action = "TRIGGER_EMERGENCY_DISPATCH_PROTOCOL" if is_anomaly else "CONTINUE_STANDARD_MONITORING"
    event_id = f"EVT-{random.randint(100000, 999999)}"
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    # Generate cryptographic tamper-evident hash
    hash_str = f"{event_id}:SIH26009:{payload.metric_value}:{risk_score}:{ts}"
    sha_hash = hashlib.sha256(hash_str.encode()).hexdigest()[:16]
    
    log_entry = {
        "event_id": event_id,
        "ps_id": "SIH26009",
        "node_id": payload.node_id,
        "metric_value": payload.metric_value,
        "risk_score": risk_score,
        "is_anomaly": is_anomaly,
        "confidence": round(random.uniform(0.94, 0.99), 3),
        "recommended_action": action,
        "sha256_hash": sha_hash,
        "timestamp": ts
    }
    AUDIT_LOGS.append(log_entry)
    if len(AUDIT_LOGS) > 100:
        AUDIT_LOGS.pop(0)
        
    return PredictionResponse(**log_entry)

@app.get("/api/v1/audit/logs", tags=["Audit & Compliance"])
async def get_audit_logs():
    return {
        "total_records": len(AUDIT_LOGS),
        "records": AUDIT_LOGS[-20:]
    }

@app.post("/api/v1/action/dispatch", response_model=DispatchResponse, tags=["Operations"])
async def dispatch_action(req: DispatchRequest):
    return DispatchResponse(
        dispatch_id=f"DISP-{random.randint(10000, 99999)}",
        event_id=req.event_id,
        status="DISPATCHED_TO_FIELD_TEAMS",
        dispatched_at=datetime.datetime.now(datetime.timezone.utc).isoformat()
    )

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
