// Alignment check: the content of every framed control (a box with a border, a fill or a ring: buttons, chips, tabs,
// badges, switches, the header buttons, the tab bar) sits in the middle of its frame, measured in pixels.
//   horizontal: the content's ink (text painted pure red for the shot, icons by their boxes) centre vs the frame centre;
//               checked where the control centres its content (text-align / justify-content center, or a shrink-wrapped box);
//               left-aligned boxes (search field, cards, list rows) are reported as "left" and not checked across.
//   vertical:   the cap-height band of the text (baseline - cap height .. baseline, from the font itself) plus icons vs the
//               frame centre, for one- and two-line controls up to 72 px tall. Descenders do not count, so Cyrillic and
//               Latin labels are judged the same way.
// Tolerance 1 px (--tol). Exit code 1 if a control is off.
//   node tests/align_check.mjs --quick      key pages x 9 languages x 390/1280, dark (used by run_all)
//   node tests/align_check.mjs --full       key pages x 9 languages x 320/390/768/1280 x both themes
//   options: --langs ru,en  --widths 390  --themes dark  --pages classes/,tools/  --jobs 6  --json FILE  --shots DIR  --all
//   (--all lists every measured control in the json, not only the off ones; --shots saves a x3 crop of each off control)
import { spawn } from 'node:child_process';
import { createServer } from 'node:http';
import { existsSync, mkdtempSync, readFileSync, statSync, writeFileSync, mkdirSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, extname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { inflateSync } from 'node:zlib';

const ROOT = resolve(process.env.ALIGN_ROOT || join(dirname(fileURLToPath(import.meta.url)), '..'));
const argv = process.argv.slice(2);
const opt = (n, d) => { const i = argv.indexOf('--' + n); return i < 0 ? d : (argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[i + 1] : true); };
const FULL = argv.includes('--full');
const ALL_LANGS = ['ru', 'uk', 'en', 'de', 'fr', 'es', 'pt', 'it', 'pl'];
const KEY = ['', 'classes/', 'classes/mage/', 'guides/spec-mage-frost/', 'guides/builds-mage/', 'talents/mage/', 'guides/tier-list/', 'guides/dungeons/', 'guides/dungeons/the-deadmines/', 'guides/faq/', 'tools/', 'guides/'];
const QUICK = ['', 'classes/mage/', 'guides/builds-mage/', 'guides/tier-list/', 'guides/dungeons/', 'tools/'];
const langs = (opt('langs', '') || ALL_LANGS.join(',')).split(',');
const widths = (opt('widths', '') || (FULL ? '320,390,768,1280' : '390,1280')).split(',').map(Number);
const themes = (opt('themes', '') || (FULL ? 'dark,light' : 'dark')).split(',');
const subs = opt('pages', '') ? String(opt('pages')).split(',').map(p => p === 'home' ? '' : p) : (FULL ? KEY : QUICK);
const jobs = +opt('jobs', 6);
const TOL = +opt('tol', 1);
const jsonOut = opt('json', '');
const shotsDir = opt('shots', '');
const ALL = argv.includes('--all');
const DPR = 2;

// ---- tiny static server
const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.svg': 'image/svg+xml', '.webp': 'image/webp', '.avif': 'image/avif', '.png': 'image/png', '.jpg': 'image/jpeg', '.woff2': 'font/woff2', '.webmanifest': 'application/manifest+json', '.xml': 'application/xml', '.ico': 'image/x-icon', '.mp3': 'audio/mpeg' };
const server = createServer((req, res) => {
  let f = join(ROOT, decodeURIComponent(req.url.split('?')[0].replace(/^\/wow\//, '/')));
  if (!f.startsWith(ROOT)) { res.writeHead(403).end(); return; }
  if (existsSync(f) && statSync(f).isDirectory()) f = join(f, 'index.html');
  if (!existsSync(f)) { res.writeHead(404).end('404'); return; }
  res.writeHead(200, { 'content-type': MIME[extname(f)] || 'application/octet-stream' });
  res.end(readFileSync(f));
});
await new Promise(r => server.listen(0, '127.0.0.1', r));
const base = `http://127.0.0.1:${server.address().port}/`;

// ---- Chrome over CDP
const CHROME = [process.env.CHROME_PATH, 'C:/Program Files/Google/Chrome/Application/chrome.exe', 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe', '/usr/bin/google-chrome', '/usr/bin/chromium', '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'].find(p => p && existsSync(p));
if (!CHROME) { console.error('Chrome not found (set CHROME_PATH)'); process.exit(2); }
const port = 9400 + Math.floor(Math.random() * 400);
const chrome = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${port}`, '--no-first-run', '--disable-gpu', '--hide-scrollbars', '--force-color-profile=srgb', `--user-data-dir=${mkdtempSync(join(tmpdir(), 'aln-'))}`, 'about:blank'], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
let ws;
for (let i = 0; i < 80 && !ws; i++) { try { const v = await (await fetch(`http://127.0.0.1:${port}/json/version`)).json(); ws = new WebSocket(v.webSocketDebuggerUrl); } catch { await sleep(250); } }
await new Promise(r => ws.onopen = r);
let seq = 0; const pend = new Map();
ws.onmessage = e => { const m = JSON.parse(e.data); if (m.id && pend.has(m.id)) { const [ok, bad] = pend.get(m.id); pend.delete(m.id); m.error ? bad(new Error(m.error.message)) : ok(m.result); } };
const send = (method, params = {}, sessionId) => new Promise((ok, bad) => { const id = ++seq; pend.set(id, [ok, bad]); ws.send(JSON.stringify({ id, method, params, sessionId })); });

// ---- minimal PNG decoder (8-bit RGB/RGBA, non-interlaced: what Chrome writes)
function png(buf) {
  let p = 8, w, h, ct; const idat = [];
  while (p < buf.length) { const len = buf.readUInt32BE(p), type = buf.toString('ascii', p + 4, p + 8), d = buf.subarray(p + 8, p + 8 + len);
    if (type === 'IHDR') { w = d.readUInt32BE(0); h = d.readUInt32BE(4); ct = d[9]; } else if (type === 'IDAT') idat.push(d); p += 12 + len; }
  const bpp = ct === 6 ? 4 : 3, raw = inflateSync(Buffer.concat(idat)), stride = w * bpp, px = Buffer.alloc(h * stride);
  for (let y = 0; y < h; y++) { const f = raw[y * (stride + 1)], so = y * (stride + 1) + 1, o = y * stride;
    for (let x = 0; x < stride; x++) { const a = x >= bpp ? px[o + x - bpp] : 0, b = y ? px[o - stride + x] : 0, c = x >= bpp && y ? px[o - stride + x - bpp] : 0; let v = raw[so + x];
      if (f === 1) v += a; else if (f === 2) v += b; else if (f === 3) v += (a + b) >> 1; else if (f === 4) { const pp = a + b - c, pa = Math.abs(pp - a), pb = Math.abs(pp - b), pc = Math.abs(pp - c); v += pa <= pb && pa <= pc ? a : pb <= pc ? b : c; }
      px[o + x] = v & 255; } }
  return { w, h, bpp, px };
}

// ---- in-page: find the framed controls, describe them, then paint their content red and everything else away
const FIND = `(() => {
  const al = c => { const m = c.match(/rgba?\\(([^)]*)\\)/); if (!m) return c === 'transparent' ? 0 : 1; const p = m[1].split(/[ ,\\/]+/).filter(Boolean); return p.length > 3 ? parseFloat(p[3]) * (p[3].endsWith('%') ? .01 : 1) : 1; };
  const vis = (e, cs) => cs.display !== 'none' && cs.visibility === 'visible' && +cs.opacity > .05;
  const ctx = document.createElement('canvas').getContext('2d');
  const fixedOf = e => { for (let a = e; a && a !== document.body; a = a.parentElement) { if (getComputedStyle(a).position === 'fixed') return a; } return null; };
  const skipTag = /^(SCRIPT|STYLE|SVG|PATH|G|USE|SYMBOL|IMG|PICTURE|SOURCE|VIDEO|CANVAS|IFRAME|BR|HR|TEMPLATE|NOSCRIPT|HTML|BODY|MAIN|SECTION|ARTICLE|HEADER|FOOTER|NAV|UL|OL|TABLE|TBODY|THEAD|TR|DIALOG|DETAILS|FORM)$/i;
  const out = []; let n = 0;
  const clipped = (e, r) => { for (let a = e.parentElement; a && a !== document.body; a = a.parentElement) { const c = getComputedStyle(a); if (c.overflowX === 'visible' && c.overflowY === 'visible') continue; const q = a.getBoundingClientRect();
    if (r.left < q.left - 1 || r.right > q.right + 1 || r.top < q.top - 1 || r.bottom > q.bottom + 1) return true; } return false; };
  // a corner badge (absolutely placed inside the control: a rank number, a count) is not the content to centre
  const badge = (t, e) => { for (let a = t.parentElement; a && a !== e; a = a.parentElement) if (getComputedStyle(a).position === 'absolute') return a; return null; };
  const all = [...document.body.querySelectorAll('*')];
  for (const e of all) {
    if (skipTag.test(e.tagName) || e.closest('svg,[hidden],[aria-hidden="true"] [aria-hidden="true"]')) continue;
    const cs = getComputedStyle(e); if (!vis(e, cs)) continue;
    if (e.checkVisibility && !e.checkVisibility({ contentVisibilityAuto: true, opacityProperty: true, visibilityProperty: true })) continue;
    const r = e.getBoundingClientRect();
    if (clipped(e, r)) continue; if (r.width < 14 || r.height < 14 || r.height > 120 || r.width > 900) continue;
    if (r.bottom + scrollY < 0 || r.right < 0 || r.left > innerWidth) continue;
    const bw = ['Top', 'Right', 'Bottom', 'Left'].map(s => parseFloat(cs['border' + s + 'Width']));
    const bcol = ['Top', 'Right', 'Bottom', 'Left'].map(s => al(cs['border' + s + 'Color']));
    const border = bw.every(x => x > 0) && bcol.every(x => x > .05);
    const fill = al(cs.backgroundColor) > .05 || /gradient/.test(cs.backgroundImage);
    const ring = /(^|, )(rgb[^)]*\\)\\s+)?0px 0px 0px [1-9]|inset/.test(cs.boxShadow);
    if (!(border || fill || ring)) continue;
    const text = (e.textContent || '').replace(/\\s+/g, ' ').trim();
    const icons = [...e.querySelectorAll('svg,img,picture,canvas,[style*="background-image"],.av,.ico')].concat([...e.querySelectorAll('span,i,b')].filter(i => { const c = getComputedStyle(i), q = i.getBoundingClientRect(); return !i.textContent.trim() && q.width <= 24 && q.height <= 24 && (al(c.backgroundColor) > .05 || c.backgroundImage !== 'none'); }))
      .filter(i => { const c = getComputedStyle(i); const q = i.getBoundingClientRect(); return c.display !== 'none' && c.visibility === 'visible' && q.width > 2 && q.height > 2 && !i.parentElement.closest('svg') && !badge(i, e); });
    const clamp = q => ({ left: Math.max(q.left, r.left), right: Math.min(q.right, r.right), top: Math.max(q.top, r.top), bottom: Math.min(q.bottom, r.bottom) });
    const isField = /^(INPUT|SELECT|TEXTAREA)$/.test(e.tagName);
    if (!isField && (!text && !icons.length)) continue;
    if (text.length > 60) continue;
    if (e.children.length > 8) continue;
    // the band of the text: cap height above each baseline (baseline from the font's ascent)
    let top = 1e9, bot = -1e9, nl = 0, tL = 1e9, tR = -1e9; const bases = new Set();
    const tw = document.createTreeWalker(e, NodeFilter.SHOW_TEXT); let t;
    while ((t = tw.nextNode())) {
      const s = t.textContent; if (!s.trim()) continue; const p = t.parentElement, pc = getComputedStyle(p);
      if (pc.visibility !== 'visible' || p.closest('[hidden]')) continue;
      const bd = badge(t, e); if (bd) { bd.dataset.alnSkip = 1; continue; } const pr = p.getBoundingClientRect(); if (pr.width <= 2 || pr.height <= 2) continue;
      if (/inset\\(50%\\)|rect\\(0/.test(pc.clipPath + pc.clip)) continue;
      const rg = document.createRange(); rg.selectNodeContents(t);
      const rects = [...rg.getClientRects()].filter(q => q.width > .5 && q.height > .5); if (!rects.length) continue;
      ctx.font = pc.fontStyle + ' ' + pc.fontWeight + ' ' + pc.fontSize + ' ' + pc.fontFamily;
      const m = ctx.measureText(s.trim()); const asc = m.fontBoundingBoxAscent, desc = m.fontBoundingBoxDescent;
      const cyr = /[\\u0400-\\u04ff]/.test(s); const capH = ctx.measureText(cyr ? '\\u041d' : 'H').actualBoundingBoxAscent;
      const low = pc.textTransform !== 'uppercase' && s.trim() === s.trim().toLowerCase() && /[a-z\\u0430-\\u044f]/.test(s);
      const xH = ctx.measureText(cyr ? '\\u0445' : 'x').actualBoundingBoxAscent;
      for (const q of rects) { tL = Math.min(tL, q.left); tR = Math.max(tR, q.right); const b = q.top + asc + (q.height - asc - desc) / 2; top = Math.min(top, b - (low ? xH : capH)); bot = Math.max(bot, b); bases.add(Math.round(b)); }
    }
    nl = bases.size;
    // the font's own side bearings: a word that starts with a wide-bearing letter (M) and ends with an overhanging one (Ukrainian i with dots)
    // has its ink off the advance box by design of the typeface; layout cannot see it. Kept apart as "bearing".
    let bear = 0;
    if (nl === 1 && !icons.length && text) { const t0 = [...e.querySelectorAll('*')].concat(e).find(x => [...x.childNodes].some(c => c.nodeType === 3 && c.textContent.trim())) || e, fc = getComputedStyle(t0);
      ctx.font = fc.fontStyle + ' ' + fc.fontWeight + ' ' + fc.fontSize + ' ' + fc.fontFamily; ctx.letterSpacing = fc.letterSpacing === 'normal' ? '0px' : fc.letterSpacing;
      const ln = (e.innerText || text).replace(/\s+/g, ' ').trim(); const m = ctx.measureText(ln); ctx.letterSpacing = '0px';
      const lsb = -m.actualBoundingBoxLeft, rsb = m.width - m.actualBoundingBoxRight; bear = +((lsb - rsb) / 2).toFixed(2); }
    for (const i of icons) { const q = clamp(i.getBoundingClientRect()); top = Math.min(top, q.top); bot = Math.max(bot, q.bottom); tL = Math.min(tL, q.left); tR = Math.max(tR, q.right); }
    const pl = parseFloat(cs.paddingLeft), pr = parseFloat(cs.paddingRight), pt = parseFloat(cs.paddingTop), pb = parseFloat(cs.paddingBottom);
    // horizontal intent
    const disp = cs.display; const flex = /flex/.test(disp), grid = /grid/.test(disp);
    let mode = 'left';
    const jc = cs.justifyContent, ta = cs.textAlign;
    const row = cs.flexDirection.startsWith('row');
    if (flex && /space-between/.test(jc) && e.children.length > 1) mode = 'spread';
    else if (flex ? (row ? /center|space-around|space-evenly/.test(jc) : /center/.test(cs.alignItems))
      : grid ? (/center/.test(cs.justifyItems) || /center/.test(jc))
      : (ta === 'center' || ta === '-webkit-center')) mode = 'center';
    else if (isField) mode = 'left';
    else {   // shrink-wrapped: no free room beside the content, equal paddings -> the eye reads it as centred
      const free = (r.width - bw[1] - bw[3] - pl - pr) - (tR - tL);
      if (tR > tL && nl <= 1 && free < 3 && Math.abs(pl - pr) < .5) mode = 'center';
    }
    const fx = fixedOf(e);
    const id = ++n; e.dataset.alnId = id;
    let cls = (typeof e.className === 'string' ? e.className : '').trim().split(/\\s+/).filter(c => c && !/^(on|is-|active|sel|cur)/.test(c)).slice(0, 2).join('.');
    let par = e.parentElement; while (par && !(typeof par.className === 'string' && par.className.trim()) && !par.id) par = par.parentElement;
    const pn = par ? (par.id ? '#' + par.id : '.' + par.className.trim().split(/\\s+/)[0]) : '';
    const role = e.getAttribute('role');
    const sig = (pn ? pn + ' ' : '') + e.tagName.toLowerCase() + (cls ? '.' + cls : '') + (role ? '[role=' + role + ']' : '');
    // pseudo content (chevrons, dots) counts as content when it is small; big pseudos are decoration
    const ps = ['before', 'after'].filter(k => { const c = getComputedStyle(e, '::' + k); if (c.content === 'none' || c.content === 'normal' || c.display === 'none') return false; const w = parseFloat(c.width), h = parseFloat(c.height); return (c.position !== 'absolute' || (w < r.width * .5 && h < r.height * .7)) && !(w >= r.width * .9); });
    if (ps.length) e.dataset.alnPs = ps.join(' ');
    const pbg = ps.filter(k => al(getComputedStyle(e, '::' + k).backgroundColor) > .05); if (pbg.length) e.dataset.alnPsbg = pbg.join(' ');
    const css = [disp, cs.flexDirection, jc, cs.alignItems, cs.justifyItems, ta].join(' ');
    out.push({ id, sig, css, text: text.slice(0, 40), lang: document.documentElement.lang, mode, fixed: !!fx, x: r.left + scrollX, y: r.top + (fx ? 0 : scrollY), w: r.width, h: r.height,
      bear, band: top < 1e8 ? { t: top + (fx ? 0 : scrollY), b: bot + (fx ? 0 : scrollY) } : null, lines: nl, pad: [pt, pr, pb, pl], bw, field: isField,
      icons: icons.map(i => { const q = clamp(i.getBoundingClientRect()); return [q.left + scrollX, q.right + scrollX]; }) });
  }
  for (const o of out) { const e = document.querySelector('[data-aln-id="' + o.id + '"]');
    const kids = out.filter(k => k !== o && e.contains(document.querySelector('[data-aln-id="' + k.id + '"]')));
    if (kids.length) { o.kids = [...e.children].filter(c => { const q = c.getBoundingClientRect(), cc = getComputedStyle(c); return q.width > 1 && q.height > 1 && cc.visibility === 'visible' && cc.position !== 'absolute'; })
      .map(c => { const q = c.getBoundingClientRect(); return { x: q.left + scrollX, y: q.top + (o.fixed ? 0 : scrollY), w: q.width, h: q.height }; }); if (!o.kids.length) { delete o.kids; continue; }
      const cs = getComputedStyle(e), kl = Math.min(...o.kids.map(q => q.x)), kr = Math.max(...o.kids.map(q => q.x + q.w));
      const free = o.w - o.bw[1] - o.bw[3] - o.pad[1] - o.pad[3] - (kr - kl);
      if (o.mode === 'left' && free < 3 && Math.abs(o.pad[1] - o.pad[3]) < .5) o.mode = 'center';
      if (o.mode !== 'center') delete o.kids; } }
  return out;
})()`;
// paint: everything transparent; the content of measured controls pure red
const PAINT = `(() => {
  const s = document.createElement('style'); s.id = 'alnst';
  s.textContent = \`
  html, body { background: #000 !important; }
  *, *::before, *::after { color: transparent !important; -webkit-text-fill-color: transparent !important; text-shadow: none !important; background: transparent !important; border-color: transparent !important; box-shadow: none !important; outline: none !important; text-decoration-color: transparent !important; caret-color: transparent !important; fill: transparent !important; stroke: transparent !important; animation: none !important; transition: none !important; filter: none !important; backdrop-filter: none !important; }
  *::placeholder { color: transparent !important; }
  img, picture, video, canvas, iframe { opacity: 0 !important; }
  [data-aln-id], [data-aln-id] * { color: #f00 !important; -webkit-text-fill-color: #f00 !important; }
  [data-aln-id]::placeholder { color: #f00 !important; -webkit-text-fill-color: #f00 !important; opacity: 1 !important; }
  [data-aln-ps~="before"]::before, [data-aln-ps~="after"]::after { color: #f00 !important; border-color: #f00 !important; }
  [data-aln-psbg~="before"]::before, [data-aln-psbg~="after"]::after { background: #f00 !important; }
  [data-aln-id] [data-aln-skip], [data-aln-id] [data-aln-skip] * { color: transparent !important; -webkit-text-fill-color: transparent !important; }
  \`;
  document.head.append(s); return 1;
})()`;
const UNPAINT = `(() => { document.getElementById('alnst')?.remove(); return 1; })()`;
const HIDE_FIXED = `(() => { const s = document.createElement('style'); s.id = 'alnfx'; document.head.append(s); const sel = []; let k = 0;
  for (const e of document.body.querySelectorAll('*')) { if (getComputedStyle(e).position === 'fixed') e.dataset.alnFx = ++k; }
  s.textContent = '[data-aln-fx]{visibility:hidden!important}'; return k; })()`;

async function newWorker() {
  const { browserContextId } = await send('Target.createBrowserContext');
  const { targetId } = await send('Target.createTarget', { url: 'about:blank', browserContextId });
  const { sessionId } = await send('Target.attachToTarget', { targetId, flatten: true });
  const S = (m, p) => send(m, p, sessionId);
  await S('Page.enable'); await S('Runtime.enable');
  const ev = async expr => { const r = await S('Runtime.evaluate', { expression: expr, returnByValue: true, awaitPromise: true }); if (r.exceptionDetails) throw new Error(r.exceptionDetails.exception?.description || r.exceptionDetails.text); return r.result.value; };
  return { S, ev, init: null };
}

function shift(it, dx, dy) {
  if (Math.abs(dx) < .01 && Math.abs(dy) < .01) return;
  it.x += dx; it.y += dy; it.dX = (it.dX || 0) + dx; it.dY = (it.dY || 0) + dy; if (it.band) { it.band.t += dy; it.band.b += dy; } it.icons = it.icons.map(([a, b]) => [a + dx, b + dx]);
}
// red pixels of a captured region -> per control: ink x/y range in css px
function inkOf(im, clip, items) {
  const k = im.w / clip.width; const res = new Map();
  for (const it of items) {
    const X0 = Math.max(0, Math.floor((it.x - clip.x) * k)), X1 = Math.min(im.w, Math.ceil((it.x + it.w - clip.x) * k));
    const Y0 = Math.max(0, Math.floor((it.y - clip.y) * k)), Y1 = Math.min(im.h, Math.ceil((it.y + it.h - clip.y) * k));
    let x0 = 1e9, x1 = -1, y0 = 1e9, y1 = -1;
    for (let y = Y0; y < Y1; y++) for (let x = X0; x < X1; x++) { const o = (y * im.w + x) * im.bpp, R = im.px[o], G = im.px[o + 1], B = im.px[o + 2];
      if (R - Math.max(G, B) > 60) { if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; } }
    res.set(it.id, x1 < 0 ? null : { l: clip.x + x0 / k, r: clip.x + (x1 + 1) / k, t: clip.y + y0 / k, b: clip.y + (y1 + 1) / k });
  }
  return res;
}

const rows = []; const errors = [];
async function checkPage(w, job) {
  const { S, ev } = w; const { lang, sub, width, theme } = job;
  await S('Emulation.setDeviceMetricsOverride', { width, height: width < 700 ? 800 : 900, deviceScaleFactor: DPR, mobile: width < 700 });
  await S('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-color-scheme', value: theme }] });
  if (w.init) await S('Page.removeScriptToEvaluateOnNewDocument', { identifier: w.init });
  w.init = (await S('Page.addScriptToEvaluateOnNewDocument', { source: `try{localStorage.setItem('wf-theme','${theme}');localStorage.setItem('gabella-lang','${lang}');localStorage.setItem('gabella-lang-hint','1')}catch(e){}` })).identifier;
  await S('Page.navigate', { url: base + (lang === 'ru' ? '' : lang + '/') + sub });
  for (let i = 0; i < 100; i++) { if (await ev(`document.readyState`) === 'complete') break; await sleep(100); }
  await ev(`document.fonts.ready.then(()=>1)`);
  await ev(`(()=>{document.documentElement.setAttribute('data-theme','${theme}');const st=document.createElement('style');st.textContent='*,*::before,*::after{animation:none!important;transition:none!important}';document.head.append(st);document.querySelectorAll('.reveal,[data-reveal]').forEach(e=>e.classList.add('in','on','shown'));return 0})()`);
  await ev(`Promise.all([...document.images].map(i=>i.loading==='lazy'?(i.loading='eager',i.decode().catch(()=>0)):0))`);
  await ev(`(async()=>{const h=document.documentElement.scrollHeight;for(let y=0;y<h;y+=innerHeight){scrollTo(0,y);await new Promise(r=>setTimeout(r,25))}scrollTo(0,0);return 1})()`);
  await sleep(250);
  await ev(`document.fonts.ready.then(()=>1)`);
  const items = await ev(FIND);
  if (!items.length) return;
  // crops of the controls as they look (before painting), only for the off ones: decided after measuring, so keep the page state
  await ev(PAINT); await sleep(60);
  const ink = new Map();
  // phase A: fixed / sticky controls (the top bar, the tab bar) in the viewport at scroll 0
  const fx = items.filter(i => i.fixed);
  if (fx.length) {
    await ev(`scrollTo(0,0);1`); await sleep(40);
    const vw = await ev(`({w:innerWidth,h:innerHeight})`);
    const clip = { x: 0, y: 0, width: vw.w, height: vw.h, scale: 1 };
    const s = await S('Page.captureScreenshot', { format: 'png', clip, captureBeyondViewport: false });
    for (const [k, v] of inkOf(png(Buffer.from(s.data, 'base64')), clip, fx)) ink.set(k, v);
  }
  // phase B: the rest of the page in bands, fixed things hidden
  const rest = items.filter(i => !i.fixed).sort((a, b) => a.y - b.y);
  if (rest.length) {
    await ev(HIDE_FIXED);
    const vw = await ev(`({w:innerWidth,h:innerHeight})`);
    let i = 0;
    while (i < rest.length) {   // bands no taller than the viewport, scrolled into view (beyond-viewport shots come out blank here)
      const y0 = Math.max(0, Math.floor(rest[i].y) - 2); let y1 = y0; const band = [];
      while (i < rest.length && rest[i].y + rest[i].h + 2 - y0 <= vw.h - 4) { band.push(rest[i]); y1 = Math.max(y1, Math.ceil(rest[i].y + rest[i].h) + 2); i++; }
      if (!band.length) { band.push(rest[i]); y1 = Math.ceil(rest[i].y + rest[i].h) + 2; i++; }
      const sy = await ev(`(scrollTo(0,${y0}),scrollY)`); await sleep(30);
      const now = await ev(`(${JSON.stringify(band.map(b => b.id))}).map(id=>{const r=document.querySelector('[data-aln-id="'+id+'"]').getBoundingClientRect();return [r.left+scrollX,r.top+scrollY]})`);
      band.forEach((b, j) => shift(b, now[j][0] - b.x, now[j][1] - b.y));   // late layout (lazy art, fonts): measure where it is now
      const clip = { x: 0, y: y0, width: vw.w, height: Math.min(y1 - y0, vw.h - (y0 - sy)), scale: 1 };
      const s = await S('Page.captureScreenshot', { format: 'png', clip, captureBeyondViewport: false });
      if (process.env.ALIGN_DEBUG) writeFileSync(join(process.env.ALIGN_DEBUG, `${lang}-${width}-${y0}.png`), Buffer.from(s.data, 'base64'));
      for (const [k, v] of inkOf(png(Buffer.from(s.data, 'base64')), clip, band)) ink.set(k, v);
    }
    await ev(`(()=>{document.getElementById('alnfx')?.remove();document.querySelectorAll('[data-aln-fx]').forEach(e=>e.removeAttribute('data-aln-fx'));return 1})()`);
  }
  await ev(UNPAINT);
  const offs = []; for (const i of items) { i.dX ||= 0; i.dY ||= 0; }
  for (const it of items) {
    const k = ink.get(it.id);
    const cx = it.x + it.w / 2, cy = it.y + it.h / 2;
    let l = k ? k.l : 1e9, r = k ? k.r : -1e9;
    for (const [a, b] of it.icons) { l = Math.min(l, a); r = Math.max(r, b); }
    if (it.kids) { const ks = it.kids.map(q => ({ ...q, x: q.x + it.dX, y: q.y + it.dY })); l = Math.min(...ks.map(q => q.x)); r = Math.max(...ks.map(q => q.x + q.w));
      it.band = { t: Math.min(...ks.map(q => q.y)), b: Math.max(...ks.map(q => q.y + q.h)) }; it.lines = 1; }
    const dx = l < 1e8 ? +(((l + r) / 2) - cx).toFixed(2) : null;
    const dy = it.band ? +(((it.band.t + it.band.b) / 2) - cy).toFixed(2) : null;
    const dyInk = k ? +(((k.t + k.b) / 2) - cy).toFixed(2) : null;
    const gapL = l < 1e8 ? +(l - it.x).toFixed(2) : null, gapR = l < 1e8 ? +(it.x + it.w - r).toFixed(2) : null;
    const checkX = it.mode === 'center' && dx !== null;
    const checkY = dy !== null && it.h <= 72 && it.lines <= 2;
    const fontOnly = checkX && Math.abs(dx) > TOL && Math.abs(dx - it.bear) <= .5 && Math.abs(it.bear) <= 1.5;   // the layout is exact, the rest is the glyphs' side bearings
    const bad = (checkX && Math.abs(dx) > TOL && !fontOnly) || (checkY && Math.abs(dy) > TOL);
    const row = { page: '/' + sub, lang, width, theme, sig: it.sig, text: it.text, mode: it.mode, css: it.css, box: `${+it.w.toFixed(1)}x${+it.h.toFixed(1)}`, dx: checkX ? dx : null, dxRaw: dx, dy: checkY ? dy : null, dyInk, gapL, gapR, pad: it.pad, lines: it.lines, bear: it.bear, fontOnly, bad };
    if (bad) offs.push({ row, it });
    if (bad || ALL) rows.push(row);
  }
  if (shotsDir && offs.length) {
    mkdirSync(shotsDir, { recursive: true });
    const seen = new Set();
    for (const { row, it } of offs) {
      const key = row.sig; if (seen.has(key)) continue; seen.add(key);
      const name = `${lang}-${theme}-${width}-${(sub || 'home').replace(/\W+/g, '_')}-${row.sig.replace(/\W+/g, '_').slice(0, 50)}.png`;
      if (!it.fixed) await ev(`(()=>{const e=document.querySelector('[data-aln-id="${it.id}"]');e&&e.scrollIntoView({block:'center'});return 1})()`); else await ev(`scrollTo(0,0);1`);
      await sleep(80);
      const c = await ev(`(()=>{const e=document.querySelector('[data-aln-id="${it.id}"]');if(!e)return null;const r=e.getBoundingClientRect();return {x:Math.max(0,r.left+scrollX-6),y:Math.max(0,r.top+scrollY-6),width:r.width+12,height:r.height+12}})()`);
      if (!c) continue;
      try { const s = await S('Page.captureScreenshot', { format: 'png', clip: { ...c, scale: 1.5 }, captureBeyondViewport: false }); writeFileSync(join(shotsDir, name), Buffer.from(s.data, 'base64')); } catch {}
    }
  }
}

const queue = [];
for (const theme of themes) for (const lang of langs) for (const sub of subs) for (const width of widths) queue.push({ lang, sub, width, theme });
const total = queue.length;
const workers = await Promise.all(Array.from({ length: Math.min(jobs, queue.length) }, newWorker));
let done = 0;
await Promise.all(workers.map(async w => { for (let j; (j = queue.shift());) { try { await checkPage(w, j); } catch (e) { errors.push(`/${j.sub} ${j.lang} ${j.width} ${j.theme}: ${String(e.message).slice(0, 160)}`); } if (++done % 50 === 0) process.stderr.write(`${done}/${total}\n`); } }));
chrome.kill(); server.close();
if (jsonOut) writeFileSync(jsonOut, JSON.stringify({ rows, errors }, null, 1));
const bad = rows.filter(r => r.bad);
// group: one line per control kind with the worst offsets and where
const grp = new Map();
for (const r of bad) { const g = grp.get(r.sig) || { n: 0, dx: 0, dy: 0, where: new Set(), langs: new Set(), ex: r }; g.n++; if (r.dx !== null && Math.abs(r.dx) > Math.abs(g.dx)) g.dx = r.dx; if (r.dy !== null && Math.abs(r.dy) > Math.abs(g.dy)) g.dy = r.dy; g.where.add(`${r.page}@${r.width}`); g.langs.add(r.lang); grp.set(r.sig, g); }
for (const [sig, g] of [...grp].sort((a, b) => b[1].n - a[1].n)) console.log(`${sig}  x${g.n}  dx ${g.dx}  dy ${g.dy}  "${g.ex.text}"  langs ${[...g.langs].join(',')}  at ${[...g.where].slice(0, 4).join(' ')}`);
for (const e of errors) console.log('ERROR ' + e);
console.log(bad.length || errors.length ? `\n${bad.length} controls off by more than ${TOL}px (${grp.size} kinds), ${errors.length} errors, ${total} page states` : `\naligned: ${total} page states, tolerance ${TOL}px`);
process.exit(bad.length || errors.length ? 1 : 0);
