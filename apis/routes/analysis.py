# api/routes/analysis.py

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any

from business.services.analysis_service import AnalysisService
from business.models.graph import City
from data.file_repository import FileRepository


router = APIRouter(prefix="/analysis", tags=["Analysis"])


# =========================
# Repository
# =========================
repo = FileRepository()


# =========================
# Load City (from file system)
# =========================
def get_city():
    data = repo.load_project("city_1")  # أو dynamic later
    return City.from_dict(data)


# =========================
# Service Dependency
# =========================
def get_analysis_service(city: City = Depends(get_city)):
    return AnalysisService(city)


# =========================
# Full City Analysis
# =========================
@router.get("/city")
async def city_analysis(
    analysis_service: AnalysisService = Depends(get_analysis_service)
):
    try:
        return await analysis_service.analyze_full_city()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# Simple Stats
# =========================
@router.get("/simple")
async def simple_analysis(
    analysis_service: AnalysisService = Depends(get_analysis_service)
):
    try:
        return await analysis_service.get_simple_stats()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))