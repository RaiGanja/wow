"""Сборка гайдов: guide.src.html + content/guides.py -> guides/[slug/]index.html, en/…, uk/….
Обвязка шаблона переводится через i18n/{ru,en,uk}.txt + i18n/guides.*.txt (строка в строку);
тело подставляется ПОСЛЕ перевода — тексты гайдов уже на трёх языках, translate() их не видит.
Запуск: python build_guides.py [--list]  (--list печатает русские фрагменты обвязки без перевода)"""
import json, os, re, sys
from html import escape

import build
import tod
from build import LANGS, SITE, page_dir, rel, localize, translate
import langs
from content.guides import GUIDES, HUB, HUBS, NEWS, NOT_FOUND, PAGES, PLAY_MILESTONES, PLAY_TX

HERE = build.HERE

_ru, _en, _uk = (build.load(f'guides.{l}.txt') for l in langs.OLD)
assert len(_ru) == len(_en) == len(_uk), (len(_ru), len(_en), len(_uk))
build.T.update({r: (e, u) for r, e, u in zip(_ru, _en, _uk)})
langs.fill([GUIDES, HUB, HUBS, NEWS, NOT_FOUND, PAGES])   # new languages of every guide text: i18n/<lang>.json by the English one

TIP = {'ru': 'Совет', 'en': 'Tip', 'uk': 'Порада'}
THIS_PAGE = {'ru': 'Эта страница', 'en': 'This page', 'uk': 'Ця сторінка'}
MORE_H = {'ru': 'Другие гайды', 'en': 'Other guides', 'uk': 'Інші гайди'}
MORE_SITE = {'ru': 'Ещё на сайте', 'en': 'More on the site', 'uk': 'Ще на сайті'}
# Extra tiles under the classes/ and races/ pages: the guides hub and the tools page
SITE_TILES = [
    {'t': HUB['title'], 'href': 'guides/', 'art': 'hero_guides',
     'd': {'ru': 'Прокачка, подземелья, профессии и ответы', 'en': 'Leveling, dungeons, professions and answers', 'uk': 'Прокачка, підземелля, професії та відповіді'}},
    {'t': {'ru': 'Инструменты', 'en': 'Tools', 'uk': 'Інструменти'}, 'href': 'tools/', 'art': 'hero_tools',
     'd': {'ru': 'Рамки, сравнение, поиск', 'en': 'Frames, compare, search', 'uk': 'Рамки, порівняння, пошук'}},
    {'t': {'ru': 'В игре', 'en': 'In game', 'uk': 'У грі'}, 'href': 'play/', 'art': 'hero_campfire',
     'd': {'ru': 'Второй экран: радио, уровень, таймеры', 'en': 'Second screen: radio, level, timers', 'uk': 'Другий екран: радіо, рівень, таймери'}},
]
# Wide hero art; everything else is a class/race portrait cut at 360/600/896
WIDTHS = {'hero_dawn': (960, 1440, 1920, 2560, 3840), 'hero_campfire': (960, 1600, 2560),
          'hero_tools': (960, 1440, 1920, 2560)}   # the tools scene is also the Tools tile
FX = {'hero_dawn': 'dawn', 'hero_campfire': 'camp'}   # living art (assets/living/living.js) over these heroes
# A guide with 'hero' gets the full-screen inner page hero (.thero, like roster and tools): its own scene, living art,
# a portrait cut on phones (tools/make_images.py INNER, CUTS); 'art' stays for the tiles and the share preview.
THERO = {'hero_guides': 'guides', 'hero_dungeons': 'dungeons', 'hero_professions': 'professions', 'hero_faq': 'faq',
         'hero_news': None, 'hero_leveling': 'leveling', 'hero_classes': 'classes', 'hero_races': 'races',
         'hero_ukrainian': 'ukrainian', 'hero_requirements': 'requirements'}
THERO_W = (960, 1440, 1920, 2560)
WIDTHS.update({h: THERO_W for h in THERO})   # a page's own scene is also its tile (cut 4:3 by the tile) and share preview


LAUNCH_UTC = '23:00 UTC'
YOUR = {'ru': 'по вашему времени', 'en': 'your time', 'uk': 'за вашим часом', 'de': 'deine Zeit', 'fr': 'votre heure',
        'es': 'tu hora', 'pt': 'seu horário', 'it': 'ora locale', 'pl': 'twój czas'}
LOCAL_JS = """<script>
document.querySelectorAll('time.lt').forEach(t => {
  const s = new Intl.DateTimeFormat(document.documentElement.lang, { day: 'numeric', month: 'long', hour: '2-digit', minute: '2-digit' }).format(new Date(t.dateTime));
  t.after(` (@@YOUR@@: ${s})`);
});
</script>
"""


def L(x, lang):
    return x[lang] if isinstance(x, dict) else x


def E(x, lang):
    return escape(L(x, lang), quote=True)


def check_langs(obj, path=''):
    """Paths of trilingual fields that miss ru/en/uk (or are empty); the new languages are derived from en by langs.fill."""
    gaps = []
    if isinstance(obj, dict) and (obj.get('only') or obj.get('langs')):   # one-language guide, ru/uk-only section
        return gaps
    if isinstance(obj, dict):
        if set(obj) & set(langs.OLD) and set(obj) <= set(langs.ALL):
            gaps += [f'{path}.{l}' for l in langs.OLD if not obj.get(l)]
        else:
            for k, v in obj.items():
                gaps += check_langs(v, f'{path}.{k}')
    elif isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            gaps += check_langs(v, f'{path}[{i}]')
    return gaps


def art_sets(art, root, big=False):
    """(avif srcset, webp srcset, fallback src). big: hero fallback = widest, else a tile-sized one."""
    ws = WIDTHS.get(art, (360, 600, 896))
    src = lambda ext: ', '.join(f'{root}assets/art/{art}-{w}.{ext} {w}w' for w in ws)
    fb = ws[-1] if big else (ws[0] if art in WIDTHS else 600)
    return src('avif'), src('webp'), f'{root}assets/art/{art}-{fb}.webp'


def thero(sec, hero):
    """The guide's art band rewritten as the full-screen hero: same crumbs, title, lead and pills (still untranslated)."""
    m = lambda ext: ', '.join(f'@@ROOT@@assets/art/{hero}-m-{w}.{ext} {w}w' for w in (600, 1000))   # noqa: E731
    big = lambda ext: ', '.join(f'@@ROOT@@assets/art/{hero}-{w}.{ext} {w}w' for w in THERO_W)   # noqa: E731
    phone = 'media="(max-width: 719px) and (max-aspect-ratio: 2/3)"'
    fx = f' data-fx="{THERO[hero]}" data-cut=".9"' if THERO[hero] else ''   # living layer only where a mask exists
    pic = (f'<picture class="thero-art" aria-hidden="true"{fx}>\n'
           f'    <source {phone} type="image/avif" srcset="{m("avif")}" sizes="78vh">\n'
           f'    <source {phone} type="image/webp" srcset="{m("webp")}" sizes="78vh">\n'
           f'    <source type="image/avif" srcset="{big("avif")}" sizes="(max-aspect-ratio: 16/9) 180vh, 100vw">\n'
           f'    <source type="image/webp" srcset="{big("webp")}" sizes="(max-aspect-ratio: 16/9) 180vh, 100vw">\n'
           f'    <img src="@@ROOT@@assets/art/{hero}-1920.webp" width="1920" height="1072" alt="" fetchpriority="high" decoding="async">\n'
           '  </picture>')
    sec = re.sub(r'@@HERO@@|<picture class="stband-art".*?</picture>', lambda _: pic, sec, count=1, flags=re.S)   # the template's slot
    return (sec.replace('<section class="stband ghero" id="top">', '<section class="thero" id="top">', 1)
               .replace('<div class="wrap">', '<div class="wrap thero-in">', 1).replace('class="glead"', 'class="lead"', 1))


def tile_links(tiles, lang, root):
    """root: path to the language home (links); art always from the site root via @@ROOT@@."""
    out = []
    for s in tiles:
        avif, webp, img = art_sets(s['art'], '@@ROOT@@')
        out.append(f'<a class="ttile" href="{root}{s["href"]}"><picture><source type="image/avif" srcset="{avif}" sizes="320px">'
                   f'<img src="{img}" srcset="{webp}" sizes="320px" alt="" loading="lazy" decoding="async"></picture>'
                   f'<b>{E(s["t"], lang)}</b><span>{E(s["d"], lang)}</span></a>')   # the update date is on the page itself
    return ''.join(out)


def render_block(kind, data, lang, root):
    if kind == 'text':
        return ''.join(f'<p>{E(p, lang)}</p>' for p in data)
    if kind == 'list':
        return '<ul>' + ''.join(f'<li>{E(p, lang)}</li>' for p in data) + '</ul>'
    if kind == 'steps':
        cards = ''.join(f'<li><span class="n">{i}</span><div><b>{E(s["t"], lang)}</b><p>{E(s["d"], lang)}</p></div></li>'
                        for i, s in enumerate(data, 1))
        return f'<ol class="steps-c">{cards}</ol>'
    if kind == 'tiles':
        return f'<div class="ttiles gtiles">{tile_links(data, lang, root)}</div>'
    if kind == 'table':
        head = [E(h, lang) for h in data['head']]
        th = ''.join(f'<th scope="col">{h}</th>' for h in head)
        rows = ''.join('<tr>' + ''.join(f'<td data-l="{h}">{E(c, lang)}</td>' for h, c in zip(head, r)) + '</tr>'
                       for r in data['rows'])
        return f'<table class="gtable"><thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table>'
    if kind == 'picks':                                           # table whose second column links class pages
        head = [E(h, lang) for h in data['head']]
        name = {c['id']: build.tr(c['n'], lang) for c in build.CLASSES}
        def cls(ids):
            return ', '.join(f'<a href="{root}classes/{i}/">{escape(name[i])}</a>' for i in ids)
        rows = ''.join(f'<tr><td data-l="{head[0]}">{E(r[0], lang)}</td><td data-l="{head[1]}">{cls(r[1])}</td>'
                       + ''.join(f'<td data-l="{h}">{E(c, lang)}</td>' for h, c in zip(head[2:], r[2:])) + '</tr>'
                       for r in data['rows'])
        th = ''.join(f'<th scope="col">{h}</th>' for h in head)
        return f'<table class="gtable picks"><thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table>'
    if kind == 'tabs':
        btns = ''.join(f'<button type="button" class="pill" role="tab" data-tab="{x["id"]}" aria-selected="{"true" if i == 0 else "false"}">'
                       f'{E(x["t"], lang)}</button>' for i, x in enumerate(data))
        panels = ''.join(f'<div role="tabpanel" data-tab="{x["id"]}"{"" if i == 0 else " hidden"}>'
                         + ''.join(render_block(k, d, lang, root) for k, d in x['blocks']) + '</div>'
                         for i, x in enumerate(data))
        return f'<div class="gtabs"><div role="tablist">{btns}</div>{panels}</div>'
    if kind == 'faq':
        ext = lambda u: u.startswith('http')   # noqa: E731  external link: new tab and an arrow, a guide page: same tab
        items = ''.join(f'<details id="{q["id"]}"><summary>{E(q["q"], lang)}</summary>'
                        + ''.join(f'<p>{E(a, lang)}</p>' for a in q['a'])
                        + (f'<p class="gbtns"><a class="btn ghost" href="{q["link"][1]}"'
                           + (f' target="_blank" rel="noopener">{E(q["link"][0], lang)} ↗' if ext(q['link'][1]) else f'>{E(q["link"][0], lang)}')
                           + '</a></p>' if q.get('link') else '') + '</details>' for q in data)
        return f'<div class="gfaq">{items}</div>'
    if kind == 'tip':
        return (f'<div class="tipbox"><svg class="ico fi" aria-hidden="true"><use href="#i-fire"/></svg>'
                f'<p><span class="tl">{TIP[lang]}</span>{E(data, lang)}</p></div>')
    if kind == 'play':                                            # Leveling: the in-game page in one line
        return (f'<a class="gplay frame" href="{root}play/"><span><b>{E(data["h"], lang)}</b> {E(data["d"], lang)}</span>'
                f'<span class="btn ghost">{E(data["go"], lang)}</span></a>')
    if kind == 'raw':
        return L(data, lang)
    if kind == 'news':                                            # our notes from NEWS, newest first
        items = ''.join(f'<a class="nitem" href="{escape(n["url"])}" target="_blank" rel="noopener">'
                        f'<time datetime="{n["date"]}">{".".join(reversed(n["date"].split("-")))}</time>'
                        f'<b>{E(n["title"], lang)}</b><p>{E(n["text"], lang)}</p></a>'
                        for n in sorted(NEWS, key=lambda n: n['date'], reverse=True))
        return f'<div class="nlist">{items}</div>'
    if kind == 'profs':
        return render_block('table', {'head': PROF_HEAD, 'rows': profs_table(home_src())}, lang, root)
    raise ValueError(f'unknown block {kind!r}')


PROF_HEAD = [{'ru': 'Профессия', 'en': 'Profession', 'uk': 'Професія'},
             {'ru': 'Объект лагеря', 'en': 'Camp object', 'uk': 'Об’єкт табору'},
             {'ru': 'Похож на бафф', 'en': 'Similar buff', 'uk': 'Схожий на бафф'}]


def home_src():
    return open(os.path.join(HERE, 'index.src.html'), encoding='utf-8').read()


def profs_table(src):
    """Camp table from PROFS of the home page: [name, object, effect]; names and effects via the home i18n."""
    tr = lambda x: langs.derive({'ru': x, 'en': build.T[x][0], 'uk': build.T[x][1]})
    return [[tr(name), obj, tr(eff)]
            for _id, name, _tier, obj, eff in re.findall(r"\['(\w+)', '([^']+)', (\d), '([^']+)', '([^']+)'\]", src)]


def render_guide(g, lang, root):
    sections = [s for s in g['sections'] if lang in s.get('langs', (lang,))]   # 'langs': a section only in these languages
    toc = ''.join(f'<a href="#{s["id"]}">{E(s["title"], lang)}</a>' for s in sections)
    body = '\n'.join(f'<section class="frame gsec" id="{s["id"]}"><h2>{E(s["title"], lang)}</h2>'
                     + ''.join(render_block(k, d, lang, root) for k, d in s['blocks']) + '</section>'
                     for s in sections)
    return toc, body


def guide_tiles(guides):
    # a tile shows the guide's own scene when it has one: portraits stay on the class and race pages, no picture twice on a page
    return [{'t': x['title'], 'd': x['tile'], 'href': f'guides/{x["slug"]}/', 'art': x.get('hero') or x['art']} for x in guides]


def section_tiles():
    return [{'t': x['title'], 'd': x['tile'], 'href': x['path'], 'art': x['art']} for x in HUBS]


def lang_guides(lang):
    """Guides of a language: a guide with 'only' exists in that one language."""
    return [g for g in GUIDES if g.get('only', lang) == lang]


def hub_body(lang, root):
    """Guides first, then the classes/ and races/ sections and the tools page: two full rows of four."""
    tiles = guide_tiles(lang_guides(lang)) + section_tiles() + SITE_TILES[1:]
    return '', f'<section class="gsec bare" id="all">{render_block("tiles", tiles, lang, root)}</section>'


JS = {}   # slug -> JS живой части; наполняется в задачах 3, 5, 7, 8, 9

JS['faq'] = r'''/* FAQ: search over questions and answers; #id opens the question */
const qIn = document.getElementById('faqQ');
const qs = [...document.querySelectorAll('.gfaq details')];
const qNone = document.getElementById('faqNone');
if (qIn) qIn.addEventListener('input', () => {
  const v = qIn.value.trim().toLowerCase();
  let n = 0;
  qs.forEach(d => {
    const hit = !v || d.textContent.toLowerCase().includes(v); d.hidden = !hit;
    if (v && hit) { n++; if (!d.open) { d.open = true; d.dataset.byq = '1'; } }
    if (!v && d.dataset.byq) { d.open = false; delete d.dataset.byq; }   // clearing the field folds what the search opened
  });
  if (qNone) qNone.hidden = !v || n > 0;
});
function openHash() { const d = location.hash && document.getElementById(decodeURIComponent(location.hash.slice(1))); if (d && d.tagName === 'DETAILS') { d.open = true; d.scrollIntoView(); } }
addEventListener('hashchange', openHash); openHash();'''


DG_TX = {
    'ru': {'h': ['Подземелье', 'Уровни', 'Где вход'], 'new': 'новое', 'shown': 'Показано', 'of': 'из',
           'none': 'Под этот уровень подземелий нет.', 'need': 'Укажите свой уровень, чтобы отфильтровать.',
           'only': {'alliance': 'Только Альянс', 'horde': 'Только Орда'}},
    'en': {'h': ['Dungeon', 'Levels', 'Entrance'], 'new': 'new', 'shown': 'Showing', 'of': 'of',
           'none': 'No dungeons for this level.', 'need': 'Enter your level to filter.',
           'only': {'alliance': 'Alliance only', 'horde': 'Horde only'}},
    'uk': {'h': ['Підземелля', 'Рівні', 'Де вхід'], 'new': 'нове', 'shown': 'Показано', 'of': 'з',
           'none': 'Під цей рівень підземель немає.', 'need': 'Вкажіть свій рівень, щоб відфільтрувати.',
           'only': {'alliance': 'Лише Альянс', 'horde': 'Лише Орда'}},
}
DG_JS = r'''/* Dungeons: level filter seeded from "My hero" (read only, the hero is edited on the home page) */
const TX = @@TX@@;
const lvRange = d => d[1] === d[2] ? String(d[1]) : `${d[1]}–${d[2]}`;
const nearLvl = (d, lv) => lv >= d[1] - 3 && lv <= d[2] + 3;
const HORDE = ['orc', 'undead', 'tauren', 'troll', 'skyH'];
let dgLvl = 0, dgFac = '';
try { const m = JSON.parse(localStorage.getItem('gabella-wf-me')) || {}; dgLvl = +m.lvl || 0; dgFac = m.race ? (HORDE.includes(m.race) ? 'horde' : 'alliance') : ''; } catch (e) {}
let dgMode = dgLvl ? 'mine' : 'all';
const lvIn = $('#dgLvl');
function renderDg() {
  let rows = DUNGEONS;
  if (dgMode === 'new') rows = rows.filter(d => d[4]);
  if (dgMode === 'mine') rows = dgLvl ? rows.filter(d => nearLvl(d, dgLvl) && (!dgFac || !d[6] || d[6] === dgFac)) : [];
  $('#dgBody').innerHTML = rows.length ? rows.map(d => {
    const mine = dgLvl && nearLvl(d, dgLvl);
    const alt = (d[5] || []).map(a => `${a[0]}: ${a[1]}`).join(', ');
    return `<tr class="${mine ? 'mine' : ''}"><td data-l="${TX.h[0]}">${esc(d[0])}${d[4] ? ` <span class="tag new">${TX.new}</span>` : ''}</td>`
      + `<td data-l="${TX.h[1]}"><span class="lvl${mine ? ' gold' : ''}">${lvRange(d)}</span>${alt ? `<span class="alt">${esc(alt)}</span>` : ''}</td>`
      + `<td data-l="${TX.h[2]}">${esc(d[3])}${d[6] ? `<span class="alt">${TX.only[d[6]]}</span>` : ''}</td></tr>`;
  }).join('') : `<tr><td colspan="3">${dgLvl ? TX.none : TX.need}</td></tr>`;
  $('#dgCount').textContent = `${TX.shown} ${rows.length} ${TX.of} ${DUNGEONS.length}`;
  document.querySelectorAll('#segD button').forEach(b => b.setAttribute('aria-pressed', b.dataset.v === dgMode));
  if (document.activeElement !== lvIn) lvIn.value = dgLvl || '';
}
$('#segD').addEventListener('click', e => { const b = e.target.closest('button'); if (b) { dgMode = b.dataset.v; renderDg(); } });
lvIn.addEventListener('input', () => { const v = parseInt(lvIn.value, 10); dgLvl = v >= 1 && v <= 60 ? v : 0; dgMode = dgLvl ? 'mine' : 'all'; renderDg(); });
document.querySelectorAll('#dgBox .lvm, #dgBox .lvp').forEach(b => b.addEventListener('click', () => {
  const up = b.classList.contains('lvp');
  dgLvl = Math.max(1, Math.min(60, (dgLvl || (up ? 0 : 2)) + (up ? 1 : -1))); dgMode = 'mine'; renderDg();
}));
renderDg();'''
langs.fill([TIP, THIS_PAGE, MORE_H, MORE_SITE, SITE_TILES, PROF_HEAD, DG_TX, PLAY_TX, PLAY_MILESTONES])
JS['dungeons'] = {l: DG_JS.replace('@@TX@@', json.dumps(DG_TX[l], ensure_ascii=False)) for l in LANGS}


def dungeons_data(src, lang=None):
    """Only the DUNGEONS array of the home page: the rest of its data is Russian and not needed here."""
    i = src.index('const DUNGEONS = [')
    return src[i:src.index('\n];', i) + 3]


JS['professions'] = r'''/* Professions: open the tab of the class from the link (#pairs=mage, class pages and the compare tool) or from "My hero" */
try {
  const link = (location.hash.match(/^#pairs=(\w+)$/) || [])[1];
  const cls = link || (JSON.parse(localStorage.getItem('gabella-wf-me')) || {}).cls;
  const tab = cls && document.querySelector(`#pairs [role="tab"][data-tab="${cls}"]`);
  if (tab) tab.click();
  if (link) document.getElementById('pairs').scrollIntoView();
} catch (e) {}'''


JS['news'] = r'''/* News: automatic Wowhead feed from assets/news.json; no file -> the list stays hidden */
fetch(ROOT + 'assets/news.json').then(r => r.ok ? r.json() : []).then(items => {
  const box = document.getElementById('feedList');
  if (!box || !items.length) return;
  let day = '';   // grouped by day: the date once as a heading, the entries under it as plain lines
  box.innerHTML = items.filter(n => /^https:\/\//.test(n.url)).map(n => (n.date !== day ? `<h3 class="nday">${esc((day = n.date).split('-').reverse().join('.'))}</h3>` : '')
    + `<a class="nitem" href="${esc(n.url)}" target="_blank" rel="noopener"><b>${esc(n.title)}</b></a>`).join('');
  box.hidden = false;
}).catch(() => {});'''


def ref_js(src, lang):
    """Classes/races data and the comparison-table helpers of the home page (ref:start…ref:end), translated like the home page."""
    i, j = src.index('/* ref:start'), src.index('/* ref:end */')
    js = src[i:j].replace('@@RACE_LEAD@@', json.dumps({r['id']: r['lead'] for r in build.RACES_PAGE}, ensure_ascii=False))
    js = js.replace('@@RACE_SLUG@@', json.dumps({r['id']: r['slug'] for r in build.RACES_PAGE}))
    return translate(js, lang)[0]


JS['classref'] = 'renderClassRef();'
JS['raceref'] = 'renderRaceRef();'

# ---------- /play/ «В игре»: compact page, a second screen while playing ----------

def leveling_parts():
    """From the Leveling guide: zone route {faction: [(lo, hi, text)]} and the tip of the pace section."""
    g = next(x for x in GUIDES if x['slug'] == 'leveling')
    sec = {s['id']: s for s in g['sections']}
    tabs = next(d for k, d in sec['route']['blocks'] if k == 'tabs')
    route = {}
    for tab in tabs:
        steps = next(d for k, d in tab['blocks'] if k == 'steps')
        route[tab['id']] = [(*map(int, L(x['t'], 'ru').split('–')), x['d']) for x in steps]
    tip = next(d for k, d in sec['pace']['blocks'] if k == 'tip')
    return route, tip


def play_data(src, lang):
    """Language data of the page script: route, milestones, labels, race -> faction and race/class names."""
    route, _ = leveling_parts()
    races = build.parse_races(src)
    data = {
        'route': {f: [[lo, hi, L(d, lang)] for lo, hi, d in rows] for f, rows in route.items()},
        'miles': [[lv, L(x, lang)] for lv, x in PLAY_MILESTONES],
        'tx': {k: L(v, lang) for k, v in PLAY_TX.items()},
        'racef': {r['id']: r['f'] for r in races},
        'rn': {r['id']: build.tr(r['n'], lang) for r in races},
        'cn': {c['id']: build.tr(c['n'], lang) for c in build.CLASSES},
    }
    return dungeons_data(src) + '\nconst P = ' + json.dumps(data, ensure_ascii=False) + ';\n'


def play_head(lang):
    """Title and lead on the left, the screen buttons on the right (each shows up only where the browser can do it)."""
    x = lambda k: E(PLAY_TX[k], lang)
    return ('<section class="phead" id="top"><div class="wrap"><div class="ptitle"><h1>@@TITLE@@</h1><p class="glead">@@LEAD@@</p></div>'
            '<div class="pacts"><button class="pill pwake" id="wakeBtn" type="button" aria-pressed="false" hidden>'
            f'<svg class="ico" aria-hidden="true"><use href="#i-sun"/></svg>{x("wake")}</button></div></div></section>'
            f'<div class="wrap"><section class="frame pway" id="pWay" aria-label="{x("profile")}" hidden></section></div>')


def play_body(lang, root):
    x = lambda k: E(PLAY_TX[k], lang)
    _, tip = leveling_parts()
    fac = ''.join(f'<button type="button" class="pill" data-f="{f}" aria-pressed="false">{x(f)}</button>' for f in ('alliance', 'horde'))
    presets = (f'<button type="button" class="pill" data-min="15" data-name="{x("food")}" title="{x("foodNote")}">{x("food")} · 15 {x("min")}</button>'
               + ''.join(f'<button type="button" class="pill" data-min="{m}">{m} {x("min")}</button>' for m in (5, 10, 30)))
    return f'''<div class="pgrid"><div class="pcol">
<section class="frame psec" id="level" aria-labelledby="hLvl">
  <div class="phero"><h2 id="hLvl">{x("lvl")}</h2><span id="pWho"></span><a href="{root}#me">{x("edit")}</a></div>
  <div class="pchars" id="pChars" role="group" aria-label="{x("chars")}" hidden></div>
  <div class="pfac" id="pFac" role="group" aria-label="{x("fac")}">{fac}</div>
  <div class="plv"><button type="button" class="lvb" id="lvDown" aria-label="{x("lvDown")}">−</button><output id="lvOut" aria-live="polite">—</output><button type="button" class="lvb" id="lvUp" aria-label="{x("lvUp")}">+</button></div>
  <div id="pNow"></div>
  {render_block('tip', tip, lang, root)}
  <a class="pmore" href="{root}guides/leveling/#route">{x("route")}</a>
</section>
<section class="frame psec" id="dung" aria-labelledby="hDg"><h2 id="hDg">{x("dung")} <span id="dgLv">…</span></h2><ul class="pdg" id="pDg"></ul>
  <a class="pmore" href="{root}guides/dungeons/#list">{x("all")}</a></section>
</div><div class="pcol">
<section class="frame psec" id="radio" aria-labelledby="hRadio"><h2 id="hRadio">{x("radio")}</h2><div id="radioDock"></div></section>
<section class="frame psec" id="timers" aria-labelledby="hT"><h2 id="hT">{x("timers")}</h2>
  <div class="ppre" id="tPre">{presets}</div>
  <form class="pform" id="tForm" novalidate><input id="tName" maxlength="40" placeholder="{x("name")}" aria-label="{x("name")}">
    <input id="tMin" type="number" min="1" max="600" inputmode="numeric" placeholder="{x("minutes")}" aria-label="{x("minutes")}">
    <button type="submit" class="pill gold">{x("start")}</button></form>
  <ul class="ptl" id="tList" aria-live="polite"></ul>
  <label class="pnotify" id="tNotify" hidden><input type="checkbox"> {x("notify")}</label>
</section>
</div></div>'''


JS['play'] = r'''/* In game: level -> zones and the next milestones (data from the Leveling guide), dungeons near the level, timers,
   screen wake lock, the mini window. Level, race and class are the shared hero "gabella-wf-me" of the home page (the level is
   written back); signed in, the hero is one of the profile characters and the level is saved to it. The chosen character,
   the faction without a race, the timers and the notification choice live in "gabella-play". */
const TX = P.tx, MEKEY = 'gabella-wf-me', PKEY = 'gabella-play';
const rd = k => { try { return JSON.parse(localStorage.getItem(k)) || {}; } catch (e) { return {}; } };
const wr = (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} };
const ps = Object.assign({ fac: 'alliance', timers: [], notify: false }, rd(PKEY));
if (!Array.isArray(ps.timers)) ps.timers = [];
const saveP = () => wr(PKEY, ps);
const GM = () => window.GabellaMe;   // me.js: the profile client, there on every page once it has loaded
let meNow = null, saveT = 0, pending = false, firstMe = true;
function chars() { return (meNow && meNow.characters) || []; }
function curChar() { const cs = chars(); return cs.find(c => c.id === ps.char) || cs.find(c => c.is_main) || cs[0] || null; }
function useChar(c) { const m = rd(MEKEY); m.race = c.race; m.cls = c.class; m.lvl = c.level; wr(MEKEY, m); }
const lvOf = m => Math.max(0, Math.min(60, parseInt(m.lvl, 10) || 0));
const lvRange = d => d[1] === d[2] ? String(d[1]) : `${d[1]}–${d[2]}`;
const nearLvl = (d, lv) => lv >= d[1] - 3 && lv <= d[2] + 3;
function setLvl(v) {
  const m = rd(MEKEY), c = curChar();
  m.lvl = Math.max(1, Math.min(60, v)); wr(MEKEY, m);
  if (c) { c.level = m.lvl; pending = true; saveLvl(); }
  renderLvl();
}
/* The level goes to the profile 1.5 s after the last tap: one request for a run of taps. While it is on its way the level on
   the screen wins over the one the profile answers with */
function saveLvl() {
  clearTimeout(saveT);
  saveT = setTimeout(() => {
    const c = curChar(), lv = lvOf(rd(MEKEY));
    if (!c || !GM()) { pending = false; return; }
    GM().api('/characters/' + c.id, { method: 'PUT', body: Object.assign({}, c, { level: lv }) }).then(r => {
      const s = ((r.me && r.me.characters) || []).find(x => x.id === c.id);
      if (s && s.level === lvOf(rd(MEKEY))) pending = false; else saveLvl();
      GM().took(r);
    }, () => { pending = false; });
  }, 1500);
}

function renderLvl() {
  const m = rd(MEKEY), lv = lvOf(m), raceF = P.racef[m.race], fac = raceF || ps.fac;
  $('#pWho').textContent = P.rn[m.race] || P.cn[m.cls] ? [P.rn[m.race], P.cn[m.cls], TX[raceF]].filter(Boolean).join(' · ') : TX.noHero;
  const cs = chars(), cur = curChar(), box = $('#pChars');
  box.hidden = !meNow;
  if (meNow) box.innerHTML = cs.length ? cs.map(c => `<button type="button" class="pill" data-c="${c.id}" aria-pressed="${c === cur}"><b>${esc(c.name)}</b>${c.level}</button>`).join('')
    : `<a href="${ROOT}profile/">${esc(TX.addChar)}</a>`;
  $('#level .phero a').href = meNow ? ROOT + 'profile/' : ROOT + '#me';
  $('#pFac').hidden = !!raceF;
  document.querySelectorAll('#pFac button').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.f === fac)));
  $('#lvOut').textContent = lv || '—';
  $('#dgLv').textContent = lv || '…';
  if (!lv) {
    $('#pNow').innerHTML = `<p class="pnote">${esc(TX.needLvl)}</p>`;
    $('#pDg').innerHTML = `<li class="pnote">${esc(TX.needLvl)}</li>`;
    return;
  }
  const route = P.route[fac], nx = route.find(r => r[0] > lv), ms = P.miles.find(x => x[0] >= lv);
  let h = route.filter(r => lv >= r[0] && lv <= r[1]).map(r => `<div class="pnow"><span class="lvl gold">${r[0]}–${r[1]}</span><p>${esc(r[2])}</p></div>`).join('');
  const next = (nx ? `<li><b>${TX.from} ${nx[0]}</b>${esc(nx[2])}</li>` : '') + (ms ? `<li><b>${ms[0] === lv ? TX.now : TX.at + ' ' + ms[0]}</b>${esc(ms[1])}</li>` : '');
  if (next) h += `<h3 class="ph">${TX.next}</h3><ul class="pnext">${next}</ul>`;
  $('#pNow').innerHTML = h;
  const dg = DUNGEONS.filter(d => nearLvl(d, lv) && (!d[6] || d[6] === fac))
    .sort((a, b) => Math.abs(a[1] + a[2] - 2 * lv) - Math.abs(b[1] + b[2] - 2 * lv)).slice(0, 6).sort((a, b) => a[1] - b[1] || a[2] - b[2]);
  $('#pDg').innerHTML = dg.length ? dg.map(d => `<li><span><b>${esc(d[0])}</b>${d[4] ? ` <span class="tag new">${TX.new}</span>` : ''}<small>${esc(d[3])}</small></span>`
    + `<span class="lvl${lv >= d[1] && lv <= d[2] ? ' gold' : ''}">${lvRange(d)}</span></li>`).join('') : `<li class="pnote">${TX.dungNone}</li>`;
}
$('#lvDown').addEventListener('click', () => setLvl((lvOf(rd(MEKEY)) || 2) - 1));
$('#lvUp').addEventListener('click', () => setLvl(lvOf(rd(MEKEY)) + 1));
$('#pChars').addEventListener('click', e => {
  const b = e.target.closest('button[data-c]'), c = b && chars().find(x => String(x.id) === b.dataset.c);
  if (!c) return;
  clearTimeout(saveT); pending = false;
  ps.char = c.id; saveP(); useChar(c); renderLvl();
});
$('#pFac').addEventListener('click', e => { const b = e.target.closest('button'); if (b) { ps.fac = b.dataset.f; saveP(); renderLvl(); } });
addEventListener('keydown', e => {   // + / − on the keyboard: level up or down, outside text fields
  if (e.ctrlKey || e.metaKey || e.altKey || e.target.closest('input, textarea, select')) return;
  if (e.key === '+' || e.key === '=') setLvl(lvOf(rd(MEKEY)) + 1);
  else if (e.key === '-' || e.key === '_') setLvl((lvOf(rd(MEKEY)) || 2) - 1);
});
addEventListener('storage', e => { if (e.key === MEKEY) renderLvl(); });
renderLvl();

/* A guest gets one line with the login; a signed-in player has the characters in the level block already */
function renderWay() {
  const w = $('#pWay');
  w.hidden = !!meNow;
  if (!meNow) w.innerHTML = `<p class="pnote">${esc(TX.guest)}</p><a class="btn" href="${ROOT}profile/">${esc(TX.login)}</a>`;
}
function gotMe(m) {
  if (!m && GM().logged()) return;   // signed in on this device: wait for the profile, no guest line in between
  meNow = m;
  const c = curChar();
  if (c && firstMe) {   // the level played here as a guest of the same hero is newer than the profile: keep it and save it
    const h = rd(MEKEY);
    if (h.race === c.race && h.cls === c.class && lvOf(h) > c.level) { c.level = lvOf(h); pending = true; saveLvl(); }
  }
  if (c) { if (pending) c.level = lvOf(rd(MEKEY)); else useChar(c); }
  if (m) firstMe = false;
  renderLvl(); renderWay();
}
function hookMe() { if (!GM()) return false; GM().onMe(gotMe); GM().me(); return true; }
if (!hookMe()) addEventListener('load', hookMe, { once: true });

/* Timers: the end time is stored, so they keep going after a reload. When one ends: three beeps, a blinking tab title
   and, if the visitor asked for it, a notification while the tab is in the background */
let actx = null;
function unlock() {   // the sound context has to start from a tap or a key
  try { actx = actx || new (window.AudioContext || window.webkitAudioContext)(); if (actx.state === 'suspended') actx.resume(); } catch (e) {}
}
function beep() {
  if (!actx) return;
  [0, .35, .7].forEach(t => {
    const o = actx.createOscillator(), g = actx.createGain(), s = actx.currentTime + t;
    o.frequency.value = 880; o.connect(g).connect(actx.destination);
    g.gain.setValueAtTime(.0001, s); g.gain.exponentialRampToValueAtTime(.3, s + .02); g.gain.exponentialRampToValueAtTime(.0001, s + .25);
    o.start(s); o.stop(s + .3);
  });
}
function notify(x) {
  if (!ps.notify || !document.hidden || !('Notification' in window) || Notification.permission !== 'granted') return;
  const opt = { body: TX.done, icon: ROOT + 'assets/icons/icon-192.png', tag: 'play-' + x.id };
  try { new Notification(x.name, opt); }
  catch (e) { if (navigator.serviceWorker) navigator.serviceWorker.ready.then(r => r.showNotification(x.name, opt)).catch(() => {}); }
}
const fmtT = ms => {
  const s = Math.max(0, Math.ceil(ms / 1000)), m = Math.floor(s / 60), ss = String(s % 60).padStart(2, '0');
  return m >= 60 ? `${Math.floor(m / 60)}:${String(m % 60).padStart(2, '0')}:${ss}` : `${m}:${ss}`;
};
const AGAIN = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 11a8 8 0 1 0-2.3 5.7M20 4v7h-7"/></svg>';
function renderTimers() {
  $('#tList').innerHTML = ps.timers.length ? ps.timers.map(x => `<li data-id="${esc(x.id)}"><span class="tn">${esc(x.name)}</span><span class="tt"></span>`
    + `<button type="button" class="iconbtn" data-act="again" aria-label="${esc(TX.again)}: ${esc(x.name)}">${AGAIN}</button>`
    + `<button type="button" class="iconbtn" data-act="rm" aria-label="${esc(TX.remove)}: ${esc(x.name)}"><svg class="ico" aria-hidden="true"><use href="#i-x"/></svg></button></li>`).join('')
    : `<li class="pnote">${esc(TX.noTimers)}</li>`;
  tick();
}
const baseTitle = document.title;
let blink = false;
function tick() {
  const now = Date.now();
  let soonest = Infinity, rung = null, changed = false;
  ps.timers.forEach(x => {
    const left = x.end - now;
    if (left <= 0 && !x.rang) { x.rang = true; changed = true; beep(); notify(x); }
    if (left > 0) soonest = Math.min(soonest, left); else rung = rung || x;
    const li = document.querySelector(`#tList li[data-id="${CSS.escape(x.id)}"]`);
    if (li) { li.classList.toggle('done', left <= 0); li.querySelector('.tt').textContent = left > 0 ? fmtT(left) : TX.done; }
  });
  if (changed) saveP();
  blink = !blink;
  document.title = rung ? (document.hidden && blink ? `⏰ ${TX.done}` : `⏰ ${rung.name} · ${baseTitle}`)
    : soonest < Infinity ? `${fmtT(soonest)} · ${baseTitle}` : baseTitle;
}
function addTimer(name, min) {
  unlock();
  ps.timers.push({ id: Date.now().toString(36) + Math.random().toString(36).slice(2, 6), name, min, end: Date.now() + min * 60000, rang: false });
  saveP(); renderTimers();
}
ps.timers.forEach(x => { if (x.end < Date.now() - 60000) x.rang = true; });   // ended while the page was closed: no beep now
$('#tPre').addEventListener('click', e => {
  const b = e.target.closest('button[data-min]');
  if (b) addTimer(b.dataset.name || `${b.dataset.min} ${TX.min}`, +b.dataset.min);
});
$('#tForm').addEventListener('submit', e => {
  e.preventDefault();
  const min = parseInt($('#tMin').value, 10);
  if (!(min >= 1 && min <= 600)) { $('#tMin').focus(); return; }
  addTimer($('#tName').value.trim() || `${TX.timer} · ${min} ${TX.min}`, min);
  $('#tName').value = ''; $('#tMin').value = '';
});
$('#tList').addEventListener('click', e => {
  const b = e.target.closest('button[data-act]');
  if (!b) return;
  const id = b.closest('li').dataset.id, x = ps.timers.find(t => t.id === id);
  if (!x) return;
  if (b.dataset.act === 'again') { unlock(); x.end = Date.now() + x.min * 60000; x.rang = false; }
  else ps.timers = ps.timers.filter(t => t !== x);
  saveP(); renderTimers();
});
addEventListener('pointerdown', unlock, { once: true });
const nBox = $('#tNotify'), nIn = nBox.querySelector('input');
if ('Notification' in window) {
  nBox.hidden = false;
  nIn.checked = ps.notify && Notification.permission === 'granted';
  nIn.addEventListener('change', () => {
    if (!nIn.checked) { ps.notify = false; saveP(); return; }
    Promise.resolve(Notification.requestPermission()).then(p => { ps.notify = p === 'granted'; nIn.checked = ps.notify; saveP(); });
  });
}
renderTimers();
setInterval(tick, 500);

/* Keep the screen on (a phone or tablet next to the keyboard); the browser drops the lock when the tab is hidden */
const wb = $('#wakeBtn');
let wl = null, wantWake = false;
const paintWake = () => wb.setAttribute('aria-pressed', String(wantWake));
function lock() {
  navigator.wakeLock.request('screen').then(l => { wl = l; l.addEventListener('release', () => { wl = null; }); }, () => { wantWake = false; paintWake(); });
}
if ('wakeLock' in navigator) {
  wb.hidden = false;
  wb.addEventListener('click', () => { wantWake = !wantWake; paintWake(); if (wantWake) lock(); else if (wl) wl.release(); });
  document.addEventListener('visibilitychange', () => { if (wantWake && !wl && document.visibilityState === 'visible') lock(); });
}'''

DATA = {'dungeons': dungeons_data, 'play': play_data}   # js key -> data blocks (from index.src.html and content)
REF = ('classref', 'raceref')        # js keys fed by ref_js (language-specific)


def page_ids(g):
    """Every id a guide puts on its page: sections, FAQ questions, raw blocks."""
    ids = [s['id'] for s in g['sections']]
    def walk(blocks):
        for k, d in blocks:
            if k == 'faq':
                ids.extend(q['id'] for q in d)
            elif k == 'tabs':
                for x in d:
                    walk(x['blocks'])
            elif k == 'raw':
                html = next(iter(d.values())) if isinstance(d, dict) else d   # raw ids are the same in every language
                ids.extend(re.findall(r'\sid="([^"]+)"', html))
    for s in g['sections']:
        walk(s['blocks'])
    return ids


def build_page(g, lang, tpl, base_css, sprite, src):
    sub = g['path'] if 'path' in g else (f'guides/{g["slug"]}/' if g['slug'] else 'guides/')   # path: classes/, races/, privacy/, '' (404)
    here = page_dir(lang, sub)
    html = tpl.replace('@@BASE_CSS@@', base_css).replace('@@SPRITE@@', sprite)
    nav = (g['path'] if g['path'] in ('classes/', 'races/', 'play/') else None) if 'path' in g else         (sub if g['slug'] in ('leveling', 'dungeons') else 'guides/')   # privacy, 404: no current item
    html = build.chrome(html, nav=nav, tab={'play': 'play/'}.get(g['slug']) if 'path' in g else 'guides/')
    if g.get('hero'):                                             # own full-screen scene instead of the art band
        html = re.sub(r'<section class="stband ghero" id="top">.*?</section>', lambda mt: thero(mt.group(0), g['hero']), html, count=1, flags=re.S)
    html, missing = translate(html, lang)                       # 1) обвязка
    root = rel(here, page_dir(lang))
    toc, body = render_guide(g, lang, root) if g['slug'] else hub_body(lang, root)
    if g.get('compact'):                                          # /play/: small heading instead of the art band
        html = re.sub(r'<section class="stband ghero" id="top">.*?</section>', lambda _: play_head(lang), html, count=1, flags=re.S)
        html = html.replace('<body>', '<body class="compact">', 1).replace('<main class="wrap gbody', '<main class="wrap gbody play', 1)
        body = play_body(lang, root)
    if g is NOT_FOUND:
        body += hub_body(lang, root)[1]                           # 404: every section of the guide as tiles
    if len(g.get('sections', ())) == 1:
        toc = ''                                                 # one section: no contents column
    section = 'path' in g                                         # classes/, races/, privacy/: not a guide
    if not g.get('more', True):
        others, more = [], ''
    elif section:
        others = [x for x in section_tiles() if x['href'] != g['path']] + SITE_TILES
        more = tile_links(others, lang, root)
    else:
        others = [x for x in lang_guides(lang) if x['slug'] != g['slug']] if g['slug'] else []
        more = tile_links(guide_tiles(others), lang, root)
    avif, webp, img = art_sets(g['art'], '@@ROOT@@', big=True)
    crumb = (f'<a href="{root}guides/">{E(HUB["title"], lang)}</a><span aria-hidden="true">/</span><span>{E(g["title"], lang)}</span>'
             if g['slug'] and not section else f'<span>{E(g["title"], lang)}</span>')
    toc_grp = f'<div class="grp"><div class="gh">{THIS_PAGE[lang]}</div>{toc}</div>' if toc else ''
    js = g.get('js')
    fx_attr = f' data-fx="{FX[g["art"]]}"' if g['art'] in FX else ''
    rep = {
        'HERO': ('@@TOD_HERO@@' if g['art'] == 'hero_dawn' else   # the leveling guide: the hero in the reader's time of day (tod.py)
                 f'<picture class="stband-art{"" if g["art"] in WIDTHS else " por"}" aria-hidden="true"{fx_attr}><source type="image/avif" srcset="{avif}" sizes="100vw">'
                 f'<img src="{img}" srcset="{webp}" sizes="100vw" alt="" decoding="async" fetchpriority="high"></picture>'),
        'TITLE': E(g['title'], lang), 'LEAD': E(g['lead'], lang), 'CRUMB': crumb,
        'PILLS': ' · '.join(E(p, lang) for p in g.get('pills', [])),   # one line of facts under the lead, no badges
        'TOC': toc, 'TOC_GRP': toc_grp, 'BODY': body, 'MORE': more,
        'SOLO': '' if toc else ' solo', 'MORE_H': (MORE_SITE if section else MORE_H)[lang],
        'SOURCES': ''.join(f'<li><a href="{u}" target="_blank" rel="noopener">{E(n, lang)}</a></li>' for n, u in g.get('sources', [])),
        'JS': ((build.js_names(DATA[js](src, lang), lang) + '\n' if js in DATA else ref_js(src, lang) + '\n' if js in REF else '') + L(JS[js], lang)) if js else '',
    }
    for k, v in rep.items():                                     # 2) тело
        html = html.replace(f'@@{k}@@', v)
    html = build.set_updated(html, sub)
    html = tod.apply(html, lang, root='@@ROOT@@', cls='stband-art', fx='dawn', mobile=True,
                     widths=WIDTHS['hero_dawn'], sizes='100vw', img_w=1920, img_h=1072, msizes='78vh')
    html = html.replace('\n    @@TOD_SW@@', '', 1)                # other guides: no switch
    if 'data-tod-art' in html:
        html = html.replace('</head>', '<link rel="stylesheet" href="@@ROOT@@assets/tod/tod.css" media="print" onload="this.media=\'all\'">\n</head>', 1)
        html = html.replace('</body>', '<script src="@@ROOT@@assets/tod/tod.js" defer></script>\n</body>', 1)
    if not others:
        html = html.replace('<section id="more">', '<section id="more" hidden>')
    if not g.get('sources'):                                     # privacy, 404: footer without the sources list
        html = re.sub(r'<!--src-->.*?<!--/src-->', '', html, flags=re.S)
    html = html.replace('<!--src-->', '').replace('<!--/src-->', '')
    html = html.replace('@@HOME@@', root)
    html = build.static_links(html, lang, root)
    if LAUNCH_UTC in html:                                       # launch time: also in the reader's time zone
        html = re.sub(rf'{LAUNCH_UTC}(?=\.</(?:td|p)>)', f'<time class="lt" datetime="2026-11-04T23:00:00Z">{LAUNCH_UTC}</time>', html)
        html = html.replace('</body>', LOCAL_JS.replace('@@YOUR@@', YOUR[lang]) + '</body>', 1)
    if g['art'] in FX or g.get('hero'):
        html = html.replace('</body>', '<script src="@@ROOT@@assets/living/living.js" defer></script>\n</body>', 1)
    html = html.replace('@@CANON@@', SITE + here)
    html = html.replace('@@ALTERNATES@@', build.alternates(sub))
    html = localize(html, lang, here).replace('assets/og.png', f'assets/og/{g.get("og") or g["slug"] or "guides"}-{lang}.jpg')   # tools/make_og.py
    return here + 'index.html', html, missing


NOT_FOUND_JS = r"""<script>
(function () {
  var m = location.pathname.match(/^\/wow\/(@@L@@)\//);
  if (!m) return;
  document.documentElement.style.visibility = 'hidden';
  try { sessionStorage.setItem('gabella-404', location.pathname + location.search + location.hash); } catch (e) {}
  location.replace('/wow/' + m[1] + '/404.html');
})();
</script>
"""
# <lang>/404.html: back to the address the reader typed (the root 404 sent them here)
NOT_FOUND_BACK = r"""<script>
try { var p = sessionStorage.getItem('gabella-404'); if (p) { sessionStorage.removeItem('gabella-404'); history.replaceState(null, '', p); } } catch (e) {}
</script>
"""


def not_found_page(tpl, base_css, sprite, src, lang='ru'):
    """404.html: the Russian page built at the guide root, served by GitHub Pages at any depth under /wow/ —
    <base> keeps its relative links working, and it is neither indexed nor canonical.
    <lang>/404.html: the same page per language; under /wow/<lang>/ the root one sends the reader there before it draws
    (a new document, not document.write over the old one: its scripts would clash with the first page's globals)."""
    _, html, missing = build_page(NOT_FOUND, lang, tpl, base_css, sprite, src)
    html = re.sub(r'<link rel="(canonical|alternate)"[^>]*>\n', '', html)
    html = re.sub(r'<meta property="og:[^>]*>\n', '', html)
    js = NOT_FOUND_JS.replace('@@L@@', '|'.join(l for l in LANGS if l != 'ru')) if lang == 'ru' else NOT_FOUND_BACK
    html = html.replace('<head>', f'<head>\n<base href="/wow/{page_dir(lang)}">\n<meta name="robots" content="noindex">', 1)
    html = html.replace('<meta charset="utf-8">\n', '<meta charset="utf-8">\n' + js, 1)
    html = html.replace('data-page=""', 'data-page="404"', 1)   # me.js: the secret for getting lost
    return page_dir(lang, '404.html'), html, missing


def main():
    gaps = (check_langs(HUB, 'HUB') + [p for g in GUIDES + HUBS + PAGES + [NOT_FOUND] for p in check_langs(g, g['slug'])]
            + check_langs(NEWS, 'NEWS') + check_langs(SITE_TILES, 'SITE_TILES')
            + check_langs(PLAY_TX, 'PLAY_TX') + check_langs(PLAY_MILESTONES, 'PLAY_MILESTONES'))
    assert not gaps, gaps[:10]
    src = open(os.path.join(HERE, 'index.src.html'), encoding='utf-8').read()
    tpl = open(os.path.join(HERE, 'guide.src.html'), encoding='utf-8').read()
    base_css = src[src.index('<style>') + 7:src.index('</style>')].strip('\n')
    s0 = src.index('<svg width="0" height="0"')
    sprite = src[s0:src.index('</svg>', s0) + 6]

    pages, allmissing = [], []
    for lang in LANGS:
        for g in [HUB] + lang_guides(lang) + HUBS + PAGES:
            path, html, missing = build_page(g, lang, tpl, base_css, sprite, src)
            assert '@@' not in html, (path, re.findall(r'@@\w+@@', html)[:5])
            pages.append((path, html))
            allmissing += missing
    for lang in LANGS:
        path, html, missing = not_found_page(tpl, base_css, sprite, src, lang)
        assert '@@' not in html, (path, re.findall(r'@@\w+@@', html)[:5])
        pages.append((path, html))
        allmissing += missing

    listing = '--list' in sys.argv
    if not listing:
        for path, html in pages:
            full = os.path.join(HERE, path)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            open(full, 'w', encoding='utf-8', newline='\n').write(html)
    uniq = list(dict.fromkeys(allmissing))
    if listing and '--missing' not in sys.argv:
        print('\n'.join(uniq))
    print(f'guides: {len(pages)}, missing: {len(uniq)}', file=sys.stderr)
    if uniq and not listing:
        sys.exit(1)


if __name__ == '__main__':
    main()
