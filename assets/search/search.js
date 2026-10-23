/* Site search of the guide: the header button .srchbtn (put in by build.py pwa()), Ctrl+K / ⌘K or "/" open a dialog over the page.
   The index assets/search/<lang>.json (made by search.py from the built pages) loads on the first open: pages, sections with
   anchors, FAQ questions, dungeons. Every word of the query must match: the start of a word in the title scores most, then
   anywhere in the title, the keys (where the entry is, page title and description, other names of a dungeon), the text. Text matches show
   a short excerpt. A level number (24) lists the dungeons for that level. A query typed in the wrong keyboard layout (vfu -> маг) is retried in the other one when nothing matches.
   Arrows move the selection, Enter opens it, Esc closes. */
(() => {
  const SCRIPT = document.currentScript, ROOT = SCRIPT.dataset.root || './';
  const V = (SCRIPT.src.match(/[?&]v=(\w+)/) || [])[1] || '';
  const btn = document.querySelector('.srchbtn');
  if (!btn) return;
  const LANG = (l => ['ru', 'en', 'uk', 'de', 'fr', 'es', 'pt', 'it', 'pl'].includes(l) ? l : 'en')(document.documentElement.lang.split('-')[0]);
  const L = {
    ru: { title: 'Поиск по сайту', ph: 'Класс, раса, подземелье, вопрос…', none: 'Ничего не нашлось. Попробуйте другое слово или английское название.', go: 'Разделы', nav: 'выбрать', open: 'открыть', close: 'закрыть', err: 'Поиск не загрузился. Проверьте сеть и откройте ещё раз.', load: 'Загрузка…', found: n => `Найдено: ${n}` },
    en: { title: 'Search the site', ph: 'Class, race, dungeon, question…', none: 'Nothing found. Try another word.', go: 'Sections', nav: 'select', open: 'open', close: 'close', err: 'Search did not load. Check your connection and open it again.', load: 'Loading…', found: n => `Found: ${n}` },
    uk: { title: 'Пошук по сайту', ph: 'Клас, раса, підземелля, питання…', none: 'Нічого не знайшлося. Спробуйте інше слово або англійську назву.', go: 'Розділи', nav: 'вибрати', open: 'відкрити', close: 'закрити', err: 'Пошук не завантажився. Перевірте мережу й відкрийте ще раз.', load: 'Завантаження…', found: n => `Знайдено: ${n}` },
    de: { title: 'Seite durchsuchen', ph: 'Klasse, Volk, Dungeon, Frage…', none: 'Nichts gefunden. Versuchen Sie ein anderes Wort oder den englischen Namen.', go: 'Bereiche', nav: 'wählen', open: 'öffnen', close: 'schließen', err: 'Die Suche wurde nicht geladen. Prüfen Sie die Verbindung und öffnen Sie sie erneut.', load: 'Wird geladen…', found: n => `Gefunden: ${n}` },
    fr: { title: 'Rechercher sur le site', ph: 'Classe, race, donjon, question…', none: 'Aucun résultat. Essayez un autre mot ou le nom anglais.', go: 'Rubriques', nav: 'choisir', open: 'ouvrir', close: 'fermer', err: 'La recherche ne s’est pas chargée. Vérifiez la connexion et rouvrez-la.', load: 'Chargement…', found: n => `Résultats : ${n}` },
    es: { title: 'Buscar en el sitio', ph: 'Clase, raza, mazmorra, pregunta…', none: 'Sin resultados. Pruebe otra palabra o el nombre en inglés.', go: 'Secciones', nav: 'elegir', open: 'abrir', close: 'cerrar', err: 'La búsqueda no se cargó. Compruebe la conexión y ábrala de nuevo.', load: 'Cargando…', found: n => `Resultados: ${n}` },
    pt: { title: 'Pesquisar no site', ph: 'Classe, raça, masmorra, pergunta…', none: 'Nada encontrado. Tente outra palavra ou o nome em inglês.', go: 'Seções', nav: 'escolher', open: 'abrir', close: 'fechar', err: 'A pesquisa não carregou. Verifique a conexão e abra de novo.', load: 'Carregando…', found: n => `Resultados: ${n}` },
    it: { title: 'Cerca nel sito', ph: 'Classe, razza, dungeon, domanda…', none: 'Nessun risultato. Prova un’altra parola o il nome inglese.', go: 'Sezioni', nav: 'scegli', open: 'apri', close: 'chiudi', err: 'La ricerca non si è caricata. Controlla la connessione e riaprila.', load: 'Caricamento…', found: n => `Risultati: ${n}` },
    pl: { title: 'Szukaj w serwisie', ph: 'Klasa, rasa, loch, pytanie…', none: 'Nic nie znaleziono. Spróbuj innego słowa.', go: 'Działy', nav: 'wybierz', open: 'otwórz', close: 'zamknij', err: 'Wyszukiwarka się nie wczytała. Sprawdź połączenie i otwórz ją ponownie.', load: 'Wczytywanie…', found: n => `Znaleziono: ${n}` },
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

  let items = null, loading = null, dlg, input, list, foot, live, sel = -1, shown = [], opener = null;

  function load() {
    loading = loading || fetch(`${ROOT}assets/search/${LANG}.json${V ? '?v=' + V : ''}`).then(r => { if (!r.ok) throw r; return r.json(); })
      .then(rows => {
        items = rows.map(([t, s, u, k, keys, x]) => ({ t, s, u, k, x, nt: norm(t), nk: norm(s + ' ' + keys), nx: norm(x) }));
        render();
      })
      .catch(() => { loading = null; if (dlg && dlg.open) msg(L.err); });
    return loading;
  }

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

  function score(it, toks, whole) {
    let s = 0, named = false;
    for (const t of toks) {
      const i = it.nt.indexOf(t);
      if (i === 0 || (i > 0 && SPLIT.test(it.nt[i - 1]))) s += 10;
      else if (i > 0) s += 6;
      else if (it.nk.includes(t)) s += 4;
      else if (it.nx.includes(t)) { s += 1; continue; }
      else return 0;
      named = true;
    }
    if (it.nt === whole) s += 30;
    else if (it.nt.startsWith(whole)) s += 12;
    return s + (named ? [3, 1, 2, 2][it.k] : 0);   // pages go first only when their name matches, not just their text
  }

  function search(q) {
    const whole = norm(q).trim(), toks = whole.split(SPLIT).filter(Boolean);
    if (!toks.length) return [];
    if (/^\d{1,2}$/.test(whole)) {   // a level: the dungeons for it
      const lv = +whole, hits = items.filter(it => {
        const m = it.k === 3 && it.s.match(/ (\d+)(?:–(\d+))? · /);
        return m && +m[1] <= lv && lv <= +(m[2] || m[1]);
      });
      if (hits.length) return hits;
    }
    return items.map(it => [score(it, toks, whole), it]).filter(r => r[0]).sort((a, b) => b[0] - a[0]).slice(0, 40).map(r => r[1]);
  }

  function mark(text, ntext, toks) {
    const hits = [];
    for (const t of toks) for (let i = ntext.indexOf(t); i >= 0; i = ntext.indexOf(t, i + t.length)) hits.push([i, i + t.length]);
    hits.sort((a, b) => a[0] - b[0]);
    let o = '', p = 0;
    for (const [a, b] of hits) { if (a < p) continue; o += esc(text.slice(p, a)) + '<mark>' + esc(text.slice(a, b)) + '</mark>'; p = b; }
    return o + esc(text.slice(p));
  }

  function excerpt(it, toks) {
    if (!toks || !it.x || toks.every(t => it.nt.includes(t))) return '';
    const at = Math.min(...toks.map(t => it.nx.indexOf(t)).filter(i => i >= 0));
    let a = Math.max(0, at - 40), b = Math.min(it.x.length, at + 110);
    if (a > 0) a = it.x.indexOf(' ', a) + 1 || a;
    if (b < it.x.length) b = it.x.lastIndexOf(' ', b) > at ? it.x.lastIndexOf(' ', b) : b;
    return (a > 0 ? '…' : '') + mark(it.x.slice(a, b), it.nx.slice(a, b), toks) + (b < it.x.length ? '…' : '');
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

  function render() {
    if (!dlg) return;
    const q = input.value;
    if (!items) { msg(L.load); return; }
    let toks = null;
    if (!q.trim()) {
      shown = items.filter(it => {
        const rel = (LANG === 'ru' ? it.u : it.u.slice(LANG.length + 1)).split('/').filter(Boolean);
        return it.k === 0 && (rel.length === 1 && rel[0] !== 'privacy' || rel.length === 2 && rel[0] === 'guides');
      });
      list.innerHTML = `<li class="srch-g" role="presentation">${esc(L.go)}</li>` + shown.map((it, i) => row(it, i, null)).join('');
      live.textContent = '';
    } else {
      let used = q;
      shown = search(q);
      if (!shown.length) {   // typed in the other keyboard layout: vfu -> маг, ьфп -> mag
        const lo = q.toLowerCase();
        used = /[а-яёієїʼ]/.test(lo) ? swap(lo, /[ієї]/.test(lo) ? UK : RU, EN) : ['ru', 'uk'].includes(LANG) ? swap(lo, EN, LANG === 'uk' ? UK : RU) : q;
        if (used !== q) shown = search(used);
      }
      if (!shown.length) { msg(L.none); return; }
      toks = norm(used).trim().split(SPLIT).filter(Boolean);
      list.innerHTML = shown.map((it, i) => row(it, i, toks)).join('');
      live.textContent = L.found(shown.length);
    }
    pick(shown.length ? 0 : -1, false);
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
