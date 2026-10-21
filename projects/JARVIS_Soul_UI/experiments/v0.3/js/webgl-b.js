import * as THREE from '../vendor/three.module.min.js';
import { ribbonVertex, ribbonFragment, pointVertex, pointFragment, fullscreenVertex, blurFragment, compositeFragment } from './shaders.js';

export const B_QUALITY = {
  Eco: { dpr: .75, maxPixels: 300000, particles: 600, filaments: 7, segments: 112, fps: 24 },
  Balanced: { dpr: 1, maxPixels: 600000, particles: 1200, filaments: 12, segments: 192, fps: 30 },
  High: { dpr: 1.35, maxPixels: 1000000, particles: 1800, filaments: 16, segments: 224, fps: 60 }
};
const stateVectors = { ready: [0,0,0,0], listening: [1,0,0,0], processing: [0,1,0,0], speaking: [0,0,1,0], attention: [0,0,0,1] };
export class WebGLB {
  constructor(canvas, { onLost, onError, onGpu } = {}) {
    this.canvas = canvas;
    this.onError = onError || (() => {});
    this.onGpu = onGpu || (() => {});
    this.lost = event => { event.preventDefault(); onLost?.('WebGL context lost'); };
    canvas.addEventListener('webglcontextlost', this.lost);
    this.renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: false,
      premultipliedAlpha: false, powerPreference: 'low-power', preserveDrawingBuffer: false });
    this.renderer.setClearColor(0x000000, 0);
    this.renderer.debug.onShaderError = (gl, program, vs, fs) => {
      this.onError(`GLSL: ${gl.getProgramInfoLog(program)} ${gl.getShaderInfoLog(vs)} ${gl.getShaderInfoLog(fs)}`);
    };
    this.renderer.info.autoReset = false;
    this.scene = new THREE.Scene();
    this.camera = new THREE.PerspectiveCamera(39, 1, .1, 20);
    this.camera.position.set(0, -.08, 5.5);
    this.camera.lookAt(0, -.08, 0);
    this.uniforms = { uTime: { value: 0 }, uState: { value: new THREE.Vector4() },
      uAudio: { value: 0 }, uPixelScale: { value: 1 } };
    this.target = new THREE.Vector4();
    this.state = 'ready'; this.audio = 0; this.flowTime = 0; this.previousTime = null;
    this.materials = [];
    this.gl = this.renderer.getContext();
    const debug = this.gl.getExtension('WEBGL_debug_renderer_info');
    this.gpu = debug ? this.gl.getParameter(debug.UNMASKED_RENDERER_WEBGL) : this.gl.getParameter(this.gl.RENDERER);
    this.timer = this.gl.getExtension('EXT_disjoint_timer_query_webgl2');
    this.queries = [];
    const type = this.gl.getExtension('EXT_color_buffer_float') ? THREE.HalfFloatType : THREE.UnsignedByteType;
    this.targetType = type === THREE.HalfFloatType ? 'RGBA16F' : 'RGBA8';
    this.sceneTarget = new THREE.WebGLRenderTarget(1,1,{type,depthBuffer:false});
    this.blurA = new THREE.WebGLRenderTarget(1,1,{type,depthBuffer:false});
    this.blurB = this.blurA.clone();
    this.postScene = new THREE.Scene(); this.postCamera = new THREE.Camera();
    this.blurMat = new THREE.ShaderMaterial({vertexShader:fullscreenVertex,fragmentShader:blurFragment,
      uniforms:{tInput:{value:null},uStep:{value:new THREE.Vector2()},uThreshold:{value:.13}}, depthTest:false,depthWrite:false});
    this.compositeMat = new THREE.ShaderMaterial({vertexShader:fullscreenVertex,fragmentShader:compositeFragment,
      uniforms:{tScene:{value:this.sceneTarget.texture},tBloom:{value:this.blurB.texture},uBloom:{value:0}},depthTest:false,depthWrite:false});
    this.quad = new THREE.Mesh(new THREE.PlaneGeometry(2,2),this.compositeMat); this.postScene.add(this.quad);
    this.setQuality('Balanced');
  }
  setInput({ state = this.state, audioLevel = this.audio }, immediate = false) {
    state = state === 'idle' ? 'ready' : state === 'error' ? 'attention' : state;
    if (!stateVectors[state]) throw new Error(`Unknown state: ${state}`);
    this.state = state; this.target.fromArray(stateVectors[state]);
    this.audio = Math.max(0,Math.min(1,Number.isFinite(audioLevel) ? audioLevel : 0));
    if (immediate) this.uniforms.uState.value.copy(this.target);
  }
  setQuality(quality) {
    this.quality = quality; const q = B_QUALITY[quality];
    if (!q) throw new Error('Unknown quality');
    for (const child of [...this.scene.children]) { this.scene.remove(child); child.geometry.dispose(); child.material.dispose(); }
    const position = new Float32Array(q.particles*3), seeds = new Float32Array(q.particles*4);
    // Integer PRNG keeps distribution deterministic across browsers and captures.
    let seed = 92371;
    const rand = () => {seed = (Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296;};
    for(let i=0;i<q.particles;i++) seeds.set([rand(),Math.floor(rand()*23)+rand()*.14,rand(),rand()],i*4);
    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position',new THREE.BufferAttribute(position,3));
    geometry.setAttribute('aSeed',new THREE.BufferAttribute(seeds,4));
    const material = (vertexShader,fragmentShader) => new THREE.ShaderMaterial({uniforms:this.uniforms,
      vertexShader,fragmentShader,transparent:true,blending:THREE.AdditiveBlending,depthWrite:false,depthTest:false,side:THREE.DoubleSide});
    const points = new THREE.Points(geometry,material(pointVertex,pointFragment)); points.frustumCulled=false; this.scene.add(points);
    const data=[], vertices=[], indices=[];
    for(let f=0;f<q.filaments+9;f++) {
      const offset=data.length/4;
      for(let j=0;j<=q.segments;j++) for(const side of [-1,1]) {
        const strandSeed=f<q.filaments?Math.floor(f/3)*3.1+(f%3)*.085:(f-q.filaments)*3.1+.06;
        const layer=f<q.filaments?0:f<q.filaments+5?1:2;
        data.push(.025+.95*j/q.segments,side,strandSeed,layer); vertices.push(0,0,0);
      }
      for(let j=0;j<q.segments;j++) {const n=offset+j*2;indices.push(n,n+1,n+2,n+1,n+3,n+2);}
    }
    const ribbons = new THREE.BufferGeometry();
    ribbons.setAttribute('position',new THREE.Float32BufferAttribute(vertices,3));
    ribbons.setAttribute('aFlow',new THREE.Float32BufferAttribute(data,4)); ribbons.setIndex(indices);
    const mesh = new THREE.Mesh(ribbons,material(ribbonVertex,ribbonFragment));mesh.frustumCulled=false;this.scene.add(mesh);
    if(quality==='Eco') this.bloom=false;
  }
  setBloom(value) { this.bloom = Boolean(value) && this.quality !== 'Eco'; }
  resetTime() { this.flowTime=0; }
  resize(w,h) {
    const q=B_QUALITY[this.quality];
    const ratio=Math.min(devicePixelRatio || 1,q.dpr,Math.sqrt(q.maxPixels/Math.max(1,w*h)));
    const width=Math.max(1,Math.floor(w*ratio)),height=Math.max(1,Math.floor(h*ratio));
    this.renderer.setSize(width,height,false);
    this.sceneTarget.setSize(width,height);
    this.blurA.setSize(Math.max(1,width>>2),Math.max(1,height>>2));this.blurB.setSize(Math.max(1,width>>2),Math.max(1,height>>2));
    this.uniforms.uPixelScale.value=ratio;
    this.camera.aspect=w/Math.max(1,h);this.camera.updateProjectionMatrix();
  }
  render(time,dt=1/30,{still=false}={}) {
    const u=this.uniforms;
    u.uState.value.lerp(this.target,still?1:1-Math.exp(-Math.min(dt,.1)*2.6));
    u.uAudio.value += (this.audio-u.uAudio.value)*(still?1:1-Math.exp(-dt*6));
    const speed=1+u.uState.value.y*.75-u.uState.value.w*.88;
    this.flowTime += Math.min(dt,.1)*speed;
    u.uTime.value=still?8:this.flowTime;
    this.scene.rotation.y = .12*Math.sin(u.uTime.value*.1);
    this.scene.rotation.z = .055*Math.sin(u.uTime.value*.13)-u.uState.value.w*.08;
    const gl=this.gl, timer=this.timer;
    if(timer) {
      const disjoint=gl.getParameter(timer.GPU_DISJOINT_EXT);
      if(disjoint){for(const query of this.queries)gl.deleteQuery(query);this.queries=[];}
      while(this.queries.length && gl.getQueryParameter(this.queries[0],gl.QUERY_RESULT_AVAILABLE)) {
        const query=this.queries.shift();if(!disjoint)this.onGpu(gl.getQueryParameter(query,gl.QUERY_RESULT)/1e6);gl.deleteQuery(query);
      }
    }
    let query=null;
    if(timer && this.queries.length<4){query=gl.createQuery();gl.beginQuery(timer.TIME_ELAPSED_EXT,query);}
    this.renderer.info.reset();
    this.renderer.setRenderTarget(this.sceneTarget); this.renderer.render(this.scene,this.camera);
    if(this.bloom) {
      this.quad.material=this.blurMat;
      this.blurMat.uniforms.tInput.value=this.sceneTarget.texture;
      this.blurMat.uniforms.uThreshold.value=.13;
      this.blurMat.uniforms.uStep.value.set(1/this.blurA.width,0);
      this.renderer.setRenderTarget(this.blurA);this.renderer.render(this.postScene,this.postCamera);
      this.blurMat.uniforms.tInput.value=this.blurA.texture;
      this.blurMat.uniforms.uThreshold.value=-.16;
      this.blurMat.uniforms.uStep.value.set(0,1/this.blurA.height);
      this.renderer.setRenderTarget(this.blurB);this.renderer.render(this.postScene,this.postCamera);
    }
    this.quad.material=this.compositeMat;this.compositeMat.uniforms.uBloom.value=this.bloom?.24:0;
    this.renderer.setRenderTarget(null);this.renderer.render(this.postScene,this.postCamera);
    if(query){gl.endQuery(timer.TIME_ELAPSED_EXT);this.queries.push(query);}
  }
  diagnostics() { const code=this.gl.getError();return code ? `WebGL error ${code}` : null; }
  simulateLoss() { this.gl.getExtension('WEBGL_lose_context')?.loseContext(); }
  info() {
    const q=B_QUALITY[this.quality];
    const {fps,...settings}=q;
    return {method:'Three.js r180 / WebGL2',quality:this.quality,...settings,targetFps:fps,resolution:[this.canvas.width,this.canvas.height],
      veils:5,innerFilaments:4,bloom:!!this.bloom,bloomResolution:[this.blurA.width,this.blurA.height],target:this.targetType,
      drawCalls:this.renderer.info.render.calls,triangles:this.renderer.info.render.triangles,
      gpu:this.gpu,gpuTimer:this.timer?'EXT_disjoint_timer_query_webgl2':'unavailable',cpuGpuUtilization:'not measured'};
  }
  dispose() {
    this.canvas.removeEventListener('webglcontextlost',this.lost);
    for(const child of this.scene.children){child.geometry.dispose();child.material.dispose();}
    for(const q of this.queries)this.gl.deleteQuery(q);
    this.sceneTarget.dispose();this.blurA.dispose();this.blurB.dispose();this.blurMat.dispose();this.compositeMat.dispose();this.quad.geometry.dispose();
    this.renderer.dispose();
    if(!this.gl.isContextLost())this.renderer.forceContextLoss();
  }
}
