import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi.responses import FileResponse

from backend.app.core.config import settings
from backend.app.db.session import engine, Base
from backend.app.api.auth import router as auth_router
from backend.app.api.business import router as business_router
from backend.app.api.industries import router as industries_router
from backend.app.api.content import router as content_router
from backend.app.api.image import router as image_router
from backend.app.api.usage import router as usage_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static Files for generated banner/marketing images
app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")

# Include Routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(business_router, prefix=settings.API_V1_STR)
app.include_router(industries_router, prefix=settings.API_V1_STR)
app.include_router(content_router, prefix=settings.API_V1_STR)
app.include_router(image_router, prefix=settings.API_V1_STR)
app.include_router(usage_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    index = Path(__file__).resolve().parents[2] / "frontend" / "dist" / "index.html"
    if index.exists():
        return FileResponse(index)
    return {
        "status": "healthy",
        "name": settings.PROJECT_NAME,
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "service": "no-prompt-content-saas-api"}

# Serve the built React application from the same origin as the API.
frontend_dist = Path(__file__).resolve().parents[2] / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/assets", StaticFiles(directory=frontend_dist / "assets"), name="assets")
    @app.get("/studio")
    async def studio():
        return FileResponse(frontend_dist / "index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
