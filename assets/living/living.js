/* Living art: a WebGL layer over the home page pictures — falling water, banners in the wind, drifting sky, mist,
   god rays, dust and birds at dawn; fire, firelight, embers, smoke and stars at the camp; lantern, gate, river and mist on the road;
   hearth, candles, banners, haze and stars in the guild hall (roster); clouds, lake, mist, banner, lantern and birds in the war tent (tools);
   guide heroes: clouds, river, mist, pennant and birds on the pass (guides); gate, mist, stream, fires and stars by the dungeon (dungeons);
   forge, anvil sparks, steam, herbs, potion and rune in the workshop (professions); sunbeam, dust, banners and candles in the library (faq).
   A picture opts in with data-fx="dawn|camp|road|roster|tools|guides|dungeons|professions|faq" on its <picture>, data-cut its phone cut (make_images.CUTS, default .6); masks are assets/living/<art>-fx.png (tools/make_living.py),
   in the 1376 x 768 grid of the source art. The canvas is transparent except where something moves, so the sharp <img>
   stays visible underneath. Off with prefers-reduced-motion, Save-Data or without WebGL; paused off screen.
   Follows the time of day (assets/tod/tod.js): sun position, rays, birds by day; stars, fireflies and moon glints at night. */
(() => {
  const me = document.currentScript;
  if (!me || matchMedia('(prefers-reduced-motion: reduce)').matches || (navigator.connection || {}).saveData) return;
  const base = me.src.replace(/living\.js.*$/, '');
  const ver = (me.src.match(/\?v=\w+/) || [''])[0];
  const ART = { dawn: 'hero_dawn', camp: 'hero_campfire', road: 'hero_road', roster: 'hero_roster', tools: 'hero_tools',
    guides: 'hero_guides', dungeons: 'hero_dungeons', professions: 'hero_professions', faq: 'hero_faq' };
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
float box(vec2 P, vec4 b, float e) { return smoothstep(b.x - e, b.x, P.x) * smoothstep(b.z + e, b.z, P.x) * smoothstep(b.y - e, b.y, P.y) * smoothstep(b.w + e, b.w, P.y); }
vec3 img(vec2 P) { return texture2D(uImg, (P / ART - uCrop.xy) / uCrop.zw).rgb; }
vec4 mask(vec2 P) { return texture2D(uMask, P / ART); }
// Texture flowing along d (art px per period): two phases cross-fade so the loop never jumps.
vec3 flow(vec2 P, vec2 d, float period, float jit) {
  float f1 = fract(uT / period + jit), f2 = fract(f1 + .5);
  return mix(img(P - d * f1), img(P - d * f2), abs(2. * f1 - 1.));
}
void over(vec3 c, float w) { acc = vec4(c * w + acc.rgb * (1. - w), w + acc.a * (1. - w)); }
float dot1(vec2 P, vec2 c, float r) { return smoothstep(r, 0., length(P - c) * uPx); }  // r in css px
float seg(vec2 p, vec2 a, vec2 b) { vec2 pa = p - a, ba = b - a; return length(pa - ba * clamp(dot(pa, ba) / dot(ba, ba), 0., 1.)); }
float bird(vec2 P, vec2 c, float s, float flap) {
  vec2 q = (P - c) / s; q.x = abs(q.x);
  float d = min(seg(q, vec2(0.), vec2(1., -.35 - flap)), seg(q, vec2(1., -.35 - flap), vec2(2., -.1 - flap * 1.4)));
  return smoothstep(.9 / (s * uPx) + .12, .12, d);
}
float isT(float t) { return 1. - step(.5, abs(uTod - t)); }
float stars(vec2 P, float cellSize, float th, float k) {
  vec2 cell = floor(P / cellSize), sp = (cell + .2 + .6 * vec2(h21(cell + 1.3), h21(cell + 7.1))) * cellSize;
  float hs = h21(cell);
  return hs > th ? dot1(P, sp, 1.5 + (hs - th) * 14.) * (.45 + .55 * sin(uT * (.8 + hs * 3.) + hs * 50.)) * k : 0.;
}
vec3 fireflies(vec2 P, vec4 area, int n) {
  vec3 s = vec3(0.);
  for (int i = 0; i < 14; i++) {
    if (i >= n) break;
    float fi = float(i), h = h21(vec2(fi, 2.9)), k = h21(vec2(fi, 8.1));
    vec2 c = area.xy + vec2(h, k) * (area.zw - area.xy) + vec2(sin(uT * (.3 + k * .4) + fi), cos(uT * (.25 + h * .3) + fi * 1.3)) * 14.;
    s += vec3(.85, 1., .6) * dot1(P, c, 1.6 + k) * pow(.5 + .5 * sin(uT * (1.2 + h) + fi * 2.), 3.) * .9;
  }
  return s;
}
vec2 artPx() { return (uCrop.xy + (vUv * uSize - uMap.xy) / uMap.zw * uCrop.zw) * ART; }
`;

  const SCENES = {
    dawn: `
void main() {
  vec2 P = artPx(); acc = vec4(0.); add = vec3(0.);
  // floating islands drift up and down a little
  float wb = box(P, vec4(598., 150., 752., 338.), 14.);  // stops short of the banner pole
  vec2 Pb = P - vec2(0., sin(uT * .55) * 1.6 * wb);
  vec4 m = mask(Pb);
  if (wb > 0.) over(img(Pb), wb);
  // sky: clouds sail slowly to the left
  if (m.b > .01) {
    vec2 d = vec2(-9., 0.) + (vec2(n2(P * .006 + uT * .03), n2(P * .006 - 7.)) - .5) * vec2(5., 3.);
    over(flow(P, d, 11., 0.), m.b);
  }
  // falling water
  if (m.r > .01) {
    vec3 c = flow(Pb, vec2(0., 18.), .8, n2(vec2(Pb.x * .25, 0.)));
    float s = n2(vec2(Pb.x * .45, Pb.y * .045 - uT * 7.));
    c += vec3(.9, .95, 1.) * smoothstep(.62, 1., s) * .2;
    over(c, m.r);
  }
  // river winds down the valley, with glints
  if (m.a > .01) {
    vec3 c = flow(P, vec2(-6., 4.), 3., 0.);
    c += vec3(1., .95, .85) * pow(n2(P * vec2(.35, .7) + vec2(uT * .9, uT * .4)), 9.) * .9;
    over(c, m.a);
  }
  // banners in the wind
  if (m.g > .01) {
    float w = m.g, ph = P.x * .045 - uT * 3.2;
    vec2 off = vec2(sin(ph + 1.) * .8, sin(ph) * 2.6 + sin(P.x * .11 - uT * 5.1) * 1.1) * w;
    over(img(P - off) * (1. + .14 * w * cos(ph)), smoothstep(.0, .12, w));
  }
  // mist in the valley and under the falls
  float band = smoothstep(420., 470., P.y) * smoothstep(650., 590., P.y) * smoothstep(740., 640., P.x);
  float fog = smoothstep(.48, .9, fbm(P * vec2(.006, .013) + vec2(uT * .022, 0.))) * band * .26;
  float spray = fbm(P * .03 - vec2(0., uT * .35)) * smoothstep(1., .2, length((P - vec2(612., 560.)) / vec2(75., 28.)));
  spray += fbm(P * .025 - vec2(uT * .1, uT * .25)) * smoothstep(1., .2, length((P - vec2(692., 332.)) / vec2(40., 18.))) * wb;
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
  // a few birds cross the open sky left of the banner now and then
  float t0 = mod(uT + 6., 40.) / 28.;
  if (t0 < 1. && uTod < 2.5) {
    vec2 c = vec2(720. - t0 * 720., 66. + sin(t0 * 3.) * 14.);
    float b = 0.;
    for (int i = 0; i < 4; i++) {
      float fi = float(i);
      b = max(b, bird(P, c + vec2(fi * 17., mod(fi, 2.) * 9. - fi * 3.), 3.6 - fi * .3, sin(uT * 9. + fi * 1.7) * .5));
    }
    over(mix(vec3(.16, .16, .2), vec3(.08, .05, .05), isT(2.)), b * .8 * smoothstep(0., .06, t0) * smoothstep(1., .94, t0));
  }
  if (uTod > 2.5) {
    add += vec3(.9, .93, 1.) * stars(P, 16., .9, .6) * m.b;
    add += fireflies(P, vec4(500., 600., 760., 740.), 10);   // the grassy ledge in front of the heroes
    if (m.a > .01) add += vec3(.7, .8, 1.) * pow(n2(P * vec2(.3, .8) + vec2(uT * .5, 0.)), 10.) * .6 * m.a;   // moon glints
  }
  gl_FragColor = vec4(acc.rgb + add, acc.a);
}`,
    camp: `
void main() {
  vec2 P = artPx(); acc = vec4(0.); add = vec3(0.);
  vec4 m = mask(P);
  if (m.b > .01) over(flow(P, vec2(-6., 0.) + (n2(P * .006 + uT * .03) - .5) * vec2(4., 2.), 12., 0.), m.b);
  // stars
  vec2 cell = floor(P / 16.), sp = (cell + .2 + .6 * vec2(h21(cell + 1.3), h21(cell + 7.1))) * 16.;
  float hs = h21(cell);
  if (hs > .9) add += vec3(.9, .93, 1.) * dot1(P, sp, 1.6 + (hs - .9) * 14.) * (.45 + .55 * sin(uT * (.8 + hs * 3.) + hs * 50.)) * .6 * m.b * (isT(2.) + isT(3.) * 1.4);
  // river
  if (m.a > .01) {
    vec3 c = flow(P, vec2(-6., 3.), 3.2, 0.);
    c += vec3(.85, .9, 1.) * pow(n2(P * vec2(.35, .7) + vec2(-uT * .8, uT * .3)), 9.) * .7;
    over(c, m.a);
  }
  // mist over the valley
  float band = smoothstep(380., 430., P.y) * smoothstep(620., 560., P.y) * smoothstep(600., 480., P.x);
  over(vec3(.62, .64, .78), smoothstep(.5, .9, fbm(P * vec2(.006, .014) + vec2(uT * .02, 0.))) * band * .25);
  // fire
  float fl = .55 + .45 * (n2(vec2(uT * 7., 0.)) * .6 + n2(vec2(uT * 13., 4.)) * .4);
  if (m.r > .01) over(flow(P, vec2(0., -10.), .42, n2(vec2(P.x * .15, 0.))) * (.9 + .35 * fl), m.r);
  vec2 F = vec2(935., 590.);
  float L = smoothstep(320., 0., length((P - F) * vec2(1., 1.35)));
  L *= L;
  add += img(P) * vec3(1., .55, .22) * L * fl * .32;
  over(vec3(0.), L * (1. - fl) * .1);
  // smoke above the pot
  float sw = 14. + (490. - P.y) * .22, sx = P.x - 940. - (490. - P.y) * .12;
  float sm = smoothstep(.45, .85, fbm(vec2(P.x * .03, P.y * .02 + uT * .55))) * smoothstep(sw, 0., abs(sx))
           * smoothstep(498., 475., P.y) * smoothstep(380., 450., P.y);
  over(vec3(.5, .5, .56), sm * .14);
  // embers
  for (int i = 0; i < 22; i++) {
    float fi = float(i), h = h21(vec2(fi, 1.7)), k = h21(vec2(fi, 5.3));
    float life = fract(uT / (1.8 + k * 2.2) + h);
    vec2 c = vec2(F.x + (h - .5) * 60. + sin(life * 6. + h * 20.) * 9. * life + life * 26., 586. - life * (130. + k * 140.));
    vec3 col = mix(vec3(1., .85, .45), vec3(1., .35, .08), life);
    add += col * dot1(P, c, 1.3 + k * 1.4) * pow(1. - life, 1.4) * 1.3;
  }
  if (uTod > 2.5) add += fireflies(P, vec4(200., 560., 1300., 740.), 9);
  gl_FragColor = vec4(acc.rgb + add, acc.a);
}`,
    road: `
void main() {
  vec2 P = artPx(); acc = vec4(0.); add = vec3(0.);
  vec4 m = mask(P);
  if (m.b > .01) over(flow(P, vec2(-5., 0.) + (n2(P * .006 + uT * .03) - .5) * vec2(4., 2.), 13., 0.), m.b);
  // stars
  vec2 cell = floor(P / 18.), sp = (cell + .2 + .6 * vec2(h21(cell + 1.3), h21(cell + 7.1))) * 18.;
  float hs = h21(cell);
  if (hs > .92) add += vec3(.9, .93, 1.) * dot1(P, sp, 1.5 + (hs - .92) * 16.) * (.45 + .55 * sin(uT * (.8 + hs * 3.) + hs * 50.)) * .55 * m.b * (isT(2.) + isT(3.) * 1.4);
  // river
  if (m.a > .01) {
    vec3 c = flow(P, vec2(6., 2.), 3.4, 0.);
    c += vec3(.8, .88, 1.) * pow(n2(P * vec2(.35, .7) + vec2(uT * .7, uT * .3)), 9.) * .7;
    over(c, m.a);
  }
  // mist drifting through the valleys
  float band = smoothstep(330., 380., P.y) * smoothstep(520., 450., P.y);
  over(vec3(.6, .66, .78), smoothstep(.5, .9, fbm(P * vec2(.005, .013) + vec2(uT * .02, 0.))) * band * .3);
  // lantern on the signpost
  float fl = .6 + .4 * (n2(vec2(uT * 6., 0.)) * .6 + n2(vec2(uT * 11., 4.)) * .4);
  vec2 Ln = vec2(1153., 222.);
  add += vec3(1., .7, .32) * (smoothstep(150., 0., length(P - Ln)) * .16 + smoothstep(16., 0., length(P - Ln)) * .35) * fl;
  add += img(P) * vec3(1., .6, .3) * smoothstep(230., 0., length((P - Ln) * vec2(1., .8))) * fl * .25;
  // the dungeon gate breathes
  vec2 G = vec2(1043., 238.);
  float pu = .5 + .5 * sin(uT * 1.3) * (.7 + .3 * n2(vec2(uT * 2., 9.)));
  add += vec3(.45, .4, 1.) * smoothstep(90., 0., length((P - G) * vec2(1., .75))) * pu * .22;
  if (uTod > 2.5) add += fireflies(P, vec4(200., 560., 1300., 740.), 9);
  gl_FragColor = vec4(acc.rgb + add, acc.a);
}`,
    roster: `
void main() {
  vec2 P = artPx(); acc = vec4(0.); add = vec3(0.);
  vec4 m = mask(P);
  // banners sway on their beams
  if (m.g > .01) {
    float w = m.g, ph = P.y * .03 - uT * 1.5;
    vec2 off = vec2(sin(ph) * 2.6 + sin(uT * .8 + P.x * .02) * 1.4, 0.) * w;
    over(img(P - off) * (1. + .1 * w * cos(ph)), smoothstep(0., .1, w));
  }
  // stars twinkle in the windows
  vec2 cell = floor(P / 14.), sp = (cell + .2 + .6 * vec2(h21(cell + 1.3), h21(cell + 7.1))) * 14.;
  float hs = h21(cell);
  if (hs > .86) add += vec3(.85, .9, 1.) * dot1(P, sp, 1.4 + (hs - .86) * 10.) * (.4 + .6 * sin(uT * (.8 + hs * 3.) + hs * 50.)) * .55 * m.b;
  // hearth fire and candle flames
  float fl = .55 + .45 * (n2(vec2(uT * 7., 0.)) * .6 + n2(vec2(uT * 13., 4.)) * .4);
  if (m.r > .01) over(flow(P, vec2(0., -9.), .45, n2(vec2(P.x * .15, 0.))) * (.9 + .35 * fl), m.r);
  vec2 F = vec2(150., 458.);
  float L = smoothstep(460., 0., length((P - F) * vec2(1., 1.2)));
  L *= L;
  add += img(P) * vec3(1., .55, .22) * L * fl * .3;
  over(vec3(0.), L * (1. - fl) * .08);
  for (int i = 0; i < 2; i++) {
    vec2 c = i == 0 ? vec2(449., 397.) : vec2(706., 404.);
    float f = .6 + .4 * n2(vec2(uT * (8. + float(i) * 3.), float(i) * 9.));
    add += vec3(1., .7, .35) * (smoothstep(70., 0., length(P - c)) * .1 + smoothstep(7., 0., length(P - c)) * .25) * f;
  }
  // smoke from the hearth drifts under the beams
  float band = smoothstep(150., 260., P.y) * smoothstep(470., 360., P.y) * smoothstep(300., 460., P.x) * smoothstep(860., 700., P.x);
  over(vec3(.5, .5, .56), smoothstep(.5, .9, fbm(P * vec2(.008, .012) + vec2(uT * .03, -uT * .02))) * band * .2);
  // sparks out of the fire
  for (int i = 0; i < 14; i++) {
    float fi = float(i), h = h21(vec2(fi, 2.9)), k = h21(vec2(fi, 6.1));
    float life = fract(uT / (2. + k * 2.4) + h);
    vec2 c = vec2(F.x + (h - .5) * 80. + sin(life * 5. + h * 20.) * 10. * life + life * 40., 470. - life * (70. + k * 90.));
    add += mix(vec3(1., .85, .45), vec3(1., .35, .08), life) * dot1(P, c, 1.2 + k * 1.2) * pow(1. - life, 1.5) * 1.2;
  }
  // dust in the firelight
  for (int i = 0; i < 18; i++) {
    float fi = float(i), h = h21(vec2(fi, 4.4)), k = h21(vec2(fi, 8.8));
    float life = fract(uT * (.02 + k * .025) + h);
    vec2 c = vec2(230. + h * 420. + sin(uT * .5 + fi) * 16., 560. - life * 300.);
    add += vec3(1., .82, .55) * dot1(P, c, 1.2 + k * 1.3) * sin(life * 3.1416) * smoothstep(560., 120., length(c - F)) * .5;
  }
  gl_FragColor = vec4(acc.rgb + add, acc.a);
}`,
    tools: `
void main() {
  vec2 P = artPx(); acc = vec4(0.); add = vec3(0.);
  vec4 m = mask(P);
  // clouds sail over the mountains
  if (m.b > .01) over(flow(P, vec2(-7., 0.) + (n2(P * .006 + uT * .03) - .5) * vec2(4., 2.), 12., 0.), m.b);
  // the lake: ripples and the sunset path
  if (m.a > .01) {
    vec3 c = flow(P, vec2(6., 1.5), 3.4, 0.);
    float path = smoothstep(140., 0., abs(P.x - 335. + (P.y - 400.) * .1));
    c += vec3(1., .78, .6) * pow(n2(P * vec2(.3, .9) + vec2(uT * .7, uT * .25)), 8.) * (.35 + .8 * path);
    over(c, m.a);
  }
  // mist drifts between the peaks
  float band = smoothstep(280., 320., P.y) * smoothstep(420., 360., P.y) * smoothstep(90., 140., P.x) * smoothstep(700., 620., P.x);
  over(vec3(.86, .8, .8), smoothstep(.5, .9, fbm(P * vec2(.006, .014) + vec2(uT * .02, 0.))) * band * .3);
  // warm rays from the sun behind the clouds
  vec2 v = P - vec2(335., 265.);
  float ang = atan(v.y, v.x), r = length(v);
  float ray = n2(vec2(ang * 9., uT * .07)) * n2(vec2(ang * 23., -uT * .05));
  add += vec3(1., .78, .6) * pow(ray, 2.) * smoothstep(380., 40., r) * smoothstep(90., 200., P.x) * smoothstep(700., 600., P.x) * .1;
  // the banner on the tent pole
  if (m.g > .01) {
    float w = m.g, ph = P.y * .05 - uT * 2.2;
    vec2 off = vec2(sin(ph) * 2.4 + sin(uT * 1.1) * 1.2, 0.) * w;
    over(img(P - off) * (1. + .12 * w * cos(ph)), smoothstep(0., .1, w));
  }
  // lantern over the map
  float fl = .6 + .4 * (n2(vec2(uT * 6., 0.)) * .6 + n2(vec2(uT * 11., 4.)) * .4);
  vec2 Ln = vec2(1055., 128.);
  add += vec3(1., .7, .32) * (smoothstep(130., 0., length(P - Ln)) * .14 + smoothstep(18., 0., length(P - Ln)) * .3) * fl;
  add += img(P) * vec3(1., .6, .3) * smoothstep(420., 0., length((P - Ln - vec2(-60., 300.)) * vec2(.8, 1.))) * fl * .14;
  // a few birds cross the sky over the lake now and then
  float t0 = mod(uT + 9., 44.) / 30.;
  if (t0 < 1.) {
    vec2 c = vec2(160. + t0 * 470., 170. + sin(t0 * 3.) * 12.);
    float b = 0.;
    for (int i = 0; i < 3; i++) {
      float fi = float(i);
      b = max(b, bird(P, c + vec2(-fi * 16., mod(fi, 2.) * 8. - fi * 3.), 3.2 - fi * .3, sin(uT * 9. + fi * 1.7) * .5));
    }
    over(vec3(.2, .15, .17), b * .75 * smoothstep(.2, .6, m.b) * smoothstep(0., .06, t0) * smoothstep(1., .94, t0));
  }
  gl_FragColor = vec4(acc.rgb + add, acc.a);
}`,
    guides: `
void main() {
  vec2 P = artPx(); acc = vec4(0.); add = vec3(0.);
  vec4 m = mask(P);
  // clouds sail over the pass
  if (m.b > .01) over(flow(P, vec2(-8., 0.) + (n2(P * .006 + uT * .03) - .5) * vec2(5., 2.), 12., 0.), m.b);
  // the river catches the sunrise
  if (m.a > .01) {
    vec3 c = flow(P, vec2(7., 3.), 3.2, 0.);
    c += vec3(1., .93, .8) * pow(n2(P * vec2(.35, .7) + vec2(uT * .8, uT * .35)), 9.) * .9;
    over(c, m.a);
  }
  // morning mist in the valley
  float band = smoothstep(340., 380., P.y) * smoothstep(470., 420., P.y) * smoothstep(640., 520., P.x);
  over(vec3(.9, .9, .9), smoothstep(.48, .9, fbm(P * vec2(.006, .014) + vec2(uT * .022, 0.))) * band * .3);
  // the pennant on the spear
  if (m.g > .01) {
    float w = m.g, ph = P.x * .06 + uT * 3.4;
    vec2 off = vec2(sin(ph + 1.) * .8, sin(ph) * 2.4 + sin(P.x * .13 + uT * 5.) * 1.) * w;
    over(img(P - off) * (1. + .14 * w * cos(ph)), smoothstep(0., .12, w));
  }
  // rays from the sun over the valley
  vec2 v = P - vec2(240., 255.);
  float ang = atan(v.y, v.x), r = length(v);
  float ray = n2(vec2(ang * 9., uT * .07)) * n2(vec2(ang * 23., -uT * .05));
  add += vec3(1., .86, .6) * pow(ray, 2.) * smoothstep(620., 50., r) * smoothstep(760., 560., P.x) * .1;
  // a few birds cross the sky now and then
  float t0 = mod(uT + 5., 42.) / 28.;
  if (t0 < 1.) {
    vec2 c = vec2(120. + t0 * 560., 150. + sin(t0 * 3.) * 14.);
    float b = 0.;
    for (int i = 0; i < 4; i++) {
      float fi = float(i);
      b = max(b, bird(P, c + vec2(-fi * 17., mod(fi, 2.) * 9. - fi * 3.), 3.4 - fi * .3, sin(uT * 9. + fi * 1.7) * .5));
    }
    over(vec3(.2, .18, .2), b * .75 * smoothstep(.2, .6, m.b) * smoothstep(0., .06, t0) * smoothstep(1., .94, t0));
  }
  gl_FragColor = vec4(acc.rgb + add, acc.a);
}`,
    dungeons: `
void main() {
  vec2 P = artPx(); acc = vec4(0.); add = vec3(0.);
  vec4 m = mask(P);
  // stars over the gorge
  vec2 cell = floor(P / 15.), sp = (cell + .2 + .6 * vec2(h21(cell + 1.3), h21(cell + 7.1))) * 15.;
  float hs = h21(cell);
  if (hs > .88) add += vec3(.9, .93, 1.) * dot1(P, sp, 1.5 + (hs - .88) * 12.) * (.45 + .55 * sin(uT * (.8 + hs * 3.) + hs * 50.)) * .6 * m.b;
  // the stream runs down from the steps
  if (m.a > .01) {
    vec3 c = flow(P, vec2(-2., 7.), 1.6, 0.);
    c += vec3(.7, .85, 1.) * pow(n2(P * vec2(.5, .35) + vec2(0., -uT * 1.4)), 8.) * .8;
    over(c, m.a);
  }
  // the gate breathes cold light, mist creeps out over the steps
  vec2 G = vec2(330., 335.);
  float pu = .5 + .5 * sin(uT * 1.1) * (.7 + .3 * n2(vec2(uT * 2., 9.)));
  add += vec3(.35, .55, 1.) * smoothstep(150., 0., length((P - G) * vec2(1., .6))) * pu * .2;
  float band = smoothstep(380., 430., P.y) * smoothstep(600., 520., P.y) * smoothstep(250., 300., P.x) * smoothstep(720., 560., P.x);
  over(vec3(.55, .66, .82), smoothstep(.45, .9, fbm(P * vec2(.008, .016) + vec2(-uT * .03, uT * .01))) * band * .32);
  // fire in the braziers, the camp and the torch
  float fl = .55 + .45 * (n2(vec2(uT * 7., 0.)) * .6 + n2(vec2(uT * 13., 4.)) * .4);
  if (m.r > .01) over(flow(P, vec2(0., -9.), .42, n2(vec2(P.x * .15, 0.))) * (.9 + .35 * fl), m.r);
  vec2 F = vec2(1050., 615.);
  float L = smoothstep(330., 0., length((P - F) * vec2(1., 1.3)));
  L *= L;
  add += img(P) * vec3(1., .55, .22) * L * fl * .3;
  over(vec3(0.), L * (1. - fl) * .1);
  for (int i = 0; i < 4; i++) {
    vec2 c = i == 0 ? vec2(248., 450.) : i == 1 ? vec2(630., 452.) : i == 2 ? vec2(1258., 318.) : vec2(1155., 655.);
    float f = .6 + .4 * n2(vec2(uT * (7. + float(i) * 2.), float(i) * 9.));
    add += vec3(1., .66, .3) * (smoothstep(110., 0., length(P - c)) * .1 + smoothstep(12., 0., length(P - c)) * .2) * f;
  }
  // embers from the camp
  for (int i = 0; i < 18; i++) {
    float fi = float(i), h = h21(vec2(fi, 1.7)), k = h21(vec2(fi, 5.3));
    float life = fract(uT / (1.8 + k * 2.2) + h);
    vec2 c = vec2(F.x + (h - .5) * 60. + sin(life * 6. + h * 20.) * 9. * life + life * 20., 612. - life * (120. + k * 130.));
    add += mix(vec3(1., .85, .45), vec3(1., .35, .08), life) * dot1(P, c, 1.3 + k * 1.4) * pow(1. - life, 1.4) * 1.3;
  }
  gl_FragColor = vec4(acc.rgb + add, acc.a);
}`,
    professions: `
void main() {
  vec2 P = artPx(); acc = vec4(0.); add = vec3(0.);
  vec4 m = mask(P);
  // clouds over the village
  if (m.b > .01) over(flow(P, vec2(-6., 0.) + (n2(P * .006 + uT * .03) - .5) * vec2(4., 2.), 12., 0.), m.b);
  // the mill stream
  if (m.a > .01) {
    vec3 c = flow(P, vec2(-5., 4.), 2.6, 0.);
    c += vec3(1., .95, .85) * pow(n2(P * vec2(.4, .7) + vec2(-uT * .9, uT * .4)), 9.) * .8;
    over(c, m.a);
  }
  // herbs sway under the beam
  if (m.g > .01) {
    float w = m.g, ph = P.y * .04 - uT * 1.3;
    vec2 off = vec2(sin(ph) * 1.8 + sin(uT * .9 + P.x * .03) * 1.1, 0.) * w;
    over(img(P - off), smoothstep(0., .1, w));
  }
  // forge fire and its light
  float fl = .55 + .45 * (n2(vec2(uT * 7., 0.)) * .6 + n2(vec2(uT * 13., 4.)) * .4);
  if (m.r > .01) over(flow(P, vec2(0., -9.), .42, n2(vec2(P.x * .15, 0.))) * (.9 + .35 * fl), m.r);
  vec2 F = vec2(175., 440.);
  float L = smoothstep(300., 0., length((P - F) * vec2(1., 1.2)));
  L *= L;
  add += img(P) * vec3(1., .55, .22) * L * fl * .28;
  // steam from the quench trough
  float sw = 30. + (640. - P.y) * .35, sx = P.x - 90. - (640. - P.y) * .25;
  over(vec3(.82, .82, .84), smoothstep(.45, .85, fbm(vec2(P.x * .02, P.y * .015 + uT * .4))) * smoothstep(sw, 0., abs(sx))
       * smoothstep(650., 600., P.y) * smoothstep(380., 520., P.y) * .3);
  // sparks out of the forge
  for (int i = 0; i < 12; i++) {
    float fi = float(i), h = h21(vec2(fi, 2.9)), k = h21(vec2(fi, 6.1));
    float life = fract(uT / (1.6 + k * 2.) + h);
    vec2 c = vec2(F.x + (h - .5) * 70. + sin(life * 5. + h * 20.) * 8. * life + life * 30., 430. - life * (60. + k * 110.));
    add += mix(vec3(1., .85, .45), vec3(1., .35, .08), life) * dot1(P, c, 1.2 + k * 1.1) * pow(1. - life, 1.5) * 1.2;
  }
  // the hammer strikes: a burst of sparks off the anvil and a flash on the blade
  float beat = fract(uT / 1.3), hit = floor(uT / 1.3);
  vec2 A = vec2(800., 605.);
  add += vec3(1., .6, .25) * smoothstep(60., 0., length((P - A) * vec2(.8, 1.4))) * exp(-beat * 6.) * .35;
  for (int i = 0; i < 14; i++) {
    float fi = float(i), h = h21(vec2(fi, hit)), k = h21(vec2(fi + 3., hit));
    float a = 3.1416 * (.1 + .8 * h), sp = 90. + k * 120., t = beat * .7;
    vec2 c = A + vec2(cos(a), -sin(a)) * sp * t + vec2(0., 140. * t * t);
    add += mix(vec3(1., .9, .55), vec3(1., .4, .1), beat) * dot1(P, c, 1.1 + k) * pow(1. - beat, 2.) * 1.3;
  }
  // the potion bubbles, the rune glows
  vec2 Po = vec2(905., 428.);
  float pp = .6 + .4 * sin(uT * 2.1);
  add += vec3(.3, 1., .45) * smoothstep(70., 0., length(P - Po)) * pp * .14;
  for (int i = 0; i < 6; i++) {
    float fi = float(i), h = h21(vec2(fi, 7.7)), life = fract(uT * (.5 + h * .4) + h);
    add += vec3(.6, 1., .7) * dot1(P, Po + vec2((h - .5) * 18., -life * 46.), 1.2 + h) * sin(life * 3.1416) * .8;
  }
  vec2 R = vec2(1135., 640.);
  add += vec3(.35, .8, 1.) * smoothstep(80., 0., length((P - R) * vec2(.8, 1.6))) * (.55 + .45 * sin(uT * 1.4)) * .2;
  gl_FragColor = vec4(acc.rgb + add, acc.a);
}`,
    faq: `
void main() {
  vec2 P = artPx(); acc = vec4(0.); add = vec3(0.);
  vec4 m = mask(P);
  // banners stir in the draught
  if (m.g > .01) {
    float w = m.g, ph = P.y * .03 - uT * 1.2;
    vec2 off = vec2(sin(ph) * 2.2 + sin(uT * .7 + P.x * .02) * 1.2, 0.) * w;
    over(img(P - off) * (1. + .08 * w * cos(ph)), smoothstep(0., .1, w));
  }
  // the sunbeam shimmers
  vec2 v = P - vec2(300., 40.);
  float ang = atan(v.y, v.x);
  float ray = n2(vec2(ang * 30., uT * .12)) * n2(vec2(ang * 61., -uT * .08));
  add += vec3(1., .92, .75) * pow(ray, 1.6) * m.b * .16;
  // dust floats in the light
  for (int i = 0; i < 40; i++) {
    float fi = float(i), h = h21(vec2(fi, 3.1)), k = h21(vec2(fi, 9.7));
    float life = fract(uT * (.012 + k * .018) + h);
    vec2 c = vec2(230. + h * 380. + sin(uT * .4 + fi) * 14. + life * 50., 100. + mod(k * 900. + life * 180., 600.));
    add += vec3(1., .93, .78) * dot1(P, c, 1.1 + k * 1.4) * sin(life * 3.1416) * (.5 + .5 * sin(uT * (1.2 + k * 2.) + fi)) * mask(c).b * .9;
  }
  // candle flames
  float fl = .55 + .45 * (n2(vec2(uT * 7., 0.)) * .6 + n2(vec2(uT * 13., 4.)) * .4);
  if (m.r > .01) over(flow(P, vec2(0., -5.), .38, n2(vec2(P.x * .3, 0.))) * (.9 + .3 * fl), m.r);
  for (int i = 0; i < 3; i++) {
    vec2 c = i == 0 ? vec2(43., 422.) : i == 1 ? vec2(69., 416.) : vec2(158., 432.);
    float f = .6 + .4 * n2(vec2(uT * (8. + float(i) * 3.), float(i) * 9.));
    add += vec3(1., .72, .38) * (smoothstep(60., 0., length(P - c)) * .1 + smoothstep(6., 0., length(P - c)) * .25) * f;
  }
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

  function texture(gl, unit, src) {
    const t = gl.createTexture();
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

  function live(pic) {
    const scene = pic.dataset.fx, img = pic.querySelector('img'), cut = parseFloat(pic.dataset.cut || '.6');
    const SUN = { dawn: [375, 210], day: [375, 210], dusk: [375, 210], night: [375, 210] };   // measured on the aligned art (tools/align_tod.py); day: above the frame
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
    let prog;
    try {
      prog = gl.createProgram();
      gl.attachShader(prog, shader(gl, gl.VERTEX_SHADER, VS));
      gl.attachShader(prog, shader(gl, gl.FRAGMENT_SHADER, COMMON + SCENES[scene]));
      gl.linkProgram(prog);
      if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(prog));
    } catch (e) { return; }
    gl.useProgram(prog);
    gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer());
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
    gl.enableVertexAttribArray(0);
    gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0);
    const U = {};
    for (const n of ['uImg', 'uMask', 'uSize', 'uMap', 'uCrop', 'uT', 'uPx', 'uTod', 'uSun']) U[n] = gl.getUniformLocation(prog, n);
    gl.uniform1i(U.uImg, 0);
    gl.uniform1i(U.uMask, 1);

    const mk = new Image();
    mk.src = base + ART[scene] + '-fx.png' + ver;
    let on = false, shown = false, raf = 0, last = 0, src = '';
    const t0 = performance.now() - Math.random() * 20000;

    function layout() {
      const w = cv.clientWidth, h = cv.clientHeight;
      if (!w || !h) return false;
      const k = Math.min(devicePixelRatio || 1, 1.5, Math.sqrt(3.2e6 / (w * h)));
      cv.width = Math.round(w * k);
      cv.height = Math.round(h * k);
      gl.viewport(0, 0, cv.width, cv.height);
      const iw = img.naturalWidth, ih = img.naturalHeight, s = Math.max(w / iw, h / ih);
      const pos = getComputedStyle(img).objectPosition.split(' ').map(v => parseFloat(v) / 100);
      const dw = iw * s, dh = ih * s;
      // phones get a portrait cut of the art (tools/make_images.py hero_mobile): .43605 of the width, at data-cut of the rest
      const crop = /hero_\w+-m-/.test(img.currentSrc) ? [cut * (1 - .43605), 0, .43605, 1] : [0, 0, 1, 1];
      gl.uniform2f(U.uSize, w, h);
      gl.uniform4f(U.uMap, (w - dw) * (isNaN(pos[0]) ? .5 : pos[0]), (h - dh) * (isNaN(pos[1]) ? .5 : pos[1]), dw, dh);
      gl.uniform4f(U.uCrop, ...crop);
      gl.uniform1f(U.uPx, dw / (crop[2] * 1376));
      return true;
    }

    function upload() {
      src = img.currentSrc;
      texture(gl, 0, img);
    }

    function frame(now) {
      raf = 0;
      if (!on || document.hidden) return;
      raf = requestAnimationFrame(frame);
      if (now - last < 1000 / FPS - 2) return;
      last = now;
      if (img.currentSrc !== src) { upload(); layout(); }
      gl.uniform1f(U.uT, ((now - t0) / 1000) % 3600);
      const t = tod();
      gl.uniform1f(U.uTod, TOD[t]);
      gl.uniform2f(U.uSun, ...SUN[t]);
      gl.drawArrays(gl.TRIANGLES, 0, 3);
      if (!shown) { shown = true; requestAnimationFrame(() => cv.classList.add('on')); }
    }

    function run(v) {
      on = v;
      if (on && !raf) raf = requestAnimationFrame(frame);
    }

    Promise.all([ready(img), mk.decode()]).then(() => {
      pic.appendChild(cv);
      upload();
      texture(gl, 1, mk);
      if (!layout()) return;
      new ResizeObserver(() => layout()).observe(cv);
      new IntersectionObserver(es => run(es[0].isIntersecting)).observe(pic);
      document.addEventListener('visibilitychange', () => run(on));
      cv.addEventListener('webglcontextlost', () => { on = false; cv.remove(); });
      document.addEventListener('gabella:tod-start', () => cv.classList.remove('on'));
      document.addEventListener('gabella:tod', () => { shown = false; });   // the next frame re-uploads the new picture and fades in
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
