"""Сборка гида: index.src.html, class.src.html, race.src.html (русские исходники) + content/classes.py, content/races.py
+ i18n/{ru,en,uk}.txt (переводы, строка в строку)
-> index.html, en/index.html, uk/index.html, classes/<id>/index.html и races/<slug>/index.html на трёх языках.
Запуск: python build.py [--list]  (--list печатает русские фрагменты без перевода)"""
import hashlib, json, os, posixpath, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
if '--missing' in sys.argv:          # python build.py --missing de: build de without its json, print what it lacks, write nothing
    os.environ['WF_LANG'] = sys.argv[sys.argv.index('--missing') + 1]
    sys.argv.append('--list')
sys.path.insert(0, os.path.join(HERE, 'content'))
from classes import CLASSES, SOURCES  # noqa: E402
from races import RACES_PAGE, SOURCES as RACE_SOURCES, NEW_RACIALS  # noqa: E402
import langs  # noqa: E402
from langs import LANGS, AUTONYM, HREFLANG, LOCALE, NAMED  # noqa: E402


def load(name):
    with open(os.path.join(HERE, 'i18n', name), encoding='utf-8') as f:
        return f.read().splitlines()


_ru, _en, _uk = load('ru.txt'), load('en.txt'), load('uk.txt')
assert len(_ru) == len(_en) == len(_uk), (len(_ru), len(_en), len(_uk))
T = {r: (e, u) for r, e, u in zip(_ru, _en, _uk)}

CYR = r'А-Яа-яЁё'
SEG = re.compile(r'(?:(?!\$\{)[^<>"\'`{}\n])*[' + CYR + r'](?:(?!\$\{)[^<>"\'`{}\n])*')
SITE = 'https://gabella.site/wow/'


def t_of(ru, lang):
    """Translation of a Russian fragment known to T: en/uk from the line files, new languages via the English one."""
    en, uk = T[ru]
    return en if lang == 'en' else uk if lang == 'uk' else langs.ov(en, lang)


def split_ws(seg):
    core = seg.strip()
    i = seg.index(core)
    return seg[:i], core, seg[i + len(core):]


def translate(src, lang):
    missing = []

    def sub(m):
        lead, core, tail = split_ws(m.group(0))
        if lang == 'ru':
            return m.group(0)
        if core not in T:
            missing.append(core)
            return m.group(0)
        return lead + t_of(core, lang) + tail
    return SEG.sub(sub, src), missing


def tr(s, lang):
    return s if lang == 'ru' or s not in T else t_of(s, lang)


def page_dir(lang, sub=''):
    """Site-relative directory of a page, e.g. 'en/classes/mage/'."""
    return ('' if lang == 'ru' else lang + '/') + sub


def rel(from_dir, to_dir):
    r = posixpath.relpath(to_dir or '.', from_dir.rstrip('/') or '.')
    return './' if r == '.' else r + '/'


CONTACT = 'contact@gabella.site'   # Cloudflare Email Routing -> почта Вячеслава
LEGAL = {
    'ru': ('Фанатский гид Gabella. Сайт не связан с Blizzard Entertainment и не одобрен ею. World of Warcraft, Warcraft и Blizzard Entertainment — '
           'товарные знаки или зарегистрированные товарные знаки Blizzard Entertainment, Inc. в США и/или других странах.', 'Конфиденциальность', 'Связь', 'Карта сайта'),
    'en': ('Gabella fan guide. Not affiliated with or endorsed by Blizzard Entertainment. World of Warcraft, Warcraft and Blizzard Entertainment are '
           'trademarks or registered trademarks of Blizzard Entertainment, Inc. in the U.S. and/or other countries.', 'Privacy', 'Contact', 'Site map'),
    'uk': ('Фанатський гід Gabella. Сайт не пов’язаний з Blizzard Entertainment і не схвалений нею. World of Warcraft, Warcraft і Blizzard Entertainment — '
           'торгові марки або зареєстровані торгові марки Blizzard Entertainment, Inc. у США та/або інших країнах.', 'Конфіденційність', 'Зв’язок', 'Мапа сайту'),
}


langs.derive(LEGAL)


TOOLS_T = langs.derive({'ru': 'Инструменты', 'en': 'Tools', 'uk': 'Інструменти'})


def site_map(lang, home):
    """Footer site map of every page: classes, races, guides, tools. home: path to the language home."""
    from content.guides import GUIDES, HUB, HUBS, ORDER, PLAY
    langs.fill([HUB, HUBS, PLAY] + GUIDES)
    if not _RACES:
        _RACES.extend(parse_races(open(os.path.join(HERE, 'index.src.html'), encoding='utf-8').read()))
    slug = {r['id']: r['slug'] for r in RACES_PAGE}
    hub = {h['slug']: h for h in HUBS}
    guides = sorted(GUIDES, key=lambda g: ORDER.index(g['slug']) if g['slug'] in ORDER else len(ORDER))
    cols = [
        (hub['classes']['title'], 'classes/', [(f'classes/{c["id"]}/', tr(c['n'], lang)) for c in CLASSES]),
        (hub['races']['title'], 'races/', [(f'races/{slug[r["id"]]}/', tr(r['n'], lang)) for r in _RACES]),
        (HUB['title'], 'guides/', [(f'guides/{g["slug"]}/', g['title'][lang]) for g in guides]),
        (TOOLS_T, 'tools/', [('tools/', TOOLS_T[lang]), ('play/', PLAY['title'][lang])]),
    ]
    out = ''.join(f'<div><a class="fh" href="{home}{href}">{esc(h[lang])}</a><ul>'
                  + ''.join(f'<li><a href="{home}{u}">{esc(n)}</a></li>' for u, n in links) + '</ul></div>'
                  for h, href, links in cols)
    return f'<nav class="fmap" aria-label="{esc(LEGAL[lang][3])}">{out}</nav>'


def legal(lang, root):
    """Footer block of every page (@@LEGAL@@): site map, trademarks, ©, privacy page, contact."""
    text, privacy, contact = LEGAL[lang][:3]
    return site_map(lang, root + page_dir(lang)) + (f'<div class="legal"><p>{text}</p><p>© 2026 Gabella<span aria-hidden="true"> · </span>'
            f'<a href="{root}{page_dir(lang, "privacy/")}">{privacy}</a><span aria-hidden="true"> · </span>'
            f'{contact}: <a href="mailto:{CONTACT}">{CONTACT}</a></p></div>')


def alternates(sub):
    """hreflang links of a page (site-relative directory sub, '' = home) in every built language; x-default = Russian."""
    alt = '\n'.join(f'<link rel="alternate" hreflang="{HREFLANG[l]}" href="{SITE}{page_dir(l, sub)}">' for l in LANGS)
    return alt + f'\n<link rel="alternate" hreflang="x-default" href="{SITE}{sub}">'


# Browser-language hint, in the visitor's language: (text, link, close button)
HINT = {
    'ru': ('Эта страница есть на русском', 'Читать по-русски', 'Закрыть'),
    'en': ('This page is available in English', 'Read in English', 'Close'),
    'uk': ('Ця сторінка є українською', 'Читати українською', 'Закрити'),
    'de': ('Diese Seite gibt es auch auf Deutsch', 'Auf Deutsch lesen', 'Schließen'),
    'fr': ('Cette page existe aussi en français', 'Lire en français', 'Fermer'),
    'es': ('Esta página también está en español', 'Leer en español', 'Cerrar'),
    'pt': ('Esta página também está em português', 'Ler em português', 'Fechar'),
    'it': ('Questa pagina è disponibile anche in italiano', 'Leggi in italiano', 'Chiudi'),
    'pl': ('Ta strona jest dostępna po polsku', 'Czytaj po polsku', 'Zamknij'),
}

LANG_JS = """<script>
(() => {
  const KEY = 'gabella-lang-hint', store = l => { try { localStorage.setItem(KEY, '1'); if (l) localStorage.setItem('gabella-lang', l); } catch (e) {} };
  const keepHash = a => a.addEventListener('click', () => { store(a.dataset.lang); a.href = a.getAttribute('href').split('#')[0] + location.hash; });
  document.querySelectorAll('.langlist a, .langgrid a').forEach(keepHash);
  const sel = document.querySelector('.langsel'), btn = sel && sel.querySelector('.langbtn'), list = sel && sel.querySelector('.langlist');
  if (btn) {
    const links = [...list.querySelectorAll('a')];
    const shut = focus => { if (list.hidden) return; list.hidden = true; btn.setAttribute('aria-expanded', 'false'); if (focus) btn.focus(); };
    btn.addEventListener('click', e => {
      e.stopPropagation();
      list.hidden = !list.hidden; btn.setAttribute('aria-expanded', String(!list.hidden));
      if (!list.hidden) (list.querySelector('[aria-current]') || links[0]).focus();
    });
    document.addEventListener('click', e => { if (!sel.contains(e.target)) shut(); });
    sel.addEventListener('keydown', e => {
      if (e.key === 'Escape') return shut(true);
      const i = links.indexOf(document.activeElement);
      if (i < 0 || !['ArrowDown', 'ArrowUp', 'Home', 'End'].includes(e.key)) return;
      e.preventDefault();
      const n = e.key === 'Home' ? 0 : e.key === 'End' ? links.length - 1 : (i + (e.key === 'ArrowDown' ? 1 : -1) + links.length) % links.length;
      links[n].focus();
    });
    sel.addEventListener('focusout', e => { if (!sel.contains(e.relatedTarget)) shut(); });
  }
  let seen = '1';
  try { seen = localStorage.getItem(KEY); } catch (e) {}
  if (seen) return;
  const H = @@HINT@@, cur = document.documentElement.lang.split('-')[0];
  const want = (navigator.languages || [navigator.language]).map(x => String(x || '').toLowerCase().split('-')[0]).find(x => x in H);
  const to = want && want !== cur && document.querySelector(`.langlist a[data-lang="${want}"]`);
  if (!to) return;
  const bar = document.createElement('div');
  bar.className = 'langhint'; bar.lang = want; bar.setAttribute('role', 'status');
  bar.innerHTML = `<span>${H[want][0]}</span><a href="${to.getAttribute('href')}" hreflang="${to.hreflang}" data-lang="${want}">${H[want][1]}</a>`
    + `<button type="button" aria-label="${H[want][2]}"><svg class="ico" aria-hidden="true"><use href="#i-x"/></svg></button>`;
  keepHash(bar.querySelector('a'));
  bar.querySelector('button').addEventListener('click', () => { store(); bar.remove(); });
  document.body.append(bar);
})();
</script>
"""

# Root /wow/ only: the visitor's language before the page draws. A saved choice (gabella-lang, set by the language menu
# here and on the hub) wins; otherwise the browser languages, English for the rest. Bots, search results and links
# from inside the site stay on the Russian page, so search engines index it as is.
AUTO_JS = r"""<script>
(function () {
  if (window.wfMoved || /bot|crawl|spider|slurp|lighthouse|headless|google-|preview/i.test(navigator.userAgent) || navigator.webdriver) return;
  var P = @@PATHS@@, A = { be: 'ru', kk: 'ru' }, w = null, r = document.referrer;
  try { w = localStorage.getItem('gabella-lang'); } catch (e) {}
  if (!(w in P)) {
    if (r && (r.indexOf(location.origin + '/') === 0 || /^https?:\/\/([^\/]*\.)?(google|bing|yandex|ya|duckduckgo|yahoo|baidu|ecosia|naver|qwant|seznam)\.[^\/]+\//.test(r))) return;
    var L = navigator.languages || [navigator.language];
    for (var i = 0; i < L.length && !w; i++) { var b = String(L[i] || '').toLowerCase().split('-')[0]; b = A[b] || b; if (b in P) w = b; }
    w = w || 'en';
  }
  if (w !== 'ru') location.replace(P[w] + location.search + location.hash);
})();
</script>
"""


def auto_lang(html):
    paths = json.dumps({l: page_dir(l) or './' for l in LANGS})
    return html.replace('<meta name="viewport"', AUTO_JS.replace('@@PATHS@@', paths) + '<meta name="viewport"', 1)


def lang_menu(html, lang, here):
    """@@LANGSEL@@ (top bar: button + dropdown list) and @@LANGSHEET@@ (phone sheet: 3x3 grid) — the same page in every language."""
    sub = here[len(page_dir(lang)):]
    label = tr('Язык', lang)
    def link(l, inner):
        cur = ' aria-current="page"' if l == lang else ''
        return f'<a href="{rel(here, page_dir(l, sub))}" data-lang="{l}" hreflang="{HREFLANG[l]}" lang="{HREFLANG[l]}"{cur}>{inner}</a>'
    items = ''.join(f'<li>{link(l, f"<span>{AUTONYM[l]}</span><small>{l.upper()}</small>")}</li>' for l in LANGS)
    sel = (f'<div class="langsel"><button type="button" class="langbtn" aria-haspopup="true" aria-expanded="false" '
           f'aria-label="{label}: {AUTONYM[lang]}">{lang.upper()}</button><ul class="langlist" hidden>{items}</ul></div>')
    sheet = f'<div class="langgrid" role="group" aria-label="{label}">{"".join(link(l, AUTONYM[l]) for l in LANGS)}</div>'
    hint = json.dumps({l: HINT[l] for l in LANGS}, ensure_ascii=False)
    return html.replace('@@LANGSEL@@', sel).replace('@@LANGSHEET@@', sheet).replace('</body>', LANG_JS.replace('@@HINT@@', hint) + '</body>', 1)


def localize(html, lang, here):
    """Language-specific attributes shared by all pages."""
    html = html.replace('@@LEGAL@@', legal(lang, rel(here, '')))
    html = html.replace('@@ROOT@@', rel(here, ''))
    html = lang_menu(html, lang, here)
    if lang != 'ru':
        html = html.replace('<html lang="ru">', f'<html lang="{HREFLANG[lang]}">')
        html = html.replace('content="ru_RU"', f'content="{LOCALE[lang]}"')
    if lang not in ('ru', 'uk'):                                  # Latin-script pages: preload the fonts they draw first
        html = html.replace('-cyrillic.woff2" as="font"', '-latin.woff2" as="font"')
    html = html.replace('</head>', REVEAL_CSS + '</head>', 1).replace('</body>', REVEAL_JS + '</body>', 1)
    return pwa(html, lang, rel(here, ''))


# Sections below the first screen fade in once when they scroll into view.
# Without JS, with reduced motion, in print or for what is already on screen nothing changes.
REVEAL_CSS = """<style>
.rv { opacity: 0; transform: translateY(18px); }
.rv.in { opacity: 1; transform: none; transition: opacity .6s var(--ease), transform .6s var(--ease); }
@media print { .rv { opacity: 1; transform: none; } }
</style>
"""
REVEAL_JS = """<script>
(function () {
  if (!('IntersectionObserver' in window) || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -6% 0px' });
  document.querySelectorAll('section.block, section.nband, section.stband:not(.ghero), .gsec, footer').forEach(function (s) {
    if (s.getBoundingClientRect().top > innerHeight) { s.classList.add('rv'); io.observe(s); }
  });
})();
</script>
"""


# ---------- installable site (PWA): manifest, icons, service worker sw.js ----------

APP = {
    'ru': {'name': 'WoW Forever — гид Gabella', 'desc': 'Классы, расы, подземелья, прокачка и сборка группы для WoW Forever.',
           'install': 'Установить', 'install_l': 'Установить гид как приложение',
           'short': [('В игре', 'play/'), ('Гайды', 'guides/'), ('Подземелья', 'guides/dungeons/'), ('Инструменты', 'tools/'), ('Классы', 'classes/')]},
    'en': {'name': 'WoW Forever — Gabella guide', 'desc': 'Classes, races, dungeons, leveling and party building for WoW Forever.',
           'install': 'Install', 'install_l': 'Install the guide as an app',
           'short': [('In game', 'play/'), ('Guides', 'guides/'), ('Dungeons', 'guides/dungeons/'), ('Tools', 'tools/'), ('Classes', 'classes/')]},
    'uk': {'name': 'WoW Forever — гід Gabella', 'desc': 'Класи, раси, підземелля, прокачування та збір групи для WoW Forever.',
           'install': 'Встановити', 'install_l': 'Встановити гід як застосунок',
           'short': [('У грі', 'play/'), ('Гайди', 'guides/'), ('Підземелля', 'guides/dungeons/'), ('Інструменти', 'tools/'), ('Класи', 'classes/')]},
}
langs.derive(APP)


def manifest(lang):
    a, home = APP[lang], page_dir(lang)
    icons = [{'src': f'assets/icons/icon-{s}.png', 'sizes': f'{s}x{s}', 'type': 'image/png', 'purpose': 'any'} for s in (192, 512)]
    icons.append({'src': 'assets/icons/icon-maskable-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'maskable'})
    return json.dumps({
        'id': './', 'name': a['name'], 'short_name': 'Gabella WoW', 'description': a['desc'], 'lang': HREFLANG[lang], 'dir': 'ltr',
        'start_url': './' + home, 'scope': './', 'display': 'standalone', 'orientation': 'any',
        'background_color': '#0a0b0d', 'theme_color': '#060708', 'categories': ['games', 'entertainment'], 'icons': icons,
        'shortcuts': [{'name': n, 'url': './' + home + u} for n, u in a['short']],
    }, ensure_ascii=False, indent=1)


PWA_JS = """<script>
if ('serviceWorker' in navigator) addEventListener('load', () => navigator.serviceWorker.register('@@R@@sw.js').catch(() => {}));
addEventListener('beforeinstallprompt', e => {
  e.preventDefault();
  const opts = document.querySelector('.sheet .opts');
  if (!opts || opts.querySelector('.installbtn')) return;
  const b = document.createElement('button');
  b.className = 'iconbtn installbtn'; b.type = 'button'; b.style.padding = '0 14px';
  b.setAttribute('aria-label', '@@L@@');
  b.innerHTML = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4v11m-5-5 5 5 5-5M5 20h14"/></svg><span>@@T@@</span>';
  b.onclick = async () => { e.prompt(); await e.userChoice; b.remove(); };
  opts.append(b);
});
</script>
"""


def sw_version():
    """sw.js VERSION = short hash of assets/ (without the news feed, the worker fetches it fresh) and the manifests."""
    h = hashlib.sha1()
    files = [os.path.join(d, f) for d, _, fs in os.walk(os.path.join(HERE, 'assets')) for f in fs if f != 'news.json']
    files += [os.path.join(HERE, f'manifest-{l}.webmanifest') for l in LANGS]
    for f in sorted(files):
        h.update(os.path.relpath(f, HERE).replace(os.sep, '/').encode())
        h.update(open(f, 'rb').read())
    sw = os.path.join(HERE, 'sw.js')
    assert '<<<<<<<' not in open(sw, encoding='utf-8').read(), 'sw.js: unresolved merge conflict'
    js = re.sub(r"const VERSION = '[^']*';", f"const VERSION = '{h.hexdigest()[:10]}';", open(sw, encoding='utf-8').read(), count=1)
    open(sw, 'w', encoding='utf-8', newline='\n').write(js)


RADIO = langs.derive({'ru': 'Радио', 'en': 'Radio', 'uk': 'Радіо'})
RADIO_BTN = ('<button class="iconbtn radiobtn" type="button" aria-label="@@L@@" title="@@L@@" aria-expanded="false" aria-controls="radioPanel" aria-pressed="false">'
             '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
             '<path d="M9 18V5l11-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="17" cy="16" r="3"/></svg>'
             '<span class="rdo-eq" aria-hidden="true"><i></i><i></i><i></i></span></button>\n    ')


SEARCH = {'ru': 'Поиск по сайту', 'en': 'Search the site', 'uk': 'Пошук по сайту', 'de': 'Seite durchsuchen', 'fr': 'Rechercher sur le site',
          'es': 'Buscar en el sitio', 'pt': 'Pesquisar no site', 'it': 'Cerca nel sito', 'pl': 'Szukaj w serwisie'}
SEARCH_BTN = ('<button class="iconbtn srchbtn" type="button" aria-label="@@L@@" aria-haspopup="dialog">'
              '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
              '<circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/></svg><kbd>Ctrl K</kbd></button>\n    ')


def search(html, lang, root):
    """Site search (assets/search/, search.py): button before the radio button, styles without blocking the page, script.
    search.py adds ?v=<hash> to both files after the index is written."""
    html = html.replace('<button class="iconbtn radiobtn"', SEARCH_BTN.replace('@@L@@', SEARCH[lang]) + '<button class="iconbtn radiobtn"', 1)
    head = f'<link rel="stylesheet" href="{root}assets/search/search.css" media="print" onload="this.media=\'all\'">\n</head>'
    js = f'<script src="{root}assets/search/search.js" data-root="{root}" defer></script>\n</body>'
    return html.replace('</head>', head, 1).replace('</body>', js, 1)


def radio(html, lang, root):
    """Radio (assets/radio/, tools/make_radio.py): button before the theme button of the top bar, styles without blocking the page, script."""
    html = html.replace('<button class="iconbtn themebtn"', RADIO_BTN.replace('@@L@@', RADIO[lang]) + '<button class="iconbtn themebtn"', 1)
    head = (f'<link rel="stylesheet" href="{root}assets/radio/radio.css" media="print" onload="this.media=\'all\'">\n</head>')
    js = f'<script src="{root}assets/radio/radio.js" data-root="{root}" defer></script>\n</body>'
    return html.replace('</head>', head, 1).replace('</body>', js, 1)


def pwa(html, lang, root):
    a = APP[lang]
    head = (f'<link rel="manifest" href="{root}manifest-{lang}.webmanifest">\n'
            f'<link rel="apple-touch-icon" href="{root}assets/icons/apple-touch-icon.png">\n'
            '<meta name="apple-mobile-web-app-title" content="Gabella WoW">\n</head>')
    js = PWA_JS.replace('@@R@@', root).replace('@@L@@', a['install_l']).replace('@@T@@', a['install'])
    return search(radio(html.replace('</head>', head, 1).replace('</body>', js + '</body>', 1), lang, root), lang, root)


# ---------- home page ----------

def upd_time(d):
    """'23.10.2026' -> <time> line of a guide card."""
    return f'<time datetime="{"-".join(reversed(d.split(".")))}">{d}</time>' if d else ''


def card_dates(html):
    """Update date at the bottom of the home guide cards (a.gt). The news feed refreshes itself, so its card has none."""
    from content.guides import GUIDES, HUBS
    dates = {f'guides/{g["slug"]}/': g.get('updated') for g in GUIDES if g['slug'] != 'news'} | {h['path']: h.get('updated') for h in HUBS}
    return re.sub(r'(<a class="gt" href="([^"#]+)">.*?)(</a>)', lambda m: m[1] + upd_time(dates.get(m[2])) + m[3], html)

def build_home(lang, src):
    src = src.replace('@@RACE_LEAD@@', json.dumps({r['id']: r['lead'] for r in RACES_PAGE}, ensure_ascii=False))
    src = src.replace('@@RACE_SLUG@@', json.dumps({r['id']: r['slug'] for r in RACES_PAGE}))
    html, missing = translate(src, lang)
    here = page_dir(lang)
    html = html.replace('@@ALTERNATES@@', alternates(''))
    html = localize(html, lang, here)
    html = static_links(html, lang, '')
    html = card_dates(html)
    html = home_dungeons(html, lang)
    if lang == 'ru':
        html = auto_lang(html)
    if lang != 'ru':
        for tag in ('rel="canonical" href', 'property="og:url" content'):
            html = html.replace(tag + f'="{SITE}"', tag + f'="{SITE}{lang}/"')
        html = html.replace('assets/og-ru.jpg', f'assets/og-{lang}.jpg')
    return here + 'index.html', html, missing


# ---------- class pages ----------

RACE_RX = re.compile(r"\{ id:'(\w+)', n:'([^']+)', f:'(\w+)'(, paid:true)?(?:, name:'([^']+)')?,\s*cls:\[([^\]]*)\]")
ROLE = {'tank': 'Танк', 'heal': 'Лекарь', 'dps': 'Урон', 'tank?': 'Танк (под вопросом)'}
COLOR = {'warrior': '#c79c6e', 'paladin': '#f58cba', 'hunter': '#abd473', 'rogue': '#fff569', 'priest': '#e8e8e8', 'shaman': '#2f8cf0', 'mage': '#40c7eb', 'warlock': '#8788ee', 'druid': '#ff7d0a'}


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


# soft hyphen points for long spec names: the engraved caps font is wide and three spec tabs share a phone screen
HYPH = {w.replace('-', ''): w.replace('-', '&shy;') for w in (
    'Совер-шен-ство-вание', 'Вдо-ско-на-лен-ня', 'Не-по-міт-ність', 'Не-ис-тов-ство', 'Де-мо-но-ло-гия', 'Де-мо-но-ло-гія',
    'Лик-ви-да-ция', 'Лік-ві-да-ція', 'Раз-ру-ше-ние', 'Руй-ну-ван-ня', 'По-слу-ша-ние', 'Кол-дов-ство', 'Скрыт-ность',
    'Assas-si-na-tion', 'Marks-man-ship', 'Retri-bu-tion', 'Resto-ra-tion', 'Destruc-tion', 'Enhance-ment',
    'Afflic-tion', 'Demo-no-lo-gy', 'Disci-pline', 'Protec-tion',
    'Tier-herr-schaft', 'Treff-sicher-heit', 'Wieder-her-stel-lung', 'Ver-stär-kung', 'Gleich-ge-wicht', 'Dä-mo-no-lo-gie',
    'Zer-stö-rung', 'Ver-gel-tung',
    'Amé-lio-ra-tion', 'Res-tau-ra-tion', 'Dé-mo-no-lo-gie', 'Élé-men-taire', 'Assas-si-nat',
    'Demo-no-lo-gía', 'Des-truc-ción', 'Res-tau-ra-ción', 'Super-vi-ven-cia', 'Repren-sión', 'Equi-li-brio', 'Protec-ción', 'Disci-pli-na',
    'Aper-fei-ço-a-men-to', 'Assas-si-na-to', 'Demo-no-lo-gia', 'Des-trui-ção', 'Equi-lí-brio', 'Res-tau-ra-ção', 'Retri-bui-ção',
    'Sobre-vi-vên-cia', 'Sub-ter-fú-gio',
    'Af-fli-zio-ne', 'Ag-gres-so-re', 'As-sas-si-nio', 'Com-bat-ti-men-to', 'Di-stru-zio-ne', 'Ele-men-ta-le', 'Po-ten-zia-men-to',
    'Pre-ci-sio-ne', 'Pro-te-zio-ne', 'Ri-ge-ne-ra-zio-ne', 'Scal-trez-za', 'So-prav-vi-ven-za')}


def hyph_tabs(html):
    return re.sub(r'(role="tab"[^>]*>)([^<]+)', lambda m: m[1] + HYPH.get(m[2], m[2]), html)


def mark_long(html):
    """Portrait cards: names with a 10+ letter word get class "long" and a smaller size (after translation, so every language)."""
    def name(m):
        return '<b class="long">' if max(len(w) for w in re.split(r'[\s-]+', m[1])) >= 10 else m[0]
    return re.sub(r'<a class="oc".*?</a>', lambda a: re.sub(r'<b>(?=([^<]+)</b>)', name, a[0]), html, flags=re.S)


def ability(ru, en, lang, tag='b'):
    """Ability name. ru: Russian + the English original; de/fr/es/pt/it: the official name (i18n/names.json, Wowhead)
    + English; en/uk/pl: English only. tag wraps the main name; '' = bare text (race cards put it in their own h3)."""
    main = ru if lang == 'ru' else langs.name(en, lang)
    if main == en:
        return f'<{tag or "span"} lang="en">{esc(en)}</{tag or "span"}>'
    head = f'<{tag}>{esc(main)}</{tag}>' if tag else esc(main)
    return f'{head}<span class="en" lang="en">{esc(en)}</span>'


JS_STR = re.compile(r"""'[^'\n]*'|"[^"\n]*\"""")
DG_ZONE = re.compile(r"""^(\s*\[(?:'[^'\n]*'|"[^"\n]*"), \d+, \d+, )('[^'\n]*'|"[^"\n]*")""", re.M)


def js_quote(s, q):
    return q + s.replace(q, '’') + q


def js_names(js, lang):
    """English game names in quoted JS data (dungeons, zones, cities) -> official localized ones on de/fr/es/pt/it.
    ru: only the entrance zone of DUNGEONS rows, as the Russian client names it + the English original
    («Тирисфальские леса (Tirisfal Glades)»); dungeon names stay English there."""
    if lang == 'ru':
        def zone(m):
            en = m[2][1:-1]
            ru = langs.NAMES.get(en, {}).get('ru')
            return m[1] + (js_quote(f'{ru} ({en})', m[2][0]) if ru else m[2])
        return DG_ZONE.sub(zone, js)
    if lang not in NAMED:
        return js
    return JS_STR.sub(lambda m: js_quote(langs.name(m[0][1:-1], lang), m[0][0]), js)


def home_dungeons(html, lang):
    """DUNGEONS on the home page: zone (and on de/fr/es/pt/it dungeon) names in the page language, as on the dungeon guide."""
    i = html.find('const DUNGEONS = [')
    if i < 0:
        return html
    j = html.index('\n];', i)
    return html[:i] + js_names(html[i:j], lang) + html[j:]


def ico(name):
    return f'<svg class="ico" aria-hidden="true"><use href="#i-{name}"/></svg>'


def ri(role):
    return f'<svg class="ri" aria-hidden="true"><use href="#i-{role.rstrip("?")}"/></svg>'


def parse_races(src):
    """RACES of the home page: classes, racial abilities [(a|p, name, what)] and the tip."""
    out = []
    block = src[src.index('const RACES = ['):]
    block = block[:block.index('\n];')]
    for m in RACE_RX.finditer(block):
        rid, n, fac, paid, name, cls = m.groups()
        can = {}
        for c in re.findall(r"'(\w+\*?)'", cls):
            can[c.rstrip('*')] = 'new' if c.endswith('*') else 'ok'
        rest = block[m.end():]
        nxt = RACE_RX.search(rest)
        body = rest[:nxt.start()] if nxt else rest
        rac = re.findall(r"\['([ap])','([^']+)','([^']+)'\]", body)
        tip = re.search(r"tip:'([^']+)'", body).group(1)
        out.append({'id': rid, 'n': name or n, 'f': fac, 'paid': bool(paid), 'can': can, 'rac': rac, 'tip': tip})
    return out


_RACES = []


def static_links(html, lang, home):
    """Plain links inside the class and race blocks the page script draws (home rosters, /classes/, /races/):
    the script replaces them, crawlers and readers without JS follow them."""
    if not _RACES:
        _RACES.extend(parse_races(open(os.path.join(HERE, 'index.src.html'), encoding='utf-8').read()))
    slug = {r['id']: r['slug'] for r in RACES_PAGE}
    cls = ''.join(f'<a href="{home}classes/{c["id"]}/">{esc(tr(c["n"], lang))}</a>' for c in CLASSES)
    rac = lambda f=None: ''.join(f'<a href="{home}races/{slug[r["id"]]}/">{esc(tr(r["n"], lang))}</a>' for r in _RACES if f in (None, r['f']))
    for box, links in (('roster', cls), ('classRef', cls), ('rosterA', rac('alliance')), ('rosterH', rac('horde')), ('raceRef', rac())):
        html = html.replace(f' id="{box}"></div>', f' id="{box}">{links}</div>', 1)
    return html


def parse_en(src):
    """English names of specs and racial abilities from the EN map of the home page."""
    block = src[src.index('const EN = {'):]
    block = block[:block.index('};')]
    return {ru: a or b for ru, a, b in re.findall(r"'([^']+)':(?:'([^']+)'|\"([^\"]+)\")", block)}


def pic(cid, root, widths, sizes, cls='', lazy=True):
    srcs = ''.join(f'<source type="image/{ext}" srcset="{", ".join(f"{root}assets/art/{cid}-{w}.{ext} {w}w" for w in widths)}" sizes="{sizes}">' for ext in ('avif', 'webp'))
    load = ' loading="lazy"' if lazy else ''
    return f'<picture{cls}>{srcs}<img src="{root}assets/art/{cid}-{widths[-1]}.webp" width="896" height="1200" alt=""{load} decoding="async"></picture>'


def render_class(c, races, lang):
    i = next(k for k, x in enumerate(CLASSES) if x['id'] == c['id'])
    roles = ''.join(f'<span class="{"q" if r.endswith("?") else ""}">{ri(r)}{ROLE[r]}</span>' for r in c['roles'])
    facts = ''.join(f'<div><dt>{k}</dt><dd>{esc(v)}</dd></div>' for k, v in (('Броня', c['armor']), ('Вооружение', c['weapons']), ('Ресурс', c['resource']), ('Прокачка', c['lvl'])))
    tabs, panels = [], []
    for k, s in enumerate(c['specs']):
        on = k == 0
        tabs.append(f'<button type="button" role="tab" id="tab-{k}" aria-controls="spec-{k}" aria-selected="{"true" if on else "false"}" tabindex="{0 if on else -1}">{esc(s["n"])}<small>{" · ".join(ROLE[r] for r in s["roles"])}</small></button>')
        keys = ''.join(f'<li><div>{ability(ru, en, lang)}</div><span class="d">{esc(d)}</span></li>' for ru, en, d in s['keys'])
        panels.append(f'<div class="spanel" role="tabpanel" id="spec-{k}" aria-labelledby="tab-{k}" tabindex="0"{"" if on else " hidden"}>'
                      f'<div class="about"><p class="what">{"".join(ri(r) for r in s["roles"])}{esc(s["what"])}</p><p class="style">{esc(s["style"])}</p>'
                      f'<div class="tipbox"><svg class="ico fi" aria-hidden="true"><use href="#i-fire"/></svg><p><span class="tl">Совет</span>{esc(s["tip"])}</p></div></div>'
                      f'<ul class="keys" aria-label="Ключевые способности">{keys}</ul></div>')
    news = ''.join(f'<li>{esc(x)}</li>' for x in c['news'])
    side = []
    for fac, title in (('alliance', 'Альянс'), ('horde', 'Орда')):
        items = []
        for r in races:
            if r['f'] != fac or c['id'] not in r['can']:
                continue
            tags = ('<span class="tag new">новое</span>' if r['can'][c['id']] == 'new' else '') + ('<span class="tag paid">платная</span>' if r['paid'] else '')
            items.append(f'<li><a href="@@HOME@@#pick={r["id"]}.{c["id"]}"><span class="rn">{esc(r["n"])}</span>{tags}<span class="go">В подборщик{ico("arrow")}</span></a></li>')
        body = f'<ul>{"".join(items)}</ul>' if items else '<p class="none">Нет доступных рас</p>'
        side.append(f'<div class="fside {fac}"><h3>{title}</h3>{body}</div>')
    group = ''.join(f'<li>{esc(x)}</li>' for x in c['group'])
    pros = ''.join(f'<li>{esc(x)}</li>' for x in c['pros'])
    cons = ''.join(f'<li>{esc(x)}</li>' for x in c['cons'])
    return {
        'ID': c['id'], 'COLOR': COLOR[c['id']], 'DESC': esc(c['desc']), 'ROLES': roles, 'FACTS': facts,
        'TABS': ''.join(tabs), 'PANELS': ''.join(panels), 'NEWS': news, 'RACES': ''.join(side),
        'RACES_TIP': esc(c['races_tip']), 'GROUP': group, 'LVL': esc(c['lvl']), 'PROFS': esc(c['profs']),
        'PROS': pros, 'CONS': cons,
        'PREV': CLASSES[i - 1], 'NEXT': CLASSES[(i + 1) % len(CLASSES)],
    }


def build_class(c, lang, tpl, base_css, sprite, races):
    here = page_dir(lang, f'classes/{c["id"]}/')
    root = rel(here, '')
    home = rel(here, page_dir(lang))
    v = render_class(c, races, lang)
    html = tpl.replace('@@BASE_CSS@@', base_css).replace('@@SPRITE@@', sprite)
    for k in ('ID', 'COLOR', 'DESC', 'ROLES', 'FACTS', 'TABS', 'PANELS', 'NEWS', 'RACES', 'RACES_TIP', 'GROUP', 'LVL', 'PROFS', 'PROS', 'CONS'):
        html = html.replace(f'@@{k}@@', v[k])
    others = ''.join(f'<a class="oc" href="../{o["id"]}/" style="--cc:{COLOR[o["id"]]}">{pic(o["id"], root, (360,), "132px")}<b>{esc(o["n"])}</b></a>' for o in CLASSES if o['id'] != c['id'])
    pager = (f'<a class="prev" href="../{v["PREV"]["id"]}/">{ico("arrow")}{esc(v["PREV"]["n"])}</a>'
             f'<a class="next" href="../{v["NEXT"]["id"]}/">{esc(v["NEXT"]["n"])}{ico("arrow")}</a>')
    toc = ''.join(f'<a href="../{o["id"]}/"{" aria-current=\"page\"" if o["id"] == c["id"] else ""}>{esc(o["n"])}</a>' for o in CLASSES)
    links = [(n, s.format(id=c['id'])) for n, s in SOURCES]
    sources = ''.join(f'<li><a href="{u}" target="_blank" rel="noopener">{esc(n)}</a></li>' for n, u in links)
    html = html.replace('@@OTHERS@@', others).replace('@@PAGER@@', pager).replace('@@TOC_CLASSES@@', toc).replace('@@SOURCES@@', sources)

    html, missing = translate(html, lang)
    html = mark_long(hyph_tabs(html))
    html = html.replace('@@NAME@@', esc(tr(c['n'], lang)))
    html = html.replace('@@HOME@@', home)
    html = html.replace('@@CANON@@', SITE + here)
    html = html.replace('@@ALTERNATES@@', alternates(f'classes/{c["id"]}/'))
    html = localize(html, lang, here)
    return here + 'index.html', html, missing


# ---------- race pages ----------

FAC = {'alliance': 'Альянс', 'horde': 'Орда'}
FHERO = {'alliance': '#86a6d8', 'horde': '#d98a84'}
NCLS = {4: 'Четыре класса', 5: 'Пять классов', 6: 'Шесть классов', 7: 'Семь классов'}
SKY_SUB = {'skyA': 'Скайборн за Альянс', 'skyH': 'Скайборн за Орду'}


def build_race(rp, lang, tpl, base_css, class_css, sprite, races, en):
    r = next(x for x in races if x['id'] == rp['id'])
    slug = {x['id']: x['slug'] for x in RACES_PAGE}
    i = next(k for k, x in enumerate(RACES_PAGE) if x['id'] == rp['id'])
    here = page_dir(lang, f'races/{rp["slug"]}/')
    root = rel(here, '')
    home = rel(here, page_dir(lang))
    classes_dir = rel(here, page_dir(lang, 'classes/'))

    facts = ''.join(f'<div><dt>{k}</dt><dd>{esc(v)}</dd></div>' for k, v in rp['facts'])
    cards = []
    for kind, ru, what in r['rac']:
        name = ability(ru, en.get(ru, ru), lang, tag='')
        new = '<span class="tag new">новое</span>' if ru in NEW_RACIALS else ''
        cards.append(f'<article class="rcard"><div class="rt"><span class="k{" a" if kind == "a" else ""}">{"Активная" if kind == "a" else "Пассивная"}</span>{new}</div><h3>{name}</h3><p>{esc(what)}</p></article>')
    priest = ''
    if rp['priest']:
        sp = ', '.join(ability(n, n, lang) + (' <span class="tag new">новое</span>' if nw else '') for n, nw in rp['priest'])
        priest = f'<p class="pspells">Свои заклинания жреца: {sp}.</p>'

    cls_cards = []
    for c in CLASSES:
        if c['id'] not in r['can']:
            continue
        tags = '<span class="tags"><span class="tag new">новое</span></span>' if r['can'][c['id']] == 'new' else ''
        cls_cards.append(f'<a class="oc" href="@@HOME@@#pick={r["id"]}.{c["id"]}" style="--cc:{COLOR[c["id"]]}">{pic(c["id"], root, (360,), "132px")}{tags}<b>{esc(c["n"])}</b><span class="go">В подборщик</span></a>')
    nope = [c['n'] for c in CLASSES if c['id'] not in r['can']]
    nope_html = ('<p class="nope">Недоступны: ' + ', '.join(f'<span>{esc(n)}</span>' for n in nope) + '.</p>') if nope else ''

    news = ''.join(f'<li>{esc(x)}</li>' for x in rp['news'])
    cn = {c['id']: c['n'] for c in CLASSES}
    best = ''.join(f'<li><a href="{classes_dir}{cid}/">{esc(cn[cid])}</a><span>{esc(why)}</span></li>' for cid, why in rp['best'])

    others = ''
    for fac in ('alliance', 'horde'):
        cards_o = ''.join(f'<a class="oc" href="../{slug[o["id"]]}/" style="--cc:var(--{fac})">{pic(slug[o["id"]], root, (360,), "132px")}<b>{esc(o["n"])}</b></a>'
                          for o in races if o['f'] == fac and o['id'] != r['id'])
        others += f'<div class="ofac {fac}"><h3>{FAC[fac]}</h3><div class="others">{cards_o}</div></div>'
    prev, nxt = RACES_PAGE[i - 1], RACES_PAGE[(i + 1) % len(RACES_PAGE)]
    rn = {x['id']: x['n'] for x in races}
    pager = (f'<a class="prev" href="../{prev["slug"]}/">{ico("arrow")}{esc(rn[prev["id"]])}</a>'
             f'<a class="next" href="../{nxt["slug"]}/">{esc(rn[nxt["id"]])}{ico("arrow")}</a>')
    cur = ' aria-current="page"'
    toc = ''.join(f'<a href="../{slug[o["id"]]}/"{cur if o["id"] == r["id"] else ""}>{esc(o["n"])}</a>' for o in races)
    sources = ''.join(f'<li><a href="{u.format(wt=rp["wt"])}" target="_blank" rel="noopener">{esc(n)}</a></li>' for n, u in RACE_SOURCES)

    v = {
        'ID': r['id'], 'ART': rp['slug'], 'FCOLOR': f'var(--{r["f"]})', 'FHERO': FHERO[r['f']], 'FACTION': FAC[r['f']],
        'PAID': ' <span class="tag paid">платная</span>' if r['paid'] else '',
        'SUB': f'<p class="sub">{SKY_SUB[r["id"]]}</p>' if r['id'] in SKY_SUB else '',
        'DESC': esc(rp['lead']), 'FACTS': facts, 'BEST': rp['best'][0][0], 'RACIALS': ''.join(cards), 'PRIEST': priest,
        'NCLS': NCLS[len(r['can'])], 'CLASSES': ''.join(cls_cards), 'NOPE': nope_html, 'NEWS': news,
        'LORE': esc(rp['lore']), 'TIP': esc(r['tip']), 'BESTLIST': best, 'OTHERS': others, 'PAGER': pager,
        'TOC_RACES': toc, 'SOURCES': sources,
    }
    html = tpl.replace('@@BASE_CSS@@', base_css).replace('@@CLASS_CSS@@', class_css).replace('@@SPRITE@@', sprite)
    for k, val in v.items():
        html = html.replace(f'@@{k}@@', val)
    html, missing = translate(html, lang)
    html = mark_long(html)
    html = html.replace('@@NAME@@', esc(tr(r['n'], lang)))
    html = html.replace('@@HOME@@', home)
    html = html.replace('@@CANON@@', SITE + here)
    html = html.replace('@@ALTERNATES@@', alternates(f'races/{rp["slug"]}/'))
    html = localize(html, lang, here)
    return here + 'index.html', html, missing


def main():
    src = open(os.path.join(HERE, 'index.src.html'), encoding='utf-8').read()
    tpl = open(os.path.join(HERE, 'class.src.html'), encoding='utf-8').read()
    rtpl = open(os.path.join(HERE, 'race.src.html'), encoding='utf-8').read()
    class_css = tpl[tpl.index('/* Class page'):tpl.index('</style>')].strip('\n')
    base_css = src[src.index('<style>') + 7:src.index('</style>')].strip('\n')
    s0 = src.index('<svg width="0" height="0"')
    sprite = src[s0:src.index('</svg>', s0) + 6]
    races = parse_races(src)
    assert len(races) == 10 and all(len(r['rac']) == 4 for r in races), [(r['id'], len(r['rac'])) for r in races]
    assert [r['id'] for r in races] == [r['id'] for r in RACES_PAGE]
    en = parse_en(src)

    pages, allmissing = [], []
    for lang in LANGS:
        for path, html, missing in [build_home(lang, src)] + [build_class(c, lang, tpl, base_css, sprite, races) for c in CLASSES] \
                + [build_race(rp, lang, rtpl, base_css, class_css, sprite, races, en) for rp in RACES_PAGE]:
            assert '@@' not in html, (path, re.findall(r'@@\w+@@', html)[:5])
            pages.append((path, html))
            allmissing += missing

    listing = '--list' in sys.argv
    if not listing:
        for path, html in pages:
            full = os.path.join(HERE, path)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            open(full, 'w', encoding='utf-8', newline='\n').write(html)
        for lang in LANGS:
            open(os.path.join(HERE, f'manifest-{lang}.webmanifest'), 'w', encoding='utf-8', newline='\n').write(manifest(lang) + '\n')
        sw_version()
    uniq = list(dict.fromkeys(allmissing))
    if listing and '--missing' not in sys.argv:
        print('\n'.join(uniq))
    print(f'pages: {len(pages)}, missing: {len(uniq)}', file=sys.stderr)
    if uniq and not listing:
        sys.exit(1)

    import build_tools  # the tools page has its own builder and translations
    build_tools.main()
    import build_guides  # guides: own builder, texts already in three languages
    build_guides.main()
    import seo  # last: titles/descriptions for search, JSON-LD, analytics, sitemap.xml over the built pages
    seo.main()
    report_new_langs()
    if not listing:
        import search  # site search index over the finished pages; it changes assets/, so the worker version is taken again
        search.main()
        sw_version()


def report_new_langs():
    """New languages: bad characters in translations fail the build; --missing prints the translator template,
    otherwise untranslated strings fail the build (the page would show English in their place)."""
    bad = [(l, en, x) for l in langs.NEW for en, x in langs.OV[l].items() if not langs.check_chars(en, x)]
    assert not bad, bad[:5]
    if '--missing' in sys.argv:
        lang = os.environ['WF_LANG']
        sys.stdout.reconfigure(encoding='utf-8')
        print(langs.missing_json(lang, langs.MISSING[lang]))
        return
    gaps = {l: len(set(langs.MISSING[l])) for l in langs.NEW if langs.MISSING[l]}
    if gaps:
        print(f'untranslated: {gaps} (python build.py --missing <lang>)', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
