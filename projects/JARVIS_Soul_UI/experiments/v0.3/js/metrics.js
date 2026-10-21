export function summarize(values) {
  if (!values.length) return { samples: 0, mean: null, sd: null, p95: null, max: null };
  const mean = values.reduce((a, b) => a + b, 0) / values.length;
  const sorted = [...values].sort((a, b) => a - b);
  const round = x => Math.round(x * 1000) / 1000;
  return { samples: values.length, mean: round(mean),
    sd: round(Math.sqrt(values.reduce((a, b) => a + (b - mean) ** 2, 0) / values.length)),
    p95: round(sorted[Math.ceil(sorted.length * .95) - 1]), max: round(sorted.at(-1)) };
}
export class Metrics {
  constructor() { this.reset(); }
  reset() { this.intervals = []; this.submit = []; this.gpu = []; this.last = null; }
  frame(time, cost) {
    if (this.last !== null) this.intervals.push(time - this.last);
    this.last = time;
    this.submit.push(cost);
    for (const a of [this.intervals, this.submit, this.gpu]) if (a.length > 3600) a.shift();
  }
  result() {
    const interval = summarize(this.intervals);
    return { fps: interval.mean ? Math.round(100000 / interval.mean) / 100 : null,
      intervalMs: interval, jsSubmitMs: summarize(this.submit), gpuDrawMs: summarize(this.gpu) };
  }
}
