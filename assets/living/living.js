/* Living art: a WebGL layer over the page pictures. Only what moves on purpose: the waterfall, banners and plants in the
   wind, clouds, mist, god rays and dust in the air, and the campfire at the bottom of the home page.
   A picture opts in with data-fx="dawn|camp|road|roster|tools|guides|dungeons|professions|faq|news|leveling|classes|races|ukrainian|bestrace|tierlist" on its <picture>, data-cut its phone cut (make_images.CUTS, default .6); masks are assets/living/<art>-fx.png (tools/make_living.py),
   in the 1376 x 768 grid of the source art. The canvas is transparent except where something moves, so the sharp <img>
   stays visible underneath. Off with prefers-reduced-motion, Save-Data, ?fx=off, without WebGL or on a device too slow for it;
   paused off screen, rebuilt after a lost WebGL context.
   Follows the time of day (assets/tod/tod.js): sun position, rays and dust by day. */
(() => {
  const me = document.currentScript;
  if (!me || matchMedia('(prefers-reduced-motion: reduce)').matches || (navigator.connection || {}).saveData || /[?&]fx=off\b/.test(location.search)) return;
  const base = me.src.replace(/living\.js.*$/, '');
  const ver = (me.src.match(/\?v=\w+/) || [''])[0];
  const ART = { dawn: 'hero_dawn', camp: 'hero_campfire', road: 'hero_road', roster: 'hero_roster', tools: 'hero_tools',
    guides: 'hero_guides', dungeons: 'hero_dungeons', professions: 'hero_professions', faq: 'hero_faq', news: 'hero_news',
    leveling: 'hero_leveling', classes: 'hero_classes', races: 'hero_races', ukrainian: 'hero_ukrainian',
    bestrace: 'hero_bestrace', tierlist: 'hero_tierlist' };
  const FPS = matchMedia('(pointer: coarse)').matches ? 30 : 60;
  const FORCE = /[?&]fx=force\b/.test(location.search);   // screenshots in headless Chrome

  const VS = 'attribute vec2 a;varying vec2 vUv;void main(){vUv=vec2(a.x*.5+.5,.5-a.y*.5);gl_Position=vec4(a,0.,1.);}';

  const COMMON = `
precision highp float;
varying vec2 vUv;
uniform sampler2D uImg, uMask;
uniform vec2 uSize;   // canvas, css px
uniform vec4 uMap;    // picture box inside the canvas: offset, size (css px)
uniform vec4 uCrop;   // part of the source art in this file: offset, size (0..1)
uniform float uT, uPx; // seconds; css px per art px
uniform float uTod;   // 0 dawn, 1 day, 2 dusk, 3 night (assets/tod/tod.js)
uniform vec2 uSun;    // sun or moon of this variant, art px
const vec2 ART = vec2(1376., 768.);
vec4 acc; vec3 add;
float h21(vec2 p) { p = fract(p * vec2(123.34, 456.21)); p += dot(p, p + 45.32); return fract(p.x * p.y); }
float n2(vec2 p) { vec2 i = floor(p), f = fract(p); f = f * f * (3. - 2. * f);
  return mix(mix(h21(i), h21(i + vec2(1., 0.)), f.x), mix(h21(i + vec2(0., 1.)), h21(i + 1.), f.x), f.y); }
float fbm(vec2 p) { float s = 0., a = .5; for (int i = 0; i < 4; i++) { s += a * n2(p); p = p * 2.03 + 17.1; a *= .5; } return s; }
vec3 img(vec2 P) { return texture2D(uImg, (P / ART - uCrop.xy) / uCrop.zw).rgb; }
vec4 mask(vec2 P) { return texture2D(uMask, P / ART); }
// Texture flowing along d (art px per period): two phases cross-fade so the loop never jumps.
vec3 flow(vec2 P, vec2 d, float period, float jit) {
  float f1 = fract(uT / period + jit), f2 = fract(f1 + .5);
  return mix(img(P - d * f1), img(P - d * f2), abs(2. * f1 - 1.));
}
// Clouds: flow, but a sample that lands on something else (a pole, a sign, a bow the sky mask brushes) keeps the
// still pixel, or the layer paints a shifted copy of it beside the original.
vec3 drift(vec2 P, vec2 d, float period) {
  float f1 = fract(uT / period), f2 = fract(f1 + .5);
  vec3 c = img(P), a = img(P - d * f1), b = img(P - d * f2);
  a = mix(a, c, smoothstep(.05, .14, length(a - c)));
  b = mix(b, c, smoothstep(.05, .14, length(b - c)));
  return mix(a, b, abs(2. * f1 - 1.));
}
void over(vec3 c, float w) { acc = vec4(c * w + acc.rgb * (1. - w), w + acc.a * (1. - w)); }
float dot1(vec2 P, vec2 c, float r) { return smoothstep(r, 0., length(P - c) * uPx); }  // r in css px
float isT(float t) { return 1. - step(.5, abs(uTod - t)); }
vec2 artPx() { return (uCrop.xy + (vUv * uSize - uMap.xy) / uMap.zw * uCrop.zw) * ART; }
`;

  // The newer scenes: everything comes from the mask (tools/make_living.py), nothing is placed by hand.
  const GEN = `
void main() {
  vec2 P = artPx(); acc = vec4(0.); add = vec3(0.);
  vec4 m = mask(P);
  // clouds drift slowly to the left
  if (m.b > .01) over(drift(P, vec2(-8., 0.) + (n2(P * .006 + uT * .03) - .5) * vec2(5., 2.), 12.), m.b);
  // plants and hanging cloth sway in a light wind
  if (m.g > .01) {
    float w = m.g, ph = P.x * .02 + uT * 1.1;
    vec2 off = vec2(sin(ph) * 1.6 + sin(uT * .7 + P.y * .03) * .7, sin(ph * 1.3) * .5) * w;
    over(img(P - off), smoothstep(0., .1, w));
  }
  gl_FragColor = vec4(acc.rgb + add, acc.a);
}`;

  const SCENES = {
    roster: GEN, tools: GEN, guides: GEN, dungeons: GEN, professions: GEN, faq: GEN, news: GEN,
    leveling: GEN, classes: GEN, races: GEN, ukrainian: GEN, bestrace: GEN, tierlist: GEN,
    dawn: `
void main() {
  vec2 P = artPx(); acc = vec4(0.); add = vec3(0.);
  vec4 m = mask(P);
  // sky: clouds sail slowly to the left
  if (m.b > .01) {
    vec2 d = vec2(-9., 0.) + (vec2(n2(P * .006 + uT * .03), n2(P * .006 - 7.)) - .5) * vec2(5., 3.);
    over(drift(P, d, 11.), m.b);
  }
  // falling water
  if (m.r > .01) {
    vec3 c = flow(P, vec2(0., 18.), .8, n2(vec2(P.x * .25, 0.)));
    float s = n2(vec2(P.x * .45, P.y * .045 - uT * 7.));
    c += vec3(.9, .95, 1.) * smoothstep(.62, 1., s) * .2;
    over(c, m.r);
  }
  // banners in the wind
  if (m.g > .01) {
    float w = m.g, ph = P.x * .045 - uT * 3.2;
    vec2 off = vec2(sin(ph + 1.) * .8, sin(ph) * 2.6 + sin(P.x * .11 - uT * 5.1) * 1.1) * w;
    // the folds catch the light on the cloth only: the mask is grown 3 px around it, and shading that margin
    // would put a light or dark rim on the sky beside the banner
    vec2 S = P - off;
    float ws = mask(S).g, core = min(min(mask(S + vec2(3.5, 0.)).g, mask(S - vec2(3.5, 0.)).g), min(mask(S + vec2(0., 3.5)).g, mask(S - vec2(0., 3.5)).g));
    over(img(S) * (1. + .14 * w * cos(ph) * smoothstep(.55, .9, core / max(ws, .01))), smoothstep(.0, .12, w));
  }
  // mist in the valley and under the falls
  float band = smoothstep(420., 470., P.y) * smoothstep(650., 590., P.y) * smoothstep(680., 580., P.x);
  float fog = smoothstep(.48, .9, fbm(P * vec2(.006, .013) + vec2(uT * .022, 0.))) * band * .26;
  float spray = fbm(P * .03 - vec2(0., uT * .35)) * smoothstep(1., .2, length((P - vec2(480., 618.)) / vec2(60., 22.)));
  over(mix(vec3(.86, .89, .93), vec3(.55, .62, .78), isT(3.)), clamp(fog * (1. + isT(3.) * .5) + spray * .5, 0., .6));
  // god rays from the sun: soft by day (it is above the frame), warm at sunset, none at night
  vec2 v = P - uSun;
  float ang = atan(v.y, v.x), r = length(v);
  float ray = n2(vec2(ang * 9., uT * .07)) * n2(vec2(ang * 23., -uT * .05));
  add += mix(vec3(1., .86, .6), vec3(1., .66, .38), isT(2.)) * pow(ray, 2.) * smoothstep(720., 60., r) * .11 * (isT(0.) + isT(1.) * .5 + isT(2.) * 1.1);
  // dust in the sunlight
  for (int i = 0; i < 26; i++) {
    float fi = float(i), h = h21(vec2(fi, 3.1)), k = h21(vec2(fi, 9.7));
    float life = fract(uT * (.025 + k * .03) + h);
    vec2 c = vec2(40. + h * 720. + sin(uT * .6 + fi) * 14. + life * 60., 600. - life * 470.);
    float tw = sin(life * 3.1416) * (.55 + .45 * sin(uT * (1.5 + k * 2.) + fi)) * smoothstep(780., 150., length(c - uSun)) * (isT(0.) + isT(2.) * .5);
    add += vec3(1., .88, .62) * dot1(P, c, 1.4 + k * 1.6) * tw * .7;
  }
  gl_FragColor = vec4(acc.rgb + add, acc.a);
}`,
    camp: `
void main() {
  vec2 P = artPx(); acc = vec4(0.); add = vec3(0.);
  vec4 m = mask(P);
  if (m.b > .01) over(drift(P, vec2(-6., 0.) + (n2(P * .006 + uT * .03) - .5) * vec2(4., 2.), 12.), m.b);
  // mist over the valley
  float band = smoothstep(380., 430., P.y) * smoothstep(620., 560., P.y) * smoothstep(580., 460., P.x);
  over(vec3(.62, .64, .78), smoothstep(.5, .9, fbm(P * vec2(.006, .014) + vec2(uT * .02, 0.))) * band * .25);
  // the campfire
  float fl = .55 + .45 * (n2(vec2(uT * 7., 0.)) * .6 + n2(vec2(uT * 13., 4.)) * .4);
  if (m.r > .01) over(flow(P, vec2(0., -10.), .42, n2(vec2(P.x * .15, 0.))) * (.9 + .35 * fl), m.r);
  gl_FragColor = vec4(acc.rgb + add, acc.a);
}`,
    road: `
void main() {
  vec2 P = artPx(); acc = vec4(0.); add = vec3(0.);
  vec4 m = mask(P);
  if (m.b > .01) over(drift(P, vec2(-5., 0.) + (n2(P * .006 + uT * .03) - .5) * vec2(4., 2.), 13.), m.b);
  // mist drifting through the valleys
  float band = smoothstep(330., 380., P.y) * smoothstep(520., 450., P.y) * smoothstep(760., 660., P.x);
  over(vec3(.6, .66, .78), smoothstep(.5, .9, fbm(P * vec2(.005, .013) + vec2(uT * .02, 0.))) * band * .3);
  gl_FragColor = vec4(acc.rgb + add, acc.a);
}`
  };

  function shader(gl, type, src) {
    const s = gl.createShader(type);
    gl.shaderSource(s, src);
    gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s));
    return s;
  }

  function texture(gl, unit, src, t) {
    t = t || gl.createTexture();
    gl.activeTexture(gl.TEXTURE0 + unit);
    gl.bindTexture(gl.TEXTURE_2D, t);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, src);
    for (const [k, v] of [[gl.TEXTURE_MIN_FILTER, gl.LINEAR], [gl.TEXTURE_MAG_FILTER, gl.LINEAR], [gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE], [gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE]])
      gl.texParameteri(gl.TEXTURE_2D, k, v);
    return t;
  }

  function ready(img) {
    return img.complete && img.naturalWidth ? Promise.resolve() : new Promise(r => img.addEventListener('load', r, { once: true }));
  }

  // phones get a portrait cut of the art (tools/make_images.py hero_mobile)
  const phone = s => /hero_\w+-m-/.test(s);

  function live(pic) {
    const scene = pic.dataset.fx, img = pic.querySelector('img'), cut = parseFloat(pic.dataset.cut || '.6');
    const SUN = { dawn: [635, 340], day: [632, 304], dusk: [634, 347], night: [641, 346] };   // measured on the aligned art (tools/align_tod.py)
    const TOD = { dawn: 0, day: 1, dusk: 2, night: 3 };
    const tod = () => (window.GabellaTod && window.GabellaTod.now) || (scene === 'dawn' ? 'dawn' : 'dusk');   // camp and road are evening scenes
    if (!SCENES[scene] || !img) return;
    const cv = document.createElement('canvas');
    cv.className = 'fx';
    cv.setAttribute('aria-hidden', 'true');
    const gl = cv.getContext('webgl', { alpha: true, premultipliedAlpha: true, antialias: false, depth: false, powerPreference: 'low-power' });
    if (!gl) return;
    // Software WebGL (no GPU: weak devices, page-speed robots) would stall the page compiling the shader.
    const dbg = gl.getExtension('WEBGL_debug_renderer_info');
    if (dbg && /swiftshader|llvmpipe|software|basic render/i.test(gl.getParameter(dbg.UNMASKED_RENDERER_WEBGL)) && !FORCE) return;
    const U = {};
    let tex = null;
    // program, geometry and textures: once at the start and again after a lost context comes back
    function setup() {
      let prog;
      try {
        prog = gl.createProgram();
        gl.attachShader(prog, shader(gl, gl.VERTEX_SHADER, VS));
        gl.attachShader(prog, shader(gl, gl.FRAGMENT_SHADER, COMMON + SCENES[scene]));
        gl.linkProgram(prog);
        if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(prog));
      } catch (e) { return false; }
      gl.useProgram(prog);
      gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer());
      gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
      gl.enableVertexAttribArray(0);
      gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0);
      for (const n of ['uImg', 'uMask', 'uSize', 'uMap', 'uCrop', 'uT', 'uPx', 'uTod', 'uSun']) U[n] = gl.getUniformLocation(prog, n);
      gl.uniform1i(U.uImg, 0);
      gl.uniform1i(U.uMask, 1);
      tex = null;
      upload();
      texture(gl, 1, mk);
      return true;
    }

    const mk = new Image();
    mk.src = base + ART[scene] + '-fx.png' + ver;
    let on = false, shown = false, raf = 0, last = 0, lost = false;
    let src = '', iw = 0, ih = 0;   // the picture in the texture: its address and size
    let want = '', hold = false;    // a new picture on its way (another width or time of day); hold: the old one does not fit it
    let n = 0, t1 = 0, slow = 0;    // frame rate check
    const t0 = performance.now() - Math.random() * 20000;

    function layout() {
      const w = cv.clientWidth, h = cv.clientHeight;
      if (!w || !h || !iw) return false;
      const k = Math.min(devicePixelRatio || 1, 1.5, Math.sqrt(3.2e6 / (w * h)));
      cv.width = Math.round(w * k);
      cv.height = Math.round(h * k);
      gl.viewport(0, 0, cv.width, cv.height);
      const s = Math.max(w / iw, h / ih);
      const pos = getComputedStyle(img).objectPosition.split(' ').map(v => parseFloat(v) / 100);
      const dw = iw * s, dh = ih * s;
      // the phone cut is .43605 of the width, at data-cut of the rest
      const crop = phone(src) ? [cut * (1 - .43605), 0, .43605, 1] : [0, 0, 1, 1];
      gl.uniform2f(U.uSize, w, h);
      gl.uniform4f(U.uMap, (w - dw) * (isNaN(pos[0]) ? .5 : pos[0]), (h - dh) * (isNaN(pos[1]) ? .5 : pos[1]), dw, dh);
      gl.uniform4f(U.uCrop, ...crop);
      gl.uniform1f(U.uPx, dw / (crop[2] * 1376));
      return true;
    }

    function upload() {
      src = img.currentSrc;
      iw = img.naturalWidth;
      ih = img.naturalHeight;
      tex = texture(gl, 0, img, tex);
    }

    // The browser picks another file for a new window width before it has loaded: currentSrc changes while the
    // picture is still coming, and uploading it then leaves an empty texture (black sky, banner, waterfall).
    // Keep the old texture until the new file is decoded.
    function swap(next) {
      want = next;
      hold = phone(next) !== phone(src);
      img.decode().catch(() => {}).then(() => {
        if (want !== next || lost) return;   // an even newer file is on its way
        if (img.currentSrc !== next) { want = ''; hold = false; return; }
        if (!img.complete || !img.naturalWidth) return;   // broken: stay on the old one
        want = '';
        hold = false;
        upload();
        layout();
      });
    }

    function frame(now) {
      raf = 0;
      if (!on || document.hidden) return;
      raf = requestAnimationFrame(frame);
      if (now - last < 1000 / FPS - 2) return;
      const gap = now - last;
      last = now;
      const cur = img.currentSrc;
      if (cur && cur !== src && cur !== want) swap(cur);
      if (hold) { gl.clear(gl.COLOR_BUFFER_BIT); return; }
      gl.uniform1f(U.uT, ((now - t0) / 1000) % 3600);
      const t = tod();
      gl.uniform1f(U.uTod, TOD[t]);
      gl.uniform2f(U.uSun, ...SUN[t]);
      gl.drawArrays(gl.TRIANGLES, 0, 3);
      if (!shown && !want) { shown = true; requestAnimationFrame(() => cv.classList.add('on')); }
      // A device that cannot keep up gets the still picture: under half the frame rate for two 4 s spans in a row.
      if (gap > 500) { n = 0; t1 = now; return; }   // back from a pause
      if (++n, now - t1 < 4000) return;
      slow = n * 1000 / (now - t1) < FPS * .45 ? slow + 1 : 0;
      n = 0;
      t1 = now;
      if (slow >= 2) { on = false; lost = true; cv.remove(); }
    }

    function run(v) {
      on = v && !lost;
      if (on && !raf) { t1 = performance.now(); n = 0; raf = requestAnimationFrame(frame); }
    }

    Promise.all([ready(img), mk.decode()]).then(() => {
      pic.appendChild(cv);
      if (!setup() || !layout()) return;
      new ResizeObserver(() => layout()).observe(cv);
      let seen = false;
      new IntersectionObserver(es => run(seen = es[0].isIntersecting)).observe(pic);
      document.addEventListener('visibilitychange', () => run(on));
      // Phones drop the context in the background: keep the canvas, rebuild everything when it comes back.
      cv.addEventListener('webglcontextlost', e => { e.preventDefault(); lost = true; on = false; shown = false; cv.classList.remove('on'); });
      cv.addEventListener('webglcontextrestored', () => {
        if (!cv.isConnected) return;
        lost = false;
        want = '';
        hold = false;
        if (!setup() || !layout()) { lost = true; cv.remove(); return; }
        run(seen);
      });
      document.addEventListener('gabella:tod-start', () => cv.classList.remove('on'));
      document.addEventListener('gabella:tod', () => { shown = false; });   // the next frame uploads the new picture once decoded and fades in
    }).catch(() => {});
  }

  // Starts on the first sign of a person (pointer, touch, scroll, key): page-speed robots never pay for WebGL.
  const start = () => document.querySelectorAll('picture[data-fx]').forEach(live);
  // a busy page (the tools search index) may not go idle for long: start anyway after 1.5 s
  const idle = window.requestIdleCallback ? f => requestIdleCallback(f, { timeout: 1500 }) : f => setTimeout(f, 200);
  const WAKE = ['pointermove', 'pointerdown', 'touchstart', 'wheel', 'scroll', 'keydown'];
  const wake = () => { WAKE.forEach(e => removeEventListener(e, wake, true)); idle(start); };
  const arm = () => FORCE ? idle(start) : WAKE.forEach(e => addEventListener(e, wake, { capture: true, passive: true }));
  if (document.readyState === 'complete') arm();
  else addEventListener('load', arm, { once: true });
})();
