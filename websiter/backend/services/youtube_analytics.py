import csv
import io
import json
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger("framepilot.analytics")

class YouTubeAnalyticsService:
    def __init__(self):
        self.client_id = ""
        self.client_secret = ""
        self.oauth_scope = "https://www.googleapis.com/auth/yt-analytics.readonly https://www.googleapis.com/auth/youtube.readonly"

    def get_oauth_url(self, redirect_uri: str = "http://localhost:8000/api/auth/youtube/callback") -> Dict[str, str]:
        """
        Reports the current integration status without returning a nonfunctional URL.
        """
        return {
            "auth_url": "",
            "scope": self.oauth_scope,
            "status": "not_implemented",
            "disclosure": "YouTube OAuth is not implemented in this build. Import a YouTube Studio retention CSV to compare measured retention; no Google account access is requested."
        }

    def parse_manual_retention_csv(self, csv_text: str) -> List[Dict[str, float]]:
        """
        Parses a retention export CSV directly from YouTube Studio Analytics.
        Expected headers include: Elapsed Time (s) or Video Time, and Audience Retention % or Watch Percentage.
        """
        points = []
        try:
            reader = csv.reader(io.StringIO(csv_text))
            rows = list(reader)
            if not rows:
                return points

            header = [h.strip().lower() for h in rows[0]]
            
            # Find relevant column indices
            time_idx = -1
            retention_idx = -1
            
            for idx, col in enumerate(header):
                if any(k in col for k in ["time", "elapsed", "second", "timestamp"]):
                    time_idx = idx
                if any(k in col for k in ["retention", "percent", "percentage", "watch"]):
                    retention_idx = idx

            if time_idx == -1:
                time_idx = 0
            if retention_idx == -1 and len(header) > 1:
                retention_idx = 1

            for row in rows[1:]:
                if len(row) <= max(time_idx, retention_idx):
                    continue
                try:
                    time_str = row[time_idx].strip().replace("s", "")
                    # handle mm:ss format if present
                    if ":" in time_str:
                        parts = time_str.split(":")
                        sec = float(parts[0]) * 60 + float(parts[1])
                    else:
                        sec = float(time_str)

                    ret_str = row[retention_idx].strip().replace("%", "")
                    ret_val = float(ret_str)
                    
                    points.append({
                        "second": round(sec, 1),
                        "measured_retention": round(ret_val, 1)
                    })
                except (ValueError, IndexError):
                    continue
        except Exception as e:
            logger.error(f"Error parsing manual retention CSV: {e}")
            raise ValueError(f"Failed to parse retention CSV: {str(e)}")

        return sorted(points, key=lambda x: x["second"])

    def parse_manual_retention_json(self, json_data: Any) -> List[Dict[str, float]]:
        """Parses manual retention JSON array of {second: number, retention: number}."""
        points = []
        if isinstance(json_data, list):
            for item in json_data:
                if isinstance(item, dict):
                    sec = float(item.get("second", item.get("time", 0)))
                    val = float(item.get("measured_retention", item.get("retention", item.get("value", 0))))
                    points.append({"second": sec, "measured_retention": val})
        return sorted(points, key=lambda x: x["second"])

youtube_analytics = YouTubeAnalyticsService()
