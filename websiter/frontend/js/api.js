/**
 * FramePilot AI — API Client Layer
 */

const isFilePage = window.location.protocol === 'file:';
const isLocalStaticServer = ['localhost', '127.0.0.1'].includes(window.location.hostname)
  && window.location.port !== '8000';
const API_BASE_URL = isFilePage
  ? 'http://127.0.0.1:8000'
  : isLocalStaticServer
    ? `${window.location.protocol}//${window.location.hostname}:8000`
    : '';

export const API = {
  url(path) {
    return `${API_BASE_URL}${path}`;
  },

  async getHealth() {
    const res = await fetch(this.url('/api/health'));
    return res.json();
  },

  async getProjects() {
    const res = await fetch(this.url('/api/projects'));
    return res.json();
  },

  async getProject(id) {
    const res = await fetch(this.url(`/api/projects/${id}`));
    if (!res.ok) throw new Error('Project not found');
    return res.json();
  },

  async patchProject(id, updates) {
    const res = await fetch(this.url(`/api/projects/${id}`), {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updates)
    });
    if (!res.ok) throw new Error('Failed to save project updates');
    return res.json();
  },

  async deleteProject(id) {
    const res = await fetch(this.url(`/api/projects/${id}`), { method: 'DELETE' });
    return res.json();
  },

  async duplicateProject(id) {
    const res = await fetch(this.url(`/api/projects/${id}/duplicate`), { method: 'POST' });
    return res.json();
  },

  async updateChecklistItem(projectId, itemId, completed) {
    const res = await fetch(this.url(`/api/projects/${projectId}/checklist`), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ item_id: itemId, completed })
    });
    return res.json();
  },

  async regenerateSection(projectId, section) {
    const res = await fetch(this.url(`/api/projects/${projectId}/regenerate/${section}`), {
      method: 'POST'
    });
    if (!res.ok) throw new Error('Failed to regenerate section');
    return res.json();
  },

  async createDemoProject(sampleKey = 'tech_review') {
    const res = await fetch(this.url(`/api/demo/${sampleKey}`), { method: 'POST' });
    if (!res.ok) throw new Error('Failed to create demo project');
    return res.json();
  },

  async uploadRetention(projectId, { file, rawCsv }) {
    const formData = new FormData();
    if (file) formData.append('file', file);
    if (rawCsv) formData.append('raw_csv', rawCsv);

    const res = await fetch(this.url(`/api/analytics/upload-retention/${projectId}`), {
      method: 'POST',
      body: formData
    });
    if (!res.ok) throw new Error('Failed to upload retention data');
    return res.json();
  },

  async getSettings() {
    const res = await fetch(this.url('/api/settings'));
    return res.json();
  },

  async updateSettings(settings) {
    const res = await fetch(this.url('/api/settings'), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(settings)
    });
    return res.json();
  },

  async getYouTubeOAuthDetails() {
    const res = await fetch(this.url('/api/analytics/youtube-oauth'));
    return res.json();
  },

  /**
   * Streams SSE video analysis from /api/analyze-stream using fetch ReadableStream
   */
  async streamAnalysis(formData, { onUploadProgress, onProgress, onComplete, onError }) {
    return new Promise((resolve) => {
      const request = new XMLHttpRequest();
      let responseOffset = 0;
      let buffer = '';
      let completed = false;
      let failed = false;

      const fail = (message) => {
        if (completed || failed) return;
        failed = true;
        if (onError) onError(message);
      };

      const processResponse = (finalChunk = false) => {
        const newText = request.responseText.slice(responseOffset).replace(/\r\n/g, '\n');
        responseOffset = request.responseText.length;
        buffer += newText;

        const blocks = buffer.split('\n\n');
        buffer = blocks.pop() || '';
        if (finalChunk && buffer.trim()) {
          blocks.push(buffer);
          buffer = '';
        }

        for (const block of blocks) {
          if (!block.trim()) continue;

          let eventType = 'message';
          const dataLines = [];
          for (const line of block.split('\n')) {
            if (line.startsWith('event:')) eventType = line.slice(6).trim();
            else if (line.startsWith('data:')) dataLines.push(line.slice(5).trim());
          }

          if (!dataLines.length) continue;
          try {
            const parsed = JSON.parse(dataLines.join('\n'));
            if (eventType === 'progress' && onProgress) {
              onProgress(parsed);
            } else if (eventType === 'complete') {
              completed = true;
              if (onComplete) Promise.resolve(onComplete(parsed)).catch((error) => fail(error.message));
            } else if (eventType === 'error') {
              fail(parsed.message || 'Analysis failed');
            }
          } catch (error) {
            console.warn('Error parsing SSE event data:', error);
          }
        }
      };

      request.upload.addEventListener('progress', (event) => {
        if (event.lengthComputable && onUploadProgress) {
          onUploadProgress({ loaded: event.loaded, total: event.total, percent: Math.round((event.loaded / event.total) * 100) });
        }
      });
      request.addEventListener('progress', () => processResponse());
      request.addEventListener('load', () => {
        processResponse(true);
        if (request.status < 200 || request.status >= 300) {
          fail(request.responseText || `Analysis request failed (${request.status})`);
        } else if (!completed && !failed) {
          fail('The analysis connection ended before completion. Please try again.');
        }
        resolve();
      });
      request.addEventListener('error', () => {
        fail('Could not connect to the analysis server. Check that the backend is running.');
        resolve();
      });
      request.addEventListener('abort', () => {
        fail('The analysis request was cancelled.');
        resolve();
      });

      request.open('POST', this.url('/api/analyze-stream'));
      request.send(formData);
    });
  }
};
