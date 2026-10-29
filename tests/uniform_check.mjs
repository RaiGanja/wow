// Uniformity check: one repeating component measured on every page / language / width. A component is "uniform" when all
// its instances in one context have the same box, the same type size, the same ring, the icon and the label on one axis.
//   node tests/uniform_check.mjs                       key pages x 9 languages x 390/1440
//   options: --langs ru,en  --widths 390,1440  --pages guides/tier-list/,classes/  --jobs 6  --shots DIR  --json FILE
// Exit code 1 if a component differs. Lists: page / language / width / component / what differs.
import { spawn } from 'node:child_process';
import { createServer } from 'node:http';
import { existsSync, mkdtempSync, readFileSync, statSync, writeFileSync, mkdirSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, extname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const argv = process.argv.slice(2);
const opt = (n, d) => { const i = argv.indexOf('--' + n); return i < 0 ? d : (argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[i + 1] : true); };
const ALL_LANGS = ['ru', 'uk', 'en', 'de', 'fr', 'es', 'pt', 'it', 'pl'];
const langs = (opt('langs', '') || ALL_LANGS.join(',')).split(',');
const widths = (opt('widths', '') || '390,1440').split(',').map(Number);
const subs = (opt('pages', '') || ['', 'classes/', 'guides/tier-list/', 'guides/builds/', 'races/', 'tools/'].join(',')).split(',');
const jobs = +opt('jobs', 6);
const shotsDir = opt('shots', '');
const jsonOut = opt('json', '');

const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.svg': 'image/svg+xml', '.webp': 'image/webp', '.avif': 'image/avif', '.png': 'image/png', '.jpg': 'image/jpeg', '.woff2': 'font/woff2', '.webmanifest': 'application/manifest+json', '.xml': 'application/xml', '.ico': 'image/x-icon' };
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

const CHROME = [process.env.CHROME_PATH, 'C:/Program Files/Google/Chrome/Application/chrome.exe', 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe', '/usr/bin/google-chrome', '/usr/bin/chromium', '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'].find(p => p && existsSync(p));
if (!CHROME) { console.error('Chrome not found (set CHROME_PATH)'); process.exit(2); }
const port = 9900 + Math.floor(Math.random() * 90);
const chrome = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${port}`, '--no-first-run', '--disable-gpu', '--hide-scrollbars', `--user-data-dir=${mkdtempSync(join(tmpdir(), 'uni-'))}`, 'about:blank'], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
let ws;
for (let i = 0; i < 80 && !ws; i++) {
  try { const v = await (await fetch(`http://127.0.0.1:${port}/json/version`)).json(); ws = new WebSocket(v.webSocketDebuggerUrl); } catch { await sleep(250); }
}
await new Promise(r => ws.onopen = r);
let seq = 0; const pend = new Map();
ws.onmessage = e => { const m = JSON.parse(e.data); if (m.id && pend.has(m.id)) { const [ok, bad] = pend.get(m.id); pend.delete(m.id); m.error ? bad(new Error(m.error.message)) : ok(m.result); } };
const send = (method, params = {}, sessionId) => new Promise((ok, bad) => { const id = ++seq; pend.set(id, [ok, bad]); ws.send(JSON.stringify({ id, method, params, sessionId })); });

// The probe runs in the page. COMPONENTS: a group = elements that must look the same; `each` = how to measure one element.
const PROBE = `() => {
  const out = [];
  const r1 = n => Math.round(n * 10) / 10;
  const box = e => e.getBoundingClientRect();
  const fs = e => { const c = getComputedStyle(e); return c.fontSize + '/' + c.fontWeight + '/' + c.lineHeight; };
  const ring = e => getComputedStyle(e).boxShadow.replace(/rgba?\\([^)]*\\)/g, 'C');
  const mid = r => r.top + r.height / 2;
  const groups = {};
  const add = (name, ctx, key, val) => { ((groups[name + ' | ' + ctx] ||= {})[key] ||= new Set()).add(val); };
  const vis = e => { const r = box(e); return r.width > 1 && r.height > 1 && getComputedStyle(e).visibility !== 'hidden'; };
  // 1. every round portrait: a square, the same ring for the same size
  for (const e of document.querySelectorAll('.av:not(.off)')) { if (!vis(e)) continue; const r = box(e);
    const ctx = e.parentElement.closest('[class]')?.className.toString().split(' ')[0] + '>' + Math.round(r.width);
    add('portrait', ctx, 'square', r1(r.width) === r1(r.height) ? 'ok' : r1(r.width) + 'x' + r1(r.height));
    add('portrait', ctx, 'ring', ring(e));
    const im = e.querySelector('img'); if (im) { const c = getComputedStyle(im); add('portrait', ctx, 'img-fit', c.objectFit + '/' + c.objectPosition + '/' + Math.round(box(im).width - r.width)); } }
  // 2. tier grid: chips of one width, labels of one size on the portrait's axis, rows of one height, the letter on the centre
  for (const p of document.querySelectorAll('.tgbox [role="tabpanel"]')) { if (p.hidden) continue;
    for (const c of p.querySelectorAll('.tgc')) { const a = c.querySelector('.av'), n = c.querySelector('.tgn'), rc = box(c), ra = box(a), rn = box(n);
      add('tier chip', 'grid', 'chip width', r1(rc.width)); add('tier chip', 'grid', 'portrait', r1(ra.width));
      add('tier chip', 'grid', 'label size', fs(n)); add('tier chip', 'grid', 'label top - portrait bottom', r1(rn.top - ra.bottom));
      const nr = document.createRange(); nr.selectNodeContents(n.firstChild); const t = nr.getBoundingClientRect();
      add('tier chip', 'grid', 'name centre - portrait centre', r1((t.left + t.right) / 2 - (ra.left + ra.right) / 2));
      add('tier chip', 'grid', 'label wraps', t.height > parseFloat(getComputedStyle(n).lineHeight) * 1.5 ? 'wraps' : 'one line'); }
    for (const li of p.querySelectorAll('.tgrid li')) { const l = li.querySelector('.tgl'), a = li.querySelector('.av'); if (!a) continue;
      const cs = [...li.querySelectorAll('.tgc')].map(box); add('tier row', 'grid', 'space above', r1(Math.min(...cs.map(c => c.top)) - box(li).top)); add('tier row', 'grid', 'space below', r1(box(li).bottom - Math.max(...cs.map(c => c.bottom)))); add('tier row', 'grid', 'letter centre - portrait centre', r1(mid(box(l)) - mid(box(a)))); add('tier row', 'grid', 'letter size', fs(l)); } }
  // 3. a class link with a small portrait: the portrait and the name on one axis
  for (const c of document.querySelectorAll('.clink')) { if (!vis(c)) continue; const a = c.querySelector('.av'); if (!a) continue;
    const ctx = c.classList.contains('two') ? 'two' : 'one'; add('class link', ctx, 'portrait', r1(box(a).width));
    const t = c.querySelector('.cn, b') || c; const nr = document.createRange(); nr.selectNodeContents(t); add('class link', ctx, 'portrait centre - text centre', r1(mid(box(a)) - mid(nr.getBoundingClientRect()))); add('class link', ctx, 'text size', fs(c)); }
  // 4. the class picker on a phone
  for (const a of document.querySelectorAll('.cpick a')) { if (!vis(a)) continue; const r = box(a);
    add('class picker', 'grid', 'tile', r1(r.width) + 'x' + r1(r.height)); add('class picker', 'grid', 'portrait', r1(box(a.querySelector('.av')).width)); add('class picker', 'grid', 'label size', fs(a.querySelector('b'))); }
  for (const [g, keys] of Object.entries(groups)) for (const [k, set] of Object.entries(keys)) {
    const vals = [...set]; const nums = vals.map(Number);
    const spread = nums.every(n => !Number.isNaN(n)) ? Math.max(...nums) - Math.min(...nums) : (vals.length > 1 ? 99 : 0);
    if (spread > 1.01) out.push([g, k, vals.slice(0, 6).join(' | ')]);   // more than 1px apart
  }
  const total = { portraits: document.querySelectorAll('.av').length, chips: document.querySelectorAll('.tgc').length, links: document.querySelectorAll('.clink').length };
  return { out, total };
}`;

async function newWorker() {
  const { browserContextId } = await send('Target.createBrowserContext');
  const { targetId } = await send('Target.createTarget', { url: 'about:blank', browserContextId });
  const { sessionId } = await send('Target.attachToTarget', { targetId, flatten: true });
  const S = (m, p) => send(m, p, sessionId);
  await S('Page.enable'); await S('Runtime.enable');
  const ev = async (expr) => {
    const r = await S('Runtime.evaluate', { expression: expr, returnByValue: true, awaitPromise: true });
    if (r.exceptionDetails) throw new Error(r.exceptionDetails.exception?.description || r.exceptionDetails.text);
    return r.result.value;
  };
  return { S, ev };
}

const found = []; const counts = [];
async function checkPage(w, job) {
  const { S, ev } = w; const { lang, sub, url, width } = job;
  await S('Emulation.setDeviceMetricsOverride', { width, height: width < 700 ? 800 : 900, deviceScaleFactor: 1, mobile: width < 700 });
  await S('Page.addScriptToEvaluateOnNewDocument', { source: `try{localStorage.setItem('wf-theme','dark');localStorage.setItem('gabella-lang','${lang}')}catch(e){}` });
  await S('Page.navigate', { url: base + url });
  for (let i = 0; i < 80; i++) { if (await ev(`document.readyState`) === 'complete') break; await sleep(100); }
  await ev(`document.fonts.ready.then(()=>1)`);
  await ev(`Promise.all([...document.images].map(i=>i.loading==='lazy'?(i.loading='eager',i.decode().catch(()=>0)):0))`);
  await ev(`(()=>{const st=document.createElement('style');st.textContent='*,*::before,*::after{animation:none!important;transition:none!important}';document.head.append(st);document.querySelectorAll('.reveal,[data-reveal]').forEach(e=>e.classList.add('in','on','shown'));return 0})()`);
  await sleep(300);
  const shot = async (name, sel) => {
    if (!shotsDir) return;
    const clip = await ev(`(()=>{const e=document.querySelector(${JSON.stringify(sel)});if(!e)return null;e.scrollIntoView({block:'start'});const r=e.getBoundingClientRect();return {x:Math.max(0,r.left+scrollX-8),y:r.top+scrollY-8,width:Math.min(r.width+16,innerWidth),height:Math.min(r.height+16,2200),scale:1}})()`);
    if (!clip) return; const r = await S('Page.captureScreenshot', { format: 'png', clip, captureBeyondViewport: true });
    mkdirSync(shotsDir, { recursive: true }); writeFileSync(join(shotsDir, `${name}.png`), Buffer.from(r.data, 'base64'));
  };
  const probe = async state => { const { out, total } = await ev(`(${PROBE})()`); counts.push({ page: '/' + sub, lang, width, state, ...total });
    for (const [g, k, v] of out) found.push({ page: '/' + sub, lang, width, state, component: g, differs: k, values: v }); };
  await probe('page');
  if (sub === 'guides/tier-list/') {
    const tabs = await ev(`[...document.querySelectorAll('.tgbox [role="tab"]')].length`);
    for (let i = 0; i < tabs; i++) { await ev(`document.querySelectorAll('.tgbox [role="tab"]')[${i}].click();0`); await sleep(120); await probe('tier tab ' + i); await shot(`${lang}-${width}-tier${i}`, '.tgbox'); }
  }
  if (sub === 'classes/') await shot(`${lang}-${width}-classes`, width < 720 ? '.cpick' : 'main');
  if (sub === '') await shot(`${lang}-${width}-home-top`, 'body');
}

const queue = [];
for (const lang of langs) for (const sub of subs) for (const width of widths) queue.push({ lang, sub, width, url: (lang === 'ru' ? '' : lang + '/') + sub });
const workers = await Promise.all(Array.from({ length: Math.min(jobs, queue.length) }, newWorker));
await Promise.all(workers.map(async w => { for (let j; (j = queue.shift());) { try { await checkPage(w, j); } catch (e) { found.push({ page: '/' + j.sub, lang: j.lang, width: j.width, component: 'ERROR', differs: String(e.message).slice(0, 120), values: '' }); } } }));
chrome.kill(); server.close();
found.sort((a, b) => (a.component + a.differs + a.lang + a.width + a.page).localeCompare(b.component + b.differs + b.lang + b.width + b.page));
if (jsonOut) writeFileSync(jsonOut, JSON.stringify({ found, counts }, null, 1));
for (const f of found) console.log(`${f.page}  ${f.lang}  ${f.width}  [${f.state || ''}] ${f.component}: ${f.differs}  ${f.values}`);
console.log(found.length ? `\n${found.length} differences` : `\nuniform: ${counts.length} page states, ${counts.reduce((a, c) => a + c.portraits, 0)} portraits, ${counts.reduce((a, c) => a + c.chips, 0)} tier chips`);
process.exit(found.length ? 1 : 0);
