// Ищет текст, который обрезан или вылезает за карточку: headless Chrome по CDP, без зависимостей (Node 22+).
// Запуск: node tests/clip_probe.mjs --base http://127.0.0.1:8765 [--langs ru,en] [--widths 375,1380] [--themes light,dark]
//         [--pages home,classes,races] [--shot DIR] [--json]
// Для каждой страницы/языка/ширины/темы: у карточек .hc по очереди открывается каждая (класс .on), и все текстовые узлы
// сверяются с ближайшим предком, который режет содержимое (overflow hidden/clip), и с границей окна.
import { spawn } from 'node:child_process';
import { mkdtempSync, writeFileSync, mkdirSync, readdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const argv = process.argv.slice(2);
const opt = (k, d) => { const i = argv.indexOf('--' + k); return i < 0 ? d : (argv[i + 1] ?? true); };
const BASE = String(opt('base', 'http://127.0.0.1:8765')).replace(/\/$/, '');
const LANGS = String(opt('langs', 'ru,en,uk,de,fr,es,pt,it,pl')).split(',');
const WIDTHS = String(opt('widths', '375,768,1380,1920,3440')).split(',').map(Number);
const THEMES = String(opt('themes', 'light,dark')).split(',');
const PAGES = String(opt('pages', 'home,classes,races,class,race,guides,misc')).split(',');
const SHOT = opt('shot', '');
const FAST = opt('fast', false);   // без переходов: карточка раскрывается мгновенно, проверка в разы быстрее

import { existsSync } from 'node:fs';
const chromePath = process.env.CHROME || ['C:/Program Files/Google/Chrome/Application/chrome.exe', '/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser'].find(existsSync);
if (!chromePath) { console.error('Chrome не найден (CHROME=путь)'); process.exit(2); }

const CLASSES = ['warrior', 'paladin', 'hunter', 'rogue', 'priest', 'shaman', 'mage', 'warlock', 'druid'];
const RACES = ['human', 'dwarf', 'night-elf', 'gnome', 'skyborne-alliance', 'orc', 'undead', 'tauren', 'troll', 'skyborne-horde'];
const ROOT = join(fileURLToPath(import.meta.url), '..', '..');
const GUIDES = readdirSync(join(ROOT, 'guides'), { withFileTypes: true }).filter(d => d.isDirectory()).map(d => d.name);
const pathFor = (page, lang) => {
  const pre = lang === 'ru' ? '/' : `/${lang}/`;
  return { home: [pre], classes: [pre + 'classes/'], races: [pre + 'races/'],
    guides: [pre + 'guides/', ...GUIDES.map(g => `${pre}guides/${g}/`)], misc: ['tools/', 'roster/', 'play/'].map(x => pre + x),
    class: CLASSES.map(c => `${pre}classes/${c}/`), race: RACES.map(r => `${pre}races/${r}/`) }[page];
};

const port = 9300 + Math.floor(Math.random() * 500);
const dir = mkdtempSync(join(tmpdir(), 'clipprobe-'));
const chrome = spawn(chromePath, [`--remote-debugging-port=${port}`, `--user-data-dir=${dir}`, '--headless=new', '--disable-gpu', '--no-first-run', '--hide-scrollbars', 'about:blank'], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
let ws, seq = 0; const pend = new Map();
async function connect() {
  for (let i = 0; i < 80; i++) {
    try {
      const list = await (await fetch(`http://127.0.0.1:${port}/json`)).json();
      const pg = list.find(t => t.type === 'page');
      if (pg) { ws = new WebSocket(pg.webSocketDebuggerUrl); await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; }); break; }
    } catch { /* ждём запуска */ }
    await sleep(250);
  }
  if (!ws) throw new Error('Chrome не отвечает');
  ws.onmessage = e => { const m = JSON.parse(e.data); if (m.id && pend.has(m.id)) { pend.get(m.id)(m); pend.delete(m.id); } };
}
const send = (method, params = {}) => new Promise((res, rej) => { const id = ++seq; pend.set(id, m => m.error ? rej(new Error(method + ': ' + m.error.message)) : res(m.result)); ws.send(JSON.stringify({ id, method, params })); });
const ev = async expr => { const r = await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true }); if (r.exceptionDetails) throw new Error(r.exceptionDetails.text + ' ' + (r.exceptionDetails.exception?.description || '')); return r.result.value; };

// В странице: каждая карточка открывается по очереди; смотрим все текстовые узлы.
const PROBE = `(async () => {
  await document.fonts.ready;
  const out = []; window.__dbg = document.querySelectorAll(".hc").length;
  const EPS = 0.75;
  const clipper = el => { for (let p = el.parentElement; p; p = p.parentElement) { const o = getComputedStyle(p); if (/hidden|clip/.test(o.overflowX) && p !== document.documentElement && p !== document.body) return p; } return null; };
  const label = el => (el.tagName.toLowerCase() + (el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\\s+/).join('.') : ''));
  function scan(tag) {
    const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    for (let n; (n = w.nextNode());) {
      const t = n.nodeValue.replace(/\\s+/g, ' ').trim(); if (!t) continue;
      const el = n.parentElement; if (!el || /^(SCRIPT|STYLE|NOSCRIPT|TITLE)$/.test(el.tagName)) continue;
      const cs = getComputedStyle(el); if (cs.visibility === 'hidden' || cs.display === 'none') continue;
      if (+cs.opacity === 0 || el.closest('[hidden],[aria-hidden="true"]:not(.vn),.sr,.sr-only,.visually-hidden')) continue;
      let sr = false;   // text hidden for the eye only (a 1 px box that clips, e.g. the header wordmark on 375–719 px): for screen readers, not a cut
      for (let p = el; p && !sr; p = p.parentElement) { const q = p.getBoundingClientRect(); sr = q.width <= 1 && q.height <= 1 && /hidden|clip/.test(getComputedStyle(p).overflowX); }
      if (sr) continue;
      const hc = el.closest('.hc'); if (hc && !hc.classList.contains('on') && !el.classList.contains('vn')) continue;   // подпись закрытой карточки — только .vn
      if (hc && hc.classList.contains('on') && el.classList.contains('vn')) continue;
      const r = document.createRange(); r.selectNodeContents(n);
      const rects = [...r.getClientRects()].filter(q => q.width > 0.5 && q.height > 0.5); if (!rects.length) continue;
      const l = Math.min(...rects.map(q => q.left)), rt = Math.max(...rects.map(q => q.right)), tp = Math.min(...rects.map(q => q.top)), bt = Math.max(...rects.map(q => q.bottom));
      const c = clipper(el);
      if (c && (getComputedStyle(c).textOverflow === 'ellipsis' || cs.textOverflow === 'ellipsis')) continue;   // намеренное «…» (подсказка поиска)
      let why = '';
      if (c) {
        const cr = c.getBoundingClientRect(); const pad = parseFloat(getComputedStyle(c).paddingRight) || 0;
        const vis = Math.max(0, Math.min(rt, cr.right) - Math.max(l, cr.left)), full = rt - l;
        if (rt > cr.right + EPS || l < cr.left - EPS) why = 'x:' + Math.round(rt - cr.right) + '/' + Math.round(cr.left - l);
        else if (hc && el.closest('.info') && rt > cr.right - 6 + EPS && el.closest('b')) why = 'edge';   // заголовок вплотную к краю карточки
        if (!why && (bt > cr.bottom + EPS || tp < cr.top - EPS) && getComputedStyle(c).overflowY !== 'visible') why = 'y:' + Math.round(bt - cr.bottom);
      }
      if (!why && !el.closest('svg,.tabs2,table')) {   // слово шире собственной коробки: вылезает на соседей
        const er = el.getBoundingClientRect(), ecs = getComputedStyle(el);
        if (ecs.display !== 'inline' && rt > er.right - (parseFloat(ecs.paddingRight) || 0) + 1.5 && ecs.whiteSpace !== 'nowrap') why = 'box:' + Math.round(rt - er.right);
      }
      if (!why && (rt > innerWidth + EPS || l < -EPS) && !el.closest('[class*="scroll"],.tabs2,table,pre,code,.marq,.rail,.strip,.carousel')) {
        // вылезает за окно, если ни один предок не прокручивается
        let sc = false; for (let p = el.parentElement; p; p = p.parentElement) { if (/auto|scroll/.test(getComputedStyle(p).overflowX) && p.scrollWidth > p.clientWidth) { sc = true; break; } }
        if (!sc) why = 'viewport:' + Math.round(rt - innerWidth);
      }
      if (why) out.push({ tag, why, text: t.slice(0, 40), el: label(el) + (c ? ' ⊂ ' + label(c) : '') });
    }
  }
  const cards = [...document.querySelectorAll('.hc')];
  const groups = new Map(); cards.forEach(c => { const g = c.parentElement; if (!groups.has(g)) groups.set(g, []); groups.get(g).push(c); });
  // уже видимые панели: каждая карточка по очереди
  const tabs = [...document.querySelectorAll('#classes [role="tab"]')];
  const panels = tabs.length ? tabs : [null];
  for (const tab of panels) {
    if (tab) { tab.click(); await new Promise(r => setTimeout(r, 50)); }
    for (const [g, list] of groups) {
      if (!g.offsetParent) continue;
      for (const c of list) {
        list.forEach(x => x.classList.toggle('on', x === c));
        await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
        await new Promise(r => setTimeout(r, window.__fast ? 30 : 750));   // flex-grow .55s
        scan((g.id || g.className) + ' → ' + (c.getAttribute('href') || '').replace(/\\/$/, '').split('/').pop());
      }
    }
  }
  if (!cards.length) scan('page');
  return out;
})()`;

async function main() {
  await connect();
  await send('Page.enable');
  const results = []; let checked = 0;
  for (const theme of THEMES) for (const width of WIDTHS) {
    const mobile = width < 768;
    await send('Emulation.setDeviceMetricsOverride', { width, height: mobile ? 812 : 1000, deviceScaleFactor: 1, mobile });
    await send('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-color-scheme', value: theme }] });
    for (const lang of LANGS) for (const page of PAGES) for (const path of pathFor(page, lang)) {
      await send('Page.navigate', { url: BASE + path });
      await sleep(350);
      if ((await ev('location.href')).startsWith('chrome-error')) throw new Error('страница не открылась: ' + BASE + path);
      await ev(`new Promise(r => { if (document.readyState === 'complete') r(); else addEventListener('load', r); })`);
      await ev(`try { localStorage.setItem('wf-theme', '${theme}') } catch (e) {} ; document.documentElement.dataset.theme = '${theme}'; 1`);
      await ev(`new Promise(r => { const t0 = Date.now(); (function w() { if (!document.querySelector('#roster') || document.querySelector('#roster .hc') || Date.now() - t0 > 8000) r(); else setTimeout(w, 100); })(); })`);
      if (FAST) await ev(`window.__fast = 1; const st = document.createElement('style'); st.textContent = '*,*::before,*::after{transition:none!important;animation:none!important}'; document.head.append(st); 1`);
      if (opt('eval', '')) console.log(path, await ev(`(async()=>{${opt('eval', '')}})()`));
      if (opt('snap', '')) { mkdirSync(opt('snap', ''), { recursive: true }); await sleep(900); const sh = await send('Page.captureScreenshot', { format: 'png' }); writeFileSync(join(opt('snap', ''), `${lang}-${width}-${theme}-${path.replace(/\W+/g, '_')}.png`), Buffer.from(sh.data, 'base64')); }
      const found = await ev(PROBE); if (process.env.DBG) console.log(path, await ev('document.querySelectorAll(".hc").length+" "+location.href+" "+document.readyState'));
      checked++;
      const seen = new Set();
      for (const f of found) { const k = f.tag + f.text + f.why; if (seen.has(k)) continue; seen.add(k); results.push({ theme, width, lang, page, path, ...f }); }
      if (SHOT && found.length) {
        mkdirSync(SHOT, { recursive: true });
        const shot = await send('Page.captureScreenshot', { format: 'png' });
        writeFileSync(join(SHOT, `${page}-${lang}-${width}-${theme}-${path.replace(/\W+/g, '_')}.png`), Buffer.from(shot.data, 'base64'));
      }
    }
  }
  return { results, checked };
}

try {
  const { results, checked } = await main();
  if (opt('json', false)) console.log(JSON.stringify(results, null, 1));
  else { for (const r of results) console.log(`${r.theme} ${r.width} ${r.lang} ${r.path} [${r.tag}] «${r.text}» ${r.why} ${r.el}`); }
  console.log(`проверено страниц×состояний: ${checked}, обрезок: ${results.length}`);
  process.exitCode = results.length ? 1 : 0;
} catch (e) { console.error(e); process.exitCode = 2; }
finally { try { ws?.close(); } catch {} chrome.kill(); }
