import asyncio
import json
import logging
import os
import re
import shutil
import uuid
from pathlib import Path
from typing import Optional, List, Dict, Any

from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Response, Query
from fastapi.responses import StreamingResponse, PlainTextResponse

from backend.config import (
    UPLOAD_DIR,
    MAX_FILE_SIZE_MB,
    ALLOWED_EXTENSIONS,
    KEEP_UPLOADS_AFTER_ANALYSIS,
    GEMINI_MODEL,
    get_settings
)
from backend.database import (
    save_project,
    list_projects,
    get_project,
    update_project,
    delete_project
)
from backend.services.ai_analyzer import ai_analyzer
from backend.services.mock_data import SAMPLE_PROJECTS
from backend.services.youtube_analytics import youtube_analytics
from backend.services.export_service import export_service

router = APIRouter(prefix="/api")
logger = logging.getLogger("framepilot.api")


def current_settings():
    settings = get_settings()
    settings["gemini_model"] = ai_analyzer.model_name
    settings["keep_uploads"] = KEEP_UPLOADS_AFTER_ANALYSIS
    return settings

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "app": "FramePilot AI",
        "version": "2.0.0",
        "settings": current_settings(),
        "live_ai_ready": ai_analyzer.is_live_ai_available()
    }

@router.get("/settings")
async def get_app_settings():
    return current_settings()

@router.post("/settings")
async def update_app_settings(payload: Dict[str, Any]):
    global GEMINI_MODEL, KEEP_UPLOADS_AFTER_ANALYSIS
    if "gemini_api_key" in payload:
        raise HTTPException(
            status_code=400,
            detail="Configure GEMINI_API_KEY in the backend .env file; API keys cannot be changed through the browser."
        )
    if "gemini_model" in payload:
        GEMINI_MODEL = str(payload["gemini_model"]).strip()
        if not GEMINI_MODEL or len(GEMINI_MODEL) > 100:
            raise HTTPException(status_code=400, detail="A valid Gemini model name is required.")
        ai_analyzer.model_name = GEMINI_MODEL
    if "keep_uploads" in payload:
        KEEP_UPLOADS_AFTER_ANALYSIS = bool(payload["keep_uploads"])
        
    return {
        "success": True,
        "message": "Settings updated successfully",
        "settings": current_settings()
    }

@router.get("/projects")
async def get_all_projects():
    return list_projects()

@router.get("/projects/{project_id}")
async def get_single_project(project_id: str):
    proj = get_project(project_id)
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    return proj

@router.patch("/projects/{project_id}")
async def patch_project(project_id: str, updates: Dict[str, Any]):
    success = update_project(project_id, updates)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found or no changes made")
    return get_project(project_id)

@router.delete("/projects/{project_id}")
async def remove_project(project_id: str):
    proj = get_project(project_id)
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Clean up uploaded video file if exists
    video_filename = proj.get("video_filename")
    if video_filename:
        file_path = UPLOAD_DIR / video_filename
        if file_path.exists():
            try:
                file_path.unlink()
            except Exception:
                pass

    delete_project(project_id)
    return {"success": True, "message": "Project deleted successfully"}

@router.post("/projects/{project_id}/duplicate")
async def duplicate_project(project_id: str):
    proj = get_project(project_id)
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
        
    new_id = f"proj-{uuid.uuid4().hex[:8]}"
    proj["id"] = new_id
    proj["title"] = f"{proj.get('title', 'Project')} (Variant B)"
    proj["created_at"] = None # will reset to now
    save_project(proj)
    return get_project(new_id)

@router.post("/projects/{project_id}/checklist")
async def update_checklist_item(project_id: str, payload: Dict[str, Any]):
    proj = get_project(project_id)
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
        
    checklist = proj.get("checklist", [])
    item_id = payload.get("item_id")
    completed = payload.get("completed", False)
    
    for item in checklist:
        if item.get("id") == item_id:
            item["completed"] = completed
            break
            
    update_project(project_id, {"checklist": checklist})
    return {"success": True, "checklist": checklist}

@router.post("/projects/{project_id}/regenerate/{section}")
async def regenerate_section(project_id: str, section: str):
    proj = get_project(project_id)
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
        
    allowed_sections = ["titles", "hook_lab", "description", "sound_studio", "thumbnails"]
    if section not in allowed_sections:
        raise HTTPException(status_code=400, detail=f"Invalid section. Must be one of {allowed_sections}")
        
    current_analysis = proj.get("analysis", {})
    metadata = {
        "title": proj.get("title"),
        "platform": proj.get("platform"),
        "niche": proj.get("niche"),
        "audience": proj.get("audience"),
        "objective": proj.get("objective")
    }
    
    new_data = await ai_analyzer.regenerate_section(section, current_analysis, metadata)
    current_analysis[section] = new_data
    update_project(project_id, {"analysis": current_analysis})
    
    return {
        "success": True,
        "section": section,
        "data": new_data
    }

@router.post("/demo/{sample_key}")
async def create_demo_project(sample_key: str):
    if sample_key not in SAMPLE_PROJECTS:
        sample_key = "tech_review"
        
    sample = SAMPLE_PROJECTS[sample_key]
    new_id = f"demo-{uuid.uuid4().hex[:8]}"
    project_data = json.loads(json.dumps(sample))
    project_data["id"] = new_id
    project_data["is_demo"] = True
    save_project(project_data)
    return get_project(new_id)

@router.post("/analytics/upload-retention/{project_id}")
async def upload_manual_retention(
    project_id: str,
    file: Optional[UploadFile] = File(None),
    raw_csv: Optional[str] = Form(None)
):
    proj = get_project(project_id)
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
        
    points = []
    if file:
        content = (await file.read()).decode("utf-8", errors="ignore")
        points = youtube_analytics.parse_manual_retention_csv(content)
    elif raw_csv:
        points = youtube_analytics.parse_manual_retention_csv(raw_csv)
    else:
        raise HTTPException(status_code=400, detail="Provide a CSV file or raw_csv string")

    if not points:
        raise HTTPException(status_code=400, detail="The CSV did not contain any valid retention points.")
        
    analysis = proj.get("analysis", {})
    retention_lab = analysis.get("retention_lab", {})
    
    # Merge measured retention points
    existing_curve = retention_lab.get("simulated_retention_curve", [])
    for item in existing_curve:
        sec = item.get("second", 0)
        # Find closest measured point within 5s
        closest = min(points, key=lambda x: abs(x["second"] - sec), default=None)
        if closest and abs(closest["second"] - sec) <= 15:
            item["measured_retention"] = closest["measured_retention"]

    retention_lab["measured_source"] = "User Uploaded CSV / YouTube Studio Export"
    analysis["retention_lab"] = retention_lab
    update_project(project_id, {"analysis": analysis})
    
    return {
        "success": True,
        "points_count": len(points),
        "curve": existing_curve
    }

@router.get("/analytics/youtube-oauth")
async def get_youtube_oauth_details():
    return youtube_analytics.get_oauth_url()

@router.get("/export/{project_id}/{export_format}")
async def export_project(project_id: str, export_format: str):
    proj = get_project(project_id)
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
        
    raw_title = proj.get("title", "framepilot-analysis").lower().replace(" ", "-")
    filename_base = re.sub(r'[^a-zA-Z0-9_\-]', '', raw_title)[:40] or "framepilot-analysis"
    
    if export_format == "markdown":
        md = export_service.generate_markdown_report(proj)
        return PlainTextResponse(
            content=md,
            media_type="text/markdown",
            headers={"Content-Disposition": f"attachment; filename={filename_base}-report.md"}
        )
    elif export_format == "checklist":
        txt = export_service.generate_editing_checklist_text(proj)
        return PlainTextResponse(
            content=txt,
            media_type="text/plain",
            headers={"Content-Disposition": f"attachment; filename={filename_base}-checklist.txt"}
        )
    elif export_format == "sound_csv":
        csv_data = export_service.generate_sound_plan_csv(proj)
        return PlainTextResponse(
            content=csv_data,
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename_base}-sound-plan.csv"}
        )
    elif export_format == "json":
        return proj
    else:
        raise HTTPException(status_code=400, detail="Supported formats: markdown, checklist, sound_csv, json")

@router.post("/analyze-stream")
async def analyze_video_stream(
    video: Optional[UploadFile] = File(None),
    title: str = Form("Untitled Analysis"),
    platform: str = Form("youtube_long"),
    niche: str = Form("General"),
    audience: str = Form("General creators"),
    language: str = Form("English"),
    region: str = Form("Global"),
    objective: str = Form("views"),
    context: str = Form(""),
    channel_name: str = Form(""),
    keywords: str = Form(""),
    duration: float = Form(0.0),
    is_demo_mode: bool = Form(False)
):
    """
    Streams analysis progress via Server-Sent Events (SSE).
    """
    saved_filename = ""
    saved_path = None
    
    if video and video.filename:
        client_filename = video.filename.replace("\\", "/").rsplit("/", 1)[-1]
        ext = Path(client_filename).suffix.lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail=f"Unsupported format {ext}. Allowed: {ALLOWED_EXTENSIONS}")

        safe_stem = re.sub(r"[^a-zA-Z0-9_-]", "_", Path(client_filename).stem).strip("_") or "video"
        saved_filename = f"{uuid.uuid4().hex[:10]}_{safe_stem}{ext}"
        saved_path = UPLOAD_DIR / saved_filename
        max_file_size = MAX_FILE_SIZE_MB * 1024 * 1024
        bytes_written = 0
        try:
            with open(saved_path, "wb") as output_file:
                while chunk := await video.read(1024 * 1024):
                    bytes_written += len(chunk)
                    if bytes_written > max_file_size:
                        raise HTTPException(
                            status_code=413,
                            detail=f"Video exceeds the {MAX_FILE_SIZE_MB} MB upload limit."
                        )
                    output_file.write(chunk)
        except Exception:
            saved_path.unlink(missing_ok=True)
            raise

    metadata = {
        "title": title,
        "platform": platform,
        "niche": niche,
        "audience": audience,
        "language": language,
        "region": region,
        "objective": objective,
        "context": context,
        "channel_name": channel_name,
        "keywords": keywords,
        "duration": duration or (54 if "short" in platform or "reels" in platform else 580),
        "is_demo": is_demo_mode or not ai_analyzer.is_live_ai_available()
    }

    async def sse_event_generator():
        try:
            steps = [
                ("upload", "Video uploaded; verifying media...", 10),
                ("inspect", "Video received; preparing analysis...", 25),
            ]

            for step_key, label, pct in steps:
                yield f"event: progress\ndata: {json.dumps({'step': step_key, 'label': label, 'percent': pct})}\n\n"
                await asyncio.sleep(0.2)

            # Report progress while the actual AI request runs instead of showing 99%
            # before the slowest part of the work has started.
            analysis_task = asyncio.create_task(
                ai_analyzer.analyze_video(str(saved_path) if saved_path else None, metadata)
            )
            loop = asyncio.get_running_loop()
            deadline = loop.time() + 45
            while not analysis_task.done():
                remaining = deadline - loop.time()
                if remaining <= 0:
                    analysis_task.cancel()
                    analysis = ai_analyzer._generate_contextual_analysis(
                        metadata,
                        error_note="Live analysis exceeded 45 seconds; demo analysis was used."
                    )
                    break

                done, _ = await asyncio.wait({analysis_task}, timeout=min(2, remaining))
                if done:
                    analysis = await analysis_task
                    break

                elapsed = 45 - (deadline - loop.time())
                percent = min(90, 30 + int(elapsed / 45 * 60))
                yield f"event: progress\ndata: {json.dumps({'step': 'analysis', 'label': 'Analyzing video; this can take a little while...', 'percent': percent})}\n\n"

            yield f"event: progress\ndata: {json.dumps({'step': 'finalizing', 'label': 'Saving your analysis...', 'percent': 95})}\n\n"
            
            # Construct checklist from retention risks & weaknesses
            checklist = []
            for idx, r in enumerate(analysis.get("retention_lab", {}).get("retention_risks", []), 1):
                checklist.append({
                    "id": f"chk-{idx}",
                    "text": r.get("suggested_edit"),
                    "completed": False,
                    "priority": r.get("severity", "medium"),
                    "timestamp": r.get("timestamp")
                })

            project_id = f"fp-{uuid.uuid4().hex[:8]}"
            project_data = {
                "id": project_id,
                "title": title if title != "Untitled Analysis" else analysis.get("titles", [{}])[0].get("title", "Untitled Project"),
                "video_filename": saved_filename,
                "video_url": f"/uploads/{saved_filename}" if (saved_filename and KEEP_UPLOADS_AFTER_ANALYSIS) else "",
                "duration": metadata["duration"],
                "platform": platform,
                "niche": niche,
                "audience": audience,
                "language": language,
                "region": region,
                "objective": objective,
                "context": context,
                "channel_name": channel_name,
                "keywords": keywords,
                "is_demo": metadata["is_demo"],
                "analysis": analysis,
                "checklist": checklist
            }

            save_project(project_data)

            yield f"event: progress\ndata: {json.dumps({'step': 'complete', 'label': 'Analysis complete', 'percent': 100})}\n\n"
            yield f"event: complete\ndata: {json.dumps({'project_id': project_id, 'project': project_data})}\n\n"

        except Exception as e:
            logger.error("Analysis stream failed (%s)", type(e).__name__)
            yield f"event: error\ndata: {json.dumps({'message': 'Analysis failed. Check the backend logs and try again.'})}\n\n"
        finally:
            if saved_path and saved_path.exists() and not KEEP_UPLOADS_AFTER_ANALYSIS:
                try:
                    saved_path.unlink()
                except OSError:
                    logger.warning("Could not remove a temporary uploaded video file.")

    return StreamingResponse(sse_event_generator(), media_type="text/event-stream")
