"""Number gate of level 2 (edits of reference pages and builds): may this commit go to main without a person?

The editor (cloud task) commits ONE commit on a branch news/<key>@<sha8>; this gate compares it with the base and the facts
of the post (the news-facts block of the issue or the entry of the news-data branch). Green only when:
  1. exactly one commit over the base (one revert rolls it back);
  2. sources touched are only texts: content/*.py, content/talents/*.json, i18n/*, updates.json; the rest must be build output
     (pages, assets/, sitemap.xml, sw.js); code, templates, tools, workflows, tests, data/ -> red;
  3. every number an edit adds (per hunk, any language) is a number of the post facts (or of the original post, when given);
     dates, times, links and ?v= hashes do not count;
  4. every old -> new pair of the facts that the edit touches ends with the new value: a hunk that drops the old value of an
     ability keeps its new value; and each changed pair has its new value next to its name in at least one English source line.
Red -> nothing goes to main, the person gets a notice (tools/news_notify.py).

    python tools/news_gate.py --facts facts.json [--base origin/main] [--head HEAD] [--original post.html] [--json out.json]
    python tools/news_gate.py --issue 12          # facts from the issue (gh)"""
import argparse, json, os, re, subprocess, sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import news_parse as np    # noqa: E402
import news_check as nc    # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEXT = re.compile(r'^(content/[^/]+\.py|content/talents/[^/]+\.json|i18n/[^/]+|updates\.json)$')
CODE = re.compile(r'^(tools/|\.github/|tests/|data/|[^/]+\.src\.(html|css|js)$|[^/]+\.py$|content/[^/]+/(?!.*\.json$))')
EN = re.compile(r'^(content/[^/]+\.py|content/talents/[^/]+\.json|i18n/en\.txt)$')
NOISE = [re.compile(p) for p in (r'https?://\S+', r'\?v=[0-9a-f]+', r'\b\d{4}-\d{2}-\d{2}(?:T[\d:.]+Z?)?\b', r'\b\d{1,2}\.\d{1,2}\.\d{4}\b',
                                 r'\b\d{1,2}\.\d{2}(?=[^\d%]|$)(?!\s*%)', r'\b\d{1,2}:\d{2}\b', r'\b(?:19|20)\d{2}\b',
                                 r'#[0-9a-fA-F]{3,8}\b', r'\b\d+px\b', r'\[\[[^|\]]*\|', r'\b(?:id|data-[a-z]+)="[^"]*"')]


def git(*a):
    return subprocess.run(['git', '-C', ROOT, *a], capture_output=True, text=True, encoding='utf-8', check=True).stdout


def scrub(s):
    for p in NOISE:
        s = p.sub(' ', s)
    return s


def nums(s):
    return [v for v, _ in np.numbers(scrub(s))]


KV = re.compile(r'^\s*"(?:[^"\\]|\\.)*"\s*:\s*(".*?")\s*,?\s*$')


def hunks(base, head, path):
    """[(before, after)] of one file: the removed and the added lines of each hunk. In i18n/<lang>.json only the translation
    counts (the key is the English string: its numbers would hide a lost number of the translation)."""
    out, cur = [], None
    val = (lambda l: (KV.match(l).group(1) if KV.match(l) else l)) if re.match(r'i18n/[^/]+\.json$', path) else (lambda l: l)
    for line in git('diff', '-U0', '--no-color', f'{base}..{head}', '--', path).splitlines():
        if line.startswith('@@'):
            cur = [[], []]
            out.append(cur)
        elif cur is not None and line.startswith('-') and not line.startswith('---'):
            cur[0].append(val(line[1:]))
        elif cur is not None and line.startswith('+') and not line.startswith('+++'):
            cur[1].append(val(line[1:]))
    return [('\n'.join(b), '\n'.join(a)) for b, a in out]


def gate(facts, base='origin/main', head='HEAD', original=None):
    fails, warn = [], []
    n = int(git('rev-list', '--count', f'{base}..{head}').strip() or 0)
    if n != 1:
        fails.append(f'commits over the base: {n} (must be exactly 1, squash it)')
    files = [f for f in git('diff', '--name-only', f'{base}..{head}').splitlines() if f]
    text = [f for f in files if TEXT.match(f)]
    code = [f for f in files if not TEXT.match(f) and CODE.match(f)]
    if code:
        fails.append('not a text edit: ' + ', '.join(code[:10]))
    if not text:
        fails.append('no text sources changed')
    items = facts.get('facts') or []
    allowed = {v for c in items for v in c.get('nums', [])} | {p[k] for c in items for p in c.get('pairs', []) for k in ('new', 'old')}
    if original:
        allowed |= set(nums(np.plain(original)))
    aliases = nc.config().get('aliases', {})
    pairs = [(c, p) for c in items for p in c.get('pairs', []) if c.get('abilities')]
    en_after = []
    for f in text:
        for before, after in hunks(base, head, f):
            extra = sorted((Counter(nums(after)) - Counter(nums(before))).keys() - allowed, key=float)
            if extra:
                fails.append(f'{f}: numbers not in the post: {", ".join(map(str, extra))} | {after.strip()[:140]}')
            b, a = Counter(nums(before)), Counter(nums(after))
            for c, p in pairs:
                names = nc.variants(c['abilities'][0], aliases)
                touched = any(x in before or x in after for x in names)
                if touched and b[p['old']] > a[p['old']] and p['new'] not in a:
                    fails.append(f"{f}: {c['abilities'][0]}: the old {p['old']} is gone but the new {p['new']} is not there")
            if EN.match(f):
                en_after.append(after)
    for c, p in pairs:
        if c.get('kind') != 'changed':
            continue
        names = nc.variants(c['abilities'][0], aliases)
        hit = any(any(x in line for x in names) and p['new'] in nums(line) for blk in en_after for line in blk.splitlines())
        if not hit:
            warn.append(f"{c['abilities'][0]}: {p['old']} -> {p['new']} not edited in English sources (left for a person)")
    return {'ok': not fails, 'fails': fails, 'left': warn, 'files': files, 'commits': n}


def facts_of_issue(num):
    import news_watch as nw
    body = subprocess.run(['gh', 'issue', 'view', str(num), '-R', nw.REPO, '--json', 'body', '-q', '.body'],
                          capture_output=True, text=True, encoding='utf-8', check=True).stdout
    f = nw.facts_from_issue(body)
    if f and f.get('facts') is None and f.get('entry'):           # a huge patch: the facts are in the news-data entry
        ref, path = f['entry'].split(':', 1)
        f['facts'] = json.loads(git('show', f'origin/{ref}:{path}'))['changes']
    return f


def facts_of_entry(path):
    """Facts from an entry of the news-data branch (the gate in Actions uses it: the same facts the issue carries)."""
    e = json.load(open(path, encoding='utf-8'))
    return {'key': e['key'], 'sha': e['sha'], 'url': e['url'], 'title': e['title'], 'facts': e['changes']}


def fetch_original(url):
    """Cooked HTML of the post behind a forum link /t/<slug>/<topic>/<post> or the article page (only the runner can read it)."""
    import urllib.request
    import news_watch as nw
    m = re.match(r'(https://[a-z]{2}\.forums\.blizzard\.com/en/wow)/t/(?:[^/]+/)?(\d+)/(\d+)', url)
    get = lambda u: urllib.request.urlopen(urllib.request.Request(u, headers=nw.UA), timeout=25).read().decode('utf-8')  # noqa: E731
    if m:
        d = json.loads(get(f'{m.group(1)}/t/{m.group(2)}.json'))
        post = int(m.group(3))
        for p in d.get('post_stream', {}).get('posts', []):
            if p.get('post_number') == post:
                return p.get('cooked')
        q = json.loads(get(f'{m.group(1)}/t/{m.group(2)}/{post}.json'))
        return next((p.get('cooked') for p in q.get('post_stream', {}).get('posts', []) if p.get('post_number') == post), None)
    return nw.article_body(get(url))


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('--facts')
    ap.add_argument('--issue', type=int)
    ap.add_argument('--entry', help='entry .json of the news-data branch')
    ap.add_argument('--fetch-original', action='store_true', help='read the original post by its link (Actions runner)')
    ap.add_argument('--base', default='origin/main')
    ap.add_argument('--head', default='HEAD')
    ap.add_argument('--original', help='HTML or text of the original post (the runner can read the forum, the cloud task cannot)')
    ap.add_argument('--json')
    a = ap.parse_args(argv)
    facts = (json.load(open(a.facts, encoding='utf-8')) if a.facts else facts_of_entry(a.entry) if a.entry else facts_of_issue(a.issue))
    if not facts:
        print('FAIL: no news-facts block')
        return 1
    orig = open(a.original, encoding='utf-8').read() if a.original else None
    if a.fetch_original and facts.get('url'):
        try:
            orig = fetch_original(facts['url'])
            if orig and np.digest(orig) != facts.get('sha', np.digest(orig)):
                print('note: the post was edited after the event (hash differs): the gate uses the facts and the current text')
        except Exception as e:   # noqa: BLE001
            print(f'note: original not read ({type(e).__name__}): the gate uses the facts only')
    res = gate(facts, a.base, a.head, orig)
    res['key'], res['sha'] = facts.get('key'), (facts.get('sha') or '')[:8]
    if a.json:
        json.dump(res, open(a.json, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(('OK' if res['ok'] else 'FAIL') + f" {res['key']}@{res['sha']}: {len(res['files'])} files, {res['commits']} commit(s)")
    for x in res['fails']:
        print('  fail:', x)
    for x in res['left']:
        print('  left:', x)
    return 0 if res['ok'] else 1


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main(sys.argv[1:]))
