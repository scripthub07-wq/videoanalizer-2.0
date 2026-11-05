import os
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

from backend.config import BASE_DIR, UPLOAD_DIR
from backend.database import init_db, list_projects, save_project
from backend.services.mock_data import SAMPLE_PROJECTS
from backend.routes.api import router as api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB
    init_db()
    # Check if we have sample projects seeded
    existing = list_projects()
    if not existing:
        for key, sample in SAMPLE_PROJECTS.items():
            try:
                save_project(sample)
            except Exception as e:
                print(f"Error seeding sample {key}: {e}")
    yield

app = FastAPI(
    title="FramePilot AI",
    description="Turn every video into a smarter next upload.",
    version="2.0.0",
    lifespan=lifespan
)

# Enable CORS for local dev / cross-origin if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router)

# Mount uploads directory for static video previews
if UPLOAD_DIR.exists():
    app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

# Frontend directory
FRONTEND_DIR = BASE_DIR / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

@app.get("/")
async def serve_index():
    index_path = FRONTEND_DIR / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return JSONResponse({"status": "FramePilot AI API is running. Frontend not found."})

@app.get("/favicon.ico")
async def serve_favicon():
    svg_icon = FRONTEND_DIR / "favicon.svg"
    if svg_icon.exists():
        return FileResponse(str(svg_icon), media_type="image/svg+xml")
    return JSONResponse({"status": "Not Found"}, status_code=404)

@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    file_path = FRONTEND_DIR / full_path
    if file_path.exists() and file_path.is_file():
        return FileResponse(str(file_path))
    # If the request looks like an asset/file (.css, .js, .svg, .png, etc.), do NOT return index.html
    if any(full_path.endswith(ext) for ext in [".css", ".js", ".svg", ".png", ".jpg", ".jpeg", ".ico", ".json", ".map", ".woff", ".woff2", ".ttf"]):
        return JSONResponse({"status": "Not Found", "file": full_path}, status_code=404)
    index_path = FRONTEND_DIR / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return JSONResponse({"status": "Not Found"}, status_code=404)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app:app", host="0.0.0.0", port=8000, reload=True)
