"""
Production-quality sample reports for demonstration and fallback modes in FramePilot AI.
Accurately mirrors real-world YouTube & Short-form video optimization scenarios.
"""

from typing import Dict, Any

SAMPLE_PROJECTS: Dict[str, Dict[str, Any]] = {
    "tech_review": {
        "id": "demo-tech-review-01",
        "title": "M4 iPad Pro: 30 Days Later — Don't Make This Mistake",
        "video_filename": "ipad_pro_m4_30days_review.mp4",
        "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4", # standard reliable test stream
        "duration": 582, # 9m 42s
        "platform": "youtube_long",
        "niche": "Technology & Consumer Electronics",
        "audience": "Tech enthusiasts, creative pros, and buyers weighing whether to upgrade",
        "language": "English",
        "region": "Global / North America",
        "objective": "views",
        "context": "Comprehensive 30-day follow up review highlighting software limitations vs hardware overkill.",
        "channel_name": "TechCraft Studio",
        "keywords": "ipad pro m4, m4 ipad review, ipad os 18, apple silicon, oled ipad",
        "is_demo": True,
        "created_at": "2026-10-12T14:30:00Z",
        "checklist": [
            {"id": "c1", "text": "Trim the 14-second desktop preamble; jump straight to the bent chassis hook", "completed": False, "priority": "high", "timestamp": "00:00 - 00:14"},
            {"id": "c2", "text": "Add sound whoosh and kinetic text overlay at 01:12 for battery test stats", "completed": True, "priority": "medium", "timestamp": "01:12"},
            {"id": "c3", "text": "Cut 28 seconds of repeated display brightness specs in section 2", "completed": False, "priority": "high", "timestamp": "02:45 - 03:13"},
            {"id": "c4", "text": "Insert side-by-side B-roll comparing M2 vs M4 rendering times in Final Cut", "completed": True, "priority": "high", "timestamp": "04:20"},
            {"id": "c5", "text": "Add ducking (-14dB) to background synth pad during thermal throttle explanation", "completed": False, "priority": "medium", "timestamp": "06:10"},
            {"id": "c6", "text": "Replace talking head outro with tangible buying decision checklist on screen", "completed": False, "priority": "low", "timestamp": "08:50"}
        ],
        "analysis": {
            "summary": "High production value review with crisp 4K visuals and balanced lighting. However, the first 15 seconds suffer from a slow conversational intro that delays the core dilemma ('Is this $1,300 machine held back by iPadOS?'). Viewer drop-off risk is highest between 02:45 and 03:30 due to unedited talking-head repetition.",
            "overall_score": 84,
            "score_breakdown": {
                "hook_strength": 72,
                "visual_pacing": 86,
                "story_structure": 81,
                "sound_design": 89,
                "seo_potential": 93
            },
            "score_rationale": "Score is based on algorithmic pacing analysis, audio-visual entropy, and search intent alignment against top-performing videos in the consumer tech niche.",
            "strengths": [
                "Exceptional macro B-roll of the Tandem OLED panel and chassis milling.",
                "Clear audio recording with negligible background noise and balanced vocal EQ.",
                "Strong closing verdict with distinct user profile recommendations."
            ],
            "weaknesses": [
                "14-second delayed hook: opening question is buried behind standard creator greetings.",
                "Static camera position for over 45 consecutive seconds during display technical discussion.",
                "Lack of patterned audio punctuation (risers/hits) leading into chapter transitions."
            ],
            "top_improvements": [
                "Replace the opening 14 seconds with the punchy chassis comparison shot recorded at 04:12.",
                "Insert pattern interrupts (zooms, graphics, screen grabs) every 6-8 seconds during spec breakdowns.",
                "Adopt title variant #2 ('The M4 iPad Trap') to exploit curiosity gap regarding software limitations."
            ],
            "titles": [
                {
                    "category": "Curiosity-Driven",
                    "title": "The M4 iPad Pro Trap: Don't Buy Until You See This",
                    "rationale": "Triggers immediate loss aversion for prospective buyers while teasing an unexpected flaw.",
                    "primary_keyword": "m4 ipad pro",
                    "score": 96
                },
                {
                    "category": "Search-Focused",
                    "title": "M4 iPad Pro 30 Days Later: Honest Review & Real Battery Test",
                    "rationale": "Targets high-intent searchers looking for long-term reliability and battery verification.",
                    "primary_keyword": "m4 ipad pro 30 days later",
                    "score": 92
                },
                {
                    "category": "Benefit-Focused",
                    "title": "Can The M4 iPad Pro Actually Replace Your MacBook? (Tested)",
                    "rationale": "Answers the perennial $1,200 question directly with empirical proof.",
                    "primary_keyword": "ipad pro replace macbook",
                    "score": 94
                },
                {
                    "category": "Storytelling",
                    "title": "I Used Only The M4 iPad Pro for 30 Days. Here's What Broke Me.",
                    "rationale": "Narrative framing creates emotional investment and anticipatory tension.",
                    "primary_keyword": "ipad pro 30 days",
                    "score": 91
                },
                {
                    "category": "Short & Direct",
                    "title": "M4 iPad Pro: Incredible Hardware, Terrible OS",
                    "rationale": "Ultra punchy contrast that fits completely in mobile notifications and browse feeds.",
                    "primary_keyword": "m4 ipad pro review",
                    "score": 89
                },
                {
                    "category": "Platform & Audience Optimized",
                    "title": "Why I'm Returning My M4 iPad Pro... (And What I'm Buying Instead)",
                    "rationale": "Classic tech turnaround format that drives sky-high click-through rates.",
                    "primary_keyword": "returning m4 ipad pro",
                    "score": 95
                },
                {
                    "category": "Search-Focused",
                    "title": "Apple M4 iPad Pro In-Depth Review: OLED Display, Performance, iPadOS",
                    "rationale": "Keyword-dense indexing for search ranking across YouTube and Google Video carousels.",
                    "primary_keyword": "apple m4 ipad pro review",
                    "score": 87
                },
                {
                    "category": "Curiosity-Driven",
                    "title": "Apple's Most Powerful Mistake?",
                    "rationale": "Minimalist intrigue hook designed for browse and suggested algorithm placement.",
                    "primary_keyword": "apple m4 ipad",
                    "score": 88
                },
                {
                    "category": "Benefit-Focused",
                    "title": "M4 iPad Pro Buyer's Guide: 11\" vs 13\" & Nano-Texture Reality",
                    "rationale": "Addresses practical pre-purchase sizing and screen coating dilemmas.",
                    "primary_keyword": "m4 ipad buyers guide",
                    "score": 90
                },
                {
                    "category": "Storytelling",
                    "title": "The Hardware Is from 2030. The Software Is from 2018.",
                    "rationale": "Vivid metaphorical comparison that crystallizes the video's core philosophical conclusion.",
                    "primary_keyword": "m4 ipad software limitations",
                    "score": 93
                }
            ],
            "description": {
                "opening": "30 days with the new M4 iPad Pro, and one thing is undeniable: this is the most insane hardware Apple has ever built, crippled by the most frustrating operating system. Here is the unvarnished truth about battery life, OLED thermals, and why you might want to save your money.",
                "main_search_phrase": "M4 iPad Pro 30 days later review",
                "summary": "In this in-depth long-term review, we test the 13-inch M4 iPad Pro against demanding 4K ProRes rendering in Final Cut, battery drain during continuous Procreate sessions, and the reality of Tandem OLED in direct sunlight. We also compare real-world workflows to the M3 MacBook Air.",
                "chapters": [
                    {"timestamp": "00:00", "title": "The $1,300 Dilemma"},
                    {"timestamp": "01:15", "title": "Tandem OLED vs Direct Sunlight"},
                    {"timestamp": "03:00", "title": "M4 Speed vs Thermal Throttling"},
                    {"timestamp": "05:10", "title": "Battery Life: Real Numbers"},
                    {"timestamp": "07:05", "title": "The iPadOS 18 Bottleneck"},
                    {"timestamp": "08:45", "title": "Final Verdict: Who Should Upgrade?"}
                ],
                "cta": "If this helped you decide, hit Subscribe and let me know in the comments: are you upgrading or sticking with your current tablet?",
                "hashtags": ["#iPadPro", "#Apple", "#M4iPadPro", "#TechReview"],
                "credits": "Audio tracks sourced via YouTube Audio Library. Sound design mastered in-house."
            },
            "seo_package": {
                "primary_topic": "Apple M4 iPad Pro Long-Term Review",
                "secondary_keywords": ["m4 chip performance", "tandem oled display", "ipados 18 workflow", "ipad pro vs macbook air", "tablet buying guide 2026"],
                "search_intent": "Commercial investigation / Pre-purchase product evaluation",
                "target_audience": "Digital artists, video editors, tech shoppers aged 22-45",
                "suggested_tags": ["m4 ipad pro", "ipad pro 2024", "ipad pro 2025", "apple ipad pro", "ipad m4 review", "ipad pro 30 days later", "tandem oled", "ipados review", "apple silicon", "tech review"],
                "suggested_filename": "m4-ipad-pro-30-days-later-review-4k60.mp4",
                "pinned_comment": "Question of the day: What is the ONE feature iPadOS needs before you would replace your laptop with an iPad? Pinning the most insightful response below! 👇",
                "playlist_ideas": ["Apple Silicon Ecosystem In-Depth", "Ultimate Creator Gear Reviews", "iPad vs Mac Faceoffs"],
                "end_screen_cards": [
                    {"type": "Video", "suggestion": "M3 MacBook Air vs M4 iPad Pro (Best Value for Creators)", "timestamp": "09:20"},
                    {"type": "Playlist", "suggestion": "Apple Tablet Buying Guides", "timestamp": "09:25"}
                ]
            },
            "thumbnails": [
                {
                    "concept_name": "The Split Reality",
                    "visual_description": "Close-up of creator holding the ultra-thin M4 iPad profile edge-on, expression of conflicted surprise. Neon red hazard tape graphic across half the screen reading 'DON'T BUY YET'.",
                    "text_overlay": "DON'T BUY YET",
                    "color_palette": "Deep Charcoal, Crisp White, Warning Red accent",
                    "rationale": "High contrast, bold 3-word rule, instantly readable at 120px mobile thumbnail resolution.",
                    "image_prompt": "Ultra-crisp 4K YouTube thumbnail, professional tech reviewer holding an impossibly thin silver modern tablet side-profile with glowing dual OLED screen, studio dark charcoal background, moody rim lighting in electric lime and cold white, high detail, high dynamic range --ar 16:9"
                },
                {
                    "concept_name": "The Spec Fallacy",
                    "visual_description": "M4 chip glowing violently through the back of an iPad, side by side with a giant red 'LOCKED' padlock icon overlaid on an iPadOS window.",
                    "text_overlay": "M4 IS WASTED?",
                    "color_palette": "Electric Cyan, Neon Amber, Graphite",
                    "rationale": "Piques hardware enthusiast curiosity by highlighting the processor vs software divide.",
                    "image_prompt": "Cinematic tech product photography, metallic sleek futuristic tablet laying on a minimalist carbon-fiber desk, glowing holographic processor core radiating blue power, dark dramatic studio lighting, octane render, 8k --ar 16:9"
                },
                {
                    "concept_name": "The Honest Faceoff",
                    "visual_description": "Creator pointing between M4 iPad Pro and M3 MacBook Air on desk, yellow highlight circle on the price tag difference.",
                    "text_overlay": "SAVE $600.",
                    "color_palette": "Minimalist Studio Black, Electric Yellow text badge",
                    "rationale": "Direct financial saving incentive that appeals to pragmatic shoppers.",
                    "image_prompt": "YouTube thumbnail, modern tech studio desk with silver M4 iPad Pro on magic keyboard next to a space black MacBook Air, clean aesthetic, studio lighting, hyper-realistic, photorealistic --ar 16:9"
                }
            ],
            "hook_lab": {
                "assessment": "The current opening spends 14 seconds saying 'Hey guys welcome back today we are finally doing the 30 day test of the iPad'. This loses approximately 32% of mobile scrollers who decide whether to stay within the first 3.8 seconds.",
                "original_opening": "Hey guys, welcome back to TechCraft. So it's been a month since Apple sent over the M4 iPad Pro, and I've been using it every single day...",
                "potential_problem": "Passive creator-centric introduction. Viewers don't yet know what stakes exist or why today's verdict is urgent.",
                "opening_retention_grade": "C+",
                "alternative_hooks": [
                    {
                        "angle": "The High-Stakes Dilemma (Loss Aversion)",
                        "script": "I spent $1,300 on Apple's fastest device ever created, and after 30 days... I think 90% of you should NEVER buy it.",
                        "visual": "Extreme close-up of sliding the credit card across the desk, then immediately cutting to the iPad spinning on the black turntable.",
                        "on_screen_text": "$1,300 MISTAKE?",
                        "pacing_notes": "Deliver in under 4.2 seconds. Cut immediately on the word 'NEVER'.",
                        "why_it_works": "Contrasts the extreme price and power with a controversial negative recommendation."
                    },
                    {
                        "angle": "The Instant Proof Demonstration",
                        "script": "Watch this: the M4 renders this 8K timeline in 40 seconds. But watch what happens when I try to export a simple folder...",
                        "visual": "Side-by-side screen recording: blazing fast render bar, followed by the iPadOS spinning error wheel.",
                        "on_screen_text": "M4 HARDWARE vs IPADOS",
                        "pacing_notes": "Start with motion audio immediately. Zero greeting.",
                        "why_it_works": "Shows the exact paradox of the product before uttering a single opinion."
                    },
                    {
                        "angle": "The Direct Curiosity Gap",
                        "script": "There is a massive flaw in the new iPad Pro that no one is talking about, and it only reveals itself after week three.",
                        "visual": "Macro probe lens shot moving across the camera bump and the ultra-thin chassis edge.",
                        "on_screen_text": "THE WEEK 3 FLAW",
                        "pacing_notes": "Low, focused vocal tone with subtle low-end bass thud.",
                        "why_it_works": "Time-release mystery makes viewers want to stay to find out what happens after week three."
                    },
                    {
                        "angle": "The Buyer's Binary Choice",
                        "script": "Before you spend $1,000 on the new OLED iPad, there is an exact formula to know whether you'll love it or return it.",
                        "visual": "Split screen showing MacBook Air on left ($1,099) vs iPad Pro setup on right ($1,650).",
                        "on_screen_text": "KEEP OR RETURN?",
                        "pacing_notes": "Snappy, pragmatic delivery with cash counter SFX.",
                        "why_it_works": "Directly serves the buyer's anxiety with structured guidance."
                    }
                ],
                "recommended_edit_sequence": [
                    {"time": "00:00 - 00:02", "shot": "Macro close-up chassis bend test + Bass Drop SFX", "overlay": "30 DAYS LATER"},
                    {"time": "00:02 - 00:05", "shot": "Creator direct to camera delivering Hook #1", "overlay": "DON'T BUY YET"},
                    {"time": "00:05 - 00:08", "shot": "Rapid 3-cut montage: OLED glare test, Final Cut crash, battery warning", "overlay": ""},
                    {"time": "00:08 - 00:10", "shot": "Cut back to creator: 'Here is what Apple didn't tell you.'", "overlay": "THE TRUTH"}
                ]
            },
            "retention_lab": {
                "disclaimer": "Footage-based findings are AI-predicted retention risks identified from visual pacing, speech tempo, and entropy shifts. Measured analytics require connecting YouTube Studio OAuth.",
                "timeline_segments": [
                    {"start": 0, "end": 14, "label": "Intro Preamble", "risk_level": "high", "drop_probability": "34%"},
                    {"start": 14, "end": 145, "label": "Tandem OLED Analysis", "risk_level": "low", "drop_probability": "8%"},
                    {"start": 145, "end": 210, "label": "Chassis & Ergonomics", "risk_level": "medium", "drop_probability": "18%"},
                    {"start": 210, "end": 320, "label": "Benchmark Speeds", "risk_level": "high", "drop_probability": "41%"},
                    {"start": 320, "end": 440, "label": "iPadOS Workflow Reality", "risk_level": "low", "drop_probability": "9%"},
                    {"start": 440, "end": 510, "label": "Battery Life Test", "risk_level": "medium", "drop_probability": "16%"},
                    {"start": 510, "end": 582, "label": "Buying Verdict & Outro", "risk_level": "medium", "drop_probability": "22%"}
                ],
                "retention_risks": [
                    {
                        "timestamp": "00:00 - 00:14",
                        "severity": "high",
                        "category": "Pacing & Opening",
                        "suspected_issue": "Standard channel greeting and delayed topic establishment.",
                        "evidence": "Creator looks down at desk notes for 3.2 seconds; zero motion graphic or dynamic framing.",
                        "suggested_edit": "Hard cut directly to 00:14 where the OLED comparison begins, or insert Hook Angle #1.",
                        "priority": 1
                    },
                    {
                        "timestamp": "02:45 - 03:25",
                        "severity": "high",
                        "category": "Repetition & Visual Stagnation",
                        "suspected_issue": "Monotonous talking head discussing Geekbench multicore scores without visual charts.",
                        "evidence": "40 consecutive seconds without a B-roll cut, screen overlay, or sound effect.",
                        "suggested_edit": "Cut the verbal reading of numbers by 50%. Display an animated bar chart overlay with subtle mechanical tick audio.",
                        "priority": 2
                    },
                    {
                        "timestamp": "04:15 - 04:38",
                        "severity": "medium",
                        "category": "Pacing Stall",
                        "suspected_issue": "Long pauses while creator looks for files in the Files app.",
                        "evidence": "Two silences measuring 2.4s and 3.1s with noticeable mouse clicking sound.",
                        "suggested_edit": "Ripple delete the search pauses and speed up screen capture to 250% with whoosh transition.",
                        "priority": 3
                    },
                    {
                        "timestamp": "07:15 - 07:42",
                        "severity": "medium",
                        "category": "Audience Disconnect",
                        "suspected_issue": "Niche developer tool discussion irrelevant to general consumer audience.",
                        "evidence": "Discussion of virtualization flags without clarifying consumer impact.",
                        "suggested_edit": "Simplify explanation into a 5-second takeaway: 'You still can't run Mac apps.'",
                        "priority": 4
                    },
                    {
                        "timestamp": "09:10 - 09:42",
                        "severity": "low",
                        "category": "Exit Signal Leakage",
                        "suspected_issue": "Saying 'Well guys, that's pretty much my thoughts' telegraphs the ending early.",
                        "evidence": "Viewer exit spikes when hearing standard closing sign-offs before end cards trigger.",
                        "suggested_edit": "Keep delivering valuable verdict advice right until the final 5 seconds; cue end screen without verbal warning.",
                        "priority": 5
                    }
                ],
                "simulated_retention_curve": [
                    {"second": 0, "predicted_retention": 100, "measured_retention": 100},
                    {"second": 15, "predicted_retention": 74, "measured_retention": 68},
                    {"second": 60, "predicted_retention": 69, "measured_retention": 65},
                    {"second": 120, "predicted_retention": 63, "measured_retention": 62},
                    {"second": 180, "predicted_retention": 58, "measured_retention": 54},
                    {"second": 240, "predicted_retention": 45, "measured_retention": 41}, # dip at benchmark stall
                    {"second": 300, "predicted_retention": 43, "measured_retention": 39},
                    {"second": 360, "predicted_retention": 42, "measured_retention": 38},
                    {"second": 420, "predicted_retention": 40, "measured_retention": 37},
                    {"second": 480, "predicted_retention": 38, "measured_retention": 35},
                    {"second": 540, "predicted_retention": 35, "measured_retention": 31},
                    {"second": 582, "predicted_retention": 28, "measured_retention": 24}
                ]
            },
            "sound_studio": {
                "overall_tone": "Analytical, sleek, contemplative tech commentary",
                "bpm_range": "100 - 118 BPM",
                "dialogue_clarity_advice": "Vocal track sits nicely at -12 LUFS. Keep background music ducked to -24dB to avoid competing with low-mid vocal frequencies (250Hz - 400Hz).",
                "youtube_audio_library_recommendations": [
                    {
                        "track_name": "Digital Atmosphere",
                        "artist": "Density & Time",
                        "duration": "2:45",
                        "mood": "Cinematic Tension / Modern Ambient",
                        "tempo": "Mid-tempo (112 BPM)",
                        "genre": "Electronic",
                        "license_type": "YouTube Audio Library (No attribution required)",
                        "official_url": "https://www.youtube.com/audiolibrary",
                        "search_query": "Digital Atmosphere Density & Time",
                        "scene_placement": "00:00 - 02:30 (Opening Hook through OLED analysis)",
                        "transition_notes": "Start with low-pass filter at 00:00, open full frequency at 00:14 when B-roll begins.",
                        "attribution_text": "Free to use across monetized YouTube uploads. Attribution not required."
                    },
                    {
                        "track_name": "Cerebral",
                        "artist": "Ezra",
                        "duration": "3:10",
                        "mood": "Analytical / Pulsing Tech Groove",
                        "tempo": "Energetic (120 BPM)",
                        "genre": "Ambient Beat",
                        "license_type": "YouTube Audio Library (No attribution required)",
                        "official_url": "https://www.youtube.com/audiolibrary",
                        "search_query": "Cerebral Ezra electronic",
                        "scene_placement": "02:30 - 05:20 (M4 Benchmark & Final Cut Stress Test)",
                        "transition_notes": "Subtle bass drop right at 02:45 on benchmark reveal. Duck -4dB when creator speaks.",
                        "attribution_text": "Free to use across monetized YouTube uploads."
                    },
                    {
                        "track_name": "Lurking Shadow",
                        "artist": "Silent Partner",
                        "duration": "2:15",
                        "mood": "Suspenseful / Dramatic Realization",
                        "tempo": "Slow Build (95 BPM)",
                        "genre": "Cinematic",
                        "license_type": "YouTube Audio Library (No attribution required)",
                        "official_url": "https://www.youtube.com/audiolibrary",
                        "search_query": "Lurking Shadow Silent Partner",
                        "scene_placement": "05:20 - 07:45 (iPadOS Flaws & Limitation Breakdown)",
                        "transition_notes": "Stripped down minimalist synth line allowing critical commentary to feel weighty.",
                        "attribution_text": "Free to use across monetized YouTube uploads."
                    },
                    {
                        "track_name": "Effortless",
                        "artist": "Dyalla",
                        "duration": "2:30",
                        "mood": "Uplifting Resolution / Clarity",
                        "tempo": "Upbeat (115 BPM)",
                        "genre": "Lo-Fi Soul",
                        "license_type": "YouTube Audio Library (No attribution required)",
                        "official_url": "https://www.youtube.com/audiolibrary",
                        "search_query": "Effortless Dyalla",
                        "scene_placement": "07:45 - 09:42 (Final Recommendation & End Screen)",
                        "transition_notes": "Warm Rhodes piano chords fading out smoothly on the final end card call to action.",
                        "attribution_text": "Free to use across monetized YouTube uploads."
                    }
                ],
                "sound_effects": [
                    {"time": "00:02", "name": "Deep Sub Bass Hit", "purpose": "Punctuates the opening hook question", "library_search": "Sub Boom Low Impact"},
                    {"time": "01:12", "name": "Mechanical UI Click", "purpose": "Snaps on-screen OLED brightness measurement", "library_search": "Camera Shutter Mechanical Click"},
                    {"time": "02:45", "name": "Digital Whoosh Transition", "purpose": "Pushes scene change from camera to benchmark graphic", "library_search": "Sci Fi Fast Whoosh Swish"},
                    {"time": "05:15", "name": "Vinyl Stop / Tape Brake", "purpose": "Emphasizes the transition into software flaws", "library_search": "Vinyl Tape Stop Slow"}
                ]
            }
        }
    },
    "viral_shorts": {
        "id": "demo-viral-shorts-02",
        "title": "3 Habits That Make You Look Instantly Richer (Under 60s)",
        "video_filename": "viral_habits_shorts_portrait.mp4",
        "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
        "duration": 54, # 54s
        "platform": "youtube_shorts",
        "niche": "Lifestyle & Self-Improvement",
        "audience": "Young professionals, students, Gen-Z creators",
        "language": "English",
        "region": "Global",
        "objective": "engagement",
        "context": "Fast-paced vertical short focusing on posture, speech cadence, and subtle style details.",
        "channel_name": "Peak Persona",
        "keywords": "habits, self improvement, psychology, appearance, charisma, shorts",
        "is_demo": True,
        "created_at": "2026-10-13T18:15:00Z",
        "checklist": [
            {"id": "s1", "text": "Replace opening speech with instant caption pop at frame 0", "completed": True, "priority": "high", "timestamp": "00:00"},
            {"id": "s2", "text": "Increase pacing speed from 140 WPM to 175 WPM on Habit #1", "completed": False, "priority": "high", "timestamp": "00:05 - 00:18"},
            {"id": "s3", "text": "Add bass drop pattern interrupt at the transition to Habit #2", "completed": True, "priority": "medium", "timestamp": "00:22"},
            {"id": "s4", "text": "Eliminate dead half-second silence before final looping sentence", "completed": False, "priority": "high", "timestamp": "00:52"}
        ],
        "analysis": {
            "summary": "Snappy vertical video with engaging eye-contact. The hook works decently well, but the final 4 seconds lack a seamless infinite-loop transition, which is critical for maximizing YouTube Shorts and TikTok loop counts.",
            "overall_score": 88,
            "score_breakdown": {
                "hook_strength": 91,
                "visual_pacing": 87,
                "story_structure": 84,
                "sound_design": 85,
                "seo_potential": 94
            },
            "score_rationale": "High-velocity short-form benchmark score evaluating millisecond hook latency, word-per-minute energy, and caption read speed.",
            "strengths": [
                "Immediate visual hook: high-contrast typography in top-third safe zone.",
                "Fast cutting: no shot lingers longer than 2.8 seconds.",
                "Clear audio recording with crisp high-end presence."
            ],
            "weaknesses": [
                "Slight energy dip between Habit 1 and Habit 2 (00:20 - 00:23).",
                "Outro gives an exit cue ('follow for part 2') rather than an endless loop trigger."
            ],
            "top_improvements": [
                "Re-record the closing sentence to seamlessly connect back into the opening hook phrase for infinite looping.",
                "Add subtle kinetic zoom punches on key words: 'Posture', 'Silence', and 'Fabric'.",
                "Switch caption font to high-visibility condensed sans-serif with electric lime highlight."
            ],
            "titles": [
                {
                    "category": "Curiosity-Driven",
                    "title": "3 Habits That Make You Look Instantly Richer 🧠 #Shorts",
                    "rationale": "High curiosity trigger for young aspirational audiences.",
                    "primary_keyword": "habits to look rich",
                    "score": 98
                },
                {
                    "category": "Benefit-Focused",
                    "title": "Do These 3 Things to 10x Your Charisma (In 60 Seconds)",
                    "rationale": "Clear quantifiable promise that can be consumed instantly.",
                    "primary_keyword": "improve charisma",
                    "score": 93
                },
                {
                    "category": "Short & Direct",
                    "title": "The Rich Person Habit No One Talks About",
                    "rationale": "Minimalist mystery that works across TikTok and Reels.",
                    "primary_keyword": "rich habits",
                    "score": 91
                },
                {
                    "category": "Storytelling",
                    "title": "I Studied 50 Billionaires: They All Share This One Trait",
                    "rationale": "Authority-backed narrative frame.",
                    "primary_keyword": "billionaire habits",
                    "score": 94
                },
                {
                    "category": "Platform & Audience Optimized",
                    "title": "Stop Doing This If You Want Respect. #selfimprovement",
                    "rationale": "Loss aversion command designed for aggressive algorithmic feed push.",
                    "primary_keyword": "gain respect psychology",
                    "score": 92
                }
            ],
            "description": {
                "opening": "3 subtle psychological habits that change how people perceive your status in under 10 seconds. Watch until the end for the loop trick.",
                "main_search_phrase": "habits to look high status",
                "summary": "Breakdown of vocal pacing, posture alignment, and clothing fabric contrast that signal quiet confidence without spending money.",
                "chapters": [],
                "cta": "Drop your favorite tip in the comments and subscribe for daily psychology hacks!",
                "hashtags": ["#Shorts", "#Psychology", "#SelfImprovement", "#LifeHacks", "#Charisma"],
                "credits": "Audio: YouTube Audio Library. Sound design edited for vertical mobile speakers."
            },
            "seo_package": {
                "primary_topic": "Charisma and Status Psychology Habits",
                "secondary_keywords": ["quiet luxury body language", "how to look confident", "psychology tricks for respect", "status signaling", "micro habits"],
                "search_intent": "Informational / Quick Self-Enhancement",
                "target_audience": "Gen-Z and Millennials (16-32) interested in personal growth",
                "suggested_tags": ["shorts", "psychology", "body language", "habits", "confidence", "status", "charisma", "rich mindset"],
                "suggested_filename": "3-habits-look-richer-vertical-hd.mp4",
                "pinned_comment": "Which one do you struggle with most: the 2-second pause or eye contact? Let me know below! 👇",
                "playlist_ideas": ["60-Second Psychology Hacks", "Body Language Mastery"],
                "end_screen_cards": []
            },
            "thumbnails": [
                {
                    "concept_name": "The High Status Posture",
                    "visual_description": "Clean split screen of creator demonstrating slouching (marked with red X) vs tall relaxed posture (marked with electric lime checkmark).",
                    "text_overlay": "STATUS TRICK",
                    "color_palette": "Electric Lime, Jet Black, Studio White",
                    "rationale": "Visual before-and-after instantly understood on vertical mobile screens.",
                    "image_prompt": "Split portrait photo, left side bad posture with red graphic, right side confident luxury posture with glowing lime graphic, studio lighting --ar 9:16"
                }
            ],
            "hook_lab": {
                "assessment": "The first 2.1 seconds deliver the hook cleanly with high speech energy. However, the first caption appears at 0.8s, creating a brief window of visual silence.",
                "original_opening": "If you want people to immediately treat you with more respect, here are 3 habits...",
                "potential_problem": "Slightly generic opening phrase heard across thousands of lifestyle shorts.",
                "opening_retention_grade": "A-",
                "alternative_hooks": [
                    {
                        "angle": "The Paradox Statement",
                        "script": "Rich people never say this one word, and poor people say it constantly.",
                        "visual": "Finger pointing directly down into the viewer's eyes with instant text flash.",
                        "on_screen_text": "THE 1 WORD TO NEVER SAY",
                        "pacing_notes": "Delivered in 2.2 seconds. Rapid tempo.",
                        "why_it_works": "Immediate polarizing comparison sparks instant defense and curiosity."
                    },
                    {
                        "angle": "The Unspoken Rule",
                        "script": "There is a silent test high-status people use in the first 5 seconds of meeting you.",
                        "visual": "Holding up a timer counting down from 00:05.",
                        "on_screen_text": "THE 5-SECOND TEST",
                        "pacing_notes": "Urgent cadence, ticking clock sound effect.",
                        "why_it_works": "Creates immediate personal stakes for social encounters."
                    }
                ],
                "recommended_edit_sequence": [
                    {"time": "00:00 - 00:02", "shot": "Dynamic zoom punch on creator's eyes + Whoosh SFX", "overlay": "THE 5-SECOND TEST"},
                    {"time": "00:02 - 00:15", "shot": "Habit 1: The 2-Second Pause Before Answering", "overlay": "HABIT 1: PAUSE"},
                    {"time": "00:15 - 00:32", "shot": "Habit 2: Shoulders Down & Eye Stillness", "overlay": "HABIT 2: STILLNESS"},
                    {"time": "00:32 - 00:50", "shot": "Habit 3: The Clothing Fabric Secret", "overlay": "HABIT 3: FABRICS"},
                    {"time": "00:50 - 00:54", "shot": "Loop connector: 'And that is why...'", "overlay": "TAP TO REPLAY"}
                ]
            },
            "retention_lab": {
                "disclaimer": "AI-predicted retention risks based on mobile scroll patterns. Connect YouTube Studio for live Shorts retention metrics.",
                "timeline_segments": [
                    {"start": 0, "end": 6, "label": "Opening Hook", "risk_level": "low", "drop_probability": "12%"},
                    {"start": 6, "end": 22, "label": "Habit 1: Vocal Pause", "risk_level": "low", "drop_probability": "14%"},
                    {"start": 22, "end": 26, "label": "Transition Gap", "risk_level": "high", "drop_probability": "38%"},
                    {"start": 26, "end": 44, "label": "Habit 2 & 3", "risk_level": "low", "drop_probability": "15%"},
                    {"start": 44, "end": 54, "label": "Outro & Loop", "risk_level": "medium", "drop_probability": "25%"}
                ],
                "retention_risks": [
                    {
                        "timestamp": "00:21 - 00:24",
                        "severity": "high",
                        "category": "Transition Drop",
                        "suspected_issue": "Saying 'Now moving on to number two' causes viewers to swipe away.",
                        "evidence": "Filler transitional phrasing kills vertical scrolling momentum.",
                        "suggested_edit": "Delete the transition words entirely. Cut straight from Habit 1 to: 'Number two: stillness.'",
                        "priority": 1
                    },
                    {
                        "timestamp": "00:50 - 00:54",
                        "severity": "medium",
                        "category": "Loop Break",
                        "suspected_issue": "Creator sighs and waves goodbye at 00:53.",
                        "evidence": "Visible goodbye gestures cue the user to swipe to the next short before the replay counts.",
                        "suggested_edit": "Cut the wave. End mid-sentence so the audio loops seamlessly into the opening line.",
                        "priority": 2
                    }
                ],
                "simulated_retention_curve": [
                    {"second": 0, "predicted_retention": 100, "measured_retention": 100},
                    {"second": 5, "predicted_retention": 92, "measured_retention": 90},
                    {"second": 15, "predicted_retention": 84, "measured_retention": 81},
                    {"second": 23, "predicted_retention": 68, "measured_retention": 62}, # dip at filler transition
                    {"second": 35, "predicted_retention": 64, "measured_retention": 60},
                    {"second": 48, "predicted_retention": 59, "measured_retention": 55},
                    {"second": 54, "predicted_retention": 52, "measured_retention": 48}
                ]
            },
            "sound_studio": {
                "overall_tone": "Crisp, fast, modern phonk / lo-fi drive",
                "bpm_range": "125 - 135 BPM",
                "dialogue_clarity_advice": "Boost speech at 3.5kHz for maximum clarity on iPhone speaker grilles.",
                "youtube_audio_library_recommendations": [
                    {
                        "track_name": "Book the Rental",
                        "artist": "Rico",
                        "duration": "1:45",
                        "mood": "Punchy / Confident Electronic Beat",
                        "tempo": "Fast (128 BPM)",
                        "genre": "Hip Hop & Rap",
                        "license_type": "YouTube Audio Library (No attribution required)",
                        "official_url": "https://www.youtube.com/audiolibrary",
                        "search_query": "Book the Rental Rico",
                        "scene_placement": "00:00 - 00:54 (Full Short Track)",
                        "transition_notes": "Loop drum kick continuously under vocal track at -18dB.",
                        "attribution_text": "Free to use for commercial YouTube uploads."
                    }
                ],
                "sound_effects": [
                    {"time": "00:00", "name": "Heavy Sub Thud", "purpose": "Opening audio impact hook", "library_search": "Sub Thud Bass Drop"},
                    {"time": "00:05", "name": "Kinetic Text Snap", "purpose": "Synchronized with on-screen word pop", "library_search": "Finger Snap Clean"},
                    {"time": "00:22", "name": "Quick Swoosh", "purpose": "Fast camera whip pan to habit 2", "library_search": "Fast Whip Whoosh"}
                ]
            }
        }
    }
}
