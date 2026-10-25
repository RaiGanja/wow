"""Адреса файлов под assets/ без ?v=<хэш> в собранном сайте: python tests/check_vhash.py [-v]
HTML отдаётся no-cache, а /wow/assets/ браузер держит 7 дней (edge 30): файл, заменённый под тем же именем и
подгруженный без версии, у посетителей остаётся старым. Проверяем HTML (атрибуты, inline-скрипты и стили), CSS (url())
и JS в assets/: у каждого адреса файла должен быть ?v= (в JS допустимо: версия пришла в рантайме — +V, ${ver}, ${q}).
Не под долгим кэшем и потому не проверяются: sw.js, manifest-*.webmanifest, updates.json, assets/news.json, внешние хосты."""
import os, re, sys

HERE = os.environ.get('CHECK_ROOT') or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXT = r'(?:webp|avif|png|jpe?g|gif|svg|ico|woff2?|mp3|ogg|m4a|wav|json|js|css|webmanifest)'
SKIP_DIRS = {'.git', '.build', 'node_modules', 'docs', 'content', 'i18n', 'tests', 'tools', '__pycache__'}
NOCACHE = re.compile(r'(?:^|/)(?:sw\.js|manifest-[\w-]+\.webmanifest|updates\.json|news\.json|sitemap\.xml)$')
# a version in the tail of the match: ?v=, ${V} / ${ver} / ${q}, + V / + ver / + q (the script got it from its own address)
RT_VER = r'(?:\$\{\s*(?:V|v|ver|q|vq|PV|AV|ARTV)\b|[\'"`]\s*\)?\s*\+\s*\(?\s*(?:V|v|ver|q|vq|PV|AV|ARTV)\b)'
# a path-looking token ending in an extension
HIT = re.compile(r'(?P<path>[\w./${}@-]*[\w}-]\.' + EXT + r')(?![\w(])(?=(?P<tail>.{0,60}))'
                 r'|(?<=[\'"`])(?P<bare>\.' + EXT + r')(?=(?P<tail2>[\'"`].{0,60}))', re.S)   # the second: '.webp' after a name built in JS


def strip_comments(text, kind):
    if kind in ('js', 'css', 'html'):
        text = re.sub(r'/\*.*?\*/', lambda m: re.sub(r'[^\n]', ' ', m[0]), text, flags=re.S)
    if kind in ('js', 'html'):
        text = re.sub(r'(?m)^(\s*)//.*$', lambda m: re.sub(r'[^\n]', ' ', m[0]), text)
        text = re.sub(r'(?<=[\s;,)])//[ \t].*$', lambda m: ' ' * len(m[0]), text, flags=re.M)
    if kind == 'html':
        text = re.sub(r'<!--.*?-->', lambda m: re.sub(r'[^\n]', ' ', m[0]), text, flags=re.S)
    return text


def scan(text, kind, name):
    out = []
    text = strip_comments(text, kind)   # same length as the source: offsets and lines stay
    for m in HIT.finditer(text):
        path, tail = m['path'] or m['bare'], m['tail'] or m['tail2']
        if tail.startswith('?v=') or re.match(RT_VER, tail) or re.match(r'''["']\s*(?::\s*["']\?v=|\])''', tail):   # or a key of the ARTV map (a literal key, or ARTV[f + '.webp'])
            continue
        before = text[max(0, m.start() - 12):m.start()]
        if re.search(r'https?:|//$', before) or path.startswith('//'):   # another host (api, fonts, wowhead): the headers are not ours
            continue
        if kind == 'js' and not re.search(r'[\'"`]', text[max(0, m.start() - 160):m.start()]):
            continue
        if NOCACHE.search(path):
            continue
        # a file name inside a string must be a file we serve: under assets/, or a part of one built in JS (no folder at all)
        line = text.count('\n', 0, m.start()) + 1
        out.append((name, line, path + tail[:20].split('\n')[0]))
    return out


def files():
    for d, dirs, fs in os.walk(HERE):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS and not x.startswith('.')]
        for f in fs:
            p = os.path.join(d, f)
            rel = os.path.relpath(p, HERE).replace(os.sep, '/')
            if f.endswith('.src.html') or f.startswith('test_') or NOCACHE.search(rel):
                continue
            if f.endswith('.html') or (rel.startswith('assets/') and f.endswith(('.css', '.js'))):
                yield p, rel


def main():
    bad = []
    for p, rel in files():
        text = open(p, encoding='utf-8').read()
        if rel.endswith('.html'):
            # inline <script> is JS, everything else (attributes, <style>) is read like markup/CSS
            bad += scan(text, 'html', rel)
        else:
            bad += scan(text, 'css' if rel.endswith('.css') else 'js', rel)
    keys = {}
    for name, line, ref in bad:
        keys.setdefault((name if name.startswith('assets/') else '<pages>', ref.split('?')[0]), []).append((name, line))
    for (name, ref), where in sorted(keys.items()):
        print(f'{name}: {ref}  ({len(where)}x, {where[0][0]}:{where[0][1]})')
    print(f'{len(keys)} addresses without ?v= ({len(bad)} places)')
    sys.exit(1 if keys else 0)


if __name__ == '__main__':
    main()
