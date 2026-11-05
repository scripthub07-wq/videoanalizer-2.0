/**
 * FramePilot AI — Audio Waveform & Cue Marker Visualizer
 * Sample 3: Dark Professional Video Analysis
 */

export class WaveformVisualizer {
  constructor(canvasId, onSeek) {
    this.canvas = document.getElementById(canvasId);
    this.onSeek = onSeek;
    this.bars = 90;
    this.cues = [];
    this.initClick();
  }

  initClick() {
    if (!this.canvas) return;
    this.canvas.addEventListener('click', (e) => {
      const rect = this.canvas.getBoundingClientRect();
      const clickX = e.clientX - rect.left;
      const ratio = clickX / rect.width;
      if (this.onSeek && this.duration) {
        this.onSeek(ratio * this.duration);
      }
    });
  }

  render(duration = 60, cues = [], currentSec = 0) {
    if (!this.canvas) return;
    this.duration = duration;
    this.cues = cues;

    const ctx = this.canvas.getContext('2d');
    const width = this.canvas.width = this.canvas.parentElement.clientWidth || 600;
    const height = this.canvas.height = 68;

    ctx.clearRect(0, 0, width, height);

    const barWidth = width / this.bars;
    const currentRatio = duration > 0 ? (currentSec / duration) : 0;

    // Draw waveform bars
    for (let i = 0; i < this.bars; i++) {
      const barRatio = i / this.bars;
      const seed = Math.sin(i * 0.4) * 0.4 + Math.cos(i * 0.8) * 0.3 + 0.5;
      const barHeight = Math.max(6, seed * (height - 20));

      const x = i * barWidth;
      const y = (height - barHeight) / 2;

      // Color: Electric blue for played, subtle navy-slate for unplayed
      if (barRatio <= currentRatio) {
        ctx.fillStyle = '#4F8CFF';
      } else {
        ctx.fillStyle = '#1D2E45';
      }

      ctx.beginPath();
      ctx.roundRect(x + 1, y, Math.max(1.5, barWidth - 2), barHeight, 2);
      ctx.fill();
    }

    // Playhead Scrubber Line
    const playheadX = currentRatio * width;
    ctx.strokeStyle = '#F1F5F9';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(playheadX, 0);
    ctx.lineTo(playheadX, height);
    ctx.stroke();

    // Cue flags (SFX markers) in violet/cyan
    cues.forEach(cue => {
      const cueRatio = cue.time / duration;
      if (cueRatio >= 0 && cueRatio <= 1) {
        const cx = cueRatio * width;
        ctx.fillStyle = '#9D7BFF';
        ctx.beginPath();
        ctx.arc(cx, 7, 3.5, 0, Math.PI * 2);
        ctx.fill();
      }
    });
  }
}
