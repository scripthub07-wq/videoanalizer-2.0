import os
from pathlib import Path
from dotenv import load_dotenv

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# Settings
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "500"))

# Storage paths
UPLOAD_DIR = BASE_DIR / "uploads"
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "framepilot.db"

# Ensure directories exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Privacy & Retention
KEEP_UPLOADS_AFTER_ANALYSIS = os.getenv("KEEP_UPLOADS_AFTER_ANALYSIS", "false").lower() == "true"
ALLOWED_EXTENSIONS = {".mp4", ".mov", ".webm", ".mkv", ".avi", ".m4v"}

def get_settings():
    return {
        "gemini_api_key_set": bool(GEMINI_API_KEY),
        "gemini_model": GEMINI_MODEL,
        "max_file_size_mb": MAX_FILE_SIZE_MB,
        "keep_uploads": KEEP_UPLOADS_AFTER_ANALYSIS,
        "supported_formats": list(ALLOWED_EXTENSIONS)
    }
