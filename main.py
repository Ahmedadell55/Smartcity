"""
Smart City API - Main Entry Point
Clean Bootstrap Layer (No Business Logic)
"""

import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

from core import settings
from core import init_city, get_city
from core import SmartCityException

from data.supabase_client import init_supabase

# Routes
from apis.routes import (
    auth,
    nodes,
    edges,
    paths,
    analysis,
    projects,
    fleet,
    parking,
    search,
    
)

# =========================
# App Initialization
# =========================
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Smart City API - AI Powered System"
)


# =========================
# Middleware (Built-in)
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# Custom Exception Handler
# =========================
@app.exception_handler(SmartCityException)
async def smart_city_exception_handler(request: Request, exc: SmartCityException):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": str(exc),
            "type": exc.__class__.__name__
        }
    )


# =========================
# Include Routers
# =========================
routers = [
    auth.router,
    nodes.router,
    edges.router,
    paths.router,
    analysis.router,
    projects.router,
    fleet.router,
    parking.router,
    search.router,
    
]

for router in routers:
    app.include_router(router)


# =========================
# Startup Event
# =========================
@app.on_event("startup")
async def startup():
    """
    Initialize only core systems
    NOT business logic
    """
    settings.ensure_directories()

    # Init City (in-memory graph)
    init_city()

    # Init Database (Supabase)
    try:
        init_supabase()
    except Exception:
        pass


# =========================
# Root Endpoint
# =========================
@app.get("/")
async def root():
    if os.path.exists("index.html"):
        return FileResponse("index.html")

    return {
        "message": "Smart City API Running 🚀",
        "docs": "/docs",
        "health": "/health"
    }


# =========================
# Health Check (lightweight)
# =========================
@app.get("/health")
async def health():
    city = get_city()

    return {
        "status": "ok",
        "nodes": len(city.nodes),
        "edges": len(city.edges)
    }


# =========================
# API Info
# =========================
@app.get("/api/info")
async def info():
    city = get_city()

    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "nodes": len(city.nodes),
        "edges": len(city.edges)
    }


# =========================
# Run Server
# =========================
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
        reload=settings.DEBUG
    )