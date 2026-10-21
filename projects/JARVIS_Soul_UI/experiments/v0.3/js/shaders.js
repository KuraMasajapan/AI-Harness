// Original shaders. No reference artwork/source is copied.
export const field = /* glsl */`
uniform float uTime;
uniform vec4 uState; // Listening, Processing, Speaking, Attention; smoothed
uniform float uAudio;
float wave(float t) { return .48 + .26*sin(t*2.3) + .16*sin(t*4.1+.8) + .1*sin(t*7.3); }
vec3 flow(float u, float seed, float spread) {
  float t = uTime;
  float envelope = pow(max(.001,sin(u*3.141593)), .63);
  float speech = uState.z*(.05+.12*wave(t)) + uAudio*.1*uState.x;
  float radius = (.43 + .56*fract(seed*.618)) * envelope;
  radius *= (1. + .12*uState.x*smoothstep(.3,.8,spread) - .22*uState.y - .16*uState.w + speech);
  radius *= 1. + uState.z*.1*sin(u*9.-t*2.3);
  radius *= spread * (1. + .027*sin(t*.65));
  float angle = seed*2.399 + u*4.4 + .8*sin(u*5.4+seed*.8) + t*.07;
  angle += .35*uState.y*sin(u*5.-t*.45);
  float y = (u-.5)*(1.9+.65*fract(seed*.57)) + .19*sin(u*8.+seed)*envelope + .17*sin(seed*2.1);
  float x = radius*cos(angle) + .25*sin(u*7.+t*.12)*envelope;
  float z = radius*sin(angle)*.9 + .16*sin(u*9.+seed*.5);
  x += .06*sin(u*19.+seed*1.7+t*.13)*envelope;
  y *= 1. + .08*uState.w + .045*uState.z*wave(t);
  return vec3(x,y,z);
}
vec3 lightColor(float depth, float seed) {
  vec3 farColor = mix(vec3(.26,.46,.75),vec3(.46,.4,.68),step(.85,fract(seed*.37)));
  return mix(farColor,vec3(.73,.93,1.),smoothstep(-.8,.7,depth));
}
`;

export const ribbonVertex = /* glsl */`
${field}
attribute vec4 aFlow; // u, side, seed, veil flag
varying vec2 vRibbon;
varying vec3 vColor;
varying float vLight;
varying float vVeil;
varying float vSeed;
void main() {
  float u = aFlow.x, seed = aFlow.z, inner = step(1.5,aFlow.w);
  float veil = step(.5,aFlow.w)*(1.-inner);
  float spread=mix(1.,.38,inner);
  vec3 p = flow(u,seed,spread);
  vec3 q = flow(min(.999,u+.002),seed,spread);
  p.y*=mix(1.,.72,inner); q.y*=mix(1.,.72,inner);
  vec3 tangent = normalize(q-p+vec3(.00001));
  vec3 side = normalize(cross(tangent,vec3(0.,0.,1.)));
  float width = mix(.034,.23,veil) * (.7+.3*sin(u*8.+seed));
  p += side*aFlow.y*width;
  vRibbon = vec2(u,aFlow.y);
  vColor = mix(lightColor(p.z,seed),vec3(.8,.96,1.),inner*.7);
  float tips = smoothstep(.01,.18,u)*(1.-smoothstep(.82,1.,u));
  float gaps = .36+.64*pow(.5+.5*sin(u*18.+seed+uTime*.16),2.);
  vLight = tips*gaps*mix(.42,1.65,smoothstep(-.8,.8,p.z))*mix(1.,.36,veil);
  vVeil=veil; vSeed=seed;
  gl_Position = projectionMatrix*modelViewMatrix*vec4(p,1.);
}
`;
export const ribbonFragment = /* glsl */`
varying vec2 vRibbon;
varying vec3 vColor;
varying float vLight;
varying float vVeil;
varying float vSeed;
uniform float uTime;
uniform vec4 uState;
void main() {
  float across=vRibbon.y + vVeil*.13*sin(vRibbon.x*26.+vSeed+uTime*.1);
  float d = across*across;
  float fiber=.55+.45*sin(across*38.+vRibbon.x*14.+vSeed);
  float softness = mix(exp(-d*38.)+.16*exp(-d*4.5),exp(-d*4.)*(.5+.5*fiber),vVeil);
  float cadence=1.+uState.z*.26*sin(uTime*2.3-vRibbon.x*5.);
  float alpha = softness*vLight*.34*cadence;
  gl_FragColor = vec4(vColor,alpha);
}
`;
export const pointVertex = /* glsl */`
${field}
attribute vec4 aSeed;
uniform float uPixelScale;
varying vec3 vColor;
varying float vAlpha;
void main() {
  float seed = aSeed.y, ambient = step(.92,aSeed.w), inner = 1.-step(.24,aSeed.w);
  float u = fract(aSeed.x + uTime*(.013+.009*fract(seed*.71)));
  vec3 p = flow(u,seed,mix(1. + .2*sin(seed*4.),.4,inner));
  p.y*=mix(1.,.78,inner);
  float jitter = mix(.075,.55,ambient);
  p += jitter*vec3(sin(seed*42.+uTime*.11),cos(seed*36.+uTime*.09),sin(seed*71.));
  p.x += ambient*sign(sin(seed))* .35;
  vec4 mv = modelViewMatrix*vec4(p,1.);
  float nearLight = smoothstep(-.85,.85,p.z);
  vColor = lightColor(p.z,seed);
  float tips = smoothstep(.02,.17,u)*(1.-smoothstep(.8,.98,u));
  vAlpha = (.17+.42*pow(aSeed.z,3.))*mix(.3,1.,nearLight)*tips*mix(1.,.3,ambient);
  gl_PointSize = clamp((2.+5.*pow(aSeed.z,4.))*uPixelScale*5.5/-mv.z,1.8,12.);
  gl_Position = projectionMatrix*mv;
}
`;
export const pointFragment = /* glsl */`
varying vec3 vColor;
varying float vAlpha;
void main() {
  vec2 uv = gl_PointCoord*2.-1.;
  float r2 = dot(uv,uv);
  if(r2>1.) discard;
  float a = exp(-r2*5.)*(1.-smoothstep(.65,1.,r2))*vAlpha;
  gl_FragColor = vec4(vColor,a);
}
`;
export const fullscreenVertex = /* glsl */`
varying vec2 vUv;
void main(){vUv=uv;gl_Position=vec4(position.xy,0.,1.);}
`;
export const blurFragment = /* glsl */`
uniform sampler2D tInput;
uniform vec2 uStep;
uniform float uThreshold;
varying vec2 vUv;
vec3 sampleLight(vec2 uv){
  vec3 c=texture2D(tInput,uv).rgb;
  float peak=max(c.r,max(c.g,c.b));
  return c*smoothstep(uThreshold,uThreshold+.16,peak);
}
void main(){
  vec3 c=sampleLight(vUv)*.227027;
  c+=sampleLight(vUv+uStep*1.384615)*.316216;
  c+=sampleLight(vUv-uStep*1.384615)*.316216;
  c+=sampleLight(vUv+uStep*3.230769)*.070270;
  c+=sampleLight(vUv-uStep*3.230769)*.070270;
  gl_FragColor=vec4(c,1.);
}
`;
export const compositeFragment = /* glsl */`
uniform sampler2D tScene;
uniform sampler2D tBloom;
uniform float uBloom;
varying vec2 vUv;
void main(){
  vec3 c=texture2D(tScene,vUv).rgb + texture2D(tBloom,vUv).rgb*uBloom;
  c=pow(1.-exp(-c*1.45),vec3(.7));
  float alpha=clamp(max(c.r,max(c.g,c.b)),0.,.94);
  gl_FragColor=vec4(c/max(alpha,.00001),alpha);
}
`;
