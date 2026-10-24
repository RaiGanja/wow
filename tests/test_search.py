"""Поиск по сайту: индекс есть на каждом языке, записи одинаковые по числу, каждая ведёт на собранную страницу и её якорь,
на всех страницах кнопка поиска и скрипты с одной версией ?v=. Запуск: python tests/test_search.py"""
import glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from langs import LANGS  # noqa: E402

import build  # noqa: E402
from content.guides import GUIDES  # noqa: E402

LIMITED = {s['id'] for g in GUIDES for s in g['sections'] if 'langs' in s}   # sections shown in some languages only

problems, sizes = [], {}
for lang in LANGS:
    rows = json.load(open(os.path.join(ROOT, 'assets', 'search', f'{lang}.json'), encoding='utf-8'))
    pre = build.page_dir(lang)
    sizes[lang] = sum(not build.only_lang(r[2].partition('#')[0][len(pre):]) and r[2].partition('#')[2] not in LIMITED
                      for r in rows)                             # one-language pages and ru/uk-only sections aside
    kinds = {k: sum(r[3] == k for r in rows) for k in range(4)}
    if kinds[0] < 31 or kinds[2] < 10 or kinds[3] < 35:
        problems.append(f'{lang}: мало записей {kinds}')
    for t, s, u, k, keys, x in rows:
        path, _, anchor = u.partition('#')
        page = os.path.join(ROOT, path, 'index.html')
        if not t.strip() or not os.path.exists(page):
            problems.append(f'{lang}: {t!r} -> {u}')
        elif anchor and f' id="{anchor}"' not in open(page, encoding='utf-8').read():
            problems.append(f'{lang}: нет якоря {u}')
    if lang != 'en':   # English names of pages are keys too: "mage" finds the mage page on any language
        mage = next((r for r in rows if r[3] == 0 and r[2] == build.page_dir(lang, 'classes/mage/')), None)
        if not mage or 'mage' not in (mage[0] + ' ' + mage[4]).lower():
            problems.append(f'{lang}: mage не ищется')
if len(set(sizes.values())) != 1:
    problems.append(f'разное число записей: {sizes}')

pages = [p for p in glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True)
         if not p.endswith('.src.html') and not re.search(r'(^|[\\/])(\.|node_modules|mock-)', os.path.relpath(p, ROOT))]
versions = set()
for p in pages:
    html = open(p, encoding='utf-8').read()
    v = re.findall(r'assets/search/search\.(?:js|css)\?v=(\w+)', html)
    if 'class="iconbtn srchbtn"' not in html or len(v) != 2:
        problems.append(f'нет поиска: {os.path.relpath(p, ROOT)}')
    versions |= set(v)
if len(versions) > 1:
    problems.append(f'разные версии поиска: {versions}')

assert not problems, '\n'.join(problems[:20])
print('OK', len(LANGS), 'languages,', sizes['ru'], 'entries,', len(pages), 'pages')
