/**
 * FramePilot AI — Video Player Component
 * Provides synchronized seeking, play/pause, and timecode jump triggers.
 */

import { formatSeconds } from '../utils.js';

export class StudioVideoPlayer {
  constructor(videoElementId, timeDisplayId) {
    this.video = document.getElementById(videoElementId);
    this.timeDisplay = document.getElementById(timeDisplayId);
    this.onTimeUpdateCallbacks = [];
    this.init();
  }

  init() {
    if (!this.video) return;

    this.video.addEventListener('timeupdate', () => {
      this.updateTimeDisplay();
      this.onTimeUpdateCallbacks.forEach(cb => cb(this.video.currentTime, this.video.duration));
    });

    this.video.addEventListener('loadedmetadata', () => {
      this.updateTimeDisplay();
    });
  }

  updateTimeDisplay() {
    if (!this.timeDisplay || !this.video) return;
    const cur = formatSeconds(this.video.currentTime || 0);
    const dur = formatSeconds(this.video.duration || 0);
    this.timeDisplay.innerText = `${cur} / ${dur}`;
  }

  seek(seconds) {
    if (!this.video) return;
    const target = Math.max(0, Math.min(seconds, this.video.duration || 9999));
    this.video.currentTime = target;
    this.video.play().catch(() => {}); // Play upon jump
    this.highlightActiveSegment(target);
  }

  highlightActiveSegment(targetSeconds) {
    // Pulse any cards or pills matching this timestamp
    document.querySelectorAll('[data-timestamp-start]').forEach(el => {
      const start = parseFloat(el.getAttribute('data-timestamp-start')) || 0;
      const end = parseFloat(el.getAttribute('data-timestamp-end')) || start + 15;
      if (targetSeconds >= start && targetSeconds <= end) {
        el.classList.add('ring-2', 'ring-[#4F8CFF]', 'bg-[#162842]');
        setTimeout(() => {
          el.classList.remove('ring-2', 'ring-[#4F8CFF]', 'bg-[#162842]');
        }, 2000);
      }
    });
  }

  loadSource(url) {
    if (!this.video) return;
    if (url) {
      this.video.src = url;
      this.video.load();
    }
  }

  onTimeUpdate(callback) {
    this.onTimeUpdateCallbacks.push(callback);
  }
}
