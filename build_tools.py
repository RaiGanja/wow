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

# Home page data blocks reused as is: classes, roles, colours, buffs, races, dungeons, professions
HOME_JS = [(r'const CLASSES = \[', r'^const RC = .*$'), (r'const DUNGEONS = \[', r'^\];$'), (r'const PROFS = \[', r'^\];$'),
           (r'const EN = \{', r'^\};$')]   # EN: English names of specs and racials, for the search


def home_data(src):
    out = []
    for start, end in HOME_JS:
        i = re.search(start, src).start()
        j = re.compile(end, re.M).search(src, i).end()
        out.append(src[i:j])
    return '\n'.join(out)


def class_data(lang):
    """Fields of content/classes.py the compare and search tools need. Ability names: the ruRU client name on the Russian page,
    official localized ones on de/fr/es/pt/it (names.json), English elsewhere."""
    cx = {}
    for c in CLASSES:
        cx[c['id']] = {
            'armor': c['armor'], 'weapons': c['weapons'], 'resource': c['resource'], 'lvl': c['lvl'],
            'group': c['group'], 'pros': c['pros'], 'cons': c['cons'],
            'specs': [{'n': s['n'], 'en': s['en'], 'roles': s['roles'], 'what': s['what'],
                       'keys': [[(langs.NAMES.get(en, {}).get('ru') or ru) if lang == 'ru' else langs.name(en, lang), en, d] for ru, en, d in s['keys']]} for s in c['specs']],
        }
    return 'const CX = ' + json.dumps(cx, ensure_ascii=False) + ';'


def build_tools(lang, src, tpl, base_css, sprite):
    here = page_dir(lang, 'tools/')
    html = build.chrome(tpl.replace('@@BASE_CSS@@', base_css).replace('@@SPRITE@@', sprite), nav='tools/')
    html = html.replace('@@DATA@@', build.js_names(home_data(src), lang) + '\n' + class_data(lang))
    html, missing = translate(html, lang)
    html = html.replace('@@CPROF@@', json.dumps({c['id']: [p[:2] for p in build.class_profs(c['id'], lang)] for c in CLASSES}, ensure_ascii=False))
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
