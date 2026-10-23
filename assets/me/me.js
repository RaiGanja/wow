/* Profiles on every page (build_me.py adds this script after radio.js): the api.gabella.site client, the small portrait in the
   top bar, achievement toasts with a short sound, progress hooks (pages, radio, tools, visits) and the secrets.
   Nothing talks to the API until the person has logged in on this device: the session cookie is HttpOnly, so the flag
   localStorage "gabella-me" stands in for it. Only the roster and profile pages ask /me without it, to show the login button.
   Texts come from assets/me/i18n-<lang>.json (achievements, ranks, a few words), loaded when a toast needs them. */
(function () {
  const S = document.currentScript, D = S.dataset;
  const ROOT = D.root || './', HOME = D.home || './', LANG = D.lang || 'ru', PAGE = D.page || '';
  const V = (S.src.match(/\?v=\w+/) || [''])[0];   // build.py me_version(): the same version for the texts
  const API = /^(127\.0\.0\.1|localhost)$/.test(location.hostname) ? 'http://127.0.0.1:8787' : 'https://api.gabella.site';
  const FLAG = 'gabella-me', CACHE = 'gabella-me-cache', SOUND = 'gabella-me-sound', DAY = 'gabella-me-day', CACHE_MS = 10 * 60000;
  const XP1 = 'gabella-me-xp1', TEASER = 'gabella-me-teaser';
  const AUTH_PAGE = /^(roster|profile)\/$/.test(PAGE);
  const ls = {
    get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set(k, v) { try { v === null ? localStorage.removeItem(k) : localStorage.setItem(k, v); } catch (e) { /* private mode */ } },
  };
  const ss = {
    get(k) { try { return JSON.parse(sessionStorage.getItem(k)); } catch (e) { return null; } },
    set(k, v) { try { v === null ? sessionStorage.removeItem(k) : sessionStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* private mode */ } },
  };
  const reduced = () => matchMedia('(prefers-reduced-motion: reduce)').matches;
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, m => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[m]));

  // ---------- API ----------
  function api(path, o = {}) {
    const init = { method: o.method || (o.body !== undefined ? 'POST' : 'GET'), credentials: 'include', headers: {} };
    if (o.body !== undefined) { init.headers['Content-Type'] = 'application/json'; init.body = JSON.stringify(o.body); }
    return fetch(API + path, init).then(r => r.json().catch(() => ({})).then(data => {
      if (r.status === 401) forget();
      if (!r.ok) throw Object.assign(new Error(data.error || 'http_' + r.status), { status: r.status, code: data.error || null });
      return data;
    }));
  }
  const logged = () => ls.get(FLAG) === '1';
  function forget() { ls.set(FLAG, null); ss.set(CACHE, null); state = null; emit(); }

  // ---------- who am I: cached for the tab, refreshed after anything that changes it ----------
  let state = null, loading = null;
  const subs = [];
  function emit() { subs.forEach(cb => { try { cb(state); } catch (e) { console.error(e); } }); dispatchEvent(new CustomEvent('gabella:me', { detail: state })); }
  function onMe(cb) { subs.push(cb); if (state !== undefined && !loading) cb(state); }
  function setMe(m) {
    state = m;
    if (m) { ls.set(FLAG, '1'); ss.set(CACHE, { t: Date.now(), m }); } else ss.set(CACHE, null);
    paintBtn(); emit();
    return m;
  }
  function me(fresh) {
    if (!logged() && !AUTH_PAGE && !fresh) return Promise.resolve(null);
    const c = ss.get(CACHE);
    if (!fresh && c && Date.now() - c.t < CACHE_MS) { if (state !== c.m) setMe(c.m); return Promise.resolve(c.m); }
    if (loading) return loading;
    loading = api('/me').then(setMe, e => (e.status === 401 ? setMe(null) : state)).finally(() => { loading = null; });
    return loading;
  }
  /** Answers of the API that change the person ({me, granted, rankUp, gained}): store the fresh /me and celebrate.
      No more than three toasts at once, the rest waits in the profile; the very first experience gets one quiet note. */
  function took(r) {
    if (r && r.me) setMe(r.me);
    else if (r && (r.granted || []).length) me(true);   // a new achievement moves points, rank and frames: the rare full refresh
    else if (r && state && (r.live || 'lfg' in r)) {   // the API sends what experience changed (Glory, week, season) and the lfg switch: patch, no /me
      if (r.live) Object.assign(state, r.live);
      if ('lfg' in r) state.user.lfg = r.lfg;
      setMe(state);
    }
    const list = [], g = r && r.gained;
    ((r && r.granted) || []).forEach(id => list.push({ kind: 'ach', id }));
    if (r && r.rankUp) list.push({ kind: 'rank', id: r.rankUp });
    if (g && g.glory_up) list.push({ kind: 'glory', id: g.glory_up });
    if (g && g.step_up) list.push({ kind: 'step', id: g.step_up });
    if (g && g.xp > 0 && ls.get(XP1) !== '1') { ls.set(XP1, '1'); if (!list.length) list.push({ kind: 'note', id: 'xp_first' }); }
    list.slice(0, 3).forEach(toast);
    return r;
  }

  // ---------- progress: only for people who logged in; skipped when the server already knows ----------
  const ONCE = new Map(), TOOL = /^(party5|raid40|compare3|share_team)$/;
  const REPEAT = { share_team: 10000, compare3: 10000 };   // a new use after a pause counts again (per-use tool experience)
  /** The server already holds this for good. */
  function server(key, item) {
    const p = state && state.progress && state.progress[key];
    if (!p) return false;
    if (item !== undefined) return (p.items || []).includes(item);
    return ['radio_min', 'search'].indexOf(key) < 0 && p.value >= 1;
  }
  /** Resolves true when there is nothing to send: the server holds it and it feeds neither an open task of this week
      (a repeat counts there) nor a tool's per-use experience. Task id -> key comes with the texts (wk). */
  function known(key, item) {
    if (!server(key, item) || TOOL.test(key)) return Promise.resolve(false);
    const open = ((state.week && state.week.tasks) || []).filter(t => !t.done);
    if (!open.length) return Promise.resolve(true);
    return texts().then(T => !open.some(t => (T.wk || {})[t.id] === key));
  }
  function track(key, item) {
    if (!logged()) return Promise.resolve(null);
    // once per page load; a team of five or forty counts again when the team changes (it is in the hash)
    const id = key + ':' + (item === undefined ? '' : item) + (key === 'party5' || key === 'raid40' ? '#' + location.hash : '');
    const t0 = Date.now(), last = ONCE.get(id);
    if (key !== 'radio_min' && key !== 'search' && last !== undefined && !(REPEAT[key] && t0 - last >= REPEAT[key])) return Promise.resolve(null);
    ONCE.set(id, t0);
    return me().then(() => (state ? known(key, item) : true)).then(skip => {
      if (skip) return null;
      const body = item === undefined ? { key } : { key, item };
      return api('/progress', { body }).then(r => {
        if (state && state.progress && key !== 'visit') {   // keep the cache honest without asking /me again
          const p = state.progress[key] || (state.progress[key] = { value: 0, items: item === undefined ? null : [] });
          if (item === undefined) p.value++; else if (!p.items.includes(item)) { p.items.push(item); p.value = p.items.length; }
          ss.set(CACHE, { t: Date.now(), m: state });
        }
        return took(r);
      }, () => null);
    });
  }

  // ---------- texts ----------
  let tx = null;
  const texts = () => tx || (tx = fetch(ROOT + 'assets/me/i18n-' + LANG + '.json' + V).then(r => r.json()).catch(() => ({ ui: {}, ach: {}, ranks: {} })));

  // ---------- toast: bottom centre, one at a time, like the game ----------
  const queue = [];
  let box = null, busy = false;
  const SMALL = /^(step|note)$/;
  function toast(t) {
    // never a wall of toasts: three at most (queue plus the one on screen); an achievement or rank pushes out a waiting Glory, step or note
    const low = x => /^(glory|step|note)$/.test(x.kind);
    if (queue.length >= 3) {
      const i = queue.findIndex(low);
      if (low(t) || i < 0) return;
      queue.splice(i, 1);
    }
    queue.push(t); if (!busy) next();
  }
  const fillTx = (s, o) => String(s || '').replace(/\{(\w+)\}/g, (m, k) => (k in o ? o[k] : m));
  function next() {
    const t = queue.shift();
    if (!t) { busy = false; return; }
    busy = true;
    texts().then(T => {
      if (!box) { box = document.createElement('div'); box.className = 'me-toasts'; box.setAttribute('role', 'status'); box.setAttribute('aria-live', 'polite'); document.body.append(box); }
      const a = t.kind === 'ach' ? T.ach[t.id] || [t.id] : null;
      const pts = a && T.pts ? T.pts[t.id] : null;
      const el = document.createElement('div');
      const G = T.g || {};
      el.className = 'me-toast' + (t.kind === 'rank' || t.kind === 'glory' ? ' rank' : '') + (SMALL.test(t.kind) ? ' sm' : '') + (reduced() ? '' : ' anim');
      if (SMALL.test(t.kind)) {   // one quiet line: a season step, or the first experience
        const text = t.kind === 'step' ? fillTx(G.season_toast, { n: t.id }) : G[t.id] || '';
        el.innerHTML = `<span class="me-tt"><b>${esc(text)}</b></span>`;
      } else if (t.kind === 'glory') {
        const fr = state && state.user ? state.user.frame || state.user.rank : 'recruit';
        el.innerHTML = `<span class="me-ti"><span class="me-ring fr-${esc(fr)}"><img src="${face(state)}" alt="" width="40" height="40"></span></span>
          <span class="me-tt"><b>${esc(fillTx(G.glory_toast, { n: t.id }))}</b></span>`;
      } else el.innerHTML = `<span class="me-ti">${t.kind === 'rank' ? `<span class="me-ring fr-${esc(t.id)}"><img src="${face(state)}" alt="" width="40" height="40"></span>` : `<img src="${ROOT}assets/me/ach/${esc(t.id)}.webp" alt="" width="44" height="44">`}</span>
        <span class="me-tt"><small>${esc(t.kind === 'rank' ? T.ui.rankUp : T.ui.got)}</small><b>${esc(t.kind === 'rank' ? T.ranks[t.id] || t.id : a[0])}</b></span>
        ${pts ? `<span class="me-shield" aria-label="${esc(pts + ' ' + (T.ui.pts || ''))}">${pts}</span>` : ''}`;
      box.append(el);
      if (!SMALL.test(t.kind)) chime(t.kind === 'rank');
      setTimeout(() => {
        el.classList.add('out');
        setTimeout(() => { el.remove(); next(); }, reduced() ? 0 : 400);
      }, t.kind === 'rank' ? 5000 : SMALL.test(t.kind) ? 3500 : 4000);
    });
  }

  // two short notes, quiet; off with localStorage gabella-me-sound = 0 (switch in the profile)
  let actx = null;
  function chime(rank) {
    if (ls.get(SOUND) === '0') return;
    try {
      actx = actx || new (window.AudioContext || window.webkitAudioContext)();
      if (actx.state === 'suspended') actx.resume();
      const t0 = actx.currentTime + 0.02;
      (rank ? [523.25, 659.25, 783.99] : [659.25, 987.77]).forEach((f, i) => {
        const o = actx.createOscillator(), g = actx.createGain(), at = t0 + i * 0.13;
        o.type = 'triangle'; o.frequency.value = f;
        g.gain.setValueAtTime(0, at); g.gain.linearRampToValueAtTime(0.07, at + 0.015); g.gain.exponentialRampToValueAtTime(0.0001, at + 0.6);
        o.connect(g).connect(actx.destination); o.start(at); o.stop(at + 0.65);
      });
    } catch (e) { /* no audio */ }
  }

  // ---------- small portrait in the top bar ----------
  const FACE = { nightelf: 'night-elf', skyA: 'skyborne-alliance', skyH: 'skyborne-horde' };
  function face(m) {
    const c = m && m.characters && (m.characters.find(x => x.is_main) || m.characters[0]);
    if (!c) return ROOT + 'assets/brand/mark.webp';
    return ROOT + 'assets/art/' + (m.user.portrait === 'class' ? c.class : FACE[c.race] || c.race) + '-face.webp';
  }
  let btn = null;
  function paintBtn() {
    const theme = document.querySelector('.topbar .themebtn');
    if (!theme) return;
    if (!state && !(AUTH_PAGE && !loading)) { if (btn) { btn.remove(); btn = null; } return; }
    texts().then(T => {
      if (!btn) { btn = document.createElement('a'); theme.before(btn); }
      btn.href = HOME + 'profile/';
      if (state) {
        btn.className = 'iconbtn mebtn';
        btn.setAttribute('aria-label', T.ui.profile || 'Profile');
        btn.title = T.ui.profile || '';
        btn.innerHTML = `<span class="me-ring fr-${esc(state.user.frame || state.user.rank)}"><img src="${face(state)}" alt="" width="30" height="30"></span>`;
      } else {
        btn.className = 'iconbtn mebtn login';
        btn.removeAttribute('title'); btn.removeAttribute('aria-label');
        btn.textContent = T.ui.login || 'Log in';
      }
    });
  }

  // ---------- hooks ----------
  function pageHooks() {
    track('lang', LANG);
    const m = PAGE.match(/^(guides|classes|races)\/([\w-]+)\/$/);
    // a language-only guide (data-solo, the uk «ukrainian») is not in the guide set: the API would answer bad_item
    if (m && !(m[1] === 'guides' && D.solo)) track({ guides: 'guide', classes: 'class', races: 'race' }[m[1]], m[2]);
    if (PAGE === 'play/') { track('play_page'); levelFromPlay(); }
    if (PAGE === '404') track('egg', '404');
    const today = new Date().toDateString();
    if (ls.get(DAY) !== today) track('visit').then(r => { if (r) ls.set(DAY, today); });
    track('hour', new Date().getHours());
  }

  // radio.js tells what happens through window events "gabella:radio"
  const tunes = [];
  addEventListener('gabella:radio', e => {
    const d = e.detail || {};
    if (d.type === 'on') track('radio_on');
    else if (d.type === 'minute') track('radio_min');
    else if (d.type === 'sleep') track('sleep_timer');
    else if (d.type === 'station') {
      track('station', d.id);
      const t = Date.now();
      tunes.push(t);
      while (tunes.length && t - tunes[0] > 60000) tunes.shift();
      if (tunes.length >= 10) track('egg', 'static');
    }
  });

  // tools: watched from outside, so the tools page keeps its own code
  function toolsHooks() {
    const team = () => {
      const m = location.hash.match(/^#team=(?:alliance|horde);(\d+);(.*)$/);
      if (!m) return;
      const n = m[2].split(',').filter(x => x && x !== '-').length;
      if (+m[1] === 5 && n >= 5) track('party5');
      if (+m[1] === 40 && n >= 40) track('raid40');
    };
    // capture phase: the tools redraw their pickers on click, so the target is looked at before it leaves the page
    document.addEventListener('click', e => {
      if (e.target.closest('#rCopyLink, #rCopyText')) track('share_team');
      const pick = !!e.target.closest('#cPick');
      setTimeout(() => {
        team();
        const cmp = document.getElementById('cmp');
        if (pick && cmp && cmp.style.getPropertyValue('--n') === '3') track('compare3');
      }, 0);
    }, true);
  }
  let lastQ = '', qTimer = 0;
  const LEEROY = /l+e+r+o+y|лирой|лірой|лиирой/i;
  document.addEventListener('input', e => {
    const el = e.target;
    if (!el.matches || !el.matches('.sfield input, input[type="search"]')) return;
    const q = el.value.trim().toLowerCase();
    if (LEEROY.test(q)) track('egg', 'leeroy');
    clearTimeout(qTimer);
    qTimer = setTimeout(() => { if (q.length >= 2 && q !== lastQ) { lastQ = q; track('search'); } }, 1500);
  });

  // griffin: ten taps on the logo within 20 s (the count survives a page change)
  document.addEventListener('click', e => {
    if (!e.target.closest('.topbar .brand')) return;
    const t = Date.now(), taps = (ss.get('gabella-me-griffin') || []).filter(x => t - x < 20000).concat(t);
    ss.set('gabella-me-griffin', taps);
    if (taps.length >= 10) { ss.set('gabella-me-griffin', null); track('egg', 'griffin'); }
  });

  // the old code
  const KONAMI = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'b', 'a'];
  let kpos = 0;
  addEventListener('keydown', e => {
    const k = e.key.length === 1 ? e.key.toLowerCase() : e.key;
    kpos = k === KONAMI[kpos] ? kpos + 1 : k === KONAMI[0] ? 1 : 0;
    if (kpos === KONAMI.length) { kpos = 0; track('egg', 'konami'); }
  });

  // «В игре» keeps the hero level in gabella-wf-me: when it outgrows the main character, offer to update it in one tap
  function levelFromPlay() {
    let lvl = 0;
    try { lvl = +(JSON.parse(localStorage.getItem('gabella-wf-me')) || {}).lvl || 0; } catch (e) { /* no level */ }
    const main = state && state.characters && state.characters.find(c => c.is_main);
    if (!main || !(lvl > main.level) || lvl > 60 || ss.get('gabella-me-lvl-asked') === lvl) return;
    ss.set('gabella-me-lvl-asked', lvl);
    texts().then(T => {
      const el = document.createElement('div');
      el.className = 'me-ask';
      el.setAttribute('role', 'dialog');
      el.innerHTML = `<span>${esc((T.ui.lvlAsk || '').replace('{name}', main.name).replace('{n}', lvl))}</span>
        <button type="button" class="btn gold">${esc(T.ui.update)}</button><button type="button" class="btn ghost">${esc(T.ui.notNow)}</button>`;
      document.body.append(el);
      const [yes, no] = el.querySelectorAll('button');
      no.onclick = () => el.remove();
      yes.onclick = () => {
        yes.disabled = true;
        api('/characters/' + main.id, { method: 'PUT', body: Object.assign({}, main, { level: lvl }) }).then(r => { el.remove(); took(r); }, () => { el.remove(); });
      };
    });
  }

  window.GabellaMe = { api, me, track, toast, onMe, took, forget, logged, texts, face, API, sound: on => (on === undefined ? ls.get(SOUND) !== '0' : ls.set(SOUND, on ? null : '0')) };

  // signed-out visitors of an article: one line about the profile, closed for good with the cross. Text comes with the page
  // (data-teaser, built per language), so it costs no request.
  function teaser() {
    if (logged() || !D.teaser || ls.get(TEASER) === '0' || !/^(guides|classes|races)\/[\w-]+\/$/.test(PAGE)) return;
    const el = document.createElement('p');
    el.className = 'me-teaser';
    el.innerHTML = `<a href="${esc(HOME)}profile/">${esc(D.teaser)}</a><button type="button" aria-label="${esc(D.close || '×')}">×</button>`;
    el.querySelector('button').onclick = () => { ls.set(TEASER, '0'); el.remove(); };
    const at = document.getElementById('sources');
    if (at) at.before(el); else (document.querySelector('main') || document.body).append(el);
  }

  if (PAGE === 'tools/') toolsHooks();
  teaser();
  if (logged() || AUTH_PAGE) me().then(() => { paintBtn(); if (state) pageHooks(); });
})();
