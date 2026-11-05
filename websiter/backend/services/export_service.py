import io
import csv
from typing import Dict, Any

class ExportService:
    @staticmethod
    def generate_markdown_report(project: Dict[str, Any]) -> str:
        analysis = project.get("analysis", {})
        title = project.get("title", "Untitled Analysis")
        platform = project.get("platform", "youtube_long").replace("_", " ").title()
        niche = project.get("niche", "General")
        score = analysis.get("overall_score", "N/A")
        
        md = []
        md.append(f"# 🎬 FramePilot AI Analysis Report: {title}")
        md.append(f"**Platform:** {platform} | **Niche:** {niche} | **Overall AI Score:** {score}/100\n")
        
        # Summary & Score Breakdown
        md.append("## 📌 Executive Summary")
        md.append(f"{analysis.get('summary', 'No summary available.')}\n")
        
        breakdown = analysis.get("score_breakdown", {})
        if breakdown:
            md.append("### Score Breakdown")
            for k, v in breakdown.items():
                label = k.replace("_", " ").title()
                md.append(f"- **{label}:** {v}/100")
            md.append("")

        # Strengths & Weaknesses
        strengths = analysis.get("strengths", [])
        if strengths:
            md.append("### Key Strengths")
            for s in strengths:
                md.append(f"- ✅ {s}")
            md.append("")

        weaknesses = analysis.get("weaknesses", [])
        if weaknesses:
            md.append("### Critical Weaknesses & Drop-off Risks")
            for w in weaknesses:
                md.append(f"- ⚠️ {w}")
            md.append("")

        top_improvements = analysis.get("top_improvements", [])
        if top_improvements:
            md.append("### 🚀 Top 3 High-Impact Improvements")
            for idx, imp in enumerate(top_improvements, 1):
                md.append(f"{idx}. {imp}")
            md.append("")

        # Titles
        titles = analysis.get("titles", [])
        if titles:
            md.append("## 🏷️ Title Variations (Ranked by AI Score)")
            for idx, t in enumerate(titles, 1):
                md.append(f"### {idx}. {t.get('title')}")
                md.append(f"- **Category:** {t.get('category')} | **Score:** {t.get('score')}/100")
                md.append(f"- **Keyword:** `{t.get('primary_keyword')}`")
                md.append(f"- **Strategy:** {t.get('rationale')}\n")

        # Description
        desc = analysis.get("description", {})
        if desc:
            md.append("## 📝 Ready-to-Paste YouTube Description")
            md.append("```text")
            md.append(desc.get("opening", ""))
            md.append("")
            md.append(desc.get("summary", ""))
            md.append("")
            
            chapters = desc.get("chapters", [])
            if chapters:
                md.append("TIMESTAMPS:")
                for c in chapters:
                    md.append(f"{c.get('timestamp')} - {c.get('title')}")
                md.append("")
                
            md.append(desc.get("cta", ""))
            md.append("")
            hashtags = " ".join(desc.get("hashtags", []))
            if hashtags:
                md.append(hashtags)
            md.append("```\n")

        # Hook Lab
        hook_lab = analysis.get("hook_lab", {})
        if hook_lab:
            md.append("## 🪝 Hook Lab & First Seconds Assessment")
            md.append(f"**Current Opening Grade:** {hook_lab.get('opening_retention_grade', 'N/A')}")
            md.append(f"**Assessment:** {hook_lab.get('assessment', '')}")
            md.append(f"**Identified Issue:** {hook_lab.get('potential_problem', '')}\n")
            
            alt_hooks = hook_lab.get("alternative_hooks", [])
            if alt_hooks:
                md.append("### Alternative Hook Scripts")
                for idx, h in enumerate(alt_hooks, 1):
                    md.append(f"#### Option {idx}: {h.get('angle')}")
                    md.append(f"> \"{h.get('script')}\"")
                    md.append(f"- **Visual:** {h.get('visual')}")
                    md.append(f"- **On-Screen Text:** `{h.get('on_screen_text')}`")
                    md.append(f"- **Why it works:** {h.get('why_it_works')}\n")

        # Retention Risks
        retention_lab = analysis.get("retention_lab", {})
        risks = retention_lab.get("retention_risks", [])
        if risks:
            md.append("## 📉 AI-Predicted Retention Risks")
            for r in risks:
                md.append(f"### ⏱️ [{r.get('timestamp')}] {r.get('category')} (Severity: {r.get('severity', '').upper()})")
                md.append(f"- **Issue:** {r.get('suspected_issue')}")
                md.append(f"- **Evidence:** {r.get('evidence')}")
                md.append(f"- **Editing Action:** {r.get('suggested_edit')}\n")

        # Sound Studio
        sound_studio = analysis.get("sound_studio", {})
        if sound_studio:
            md.append("## 🎵 Sound Studio & Audio Cues")
            md.append(f"- **Overall Tone:** {sound_studio.get('overall_tone')}")
            md.append(f"- **Recommended BPM:** {sound_studio.get('bpm_range')}")
            md.append(f"- **Dialogue Advice:** {sound_studio.get('dialogue_clarity_advice')}\n")
            
            tracks = sound_studio.get("youtube_audio_library_recommendations", [])
            if tracks:
                md.append("### YouTube Audio Library Tracks")
                for t in tracks:
                    md.append(f"- **Track:** {t.get('track_name')} by *{t.get('artist')}* ({t.get('duration')})")
                    md.append(f"  - Mood: {t.get('mood')} | Scene: {t.get('scene_placement')}")
                    md.append(f"  - Search in Library: `{t.get('search_query')}`")
                    md.append(f"  - License: {t.get('license_type')}\n")

        # Checklist
        checklist = project.get("checklist", [])
        if checklist:
            md.append("## ✅ Action Plan & Editing Checklist")
            for item in checklist:
                box = "[x]" if item.get("completed") else "[ ]"
                time_tag = f"({item.get('timestamp')}) " if item.get("timestamp") else ""
                md.append(f"- {box} {time_tag}{item.get('text')} *(Priority: {item.get('priority', 'medium').capitalize()})*")
            md.append("")

        md.append("---")
        md.append("*Generated by FramePilot AI — Turn every video into a smarter next upload.*")
        return "\n".join(md)

    @staticmethod
    def generate_editing_checklist_text(project: Dict[str, Any]) -> str:
        checklist = project.get("checklist", [])
        title = project.get("title", "Untitled Project")
        lines = [f"EDITING CHECKLIST — {title.upper()}", "=" * 50, ""]
        
        for idx, item in enumerate(checklist, 1):
            status = "[DONE]" if item.get("completed") else "[TODO]"
            timestamp = f"[{item.get('timestamp')}] " if item.get("timestamp") else ""
            priority = item.get("priority", "medium").upper()
            lines.append(f"{idx}. {status} {timestamp}{item.get('text')} (Priority: {priority})")
            
        lines.append("")
        lines.append("=" * 50)
        lines.append("Exported from FramePilot AI")
        return "\n".join(lines)

    @staticmethod
    def generate_sound_plan_csv(project: Dict[str, Any]) -> str:
        analysis = project.get("analysis", {})
        sound = analysis.get("sound_studio", {})
        tracks = sound.get("youtube_audio_library_recommendations", [])
        sfx = sound.get("sound_effects", [])
        
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Type", "Timestamp / Placement", "Name / Search Query", "Artist / Library", "Mood / Purpose", "License & Attribution"])
        
        for t in tracks:
            writer.writerow([
                "Music Track",
                t.get("scene_placement", ""),
                f"{t.get('track_name')} ({t.get('search_query')})",
                t.get("artist", ""),
                t.get("mood", ""),
                t.get("license_type", "")
            ])
            
        for s in sfx:
            writer.writerow([
                "Sound Effect",
                s.get("time", ""),
                s.get("name", ""),
                s.get("library_search", ""),
                s.get("purpose", ""),
                "Royalty-Free SFX"
            ])
            
        return output.getvalue()

export_service = ExportService()
