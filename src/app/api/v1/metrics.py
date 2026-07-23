# src/app/api/metrics.py
from fastapi import APIRouter
from src.app.services.stats_service import stats_service

router = APIRouter(prefix="/api", tags=["Metrics & Health"])


@router.get("/health")
async def health_check():
    return {"status": "ok", "service": "Developer CV AI API"}


@router.get("/metrics")
async def get_metrics():
    stats = stats_service.get_stats()
    return {"status": "success", "data": stats}