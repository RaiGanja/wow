/* Site search of the guide: the header button .srchbtn (put in by build.py pwa()), Ctrl+K / ⌘K or "/" open a dialog over the page.
   The index assets/search/<lang>.json (made by search.py from the built pages) loads on the first open: entries (pages, sections
   with anchors, FAQ questions, dungeons), aliases (other names -> the name on these pages), questions (phrase -> answer), the
   popular links and the stop words. Every word of the query but the stop words must match, as itself, its stem, an alias or,
   when no title has a word starting with it, the nearest title word (one typo up to 6 letters, two from 7): the start of a word
   in the title scores most, then the keys (where the entry is, page title and description, other names of a dungeon), inside a
   word, the text. Text matches show a short excerpt. A query that asks a known question puts its answer first. A level number
   (24, "dungeons 24") lists the dungeons for that level. A query typed in the wrong keyboard layout (vfu -> маг) is retried in
   the other one when nothing matches. An empty query and a query with no answer show the popular links.
   Arrows move the selection, Enter opens it, Esc closes. */
(() => {
  const SCRIPT = document.currentScript, ROOT = SCRIPT.dataset.root || './';
  const V = (SCRIPT.src.match(/[?&]v=(\w+)/) || [])[1] || '';
  const btn = document.querySelector('.srchbtn');
  if (!btn) return;
  const LANG = (l => ['ru', 'en', 'uk', 'de', 'fr', 'es', 'pt', 'it', 'pl'].includes(l) ? l : 'en')(document.documentElement.lang.split('-')[0]);
  const L = {
    ru: { title: 'Поиск по сайту', ph: 'Класс, раса, подземелье, вопрос…', none: 'Ничего не нашлось.', pop: 'Популярное', go: 'Разделы', nav: 'выбрать', open: 'открыть', close: 'закрыть', err: 'Поиск не загрузился. Проверьте сеть и откройте ещё раз.', off: 'Нет сети. Поиск загрузится, когда она вернётся.', load: 'Загрузка…', found: n => `Найдено: ${n}` },
    en: { title: 'Search the site', ph: 'Class, race, dungeon, question…', none: 'Nothing found.', pop: 'Popular', go: 'Sections', nav: 'select', open: 'open', close: 'close', err: 'Search did not load. Check your connection and open it again.', off: 'No connection. Search will load when it is back.', load: 'Loading…', found: n => `Found: ${n}` },
    uk: { title: 'Пошук по сайту', ph: 'Клас, раса, підземелля, питання…', none: 'Нічого не знайшлося.', pop: 'Популярне', go: 'Розділи', nav: 'вибрати', open: 'відкрити', close: 'закрити', err: 'Пошук не завантажився. Перевірте мережу й відкрийте ще раз.', off: 'Немає мережі. Пошук завантажиться, коли вона повернеться.', load: 'Завантаження…', found: n => `Знайдено: ${n}` },
    de: { title: 'Seite durchsuchen', ph: 'Klasse, Volk, Dungeon, Frage…', none: 'Nichts gefunden.', pop: 'Beliebt', go: 'Bereiche', nav: 'wählen', open: 'öffnen', close: 'schließen', err: 'Die Suche wurde nicht geladen. Prüf die Verbindung und öffne sie erneut.', off: 'Keine Verbindung. Die Suche lädt, sobald sie zurück ist.', load: 'Wird geladen…', found: n => `Gefunden: ${n}` },
    fr: { title: 'Rechercher sur le site', ph: 'Classe, race, donjon, question…', none: 'Aucun résultat.', pop: 'Populaire', go: 'Rubriques', nav: 'choisir', open: 'ouvrir', close: 'fermer', err: 'La recherche ne s’est pas chargée. Vérifiez la connexion et rouvrez-la.', off: 'Pas de connexion. La recherche se chargera à son retour.', load: 'Chargement…', found: n => `Résultats : ${n}` },
    es: { title: 'Buscar en el sitio', ph: 'Clase, raza, mazmorra, pregunta…', none: 'Sin resultados.', pop: 'Populares', go: 'Secciones', nav: 'elegir', open: 'abrir', close: 'cerrar', err: 'La búsqueda no se cargó. Revisa la conexión y vuelve a abrirla.', off: 'Sin conexión. La búsqueda se cargará cuando vuelva.', load: 'Cargando…', found: n => `Resultados: ${n}` },
    pt: { title: 'Pesquisar no site', ph: 'Classe, raça, masmorra, pergunta…', none: 'Nada encontrado.', pop: 'Populares', go: 'Seções', nav: 'escolher', open: 'abrir', close: 'fechar', err: 'A pesquisa não carregou. Verifique a conexão e abra de novo.', off: 'Sem conexão. A pesquisa vai carregar quando ela voltar.', load: 'Carregando…', found: n => `Resultados: ${n}` },
    it: { title: 'Cerca nel sito', ph: 'Classe, razza, dungeon, domanda…', none: 'Nessun risultato.', pop: 'Popolari', go: 'Sezioni', nav: 'scegli', open: 'apri', close: 'chiudi', err: 'La ricerca non si è caricata. Controlla la connessione e riaprila.', off: 'Nessuna connessione. La ricerca si caricherà quando torna.', load: 'Caricamento…', found: n => `Risultati: ${n}` },
    pl: { title: 'Szukaj w serwisie', ph: 'Klasa, rasa, dungeon, pytanie…', none: 'Nic nie znaleziono.', pop: 'Popularne', go: 'Działy', nav: 'wybierz', open: 'otwórz', close: 'zamknij', err: 'Wyszukiwarka się nie wczytała. Sprawdź połączenie i otwórz ją ponownie.', off: 'Brak połączenia. Wyszukiwarka wczyta się, gdy wróci.', load: 'Wczytywanie…', found: n => `Znaleziono: ${n}` },
  }[LANG];
  const MAC = /Mac|iPhone|iPad/.test(navigator.platform || navigator.userAgent);
  const KEY = MAC ? '⌘K' : 'Ctrl K';
  btn.title = `${btn.getAttribute('aria-label')} (${KEY})`;
  btn.setAttribute('aria-keyshortcuts', MAC ? 'Meta+K' : 'Control+K');
  const kb = btn.querySelector('kbd');
  if (kb) kb.textContent = KEY;

  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);
  // lower case without accents, ё -> е; one output character per input character, so positions match the original text
  const norm = s => {
    let o = '';
    for (const ch of s) {
      const c = ch.toLowerCase().normalize('NFD')[0];
      o += (c === 'ё' ? 'е' : c === 'ї' ? 'і' : c) + (ch.length > 1 ? ' ' : '');
    }
    return o;
  };
  const SPLIT = /[\s\-–—.,:;!?()«»"“”„'’/·]+/;
  const EN = '`qwertyuiop[]asdfghjkl;\'zxcvbnm,.', RU = 'ёйцукенгшщзхъфывапролджэячсмитьбю', UK = 'ʼйцукенгшщзхїфівапролджєячсмитьбю';
  const swap = (s, from, to) => [...s].map(c => { const i = from.indexOf(c); return i < 0 ? c : to[i]; }).join('');

  const words = s => s.split(SPLIT).filter(Boolean);
  // endings cut off for the stem ("мага" -> "маг", "choosing" -> "choos"); the stem keeps at least 3 letters
  const END = {
    ru: 'ями ами ого его ому ему ыми ими ой ей ий ый ая яя ое ее ые ие ую юю ов ев ам ям ах ях ом ем а я о е ы и у ю ь',
    uk: 'ями ами ого ому ими ою ею ій ий ая яя ее ие ів ам ям ах ях ом ем а я о е и і у ю ь',
    en: 'ing ers ies es ed er s e', de: 'en er es e n s', fr: 'es s e', es: 'es os as s a o e', pt: 'es os as s a o e',
    it: 'i e a o', pl: 'ami ach ow om ego emu ej a e y i u o',
  }[LANG].split(' ');

  let items = null, alias = {}, asks = [], popular = [], stop = new Set(), vocab = [], loading = null;
  let dlg, input, list, foot, live, sel = -1, shown = [], opener = null;

  function load() {
    if (loading) return loading;
    const ctl = typeof AbortController === 'function' ? new AbortController() : null;
    const slow = setTimeout(() => ctl && ctl.abort(), 8000);   // a stalled request (no network behind the service worker) ends in a message
    loading = fetch(`${ROOT}assets/search/${LANG}.json${V ? '?v=' + V : ''}`, ctl ? { signal: ctl.signal } : {})
      .then(r => { if (!r.ok) throw r; return r.json(); })
      .then(d => {
        clearTimeout(slow);
        items = d.i.map(([t, s, u, k, keys, x]) => ({ t, s, u, k, x, nt: norm(t), nk: norm(s + ' ' + keys), nx: norm(x) }));
        for (const it of items) it.ntw = words(it.nt).join(' ');
        for (const [a, v] of Object.entries(d.a)) alias[norm(a)] = v.split('|').map(words);
        asks = d.q.map(([u, ph]) => [items.find(it => it.u === u), ph.split('|').map(p => words(norm(p)))]);
        popular = d.p.map(([t, u]) => { const it = items.find(x => x.u === u); return { ...it, t, nt: norm(t), x: '', s: it.k ? it.s : '' }; });
        stop = new Set(words(norm(d.s)));
        const w = new Set(Object.keys(alias).flatMap(words));
        for (const it of items) for (const x of words(it.nt + ' ' + it.nk)) if (x.length > 2) w.add(x);
        vocab = [...w].sort();
        render();
      })
      .catch(() => { clearTimeout(slow); loading = null; if (dlg && dlg.open) msg(navigator.onLine === false || (ctl && ctl.signal.aborted) ? L.off : L.err); });
    return loading;
  }
  addEventListener('online', () => { if (!items && dlg && dlg.open) load(); });

  function build() {
    dlg = document.createElement('dialog');
    dlg.className = 'srch';
    dlg.setAttribute('aria-label', L.title);
    dlg.innerHTML = `<div class="srch-in"><div class="srch-f"><svg class="ico" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/></svg>
<input type="search" role="combobox" aria-expanded="true" aria-controls="srchList" aria-autocomplete="list" autocomplete="off" spellcheck="false" enterkeyhint="go" placeholder="${esc(L.ph)}" aria-label="${esc(L.title)}">
<button type="button" class="srch-x" aria-label="${esc(L.close)}"><kbd>Esc</kbd><svg class="ico" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 6l12 12M18 6 6 18"/></svg></button></div>
<ul class="srch-l" id="srchList" role="listbox" aria-label="${esc(L.title)}"></ul>
<p class="srch-h" aria-hidden="true"><span><kbd>↑</kbd><kbd>↓</kbd> ${esc(L.nav)}</span><span><kbd>Enter</kbd> ${esc(L.open)}</span><span><kbd>Esc</kbd> ${esc(L.close)}</span></p>
<p class="sr" aria-live="polite"></p></div>`;
    document.body.append(dlg);
    input = dlg.querySelector('input'); list = dlg.querySelector('.srch-l'); foot = dlg.querySelector('.srch-h'); live = dlg.querySelector('.sr');
    input.addEventListener('input', () => render());
    input.addEventListener('keydown', key);
    dlg.querySelector('.srch-x').onclick = close;
    dlg.addEventListener('click', e => { if (e.target === dlg) close(); });   // click on the backdrop
    dlg.addEventListener('close', () => { document.documentElement.classList.remove('srch-on'); if (opener) opener.focus({ preventScroll: true }); });
    list.addEventListener('click', e => { if (e.target.closest('a')) dlg.close(); });
    list.addEventListener('mousemove', e => { const li = e.target.closest('li[role="option"]'); if (li) pick(+li.dataset.i, false); });
  }

  function open() {
    if (!dlg) build();
    if (dlg.open) { input.select(); return; }
    opener = document.activeElement;
    load();
    render();
    dlg.showModal();
    document.documentElement.classList.add('srch-on');
    input.select();
  }
  function close() { if (dlg && dlg.open) dlg.close(); }

  // where a token is in a string: 2 at the start of a word, 1 inside a word, 0 nowhere
  function at(s, t) {
    let i = s.indexOf(t);
    if (i < 0) return 0;
    for (; i >= 0; i = s.indexOf(t, i + 1)) if (i === 0 || SPLIT.test(s[i - 1])) return 2;
    return 1;
  }

  // one token against an entry: [score, matched the name or the keys]
  function hit(it, t) {
    const a = at(it.nt, t);
    if (a === 2) return [10, true];
    const b = at(it.nk, t);
    if (b === 2) return [5, true];
    if (a && t.length > 3) return [3, true];   // inside a word: "мак" is not "Шамана"
    if (b && t.length > 3) return [2, true];
    const c = at(it.nx, t);
    return c === 2 || (c && t.length > 4) ? [1, false] : [0, false];
  }

  const stem = t => { if (t.length > 3) for (const e of END) if (t.endsWith(e) && t.length - e.length >= 3) return t.slice(0, -e.length); return t; };

  // a title word starts with the token (binary search in the sorted vocabulary)
  function known(t) {
    let a = 0, b = vocab.length;
    while (a < b) { const m = (a + b) >> 1; if (vocab[m] < t) a = m + 1; else b = m; }
    return a < vocab.length && vocab[a].startsWith(t);
  }

  // edit distance (with swapped neighbours) from a to the nearest start of b; more than k -> k + 1
  function dist(a, b, k) {
    const n = a.length, m = Math.min(b.length, n + k);
    if (m < n - k) return k + 1;
    let p2 = null, p = Array.from({ length: m + 1 }, (_, j) => j);
    for (let i = 1; i <= n; i++) {
      const c = [i];
      let low = i;
      for (let j = 1; j <= m; j++) {
        let v = Math.min(p[j] + 1, c[j - 1] + 1, p[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
        if (i > 1 && j > 1 && a[i - 1] === b[j - 2] && a[i - 2] === b[j - 1]) v = Math.min(v, p2[j - 2] + 1);
        c.push(v);
        if (v < low) low = v;
      }
      if (low > k) return k + 1;
      p2 = p; p = c;
    }
    return Math.min(...p.slice(Math.max(0, n - k)));
  }

  // a typo: the title words nearest to the token, only when no title word starts with it
  function fuzzy(t) {
    if (t.length < 4 || /\d/.test(t) || known(t)) return [];
    const k = t.length >= 7 ? 2 : 1;
    let best = k + 1, out = [];
    for (const w of vocab) {
      if (Math.abs(w.length - t.length) > k && w.length < t.length) continue;
      const d = dist(t, w, Math.min(k, best));
      if (d < best) { best = d; out = [w]; } else if (d === best && d <= k && out.length < 6) out.push(w);
    }
    return best <= k ? out : [];
  }

  // the query as terms; a term is met by any of its variants, a variant is a list of tokens that all have to match
  function terms(q) {
    const raw = words(norm(q)), out = [];
    for (let i = 0; i < raw.length;) {
      let n = Math.min(3, raw.length - i);
      while (n > 1 && !alias[raw.slice(i, i + n).join(' ')]) n--;
      const t = raw.slice(i, i + n), key = t.join(' '), alts = [{ toks: t, w: 1 }];
      i += n;
      const more = (k, w) => { for (const x of alias[k] || []) alts.push({ toks: x, w }); };
      more(key, 0.9);
      if (n === 1) {
        const s = stem(key);
        if (s !== key) alts.push({ toks: [s], w: 0.8 });
        if (!alias[key]) for (const f of fuzzy(key)) { alts.push({ toks: [f], w: 0.7 }); more(f, 0.65); }
      }
      out.push({ alts, stop: n === 1 && stop.has(key) });
    }
    const keep = out.filter(x => !x.stop);
    return keep.length ? keep : out;
  }

  function score(it, T, whole) {
    let s = 0, miss = 0, named = false;
    for (const term of T) {
      let best = 0, nm = false;
      for (const a of term.alts) {
        let sum = 0, n = false;
        for (const t of a.toks) { const [v, x] = hit(it, t); if (!v) { sum = 0; break; } sum += v; n = n || x; }
        let v = sum / a.toks.length * a.w;
        if (v && T.length === 1 && a.toks.join(' ') === it.ntw) v += 20 * a.w;   // the name itself: "warrior" -> «Воин», not «Прокачка Воина»
        if (v > best) { best = v; nm = n; }
      }
      if (best) { s += best; named = named || nm; } else miss++;
    }
    if (it.nt === whole) s += 30;
    else if (it.nt.startsWith(whole)) s += 12;
    return [s + (named ? [3, 1, 2, 2][it.k] : 0), miss, named];   // pages go first only when their name matches, not just their text
  }

  function level(lv) {   // the dungeons for a level
    return items.filter(it => {
      const m = it.k === 3 && it.s.match(/ (\d+)(?:–(\d+))? · /);
      return m && +m[1] <= lv && lv <= +(m[2] || m[1]);
    });
  }

  // a known question: its answers, the phrase with the most words first
  function asked(q) {
    const raw = words(norm(q)), last = raw[raw.length - 1];
    const has = p => raw.some(t => t.startsWith(p) || (t === last && t.length > 2 && p.startsWith(t)));
    return asks.map(([it, phs]) => [it, Math.max(0, ...phs.filter(ph => ph.every(has)).map(ph => ph.length))])
      .filter(r => r[1]).sort((a, b) => b[1] - a[1]).slice(0, 2).map(r => r[0]);
  }

  function search(q) {
    const whole = norm(q).trim(), raw = words(whole);
    if (!raw.length || !/[\p{L}\p{N}]/u.test(whole)) return [];
    if (/^\d{1,2}$/.test(whole)) return level(+whole);
    const T = terms(q), lv = raw.find(t => /^\d{1,2}$/.test(t)), top = asked(q);
    let rows = items.map(it => [it, ...score(it, T, whole)]);
    let hits = rows.filter(r => r[1] && !r[2]);
    if (!hits.length && T.length > 1) hits = rows.filter(r => r[2] === 1 && r[3]).map(r => [r[0], r[1] - 5]);   // all words but one
    hits = hits.sort((a, b) => b[1] - a[1] || a[0].t.length - b[0].t.length).map(r => r[0]);
    if (lv && +lv <= 60) {   // "подземелья 20": the dungeons of the level right after the list itself
      const words2 = T.filter(t => !t.alts.some(a => a.toks.includes(lv)));
      const dg = items.find(it => it.k === 0 && it.u.endsWith('guides/dungeons/'));
      if (words2.length && dg && !score(dg, words2, '')[1]) top.push(dg, ...level(+lv));
    }
    return [...new Set([...top, ...hits])].slice(0, 40);
  }

  // the search as the dialog runs it: when nothing matches, the query is retried in the other keyboard layout (vfu -> маг, ьфп -> mag)
  function find(q) {
    let shown = search(q), used = q;
    if (!shown.length && /\p{L}/u.test(q)) {
      const lo = q.toLowerCase();
      used = /[а-яёієїʼ]/.test(lo) ? swap(lo, /[ієї]/.test(lo) ? UK : RU, EN) : ['ru', 'uk'].includes(LANG) ? swap(lo, EN, LANG === 'uk' ? UK : RU) : q;
      if (used !== q) shown = search(used);
    }
    return Object.assign(shown, { used });
  }

  function mark(text, ntext, toks) {
    const hits = [];
    const W = /[\p{L}\p{N}]/u;   // the mark covers the whole word ("магия" for "маг"), not a cut piece of it
    for (const t of toks) for (let i = ntext.indexOf(t); i >= 0; i = ntext.indexOf(t, i + t.length)) {
      let a = i, b = i + t.length;
      while (a > 0 && W.test(ntext[a - 1])) a--;
      while (b < ntext.length && W.test(ntext[b])) b++;
      hits.push([a, b]);
    }
    hits.sort((a, b) => a[0] - b[0]);
    let o = '', p = 0;
    for (const [a, b] of hits) { if (a < p) continue; o += esc(text.slice(p, a)) + '<mark>' + esc(text.slice(a, b)) + '</mark>'; p = b; }
    return o + esc(text.slice(p));
  }

  // The text holds one line per block (paragraph, list item, card). The excerpt is the line of sentence length with the most
  // query words, cut to ~150 characters around the first of them; short lines (card labels, chips) are matched but never shown.
  function excerpt(it, toks) {
    if (!toks || !it.x || toks.every(t => it.nt.includes(t))) return '';
    let best = null;
    for (let a = 0, b; a < it.x.length; a = b + 1) {
      b = it.x.indexOf('\n', a);
      if (b < 0) b = it.x.length;
      const line = it.nx.slice(a, b), n = toks.filter(t => line.includes(t)).length;
      if (n && b - a >= 40 && (!best || n > best[2])) best = [a, b, n];
    }
    if (!best) return '';
    const [s, e] = best, at = Math.min(...toks.map(t => it.nx.indexOf(t, s)).filter(i => i >= 0 && i < e));
    let a = Math.max(s, at - 40), b = Math.min(e, at + 110);
    if (a > s) a = it.x.indexOf(' ', a) + 1 || a;
    if (b < e) b = it.x.lastIndexOf(' ', b) > at ? it.x.lastIndexOf(' ', b) : b;
    return (a > s ? '…' : '') + mark(it.x.slice(a, b), it.nx.slice(a, b), toks) + (b < e ? '…' : '');
  }

  const ICON = ['<path d="M4 5h16v14H4zM4 9h16"/>', '<path d="M5 7h14M5 12h14M5 17h9"/>', '<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.6.3-1 .8-1 1.5V14M12 17.5h.01"/>',
    '<path d="M4 20V10l8-6 8 6v10M9 20v-5h6v5"/>'];

  function row(it, i, toks) {
    const ex = excerpt(it, toks);
    return `<li role="option" id="sr-${i}" data-i="${i}" aria-selected="false"><a href="${esc(ROOT + it.u)}" tabindex="-1">`
      + `<svg class="ico" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">${ICON[it.k]}</svg>`
      + `<span class="srch-t"><b>${toks ? mark(it.t, it.nt, toks) : esc(it.t)}</b>${it.s ? `<small>${esc(it.s)}</small>` : ''}${ex ? `<span class="srch-x2">${ex}</span>` : ''}</span></a></li>`;
  }

  function msg(text) { list.innerHTML = `<li class="srch-m">${esc(text)}</li>`; shown = []; sel = -1; input.removeAttribute('aria-activedescendant'); live.textContent = text; }

  const group = (label, from, rows, toks) => `<li class="srch-g" role="presentation">${esc(label)}</li>` + rows.map((it, i) => row(it, from + i, toks)).join('');

  function render() {
    if (!dlg) return;
    const q = input.value;
    if (!items) { msg(L.load); return; }
    if (!q.trim()) {
      const go = items.filter(it => {
        const rel = (LANG === 'ru' ? it.u : it.u.slice(LANG.length + 1)).split('/').filter(Boolean);
        return it.k === 0 && (rel.length === 1 && rel[0] !== 'privacy' || rel.length === 2 && rel[0] === 'guides');
      });
      shown = [...popular, ...go];
      list.innerHTML = group(L.pop, 0, popular, null) + group(L.go, popular.length, go, null);
      live.textContent = '';
      pick(0, false);
      return;
    }
    shown = find(q);
    if (!shown.length) {   // nothing: the popular questions instead of a dead end
      shown = popular;
      list.innerHTML = `<li class="srch-m">${esc(L.none)}</li>` + group(L.pop, 0, popular, null);
      live.textContent = L.none;
      pick(-1, false);
      return;
    }
    const toks = [...new Set(terms(shown.used).flatMap(t => t.alts.flatMap(a => a.toks)))];
    list.innerHTML = shown.map((it, i) => row(it, i, toks)).join('');
    live.textContent = L.found(shown.length);
    pick(0, false);
  }

  function pick(i, scroll = true) {
    if (sel >= 0) { const o = list.querySelector(`#sr-${sel}`); if (o) o.setAttribute('aria-selected', 'false'); }
    sel = i;
    const li = i >= 0 && list.querySelector(`#sr-${i}`);
    if (!li) { input.removeAttribute('aria-activedescendant'); return; }
    li.setAttribute('aria-selected', 'true');
    input.setAttribute('aria-activedescendant', li.id);
    if (scroll) li.scrollIntoView({ block: 'nearest' });
  }

  function key(e) {
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
      e.preventDefault();
      if (shown.length) pick((sel + (e.key === 'ArrowDown' ? 1 : -1) + shown.length) % shown.length);
    } else if (e.key === 'Enter' && sel >= 0) {
      e.preventDefault();
      const a = list.querySelector(`#sr-${sel} a`);
      if (e.ctrlKey || e.metaKey) { window.open(a.href, '_blank', 'noopener'); return; }
      dlg.close();
      a.click();
    }
  }

  globalThis.gabellaFind = q => load().then(() => (items ? find(q) : []));   // the same search for the FAQ filter (build_guides.py)
  btn.addEventListener('click', open);
  btn.addEventListener('pointerenter', () => { if (!items) load(); }, { once: true });
  addEventListener('keydown', e => {
    if ((e.ctrlKey || e.metaKey) && !e.altKey && !e.shiftKey && (e.code === 'KeyK' || e.key.toLowerCase() === 'k')) {
      e.preventDefault();
      open();
    } else if (e.key === '/' && !e.ctrlKey && !e.metaKey && !e.altKey && !(dlg && dlg.open)) {
      const el = document.activeElement;
      if (el && (el.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(el.tagName))) return;
      e.preventDefault();
      open();
    }
  });
})();
