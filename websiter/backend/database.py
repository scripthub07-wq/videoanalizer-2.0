import sqlite3
import json
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from backend.config import DB_PATH

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            video_filename TEXT,
            video_url TEXT,
            duration REAL DEFAULT 0,
            platform TEXT NOT NULL DEFAULT 'youtube_long',
            niche TEXT DEFAULT '',
            audience TEXT DEFAULT '',
            language TEXT DEFAULT 'English',
            region TEXT DEFAULT 'Global',
            objective TEXT DEFAULT 'views',
            context TEXT DEFAULT '',
            channel_name TEXT DEFAULT '',
            keywords TEXT DEFAULT '',
            is_demo INTEGER DEFAULT 0,
            analysis_json TEXT NOT NULL,
            checklist_json TEXT DEFAULT '[]',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_project(project_data: Dict[str, Any]) -> str:
    conn = get_connection()
    cursor = conn.cursor()
    
    project_id = project_data.get("id") or str(uuid.uuid4())
    now = datetime.utcnow().isoformat()
    
    analysis_json = json.dumps(project_data.get("analysis", {}))
    checklist_json = json.dumps(project_data.get("checklist", []))
    
    cursor.execute("""
        INSERT OR REPLACE INTO projects (
            id, title, video_filename, video_url, duration, platform,
            niche, audience, language, region, objective, context,
            channel_name, keywords, is_demo, analysis_json, checklist_json,
            created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        project_id,
        project_data.get("title", "Untitled Analysis"),
        project_data.get("video_filename", ""),
        project_data.get("video_url", ""),
        float(project_data.get("duration", 0)),
        project_data.get("platform", "youtube_long"),
        project_data.get("niche", ""),
        project_data.get("audience", ""),
        project_data.get("language", "English"),
        project_data.get("region", "Global"),
        project_data.get("objective", "views"),
        project_data.get("context", ""),
        project_data.get("channel_name", ""),
        project_data.get("keywords", ""),
        1 if project_data.get("is_demo") else 0,
        analysis_json,
        checklist_json,
        project_data.get("created_at", now),
        now
    ))
    conn.commit()
    conn.close()
    return project_id

def list_projects() -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, video_filename, video_url, duration, platform,
               niche, audience, objective, is_demo, created_at, updated_at
        FROM projects
        ORDER BY created_at DESC
    """)
    rows = cursor.fetchall()
    projects = []
    for r in rows:
        projects.append(dict(r))
    conn.close()
    return projects

def get_project(project_id: str) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    data = dict(row)
    data["analysis"] = json.loads(data["analysis_json"])
    data["checklist"] = json.loads(data["checklist_json"])
    del data["analysis_json"]
    del data["checklist_json"]
    return data

def update_project(project_id: str, updates: Dict[str, Any]) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    
    fields = []
    values = []
    
    if "title" in updates:
        fields.append("title = ?")
        values.append(updates["title"])
    if "checklist" in updates:
        fields.append("checklist_json = ?")
        values.append(json.dumps(updates["checklist"]))
    if "analysis" in updates:
        fields.append("analysis_json = ?")
        values.append(json.dumps(updates["analysis"]))
        
    fields.append("updated_at = ?")
    values.append(datetime.utcnow().isoformat())
    values.append(project_id)
    
    if not fields:
        conn.close()
        return False
        
    cursor.execute(f"UPDATE projects SET {', '.join(fields)} WHERE id = ?", values)
    affected = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return affected

def delete_project(project_id: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
    affected = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return affected
