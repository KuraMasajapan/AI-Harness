import {test} from 'node:test';
import assert from 'node:assert/strict';
import {Metrics,summarize} from '../js/metrics.js';
test('FPS uses actual timestamps, not quality targets',()=>{
  const m=new Metrics();for(const time of [0,50,100,150])m.frame(time,2);
  assert.equal(m.result().fps,20);assert.equal(m.result().intervalMs.mean,50);
  assert.equal(m.result().intervalMs.sd,0);
});
test('spread and percentile include long frames',()=>{
  assert.deepEqual(summarize([10,20,30]),{samples:3,mean:20,sd:8.165,p95:30,max:30});
});
test('reset has no synthetic frame or artificial FPS',()=>{
  const m=new Metrics();m.frame(1000,1);m.reset();m.frame(5000,1);
  assert.equal(m.result().fps,null);assert.equal(m.result().intervalMs.samples,0);
});
