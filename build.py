"""Сборка гида: index.src.html и class.src.html (русские исходники) + content/classes.py + i18n/{ru,en,uk}.txt (переводы, строка в строку)
-> index.html, en/index.html, uk/index.html и classes/<id>/index.html на трёх языках.
Запуск: python build.py [--list]  (--list печатает русские фрагменты без перевода)"""
import os, posixpath, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'content'))
from classes import CLASSES, SOURCES  # noqa: E402


def load(name):
    with open(os.path.join(HERE, 'i18n', name), encoding='utf-8') as f:
        return f.read().splitlines()


_ru, _en, _uk = load('ru.txt'), load('en.txt'), load('uk.txt')
assert len(_ru) == len(_en) == len(_uk), (len(_ru), len(_en), len(_uk))
T = {r: (e, u) for r, e, u in zip(_ru, _en, _uk)}

CYR = r'А-Яа-яЁё'
SEG = re.compile(r'(?:(?!\$\{)[^<>"\'`{}\n])*[' + CYR + r'](?:(?!\$\{)[^<>"\'`{}\n])*')
LANGS = ('ru', 'en', 'uk')
SITE = 'https://raiganja.github.io/wow/'


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
        return lead + T[core][0 if lang == 'en' else 1] + tail
    return SEG.sub(sub, src), missing


def tr(s, lang):
    return s if lang == 'ru' else T.get(s, (s, s))[0 if lang == 'en' else 1]


def page_dir(lang, sub=''):
    """Site-relative directory of a page, e.g. 'en/classes/mage/'."""
    return ('' if lang == 'ru' else lang + '/') + sub


def rel(from_dir, to_dir):
    r = posixpath.relpath(to_dir or '.', from_dir.rstrip('/') or '.')
    return './' if r == '.' else r + '/'


def localize(html, lang, here):
    """Language-specific attributes shared by all pages."""
    html = html.replace('@@ROOT@@', rel(here, ''))
    if lang != 'ru':
        html = html.replace('<html lang="ru">', f'<html lang="{lang}">')
        html = html.replace('content="ru_RU"', 'content="en_US"' if lang == 'en' else 'content="uk_UA"')
    return html


# ---------- home page ----------

def build_home(lang, src):
    html, missing = translate(src, lang)
    here = page_dir(lang)
    html = html.replace('@@RU@@', rel(here, page_dir('ru'))).replace('@@EN@@', rel(here, page_dir('en'))).replace('@@UK@@', rel(here, page_dir('uk')))
    html = localize(html, lang, here)
    if lang != 'ru':
        for tag in ('rel="canonical" href', 'property="og:url" content'):
            html = html.replace(tag + f'="{SITE}"', tag + f'="{SITE}{lang}/"')
        html = html.replace('assets/og.png', f'assets/og-{lang}.png')
        html = html.replace('data-lang="ru" hreflang="ru" lang="ru" aria-current="true"', 'data-lang="ru" hreflang="ru" lang="ru" aria-current="false"')
        html = html.replace(f'data-lang="{lang}" hreflang="{lang}" lang="{lang}" aria-current="false"', f'data-lang="{lang}" hreflang="{lang}" lang="{lang}" aria-current="true"')
    return here + 'index.html', html, missing


# ---------- class pages ----------

RACE_RX = re.compile(r"\{ id:'(\w+)', n:'([^']+)', f:'(\w+)'(, paid:true)?(?:, name:'([^']+)')?,\s*cls:\[([^\]]*)\]")
ROLE = {'tank': 'Танк', 'heal': 'Лекарь', 'dps': 'Урон', 'tank?': 'Танк (под вопросом)'}
COLOR = {'warrior': '#c79c6e', 'paladin': '#f58cba', 'hunter': '#abd473', 'rogue': '#fff569', 'priest': '#e8e8e8', 'shaman': '#2f8cf0', 'mage': '#40c7eb', 'warlock': '#8788ee', 'druid': '#ff7d0a'}


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def ico(name):
    return f'<svg class="ico" aria-hidden="true"><use href="#i-{name}"/></svg>'


def ri(role):
    return f'<svg class="ri" aria-hidden="true"><use href="#i-{role.rstrip("?")}"/></svg>'


def parse_races(src):
    out = []
    for rid, n, fac, paid, name, cls in RACE_RX.findall(src):
        can = {}
        for c in re.findall(r"'(\w+\*?)'", cls):
            can[c.rstrip('*')] = 'new' if c.endswith('*') else 'ok'
        out.append({'id': rid, 'n': name or n, 'f': fac, 'paid': bool(paid), 'can': can})
    return out


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
        # ability names: Russian with the English original; other languages use the English name only
        name = (lambda ru, en: f'<b>{esc(ru)}</b><span class="en" lang="en">{esc(en)}</span>') if lang == 'ru' else (lambda ru, en: f'<b lang="en">{esc(en)}</b>')
        keys = ''.join(f'<li><div>{name(ru, en)}</div><span class="d">{esc(d)}</span></li>' for ru, en, d in s['keys'])
        panels.append(f'<div class="spanel" role="tabpanel" id="spec-{k}" aria-labelledby="tab-{k}" tabindex="0"{"" if on else " hidden"}>'
                      f'<div class="about"><p class="what">{"".join(ri(r) for r in s["roles"])}{esc(s["what"])}</p><p class="style">{esc(s["style"])}</p>'
                      f'<p class="note tipn"><span class="mk tip">совет</span>{esc(s["tip"])}</p></div>'
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
    html = html.replace('@@NAME@@', esc(tr(c['n'], lang)))
    html = html.replace('@@HOME@@', home)
    for l in LANGS:
        html = html.replace(f'@@{l.upper()}@@', rel(here, page_dir(l, f'classes/{c["id"]}/')))
        html = html.replace(f'@@CUR_{l.upper()}@@', 'true' if l == lang else 'false')
    html = html.replace('@@CANON@@', SITE + here)
    alt = '\n'.join(f'<link rel="alternate" hreflang="{l}" href="{SITE}{page_dir(l, "classes/" + c["id"] + "/")}">' for l in LANGS)
    alt += f'\n<link rel="alternate" hreflang="x-default" href="{SITE}classes/{c["id"]}/">'
    html = html.replace('@@ALTERNATES@@', alt)
    html = localize(html, lang, here)
    return here + 'index.html', html, missing


def main():
    src = open(os.path.join(HERE, 'index.src.html'), encoding='utf-8').read()
    tpl = open(os.path.join(HERE, 'class.src.html'), encoding='utf-8').read()
    base_css = src[src.index('<style>') + 7:src.index('</style>')].strip('\n')
    s0 = src.index('<svg width="0" height="0"')
    sprite = src[s0:src.index('</svg>', s0) + 6]
    races = parse_races(src)
    assert len(races) == 10, len(races)

    pages, allmissing = [], []
    for lang in LANGS:
        for path, html, missing in [build_home(lang, src)] + [build_class(c, lang, tpl, base_css, sprite, races) for c in CLASSES]:
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
    if listing:
        print('\n'.join(uniq))
    print(f'pages: {len(pages)}, missing: {len(uniq)}', file=sys.stderr)
    if uniq and not listing:
        sys.exit(1)


if __name__ == '__main__':
    main()
