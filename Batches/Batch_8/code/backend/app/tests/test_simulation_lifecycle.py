import pytest
from starlette.testclient import TestClient
from backend.app.main import app

def test_live_simulation_full_lifecycle():
    client = TestClient(app)

    # 1. Check health
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

    # 2. Reset initial state
    res = client.post("/api/telemetry/reset")
    assert res.status_code == 200
    assert res.json()["status"] == "reset"

    # 3. Check initial metrics
    res = client.get("/api/telemetry/metrics")
    assert res.status_code == 200
    metrics = res.json()
    assert metrics["message_rate"] == 40
    assert metrics["original_bitrate"] == 120
    assert metrics["compressed_bitrate"] > 0
    assert metrics["percentage_savings"] > 0

    # 4. Check initial simulation status
    res = client.get("/api/telemetry/status")
    assert res.status_code == 200
    st = res.json()
    assert st["is_running"] is False
    assert st["messages_transmitted"] == 0

    # 5. Start simulation
    res = client.post("/api/telemetry/start")
    assert res.status_code == 200
    assert res.json()["status"] == "started"

    # 6. Verify status shows running
    res = client.get("/api/telemetry/status")
    st = res.json()
    assert st["is_running"] is True
    assert st["is_paused"] is False

    # 7. Pause simulation
    res = client.post("/api/telemetry/pause")
    assert res.status_code == 200
    assert res.json()["status"] == "paused"
    res = client.get("/api/telemetry/status")
    assert res.json()["is_paused"] is True

    # 8. Resume simulation
    res = client.post("/api/telemetry/resume")
    assert res.status_code == 200
    assert res.json()["status"] == "resumed"
    res = client.get("/api/telemetry/status")
    assert res.json()["is_paused"] is False

    # 9. Configure telemetry (message rate, seed)
    res = client.post("/api/telemetry/configure", json={"message_rate": 60, "random_seed": 999})
    assert res.status_code == 200
    conf = res.json()
    assert conf["message_rate"] == 60
    assert conf["original_bitrate"] == 180

    # 10. Test one-hour projection
    res = client.get("/api/telemetry/one-hour")
    assert res.status_code == 200
    hour = res.json()
    assert hour["duration_hours"] == 1
    assert hour["total_messages"] == 216000  # 60 msgs/s * 3600
    assert hour["package_merge_bits_saved"] > 0
    assert hour["package_merge_bytes"] > 0

    # 11. WebSocket connection and message interchange
    with client.websocket_connect("/ws/telemetry") as websocket:
        websocket.send_text("PING")
        data = websocket.receive_text()
        assert data == "PONG"

    # 12. Reset simulation and config back to default 40 msgs/s
    res = client.post("/api/telemetry/reset")
    assert res.status_code == 200
    res = client.post("/api/telemetry/configure", json={"message_rate": 40, "random_seed": None})
    assert res.status_code == 200
    res = client.get("/api/telemetry/status")
    assert res.json()["is_running"] is False
    assert res.json()["messages_transmitted"] == 0

if __name__ == "__main__":
    test_live_simulation_full_lifecycle()
    print("ALL SIMULATION TESTS PASSED PERFECTLY!")
