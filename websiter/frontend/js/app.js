/**
 * FramePilot AI — Main Application Controller
 * Redesigned for Sample 3: Dark Professional Video Analysis
 */

import { API } from './api.js';
import { showToast, copyToClipboard, formatSeconds, parseTimecode, escapeHtml } from './utils.js';
import { StudioVideoPlayer } from './components/videoPlayer.js';
import { RetentionChart } from './components/retentionChart.js';
import { WaveformVisualizer } from './components/waveform.js';

class FramePilotApp {
  constructor() {
    this.currentView = 'view-landing';
    this.currentTab = 'tab-overview';
    this.currentProject = null;
    this.projectsList = [];
    this.player = null;
    this.retentionChart = null;
    this.waveform = null;
    this.uploadedFile = null;
    this.uploadedFileProjectId = null;
  }

  async init() {
    this.bindNavigation();
    this.bindUploadForm();
    this.bindThumbnailActions();
    this.bindSettingsForm();
    this.bindModals();

    // Initialize Video Player & Visualizers
    this.player = new StudioVideoPlayer('studio-video-player', 'video-time-display');
    this.retentionChart = new RetentionChart('retention-chart-canvas', (sec) => {
      this.player.seek(sec);
      showToast(`Playback scrubbed to ${formatSeconds(sec)}`, 'success');
    });

    this.waveform = new WaveformVisualizer('sound-waveform-canvas', (sec) => {
      this.player.seek(sec);
      showToast(`Audio scrubbed to ${formatSeconds(sec)}`, 'success');
    });

    this.player.onTimeUpdate((cur, dur) => {
      if (this.currentTab === 'tab-sound' && this.waveform) {
        this.waveform.render(dur || 60, this.getSoundCues(), cur);
      }
    });

    // Check backend health & pre-load projects
    await this.refreshProjects();
    this.checkHealthStatus();

    // Set initial view from URL hash if available
    const hash = window.location.hash.replace('#', '');
    if (hash && document.getElementById(hash)) {
      this.switchView(hash);
    } else {
      this.switchView('view-landing');
    }
  }

  /* ── Navigation ────────────────────────────────────────────────────────── */
  bindNavigation() {
    // Topbar & Sidebar nav links
    document.querySelectorAll('[data-nav-target]').forEach(el => {
      el.addEventListener('click', (e) => {
        e.preventDefault();
        const target = el.getAttribute('data-nav-target');
        this.switchView(target);
      });
    });

    // Sub-tabs in Analysis Report
    document.querySelectorAll('[data-tab-target]').forEach(el => {
      el.addEventListener('click', (e) => {
        e.preventDefault();
        const target = el.getAttribute('data-tab-target');
        this.switchTab(target);
      });
    });

    // Logo click -> Landing
    const logo = document.getElementById('brand-logo');
    if (logo) {
      logo.addEventListener('click', () => this.switchView('view-landing'));
    }

    // Interactive timecode clicks across the entire document
    document.addEventListener('click', (e) => {
      const tcBtn = e.target.closest('[data-timecode]');
      if (tcBtn) {
        const tcStr = tcBtn.getAttribute('data-timecode');
        const sec = parseTimecode(tcStr);
        this.player.seek(sec);
        showToast(`Jumped to ${formatSeconds(sec)}`, 'success');
      }
    });
  }

  switchView(viewId) {
    document.querySelectorAll('.view-container').forEach(el => el.classList.add('hidden'));
    const target = document.getElementById(viewId);
    if (target) {
      target.classList.remove('hidden');
      this.currentView = viewId;
      window.location.hash = viewId;
    }

    // Update active nav button state
    document.querySelectorAll('[data-nav-target]').forEach(el => {
      if (el.getAttribute('data-nav-target') === viewId) {
        el.classList.add('active');
      } else {
        el.classList.remove('active');
      }
    });

    // Special view triggers
    if (viewId === 'view-dashboard') {
      this.renderDashboard();
    } else if (viewId === 'view-projects') {
      this.renderProjectsList();
    } else if (viewId === 'view-settings') {
      this.loadSettings();
    }
  }

  switchTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
    const target = document.getElementById(tabId);
    if (target) {
      target.classList.remove('hidden');
      this.currentTab = tabId;
    }

    document.querySelectorAll('[data-tab-target]').forEach(el => {
      if (el.getAttribute('data-tab-target') === tabId) {
        el.classList.add('active');
      } else {
        el.classList.remove('active');
      }
    });

    // Refresh charts if entering their respective tabs
    if (tabId === 'tab-retention' && this.currentProject) {
      const curve = this.currentProject.analysis?.retention_lab?.simulated_retention_curve;
      setTimeout(() => this.retentionChart.render(curve), 50);
    } else if (tabId === 'tab-sound' && this.currentProject) {
      setTimeout(() => {
        const cues = this.getSoundCues();
        this.waveform.render(this.currentProject.duration || 60, cues, this.player.video?.currentTime || 0);
      }, 50);
    }
  }

  /* ── Video Upload & Stream Analysis ────────────────────────────────────── */
  bindUploadForm() {
    const dropzone = document.getElementById('upload-dropzone');
    const fileInput = document.getElementById('video-file-input');
    const form = document.getElementById('analysis-form');

    if (!dropzone || !fileInput) return;

    ['dragenter', 'dragover'].forEach(name => {
      dropzone.addEventListener(name, (e) => {
        e.preventDefault();
        dropzone.classList.add('border-[#4F8CFF]', 'bg-[#111F32]');
      });
    });

    ['dragleave', 'drop'].forEach(name => {
      dropzone.addEventListener(name, (e) => {
        e.preventDefault();
        dropzone.classList.remove('border-[#4F8CFF]', 'bg-[#111F32]');
      });
    });

    dropzone.addEventListener('drop', (e) => {
      if (e.dataTransfer.files && e.dataTransfer.files[0]) {
        this.handleFileSelected(e.dataTransfer.files[0]);
      }
    });

    fileInput.addEventListener('change', () => {
      if (fileInput.files && fileInput.files[0]) {
        this.handleFileSelected(fileInput.files[0]);
      }
    });

    // Remove selected file button
    const removeBtn = document.getElementById('btn-remove-file');
    if (removeBtn) {
      removeBtn.addEventListener('click', (e) => {
        e.preventDefault();
        this.uploadedFile = null;
        fileInput.value = '';
        document.getElementById('upload-idle-state').classList.remove('hidden');
        document.getElementById('upload-file-details').classList.add('hidden');
      });
    }

    // Submit Analysis
    if (form) {
      form.addEventListener('submit', async (e) => {
        e.preventDefault();
        await this.startAnalysisStream(form);
      });
    }

    // Demo Mode buttons on upload & landing pages
    document.querySelectorAll('[data-load-demo]').forEach(btn => {
      btn.addEventListener('click', async (e) => {
        e.preventDefault();
        const demoKey = btn.getAttribute('data-load-demo') || 'tech_review';
        showToast('Loading reference analysis...', 'success');
        try {
          const proj = await API.createDemoProject(demoKey);
          await this.openProject(proj.id);
        } catch (err) {
          showToast(err.message, 'error');
        }
      });
    });
  }

  handleFileSelected(file) {
    this.uploadedFile = file;
    const details = document.getElementById('upload-file-details');
    const idle = document.getElementById('upload-idle-state');
    
    document.getElementById('selected-filename').innerText = file.name;
    document.getElementById('selected-filesize').innerText = `${(file.size / (1024 * 1024)).toFixed(1)} MB`;

    // Attempt HTML5 video probe for duration
    const tempUrl = URL.createObjectURL(file);
    const probeVideo = document.createElement('video');
    probeVideo.preload = 'metadata';
    probeVideo.src = tempUrl;
    probeVideo.onloadedmetadata = () => {
      document.getElementById('selected-duration').innerText = formatSeconds(probeVideo.duration);
      document.getElementById('form-duration-input').value = Math.round(probeVideo.duration);
      URL.revokeObjectURL(tempUrl);
    };

    idle.classList.add('hidden');
    details.classList.remove('hidden');
  }

  bindThumbnailActions() {
    const button = document.getElementById('btn-generate-thumbnails');
    if (!button) return;

    button.addEventListener('click', async () => {
      if (!this.currentProject || !this.uploadedFile || this.uploadedFileProjectId !== this.currentProject.id) {
        showToast('Generate thumbnails immediately after analyzing a video in this session.', 'error');
        return;
      }

      button.disabled = true;
      try {
        await this.generateThumbnailImages(
          this.currentProject.id,
          this.currentProject.analysis,
          this.uploadedFile
        );
      } catch (error) {
        showToast(`Could not generate thumbnails: ${error.message}`, 'error');
      } finally {
        button.disabled = false;
      }
    });
  }

  async startAnalysisStream(form) {
    const formData = new FormData(form);
    if (this.uploadedFile) {
      formData.set('video', this.uploadedFile);
    }

    // Open progress modal
    const modal = document.getElementById('modal-analysis-progress');
    modal.classList.remove('hidden');

    const labelEl = document.getElementById('progress-step-label');
    const barEl = document.getElementById('progress-bar-fill');
    const pctEl = document.getElementById('progress-percent-text');

    if (labelEl) labelEl.innerText = 'Uploading video...';
    if (barEl) barEl.style.width = '0%';
    if (pctEl) pctEl.innerText = '0%';

    await API.streamAnalysis(formData, {
      onUploadProgress: (progress) => {
        const percent = Math.round(progress.percent * 0.1);
        if (labelEl) labelEl.innerText = `Uploading video... ${progress.percent}%`;
        if (barEl) barEl.style.width = `${percent}%`;
        if (pctEl) pctEl.innerText = `${percent}%`;
      },
      onProgress: (p) => {
        if (labelEl) labelEl.innerText = p.label;
        if (barEl) barEl.style.width = `${p.percent}%`;
        if (pctEl) pctEl.innerText = `${p.percent}%`;
      },
      onComplete: async (data) => {
        modal.classList.add('hidden');
        this.uploadedFileProjectId = data.project_id;
        if (this.uploadedFile && data.project?.analysis) {
          try {
            await this.generateThumbnailImages(data.project_id, data.project.analysis, this.uploadedFile);
          } catch (error) {
            showToast(`Analysis finished, but thumbnail generation failed: ${error.message}`, 'error');
          }
        }
        showToast('Analysis complete! Opening workspace...', 'success');
        await this.refreshProjects();
        await this.openProject(data.project_id);
      },
      onError: (err) => {
        modal.classList.add('hidden');
        showToast(`Analysis error: ${err}`, 'error');
      }
    });
  }

  /* ── Project Workspace Rendering ───────────────────────────────────────── */
  async openProject(projectId) {
    try {
      const proj = await API.getProject(projectId);
      this.currentProject = proj;
      this.renderProjectWorkspace(proj);
      this.switchView('view-report');
      this.switchTab('tab-overview');
    } catch (err) {
      showToast(err.message, 'error');
    }
  }

  renderProjectWorkspace(proj) {
    const a = proj.analysis || {};
    
    // Header Info
    document.getElementById('report-project-title').innerText = proj.title || 'Untitled Video';
    document.getElementById('report-platform-badge').innerText = (proj.platform || 'YouTube').replace('_', ' ').toUpperCase();
    document.getElementById('report-niche-badge').innerText = proj.niche || 'General';
    document.getElementById('report-score-pill').innerText = `${a.overall_score || 85} / 100`;

    // Demo Mode notice
    const demoBanner = document.getElementById('report-demo-banner');
    if (demoBanner) {
      if (proj.is_demo || a.api_note) {
        demoBanner.classList.remove('hidden');
        document.getElementById('report-demo-note').innerText = a.api_note || 'Reference Analysis (Demo Dataset)';
      } else {
        demoBanner.classList.add('hidden');
      }
    }

    // Video Source
    const videoSrc = proj.video_url || 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4';
    this.player.loadSource(videoSrc);

    // 1. Overview Tab
    document.getElementById('overview-summary-text').innerText = a.summary || '';
    document.getElementById('overview-score-big').innerText = a.overall_score || 85;
    document.getElementById('overview-score-rationale').innerText = a.score_rationale || '';

    // Score Breakdown
    const b = a.score_breakdown || {};
    const breakdownContainer = document.getElementById('overview-breakdown-bars');
    if (breakdownContainer) {
      breakdownContainer.innerHTML = Object.entries(b).map(([k, val]) => `
        <div>
          <div class="flex justify-between text-xs text-[#93A4BA] mb-1.5 font-medium">
            <span>${k.replace('_', ' ').toUpperCase()}</span>
            <span class="font-mono text-[#F1F5F9]">${val}%</span>
          </div>
          <div class="h-1.5 w-full bg-[#111F32] rounded-full overflow-hidden border border-[#1D2E45]">
            <div class="h-full bg-[#4F8CFF] rounded-full" style="width: ${val}%"></div>
          </div>
        </div>
      `).join('');
    }

    // Strengths, Weaknesses, Improvements
    const renderList = (id, items, markerClass) => {
      const el = document.getElementById(id);
      if (!el) return;
      el.innerHTML = (items || []).map(item => `
        <li class="flex items-start gap-2.5 text-xs text-[#F1F5F9] leading-relaxed">
          <span class="${markerClass} mt-0.5 shrink-0">●</span>
          <span>${escapeHtml(item)}</span>
        </li>
      `).join('');
    };

    renderList('overview-strengths-list', a.strengths, 'text-[#38E1A0]');
    renderList('overview-weaknesses-list', a.weaknesses, 'text-[#FF5A65]');
    renderList('overview-improvements-list', a.top_improvements, 'text-[#4F8CFF]');

    // 2. Titles & SEO Tab
    this.renderTitles(a.titles || []);
    this.renderDescription(a.description || {});
    this.renderSeoPackage(a.seo_package || {});

    // 3. Hook Lab Tab
    this.renderHookLab(a.hook_lab || {});

    // 4. Retention Lab Tab
    this.renderRetentionLab(a.retention_lab || {});

    // 5. Sound Studio Tab
    this.renderSoundStudio(a.sound_studio || {});

    // 6. Thumbnails Tab
    this.renderThumbnails(a.thumbnails || []);

    // 7. Action Plan Checklist
    this.renderChecklist(proj.checklist || []);

    // Export buttons binding
    this.bindExportActions(proj.id);
  }

  /* ── Tab Renderers ─────────────────────────────────────────────────────── */
  renderTitles(titles) {
    const container = document.getElementById('seo-titles-container');
    if (!container) return;

    container.innerHTML = titles.map((t, idx) => `
      <div class="panel p-4 hover:border-[#243B59] transition flex flex-col justify-between">
        <div>
          <div class="flex items-center justify-between gap-3 mb-2.5">
            <div class="flex items-center gap-2">
              <span class="status-chip status-chip-accent font-medium">
                ${escapeHtml(t.category)}
              </span>
              <span class="font-mono text-xs text-[#93A4BA] font-medium">
                Score: <strong class="text-[#F1F5F9]">${t.score}</strong>/100
              </span>
            </div>
            <button class="btn-copy-title btn-secondary px-2.5 py-1 text-xs" data-copy="${escapeHtml(t.title)}">
              <svg class="w-3.5 h-3.5 text-[#93A4BA]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/></svg>
              <span>Copy</span>
            </button>
          </div>
          <h4 class="text-sm font-semibold text-[#F1F5F9] mb-1.5 leading-snug">${escapeHtml(t.title)}</h4>
          <p class="text-xs text-[#93A4BA] leading-relaxed mb-3">${escapeHtml(t.rationale)}</p>
        </div>
        <div class="pt-2 border-t border-[#1D2E45] text-[11px] font-mono text-[#62768F]">
          Target Keyword: <span class="text-[#F1F5F9] font-sans font-medium">${escapeHtml(t.primary_keyword)}</span>
        </div>
      </div>
    `).join('');

    container.querySelectorAll('.btn-copy-title').forEach(b => {
      b.addEventListener('click', () => copyToClipboard(b.getAttribute('data-copy'), 'Title copied to clipboard!'));
    });

    // Regenerate Titles Button
    const regenBtn = document.getElementById('btn-regen-titles');
    if (regenBtn) {
      regenBtn.onclick = async () => {
        showToast('Refreshing title variations...', 'success');
        try {
          const res = await API.regenerateSection(this.currentProject.id, 'titles');
          this.currentProject.analysis.titles = res.data;
          this.renderTitles(res.data);
          showToast('Titles regenerated successfully!', 'success');
        } catch (e) {
          showToast(e.message, 'error');
        }
      };
    }
  }

  renderDescription(desc) {
    const textEl = document.getElementById('seo-description-text');
    if (!textEl) return;

    let fullDesc = `${desc.opening || ''}\n\n${desc.summary || ''}\n\n`;
    if (desc.chapters && desc.chapters.length > 0) {
      fullDesc += 'TIMESTAMPS:\n';
      desc.chapters.forEach(c => {
        fullDesc += `${c.timestamp} - ${c.title}\n`;
      });
      fullDesc += '\n';
    }
    if (desc.cta) fullDesc += `${desc.cta}\n\n`;
    if (desc.hashtags) fullDesc += `${desc.hashtags.join(' ')}\n\n`;
    if (desc.credits) fullDesc += `${desc.credits}\n`;

    textEl.value = fullDesc.trim();

    const copyBtn = document.getElementById('btn-copy-description');
    if (copyBtn) {
      copyBtn.onclick = () => copyToClipboard(textEl.value, 'Full description copied ready to paste in YouTube Studio!');
    }
  }

  renderSeoPackage(pkg) {
    document.getElementById('seo-primary-topic').innerText = pkg.primary_topic || 'N/A';
    document.getElementById('seo-search-intent').innerText = pkg.search_intent || 'N/A';
    document.getElementById('seo-filename').innerText = pkg.suggested_filename || 'video-final-render.mp4';
    document.getElementById('seo-pinned-comment').innerText = pkg.pinned_comment || '';

    // Secondary Keywords Pills
    const kwContainer = document.getElementById('seo-secondary-keywords');
    if (kwContainer) {
      kwContainer.innerHTML = (pkg.secondary_keywords || []).map(kw => `
        <span class="status-chip status-chip-accent">${escapeHtml(kw)}</span>
      `).join('');
    }

    // Tags
    const tagsContainer = document.getElementById('seo-tags-pills');
    if (tagsContainer) {
      tagsContainer.innerHTML = (pkg.suggested_tags || []).map(tag => `
        <span class="px-2 py-0.5 rounded bg-[#07111F] border border-[#1D2E45] text-xs font-mono text-[#93A4BA]">${escapeHtml(tag)}</span>
      `).join('');
    }

    const copyTagsBtn = document.getElementById('btn-copy-tags');
    if (copyTagsBtn) {
      copyTagsBtn.onclick = () => copyToClipboard((pkg.suggested_tags || []).join(', '), 'Tags copied as comma-separated list!');
    }
  }

  renderHookLab(hook) {
    document.getElementById('hook-grade-badge').innerText = `GRADE: ${hook.opening_retention_grade || 'B+'}`;
    document.getElementById('hook-critique-text').innerText = hook.assessment || '';
    document.getElementById('hook-original-text').innerText = hook.original_opening || 'No opening speech detected.';
    document.getElementById('hook-problem-text').innerText = hook.potential_problem || 'Opening communicates slowly.';

    // Alternative Hooks
    const altContainer = document.getElementById('hook-alternatives-container');
    if (altContainer) {
      altContainer.innerHTML = (hook.alternative_hooks || []).map((h, idx) => `
        <div class="panel p-5 border-l-2 border-l-[#4F8CFF]">
          <div class="flex items-center justify-between mb-2.5">
            <span class="status-chip status-chip-accent font-semibold">${escapeHtml(h.angle)}</span>
            <button class="btn-copy-hook btn-secondary px-2.5 py-1 text-xs" data-copy="${escapeHtml(h.script)}">
              Copy Script
            </button>
          </div>
          <p class="text-sm text-[#F1F5F9] font-medium mb-3 italic leading-relaxed">"${escapeHtml(h.script)}"</p>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs text-[#93A4BA] bg-[#07111F] p-3 rounded-md border border-[#1D2E45]">
            <div><span class="text-[#F1F5F9] font-medium">Visual Shot:</span> ${escapeHtml(h.visual)}</div>
            <div><span class="text-[#F1F5F9] font-medium">On-Screen Text:</span> <span class="font-mono text-[#4F8CFF]">${escapeHtml(h.on_screen_text)}</span></div>
            <div><span class="text-[#F1F5F9] font-medium">Pacing:</span> ${escapeHtml(h.pacing_notes)}</div>
            <div><span class="text-[#F1F5F9] font-medium">Psychological Trigger:</span> ${escapeHtml(h.why_it_works)}</div>
          </div>
        </div>
      `).join('');

      altContainer.querySelectorAll('.btn-copy-hook').forEach(b => {
        b.onclick = () => copyToClipboard(b.getAttribute('data-copy'), 'Hook script copied!');
      });
    }

    // Edit Sequence
    const seqContainer = document.getElementById('hook-sequence-list');
    if (seqContainer) {
      seqContainer.innerHTML = (hook.recommended_edit_sequence || []).map(seq => `
        <div class="flex items-center gap-3 p-2.5 rounded-md bg-[#07111F] border border-[#1D2E45]">
          <button class="timecode-pill" data-timecode="${escapeHtml(seq.time)}">
            ${escapeHtml(seq.time)}
          </button>
          <div class="text-xs text-[#F1F5F9] flex-1">${escapeHtml(seq.shot)}</div>
          ${seq.overlay ? `<span class="text-[11px] font-mono px-2 py-0.5 rounded bg-[#4F8CFF]/10 text-[#4F8CFF] border border-[#4F8CFF]/25">OVERLAY: ${escapeHtml(seq.overlay)}</span>` : ''}
        </div>
      `).join('');
    }
  }

  renderRetentionLab(retention) {
    // Segments Track
    const track = document.getElementById('retention-segments-track');
    const segs = retention.timeline_segments || [];
    const totalDuration = this.currentProject?.duration || 100;

    if (track && segs.length > 0) {
      track.innerHTML = segs.map(seg => {
        const leftPct = (seg.start / totalDuration) * 100;
        const widthPct = ((seg.end - seg.start) / totalDuration) * 100;
        const riskClass = `risk-${seg.risk_level || 'low'}`;
        return `
          <div class="timeline-block ${riskClass}"
               style="left: ${leftPct}%; width: ${Math.max(2, widthPct)}%;"
               title="${escapeHtml(seg.label)} (${seg.drop_probability} drop risk)"
               data-timecode="${seg.start}">
            <span class="truncate px-1">${escapeHtml(seg.label)}</span>
          </div>
        `;
      }).join('');
    }

    // Retention Risks Cards
    const risksContainer = document.getElementById('retention-risks-container');
    if (risksContainer) {
      risksContainer.innerHTML = (retention.retention_risks || []).map(r => {
        const chipClass = r.severity === 'high' ? 'status-chip-danger' : (r.severity === 'medium' ? 'status-chip-warning' : 'status-chip-positive');
        const startSec = parseTimecode(r.timestamp);
        return `
          <div class="panel p-4 transition" data-timestamp-start="${startSec}">
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center gap-2">
                <button class="timecode-pill" data-timecode="${escapeHtml(r.timestamp)}">
                  ${escapeHtml(r.timestamp)}
                </button>
                <span class="status-chip ${chipClass} uppercase font-mono font-semibold">
                  ${r.severity} Risk
                </span>
              </div>
              <span class="text-xs text-[#93A4BA] font-medium">${escapeHtml(r.category)}</span>
            </div>
            <h5 class="text-sm font-semibold text-[#F1F5F9] mb-1">${escapeHtml(r.suspected_issue)}</h5>
            <p class="text-xs text-[#93A4BA] mb-2.5"><span class="text-[#F1F5F9] font-medium">Evidence:</span> ${escapeHtml(r.evidence)}</p>
            <div class="text-xs bg-[#07111F] p-3 rounded-md border border-[#1D2E45] text-[#F1F5F9]">
              <span class="font-semibold text-[#4F8CFF]">Actionable Edit:</span> ${escapeHtml(r.suggested_edit)}
            </div>
          </div>
        `;
      }).join('');
    }

    // Retention Curve Chart
    this.retentionChart.render(retention.simulated_retention_curve);

    // YouTube Connect & Upload Modal bindings
    const ytBtn = document.getElementById('btn-connect-youtube-oauth');
    if (ytBtn) {
      ytBtn.onclick = async () => {
        try {
          const details = await API.getYouTubeOAuthDetails();
          showToast(details.disclosure, 'error');
        } catch (err) {
          showToast(`Could not check YouTube integration: ${err.message}`, 'error');
        }
      };
    }

    const uploadRetentionBtn = document.getElementById('btn-upload-retention-csv');
    if (uploadRetentionBtn) {
      uploadRetentionBtn.onclick = () => {
        document.getElementById('modal-retention-upload').classList.remove('hidden');
      };
    }
  }

  renderSoundStudio(sound) {
    document.getElementById('sound-tone-text').innerText = sound.overall_tone || 'Analytical tech commentary';
    document.getElementById('sound-bpm-text').innerText = sound.bpm_range || '110 - 120 BPM';
    document.getElementById('sound-dialogue-advice').innerText = sound.dialogue_clarity_advice || '';

    // YouTube Audio Library Tracks
    const tracksContainer = document.getElementById('sound-tracks-container');
    if (tracksContainer) {
      tracksContainer.innerHTML = (sound.youtube_audio_library_recommendations || []).map(t => `
        <div class="panel p-4 flex flex-col justify-between">
          <div>
            <div class="flex items-start justify-between gap-3 mb-2">
              <div>
                <h5 class="text-sm font-semibold text-[#F1F5F9]">${escapeHtml(t.track_name)} <span class="text-xs font-normal text-[#93A4BA]">by ${escapeHtml(t.artist)}</span></h5>
                <div class="flex items-center gap-2 mt-1">
                  <span class="status-chip status-chip-accent font-mono">${escapeHtml(t.duration)}</span>
                  <span class="text-xs text-[#93A4BA]">${escapeHtml(t.mood)}</span>
                </div>
              </div>
              <a href="${t.official_url}?search=${encodeURIComponent(t.search_query)}" target="_blank" rel="noopener noreferrer"
                 class="btn-primary text-xs px-2.5 py-1 shrink-0">
                <span>Find in Library</span>
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
              </a>
            </div>
            <div class="text-xs text-[#93A4BA] space-y-1 mt-3 bg-[#07111F] p-3 rounded-md border border-[#1D2E45]">
              <div><span class="text-[#F1F5F9] font-medium">Placement:</span> ${escapeHtml(t.scene_placement)}</div>
              <div><span class="text-[#F1F5F9] font-medium">Transition:</span> ${escapeHtml(t.transition_notes)}</div>
              <div class="text-[11px] text-[#62768F] pt-1 border-t border-[#1D2E45]">${escapeHtml(t.attribution_text)}</div>
            </div>
          </div>
        </div>
      `).join('');
    }

    // SFX
    const sfxContainer = document.getElementById('sound-sfx-container');
    if (sfxContainer) {
      sfxContainer.innerHTML = (sound.sound_effects || []).map(s => `
        <div class="flex items-center justify-between p-2.5 rounded-md bg-[#07111F] border border-[#1D2E45]">
          <div class="flex items-center gap-3">
            <button class="timecode-pill" data-timecode="${escapeHtml(s.time)}">
              ${escapeHtml(s.time)}
            </button>
            <span class="text-xs font-semibold text-[#F1F5F9]">${escapeHtml(s.name)}</span>
          </div>
          <span class="text-xs text-[#93A4BA]">${escapeHtml(s.purpose)}</span>
        </div>
      `).join('');
    }

    // Render Waveform Canvas
    setTimeout(() => {
      const cues = this.getSoundCues();
      this.waveform.render(this.currentProject?.duration || 60, cues, this.player.video?.currentTime || 0);
    }, 50);
  }

  getSoundCues() {
    const sound = this.currentProject?.analysis?.sound_studio || {};
    const cues = [];
    (sound.sound_effects || []).forEach(s => {
      cues.push({ time: parseTimecode(s.time), label: s.name });
    });
    return cues;
  }

  async generateThumbnailImages(projectId, analysis, videoFile) {
    const thumbnails = (analysis?.thumbnails || []).slice(0, 2);
    if (thumbnails.length < 2) throw new Error('The analysis has fewer than two thumbnail concepts.');

    const video = document.createElement('video');
    const objectUrl = URL.createObjectURL(videoFile);
    video.muted = true;
    video.playsInline = true;
    video.preload = 'auto';

    try {
      await new Promise((resolve, reject) => {
        const timeout = setTimeout(() => reject(new Error('The video could not be opened in the browser.')), 15000);
        video.addEventListener('loadedmetadata', () => { clearTimeout(timeout); resolve(); }, { once: true });
        video.addEventListener('error', () => { clearTimeout(timeout); reject(new Error('This browser could not decode the video.')); }, { once: true });
        video.src = objectUrl;
        video.load();
      });

      if (!video.videoWidth || !video.videoHeight || !Number.isFinite(video.duration)) {
        throw new Error('The uploaded video does not contain readable frames.');
      }

      for (const [index, thumbnail] of thumbnails.entries()) {
        const frameTime = Math.max(0, Math.min(video.duration - 0.05, video.duration * (index === 0 ? 0.24 : 0.64)));
        if (Math.abs(video.currentTime - frameTime) > 0.01) {
          await new Promise((resolve, reject) => {
            const timeout = setTimeout(() => reject(new Error('Timed out reading a video frame.')), 10000);
            video.addEventListener('seeked', () => { clearTimeout(timeout); resolve(); }, { once: true });
            video.currentTime = frameTime;
          });
        }

        const canvas = document.createElement('canvas');
        canvas.width = 1280;
        canvas.height = 720;
        const context = canvas.getContext('2d');
        if (!context) throw new Error('Canvas image generation is unavailable.');

        const scale = Math.max(canvas.width / video.videoWidth, canvas.height / video.videoHeight);
        const sourceWidth = canvas.width / scale;
        const sourceHeight = canvas.height / scale;
        context.drawImage(
          video,
          (video.videoWidth - sourceWidth) / 2,
          (video.videoHeight - sourceHeight) / 2,
          sourceWidth,
          sourceHeight,
          0,
          0,
          canvas.width,
          canvas.height
        );

        const shade = context.createLinearGradient(0, 300, 0, canvas.height);
        shade.addColorStop(0, 'rgba(3, 7, 10, 0.02)');
        shade.addColorStop(0.42, 'rgba(3, 7, 10, 0.42)');
        shade.addColorStop(1, 'rgba(3, 7, 10, 0.94)');
        context.fillStyle = shade;
        context.fillRect(0, 0, canvas.width, canvas.height);

        const accent = index === 0 ? '#CCFF00' : '#00F0FF';
        context.fillStyle = 'rgba(3, 7, 10, 0.75)';
        context.fillRect(64, 52, 330, 42);
        context.font = '700 20px Arial, sans-serif';
        context.fillStyle = accent;
        context.fillText(`VIDEO THUMBNAIL 0${index + 1}`, 82, 80);

        const headline = String(thumbnail.text_overlay || thumbnail.concept_name || 'WATCH THIS')
          .replace(/\s+/g, ' ').trim().toUpperCase().slice(0, 42);
        const words = headline.split(' ');
        let fontSize = 86;
        let lines = [];
        while (fontSize >= 54) {
          context.font = `900 ${fontSize}px Arial, sans-serif`;
          lines = [''];
          for (const word of words) {
            const lineIndex = lines.length - 1;
            const candidate = `${lines[lineIndex]} ${word}`.trim();
            if (context.measureText(candidate).width <= 1120) lines[lineIndex] = candidate;
            else if (lines.length < 2) lines.push(word);
            else break;
          }
          if (lines.length <= 2 && lines.every(line => context.measureText(line).width <= 1120)) break;
          fontSize -= 4;
        }
        lines = lines.slice(0, 2);
        const lineHeight = fontSize * 1.05;
        const firstLineY = 610 - (lines.length - 1) * lineHeight;
        context.fillStyle = accent;
        context.fillRect(72, firstLineY - fontSize - 28, 112, 10);
        context.font = `900 ${fontSize}px Arial, sans-serif`;
        context.textBaseline = 'alphabetic';
        context.lineJoin = 'round';
        context.lineWidth = 12;
        context.strokeStyle = 'rgba(0, 0, 0, 0.88)';
        context.fillStyle = '#FFFFFF';
        lines.forEach((line, lineIndex) => {
          const y = firstLineY + lineIndex * lineHeight;
          context.strokeText(line, 72, y, 1120);
          context.fillText(line, 72, y, 1120);
        });
        context.font = '600 21px Arial, sans-serif';
        context.fillStyle = '#E2E8F0';
        context.fillText(String(thumbnail.concept_name || 'Video insight').toUpperCase().slice(0, 54), 76, 680, 1120);
        thumbnail.image_data_url = canvas.toDataURL('image/jpeg', 0.9);
      }

      const updatedProject = await API.patchProject(projectId, { analysis });
      this.uploadedFileProjectId = projectId;
      if (this.currentProject?.id === projectId) {
        this.currentProject = updatedProject;
        this.renderThumbnails(updatedProject.analysis.thumbnails || []);
      }
      showToast('Two video thumbnails generated and saved.', 'success');
    } finally {
      video.pause();
      video.removeAttribute('src');
      video.load();
      URL.revokeObjectURL(objectUrl);
    }
  }

  renderThumbnails(thumbs) {
    const container = document.getElementById('thumbnails-container');
    if (!container) return;

    const selectedThumbnails = thumbs.slice(0, 2);
    const generateButton = document.getElementById('btn-generate-thumbnails');
    const canGenerate = Boolean(
      this.currentProject &&
      this.uploadedFile &&
      this.uploadedFileProjectId === this.currentProject.id
    );
    if (generateButton) {
      generateButton.disabled = !canGenerate;
      generateButton.textContent = selectedThumbnails.some(thumbnail => thumbnail.image_data_url)
        ? 'Regenerate 2 Thumbnails'
        : 'Generate 2 Thumbnails';
      generateButton.title = canGenerate
        ? 'Create two new images from frames in the uploaded video'
        : 'Generate thumbnails immediately after analyzing a video in this session';
    }

    container.innerHTML = selectedThumbnails.map((th, idx) => `
      <div class="panel p-5 flex flex-col justify-between">
        <div>
          <div class="aspect-video w-full rounded-md bg-[#07111F] border border-[#1D2E45] relative overflow-hidden mb-4">
            ${th.image_data_url
              ? `<img class="w-full h-full object-cover" src="${escapeHtml(th.image_data_url)}" alt="Generated thumbnail: ${escapeHtml(th.concept_name)}">`
              : `<div class="absolute inset-0 flex items-center justify-center p-4 text-center"><span class="text-lg font-bold text-white uppercase font-mono">${escapeHtml(th.text_overlay || th.concept_name)}</span></div>`}
            <div class="absolute top-2 right-2 text-[10px] font-mono px-2 py-0.5 rounded bg-[#4F8CFF]/15 text-[#4F8CFF] border border-[#4F8CFF]/30">
              THUMBNAIL #${idx + 1}
            </div>
          </div>
          <h4 class="text-sm font-semibold text-[#F1F5F9] mb-1.5">${escapeHtml(th.concept_name)}</h4>
          <p class="text-xs text-[#93A4BA] leading-relaxed mb-3">${escapeHtml(th.visual_description)}</p>
          <div class="text-xs text-[#62768F] mb-3">Rationale: <span class="text-[#F1F5F9]">${escapeHtml(th.rationale)}</span></div>
        </div>
        <div class="pt-3 border-t border-[#1D2E45]">
          <div class="text-[11px] font-mono text-[#93A4BA] mb-1.5">AI Image Generation Prompt:</div>
          <div class="text-xs font-mono bg-[#07111F] p-2.5 rounded-md border border-[#1D2E45] text-[#93A4BA] mb-3 line-clamp-3">
            ${escapeHtml(th.image_prompt)}
          </div>
          ${th.image_data_url
            ? `<a class="btn-primary block py-1.5 text-xs font-semibold text-center mb-2" href="${escapeHtml(th.image_data_url)}" download="framepilot-thumbnail-${idx + 1}.jpg">Download JPEG</a>`
            : ''}
          <button class="btn-copy-prompt btn-secondary w-full py-1.5 text-xs font-medium" data-copy="${escapeHtml(th.image_prompt)}">
            <svg class="w-3.5 h-3.5 text-[#93A4BA]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/></svg>
            <span>Copy Image Prompt</span>
          </button>
        </div>
      </div>
    `).join('');

    container.querySelectorAll('.btn-copy-prompt').forEach(b => {
      b.onclick = () => copyToClipboard(b.getAttribute('data-copy'), 'Image prompt copied!');
    });
  }

  renderChecklist(checklist) {
    const container = document.getElementById('action-plan-checklist');
    if (!container) return;

    const completedCount = checklist.filter(c => c.completed).length;
    const totalCount = checklist.length;
    const pct = totalCount > 0 ? Math.round((completedCount / totalCount) * 100) : 0;

    document.getElementById('checklist-progress-text').innerText = `${completedCount} of ${totalCount} completed (${pct}%)`;
    document.getElementById('checklist-progress-bar').style.width = `${pct}%`;

    container.innerHTML = checklist.map(item => `
      <label class="flex items-start gap-3 p-3.5 rounded-md bg-[#07111F] border border-[#1D2E45] hover:border-[#243B59] cursor-pointer transition">
        <input type="checkbox" class="chk-item mt-1 rounded bg-[#0D1929] border-[#243B59] text-[#4F8CFF] focus:ring-[#4F8CFF]"
               data-item-id="${item.id}" ${item.completed ? 'checked' : ''}>
        <div class="flex-1 text-xs ${item.completed ? 'line-through text-[#62768F]' : 'text-[#F1F5F9]'}">
          <div class="flex items-center gap-2 mb-1">
            ${item.timestamp ? `<button type="button" class="timecode-pill" data-timecode="${escapeHtml(item.timestamp)}">${escapeHtml(item.timestamp)}</button>` : ''}
            <span class="status-chip ${item.priority === 'high' ? 'status-chip-danger' : 'status-chip-warning'} uppercase font-mono text-[10px]">${item.priority}</span>
          </div>
          <span>${escapeHtml(item.text)}</span>
        </div>
      </label>
    `).join('');

    container.querySelectorAll('.chk-item').forEach(chk => {
      chk.addEventListener('change', async () => {
        const itemId = chk.getAttribute('data-item-id');
        await API.updateChecklistItem(this.currentProject.id, itemId, chk.checked);
        const target = this.currentProject.checklist.find(c => c.id === itemId);
        if (target) target.completed = chk.checked;
        this.renderChecklist(this.currentProject.checklist);
      });
    });
  }

  /* ── Export Actions ────────────────────────────────────────────────────── */
  bindExportActions(projectId) {
    document.getElementById('btn-export-markdown').onclick = () => {
      window.location.href = API.url(`/api/export/${projectId}/markdown`);
    };
    document.getElementById('btn-export-checklist').onclick = () => {
      window.location.href = API.url(`/api/export/${projectId}/checklist`);
    };
    document.getElementById('btn-export-sound-csv').onclick = () => {
      window.location.href = API.url(`/api/export/${projectId}/sound_csv`);
    };
    document.getElementById('btn-copy-full-seo').onclick = () => {
      const p = this.currentProject;
      const a = p.analysis || {};
      const full = `TITLE:\n${a.titles?.[0]?.title || p.title}\n\nDESCRIPTION:\n${document.getElementById('seo-description-text')?.value || ''}\n\nTAGS:\n${(a.seo_package?.suggested_tags || []).join(', ')}`;
      copyToClipboard(full, 'Full SEO Package (Title + Description + Tags) copied!');
    };
  }

  /* ── Dashboard & Projects Library ──────────────────────────────────────── */
  async refreshProjects() {
    try {
      this.projectsList = await API.getProjects();
    } catch (e) {
      console.warn('Could not load projects list:', e);
    }
  }

  renderDashboard() {
    const container = document.getElementById('dashboard-recent-projects');
    if (!container) return;

    if (this.projectsList.length === 0) {
      container.innerHTML = `
        <div class="col-span-full py-12 text-center text-[#93A4BA]">
          <p class="mb-4">No video analyses yet.</p>
          <button class="btn-primary" data-nav-target="view-upload">
            Analyze Your First Video
          </button>
        </div>
      `;
      return;
    }

    container.innerHTML = this.projectsList.slice(0, 4).map(p => this.createProjectCard(p)).join('');
    this.bindProjectCardEvents(container);
  }

  renderProjectsList() {
    const container = document.getElementById('projects-library-grid');
    if (!container) return;

    if (this.projectsList.length === 0) {
      container.innerHTML = `<div class="col-span-full py-12 text-center text-[#93A4BA]">No saved projects found.</div>`;
      return;
    }

    container.innerHTML = this.projectsList.map(p => this.createProjectCard(p)).join('');
    this.bindProjectCardEvents(container);
  }

  createProjectCard(p) {
    return `
      <div class="panel p-5 flex flex-col justify-between group" data-project-id="${p.id}">
        <div>
          <div class="flex items-center justify-between gap-2 mb-3">
            <span class="status-chip status-chip-accent font-mono font-medium">
              ${(p.platform || 'youtube').replace('_', ' ').toUpperCase()}
            </span>
            <span class="text-xs text-[#62768F] font-mono">${p.created_at ? new Date(p.created_at).toLocaleDateString() : 'Recent'}</span>
          </div>
          <h4 class="text-sm font-semibold text-[#F1F5F9] group-hover:text-[#4F8CFF] transition mb-1 cursor-pointer btn-open-project line-clamp-2">
            ${escapeHtml(p.title)}
          </h4>
        </div>
        <div class="flex items-center justify-between gap-3 mt-4">
          <button class="btn-open-project btn-primary px-3 py-1.5 text-xs font-semibold">Open Workspace</button>
          <div class="flex items-center gap-1.5">
            <button class="btn-dup-project p-1.5 text-[#93A4BA] hover:text-[#F1F5F9] hover:bg-[#111F32] rounded transition" title="Duplicate Variant">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7v8a2 2 0 002 2h6M8 7V5a2 2 0 012-2h4.586a1 1 0 01.707.293l4.414 4.414a1 1 0 01.293.707V15a2 2 0 01-2 2h-2M8 7H6a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2v-2"/></svg>
            </button>
            <button class="btn-del-project p-1.5 text-[#93A4BA] hover:text-[#FF5A65] hover:bg-[#111F32] rounded transition" title="Delete Project">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
            </button>
          </div>
        </div>
      </div>
    `;
  }

  bindProjectCardEvents(container) {
    container.querySelectorAll('.panel').forEach(card => {
      const pid = card.getAttribute('data-project-id');
      card.querySelectorAll('.btn-open-project').forEach(b => {
        b.onclick = () => this.openProject(pid);
      });
      const dup = card.querySelector('.btn-dup-project');
      if (dup) {
        dup.onclick = async () => {
          showToast('Duplicating project variant...', 'success');
          await API.duplicateProject(pid);
          await this.refreshProjects();
          this.renderProjectsList();
          this.renderDashboard();
          showToast('Project duplicated!', 'success');
        };
      }
      const del = card.querySelector('.btn-del-project');
      if (del) {
        del.onclick = async () => {
          if (confirm('Are you sure you want to delete this project?')) {
            await API.deleteProject(pid);
            await this.refreshProjects();
            this.renderProjectsList();
            this.renderDashboard();
            showToast('Project deleted', 'success');
          }
        };
      }
    });
  }

  /* ── Settings ──────────────────────────────────────────────────────────── */
  async loadSettings() {
    try {
      const s = await API.getSettings();
      document.getElementById('select-gemini-model').value = s.gemini_model || 'gemini-2.5-flash';
      document.getElementById('chk-keep-uploads').checked = s.keep_uploads || false;
      this.updateApiKeyStatusPill(s.gemini_api_key_set);
    } catch (e) {
      console.warn('Error loading settings:', e);
    }
  }

  bindSettingsForm() {
    const form = document.getElementById('settings-form');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const payload = {
        gemini_model: document.getElementById('select-gemini-model').value,
        keep_uploads: document.getElementById('chk-keep-uploads').checked
      };

      try {
        const res = await API.updateSettings(payload);
        showToast('Settings saved successfully!', 'success');
        this.updateApiKeyStatusPill(res.settings?.gemini_api_key_set);
      } catch (err) {
        showToast(`Failed to save settings: ${err.message}`, 'error');
      }
    });
  }

  updateApiKeyStatusPill(isSet) {
    const pill = document.getElementById('api-key-status-pill');
    if (!pill) return;
    if (isSet) {
      pill.innerHTML = `
        <span class="w-2 h-2 rounded-full bg-[#38E1A0]"></span>
        <span class="text-xs text-[#F1F5F9] font-medium">Multimodal AI Active</span>
      `;
    } else {
      pill.innerHTML = `
        <span class="w-2 h-2 rounded-full bg-[#FFB743]"></span>
        <span class="text-xs text-[#93A4BA]">Reference Dataset Mode</span>
      `;
    }
  }

  async checkHealthStatus() {
    try {
      const h = await API.getHealth();
      this.updateApiKeyStatusPill(h.live_ai_ready);
    } catch (e) {
      this.updateApiKeyStatusPill(false);
    }
  }

  bindModals() {
    // Retention upload modal
    const modal = document.getElementById('modal-retention-upload');
    const closeBtn = document.getElementById('btn-close-retention-modal');
    const submitBtn = document.getElementById('btn-submit-retention-csv');

    if (closeBtn && modal) {
      closeBtn.onclick = () => modal.classList.add('hidden');
    }

    if (submitBtn && modal) {
      submitBtn.onclick = async () => {
        const file = document.getElementById('retention-csv-file')?.files?.[0];
        const raw = document.getElementById('retention-raw-csv')?.value;
        if (!file && !raw) {
          showToast('Please select a CSV file or paste raw data', 'error');
          return;
        }

        try {
          showToast('Parsing retention data...', 'success');
          const res = await API.uploadRetention(this.currentProject.id, { file, rawCsv: raw });
          this.currentProject.analysis.retention_lab.simulated_retention_curve = res.curve;
          this.retentionChart.render(res.curve);
          modal.classList.add('hidden');
          showToast(`Successfully mapped ${res.points_count} measured data points!`, 'success');
        } catch (e) {
          showToast(e.message, 'error');
        }
      };
    }
  }
}

// Instantiate on DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
  window.framePilotApp = new FramePilotApp();
  window.framePilotApp.init();
});
