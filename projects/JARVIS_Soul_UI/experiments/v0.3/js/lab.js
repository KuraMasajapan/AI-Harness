import { CanvasA, A_QUALITY } from './canvas-a.js';
import { Metrics } from './metrics.js';

const $ = selector => document.querySelector(selector);
const metrics = new Metrics(), errors = [], results = [];
let renderer, raf=0, last=0, next=0, time=0, paused=false, dirty=true, run=null, version=0, recording=false, recordLayer=null;
let state='ready', mode='B', quality='Balanced';
const motion = matchMedia('(prefers-reduced-motion: reduce)');
const reduced = () => motion.matches || $('#reduce').checked;
const still = () => $('#still').checked || reduced();
const reportError = message => { errors.push(String(message)); $('#errors').textContent=errors.join('\n'); };
window.addEventListener('error',event=>reportError(event.message));
window.addEventListener('unhandledrejection',event=>reportError(event.reason?.stack || event.reason));
const copy = {
  ready:['Ready','A quiet, breathing current of light.'],
  listening:['Listening','The outer flow opens gently. Demo only; no microphone access.'],
  processing:['Processing','Light gathers inward and circulates through the interior.'],
  speaking:['Speaking','A soft, irregular cadence suggests speech. No audio is connected.'],
  attention:['Attention','Movement settles; a narrower posture carries quiet tension.']
};
function setState(value) {
  state=value;
  document.querySelectorAll('.state-button').forEach(button=>{const active=button.dataset.state===state;button.classList.toggle('is-selected',active);button.setAttribute('aria-pressed',String(active));});
  $('#status-title').textContent=copy[state][0];$('#status-copy').textContent=copy[state][1];
  $('#state-label').textContent=state==='ready'?'Ready for a demo':`${copy[state][0]} · demo`;
  renderer?.setInput({state,audioLevel:Number($('#audio').value)},still()||paused);wake();
}
function size() {
  if(!renderer)return;
  const rect=renderer.canvas.getBoundingClientRect();renderer.resize(rect.width,rect.height);wake();environment();
}
function environment() {
  if(!renderer)return;
  $('#environment').textContent=JSON.stringify({...renderer.info(),viewport:[innerWidth,innerHeight],devicePixelRatio,
    browser:navigator.userAgent,reducedMotionSystem:motion.matches,reducedMotionEffective:reduced()},null,2);
}
function wake(){dirty=true;if(!raf&&!document.hidden)raf=requestAnimationFrame(frame);}
function frame(now) {
  raf=0;if(!renderer || document.hidden)return;
  const fps=quality==='High'?60:quality==='Eco'?24:30, interval=1000/fps;
  if(dirty || now>=next-.5){
    const dt=last?Math.min(.1,(now-last)/1000):interval/1000;
    if(!paused&&!still())time+=dt;
    const start=performance.now();renderer.render(still()?8:time,paused?0:dt,{still:still()});
    const submit=performance.now()-start;metrics.frame(now,submit);
    if(recordLayer){
      // MP4 has no alpha: composite immediately after drawing while WebGL pixels exist.
      // Never encode unpremultiplied RGB from the transparent framebuffer directly.
      const {ctx,canvas}=recordLayer;ctx.fillStyle='#050a11';ctx.fillRect(0,0,canvas.width,canvas.height);
      ctx.drawImage(renderer.canvas,0,0,canvas.width,canvas.height);
    }
    if(now-next>interval*2 || dirty)next=now+interval;else next+=interval;
    last=now;dirty=false;
    if(run) {
      if(!run.started && now>=run.start){metrics.reset();run.started=now;$('#run-status').textContent='Measuring… keep this tab active';}
      else if(run.started && now-run.started>=10000){
        const error=renderer.diagnostics?.();if(error)reportError(error);
        const result={...metrics.result(),...renderer.info(),state,viewport:[innerWidth,innerHeight],
          durationMs:Math.round(now-run.started),errors:[...errors],recordedAt:new Date().toISOString()};
        results.push(result);$('#metrics').textContent=JSON.stringify(results,null,2);
        $('#run-status').textContent=`Measured ${result.fps} fps · ${result.intervalMs.mean} ms`;run=null;lock(false);environment();
      }
    }
    if(!run && metrics.submit.length%30===0 || still() || paused){
      const m=metrics.result();$('#dev-overlay').textContent=`${mode} · ${quality} · ${still()?'still':paused?'paused':`${m.fps??'—'} measured fps`} · ${renderer.canvas.width}×${renderer.canvas.height}`;
    }
  }
  if(!paused&&!still())raf=requestAnimationFrame(frame);
}
function lock(value){document.querySelectorAll('.lab-bar select,.lab-bar input,.lab-bar button,.state-button,#reduce,#audio,#loss,#record').forEach(el=>el.disabled=value);if(!value)syncControls();}
function syncControls(){
  $('#bloom').disabled=mode==='A'||quality==='Eco';if($('#bloom').disabled)$('#bloom').checked=false;
  $('#loss').disabled=mode==='A';$('#benchmark').disabled=paused||still();$('#record').disabled=paused||still()||recording;
}
async function switchRenderer(value,reason='') {
  const own=++version;
  if(raf)cancelAnimationFrame(raf);raf=0;observer.disconnect();
  renderer?.dispose();renderer=null;
  // Each renderer gets its own canvas/context. Context types are never mixed.
  const old=$('#soul-canvas'),canvas=old.cloneNode(false);old.replaceWith(canvas);
  mode=value;$('#renderer').value=mode;
  try {
    if(mode==='B') {
      const {WebGLB}=await import('./webgl-b.js');if(own!==version)return;
      renderer=new WebGLB(canvas,{onLost:message=>{$('#notice').textContent=`${message}; switched to Canvas fallback.`;switchRenderer('A',message);},onError:reportError,onGpu:ms=>metrics.gpu.push(ms)});
    } else renderer=new CanvasA(canvas);
  } catch(error) {
    if(mode==='B'){await switchRenderer('A',`WebGL unavailable: ${error.message}`);return;}reportError(error.message);return;
  }
  renderer.setQuality(quality);renderer.setInput({state,audioLevel:Number($('#audio').value)},still());
  syncControls();renderer.setBloom?.($('#bloom').checked);size();observer.observe(canvas);
  $('#notice').textContent=reason?`${reason}. Canvas A fallback is active; its baseline visual limitations remain.`:
    mode==='A'?'A: clearRect only changes the image. The opaque core and limited state differences are retained as the control.':
    'B: original 3D flow, soft particles and open filaments. Bloom OFF is the reference. This is not the formal UI.';
  time=0;last=0;next=0;metrics.reset();wake();environment();
}
const observer=new ResizeObserver(size);
document.querySelectorAll('.state-button').forEach(button=>button.addEventListener('click',()=>setState(button.dataset.state)));
$('.mic-button').addEventListener('click',()=>setState('listening'));
$('.voice-tool').addEventListener('click',()=>$('#quality').focus());
document.querySelectorAll('.voice-tool')[1].addEventListener('click',()=>$('.state-button').focus());
document.querySelectorAll('.nav-item,.quick-actions button').forEach(b=>b.addEventListener('click',()=>$('#notice').textContent='Visual placeholder only — no connected service or AI action.'));
$('#renderer').addEventListener('change',()=>switchRenderer($('#renderer').value));
$('#quality').addEventListener('change',()=>{quality=$('#quality').value;renderer.setQuality(quality);syncControls();renderer.setBloom?.($('#bloom').checked);metrics.reset();size();});
$('#bloom').addEventListener('change',()=>{renderer.setBloom?.($('#bloom').checked);wake();environment();});
for(const id of ['#still','#reduce']) $(id).addEventListener('change',()=>{setState(state);syncControls();environment();});
motion.addEventListener('change',()=>{setState(state);syncControls();environment();});
$('#audio').addEventListener('input',()=>setState(state));
$('#pause').addEventListener('click',()=>{paused=!paused;$('#pause').setAttribute('aria-pressed',String(paused));$('#pause').textContent=paused?'Resume':'Pause';syncControls();wake();});
$('#benchmark').addEventListener('click',()=>{if(paused||still())return;lock(true);time=0;last=0;next=0;renderer.resetTime?.();metrics.reset();run={start:performance.now()+2000,started:0};$('#run-status').textContent='Warming up · 2s';wake();});
$('#loss').addEventListener('click',()=>renderer.simulateLoss?.());
document.addEventListener('keydown',event=>{
  if(event.target.closest('input,select,button,a') || event.altKey || event.ctrlKey || event.metaKey || run)return;
  if('12345'.includes(event.key)){setState(Object.keys(copy)[Number(event.key)-1]);}
  if(event.code==='Space'){event.preventDefault();$('#pause').click();}
});
document.addEventListener('visibilitychange',()=>{
  if(document.hidden){if(raf)cancelAnimationFrame(raf);raf=0;if(run){run=null;lock(false);$('#run-status').textContent='Measurement cancelled: tab became hidden';}}
  else {last=0;next=0;metrics.reset();wake();}
});
$('#record').addEventListener('click',()=>{
  if(typeof MediaRecorder==='undefined'){ $('#record-status').textContent='MediaRecorder unavailable';return; }
  const mime=['video/mp4;codecs=avc1.42001E','video/mp4','video/webm;codecs=vp9','video/webm'].find(t=>MediaRecorder.isTypeSupported(t));
  if(!mime){$('#record-status').textContent='No supported video encoder';return;}
  const output=document.createElement('canvas');
  output.width=Math.max(2,renderer.canvas.width&~1);output.height=Math.max(2,renderer.canvas.height&~1);
  recordLayer={canvas:output,ctx:output.getContext('2d',{alpha:false})};
  const stream=output.captureStream(30),recorder=new MediaRecorder(stream,{mimeType:mime,videoBitsPerSecond:1400000}),chunks=[];
  const label=`${mode.toLowerCase()}-${state}-${quality.toLowerCase()}-composited`;
  recording=true;lock(true);$('#record-status').textContent='Recording 6s · canvas only';
  recorder.ondataavailable=e=>{if(e.data.size)chunks.push(e.data);};
  recorder.onstop=()=>{
    stream.getTracks().forEach(t=>t.stop());recording=false;recordLayer=null;lock(false);
    const blob=new Blob(chunks,{type:mime}),url=URL.createObjectURL(blob);
    const a=document.createElement('a');a.href=url;a.download=`${label}.${mime.includes('mp4')?'mp4':'webm'}`;a.textContent=`Download ${label} (${(blob.size/1024).toFixed(0)} KB)`;
    const video=document.createElement('video');video.controls=true;video.playsInline=true;video.src=url;
    $('#recordings').append(a,video);$('#record-status').textContent=`Recorded ${mime}. Playback can be inspected below.`;
  };
  recorder.start();setTimeout(()=>{if(recorder.state==='recording')recorder.stop();},6000);
});
const params=new URLSearchParams(location.search);
if(['A','B'].includes(params.get('renderer')))mode=params.get('renderer');
if(A_QUALITY[params.get('quality')])quality=params.get('quality');
if(copy[params.get('state')])state=params.get('state');
$('#quality').value=quality;$('#bloom').checked=params.get('bloom')==='1';$('#still').checked=params.get('still')==='1';
setState(state);await switchRenderer(mode);
