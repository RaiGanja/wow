/* Radio of the guide: the header button .radiobtn (put in by build.py pwa()) opens a panel with 4 stations
   (tracks from stations.json, made by tools/make_radio.py) and ambient sounds synthesised with Web Audio
   (campfire, rain, wind). State lives in localStorage, so the music goes on after moving to another page:
   it restarts at the saved second if the page changed less than a minute ago; when the browser blocks
   autoplay, the first click or key press on the new page resumes it. */
(() => {
  const SCRIPT = document.currentScript, ROOT = SCRIPT.dataset.root || './';
  const btn = document.querySelector('.radiobtn');
  if (!btn) return;
  const LANG = ['en', 'uk'].includes(document.documentElement.lang) ? document.documentElement.lang : 'ru';
  const L = {
    ru: { title: 'Радио Gabella', play: 'Играть', pause: 'Пауза', prev: 'Предыдущий трек', next: 'Следующий трек', close: 'Закрыть',
      vol: 'Громкость музыки', seek: 'Позиция в треке', amb: 'Звуки вокруг', fire: 'Костёр', rain: 'Дождь', wind: 'Ветер',
      ambVol: 'Громкость: ', music: 'Музыка', err: 'Трек не загрузился — проверьте сеть', pick: 'Выберите станцию' },
    en: { title: 'Gabella Radio', play: 'Play', pause: 'Pause', prev: 'Previous track', next: 'Next track', close: 'Close',
      vol: 'Music volume', seek: 'Track position', amb: 'Sounds around', fire: 'Campfire', rain: 'Rain', wind: 'Wind',
      ambVol: 'Volume: ', music: 'Music', err: 'The track did not load — check your connection', pick: 'Pick a station' },
    uk: { title: 'Радіо Gabella', play: 'Грати', pause: 'Пауза', prev: 'Попередній трек', next: 'Наступний трек', close: 'Закрити',
      vol: 'Гучність музики', seek: 'Позиція в треку', amb: 'Звуки довкола', fire: 'Багаття', rain: 'Дощ', wind: 'Вітер',
      ambVol: 'Гучність: ', music: 'Музика', err: 'Трек не завантажився — перевірте мережу', pick: 'Оберіть станцію' },
  }[LANG];
  const KEY = 'gabella-radio', RESUME_MS = 60000;
  const ICO = {
    play: '<path d="M8 5.5v13l11-6.5z" fill="currentColor" stroke="none"/>',
    pause: '<path d="M8 5h3v14H8zM13 5h3v14h-3z" fill="currentColor" stroke="none"/>',
    prev: '<path d="M6 5v14M18 6 9 12l9 6z"/>', next: '<path d="M18 5v14M6 6l9 6-9 6z"/>', x: '<path d="M6 6l12 12M18 6 6 18"/>',
    vol: '<path d="M4 9.5h3.5L12 6v12l-4.5-3.5H4z"/><path d="M15.5 9a4 4 0 0 1 0 6M18 6.5a7.5 7.5 0 0 1 0 11"/>',
    fire: '<path d="M12 3c.5 3.5 4.5 5 4.5 10a4.5 4.5 0 0 1-9 0c0-2.5 1.5-3.5 2.2-5.3.8 1.3 1.3 2.3 1.3 3.3 1-1.5 1.5-4.5 1-8z"/><path d="M5 21h14"/>',
    rain: '<path d="M7 15a4 4 0 0 1 .5-8 5.5 5.5 0 0 1 10.5 1.5A3.3 3.3 0 0 1 17.5 15z"/><path d="M8.5 18l-1 2.5M12.5 18l-1 2.5M16.5 18l-1 2.5"/>',
    wind: '<path d="M3 9h11a3 3 0 1 0-3-3M3 15h15a3 3 0 1 1-3 3M3 12h7"/>',
  };
  const svg = (k, cls = 'ico') => `<svg class="${cls}" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${ICO[k]}</svg>`;
  const fmt = s => (s = Math.max(0, Math.floor(s || 0)), Math.floor(s / 60) + ':' + String(s % 60).padStart(2, '0'));

  // ---------- state ----------
  const st = Object.assign({ s: null, i: 0, t: 0, on: false, vol: 0.6, amb: { fire: 0, rain: 0, wind: 0 }, ts: 0 }, read());
  function read() { try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { return {}; } }
  function save() { st.ts = Date.now(); try { localStorage.setItem(KEY, JSON.stringify(st)); } catch (e) { /* private mode */ } }

  let data = null;
  const getData = () => data ? Promise.resolve(data) : fetch(ROOT + 'assets/radio/stations.json').then(r => r.json()).then(d => (data = d));
  const station = () => data && data.stations.find(s => s.id === st.s);
  const track = () => station() && station().tracks[st.i];
  const art = s => ROOT + 'assets/art/' + s.art + '.webp';

  // ---------- music ----------
  const audio = new Audio();
  audio.preload = 'none';
  audio.volume = st.vol;
  let failed = false;

  function load(at = 0) {
    const t = track();
    if (!t) return;
    audio.src = ROOT + 'assets/radio/' + t.f;
    if (at) audio.addEventListener('loadedmetadata', () => { audio.currentTime = Math.min(at, (audio.duration || at + 1) - 1); }, { once: true });
    failed = false;
    meta();
  }
  function play() {
    if (!audio.src) load(st.t);
    if (ctx && ctx.state === 'suspended') ctx.resume();
    return audio.play().then(() => { st.on = true; save(); render(); }, () => { st.on = false; render(); });
  }
  function pause() { audio.pause(); st.on = false; save(); render(); }
  function step(d) {
    const s = station();
    if (!s) return;
    st.i = (st.i + d + s.tracks.length) % s.tracks.length; st.t = 0;
    load(); play();
  }
  function tune(id) {
    if (st.s === id) return st.on ? pause() : play();
    st.s = id; st.t = 0;
    st.i = Math.floor(Math.random() * station().tracks.length);
    load(); play();
  }
  audio.addEventListener('ended', () => step(1));
  audio.addEventListener('error', () => { if (!audio.src) return; failed = true; st.on = false; render(); });
  let lastSave = 0;
  audio.addEventListener('timeupdate', () => {
    st.t = audio.currentTime;
    if (Date.now() - lastSave > 2000) { lastSave = Date.now(); save(); }
    progress();
  });
  addEventListener('pagehide', () => { if (audio.src) st.t = audio.currentTime; save(); });

  function meta() {
    const s = station(), t = track();
    if (!('mediaSession' in navigator) || !t) return;
    navigator.mediaSession.metadata = new MediaMetadata({ title: t.t, artist: 'Kevin MacLeod', album: L.title + ' · ' + s.name[LANG],
      artwork: [{ src: new URL(art(s), location).href, sizes: '960x540', type: 'image/webp' }] });
    navigator.mediaSession.setActionHandler('play', play);
    navigator.mediaSession.setActionHandler('pause', pause);
    navigator.mediaSession.setActionHandler('previoustrack', () => step(-1));
    navigator.mediaSession.setActionHandler('nexttrack', () => step(1));
  }

  // ---------- ambient sounds (Web Audio, nothing to download) ----------
  let ctx = null;
  const layers = {};
  function ac() {
    if (!ctx) {
      const C = window.AudioContext || window.webkitAudioContext;
      if (!C) return null;
      ctx = new C();
    }
    if (ctx.state === 'suspended') ctx.resume();
    return ctx;
  }
  function noise(c, brown) {
    const b = c.createBuffer(1, c.sampleRate * 4, c.sampleRate), d = b.getChannelData(0);
    let last = 0;
    for (let i = 0; i < d.length; i++) {
      const w = Math.random() * 2 - 1;
      d[i] = brown ? (last = (last + 0.02 * w) / 1.02) * 3.5 : w;
    }
    const src = c.createBufferSource();
    src.buffer = b; src.loop = true;
    return src;
  }
  function filter(c, type, freq, q = 0.7) { const f = c.createBiquadFilter(); f.type = type; f.frequency.value = freq; f.Q.value = q; return f; }
  function lfo(c, rate, depth, target) {
    const o = c.createOscillator(), g = c.createGain();
    o.frequency.value = rate; g.gain.value = depth;
    o.connect(g).connect(target); o.start();
    return o;
  }
  const SYNTH = {
    fire(c, out) {
      const rumble = noise(c, true), g = c.createGain();
      g.gain.value = 0.55;
      rumble.connect(filter(c, 'lowpass', 260)).connect(g).connect(out); rumble.start();
      const crackle = noise(c, false), hp = filter(c, 'highpass', 2200), cg = c.createGain();
      cg.gain.value = 0;
      crackle.connect(hp).connect(cg).connect(out); crackle.start();
      let timer = 0;
      (function pop() {   // short random pops, a few per second, sometimes in bursts
        const now = c.currentTime, n = Math.random() < 0.25 ? 3 : 1;
        for (let k = 0; k < n; k++) {
          const t = now + k * (0.02 + Math.random() * 0.05), a = 0.15 + Math.random() * 0.6, len = 0.004 + Math.random() * 0.025;
          cg.gain.setValueAtTime(a, t); cg.gain.exponentialRampToValueAtTime(0.0001, t + len);
        }
        hp.frequency.setValueAtTime(1500 + Math.random() * 3500, now);
        timer = setTimeout(pop, 80 + Math.random() * 520);
      })();
      return () => { clearTimeout(timer); rumble.stop(); crackle.stop(); };
    },
    rain(c, out) {
      const hiss = noise(c, false), g = c.createGain();
      g.gain.value = 0.22;
      hiss.connect(filter(c, 'highpass', 900)).connect(filter(c, 'lowpass', 7000)).connect(g).connect(out); hiss.start();
      const body = noise(c, true), bg = c.createGain();
      bg.gain.value = 0.5;
      body.connect(filter(c, 'lowpass', 1100)).connect(bg).connect(out); body.start();
      const swell = lfo(c, 0.06, 0.08, g.gain);
      return () => { hiss.stop(); body.stop(); swell.stop(); };
    },
    wind(c, out) {
      const src = noise(c, true), bp = filter(c, 'bandpass', 520, 1.4), g = c.createGain();
      g.gain.value = 0.9;
      src.connect(bp).connect(g).connect(out); src.start();
      const howl = lfo(c, 0.07, 260, bp.frequency), gust = lfo(c, 0.11, 0.45, g.gain);
      return () => { src.stop(); howl.stop(); gust.stop(); };
    },
  };
  function ambient(name, level) {
    st.amb[name] = level; save();
    const c = level > 0 ? ac() : ctx;
    if (!c) return;
    let l = layers[name];
    if (level > 0 && !l) {
      const gain = c.createGain();
      gain.gain.value = 0;
      gain.connect(c.destination);
      l = layers[name] = { gain, stop: SYNTH[name](c, gain) };
    }
    if (!l) return;
    l.gain.gain.setTargetAtTime(level * 0.5, c.currentTime, 0.4);
    if (level === 0) {
      setTimeout(() => { if (st.amb[name] === 0 && layers[name] === l) { l.stop(); l.gain.disconnect(); delete layers[name]; } }, 2500);
    }
  }

  // ---------- panel ----------
  let panel = null;
  const $ = s => panel.querySelector(s);
  function build() {
    panel = document.createElement('div');
    panel.className = 'rdo'; panel.id = 'radioPanel'; panel.hidden = true;
    panel.setAttribute('role', 'dialog'); panel.setAttribute('aria-label', L.title);
    const tiles = data.stations.map(s => `<button class="rdo-tile" type="button" data-s="${s.id}" aria-pressed="false">
      <img src="${art(s)}" alt="" loading="lazy" decoding="async" style="object-position:${s.pos || '50% 50%'}"><span class="rdo-tn"><b>${s.name[LANG]}</b><span>${s.mood[LANG]}</span></span>
      <span class="rdo-eq" aria-hidden="true"><i></i><i></i><i></i></span></button>`).join('');
    const amb = ['fire', 'rain', 'wind'].map(n => `<div class="rdo-amb-row">
      <button class="rdo-amb-t" type="button" data-a="${n}" aria-pressed="false">${svg(n)}<span>${L[n]}</span></button>
      <input class="rdo-range" type="range" min="0" max="1" step="0.05" data-a="${n}" aria-label="${L.ambVol}${L[n]}"></div>`).join('');
    const credits = data.stations.flatMap(s => s.tracks.map(t => `<li>«${t.t}»</li>`)).join('');
    panel.innerHTML = `<div class="rdo-hero"><img class="rdo-art" alt="" decoding="async">
      <div class="rdo-now"><span class="rdo-st"></span><b class="rdo-tt"></b></div>
      <button class="rdo-x" type="button" aria-label="${L.close}">${svg('x')}</button></div>
      <div class="rdo-body">
      <div class="rdo-seekrow"><span class="rdo-cur">0:00</span><input class="rdo-range rdo-seek" type="range" min="0" max="1" step="1" value="0" aria-label="${L.seek}"><span class="rdo-dur">0:00</span></div>
      <div class="rdo-ctl">
        <button class="rdo-b" type="button" data-do="prev" aria-label="${L.prev}">${svg('prev')}</button>
        <button class="rdo-b rdo-play" type="button" data-do="play" aria-label="${L.play}">${svg('play')}</button>
        <button class="rdo-b" type="button" data-do="next" aria-label="${L.next}">${svg('next')}</button>
        <label class="rdo-vol">${svg('vol')}<input class="rdo-range" type="range" min="0" max="1" step="0.05" aria-label="${L.vol}"></label>
      </div>
      <div class="rdo-tiles">${tiles}</div>
      <p class="rdo-h">${L.amb}</p>
      <div class="rdo-amb">${amb}</div>
      <details class="rdo-cr"><summary>${L.music}: ${data.author} · ${data.license}</summary>
        <ol>${credits}</ol><p>${data.author}. <a href="${data.license_url}" target="_blank" rel="noopener">Creative Commons ${data.license}</a></p></details>
      </div>`;
    document.body.append(panel);

    panel.addEventListener('click', e => {
      const b = e.target.closest('button');
      if (!b) return;
      if (b.dataset.s) tune(b.dataset.s);
      else if (b.dataset.a) ambient(b.dataset.a, st.amb[b.dataset.a] > 0 ? 0 : 0.6);
      else if (b.dataset.do === 'play') station() ? (st.on ? pause() : play()) : tune(data.stations[0].id);
      else if (b.dataset.do === 'prev') step(-1);
      else if (b.dataset.do === 'next') step(1);
      else if (b.classList.contains('rdo-x')) close();
      render();
    });
    $('.rdo-vol input').addEventListener('input', e => { audio.volume = st.vol = +e.target.value; save(); });
    panel.querySelectorAll('.rdo-amb input').forEach(r => r.addEventListener('input', () => { ambient(r.dataset.a, +r.value); render(); }));
    const seek = $('.rdo-seek');
    seek.addEventListener('input', () => { seeking = true; $('.rdo-cur').textContent = fmt(seek.value); });
    seek.addEventListener('change', () => { seeking = false; if (audio.src) audio.currentTime = +seek.value; });
    panel.addEventListener('keydown', e => { if (e.key === 'Escape') { close(); btn.focus(); } });
  }
  let seeking = false;
  function progress() {
    if (!panel || panel.hidden || seeking) return;
    const t = track(), dur = audio.duration || (t && t.d) || 0, seek = $('.rdo-seek');
    seek.max = Math.max(1, Math.floor(dur)); seek.value = Math.floor(audio.currentTime || st.t);
    seek.style.setProperty('--p', (seek.value / seek.max * 100) + '%');
    $('.rdo-cur').textContent = fmt(audio.currentTime || st.t); $('.rdo-dur').textContent = fmt(dur);
  }
  function render() {
    btn.classList.toggle('on', st.on);
    btn.setAttribute('aria-pressed', String(st.on));
    if (!panel) return;
    const s = station(), t = track(), hero = s || data.stations[0];
    const img = $('.rdo-art');
    if (img.getAttribute('src') !== art(hero)) { img.src = art(hero); img.style.objectPosition = hero.pos || '50% 50%'; }
    $('.rdo-st').textContent = s ? s.name[LANG] + ' · ' + s.mood[LANG] : L.title;
    $('.rdo-tt').textContent = failed ? L.err : t ? t.t : L.pick;
    const pb = $('.rdo-play');
    pb.innerHTML = svg(st.on ? 'pause' : 'play'); pb.setAttribute('aria-label', st.on ? L.pause : L.play);
    panel.querySelectorAll('.rdo-tile').forEach(b => {
      b.setAttribute('aria-pressed', String(b.dataset.s === st.s));
      b.classList.toggle('playing', b.dataset.s === st.s && st.on);
    });
    panel.querySelectorAll('.rdo-amb-t').forEach(b => b.setAttribute('aria-pressed', String(st.amb[b.dataset.a] > 0)));
    panel.querySelectorAll('.rdo-amb input').forEach(r => { r.value = st.amb[r.dataset.a]; r.style.setProperty('--p', st.amb[r.dataset.a] * 100 + '%'); });
    const v = $('.rdo-vol input');
    v.value = st.vol; v.style.setProperty('--p', st.vol * 100 + '%');
    progress();
  }
  function open() {
    getData().then(() => {
      if (!panel) build();
      panel.hidden = false;
      btn.setAttribute('aria-expanded', 'true');
      render();
      (panel.querySelector('.rdo-tile[aria-pressed="true"]') || panel.querySelector('.rdo-tile')).focus({ preventScroll: true });
    });
  }
  function close() { if (panel) panel.hidden = true; btn.setAttribute('aria-expanded', 'false'); }
  btn.addEventListener('click', () => (panel && !panel.hidden ? close() : open()));
  document.addEventListener('pointerdown', e => { if (panel && !panel.hidden && !panel.contains(e.target) && !btn.contains(e.target)) close(); });

  // ---------- go on after a page change ----------
  const fresh = Date.now() - st.ts < RESUME_MS;
  if (!fresh) { st.on = false; st.amb = { fire: 0, rain: 0, wind: 0 }; }
  const wantMusic = st.on && st.s, wantAmb = Object.keys(st.amb).filter(n => st.amb[n] > 0);
  render();
  if (wantMusic || wantAmb.length) {
    getData().then(() => {
      if (!station()) st.s = null;
      wantAmb.forEach(n => ambient(n, st.amb[n]));
      const music = wantMusic && station();
      (music ? (load(st.t), play()) : Promise.resolve()).then(() => {
        const musicBlocked = music && audio.paused, ambBlocked = ctx && ctx.state !== 'running';
        if (!musicBlocked && !ambBlocked) return;
        if (musicBlocked) { st.on = true; render(); }   // blocked: show as playing and wait for the first gesture
        const resume = () => {
          removeEventListener('pointerdown', resume, true); removeEventListener('keydown', resume, true);
          if (ctx) ctx.resume();
          if (music && audio.paused) play();
        };
        addEventListener('pointerdown', resume, true); addEventListener('keydown', resume, true);
      });
    });
  }
})();
