# api/routes/paths.py

from fastapi import APIRouter, HTTPException, Depends

from business.services.path_service import PathService
from business.models.graph import City
from business.models.dto import PathRequest, PathResult
from data.file_repository import FileRepository


router = APIRouter(prefix="/paths", tags=["Path Algorithms"])


# =========================
# Repository
# =========================
repo = FileRepository()


# =========================
# Load City from file
# =========================
def get_city(filename: str = "city_1"):
    """
    هنا بنجيب المدينة من الملفات (.dar)
    """
    data = repo.load_project(filename)
    return City.from_dict(data)  # مهم جدًا لازم تكون موجودة في City


# =========================
# PathService Dependency
# =========================
def get_path_service(city: City = Depends(get_city)):
    return PathService(city)


# =========================
# Shortest Path
# =========================
@router.post("/shortest", response_model=PathResult)
async def shortest_path(
    request: PathRequest,
    path_service: PathService = Depends(get_path_service)
):
    try:
        return await path_service.solve_shortest_path(
            start=request.start,
            end=request.end,
            algorithm=request.algorithm
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# Best Path
# =========================
@router.post("/best", response_model=PathResult)
async def best_path(
    request: PathRequest,
    path_service: PathService = Depends(get_path_service)
):
    try:
        return await path_service.solve_best_path(
            start=request.start,
            end=request.end
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))