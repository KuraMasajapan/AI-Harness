import { SoulRenderer } from './soul-renderer.js?v=2';

const copy = {
  idle:['Ready','A quiet visual baseline. Choose a state to preview the motion language.'],
  listening:['Listening','A restrained pulse suggests an input state. No microphone is requested.'],
  processing:['Processing','A slow inward flow suggests work in progress. Demo state only.'],
  speaking:['Speaking','A small lift in the glow suggests output. No audio is connected.'],
  error:['Attention','The visual settles back so text can carry the message.']
};
const canvas=document.querySelector('#soul-canvas');
const renderer=new SoulRenderer(canvas,document.querySelector('#dev-overlay'));
const setState=(state)=>{document.querySelectorAll('.state-button').forEach(b=>{const selected=b.dataset.state===state;b.classList.toggle('is-selected',selected);b.setAttribute('aria-pressed',String(selected));});document.querySelector('#status-title').textContent=copy[state][0];document.querySelector('#status-copy').textContent=copy[state][1];document.querySelector('#state-label').textContent=state==='idle'?'Ready for a demo':`${copy[state][0]} · demo`;renderer.setState(state)};
document.querySelectorAll('.state-button').forEach(b=>b.addEventListener('click',()=>setState(b.dataset.state)));
document.querySelector('.mic-button').addEventListener('click',()=>setState('listening'));
renderer.start();

