# 🎬 FramePilot AI

> **Turn every video into a smarter next upload.**

A world-class, creative-studio grade AI video analysis and YouTube SEO web application designed for YouTubers, Shorts creators, Instagram Reels creators, TikTok creators, editors, and growth strategists.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.143-green)
![Gemini](https://img.shields.io/badge/Google%20Gemini-Multimodal-purple)
![License](https://img.shields.io/badge/License-MIT-emerald)

---

## ✨ Features & Architecture

### 1. Ingestion & Multi-Platform Targeting
- Drag-and-drop video upload for MP4, MOV, WebM, and MKV with automatic duration and format detection.
- Configurable platform profiles: **YouTube Long-Form**, **YouTube Shorts**, **Instagram Reels**, and **TikTok**.
- Custom optimization objectives: Maximize Views & CTR, Search Discovery, Audience Retention, Channel Subscribers, and Educational Clarity.

### 2. Multimodal AI Analysis Engine
- Direct multimodal analysis of video footage, pacing entropy, visual variety, and vocal delivery powered by the modern Google GenAI SDK (`google-genai`).
- Configurable models: `gemini-2.5-flash`, `gemini-2.0-flash`, `gemini-1.5-flash`, and `gemini-2.5-pro`.
- Robust **High-Fidelity Demo Mode** for testing and showcasing without requiring immediate API keys.

### 3. YouTube Title & SEO Studio
- **10 Categorized Title Variations** (Search-Focused, Curiosity-Driven, Benefit-Focused, Storytelling, Short & Direct, and Platform-Optimized) with strategic rationale and AI scores.
- Ready-to-paste YouTube description generator with natural keyword context, timestamped chapters, calls to action, hashtags, and music credits.
- Primary topic, secondary keywords, search intent, suggested tags, export filename optimizer, pinned comments, playlist ideas, and end screen cards.
- **3 Thumbnail Concepts** with visual art direction, high-contrast text overlays, and Midjourney / Imagen image-generation prompts.

### 4. Hook Lab (First Seconds Engineering)
- In-depth critique of the opening 3-15 seconds and early retention grade.
- 4 alternative hook angle scripts: *Curiosity Gap*, *High-Stakes Loss Aversion*, *Instant Proof Demonstration*, and *Buyer's Binary Choice*.
- Concrete visual shots, on-screen text overlays, delivery pacing, and psychological triggers.
- Timestamped opening edit sequences.

### 5. Retention Optimization Lab
- Interactive visual timeline bar highlighting high, medium, and low attention risks.
- Clear distinction between **AI-predicted footage retention risks** and **measured channel analytics**.
- Interactive Chart.js retention curve graphing predicted retention vs measured retention with timestamped dips.
- Manual retention CSV import from YouTube Studio. OAuth is not implemented in this build.
- Manual retention CSV parser for YouTube Studio Analytics export files.
- Interactive editing checklist with completion progress tracking.

### 6. Sound Studio (Music & SFX Cues)
- Tone, emotional profile, and recommended tempo (BPM) analysis.
- Scene-by-scene track recommendations sourced directly from the official **YouTube Audio Library** with search links and licensing/attribution details.
- Specific sound effect trigger points and pattern interrupts.
- Canvas audio waveform visualizer with synchronized playback scrubbing.

### 7. Export & Productivity
- 1-click copy on every title, description, and image prompt with toast notifications.
- Export complete Markdown analysis report (`.md`).
- Export timestamped editing checklist (`.txt`).
- Export Sound Design cue sheet (`.csv`).
- Persistent SQLite storage for reopening, renaming, duplicating (for A/B tests), and deleting projects.

---

## 🚀 Quick Start

### 1. Requirements
- Python 3.10 or newer (tested on Python 3.11)
- Modern web browser (Chrome, Edge, Safari, Firefox, Brave)

### 2. Configure Environment Variables
The local `.env` file is private and is not exposed to the browser. If it does not exist, create it from the template:
```bash
copy .env.example .env
```

Open the project-root `.env` file and add your Gemini key locally:
```ini
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
MAX_FILE_SIZE_MB=500
KEEP_UPLOADS_AFTER_ANALYSIS=false
```
Do not paste the key into the website settings or commit `.env`. Without a key, demo analysis and sample projects remain available.

### 3. Run the Server
Launch the FastAPI application:
```bash
python -m uvicorn backend.app:app --port 8000 --reload
```

### 4. Open in Your Browser
Open:
```
http://localhost:8000
```

On Windows, you can instead double-click `start_framepilot.bat`. It creates a virtual environment if needed, installs the listed Python dependencies, creates missing data/upload folders without deleting existing contents, and starts FastAPI.

### Optional: Use VS Code Live Server
You can also open `frontend/index.html` with Live Server or directly as a local file. Start the FastAPI server above as well; Live Server serves only the frontend files, while the API and video analysis still come from FastAPI on port 8000. The frontend sends API requests to that backend for local Live Server and `file://` pages.

Tailwind is loaded from its CDN for this local prototype, so its production-use warning is expected. There is no frontend build pipeline in this repository; a compiled Tailwind bundle is needed before public production deployment. Chart.js and web fonts are also loaded from third-party CDNs.

---

## 🗂️ Project Structure

```
websiter/
├── backend/
│   ├── app.py                 # FastAPI application & static mounting
│   ├── config.py              # Environment settings & storage paths
│   ├── database.py            # SQLite database layer (projects, checklist)
│   ├── routes/
│   │   └── api.py             # SSE stream, CRUD, settings, exports, retention
│   └── services/
│       ├── ai_analyzer.py     # Google GenAI multimodal analysis pipeline
│       ├── mock_data.py       # High-fidelity realistic demonstration reports
│       ├── youtube_analytics.py # OAuth & manual CSV retention parser
│       └── export_service.py  # Markdown, TXT checklist, CSV cue sheet exports
├── frontend/
│   ├── index.html             # Studio single-page application
│   ├── css/
│   │   └── studio.css         # Creative studio design system & animations
│   └── js/
│       ├── app.js             # Application controller & state management
│       ├── api.js             # API client & SSE stream handler
│       ├── utils.js           # Clipboard, toast notifications, timecode helpers
│       └── components/
│           ├── videoPlayer.js # Synchronized video player & scrubber
│           ├── retentionChart.js # Chart.js dual retention curve
│           └── waveform.js    # Canvas audio waveform visualizer
├── data/                      # Local SQLite database storage
├── uploads/                   # Temporary upload directory (auto-purged)
├── .env.example               # Environment variables template
├── requirements.txt           # Python runtime and test dependencies
├── start_framepilot.bat       # Windows setup and startup helper
├── .gitignore                 # Ignore local secrets, database, uploads, and caches
└── README.md                  # This file
```

---

## 🔌 API Endpoints Summary

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Health check & model status |
| `POST` | `/api/analyze-stream` | Multipart video upload with real-time SSE progress stream |
| `GET` | `/api/projects` | List all saved projects |
| `GET` | `/api/projects/{id}` | Get single project with complete analysis |
| `PATCH` | `/api/projects/{id}` | Update project metadata |
| `DELETE` | `/api/projects/{id}` | Delete project and associated media |
| `POST` | `/api/projects/{id}/duplicate` | Duplicate project for A/B testing |
| `POST` | `/api/projects/{id}/checklist` | Update checklist item completion state |
| `POST` | `/api/projects/{id}/regenerate/{section}` | Regenerate specific section (e.g. titles, hooks) |
| `POST` | `/api/analytics/upload-retention/{id}` | Upload YouTube Studio CSV retention report |
| `GET` | `/api/analytics/youtube-oauth` | Reports that OAuth is not implemented |
| `GET` | `/api/export/{id}/{format}` | Export project (`markdown`, `checklist`, `sound_csv`, `json`) |
| `POST` | `/api/demo/{sample_key}` | Instantiate demo project (`tech_review` or `viral_shorts`) |

---

## 🛡️ Privacy & Security
- **Temporary Media Purging:** By default, uploaded media files are deleted immediately after multimodal analysis unless `KEEP_UPLOADS_AFTER_ANALYSIS=true` is set.
- **Client Security:** API keys are stored server-side and never exposed to frontend code.
- **Read-Only Scopes:** The YouTube integration uses strictly read-only scopes (`yt-analytics.readonly`).

---

## 📄 License
MIT — Open for personal and commercial creator use.
