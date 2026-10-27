"""Compare the changes of an official post (tools/news_parse.py) with what the site says now -> list of outdated pages.

The site base is the built English pages (en/**/index.html: what people see) and the personal home data assets/hero/en.json;
where to edit is found in the sources (content/*.py, *.src.html, content/talents/*.json, i18n/en.txt).
Statuses of one change on one page:
  outdated  - the page shows the old number (was Y) and not the new one, or shows a removed ability as current
  ok        - the page already shows the new number
  check     - the ability is mentioned without the changed number, or the post says 'no longer …' (a person decides)
  missing   - a new ability the site does not mention anywhere
verify_edit() is the number gate for automatic edits (stage 4): every number added by an edit must be in the original post,
and every new value of the change must be in the edited text.

    python tools/news_check.py <post.html | topic.json [post_number]>   - report for one post"""
import glob, json, os, re, sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import news_parse as np   # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://gabella.site/wow/'
STAT_TAIL = {'haste', 'bonus', 'damage', 'chance', 'speed', 'effect'}
UNIT_UNITS = ('article', 'tr', 'li', 'p', 'dd', 'h3', 'h4')


def config():
    p = os.path.join(ROOT, 'tools', 'news_sources.json')
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {}


def variants(name, aliases):
    """Spellings to look for: the name, its aliases ('Earth Fury' ~ 'Earthen Fury'), without 'The', without a stat word
    at the end ('Wind-Blessed Haste' -> 'Wind-Blessed'), hyphen as space."""
    out = {name, *aliases.get(name, [])}
    for n in list(out):
        out.add(re.sub(r'^The\s+', '', n))
        out.add('The ' + n)
        out.add(n.replace('-', ' '))
        words = n.split()
        if len(words) > 1 and words[-1].lower() in STAT_TAIL:
            out.add(' '.join(words[:-1]))
            out.add(' '.join(words[:-1]).replace('-', ' '))
    return sorted((v for v in out if len(v) > 3), key=len, reverse=True)


def units(src):
    """Text units of a page: a card (article), a table row, a list item, a paragraph."""
    root = np.tree(src)
    out = []

    def walk(n):
        for k in n.kids:
            if isinstance(k, str):
                continue
            if k.tag in UNIT_UNITS:
                t = k.text() if k.tag != 'li' else k.own_text()
                if t:
                    out.append(t)
                if k.tag in ('article', 'tr'):
                    continue
            walk(k)
    walk(root)
    return out


_PAGES = None


def pages(root=ROOT):
    """{page path ('races/tauren/'): [text units]} from en/ plus the personal home strings."""
    global _PAGES
    if _PAGES is not None and root == ROOT:
        return _PAGES
    res = {}
    for f in glob.glob(os.path.join(root, 'en', '**', 'index.html'), recursive=True):
        rel = os.path.relpath(os.path.dirname(f), os.path.join(root, 'en')).replace('\\', '/')
        rel = '' if rel == '.' else rel + '/'
        src = open(f, encoding='utf-8').read()
        src = re.sub(r'<(script|style|head)\b.*?</\1>', ' ', src, flags=re.S)
        src = re.sub(r'<(header|footer|nav)\b.*?</\1>', ' ', src, flags=re.S)
        res[rel] = units(src)
    hero = os.path.join(root, 'assets', 'hero', 'en.json')
    if os.path.exists(hero):
        strings = []

        def collect(x):
            if isinstance(x, str) and len(x) > 12:
                strings.append(x)
            elif isinstance(x, dict):
                for v in x.values():
                    collect(v)
            elif isinstance(x, list):
                for v in x:
                    collect(v)
        collect(json.load(open(hero, encoding='utf-8')))
        res['assets/hero/en.json'] = strings
    if root == ROOT:
        _PAGES = res
    return res


def segments(text, name, longer):
    """Pieces of a unit that talk about this name: from the name to the end of the sentence or the next ability name.
    A hit inside a longer known name ('Savage' in 'Savage Fury') is not a hit."""
    out = []
    covers = [(x.start(), x.end()) for l in longer for x in re.finditer(re.escape(l), text)]
    for m in re.finditer(r'(?<![\w’\'-])' + re.escape(name) + r'(?![\w’\'-])', text):
        if any(a <= m.start() and m.end() <= b and (b - a) > (m.end() - m.start()) for a, b in covers):
            continue
        rest = text[m.end():m.end() + 110]
        stop = re.search(r'(?<!\d)[.;](?:\s|$)|\s[|]\s|, (?=[A-Z][a-z]+(?: [A-Z][a-z]+)* (?:gives|adds|is|cuts|boosts|removes)\b)', rest)
        out.append(text[m.start():m.end() + (stop.start() if stop else len(rest))])
    return out


def same(a, b):
    return a[0] == b[0] and (not a[1] or not b[1] or a[1] == b[1])


def judge(change, seg):
    nums = np.numbers(seg)
    k = change['kind']
    if k in ('removed', 'replaced'):
        return 'outdated', 'removed in the post, the page still shows it'
    if k == 'no_longer':
        return 'check', 'post: no longer …'
    if change['pairs']:
        res = []
        for p in change['pairs']:
            new, old = (p['new'], p['unit']), (p['old'], p['old_unit'])
            if any(same(n, new) for n in nums):
                res.append('ok')
            elif any(same(n, old) for n in nums):
                res.append('outdated')
            else:
                res.append('check')
        if 'outdated' in res:
            return 'outdated', 'shows the old value ' + ', '.join(f"{p['old']}{p['old_unit']}" for p in change['pairs'])
        if all(r == 'ok' for r in res):
            return 'ok', 'already shows ' + ', '.join(f"{p['new']}{p['unit']}" for p in change['pairs'])
        return 'check', 'number not shown next to the name'
    if k == 'added':
        return 'ok', 'mentioned'
    return 'check', 'mentioned, the post changes it'


_TALENTS = None


def talent_classes():
    """{talent name: {class}} from content/talents/*.json: 'Endurance' is a rogue talent and a tauren racial."""
    global _TALENTS
    if _TALENTS is None:
        _TALENTS = {}
        for f in glob.glob(os.path.join(ROOT, 'content', 'talents', '*.json')):
            d = json.load(open(f, encoding='utf-8'))
            for tr in d.get('trees', []):
                for t in tr.get('talents', []):
                    if t.get('n', {}).get('en'):
                        _TALENTS.setdefault(t['n']['en'], set()).add(d.get('class'))
    return _TALENTS


RACE_WORDS = {'human': 'Human', 'dwarf': 'Dwarf', 'nightelf': 'Night Elf', 'gnome': 'Gnome', 'skyborne': 'Skyborne', 'orc': 'Orc',
              'undead': 'Undead', 'tauren': 'Tauren', 'troll': 'Troll'}
RACE_SLUGS = {'nightelf': 'night-elf'}


def relevant(subject, name, page, unit):
    """A racial name that is also a class talent counts only on that race's page or next to the race word."""
    if subject.get('type') != 'race' or name not in talent_classes():
        return True
    rid = subject['id']
    return page.startswith('races/' + RACE_SLUGS.get(rid, rid)) or RACE_WORDS.get(rid, '~') in unit


def sources_for(name, subject=None, longer=()):
    """file:line of the English name in the sources: where an edit goes (talent files only for class changes)."""
    files = glob.glob(os.path.join(ROOT, 'content', '*.py')) + glob.glob(os.path.join(ROOT, '*.src.html')) + [os.path.join(ROOT, 'i18n', 'en.txt')]
    if not subject or subject.get('type') == 'class':
        files += glob.glob(os.path.join(ROOT, 'content', 'talents', '*.json'))
    out = []
    for f in files:
        if not os.path.exists(f):
            continue
        for i, line in enumerate(open(f, encoding='utf-8'), 1):
            if name in line and segments(line, name, longer) and relevant(subject or {}, name, '', line):
                out.append(f'{os.path.relpath(f, ROOT).replace(os.sep, "/")}:{i}')
    return out


def check(items, site=None, cfg=None):
    """Per change: its findings on pages; plus the summary of outdated pages. Fixes and notes without names are skipped."""
    cfg = cfg if cfg is not None else config()
    aliases, skip_pages = cfg.get('aliases', {}), set(cfg.get('history_pages', ['guides/news/']))
    site = site if site is not None else pages()
    names = np.known_names()
    report = []
    for c in items:
        if c['kind'] in ('fix', 'note') or not c['abilities']:
            continue
        main = c['abilities'][0]
        vs = variants(main, aliases)
        longer = [n for n in names if n not in vs and any(re.search(r'(?<![\w’\'-])' + re.escape(v) + r'(?![\w’\'-])', n) for v in vs)]
        found = []
        for page, us in site.items():
            if page in skip_pages:
                continue
            for u in us:
                for v in vs:
                    if v not in u or not relevant(c['subject'], main, page, u):
                        continue
                    for seg in segments(u, v, longer):
                        st, why = judge(c, seg)
                        found.append({'page': page, 'status': st, 'why': why, 'seen': seg[:120]})
        if c['kind'] == 'added' and not found:
            found.append({'page': None, 'status': 'missing', 'why': 'new in the post, not on the site', 'seen': ''})
        # one finding per page and status, the worst first
        rank = {'outdated': 0, 'missing': 1, 'check': 2, 'ok': 3}
        best = {}
        for f in sorted(found, key=lambda f: rank[f['status']]):
            best.setdefault((f['page'], f['status']), f)
        report.append({'subject': c['subject'], 'ability': main, 'kind': c['kind'], 'pairs': c['pairs'], 'h': c['h'],
                       'findings': sorted(best.values(), key=lambda f: (rank[f['status']], f['page'] or '')),
                       'sources': sources_for(main, c['subject'], longer) if any(f['status'] in ('outdated', 'check') for f in best.values()) else []})
    return report


def outdated_pages(report):
    """{page: [ability: reason]} for pages to fix (status outdated), and the same for 'check'."""
    out, chk = {}, {}
    for r in report:
        for f in r['findings']:
            if f['page'] is None:
                continue
            tgt = out if f['status'] == 'outdated' else chk if f['status'] == 'check' else None
            if tgt is not None:
                tgt.setdefault(f['page'], []).append(f"{r['ability']}: {f['why']}")
    return out, chk


def page_url(page, lang='en'):
    if page.startswith('assets/'):
        return SITE + page
    return SITE + ('' if lang == 'ru' else lang + '/') + page


def verify_edit(original, before, after, expected=()):
    """Number gate for an automatic edit of a page text (any language).
    original: text of the official post; before/after: the site text before and after the edit; expected: pairs of the change.
    ok when every number the edit adds is in the original and every expected new value is present after the edit."""
    orig = {v for v, _ in np.numbers(original)}
    added = Counter(v for v, _ in np.numbers(after)) - Counter(v for v, _ in np.numbers(before))
    extra = sorted(v for v in added if v not in orig)
    have = {v for v, _ in np.numbers(after)}
    missing = sorted({p['new'] for p in expected if p['new'] not in have})
    return {'ok': not extra and not missing, 'extra': extra, 'missing': missing}


def render(report, title=''):
    """Short Markdown for a person: what changed, which pages are outdated (9 languages each), where to edit."""
    out, chk = outdated_pages(report)
    lines = [f'### {title}' if title else '', f'Изменений с названиями: {len(report)}. Устарело страниц: {len(out)}, проверить: {len(chk)}.', '']
    if out:
        lines.append('**Устарело** (страница × 9 языков):')
        for p, why in sorted(out.items()):
            lines.append(f'- {page_url(p)} — ' + '; '.join(sorted(set(why)))[:300])
    if chk:
        lines.append('', ) if out else None
        lines.append('**Проверить:**')
        for p, why in sorted(chk.items()):
            lines.append(f'- {page_url(p)} — ' + '; '.join(sorted(set(why)))[:300])
    miss = [r['ability'] for r in report if any(f['status'] == 'missing' for f in r['findings'])]
    if miss:
        lines += ['', '**Нет на сайте (новое):** ' + ', '.join(miss)]
    src = sorted({s for r in report for s in r['sources']})
    if src:
        lines += ['', '**Где править (исходники):** ' + ', '.join(src[:40]) + (' …' if len(src) > 40 else '')]
    return '\n'.join(l for l in lines if l is not None).strip()


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    cooked, meta = np.load(argv[0], argv[1] if len(argv) > 1 else None)
    rep = check(np.changes(cooked))
    print(render(rep, json.dumps(meta)))
    return 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main(sys.argv[1:]))
