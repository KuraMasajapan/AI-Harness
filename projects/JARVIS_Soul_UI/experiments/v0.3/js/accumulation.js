import {CanvasA} from './canvas-a.js';
const original=new CanvasA(document.querySelector('#original'),{clear:false});
const corrected=new CanvasA(document.querySelector('#corrected'));
let running=false;
function pixels(renderer){
  const {width,height}=renderer.canvas;
  const data=renderer.ctx.getImageData(0,0,width,height).data;
  let sum=0,opaque=0,visible=0;
  for(let i=3;i<data.length;i+=4){sum+=data[i]/255;if(data[i]>=242)opaque++;if(data[i]>2)visible++;}
  const n=width*height,round=x=>Math.round(x*10000)/10000;
  return {meanAlpha:round(sum/n),opaqueFraction:round(opaque/n),visibleFraction:round(visible/n),resolution:[width,height]};
}
document.querySelector('#start').addEventListener('click',()=>{
  if(running)return;running=true;
  document.querySelector('#start').disabled=true;
  document.querySelector('#evidence').replaceChildren();
  // Backing size approximately 464 x 348; actual integer dimensions are recorded.
  for(const r of [original,corrected])r.resize(800,600);
  const captured=[],deadlines=[0,5000,15000];let start=null,last=null,next=0,frames=0;
  function frame(now){
    if(document.hidden){running=false;document.querySelector('#start').disabled=false;document.querySelector('#progress').textContent='Cancelled: keep this tab active for a valid comparison.';return;}
    if(start===null){start=now;next=now;}
    if(now>=next-.5){
      const elapsed=now-start;frames++;
      original.render(elapsed/1000);corrected.render(elapsed/1000);
      if(now-next>100)next=now+1000/30;else next+=1000/30;
      if(elapsed>=deadlines[captured.length]){
        const row={targetMs:deadlines[captured.length],actualMs:Math.round(elapsed),frames,original:pixels(original),corrected:pixels(corrected)};
        captured.push(row);
        const section=document.createElement('section'),h=document.createElement('h2');h.textContent=`${row.targetMs/1000}s · ${frames} frames`;section.append(h);
        for(const [name,r] of [['Original · no clear',original],['A · clear each frame',corrected]]){
          const heading=document.createElement('h3');heading.textContent=name;
          const figure=document.createElement('figure'),image=new Image(),caption=document.createElement('figcaption');
          image.src=r.canvas.toDataURL('image/webp',.9);image.alt=`${name}, ${row.actualMs} ms`;
          const m=r===original?row.original:row.corrected;
          caption.textContent=`mean α ${m.meanAlpha} · opaque ${(100*m.opaqueFraction).toFixed(2)}% · actual ${row.actualMs} ms`;
          figure.append(image,caption);section.append(heading,figure);
        }
        document.querySelector('#evidence').append(section);document.querySelector('#raw').textContent=JSON.stringify(captured,null,2);
      }
      document.querySelector('#progress').textContent=`${(elapsed/1000).toFixed(1)}s · ${frames} rendered frames · ${captured.length}/3 captures`;
      last=now;
    }
    if(captured.length<3)requestAnimationFrame(frame);
    else {running=false;document.querySelector('#start').disabled=false;document.querySelector('#progress').textContent+=' · complete';}
  }
  requestAnimationFrame(frame);
});
