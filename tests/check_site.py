"""Проверка собранного сайта: локальные ссылки существуют, нет @@, на EN-гайдах нет кириллицы,
у каждой страницы есть title, description, canonical и JSON-LD, sitemap.xml совпадает со страницами.
Запуск: python tests/check_site.py"""
import json, os, re, sys
import xml.etree.ElementTree as ET
from urllib.parse import unquote, urlsplit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import langs  # noqa: E402
SKIP_DIRS = {'.git', '.github', '.claude', 'docs', 'content', 'i18n', 'tests', 'node_modules'}
ATTR = re.compile(r'(?:href|src)="([^"]+)"')
SRCSET = re.compile(r'srcset="([^"]+)"')
IDS = re.compile(r'\sid="([^"]+)"')
OG = re.compile(r'property="og:image" content="([^"]+)"')
SITE = 'https://gabella.site/wow/'
HEAD = {'title': r'<title>[^<]+</title>', 'description': r'<meta name="description" content="[^"]+">',
        'canonical': r'<link rel="canonical" href="https://gabella.site/wow/[^"]*">'}


def pages():
    for d, dirs, files in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
        for f in files:
            if f == 'index.html':
                yield os.path.join(d, f)


def targets(html):
    out = ATTR.findall(html)
    for s in SRCSET.findall(html):
        if '${' in s:   # JS template srcset: commas inside ${...} break the split
            continue
        out += [p.strip().split(' ')[0] for p in s.split(',') if p.strip()]
    return [t for t in out if '{tod}' not in t]   # tod.py templates: the variant is filled in by the browser (files: tests/test_tod.py)


def check_sitemap(pages):
    """sitemap.xml: valid XML, exactly the built pages, every hreflang alternate is a page too."""
    ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9', 'x': 'http://www.w3.org/1999/xhtml'}
    try:
        root = ET.parse(os.path.join(ROOT, 'sitemap.xml')).getroot()
    except (OSError, ET.ParseError) as e:
        return [f'sitemap.xml: {e}']
    locs = {u.findtext('s:loc', namespaces=ns) for u in root.findall('s:url', ns)}
    alts = {a.get('href') for a in root.iter('{http://www.w3.org/1999/xhtml}link')}
    return ([f'sitemap.xml: нет страницы {u}' for u in sorted(pages - locs)]
            + [f'sitemap.xml: лишний адрес {u}' for u in sorted((locs | alts) - pages)])


def main():
    problems, n, listed = [], 0, set()
    for page in pages():
        n += 1
        html = open(page, encoding='utf-8').read()
        rel = os.path.relpath(page, ROOT).replace(os.sep, '/')
        if '@@' in html:
            problems.append(f'{rel}: остался @@')
        problems += [f'{rel}: нет {k}' for k, rx in HEAD.items() if not re.search(rx, html)]
        lds = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
        if not lds:
            problems.append(f'{rel}: нет JSON-LD')
        for ld in lds:
            try:
                json.loads(ld)
            except ValueError as e:
                problems.append(f'{rel}: битый JSON-LD: {e}')
        if '<meta name="robots" content="noindex">' not in html:   # personal pages (profile, player) stay out of the sitemap
            listed.add(SITE + rel[:-len('index.html')])
        if rel.startswith('en/guides/') or rel.split('/')[0] in langs.NEW:   # Latin-script pages: no Russian left
            body = re.sub(r'<(script|style)\b.*?</\1>', '', html, flags=re.S)
            body = re.sub(r'<a [^>]*\blang="(ru|uk)"[^>]*>.*?</a>', '', body, flags=re.S)   # language menu: autonyms
            body = re.sub(r'<[^>]+>', ' ', body)
            cyr = re.findall(r'[А-Яа-яЁёІіЇїЄєҐґ][^<\n]{0,30}', body)
            if cyr:
                problems.append(f'{rel}: кириллица: {cyr[:3]}')
        for u in OG.findall(html):   # share preview: absolute URL of a file in this repo
            if not u.startswith(SITE) or not os.path.exists(os.path.join(ROOT, u[len(SITE):])):
                problems.append(f'{rel}: нет картинки превью {u}')
        if 'rel="manifest"' not in html or 'serviceWorker' not in html:
            problems.append(f'{rel}: нет манифеста или service worker')
        ids = set(IDS.findall(html))
        static = set(targets(re.sub(r'<script\b.*?</script>', '', html, flags=re.S)))
        for t in targets(html):
            if t.startswith(('http:', 'https:', 'mailto:', 'data:', 'javascript:', '${')) or '${' in t:
                continue
            u = urlsplit(t)
            if not u.path:
                # a hash inside a script template is a route of that page (profile: #chars, #account), not an anchor
                if u.fragment and u.fragment not in ids and t in static and not u.fragment.startswith(('pick=', 'team=', 'pairs=')):
                    problems.append(f'{rel}: нет якоря #{u.fragment}')
                continue
            p = os.path.normpath(os.path.join(os.path.dirname(page), unquote(u.path)))
            if p.endswith(os.sep) or os.path.isdir(p):
                p = os.path.join(p, 'index.html')
            if not os.path.exists(p):
                problems.append(f'{rel}: нет файла {t}')
    for lang in langs.LANGS:   # installable site: every manifest icon exists
        m = json.load(open(os.path.join(ROOT, f'manifest-{lang}.webmanifest'), encoding='utf-8'))
        problems += [f'manifest-{lang}: нет {i["src"]}' for i in m['icons'] if not os.path.exists(os.path.join(ROOT, i['src']))]
    if "const VERSION = 'dev'" in open(os.path.join(ROOT, 'sw.js'), encoding='utf-8').read():
        problems.append('sw.js: VERSION не проставлен сборкой')
    problems += check_sitemap(listed)
    for p in problems:
        print(p)
    if problems:
        print(f'FAIL {len(problems)} problems in {n} pages')
        sys.exit(1)
    print(f'OK {n} pages')


if __name__ == '__main__':
    main()
