"""Проверка собранного сайта: локальные ссылки существуют, нет @@, на EN-гайдах нет кириллицы.
Запуск: python tests/check_site.py"""
import os, re, sys
from urllib.parse import unquote, urlsplit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {'.git', '.github', '.claude', 'docs', 'content', 'i18n', 'tests', 'node_modules'}
ATTR = re.compile(r'(?:href|src)="([^"]+)"')
SRCSET = re.compile(r'srcset="([^"]+)"')
IDS = re.compile(r'\sid="([^"]+)"')


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
    return out


def main():
    problems, n = [], 0
    for page in pages():
        n += 1
        html = open(page, encoding='utf-8').read()
        rel = os.path.relpath(page, ROOT).replace(os.sep, '/')
        if '@@' in html:
            problems.append(f'{rel}: остался @@')
        if rel.startswith('en/guides/'):
            body = re.sub(r'<(script|style)\b.*?</\1>', '', html, flags=re.S)
            body = re.sub(r'<[^>]+>', ' ', body)
            cyr = re.findall(r'[А-Яа-яЁёІіЇїЄєҐґ][^<\n]{0,30}', body)
            if cyr:
                problems.append(f'{rel}: кириллица на EN: {cyr[:3]}')
        ids = set(IDS.findall(html))
        for t in targets(html):
            if t.startswith(('http:', 'https:', 'mailto:', 'data:', 'javascript:', '${')) or '${' in t:
                continue
            u = urlsplit(t)
            if not u.path:
                if u.fragment and u.fragment not in ids and not u.fragment.startswith(('pick=', 'team=')):
                    problems.append(f'{rel}: нет якоря #{u.fragment}')
                continue
            p = os.path.normpath(os.path.join(os.path.dirname(page), unquote(u.path)))
            if p.endswith(os.sep) or os.path.isdir(p):
                p = os.path.join(p, 'index.html')
            if not os.path.exists(p):
                problems.append(f'{rel}: нет файла {t}')
    for p in problems:
        print(p)
    if problems:
        print(f'FAIL {len(problems)} problems in {n} pages')
        sys.exit(1)
    print(f'OK {n} pages')


if __name__ == '__main__':
    main()
