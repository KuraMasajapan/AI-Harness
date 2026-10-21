import { SoulRenderer } from '../../../js/soul-renderer.js';

export const A_QUALITY = {
  Eco: { scale: .42, particles: 80, filaments: 6, fps: 24 },
  Balanced: { scale: .58, particles: 150, filaments: 10, fps: 30 },
  High: { scale: .76, particles: 230, filaments: 14, fps: 60 }
};

// A deliberate control experiment: reuse the untouched baseline draw routine.
// Only the clear changes the image. Lifecycle/measurement live outside the baseline.
export class CanvasA {
  constructor(canvas, { clear = true } = {}) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    if (!this.ctx) throw new Error('Canvas 2D unavailable');
    this.clear = clear;
    this.quality = 'Balanced';
    this.state = 'idle';
    this.seed = Array.from({ length: 240 }, (_, i) => ({
      a: i * 2.399, x: Math.sin(i * 7.13), y: Math.cos(i * 4.7),
      p: (i * 1.7) % 6.28, s: (i % 7) / 7
    }));
  }
  setInput({ state }) { this.state = state === 'attention' ? 'error' : state === 'ready' ? 'idle' : state; }
  setQuality(q) { this.quality = q; }
  resize(w, h) {
    const scale = A_QUALITY[this.quality].scale;
    this.canvas.width = Math.max(1, Math.floor(w * scale));
    this.canvas.height = Math.max(1, Math.floor(h * scale));
  }
  render(t) {
    if (this.clear) this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    SoulRenderer.prototype.draw2d.call(this, t, false);
  }
  info() {
    const {fps,...settings}=A_QUALITY[this.quality];
    return { method: 'Canvas 2D', quality: this.quality, ...settings, targetFps:fps,
      resolution: [this.canvas.width, this.canvas.height], bloom: false,
      gpu: 'Canvas compositor; utilization unmeasured', gpuTimer: 'unavailable',
      limitation: 'Baseline geometry retained; only Listening differs from Ready.' };
  }
  dispose() {}
}
