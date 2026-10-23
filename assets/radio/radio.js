/* Radio of the guide: the header button .radiobtn (put in by build.py pwa()) opens a panel with "On air" (stations picked by
   the listener's local hour), 8 stations (tracks from stations.json, made by tools/make_radio.py), a sleep timer and ambient
   sounds synthesised with Web Audio (campfire, rain, wind). Tracks come from a shuffled bag per station, so none repeats until
   all have played; the next track loads ahead and fades in over the last seconds of the current one (two audio elements;
   where the browser does not let a page set the volume, as on iPhone, they just follow each other). State lives in
   localStorage, so the music goes on after moving to another page: it restarts at the saved second if the page changed less
   than a minute ago; when the browser blocks autoplay, the first click or key press on the new page resumes it.
   A page with #radioDock (the in-game page /play/) gets the panel built into it, always open; the header button scrolls to it. */
(() => {
  const SCRIPT = document.currentScript, ROOT = SCRIPT.dataset.root || './';
  const btn = document.querySelector('.radiobtn'), dock = document.getElementById('radioDock');
  if (!btn) return;
  const LANG = (l => ['ru', 'en', 'uk', 'de', 'fr', 'es', 'pt', 'it', 'pl'].includes(l) ? l : 'en')(document.documentElement.lang.split('-')[0]);
  const L = {
    ru: { title: 'Радио Gabella', play: 'Играть', pause: 'Пауза', prev: 'Предыдущий трек', next: 'Следующий трек', close: 'Закрыть',
      vol: 'Громкость музыки', seek: 'Позиция в треке', amb: 'Звуки вокруг', fire: 'Костёр', rain: 'Дождь', wind: 'Ветер',
      ambVol: 'Громкость: ', music: 'Музыка', err: 'Трек не загрузился — проверьте сеть', pick: 'Выберите станцию',
      air: 'Эфир', airNow: 'По времени суток · сейчас ', stations: 'Станции', sleep: 'Таймер сна', off: 'Выкл', min: ' мин',
      left: 'выключится через ', sleepSet: 'Выключить музыку через ', more: 'Таймер сна и звуки вокруг' },
    en: { title: 'Gabella Radio', play: 'Play', pause: 'Pause', prev: 'Previous track', next: 'Next track', close: 'Close',
      vol: 'Music volume', seek: 'Track position', amb: 'Sounds around', fire: 'Campfire', rain: 'Rain', wind: 'Wind',
      ambVol: 'Volume: ', music: 'Music', err: 'The track did not load — check your connection', pick: 'Pick a station',
      air: 'On air', airNow: 'By the time of day · now ', stations: 'Stations', sleep: 'Sleep timer', off: 'Off', min: ' min',
      left: 'stops in ', sleepSet: 'Stop the music in ', more: 'Sleep timer and sounds around' },
    uk: { title: 'Радіо Gabella', play: 'Грати', pause: 'Пауза', prev: 'Попередній трек', next: 'Наступний трек', close: 'Закрити',
      vol: 'Гучність музики', seek: 'Позиція в треку', amb: 'Звуки довкола', fire: 'Багаття', rain: 'Дощ', wind: 'Вітер',
      ambVol: 'Гучність: ', music: 'Музика', err: 'Трек не завантажився — перевірте мережу', pick: 'Оберіть станцію',
      air: 'Ефір', airNow: 'За часом доби · зараз ', stations: 'Станції', sleep: 'Таймер сну', off: 'Вимк', min: ' хв',
      left: 'вимкнеться за ', sleepSet: 'Вимкнути музику за ', more: 'Таймер сну та звуки довкола' },
    de: { title: 'Gabella Radio', play: 'Abspielen', pause: 'Pause', prev: 'Vorheriger Titel', next: 'Nächster Titel', close: 'Schließen',
      vol: 'Musiklautstärke', seek: 'Position im Titel', amb: 'Umgebungsgeräusche', fire: 'Lagerfeuer', rain: 'Regen', wind: 'Wind',
      ambVol: 'Lautstärke: ', music: 'Musik', err: 'Titel nicht geladen – prüfe deine Verbindung', pick: 'Wähle einen Sender',
      air: 'Live', airNow: 'Nach Tageszeit · jetzt ', stations: 'Sender', sleep: 'Sleep-Timer', off: 'Aus', min: ' Min.',
      left: 'endet in ', sleepSet: 'Musik beenden in ', more: 'Sleep-Timer und Umgebungsgeräusche' },
    fr: { title: 'Radio Gabella', play: 'Lecture', pause: 'Pause', prev: 'Piste précédente', next: 'Piste suivante', close: 'Fermer',
      vol: 'Volume de la musique', seek: 'Position dans la piste', amb: 'Ambiance', fire: 'Feu de camp', rain: 'Pluie', wind: 'Vent',
      ambVol: 'Volume : ', music: 'Musique', err: 'La piste ne s’est pas chargée — vérifiez la connexion', pick: 'Choisissez une station',
      air: 'À l’antenne', airNow: 'Selon l’heure · maintenant ', stations: 'Stations', sleep: 'Minuterie', off: 'Non', min: ' min',
      left: 's’arrête dans ', sleepSet: 'Arrêter la musique dans ', more: 'Minuterie et ambiance' },
    es: { title: 'Radio Gabella', play: 'Reproducir', pause: 'Pausa', prev: 'Pista anterior', next: 'Pista siguiente', close: 'Cerrar',
      vol: 'Volumen de la música', seek: 'Posición en la pista', amb: 'Sonidos de ambiente', fire: 'Hoguera', rain: 'Lluvia', wind: 'Viento',
      ambVol: 'Volumen: ', music: 'Música', err: 'La pista no se cargó: revisa la conexión', pick: 'Elige una emisora',
      air: 'En antena', airNow: 'Según la hora · ahora ', stations: 'Emisoras', sleep: 'Temporizador', off: 'No', min: ' min',
      left: 'se apaga en ', sleepSet: 'Apagar la música en ', more: 'Temporizador y sonidos de ambiente' },
    pt: { title: 'Rádio Gabella', play: 'Tocar', pause: 'Pausar', prev: 'Faixa anterior', next: 'Próxima faixa', close: 'Fechar',
      vol: 'Volume da música', seek: 'Posição na faixa', amb: 'Sons ambientes', fire: 'Fogueira', rain: 'Chuva', wind: 'Vento',
      ambVol: 'Volume: ', music: 'Música', err: 'A faixa não carregou — verifique a conexão', pick: 'Escolha uma estação',
      air: 'No ar', airNow: 'Pela hora do dia · agora ', stations: 'Estações', sleep: 'Timer para dormir', off: 'Desl.', min: ' min',
      left: 'desliga em ', sleepSet: 'Desligar a música em ', more: 'Timer para dormir e sons ambientes' },
    it: { title: 'Radio Gabella', play: 'Riproduci', pause: 'Pausa', prev: 'Brano precedente', next: 'Brano successivo', close: 'Chiudi',
      vol: 'Volume della musica', seek: 'Posizione nel brano', amb: 'Suoni d’ambiente', fire: 'Falò', rain: 'Pioggia', wind: 'Vento',
      ambVol: 'Volume: ', music: 'Musica', err: 'Il brano non si è caricato — controlla la connessione', pick: 'Scegli una stazione',
      air: 'In onda', airNow: 'In base all’ora · ora ', stations: 'Stazioni', sleep: 'Timer', off: 'No', min: ' min',
      left: 'si spegne tra ', sleepSet: 'Spegni la musica tra ', more: 'Timer e suoni d’ambiente' },
    pl: { title: 'Radio Gabella', play: 'Odtwórz', pause: 'Pauza', prev: 'Poprzedni utwór', next: 'Następny utwór', close: 'Zamknij',
      vol: 'Głośność muzyki', seek: 'Pozycja w utworze', amb: 'Dźwięki otoczenia', fire: 'Ognisko', rain: 'Deszcz', wind: 'Wiatr',
      ambVol: 'Głośność: ', music: 'Muzyka', err: 'Utwór się nie wczytał — sprawdź połączenie', pick: 'Wybierz stację',
      air: 'Na antenie', airNow: 'Według pory dnia · teraz ', stations: 'Stacje', sleep: 'Wyłącznik czasowy', off: 'Wył.', min: ' min',
      left: 'wyłączy się za ', sleepSet: 'Wyłącz muzykę za ', more: 'Wyłącznik czasowy i dźwięki otoczenia' },
  }[LANG];
  const KEY = 'gabella-radio', RESUME_MS = 60000;
  const FADE = 5, FADE_TUNE = 1.5, PRELOAD = 30, HISTORY = 30, SLEEP = [15, 30, 60, 90], SLEEP_FADE = 30000;
  const ICO = {
    play: '<path d="M8 5.5v13l11-6.5z" fill="currentColor" stroke="none"/>',
    pause: '<path d="M8 5h3v14H8zM13 5h3v14h-3z" fill="currentColor" stroke="none"/>',
    prev: '<path d="M6 5v14M18 6 9 12l9 6z"/>', next: '<path d="M18 5v14M6 6l9 6-9 6z"/>', x: '<path d="M6 6l12 12M18 6 6 18"/>',
    vol: '<path d="M4 9.5h3.5L12 6v12l-4.5-3.5H4z"/><path d="M15.5 9a4 4 0 0 1 0 6M18 6.5a7.5 7.5 0 0 1 0 11"/>',
    fire: '<path d="M12 3c.5 3.5 4.5 5 4.5 10a4.5 4.5 0 0 1-9 0c0-2.5 1.5-3.5 2.2-5.3.8 1.3 1.3 2.3 1.3 3.3 1-1.5 1.5-4.5 1-8z"/><path d="M5 21h14"/>',
    rain: '<path d="M7 15a4 4 0 0 1 .5-8 5.5 5.5 0 0 1 10.5 1.5A3.3 3.3 0 0 1 17.5 15z"/><path d="M8.5 18l-1 2.5M12.5 18l-1 2.5M16.5 18l-1 2.5"/>',
    wind: '<path d="M3 9h11a3 3 0 1 0-3-3M3 15h15a3 3 0 1 1-3 3M3 12h7"/>',
    air: '<circle cx="12" cy="12" r="2"/><path d="M8.5 8.5a5 5 0 0 0 0 7M15.5 8.5a5 5 0 0 1 0 7M5.6 5.6a9 9 0 0 0 0 12.8M18.4 5.6a9 9 0 0 1 0 12.8"/>',
    moon: '<path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/>',
  };
  const svg = (k, cls = 'ico') => `<svg class="${cls}" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${ICO[k]}</svg>`;
  const fmt = s => (s = Math.max(0, Math.floor(s || 0)), Math.floor(s / 60) + ':' + String(s % 60).padStart(2, '0'));
  const clamp = v => Math.min(1, Math.max(0, v));

  // ---------- state ----------
  // mode: 'air' or a station id; cur: file of the track playing; next: file loaded ahead; bags: tracks left per station / part of day
  const st = Object.assign({ mode: null, cur: null, next: null, t: 0, on: false, vol: 0.6, amb: { fire: 0, rain: 0, wind: 0 },
    bags: {}, hist: [], sleep: 0, sleepMin: 0, ts: 0 }, read());
  if ('i' in st) { delete st.s; delete st.i; st.on = false; }   // state of the first radio (4 stations, no bags)
  function read() { try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { return {}; } }
  function save() { st.ts = Date.now(); try { localStorage.setItem(KEY, JSON.stringify(st)); } catch (e) { /* private mode */ } }

  let data = null, byFile = {}, base = '';
  const getData = () => data ? Promise.resolve(data) : fetch(ROOT + 'assets/radio/stations.json').then(r => r.json()).then(d => {
    data = d;
    base = d.media ? d.media.replace(/\/?$/, '/') : ROOT + 'assets/radio/';
    d.stations.forEach(s => s.tracks.forEach(t => { byFile[t.f] = { t, s }; }));
    return d;
  });
  const stationById = id => data.stations.find(s => s.id === id);
  const art = s => ROOT + 'assets/art/' + s.art + '.webp';
  const now = () => byFile[st.cur];

  // ---------- what plays next ----------
  function airPart(d = new Date()) {
    const h = d.getHours();
    return data.air.find(p => p.from < p.to ? h >= p.from && h < p.to : h >= p.from || h < p.to) || data.air[0];
  }
  const poolKey = () => st.mode === 'air' ? 'air:' + airPart().id : st.mode;
  function pool() {
    const ids = st.mode === 'air' ? airPart().stations : [st.mode];
    return ids.map(stationById).filter(Boolean).flatMap(s => s.tracks.map(t => t.f));
  }
  function shuffle(a) {
    for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; }
    return a;
  }
  function nextFile() {
    const files = pool();
    if (st.next && files.includes(st.next) && st.next !== st.cur) { const f = st.next; st.next = null; return f; }
    st.next = null;
    const key = poolKey();
    let bag = (st.bags[key] || []).filter(f => files.includes(f) && f !== st.cur);
    if (!bag.length) {
      bag = shuffle(files.filter(f => f !== st.cur));
      if (!bag.length) bag = files.slice();
    }
    const f = bag.shift();
    st.bags[key] = bag;
    return f;
  }

  // ---------- music: two elements, the next track fades in on the second one ----------
  const A = [0, 1].map(() => {
    const el = new Audio();
    el.preload = 'none'; el.g = 1; el.fid = null;
    el.addEventListener('timeupdate', () => el === cur() ? onTime() : tick());
    el.addEventListener('ended', () => { if (el === cur()) advance(1, 0); });
    el.addEventListener('error', () => { if (el !== cur() || !el.fid) return; failed = true; st.on = false; render(); });
    return el;
  });
  let ci = 0, failed = false, fading = null, sleepK = 1;
  const cur = () => A[ci], alt = () => A[1 - ci];
  const canFade = (() => { const a = new Audio(); a.volume = 0.5; return Math.abs(a.volume - 0.5) < 0.01; })();
  function vol() { A.forEach(el => { el.volume = clamp(st.vol * el.g * sleepK); }); }

  function prime(el, f, at = 0) {
    if (el.fid !== f) {
      el.fid = f; el.src = base + f; el.preload = 'auto';
      if (at) el.addEventListener('loadedmetadata', () => { el.currentTime = Math.min(at, (el.duration || at + 1) - 1); }, { once: true });
    } else if (at) el.currentTime = at;
  }
  function play() {
    if (!st.cur) { if (!st.mode) st.mode = 'air'; st.cur = nextFile(); }
    if (!cur().fid) prime(cur(), st.cur, st.t);
    if (ctx && ctx.state === 'suspended') ctx.resume();
    vol(); meta();
    return cur().play().then(() => { failed = false; st.on = true; save(); render(); }, () => { st.on = false; render(); });
  }
  function pause() { endFade(); cur().pause(); st.on = false; save(); render(); }
  // move to track f; with sec > 0 and music on, the two tracks cross-fade. Without volume control (iPhone) one element
  // just changes its track: a second element started outside a tap may be refused there.
  function switchTo(f, sec) {
    endFade();
    const from = cur(), wasOn = st.on, fade = wasOn && sec > 0 && canFade && !from.paused;
    const to = canFade ? alt() : from;
    prime(to, f);
    if (to.currentTime) to.currentTime = 0;
    if (to !== from) { ci = 1 - ci; if (!fade) from.pause(); }
    st.cur = f; st.t = 0; failed = false;
    to.g = fade ? 0 : 1; vol(); meta();
    if (wasOn) {
      to.play().then(() => { st.on = true; save(); render(); }, () => { st.on = false; render(); });
      if (fade) fading = { from, to, t0: performance.now(), ms: sec * 1000 };
    }
    save(); render();
  }
  function tick() {   // fade step: from timers, and from timeupdate, which also runs in background tabs
    if (!fading) return;
    const k = clamp((performance.now() - fading.t0) / fading.ms);
    fading.to.g = Math.sin(k * Math.PI / 2); fading.from.g = Math.cos(k * Math.PI / 2);
    vol();
    if (k >= 1) endFade();
  }
  function endFade() {
    if (!fading) return;
    const { from, to } = fading;
    fading = null;
    from.pause(); from.g = 0; to.g = 1; vol();
  }
  setInterval(() => { tick(); sleepTick(); }, 250);

  function advance(d, sec) {
    if (d < 0) {
      const f = st.hist.pop();
      if (cur().currentTime > 5 || !f) { cur().currentTime = 0; return; }
      return switchTo(f, 0);
    }
    if (st.cur) st.hist = st.hist.concat(st.cur).slice(-HISTORY);
    switchTo(nextFile(), sec);
  }
  function tune(id) {
    if (st.mode === id && st.cur) return st.on ? pause() : play();
    st.mode = id; st.next = null;
    const wasOn = st.on;
    if (st.cur) st.hist = st.hist.concat(st.cur).slice(-HISTORY);
    switchTo(nextFile(), FADE_TUNE);
    if (!wasOn) play();
  }
  let lastSave = 0;
  function onTime() {
    const el = cur();
    st.t = el.currentTime;
    tick();
    if (Date.now() - lastSave > 2000) { lastSave = Date.now(); save(); }
    progress();
    const left = (el.duration || 0) - el.currentTime;
    if (!el.duration || !st.on || fading) return;
    if (canFade && left < PRELOAD && (!st.next || alt().fid !== st.next)) {   // load the next track ahead
      if (!st.next) st.next = nextFile();
      prime(alt(), st.next);
    }
    if (canFade && left <= FADE && el.duration > FADE * 3) advance(1, FADE);
  }
  addEventListener('pagehide', () => { if (cur().fid) st.t = cur().currentTime; save(); });

  function meta() {
    const n = now();
    if (!('mediaSession' in navigator) || !n) return;
    navigator.mediaSession.metadata = new MediaMetadata({ title: n.t.t, artist: n.t.a || n.s.author, album: L.title + ' · ' + n.s.name[LANG],
      artwork: [{ src: new URL(art(n.s), location).href, sizes: '600x600', type: 'image/webp' }] });
    navigator.mediaSession.setActionHandler('play', play);
    navigator.mediaSession.setActionHandler('pause', pause);
    navigator.mediaSession.setActionHandler('previoustrack', () => advance(-1, 0));
    navigator.mediaSession.setActionHandler('nexttrack', () => advance(1, FADE_TUNE));
  }

  // ---------- sleep timer: fades music and sounds out over the last 30 s, then stops them ----------
  function setSleep(min) { st.sleep = min ? Date.now() + min * 60000 : 0; st.sleepMin = min; sleepK = 1; vol(); if (ambOut) ambOut.gain.value = 1; save(); render(); }
  let lastLeft = '';
  function sleepTick() {
    if (!st.sleep) return;
    const left = st.sleep - Date.now();
    if (left <= 0) {
      st.sleep = 0; pause();
      Object.keys(st.amb).forEach(n => { if (st.amb[n] > 0) ambient(n, 0); });
      sleepK = 1; vol(); if (ambOut) ambOut.gain.value = 1;
      return render();
    }
    sleepK = left < SLEEP_FADE ? left / SLEEP_FADE : 1;
    vol();
    if (ambOut) ambOut.gain.value = sleepK;
    const label = Math.ceil(left / 60000) + L.min;
    if (label !== lastLeft) { lastLeft = label; renderSleep(); }
  }

  // ---------- ambient sounds (Web Audio, nothing to download) ----------
  let ctx = null, ambOut = null;
  const layers = {};
  function ac() {
    if (!ctx) {
      const C = window.AudioContext || window.webkitAudioContext;
      if (!C) return null;
      ctx = new C();
      ambOut = ctx.createGain();
      ambOut.connect(ctx.destination);
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
      gain.connect(ambOut);
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
    panel.className = dock ? 'rdo rdo-docked' : 'rdo'; panel.id = 'radioPanel'; panel.hidden = !dock;
    panel.setAttribute('role', dock ? 'region' : 'dialog'); panel.setAttribute('aria-label', L.title);
    const eq = '<span class="rdo-eq" aria-hidden="true"><i></i><i></i><i></i></span>';
    const tiles = data.stations.map(s => `<button class="rdo-tile" type="button" data-s="${s.id}" aria-pressed="false" title="${s.mood[LANG]}">
      <img src="${art(s)}" alt="" loading="lazy" decoding="async" style="object-position:${s.pos || '50% 50%'}"><span class="rdo-tn"><b>${s.name[LANG]}</b><span>${s.mood[LANG]}</span></span>${eq}</button>`).join('');
    const amb = ['fire', 'rain', 'wind'].map(n => `<div class="rdo-amb-row">
      <button class="rdo-amb-t" type="button" data-a="${n}" aria-pressed="false">${svg(n)}<span>${L[n]}</span></button>
      <input class="rdo-range" type="range" min="0" max="1" step="0.05" data-a="${n}" aria-label="${L.ambVol}${L[n]}"></div>`).join('');
    const sleep = [0, ...SLEEP].map(m => `<button class="rdo-chip" type="button" data-sleep="${m}" aria-pressed="false"${m ? ` aria-label="${L.sleepSet}${m}${L.min}"` : ''}>${m || L.off}</button>`).join('');
    const authors = [...new Set(data.stations.flatMap(s => s.tracks.map(t => t.a || s.author)))];
    const credits = data.stations.map(s => `<li><b>${s.name[LANG]}</b>: ${s.tracks.map(t => '«' + t.t + '»' + (t.a ? ' — ' + t.a : '')).join(', ')}</li>`).join('');
    const who = authors.map(a => data.sources[a] ? `${a} (${data.sources[a]})` : a).join(', ');
    panel.innerHTML = `<div class="rdo-hero"><img class="rdo-art" alt="" decoding="async">
      <div class="rdo-now"><span class="rdo-st"></span><b class="rdo-tt"></b></div>
      ${dock ? '' : `<button class="rdo-x" type="button" aria-label="${L.close}">${svg('x')}</button>`}</div>
      <div class="rdo-body">
      <div class="rdo-seekrow"><span class="rdo-cur">0:00</span><input class="rdo-range rdo-seek" type="range" min="0" max="1" step="1" value="0" aria-label="${L.seek}"><span class="rdo-dur">0:00</span></div>
      <div class="rdo-ctl">
        <button class="rdo-b" type="button" data-do="prev" aria-label="${L.prev}">${svg('prev')}</button>
        <button class="rdo-b rdo-play" type="button" data-do="play" aria-label="${L.play}">${svg('play')}</button>
        <button class="rdo-b" type="button" data-do="next" aria-label="${L.next}">${svg('next')}</button>
        <label class="rdo-vol">${svg('vol')}<input class="rdo-range" type="range" min="0" max="1" step="0.05" aria-label="${L.vol}"></label>
      </div>
      <button class="rdo-air" type="button" data-s="air" aria-pressed="false">${svg('air')}<span class="rdo-tn"><b>${L.air}</b><span class="rdo-airnow"></span></span>${eq}</button>
      <p class="rdo-h">${L.stations}</p>
      <div class="rdo-tiles">${tiles}</div>
      ${dock ? `<details class="rdo-more"><summary>${L.more}</summary>` : ''}
      <div class="rdo-sleep"><p class="rdo-h">${svg('moon')}<span>${L.sleep}</span><span class="rdo-left" aria-live="polite"></span></p>
        <div class="rdo-chips" role="group" aria-label="${L.sleep}">${sleep}</div></div>
      <p class="rdo-h">${L.amb}</p>
      <div class="rdo-amb">${amb}</div>${dock ? '</details>' : ''}
      <details class="rdo-cr"><summary>${L.music}: ${who} · ${data.license}</summary>
        <ul>${credits}</ul><p>${who}. <a href="${data.license_url}" target="_blank" rel="noopener">Creative Commons ${data.license}</a></p></details>
      </div>`;
    (dock || document.body).append(panel);

    panel.addEventListener('click', e => {
      const b = e.target.closest('button');
      if (!b) return;
      if (b.dataset.s) tune(b.dataset.s);
      else if (b.dataset.a) ambient(b.dataset.a, st.amb[b.dataset.a] > 0 ? 0 : 0.6);
      else if (b.dataset.sleep) setSleep(+b.dataset.sleep);
      else if (b.dataset.do === 'play') st.cur ? (st.on ? pause() : play()) : tune('air');
      else if (b.dataset.do === 'prev') advance(-1, 0);
      else if (b.dataset.do === 'next') advance(1, FADE_TUNE);
      else if (b.classList.contains('rdo-x')) close();
      render();
    });
    $('.rdo-vol input').addEventListener('input', e => { st.vol = +e.target.value; vol(); save(); });
    panel.querySelectorAll('.rdo-amb input').forEach(r => r.addEventListener('input', () => { ambient(r.dataset.a, +r.value); render(); }));
    const seek = $('.rdo-seek');
    seek.addEventListener('input', () => { seeking = true; $('.rdo-cur').textContent = fmt(seek.value); });
    seek.addEventListener('change', () => { seeking = false; if (cur().fid) { endFade(); cur().currentTime = +seek.value; } });
    if (!dock) panel.addEventListener('keydown', e => { if (e.key === 'Escape') { close(); btn.focus(); } });
  }
  let seeking = false;
  function progress() {
    if (!panel || panel.hidden || seeking) return;
    const n = now(), el = cur(), dur = el.duration || (n && n.t.d) || 0, seek = $('.rdo-seek');
    seek.max = Math.max(1, Math.floor(dur)); seek.value = Math.floor(el.currentTime || st.t);
    seek.style.setProperty('--p', (seek.value / seek.max * 100) + '%');
    $('.rdo-cur').textContent = fmt(el.currentTime || st.t); $('.rdo-dur').textContent = fmt(dur);
  }
  function renderSleep() {
    if (!panel) return;
    const left = st.sleep ? Math.ceil((st.sleep - Date.now()) / 60000) : 0;
    $('.rdo-left').textContent = left > 0 ? ' · ' + L.left + left + L.min : '';
    const pick = st.sleep ? st.sleepMin : 0;
    panel.querySelectorAll('.rdo-chip').forEach(b => b.setAttribute('aria-pressed', String(+b.dataset.sleep === pick)));
  }
  function render() {
    btn.classList.toggle('on', st.on);
    btn.setAttribute('aria-pressed', String(st.on));
    if (!panel) return;
    const n = now(), hero = n ? n.s : data.stations[0], part = airPart();
    const img = $('.rdo-art');
    if (img.getAttribute('src') !== art(hero)) { img.src = art(hero); img.style.objectPosition = hero.pos || '50% 50%'; }
    $('.rdo-st').textContent = !n ? L.title : st.mode === 'air' ? L.air + ' · ' + part.name[LANG] + ' · ' + n.s.name[LANG] : n.s.name[LANG] + ' · ' + n.s.mood[LANG];
    $('.rdo-tt').textContent = failed ? L.err : n ? n.t.t : L.pick;
    $('.rdo-airnow').textContent = L.airNow + part.name[LANG].toLowerCase() + ': ' + part.stations.map(id => stationById(id).name[LANG]).join(', ');
    const pb = $('.rdo-play');
    pb.innerHTML = svg(st.on ? 'pause' : 'play'); pb.setAttribute('aria-label', st.on ? L.pause : L.play);
    panel.querySelectorAll('[data-s]').forEach(b => {
      b.setAttribute('aria-pressed', String(b.dataset.s === st.mode));
      b.classList.toggle('playing', b.dataset.s === st.mode && st.on);
    });
    panel.querySelectorAll('.rdo-amb-t').forEach(b => b.setAttribute('aria-pressed', String(st.amb[b.dataset.a] > 0)));
    panel.querySelectorAll('.rdo-amb input').forEach(r => { r.value = st.amb[r.dataset.a]; r.style.setProperty('--p', st.amb[r.dataset.a] * 100 + '%'); });
    const v = $('.rdo-vol input');
    v.value = st.vol; v.style.setProperty('--p', st.vol * 100 + '%');
    renderSleep();
    progress();
  }
  function open() {
    getData().then(() => {
      if (!panel) build();
      panel.hidden = false;
      btn.setAttribute('aria-expanded', 'true');
      render();
      (panel.querySelector('[data-s][aria-pressed="true"]') || panel.querySelector('.rdo-air')).focus({ preventScroll: true });
    });
  }
  function close() { if (panel) panel.hidden = true; btn.setAttribute('aria-expanded', 'false'); }
  if (dock) {
    btn.setAttribute('aria-expanded', 'true');
    btn.addEventListener('click', () => { dock.scrollIntoView({ behavior: 'smooth', block: 'center' }); if (panel) $('.rdo-play').focus({ preventScroll: true }); });
    getData().then(() => { if (!panel) build(); render(); });
  } else {
    btn.addEventListener('click', () => (panel && !panel.hidden ? close() : open()));
    document.addEventListener('pointerdown', e => { if (panel && !panel.hidden && !panel.contains(e.target) && !btn.contains(e.target)) close(); });
  }

  // ---------- go on after a page change ----------
  const fresh = Date.now() - st.ts < RESUME_MS;
  if (!fresh) { st.on = false; st.amb = { fire: 0, rain: 0, wind: 0 }; st.sleep = 0; }
  const wantMusic = st.on && st.cur, wantAmb = Object.keys(st.amb).filter(n => st.amb[n] > 0);
  render();
  if (wantMusic || wantAmb.length) {
    getData().then(() => {
      if (!byFile[st.cur]) { st.cur = null; st.next = null; }
      if (st.mode !== 'air' && !stationById(st.mode)) st.mode = null;
      wantAmb.forEach(n => ambient(n, st.amb[n]));
      const music = wantMusic && st.cur;
      (music ? play() : Promise.resolve()).then(() => {
        const musicBlocked = music && cur().paused, ambBlocked = ctx && ctx.state !== 'running';
        if (!musicBlocked && !ambBlocked) return;
        if (musicBlocked) { st.on = true; render(); }   // blocked: show as playing and wait for the first gesture
        const resume = () => {
          removeEventListener('pointerdown', resume, true); removeEventListener('keydown', resume, true);
          if (ctx) ctx.resume();
          if (music && cur().paused) play();
        };
        addEventListener('pointerdown', resume, true); addEventListener('keydown', resume, true);
      });
    });
  }
})();
