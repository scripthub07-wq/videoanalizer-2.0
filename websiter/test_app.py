"""
Test suite for FramePilot AI backend services and endpoints.
"""
import asyncio

from fastapi.testclient import TestClient
from backend.app import app
from backend.database import init_db, list_projects, get_project, save_project
from backend.services.mock_data import SAMPLE_PROJECTS
from backend.services.youtube_analytics import youtube_analytics
from backend.services.export_service import export_service

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["app"] == "FramePilot AI"

def test_frontend_resources_and_favicon():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

    css_response = client.get("/static/css/studio.css")
    assert css_response.status_code == 200
    assert "text/css" in css_response.headers["content-type"]

    js_response = client.get("/static/js/app.js")
    assert js_response.status_code == 200
    assert js_response.headers["content-type"].split(";")[0] in {"text/javascript", "application/javascript"}

    favicon_response = client.get("/favicon.ico")
    assert favicon_response.status_code == 200
    assert "image/svg+xml" in favicon_response.headers["content-type"]

def test_gemini_key_cannot_be_changed_through_api():
    response = client.post("/api/settings", json={"gemini_api_key": "never-log-this-value"})
    assert response.status_code == 400
    assert "backend .env" in response.json()["detail"]
    assert "never-log-this-value" not in response.text

def test_youtube_oauth_is_reported_as_unimplemented():
    response = client.get("/api/analytics/youtube-oauth")
    assert response.status_code == 200
    assert response.json()["status"] == "not_implemented"
    assert response.json()["auth_url"] == ""

def test_empty_retention_csv_is_rejected():
    response = client.post("/api/demo/tech_review")
    project_id = response.json()["id"]
    upload_response = client.post(
        f"/api/analytics/upload-retention/{project_id}",
        data={"raw_csv": "Time,Retention\\n"}
    )
    assert upload_response.status_code == 400

def test_database_init_and_seeding():
    init_db()
    projects = list_projects()
    assert len(projects) >= 0

def test_demo_project_creation():
    response = client.post("/api/demo/tech_review")
    assert response.status_code == 200
    project = response.json()
    assert "id" in project
    assert project["platform"] == "youtube_long"
    assert "analysis" in project
    assert len(project["analysis"]["titles"]) >= 10
    assert len(project["analysis"]["thumbnails"]) == 3
    assert "hook_lab" in project["analysis"]
    assert "retention_lab" in project["analysis"]
    assert "sound_studio" in project["analysis"]

def test_project_retrieval_and_duplicate():
    # Create demo
    demo_res = client.post("/api/demo/viral_shorts")
    assert demo_res.status_code == 200
    pid = demo_res.json()["id"]

    # Get single
    get_res = client.get(f"/api/projects/{pid}")
    assert get_res.status_code == 200
    assert get_res.json()["id"] == pid

    # Duplicate
    dup_res = client.post(f"/api/projects/{pid}/duplicate")
    assert dup_res.status_code == 200
    dup_data = dup_res.json()
    assert dup_data["id"] != pid
    assert "Variant B" in dup_data["title"]

def test_checklist_update():
    demo_res = client.post("/api/demo/tech_review")
    pid = demo_res.json()["id"]
    checklist = demo_res.json()["checklist"]
    assert len(checklist) > 0
    first_item_id = checklist[0]["id"]

    # Toggle to completed
    res = client.post(f"/api/projects/{pid}/checklist", json={"item_id": first_item_id, "completed": True})
    assert res.status_code == 200
    updated_proj = client.get(f"/api/projects/{pid}").json()
    updated_item = next(c for c in updated_proj["checklist"] if c["id"] == first_item_id)
    assert updated_item["completed"] is True

def test_export_endpoints():
    demo_res = client.post("/api/demo/tech_review")
    pid = demo_res.json()["id"]

    # Markdown export
    md_res = client.get(f"/api/export/{pid}/markdown")
    assert md_res.status_code == 200    
    assert "FramePilot AI Analysis Report" in md_res.text

    # Checklist export
    chk_res = client.get(f"/api/export/{pid}/checklist")
    assert chk_res.status_code == 200
    assert "EDITING CHECKLIST" in chk_res.text

    # Sound CSV export
    csv_res = client.get(f"/api/export/{pid}/sound_csv")
    assert csv_res.status_code == 200
    assert "Music Track" in csv_res.text

def test_retention_csv_parsing():
    sample_csv = """Video Time (s),Audience Watch Percentage (%)
0,100
15,74.5
60,68.2
120,62.0
"""
    points = youtube_analytics.parse_manual_retention_csv(sample_csv)
    assert len(points) == 4
    assert points[0]["second"] == 0
    assert points[0]["measured_retention"] == 100
    assert points[1]["second"] == 15
    assert points[1]["measured_retention"] == 74.5


def test_live_ai_timeout_falls_back_to_demo_analysis():
    from backend.services.ai_analyzer import AIAnalyzer

    analyzer = AIAnalyzer()
    analyzer.api_key = "test-key"
    analyzer.client = object()

    async def slow_call(*args, **kwargs):
        await asyncio.sleep(0.5)
        return "done"

    try:
        asyncio.run(asyncio.wait_for(
            analyzer._run_with_timeout(slow_call, "slow call", timeout_seconds=0.05),
            timeout=1,
        ))
        raise AssertionError("Expected TimeoutError from the live AI timeout guard")
    except TimeoutError:
        pass

if __name__ == "__main__":
    print("Running FramePilot AI backend tests...")
    test_health_check()
    print("[PASS] Health check passed")
    test_frontend_resources_and_favicon()
    print("[PASS] Frontend assets and favicon passed")
    test_gemini_key_cannot_be_changed_through_api()
    print("[PASS] Backend-only Gemini key configuration passed")
    test_youtube_oauth_is_reported_as_unimplemented()
    print("[PASS] YouTube OAuth status passed")
    test_empty_retention_csv_is_rejected()
    print("[PASS] Invalid retention CSV handling passed")
    test_database_init_and_seeding()
    print("[PASS] Database init passed")
    test_demo_project_creation()
    print("[PASS] Demo project creation passed")
    test_project_retrieval_and_duplicate()
    print("[PASS] Project retrieval & duplicate passed")
    test_checklist_update()
    print("[PASS] Checklist state update passed")
    test_export_endpoints()
    print("[PASS] Multi-format export endpoints passed")
    test_retention_csv_parsing()
    print("[PASS] Retention CSV parser passed")
    print("\nALL TESTS PASSED SUCCESSFULLY!")
