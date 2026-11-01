from fastapi import APIRouter
from typing import Dict, Any
from ..schemas.telemetry import TelemetryConfig, NetworkMetrics, SimulationStatus
from ..services.telemetry_service import telemetry_service

router = APIRouter(prefix="/api/telemetry", tags=["Live Telemetry & Network"])

@router.get("/metrics", response_model=NetworkMetrics)
def get_network_metrics():
    """
    Returns theoretical network capacity, bitrates, link utilization,
    and bandwidth savings based on active parameters or live rolling window.
    """
    if telemetry_service.is_running and telemetry_service.messages_transmitted > 0:
        return telemetry_service.get_dynamic_metrics()
    return telemetry_service.get_theoretical_metrics()

@router.get("/status", response_model=SimulationStatus)
def get_simulation_status():
    """
    Returns current live simulation state, transmitted message counts, and cumulative savings.
    """
    return telemetry_service.get_status()

@router.post("/configure", response_model=NetworkMetrics)
def configure_telemetry(config: TelemetryConfig):
    """
    Updates operational network parameters (aggregate message rate, channel capacity, population).
    """
    return telemetry_service.configure(config)

@router.post("/start")
async def start_simulation():
    telemetry_service.start_simulation()
    return {"status": "started", "simulation": telemetry_service.get_status()}

@router.post("/pause")
async def pause_simulation():
    telemetry_service.pause_simulation()
    return {"status": "paused", "simulation": telemetry_service.get_status()}

@router.post("/resume")
async def resume_simulation():
    telemetry_service.resume_simulation()
    return {"status": "resumed", "simulation": telemetry_service.get_status()}

@router.post("/reset")
async def reset_simulation():
    telemetry_service.reset_simulation()
    return {"status": "reset", "simulation": telemetry_service.get_status()}

@router.get("/one-hour")
def get_one_hour_projection():
    """
    Calculates exact mathematical projection of transmitting telemetry for 1 full hour
    (144,000 messages) across original, Huffman, and Package-Merge.
    """
    return telemetry_service.simulate_one_hour()

