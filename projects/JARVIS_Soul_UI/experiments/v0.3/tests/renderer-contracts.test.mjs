import {test} from 'node:test';
import assert from 'node:assert/strict';
import {CanvasA,A_QUALITY} from '../js/canvas-a.js';
import {B_QUALITY} from '../js/webgl-b.js';

function makeCanvas(){
  const calls=[];
  const ctx=new Proxy({}, {get:(_,key)=>key==='createRadialGradient'?()=>({addColorStop(){}}):(...args)=>calls.push([key,...args])});
  return {canvas:{width:464,height:348,getContext:()=>ctx},calls};
}
test('A clears transparently exactly once before reusing the baseline',()=>{
  const {canvas,calls}=makeCanvas(),a=new CanvasA(canvas);a.render(8);
  assert.deepEqual(calls[0],['clearRect',0,0,464,348]);
  assert.equal(calls.filter(c=>c[0]==='clearRect').length,1);
  assert.equal(calls.filter(c=>c[0]==='fillRect').length,150);
  assert.equal(calls.filter(c=>c[0]==='stroke').length,10);
});
test('no-clear diagnostic keeps the original drawing operations',()=>{
  const left=makeCanvas(),right=makeCanvas();
  new CanvasA(left.canvas).render(8);new CanvasA(right.canvas,{clear:false}).render(8);
  assert.deepEqual(left.calls.slice(1),right.calls);
});
test('state aliases preserve baseline control behavior',()=>{
  const a=new CanvasA(makeCanvas().canvas);
  a.setInput({state:'ready'});assert.equal(a.state,'idle');
  a.setInput({state:'attention'});assert.equal(a.state,'error');
});
test('quality budgets remain bounded',()=>{
  for(const q of Object.values(B_QUALITY)){assert(q.particles<=1800);assert(q.maxPixels<=1000000);}
  assert.equal(B_QUALITY.Eco.fps,24);assert.equal(A_QUALITY.Balanced.particles,150);
});
