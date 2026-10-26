"""Talent trees in the spec guides (guides/builds-<class>/): the full class tree with our path in gold, a card under the tree
and the order by level. Decision 26.10 (variant B of docs/wow/audit/2026-10-26-talents).

Data: content/talents/<class>.json, written by tools/talent_import.py from the GabellaTalents addon (rows, columns, arrows and
icons straight from the Forever client through the addon API) and tools/talent_icons.py (icon names from the Blizzard Game Data
API, the pictures from Blizzard's render CDN into one sprite per class, assets/talents/<class>.webp). No file -> no tree: the
page keeps its table. The points come from the spec's talent table in content/spec_builds.py (one source for the numbers).
Rendered at build time: no fetch, no layout shift; the inline script only opens the card, switches tabs and wakes the sprite."""
import json, os, re
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, 'content', 'talents')
FIRST_LEVEL, CAP_LEVEL = 10, 30            # the first talent point, the beta cap the spec guides are written for
ROW_POINTS = 5                             # a row opens every 5 points spent in its tree

# The order of the talent tabs in the client, the same as the spec sections of guides/builds-<class>/
TREES = {'paladin': ['holy', 'protection', 'retribution'], 'warrior': ['arms', 'fury', 'protection'],
         'mage': ['arcane', 'fire', 'frost'], 'hunter': ['beast-mastery', 'marksmanship', 'survival'],
         'rogue': ['assassination', 'combat', 'subtlety'], 'priest': ['discipline', 'holy', 'shadow'],
         'shaman': ['elemental', 'enhancement', 'restoration'], 'warlock': ['affliction', 'demonology', 'destruction'],
         'druid': ['balance', 'feral', 'restoration']}

UI = {
    'hint': {'ru': 'Нажмите на значок: здесь откроется талант.', 'en': 'Tap an icon to see the talent here.',
             'uk': 'Натисніть на значок: тут відкриється талант.', 'de': 'Tippe auf ein Symbol, um das Talent hier zu sehen.',
             'es': 'Toca un icono para ver aquí el talento.', 'fr': 'Touchez une icône pour afficher le talent ici.',
             'it': 'Tocca un’icona per vedere qui il talento.', 'pl': 'Dotknij ikony, aby zobaczyć tu talent.',
             'pt': 'Toque num ícone para ver o talento aqui.'},
    'take': {'ru': 'Берём {p} из {m}', 'en': 'Take {p} of {m}', 'uk': 'Беремо {p} з {m}', 'de': '{p} von {m} nehmen',
             'es': 'Tomar {p} de {m}', 'fr': 'Prendre {p} sur {m}', 'it': 'Prendere {p} su {m}', 'pl': 'Bierzemy {p} z {m}',
             'pt': 'Pegar {p} de {m}'},
    'skip': {'ru': 'Не берём · рангов: {m}', 'en': 'Not taken · ranks: {m}', 'uk': 'Не беремо · рангів: {m}',
             'de': 'Nicht genommen · Ränge: {m}', 'es': 'No se toma · rangos: {m}', 'fr': 'Non pris · rangs : {m}',
             'it': 'Non preso · gradi: {m}', 'pl': 'Nie bierzemy · rangi: {m}', 'pt': 'Não pegar · níveis: {m}'},
    'lv': {'ru': 'ур. {a}', 'en': 'lvl {a}', 'uk': 'рів. {a}', 'de': 'Stufe {a}', 'es': 'nivel {a}', 'fr': 'niv. {a}',
           'it': 'liv. {a}', 'pl': 'poz. {a}', 'pt': 'nív. {a}'},
    'row': {'ru': 'Открыт с {n} очков в ветке', 'en': 'Opens at {n} points in the tree', 'uk': 'Відкривається з {n} очок у гілці',
            'de': 'Ab {n} Punkten im Baum', 'es': 'Desde {n} puntos en el árbol', 'fr': 'Dès {n} points dans l’arbre',
            'it': 'Da {n} punti nell’albero', 'pl': 'Od {n} punktów w drzewie', 'pt': 'A partir de {n} pontos na árvore'},
    'free': {'ru': 'На выбор', 'en': 'Your pick', 'uk': 'На вибір', 'de': 'Freie Wahl', 'es': 'A elegir', 'fr': 'Au choix',
             'it': 'A scelta', 'pl': 'Do wyboru', 'pt': 'À escolha'},
    'free_d': {'ru': 'Здесь Icy Veins и Wowhead расходятся: варианты — в тексте ниже.',
               'en': 'Icy Veins and Wowhead differ here: the options are in the text below.',
               'uk': 'Тут Icy Veins і Wowhead розходяться: варіанти — у тексті нижче.',
               'de': 'Hier gehen Icy Veins und Wowhead auseinander: Die Optionen stehen im Text unten.',
               'es': 'Aquí Icy Veins y Wowhead difieren: las opciones están en el texto de abajo.',
               'fr': 'Ici, Icy Veins et Wowhead divergent : les options sont dans le texte ci-dessous.',
               'it': 'Qui Icy Veins e Wowhead divergono: le opzioni sono nel testo qui sotto.',
               'pl': 'Tu Icy Veins i Wowhead się różnią: opcje są w tekście poniżej.',
               'pt': 'Aqui o Icy Veins e o Wowhead divergem: as opções estão no texto abaixo.'},
    'order': {'ru': 'Порядок по уровням', 'en': 'Order by level', 'uk': 'Порядок за рівнями', 'de': 'Reihenfolge nach Stufe',
              'es': 'Orden por nivel', 'fr': 'Ordre par niveau', 'it': 'Ordine per livello', 'pl': 'Kolejność wg poziomu',
              'pt': 'Ordem por nível'},
}
EN_NAMES = ('en', 'uk', 'pl')              # the site keeps English talent names on these pages (content/spec_builds.py)

_names = None


def names():
    """i18n/names.json: English name -> de/es/fr/it/pt/ru (the client names, the same file the guides use)."""
    global _names
    if _names is None:
        _names = json.load(open(os.path.join(HERE, 'i18n', 'names.json'), encoding='utf-8'))
    return _names


def load(cid):
    p = os.path.join(DATA, f'{cid}.json')
    return json.load(open(p, encoding='utf-8')) if os.path.isfile(p) else None


def tname(t, lang):
    """A talent name on a page: the client's own name in that language, else the guides' dictionary, else English."""
    n = t['n']
    if lang in EN_NAMES:
        return n.get('en') or n.get('ru', '')
    return n.get(lang) or names().get(n.get('en', ''), {}).get(lang) or n.get('en') or n.get('ru', '')


def desc(t, lang):
    """The client's tooltip text for the talent in that language (the longest line that is not the name, rank or requirement)."""
    lines = (t.get('tip') or {}).get('en' if lang in EN_NAMES else lang) or []
    body = [x for x in lines[1:] if not re.match(r'^(Rank|Ранг|Requires|Требует|Rang|Rango|Grado|Nível)\b', x)]
    return max(body, key=len) if body else ''


def _plain(x):
    return re.sub(r'\s*\(.*\)$', '', x).strip().lower()


def match(data, cell):
    """The talent of a table row: its English name (or the spell id from i18n/names_ids.json), else the Russian one."""
    en = cell['en'] if isinstance(cell, dict) else cell
    ru = _plain(cell['ru']) if isinstance(cell, dict) else ''
    ids = json.load(open(os.path.join(HERE, 'i18n', 'names_ids.json'), encoding='utf-8')).get(en) or {}
    for tree in data['trees']:
        for t in tree['talents']:
            if _plain(t['n'].get('en', '')) == en.lower() or (ids.get('id') and ids['id'] in t.get('spells', ())):
                return tree, t
    for tree in data['trees']:
        for t in tree['talents']:
            if ru and _plain(t['n'].get('ru', '')) == ru:
                return tree, t
    return None, None


def plan(data, rows):
    """Our points on the tree and the order by level. rows: (table cell, points) in table order.
    Returns ({talent id: points}, steps). A step is (talent or None, points, first level, last level); None is a run of points
    the sources do not agree on: a row of the tree needs 5 points per row spent in it first, and the tail up to level 30."""
    picks, unknown = [], []
    for cell, pts in rows:
        tree, t = match(data, cell)
        if t is None:
            unknown.append(cell)
            continue
        picks.append((tree['key'], t, int(pts)))
    order = sorted(range(len(picks)), key=lambda i: (picks[i][1]['r'], i))
    spent, steps, level = {}, [], FIRST_LEVEL
    for i in order:
        key, t, pts = picks[i]
        need = ROW_POINTS * (t['r'] - 1) - spent.get(key, 0)
        if need > 0:                                               # the tree needs points we do not name
            steps.append((None, need, level, level + need - 1))
            spent[key] = spent.get(key, 0) + need
            level += need
        steps.append((t, pts, level, level + pts - 1))
        spent[key] = spent.get(key, 0) + pts
        level += pts
    if level <= CAP_LEVEL:
        steps.append((None, CAP_LEVEL - level + 1, level, CAP_LEVEL))
    return {t['id']: pts for _, t, pts in picks}, steps, spent, unknown


def lv(a, b, lang):
    return UI['lv'][lang].format(a=f'{a}–{b}' if b > a else a)


def _span(a, b):
    return f'{a}–{b}' if b > a else str(a)


def _icon(t, letters):
    """The sprite cell of a talent (--i on the button), or two letters on a plate when the icon is not known legally yet."""
    return '<i class="tt-ic"></i>' if t.get('icon') is not None else f'<i class="tt-ic no">{escape(letters)}</i>'


def _letters(name):
    w = re.findall(r'\w+', name)
    return (w[0][:2] if len(w) < 2 else w[0][0] + w[1][0]).capitalize() if w else '?'


def _arrows(tree, picked):
    """Lines from a prerequisite to its talent: straight down, straight across, or across then down (an elbow).
    --r/--c: the row and the leftmost column of the line, --n: how many rows or columns it spans (the CSS does the rest)."""
    by = {t['id']: t for t in tree['talents']}
    out = []
    for t in tree['talents']:
        src = by.get(t.get('req'))
        if not src:
            continue
        on = ' on' if t['id'] in picked and src['id'] in picked else ''
        r1, c1, r2, c2 = src['r'], src['c'], t['r'], t['c']
        if c1 == c2:                                               # down
            out.append(f'<i class="tt-ar v{on}" style="--r:{r1};--c:{c1};--n:{r2 - r1}"></i>')
            continue
        side = 'r' if c2 > c1 else 'l'
        if r1 == r2:                                               # across
            out.append(f'<i class="tt-ar h {side}{on}" style="--r:{r1};--c:{min(c1, c2)};--n:{abs(c2 - c1)}"></i>')
            continue
        out.append(f'<i class="tt-ar e {side}{on}" style="--r:{r1};--c:{min(c1, c2)};--n:{abs(c2 - c1)}"></i>'
                   f'<i class="tt-ar v m{on}" style="--r:{r1};--c:{c2};--n:{r2 - r1}"></i>')
    return ''.join(out)


def _l(x, lang):
    return x.get(lang) or x.get('en', '') if isinstance(x, dict) else x


PAGE = {}   # (class, lang) -> the talents of the page for the card, written once per page by page()


def render(cid, spec, rows, titles, lang, root):
    """The tree block of one spec section. rows: the spec's talent table rows [name cell, points, why],
    titles: {tree key: name, a t() dict}. '' when the class has no data yet. The card texts live in one JSON per page
    (page()), the block carries only its points: data-p = {talent id: [points, first level, last level, our line]}."""
    data = load(cid)
    if not data:
        return ''
    picked, steps, spent, _ = plan(data, [(r[0], r[1]) for r in rows])
    why = {}
    for r in rows:
        _, t = match(data, r[0])
        if t:
            why[t['id']] = _l(r[2], lang)
    titles = {k: _l(v, lang).split(':')[0].strip() for k, v in titles.items()}
    PAGE[(cid, lang)] = {'u': {k: v[lang] for k, v in UI.items() if k != 'hint'},
                         't': {t['id']: [tname(t, lang), t['m'], t['r'], desc(t, lang)] for tr in data['trees'] for t in tr['talents']}}
    pts = {}
    for i, (t, n, a, b) in enumerate(steps):
        pts[t['id'] if t else f'f{i}'] = [n, a, b, why.get(t['id'], '')] if t else [n, a, b]
    main = spec if spec in spent or not spent else max(spent, key=spent.get)
    tabs, trees = [], []
    for tree in data['trees']:
        key = tree['key']
        n = sum(picked.get(t['id'], 0) for t in tree['talents'])  # our named points; the runs «your pick» are not counted
        on = key == main
        title = escape(titles.get(key, key))
        tabs.append(f'<button type="button" role="tab" class="tt-tab" data-t="{key}" aria-selected="{"true" if on else "false"}">'
                    f'{title}<span>{n}</span></button>')
        cells = []
        for t in tree['talents']:
            name = tname(t, lang)
            p = picked.get(t['id'], 0)
            ic = f';--i:{t["icon"]}' if t.get('icon') is not None else ''
            cells.append(f'<button type="button" class="tt-t{" on" if p else ""}" style="--r:{t["r"]};--c:{t["c"]}{ic}" data-k="{t["id"]}" '
                         f'aria-label="{escape(name)}{f" {p}/{t["m"]}" if p else ""}">{_icon(t, _letters(name))}{f"<b>{p}</b>" if p else ""}</button>')
        rows_n = max(t['r'] for t in tree['talents'])
        trees.append(f'<div class="tt-tree{" on" if on else ""}" data-t="{key}" role="group" aria-label="{title}">'
                     f'<h3>{title}<span{" class=on" if n else ""}>{n}</span></h3>'
                     f'<div class="tt-grid" style="--rows:{rows_n}">{_arrows(tree, picked)}{"".join(cells)}</div></div>')
    rib = []
    for i, (t, n, a, b) in enumerate(steps):
        if t is None:
            rib.append(f'<li><span>{_span(a, b)}</span><button type="button" class="tt-t free" data-k="f{i}" aria-label="{UI["free"][lang]}">'
                       f'<i class="tt-ic no">?</i></button><b>×{n}</b></li>')
            continue
        name = tname(t, lang)
        ic = f' style="--i:{t["icon"]}"' if t.get('icon') is not None else ''
        rib.append(f'<li><span>{_span(a, b)}</span><button type="button" class="tt-t on"{ic} data-k="{t["id"]}" aria-label="{escape(name)}">'
                   f'{_icon(t, _letters(name))}</button><b>×{n}</b></li>')
    p_attr = escape(json.dumps(pts, ensure_ascii=False, separators=(',', ':')))
    return (f'<div class="tt" data-c="{cid}" data-l="{lang}" data-p="{p_attr}" '
            f'style="--n:{max(data.get("sprite", 0), 2)};--sp:url({root}assets/talents/{cid}.webp)">'
            f'<div class="tt-tabs" role="tablist">{"".join(tabs)}</div><div class="tt-trees">{"".join(trees)}</div>'
            f'<div class="tt-card" aria-live="polite"><p class="tt-hint">{UI["hint"][lang]}</p></div>'
            f'<h3 class="tt-oh">{UI["order"][lang]} @@BETA@@</h3><ol class="tt-rib">{"".join(rib)}</ol></div>')


CSS = """/* Talent trees (talents.py): three trees in a row when there is room, else the spec's tree and tabs; icons from one sprite */
.tt { container-type: inline-size; display: grid; gap: 14px; margin: 4px 0 6px; }
.tt-tabs { display: none; gap: 4px; flex-wrap: wrap; }
.tt-tab { min-height: 44px; padding: 0 14px; border: 0; border-radius: 6px; background: transparent; color: var(--muted); cursor: pointer; font: inherit; font-weight: 600; }
.tt-tab span { margin-left: 8px; color: var(--muted); font-variant-numeric: tabular-nums; }
.tt-tab:hover { background: var(--zebra); }
.tt-tab[aria-selected="true"] { background: var(--seg-on); color: var(--gold-2); }
.tt-trees { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; }
.tt-tree { --s: 44px; --g: 20px; --u: calc(var(--s) + var(--g)); padding: 12px 12px 18px; border-radius: 8px; background: var(--panel-2); min-width: 0; }
.tt-tree h3 { color: var(--fg); display: flex; justify-content: space-between; margin: 0 0 14px; font-family: var(--font-body); font-size: var(--fs-14); font-weight: 600; line-height: 1.3; letter-spacing: 0; }
.tt-tree h3 span { color: var(--muted); font-variant-numeric: tabular-nums; }
.tt-tree h3 span.on { color: var(--gold-2); }
.tt-grid { position: relative; display: grid; grid-template-columns: repeat(4, var(--s)); grid-template-rows: repeat(var(--rows), var(--s)); gap: var(--g); width: max-content; margin: 0 auto; }
.tt-t { position: relative; grid-row: var(--r); grid-column: var(--c); width: var(--s); height: var(--s); padding: 0; border: 1px solid var(--line-2); border-radius: 6px; background: #101114; cursor: pointer; }
.tt-ic { position: absolute; inset: 1px; border-radius: 4px; background: #16181c no-repeat 0 0 / calc(var(--n) * 100%) 100%; background-position-x: calc(var(--i) / (var(--n) - 1) * 100%); }
.tt.ld .tt-ic:not(.no) { background-image: var(--sp); }
.tt-ic.no { display: grid; place-items: center; font: 600 12px/1 var(--serif, Georgia), serif; color: #8d8a82; font-style: normal; }
.tt-t:not(.on) { border-color: var(--line); }
.tt-t:not(.on) .tt-ic { filter: grayscale(1) brightness(.62); }
.tt-t.on { border-color: var(--gold); }
.tt-t.free { border-style: dashed; border-color: var(--line-2); }
.tt-t.free .tt-ic { filter: none; opacity: 1; }
.tt-t b { position: absolute; right: -7px; bottom: -7px; min-width: 16px; padding: 1px 3px; border: 1px solid var(--gold); border-radius: 4px; background: var(--bg); color: var(--gold-2); font: 600 11px/1.2 system-ui, sans-serif; font-variant-numeric: tabular-nums; }
.tt-t[aria-pressed="true"] { outline: 2px solid var(--fg); outline-offset: 2px; }
.tt-t:focus-visible { outline: 2px solid var(--gold-2); outline-offset: 2px; }
.tt-ar { position: absolute; background: var(--line-2); color: var(--line-2); }
.tt-ar.v { width: 2px; left: calc((var(--c) - 1) * var(--u) + var(--s) / 2 - 1px); top: calc((var(--r) - 1) * var(--u) + var(--s)); height: calc(var(--n) * var(--u) - var(--s)); }
.tt-ar.v.m { top: calc((var(--r) - 1) * var(--u) + var(--s) / 2); height: calc(var(--n) * var(--u) - var(--s) / 2); }
.tt-ar.h, .tt-ar.e { height: 2px; top: calc((var(--r) - 1) * var(--u) + var(--s) / 2 - 1px); }
.tt-ar.h { left: calc((var(--c) - 1) * var(--u) + var(--s)); width: calc(var(--n) * var(--u) - var(--s)); }
.tt-ar.e.r { left: calc((var(--c) - 1) * var(--u) + var(--s)); width: calc(var(--n) * var(--u) - var(--s) / 2 + 1px); }
.tt-ar.e.l { left: calc((var(--c) - 1) * var(--u) + var(--s) / 2 - 1px); width: calc(var(--n) * var(--u) - var(--s) / 2 + 1px); }
.tt-ar.on { background: var(--gold); color: var(--gold); }
.tt-ar.v::after { content: ""; position: absolute; left: -3px; bottom: -1px; border: 4px solid transparent; border-bottom: 0; border-top: 5px solid currentColor; }
.tt-ar.h.r::after { content: ""; position: absolute; right: -1px; top: -3px; border: 4px solid transparent; border-right: 0; border-left: 5px solid currentColor; }
.tt-ar.h.l::after { content: ""; position: absolute; left: -1px; top: -3px; border: 4px solid transparent; border-left: 0; border-right: 5px solid currentColor; }
.tt-card { min-height: 48px; padding: 12px 14px; border: 1px solid var(--line); border-radius: 8px; }
.tt-card .h { display: block; margin: 0 0 2px; font-family: var(--font-body); font-size: var(--fs-16); font-weight: 600; line-height: 1.3; letter-spacing: 0; color: var(--fg); }
.tt-card .m { margin: 0 0 6px; font-size: var(--fs-13); color: var(--gold-2); }
.tt-card p { margin: 0; color: var(--fg); font-size: var(--fs-14); }
.tt-card .tt-hint { color: var(--muted); }
.tt-oh { margin: 6px 0 0; font-family: var(--font-body); font-size: var(--fs-14); font-weight: 600; line-height: 1.3; letter-spacing: 0; color: var(--fg); }
.tt-rib { display: flex; flex-wrap: wrap; gap: 12px 18px; margin: 0; padding: 0; list-style: none; }
.tt-rib li { display: grid; grid-template-columns: auto auto; grid-template-rows: auto auto; column-gap: 6px; align-items: center; }
.tt-rib span { grid-column: 1 / -1; font-size: var(--fs-13); color: var(--gold-2); font-variant-numeric: tabular-nums; white-space: nowrap; }
.tt-rib .tt-t { --s: 36px; }
.tt-rib b { font-family: var(--font-body); font-size: var(--fs-14); font-weight: 600; line-height: 1; letter-spacing: 0; color: var(--muted); font-variant-numeric: tabular-nums; }
@container (max-width: 759px) {
  .tt-tabs { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); }
  .tt-tab { padding: 4px; font-size: var(--fs-14); line-height: 1.2; }
  .tt-tab span { display: inline-block; margin-left: 5px; white-space: nowrap; }
  .tt-trees { grid-template-columns: minmax(0, 1fr); }
  .tt-tree:not(.on) { display: none; }
  .tt-tree { --s: 44px; --g: min(26px, calc((100cqi - 24px - 4 * var(--s)) / 3)); }
  .tt-tree h3 { display: none; }
}
"""

JS = r"""<script>
/* Talent trees: the card under the tree on tap (and on hover with a mouse), the tabs on narrow screens, the sprite near the screen.
   #ttData: {u: texts, t: {id: [name, ranks, row, client text]}}; a block's data-p: {id: [points, from, to, our line]}. */
(function () {
  var D = JSON.parse(document.getElementById('ttData').textContent), U = D.u;
  var hover = window.matchMedia && matchMedia('(hover: hover)').matches;
  function f(s, o) { return s.replace(/\{(\w)\}/g, function (_, k) { return o[k]; }); }
  function lv(a, b) { return f(U.lv, { a: b > a ? a + '–' + b : a }); }
  document.querySelectorAll('.tt').forEach(function (w) {
    var card = w.querySelector('.tt-card'), P = JSON.parse(w.dataset.p), cur = null;
    function line(cls, text) { var e = document.createElement(cls === 'h' ? 'b' : 'p'); e.className = cls; e.textContent = text; card.appendChild(e); }
    function show(b) {
      var k = b.dataset.k, p = P[k], t = D.t[k], meta = [];
      if (cur) cur.removeAttribute('aria-pressed');
      cur = b; b.setAttribute('aria-pressed', 'true');
      card.textContent = '';
      if (!t) { line('h', U.free); line('m', lv(p[1], p[2])); line('w', U.free_d); return; }
      meta.push(p ? f(U.take, { p: p[0], m: t[1] }) : f(U.skip, { m: t[1] }));
      if (p) meta.push(lv(p[1], p[2]));
      if (t[2] > 1) meta.push(f(U.row, { n: 5 * (t[2] - 1) }));
      line('h', t[0]); line('m', meta.join(' · '));
      if ((p && p[3]) || t[3]) line('w', (p && p[3]) || t[3]);
    }
    w.addEventListener('click', function (e) {
      var tab = e.target.closest('.tt-tab');
      if (tab) {
        w.querySelectorAll('.tt-tab').forEach(function (x) { x.setAttribute('aria-selected', x === tab ? 'true' : 'false'); });
        w.querySelectorAll('.tt-tree').forEach(function (x) { x.classList.toggle('on', x.dataset.t === tab.dataset.t); });
        return;
      }
      var b = e.target.closest('[data-k]');
      if (b) show(b);
    });
    if (hover) w.addEventListener('mouseover', function (e) { var b = e.target.closest('[data-k]'); if (b && b !== cur) show(b); });
  });
  var all = document.querySelectorAll('.tt');
  if (!('IntersectionObserver' in window)) { all.forEach(function (w) { w.classList.add('ld'); }); return; }
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('ld'); io.unobserve(e.target); } });
  }, { rootMargin: '300px 0px' });
  all.forEach(function (w) { io.observe(w); });
})();
</script>
"""


def page(html):
    """Adds the styles, the talents of the page (card texts) and the script once to a built page that has a tree."""
    m = re.search(r'<div class="tt" data-c="([a-z]+)" data-l="([a-z]+)"', html)
    if not m:
        return html
    data = json.dumps(PAGE[(m.group(1), m.group(2))], ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    html = html.replace('</style>', CSS + '</style>', 1)
    return html.replace('</body>', f'<script type="application/json" id="ttData">{data}</script>\n' + JS + '</body>', 1)
