"""Сборка страницы инструментов: tools.src.html + данные главной (классы, расы, подземелья, профессии)
+ content/classes.py -> tools/index.html, en/tools/index.html, uk/tools/index.html.
Переводы: общие i18n/{ru,en,uk}.txt плюс свои i18n/tools.{ru,en,uk}.txt (строка в строку).
Запуск: python build_tools.py [--list]  (--list печатает русские фрагменты без перевода)"""
import json, os, re, sys

import build
from build import CLASSES, LANGS, SITE, page_dir, rel, localize, translate
import langs

HERE = build.HERE

_ru, _en, _uk = (build.load(f'tools.{l}.txt') for l in langs.OLD)
assert len(_ru) == len(_en) == len(_uk), (len(_ru), len(_en), len(_uk))
build.T.update({r: (e, u) for r, e, u in zip(_ru, _en, _uk)})

# Home page data blocks reused as is: classes, roles, colours, buffs, races; English spec and racial names
HOME_JS = [(r'const CLASSES = \[', r'^const RC = .*$'), (r'const EN = \{', r'^RC\.skyA\.en = .*$')]   # + English names of specs and racials (the picker)


def home_data(src, blocks=HOME_JS):
    out = []
    for start, end in blocks:
        i = re.search(start, src).start()
        j = re.compile(end, re.M).search(src, i).end()
        out.append(src[i:j])
    return '\n'.join(out)


def class_data(lang):
    """Fields of content/classes.py the class compare needs."""
    cx = {}
    for c in CLASSES:
        cx[c['id']] = {
            'armor': c['armor'], 'weapons': c['weapons'], 'resource': c['resource'], 'lvl': c['lvl'],
            'group': c['group'], 'pros': c['pros'], 'cons': c['cons'],
            'specs': [{'n': s['n'], 'what': s['what']} for s in c['specs']],
        }
    return 'const CX = ' + json.dumps(cx, ensure_ascii=False) + ';'


def game_name(en, lang):
    """A dungeon or raid name as the game client shows it: ruRU on ru, the official one on de/fr/es/pt/it, English elsewhere."""
    return (langs.NAMES.get(en, {}).get('ru') or en) if lang == 'ru' else langs.name(en, lang)


LFG_RAIDS = {10: 'Barrow Deeps', 20: 'Hyjal Summit', 40: 'Onyxia’s Lair'}   # the raids of tools.src.html RAIDS by size


def lfg_data(src, lang):
    """Places for the LFG line of the group builder: dungeons [name, min, max, entrance faction] from DUNGEONS, raids by size."""
    i = src.index('const DUNGEONS = [')
    rows = re.findall(r"""^\s*\[(['"])(.+?)\1, (\d+), (\d+), .*?(?:, '(horde|alliance)')?\],?$""", src[i:src.index('\n];', i)], re.M)
    assert len(rows) > 30, len(rows)
    d = [[game_name(n, lang), int(lo), int(hi), f or 0] for _, n, lo, hi, f in rows]
    return json.dumps({'d': d, 'r': {k: game_name(v, lang) for k, v in LFG_RAIDS.items()}}, ensure_ascii=False)


def painted():
    """class-race pairs that have their own painting assets/art/<class>-<race>-360.webp (tools.src.html PAINTED)"""
    d = os.path.join(HERE, 'assets', 'art')
    races = json.load(open(os.path.join(HERE, 'assets', 'game.json'), encoding='utf-8'))['races']
    return sorted(f'{c["id"]}-{r}' for c in CLASSES for r in races if os.path.isfile(os.path.join(d, f'{c["id"]}-{r}-360.webp')))


def build_tools(lang, src, tpl, base_css, sprite):
    here = page_dir(lang, 'tools/')
    html = build.chrome(tpl.replace('@@BASE_CSS@@', base_css).replace('@@SPRITE@@', sprite), nav='tools/')
    html = html.replace('@@DATA@@', build.js_names(home_data(src), lang) + '\n' + class_data(lang))
    html, missing = translate(html, lang)
    html = build.set_updated(html, 'tools/')
    html = html.replace('@@LFG@@', lfg_data(src, lang))
    import build_guides   # the hero of this browser: names, best races, labels (after translate: it is in the page language already)
    html = html.replace('@@HERO@@', build_guides.hero_js(lang))
    html = html.replace('@@CPROF@@', json.dumps({c['id']: build.class_profs_short(c['id'], lang) for c in CLASSES}, ensure_ascii=False))
    html = html.replace('@@PAINTED@@', json.dumps(painted()))
    html = html.replace('@@HOME@@', rel(here, page_dir(lang)))
    html = html.replace('@@CANON@@', SITE + here)
    html = html.replace('@@ALTERNATES@@', build.alternates('tools/'))
    html = localize(html, lang, here).replace('assets/og.png', f'assets/og/tools-{lang}.jpg')
    return here + 'index.html', html, missing


def main():
    src = open(os.path.join(HERE, 'index.src.html'), encoding='utf-8').read()
    tpl = open(os.path.join(HERE, 'tools.src.html'), encoding='utf-8').read()
    base_css = src[src.index('<style>') + 7:src.index('</style>')].strip('\n')
    s0 = src.index('<svg width="0" height="0"')
    sprite = src[s0:src.index('</svg>', s0) + 6]

    pages, allmissing = [], []
    for lang in LANGS:
        path, html, missing = build_tools(lang, src, tpl, base_css, sprite)
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
    print(f'pages: {len(pages)}, missing: {len(uniq)}', file=sys.stderr)
    if uniq and not listing:
        sys.exit(1)


if __name__ == '__main__':
    main()
