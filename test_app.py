"""
Automated Pytest Suite for SIH26009 FastAPI Microservice
"""

import os
import sys
import importlib.util
import pytest
from fastapi.testclient import TestClient

app_path = os.path.join(os.path.dirname(__file__), "app.py")
spec = importlib.util.spec_from_file_location("app_sih26009", app_path)
app_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app_module)
app = app_module.app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["problem_id"] == "SIH26009"
    assert data["status"] == "OPERATIONAL"
    assert "timestamp" in data

def test_stats_endpoint():
    response = client.get("/api/v1/telemetry/stats")
    assert response.status_code == 200
    data = response.json()
    assert "active_streams" in data
    assert "avg_latency_ms" in data
    assert data["system_health"] == "OPTIMAL"

def test_telemetry_ingest():
    payload = {
        "node_id": "TEST_NODE_01",
        "metric_value": 85.5,
        "attributes": {"sensor_model": "GEN_IV", "calibration": "OK"}
    }
    response = client.post("/api/v1/telemetry/ingest", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["ps_id"] == "SIH26009"
    assert data["metric_value"] == 85.5
    assert 0.0 <= data["risk_score"] <= 1.0
    assert isinstance(data["is_anomaly"], bool)
    assert "sha256_hash" in data

def test_audit_logs():
    response = client.get("/api/v1/audit/logs")
    assert response.status_code == 200
    data = response.json()
    assert "total_records" in data
    assert isinstance(data["records"], list)

def test_dispatch_action():
    payload = {
        "event_id": "EVT-999888",
        "protocol_type": "URGENT_OPERATIONAL_ESCALATION",
        "notes": "Automated pipeline trigger"
    }
    response = client.post("/api/v1/action/dispatch", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["event_id"] == "EVT-999888"
    assert data["status"] == "DISPATCHED_TO_FIELD_TEAMS"
