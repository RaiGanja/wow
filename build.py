"""Сборка гида: index.src.html, class.src.html, race.src.html (русские исходники) + content/classes.py, content/races.py
+ i18n/{ru,en,uk}.txt (переводы, строка в строку)
-> index.html, en/index.html, uk/index.html, classes/<id>/index.html и races/<slug>/index.html на трёх языках.
Запуск: python build.py [--list]  (--list печатает русские фрагменты без перевода)"""
import hashlib, html as _html, json, os, posixpath, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
if '--missing' in sys.argv:          # python build.py --missing de: build de without its json, print what it lacks, write nothing
    os.environ['WF_LANG'] = sys.argv[sys.argv.index('--missing') + 1]
    sys.argv.append('--list')
sys.path.insert(0, os.path.join(HERE, 'content'))
from classes import CLASSES, SOURCES  # noqa: E402
from races import RACES_PAGE, SOURCES as RACE_SOURCES, NEW_RACIALS  # noqa: E402
import langs  # noqa: E402
import tod  # noqa: E402
import looks as LK  # noqa: E402
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
DISCORD = 'https://discord.gg/Zd45sNHy9x'   # постоянное приглашение на сервер Gabella Team (без срока и лимита)
# Свои постоянные приглашения по местам ссылки (Discord считает переходы по каждому — замер воронки).
# Discord не даёт двух бессрочных приглашений в один канал, поэтому места разведены по открытым каналам ИНФО.
DISCORD_AT = {
    'menu': 'https://discord.gg/CfTZa7QKAG',      # шапка и «Ещё» -> #игровые-новости
    'guide': 'https://discord.gg/ZTwSk79Hju',     # строка в конце гайдов, классов и рас -> #wow-гид
    'home': 'https://discord.gg/c7dANjdJnR',      # главная, блок «Группа» -> #правила
    'faq': 'https://discord.gg/c7dANjdJnR',       # FAQ, «Где найти группу?» -> #правила
    'profile': 'https://discord.gg/c7dANjdJnR',   # кабинет, экран «не участник» -> #правила
    'footer': DISCORD,                            # подвал -> #объявления (общий с хабом и ботом)
}
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
    guides = sorted((g for g in GUIDES if g.get('only', lang) == lang), key=lambda g: ORDER.index(g['slug']) if g['slug'] in ORDER else len(ORDER))
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
    """Footer block of every page (@@LEGAL@@): site map, trademarks, ©, privacy page, Discord, contact."""
    text, privacy, contact = LEGAL[lang][:3]
    return site_map(lang, root + page_dir(lang)) + (f'<div class="legal"><p>{text}</p><p>© 2026 Gabella<span aria-hidden="true"> · </span>'
            f'<a href="{root}{page_dir(lang, "privacy/")}">{privacy}</a><span aria-hidden="true"> · </span>'
            f'{discord_link("footer")}<span aria-hidden="true"> · </span>'
            f'{contact}: <a href="mailto:{CONTACT}">{CONTACT}</a></p></div>')


def only_lang(sub):
    """Language of a page built in one language only (a guide with 'only': 'uk'), else None."""
    from content.guides import GUIDES
    return next((g['only'] for g in GUIDES if g.get('only') and sub == f'guides/{g["slug"]}/'), None)


def alternates(sub):
    """hreflang links of a page (site-relative directory sub, '' = home) in every built language; x-default = Russian
    (a one-language page: only its own language, which is also x-default)."""
    only = only_lang(sub)
    alt = '\n'.join(f'<link rel="alternate" hreflang="{HREFLANG[l]}" href="{SITE}{page_dir(l, sub)}">' for l in ([only] if only else LANGS))
    return alt + f'\n<link rel="alternate" hreflang="x-default" href="{SITE}{page_dir(only, sub) if only else sub}">'


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
  const to = want && want !== cur && document.querySelector(`.langlist a[data-lang="${want}"]:not([data-list])`);
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
    w = null;
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
    only = only_lang(sub)
    label = tr('Язык', lang)
    def link(l, inner):
        cur = ' aria-current="page"' if l == lang else ''
        to = 'guides/' if only and l != only else sub            # a one-language guide: other languages open their guide list
        lst = ' data-list' if to != sub else ''                   # not this page in that language: no browser-language hint
        return f'<a href="{rel(here, page_dir(l, to))}" data-lang="{l}" hreflang="{HREFLANG[l]}" lang="{HREFLANG[l]}"{cur}{lst}>{inner}</a>'
    items = ''.join(f'<li>{link(l, f"<span>{AUTONYM[l]}</span><small>{l.upper()}</small>")}</li>' for l in LANGS)
    sel = (f'<div class="langsel"><button type="button" class="langbtn" aria-haspopup="true" aria-expanded="false" '
           f'aria-label="{label}: {AUTONYM[lang]}">{lang.upper()}</button><ul class="langlist" hidden>{items}</ul></div>')
    sheet = f'<div class="langgrid" role="group" aria-label="{label}">{"".join(link(l, AUTONYM[l]) for l in LANGS)}</div>'
    hint = json.dumps({l: HINT[l] for l in LANGS}, ensure_ascii=False)
    return html.replace('@@LANGSEL@@', sel).replace('@@LANGSHEET@@', sheet).replace('</body>', LANG_JS.replace('@@HINT@@', hint) + '</body>', 1)


# Bottom tab bar on phones: the same tabs in the same order on every page (the profile button of the top bar is hidden there).
TABS = (('', 'home', 'Главная'), ('guides/', 'book', 'Гайды'), ('play/', 'sword', 'В игре'), ('profile/', 'user', 'Профиль'))


def tabbar(cur=None, home='@@HOME@@'):
    """Tab bar markup; cur — path of the current tab ('', 'guides/', 'play/', 'profile/'); home '' — the home page itself."""
    on = ' aria-current="true"'
    tabs = ''.join(f'\n  <a href="{home + p if home or p else "#top"}"{on if p == cur else ""}>'
                   f'<svg class="ico" aria-hidden="true"><use href="#i-{i}"/></svg>{t}</a>' for p, i, t in TABS)
    return (f'<nav class="tabbar" aria-label="Быстрые разделы">{tabs}\n  <button type="button" class="morebtn" aria-haspopup="dialog" aria-controls="moreDlg">'
            '<svg class="ico" aria-hidden="true"><use href="#i-dots"/></svg>Ещё</button>\n</nav>')


# Top menu: the same items in the same order on every page; anchors of the home page stay in its own «Ещё» group.
NAV = (('classes/', 'Классы'), ('races/', 'Расы'), ('guides/leveling/', 'Прокачка'), ('guides/dungeons/', 'Подземелья'),
       ('guides/', 'Гайды'), ('tools/', 'Инструменты'), ('play/', 'В игре'))
# Sections sheet («Ещё»): (group, [(path from the language home, label)]); '#…' — a block of the home page.
MORE = (
    ('Справочник', (('', 'Главная'), ('classes/', 'Классы: сравнение'), ('races/', 'Расы: сравнение'), ('guides/leveling/', 'Прокачка 1–60'),
                    ('guides/dungeons/', 'Подземелья и рейды'), ('guides/professions/', 'Профессии'), ('guides/faq/', 'FAQ и даты'),
                    ('guides/news/', 'Новости'), ('guides/', 'Все гайды'))),
    ('Инструменты', (('#picker', 'Подборщик'), ('#builder', 'Конструктор группы'), ('tools/', 'Рамки, сравнение, поиск'), ('play/', 'В игре'))),
    ('Сообщество', (('discord', 'Discord'), ('roster/', 'Состав'), ('profile/', 'Мой профиль'))),
)


def discord_link(src, text='Discord', cls=''):
    c = f' class="{cls}"' if cls else ''
    return f'<a{c} href="{DISCORD_AT[src]}" target="_blank" rel="noopener">{text}</a>'


def mainnav(cur=None, home='@@HOME@@'):
    """Top menu markup; cur — path of the current item (NAV), home '' — the home page itself."""
    on = ' aria-current="true"'
    links = ''.join(f'<a href="{home}{p}"{on if p == cur else ""}>{t}</a>' for p, t in NAV)
    return f'<nav class="mainnav" aria-label="Разделы">\n    {links}{discord_link("menu")}\n  </nav>'


def more_groups(home='@@HOME@@'):
    """Common groups of the sections sheet, after the page's own («Эта страница», list of classes or races)."""
    def a(p, t):
        if p == 'discord':
            return discord_link('menu', t)
        return f'<a href="{home + p if home or (p and p[0] != "#") else (p or "#top")}">{t}</a>'
    return '\n    '.join(f'<div class="grp"><div class="gh">{g}</div>{"".join(a(p, t) for p, t in items)}</div>' for g, items in MORE)


def chrome(html, nav=None, tab=None, home='@@HOME@@'):
    """Menu, sections sheet and phone tab bar of a page (@@MAINNAV@@, @@MORENAV@@, @@TABBAR@@), before translate."""
    return (html.replace('@@MAINNAV@@', mainnav(nav, home)).replace('@@MORENAV@@', more_groups(home))
            .replace('@@TABBAR@@', tabbar(tab, home)))


def localize(html, lang, here):
    """Language-specific attributes shared by all pages."""
    html = html.replace('@@LEGAL@@', legal(lang, rel(here, '')))
    html = html.replace('@@ROOT@@', rel(here, ''))
    html = html.replace('@@DISCORD@@', DISCORD_AT['home']).replace('@@DISCORD_GUIDE@@', DISCORD_AT['guide'])
    html = lang_menu(html, lang, here)
    if lang == 'ru':
        html = ru_names(html)
    else:
        html = html.replace('<html lang="ru">', f'<html lang="{HREFLANG[lang]}">')
        html = html.replace('content="ru_RU"', f'content="{LOCALE[lang]}"')
    if lang == 'en':
        html = en_dates(html)
    if lang not in ('ru', 'uk'):                                  # Latin-script pages: preload the fonts they draw first
        html = html.replace('-cyrillic.woff2" as="font"', '-latin.woff2" as="font"')
    html = html.replace('</head>', REVEAL_CSS + '</head>', 1).replace('</body>', REVEAL_JS + '</body>', 1)
    return me(pwa(html, lang, rel(here, '')), lang, here)


EN_DATE = re.compile(r'(?<![\d.,:/\w-])(0[1-9]|[12]\d|3[01])\.(0[1-9]|1[0-2])(?:\.(20\d\d))?(?![\d\w]|\.\d)')
MONTHS = 'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split()


def en_dates(html):
    """English pages: 04.11 reads as April 11 to a US reader, so dd.mm(.yyyy) in the text becomes «Nov 4» («Nov 4, 2026»). Styles stay."""
    def one(m):
        d = f'{MONTHS[int(m[2]) - 1]} {int(m[1])}'
        return f'{d}, {m[3]}' if m[3] else d
    parts = re.split(r'(<style\b.*?</style>)', html, flags=re.S)
    return ''.join(p if p.startswith('<style') else EN_DATE.sub(one, p) for p in parts)


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


# Home page: the files the first screen does without (radio, search, profile, living art, time of day, analytics, manifest)
# wait in the page asleep, a <link> with data-rel and a <script> with data-src, and LATE_JS wakes them once the hero
# picture is painted, or at the first touch, key or scroll. Lighthouse counts every file that finishes before that paint.
LATE_JS = """<script>
(function () {
  var done = false;
  function wake() {
    if (done) return; done = true;
    document.querySelectorAll('link[data-rel]').forEach(function (l) { l.rel = l.dataset.rel; });
    document.querySelectorAll('script[data-src]').forEach(function (s) {
      var n = document.createElement('script');
      for (var i = 0; i < s.attributes.length; i++) if (s.attributes[i].name !== 'data-src') n.setAttribute(s.attributes[i].name, s.attributes[i].value);
      n.src = s.dataset.src; n.async = false;   // in page order: radio before the profile, as with defer
      s.replaceWith(n);
    });
  }
  ['pointerdown', 'keydown', 'touchstart', 'wheel', 'scroll'].forEach(function (t) { addEventListener(t, wake, { once: true, passive: true, capture: true }); });
  if (location.hash.length > 1) return wake();   // a link to a section: the blocks above it are drawn before the jump settles
  setTimeout(wake, 4000);   // a tab in the background paints nothing
  var img = document.querySelector('.hero-art img');
  var lcp = window.PerformanceObserver && PerformanceObserver.supportedEntryTypes && PerformanceObserver.supportedEntryTypes.indexOf('largest-contentful-paint') >= 0;
  if (img && lcp)   // the phone: the browser reports the hero picture once it is on the screen
    new PerformanceObserver(function (l) { if (l.getEntries().some(function (e) { return e.element === img; })) setTimeout(wake, 0); })
      .observe({ type: 'largest-contentful-paint', buffered: true });
  function later() {   // a wide screen, where the heading counts as the largest: a moment after the picture is drawn
    var go = function () { requestAnimationFrame(function () { setTimeout(wake, 500); }); };
    if (img && img.decode) img.decode().then(go, go); else go();
  }
  if (document.readyState === 'complete') later(); else addEventListener('load', later, { once: true });
})();
</script>
"""
LATE_FILES = r'assets/(?:radio|search|me|tod|living)/|manifest-\w+\.webmanifest|static\.cloudflareinsights\.com/'


def late(html):
    """Puts the files of LATE_FILES to sleep on a home page and adds LATE_JS (seo.apply calls it after the analytics tag)."""
    link =lambda m: f'<link data-rel="{m[1]}" href="{m[2]}">' if re.search(LATE_FILES, m[2]) else m[0]
    html = re.sub(r'<link rel="(stylesheet|manifest)" href="([^"]+)"(?: media="print" onload="[^"]*")?>', link, html)
    script = lambda m: f'<script{m[1] or ""} data-src="{m[2]}"{m[3].replace(" defer", "")}></script>' if re.search(LATE_FILES, m[2]) else m[0]
    html = re.sub(r'<script( type="module")? src="([^"]+)"([^>]*)></script>', script, html)
    return html if 'link[data-rel]' in html else html.replace('</body>', LATE_JS + '</body>', 1)


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


TEXT_EXT = ('.js', '.css', '.json', '.webmanifest', '.svg', '.txt', '.html', '.xml', '.vtt', '.md')


def read_norm(path):
    """File bytes with CRLF turned into LF for text files, so hashes are the same on LF and CRLF checkouts (autocrlf)."""
    b = open(path, 'rb').read()
    return b.replace(b'\r\n', b'\n') if path.endswith(TEXT_EXT) else b


def sw_version():
    """sw.js VERSION = short hash of assets/ (without the news feed, the worker fetches it fresh) and the manifests."""
    h = hashlib.sha1()
    files = [os.path.join(d, f) for d, _, fs in os.walk(os.path.join(HERE, 'assets')) for f in fs if f != 'news.json']
    files += [os.path.join(HERE, f'manifest-{l}.webmanifest') for l in LANGS]
    for f in sorted(files):
        h.update(os.path.relpath(f, HERE).replace(os.sep, '/').encode())
        h.update(read_norm(f))
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


TEASER = langs.derive({'ru': 'Профиль хранит ваших персонажей, достижения и рамки', 'en': 'Your profile keeps your characters, achievements and frames',
                       'uk': 'Профіль зберігає ваших персонажів, досягнення й рамки'})   # the line for signed-out readers; same words as MORE['teaser']


def me(html, lang, here):
    """Profiles (assets/me/, build_me.py): after the radio, so its events are heard. data-page is the path under the language
    home (guides/leveling/, tools/, play/; the 404 page swaps in 404) — me.js finds the page it is on without parsing URLs."""
    root, home = rel(here, ''), rel(here, page_dir(lang))
    page = here[len(page_dir(lang)):]
    solo = ' data-solo="1"' if only_lang(page) else ''   # a language-only guide is not in the guide set of game.json: me.js skips it
    head = f'<link rel="stylesheet" href="{root}assets/me/me.css" media="print" onload="this.media=\'all\'">\n</head>'
    js = f'<script src="{root}assets/me/me.js" data-root="{root}" data-home="{home}" data-lang="{lang}" data-teaser="{_html.escape(TEASER[lang])}" data-close="{_html.escape(tr('Закрыть', lang))}" data-page="{page}" data-look="{LK.V}"{solo} defer></script>\n</body>'
    return html.replace('</head>', head, 1).replace('</body>', js, 1)


def me_version():
    """?v=<hash> on me.js/me.css in every page: Cloudflare keeps /wow/assets/ for 30 days, a new address skips that cache."""
    d = os.path.join(HERE, 'assets', 'me')
    h = hashlib.sha1()
    for f in sorted(os.listdir(d)):
        if f in ('me.js', 'me.css') or f.startswith('i18n-'):   # me.js passes the same version on to the texts
            h.update(open(os.path.join(d, f), 'rb').read())
    v = h.hexdigest()[:10]
    n = 0
    for root, dirs, files in os.walk(HERE):
        dirs[:] = [x for x in dirs if not x.startswith('.') and x not in ('assets', 'content', 'i18n', 'tests', 'node_modules')]
        for f in files:
            if f.endswith('.html') and not f.endswith('.src.html'):
                p = os.path.join(root, f)
                html = open(p, encoding='utf-8').read()
                new = re.sub(r'(assets/me/me\.(?:js|css))(?:\?v=\w+)?', rf'\1?v={v}', html)
                if new != html:
                    open(p, 'w', encoding='utf-8', newline='\n').write(new)
                    n += 1
    print(f'me: {n} pages, v={v}', file=sys.stderr)


def script_version(folder, names):
    """?v=<hash of assets/<folder>/*> on the given files of that folder in every built page, like me_version."""
    d = os.path.join(HERE, 'assets', folder)
    h = hashlib.sha1()
    for f in sorted(os.listdir(d)):
        h.update(read_norm(os.path.join(d, f)))
    v = h.hexdigest()[:10]
    rx = re.compile(rf'(assets/{folder}/(?:{"|".join(re.escape(n) for n in names)}))(?:\?v=\w+)?')
    for root, dirs, files in os.walk(HERE):
        dirs[:] = [x for x in dirs if not x.startswith('.') and x not in ('assets', 'content', 'i18n', 'tests', 'node_modules')]
        for f in files:
            if f.endswith('.html') and not f.endswith('.src.html'):
                p = os.path.join(root, f)
                html = open(p, encoding='utf-8').read()
                new = rx.sub(rf'\1?v={v}', html)
                if new != html:
                    open(p, 'w', encoding='utf-8', newline='\n').write(new)
    print(f'{folder}: v={v}', file=sys.stderr)


def living_version():
    """?v=<hash> on assets/living/living.js (art masks included; the script passes the version on to them)."""
    script_version('living', ['living.js'])


def tod_version():
    script_version('tod', ['tod.js', 'tod.css'])


def art_version():
    """?v=<hash> on every assets/art/<file> address in the pages: Cloudflare and the browser keep /wow/assets/ for days
    (7 in the browser, plus the service worker), so a picture redrawn under the same name would otherwise stay old
    for returning visitors while living.js and its masks (versioned) already move on — water and fire off their places."""
    d = os.path.join(HERE, 'assets', 'art')
    ver = {}

    def tag(m):
        name = m.group(2)
        if name not in ver:
            # hero_{tod}-<w>.<ext> (tod.py) is filled in by the browser: one version over all four times of day
            fs = [os.path.join(d, name.replace('{tod}', t)) for t in tod.PARTS] if '{tod}' in name else [os.path.join(d, name)]
            h = hashlib.sha1()
            for f in fs:
                if os.path.isfile(f):
                    h.update(open(f, 'rb').read())
            ver[name] = h.hexdigest()[:8] if any(os.path.isfile(f) for f in fs) else ''
        return m.group(1) + (f'?v={ver[name]}' if ver[name] else '')
    scenes = {f: '?v=' + hashlib.sha1(open(os.path.join(d, f), 'rb').read()).hexdigest()[:8]
              for f in sorted(os.listdir(d)) if f.startswith('hero_')}
    # pic() in page JS draws only the scenes the script names in quotes ('hero_dawn-960'): the map carries just those
    artv = lambda html: '/*ARTV*/' + json.dumps({f: v for f, v in scenes.items() if f"'{f.rsplit('.', 1)[0]}'" in html}, separators=(',', ':'))
    n = 0
    for root, dirs, files in os.walk(HERE):
        dirs[:] = [x for x in dirs if not x.startswith('.') and x not in ('assets', 'content', 'i18n', 'tests', 'node_modules')]
        for f in files:
            if f.endswith('.html') and not f.endswith('.src.html'):
                p = os.path.join(root, f)
                was = html = open(p, encoding='utf-8').read()
                html = re.sub(r'/\*ARTV\*/\{[^}]*\}', lambda _: artv(html), html)   # pic() in page JS
                new = re.sub(r'(assets/art/([A-Za-z0-9_.{}-]+\.(?:avif|webp|jpg|png)))(?:\?v=\w+)?', tag, html)
                if new != was:
                    open(p, 'w', encoding='utf-8', newline='\n').write(new)
                    n += 1
    print(f'art: {n} pages, {len(ver)} files', file=sys.stderr)


def home_js():
    """The page script of each language home (all but the first-screen script before it) -> assets/home/<lang>.js?v=<hash>,
    asleep in the page like the LATE_FILES. Last of the page passes (after art_version), so its texts and addresses are final."""
    d = os.path.join(HERE, 'assets', 'home')
    os.makedirs(d, exist_ok=True)
    for lang in LANGS:
        p = os.path.join(HERE, page_dir(lang), 'index.html')
        html = open(p, encoding='utf-8').read()
        m = re.search(r"<script>\n(const HOME = ''.*?)</script>\n", html, re.S)
        assert m, p
        open(os.path.join(d, f'{lang}.js'), 'w', encoding='utf-8', newline='\n').write(m[1])
        v = hashlib.sha1(m[1].encode('utf-8')).hexdigest()[:10]
        tag = f'<script data-src="{rel(page_dir(lang), "")}assets/home/{lang}.js?v={v}"></script>\n'
        open(p, 'w', encoding='utf-8', newline='\n').write(html[:m.start()] + tag + html[m.end():])
    print(f'home: {len(LANGS)} scripts', file=sys.stderr)


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

# ru/uk home: one quiet line above the footer on how to play in the language; once closed (or followed), never again.
GAME_HINT = {'ru': ('В игре есть русский язык.', 'Как включить', 'guides/faq/#language', 'Закрыть'),
             'uk': ('Українською грають з аддоном.', 'Як встановити', 'guides/ukrainian/', 'Закрити')}
GAME_JS = """<script>
(function () {
  var KEY = 'gabella-game-lang', bar = document.getElementById('gamehint'), seen = '1';
  try { seen = localStorage.getItem(KEY); } catch (e) {}
  if (seen) return;
  var done = function () { try { localStorage.setItem(KEY, '1'); } catch (e) {} };
  bar.hidden = false;
  bar.querySelector('a').addEventListener('click', done);
  bar.querySelector('button').addEventListener('click', function () { done(); bar.remove(); });
})();
</script>
"""


def game_hint(lang):
    text, link, href, close = GAME_HINT[lang]
    return (f'<div class="gamehint" id="gamehint" hidden><span>{text} <a href="{href}">{link}</a></span>'
            f'<button type="button" aria-label="{close}"><svg class="ico" aria-hidden="true"><use href="#i-x"/></svg></button></div>\n'
            + GAME_JS)


def build_home(lang, src):
    src = src.replace('@@RACE_LEAD@@', json.dumps({r['id']: r['lead'] for r in RACES_PAGE}, ensure_ascii=False))
    src = src.replace('@@RACE_SLUG@@', json.dumps({r['id']: r['slug'] for r in RACES_PAGE}))
    src = chrome(src, tab='', home='')
    html, missing = translate(src, lang)
    html = tod.apply(html, lang)   # the hero in the reader's time of day (tod.py)
    here = page_dir(lang)
    html = html.replace('@@ALTERNATES@@', alternates(''))
    html = localize(html, lang, here)
    html = static_links(html, lang, '')
    html = card_dates(html)
    html = home_dungeons(html, lang)
    if lang in GAME_HINT:
        html = html.replace('<footer id="sources"', game_hint(lang) + '<footer id="sources"', 1)
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
    """Ability name. ru: the ruRU client name (names.json, else the site's Russian) + the English original; de/fr/es/pt/it: the official name (i18n/names.json, Wowhead)
    + English; en/uk/pl: English only. tag wraps the main name; '' = bare text (race cards put it in their own h3)."""
    main = langs.NAMES.get(en, {}).get('ru') or ru if lang == 'ru' else langs.name(en, lang)
    if main == en:
        return f'<{tag or "span"} lang="en">{esc(en)}</{tag or "span"}>'
    head = f'<{tag}>{esc(main)}</{tag}>' if tag else esc(main)
    return f'{head}<span class="en" lang="en">{esc(en)}</span>'


JS_STR = re.compile(r"""'[^'\n]*'|"[^"\n]*\"""")


def js_quote(s, q):
    return q + s.replace(q, '’') + q


def js_names(js, lang):
    """English game names in quoted JS data (dungeons, zones, cities) -> official localized ones on de/fr/es/pt/it and
    the ruRU client names on ru (the English stays a search key). uk/en/pl keep English: there is no Ukrainian client."""
    if lang == 'ru':
        def one(m):                                                # names inside Russian text; an English string only as a whole
            s = m[0][1:-1]
            return js_quote(ru_plain(s) if re.search(f'[{CYR}]', s) else ru_word(s), m[0][0])

        def row(m):                                                # DUNGEONS row: «Мертвые копи (The Deadmines)», the rest in Russian
            ru = ru_word(m[2])
            return m[1] + js_quote(f'{ru} ({m[2]})' if ru != m[2] else ru, "'") + JS_STR.sub(one, m[3])
        e = js.find('const EN = {')                                # EN maps Russian names to English: keep its English
        if e >= 0:
            f = js.index('\n};', e)
            return js_names(js[:e], lang) + js[e:f] + js_names(js[f:], lang)
        i = js.find('const DUNGEONS = [')
        if i < 0:
            return JS_STR.sub(one, js)
        j = js.find('\n];', i) % (len(js) + 1)                     # home_dungeons passes the block without its end
        return JS_STR.sub(one, js[:i]) + re.sub(r"(?m)^(\s*\[)'([^'\n]*)'(.*)$", row, js[i:j]) + JS_STR.sub(one, js[j:])
    if lang not in NAMED:
        return js
    return JS_STR.sub(lambda m: js_quote(langs.name(m[0][1:-1], lang), m[0][0]), js)


RU_MARK = re.compile(r'\[\[([^\[\]|\n]+)\|([^\[\]|\n]+)\]\]')   # ru sources: [[Дуротаре|Durotar]] = the name in a case form
RU_SKIP = re.compile(r'<head\b.*?</head>|<script\b.*?</script>|<style\b.*?</style>|<(\w+)\b[^>]*\blang="en"[^>]*>.*?</\1>|<[^>]+>', re.S)
_ru_rx = []


def ru_word(en):
    """Russian client name of an English game name (names.json, Wowhead ruRU); English when the client has none."""
    return langs.NAMES.get(en, {}).get('ru') or en


def ru_rx():
    """[[форма|English]] markup (groups 1, 2) or a bare English name with a ruRU name (group 3), not inside a longer English phrase."""
    if not _ru_rx:
        names = sorted((en for en, v in langs.NAMES.items() if v.get('ru') and v['ru'] != en), key=len, reverse=True) or ['\0']
        _ru_rx.append(re.compile(RU_MARK.pattern + r'|(?<![A-Za-z’\'-])(?<![A-Za-z] )(' + '|'.join(map(re.escape, names))
                                 + r')(?![A-Za-z’-])(?! [A-Za-z])'))
    return _ru_rx[0]


JS_TEXT = re.compile(r"""'[^'\n]*'|"[^"\n]*"|`[^`]*`""")


def ru_plain(s):
    """Russian text outside the page flow (script strings, JSON-LD): names in the client's Russian, without the English."""
    def word(n):
        if n[3] and n.string[n.start() - 1:n.start()] == '(' and n.string[n.end():n.end() + 1] == ')':
            return n[0]                                            # «Мертвые копи (The Deadmines)»: the English stays
        return n[1] or ru_word(n[3])
    return ru_rx().sub(word, s)


def ru_names(html):
    """Russian pages: game names as the ruRU client shows them. The first mention on a page reads «Оргриммар (Orgrimmar)»,
    later ones «Оргриммар». Bare English names in the text are nominative; other cases come marked in the source
    as [[Оргриммаре|Orgrimmar]]. Head, scripts, attributes and lang="en" elements are left alone (markup there loses the English)."""
    rx = ru_rx()
    seen = set()

    def name(m):
        word, en = (m[1], m[2]) if m[1] else (ru_word(m[3]), m[3])
        if en in seen:
            return word
        s, a, b = m.string, m.start(), m.end()
        if s[:a].endswith('(') and s[:a - 1].rstrip().endswith(word):   # «Мертвые копи (The Deadmines)» as written
            seen.add(en)
            return en
        if s[b:].lstrip(' ').startswith('(') or s[:a].endswith('('):   # not «(Hyjal Summit) (20)», «(Ремонтный робот (Repair Bot))»
            return word
        seen.add(en)
        return f'{word} ({en})'

    out, i = [], 0
    for m in RU_SKIP.finditer(html):
        out.append(rx.sub(name, html[i:m.start()]))
        block = m[0]
        if m[1]:                                                   # lang="en" element: its English counts as mentioned
            seen.add(re.sub(r'<[^>]+>', '', block).strip())
        elif block.startswith('<script'):                          # Russian strings in scripts: the client name, no English
            block = JS_TEXT.sub(lambda s: ru_plain(s[0]) if re.search(f'[{CYR}]', s[0]) else s[0], block)
        out.append(block)
        i = m.end()
    out.append(rx.sub(name, html[i:]))
    return RU_MARK.sub(r'\1', ''.join(out))


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


# ---------- professions on a class page and in the compare tool: pairs of the Professions guide + camp objects of the home PROFS ----------

PAIR_PROFS = {'bs': ('blacksmithing', 'mining'), 'eng': ('engineering', 'mining'), 'lw': ('leatherworking', 'skinning'),
              'tail': ('tailoring', 'enchanting'), 'alch': ('alchemy', 'herbalism')}
PROF_T = langs.fill({
    'h': {'ru': 'Профессии', 'en': 'Professions', 'uk': 'Професії'},
    'camp': {'ru': 'В лагере', 'en': 'In camp', 'uk': 'У таборі'},
    'note': {'ru': 'Пассивных бонусов у профессий в Forever нет: характеристики дают вещи, зелья и чары, которые вы делаете, и баффы объектов лагеря.',
             'en': 'Professions in Forever have no passive bonuses: stats come from the gear, potions and enchants you make, and from camp object buffs.',
             'uk': 'Пасивних бонусів у професій у Forever немає: характеристики дають речі, зілля й чари, які ви робите, і баффи об’єктів табору.'},
    'more': {'ru': 'Все пары, объекты лагеря и прокачка навыка', 'en': 'All pairs, camp objects and skill leveling',
             'uk': 'Усі пари, об’єкти табору й прокачування навички'},
})
_CAMP = {}


def camp_objects():
    """{profession id: (camp object, Russian effect)} from PROFS of the home page."""
    if not _CAMP:
        src = open(os.path.join(HERE, 'index.src.html'), encoding='utf-8').read()
        _CAMP.update({pid: (obj, eff) for pid, _n, _tier, obj, eff in re.findall(r"\['(\w+)', '([^']+)', (\d), '([^']+)', '([^']+)'\]", src)})
    return _CAMP


def class_profs(cid, lang):
    """Recommended pairs of a class in lang: [(pair, why, [(camp object, effect), …])]."""
    from content.guides import PAIRS, CLASS_PAIRS
    L = lambda d: langs.derive(d)[lang]
    camp = camp_objects()
    pairs = next(p for c, _n, p in CLASS_PAIRS if c == cid)
    return [(L(PAIRS[p][0]), L(why or PAIRS[p][1]), [(camp[x][0], camp[x][1] if lang == 'ru' else t_of(camp[x][1], lang)) for x in PAIR_PROFS[p]])
            for p, why in pairs]


def profs_panel(cid, lang):
    """Class page panel «Профессии»: two pairs, their camp buffs, the no-passives note and a link to this class in the guide."""
    tx = {k: v[lang] for k, v in PROF_T.items()}
    items = ''.join(f'<li><b>{esc(pair)}</b><span class="d">{esc(why)}</span>'
                    f'<span class="pcamp"><svg class="ico" aria-hidden="true"><use href="#i-fire"/></svg><span>{tx["camp"]}: '
                    + '; '.join(f'{esc(o)} — {esc(e)}' for o, e in camp) + '</span></span></li>'
                    for pair, why, camp in class_profs(cid, lang))
    return (f'<div class="panel cprofs" id="profs"><h3>{tx["h"]}</h3><ul class="cpairs">{items}</ul>'
            f'<p class="small">{esc(tx["note"])}</p>'
            f'<a class="pmore" href="@@HOME@@guides/professions/#pairs={cid}">{tx["more"]}{ico("arrow")}</a></div>')


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
        'RACES_TIP': esc(c['races_tip']), 'GROUP': group, 'LVL': esc(c['lvl']),
        'PROS': pros, 'CONS': cons,
        'PREV': CLASSES[i - 1], 'NEXT': CLASSES[(i + 1) % len(CLASSES)],
    }


def build_class(c, lang, tpl, base_css, sprite, races):
    here = page_dir(lang, f'classes/{c["id"]}/')
    root = rel(here, '')
    home = rel(here, page_dir(lang))
    v = render_class(c, races, lang)
    html = chrome(tpl.replace('@@BASE_CSS@@', base_css).replace('@@SPRITE@@', sprite), nav='classes/')
    for k in ('ID', 'COLOR', 'DESC', 'ROLES', 'FACTS', 'TABS', 'PANELS', 'NEWS', 'RACES', 'RACES_TIP', 'GROUP', 'LVL', 'PROS', 'CONS'):
        html = html.replace(f'@@{k}@@', v[k])
    others = ''.join(f'<a class="oc" href="../{o["id"]}/" style="--cc:{COLOR[o["id"]]}">{pic(o["id"], root, (360,), "132px")}<b>{esc(o["n"])}</b></a>' for o in CLASSES if o['id'] != c['id'])
    pager = (f'<a class="prev" href="../{v["PREV"]["id"]}/">{ico("arrow")}{esc(v["PREV"]["n"])}</a>'
             f'<a class="next" href="../{v["NEXT"]["id"]}/">{esc(v["NEXT"]["n"])}{ico("arrow")}</a>')
    toc = ''.join(f'<a href="../{o["id"]}/"{" aria-current=\"page\"" if o["id"] == c["id"] else ""}>{esc(o["n"])}</a>' for o in CLASSES)
    links = [(n, s.format(id=c['id'])) for n, s in SOURCES]
    sources = ''.join(f'<li><a href="{u}" target="_blank" rel="noopener">{esc(n)}</a></li>' for n, u in links)
    html = html.replace('@@OTHERS@@', others).replace('@@PAGER@@', pager).replace('@@TOC_CLASSES@@', toc).replace('@@SOURCES@@', sources)

    html, missing = translate(html, lang)
    html = html.replace('@@PROFS@@', profs_panel(c['id'], lang))   # already in lang: the pairs come from the Professions guide
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


PLACE_FACTS = ('Столица', 'Стартовая зона', 'Репутация')


def fact_ru(k, v):
    """Russian race page: places and factions by their English game name, which ru_names turns into the ruRU client name
    + (English); the Russian source stays the translation key. Site-named factions (Высший орден) keep their Russian name."""
    if k in PLACE_FACTS and v in T and t_of(v, 'uk') == t_of(v, 'en'):
        return t_of(v, 'en')
    return v


def build_race(rp, lang, tpl, base_css, class_css, sprite, races, en):
    r = next(x for x in races if x['id'] == rp['id'])
    slug = {x['id']: x['slug'] for x in RACES_PAGE}
    i = next(k for k, x in enumerate(RACES_PAGE) if x['id'] == rp['id'])
    here = page_dir(lang, f'races/{rp["slug"]}/')
    root = rel(here, '')
    home = rel(here, page_dir(lang))
    classes_dir = rel(here, page_dir(lang, 'classes/'))

    facts = ''.join(f'<div><dt>{k}</dt><dd>{esc(fact_ru(k, v) if lang == "ru" else v)}</dd></div>' for k, v in rp['facts'])
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
    html = chrome(html, nav='races/')
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

    sys.path.insert(0, os.path.join(HERE, 'tools'))
    import export_game  # game rules for profiles -> assets/game.json (the API copies it with npm run sync)
    export_game.main()
    import build_me  # profile texts -> assets/me/i18n-<lang>.json
    build_me.main()
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
        me_version()
        living_version()
        tod_version()
        art_version()
        home_js()
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
