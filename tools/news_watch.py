"""Watcher of official Blizzard sources about WoW Forever: new posts and edits -> hash, structured changes, check against the site.

Sources (tools/news_sources.json, only public JSON and pages allowed by robots.txt):
  forum categories WoW: Forever (US/EU) and their beta sections -> topics with a staff poster or from watch_topics;
  watched topics (Development Notes, patch notes) are read every run: an edit of an old post is caught by its text hash;
  worldofwarcraft.blizzard.com/en-us/news -> articles with 'forever' in the title or address;
  the forum Blue Tracker (groups/blizzard-tracker) is a hint only and is off: robots.txt disallows /en/wow/g.
State (--state DIR, in Actions the branch news-data): ledger.json (what was seen: key -> hash, time), log.jsonl (one line per event),
entries/<date>-<key>-<sha8>.json (structured changes, check report, draft of the short news). Full post texts are not kept:
the link and the hash identify the version, Discourse keeps the edit history itself.
First run with an empty ledger only marks everything as seen (unless --since H: posts of the last H hours are events).

    python tools/news_watch.py --state .news-state --dry-run [--since 48]   - show what would happen, write nothing
    python tools/news_watch.py --state DIR                                  - normal run (writes the state)
    python tools/news_watch.py --state DIR --issues                         - also a GitHub issue per story (GITHUB_TOKEN)
Network errors: the source is skipped and counted in ledger.json sources (fails, last error); exit code 0."""
import argparse, hashlib, html, json, os, re, sys, time, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import news_parse as np    # noqa: E402
import news_check as nc    # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = 'gabella-wow/wow'
LABEL = 'news-auto'
UA = {'User-Agent': 'gabella-wow-guide (+https://gabella.site/wow/)', 'Accept': 'application/json, text/html;q=0.9'}
ARTICLE_RECHECK_H = 6
EMPTY = hashlib.sha256(b'').hexdigest()     # a post with no text (a video only): equal hashes do not make two such posts one story


def now_utc():
    return datetime.now(timezone.utc)


def iso(d):
    return d.strftime('%Y-%m-%dT%H:%M:%SZ')


def when(s):
    return datetime.fromisoformat(s.replace('Z', '+00:00')) if s else None


class Fetcher:
    """GET with the site User-Agent; a failure is recorded per source and returns None (the run goes on)."""

    def __init__(self, ledger, pause=0.3):
        self.src = ledger.setdefault('sources', {})
        self.pause, self.count = pause, 0

    def get(self, name, url, as_json=True):
        try:
            time.sleep(self.pause if self.count else 0)
            self.count += 1
            r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25)
            data = r.read().decode('utf-8')
            s = self.src.setdefault(name, {})
            s.update({'ok': iso(now_utc()), 'fails': 0})
            return json.loads(data) if as_json else data
        except Exception as e:   # noqa: BLE001  (any network / JSON error: skip the source this run)
            s = self.src.setdefault(name, {})
            s.update({'err': f'{type(e).__name__}: {str(e)[:120]}', 'err_at': iso(now_utc()), 'fails': s.get('fails', 0) + 1})
            print(f'skip {name}: {type(e).__name__}: {str(e)[:120]}', file=sys.stderr)
            return None


def topic_url(base, slug, topic, post):
    return f'{base}/t/{slug}/{topic}/{post}' if slug else f'{base}/t/{topic}/{post}'


def forum_records(f, cfg, ledger, region):
    """Staff posts of new or bumped Forever topics and of the watched topics."""
    fcfg = cfg['forums'][region]
    base = fcfg['base']
    beta = set(cfg.get('beta_categories', {}).get(region, []))
    cursors = ledger.setdefault('topics', {})
    watch = set(cfg.get('watch_topics', {}).get(region, []))
    todo = {t: None for t in watch}
    lists = []
    for path in fcfg['categories']:     # bumped order (new replies) and created order (a new staff topic stays visible under busy threads)
        lists.append(f.get(f'{region}:c/{path}', f'{base}/c/{path}.json'))
        if cfg.get('created_order', True):
            lists.append(f.get(f'{region}:c/{path}/new', f'{base}/c/{path}/l/latest.json?order=created'))
    for d in lists:
        if not d:
            continue
        for t in d.get('topic_list', {}).get('topics', []):
            staff = any(p.get('primary_group_id') for p in t.get('posters', []))
            key = f'{region}-{t["id"]}'
            mark = f'{t.get("last_posted_at")}|{t.get("highest_post_number")}'
            if (staff or t['id'] in watch) and cursors.get(key) != mark:
                todo[t['id']] = mark
    out = []
    for tid, mark in todo.items():
        d = f.get(f'{region}:t/{tid}', f'{base}/t/{tid}.json')
        if not d:
            continue
        posts = d.get('post_stream', {}).get('posts', [])
        loaded = {p['id'] for p in posts}
        rest = [i for i in d.get('post_stream', {}).get('stream', []) if i not in loaded][-20 * (cfg.get('max_topic_pages', 2) - 1):]
        if rest:
            q = '&'.join('post_ids[]=' + str(i) for i in rest)
            more = f.get(f'{region}:t/{tid}/posts', f'{base}/t/{tid}/posts.json?{q}')
            posts += (more or {}).get('post_stream', {}).get('posts', [])
        for p in posts:
            if not p.get('staff') or not p.get('cooked') or p.get('hidden') or p.get('deleted_at'):
                continue
            out.append({'key': f'{region}-{tid}-{p["post_number"]}', 'source': 'forum', 'region': region, 'topic': tid,
                        'post': p['post_number'], 'url': topic_url(base, d.get('slug'), tid, p['post_number']),
                        'title': html.unescape(d.get('title') or ''), 'author': p.get('username'), 'role': p.get('user_title'),
                        'created_at': p.get('created_at'), 'updated_at': p.get('updated_at'), 'version': p.get('version'),
                        'category': d.get('category_id'), 'beta': d.get('category_id') in beta or 'beta' in (d.get('title') or '').lower(),
                        'cooked': p['cooked']})
        if mark:
            cursors[f'{region}-{tid}'] = mark
    return out


ART = re.compile(r'<article class="NewsBlog">(.*?)</article>', re.S)


def article_list(src, base, match):
    out = []
    for m in ART.finditer(src or ''):
        a = m.group(1)
        href = re.search(r'href="(/(?:[a-z]{2}-[a-z]{2}/)?news/(\d+)[^"]*)"', a)
        t = re.search(r'NewsBlog-title[^>]*>([^<]+)<', a)
        d = re.search(r'iso8601&quot;:&quot;([^&]+)&quot;', a)
        if not (href and t):
            continue
        title = html.unescape(t.group(1)).strip()
        if match not in (title + href.group(1)).lower():
            continue
        path = href.group(1) if href.group(1).startswith('/en-us/') else '/en-us' + href.group(1)
        out.append({'id': href.group(2), 'title': title, 'url': base + path, 'created_at': d.group(1) if d else None})
    return out


def article_body(src):
    m = re.search(r'<div class="detail">(.*?)</div>\s*(?:</div>\s*){0,3}<(?:footer|div class="Blog-footer|section)', src or '', re.S)
    if m:
        return m.group(1)
    m = re.search(r'<div class="detail">(.*)', src or '', re.S)
    return m.group(1)[:200000] if m else ''


def article_records(f, cfg, ledger):
    a = cfg.get('articles')
    if not a:
        return []
    lst = article_list(f.get('articles:list', a['list'], as_json=False), a['base'], a.get('match', 'forever'))
    seen = ledger.setdefault('posts', {})
    out = []
    for it in lst:
        key = f'art-{it["id"]}'
        old = seen.get(key)
        stale = not old or old.get('title') != it['title'] or (now_utc() - when(old.get('checked') or old['seen'])) > timedelta(hours=ARTICLE_RECHECK_H)
        if not stale:
            continue
        page = f.get(f'articles:{it["id"]}', it['url'], as_json=False)
        if page is None:
            continue
        body = article_body(page)
        out.append({'key': key, 'source': 'article', 'region': 'us', 'topic': None, 'post': None, 'url': it['url'], 'title': it['title'],
                    'author': 'Blizzard Entertainment', 'role': 'Blizzard News', 'created_at': it['created_at'], 'updated_at': None,
                    'version': None, 'category': None, 'beta': 'beta' in it['title'].lower(), 'cooked': body})
    return out


def tracker_records(f, cfg, ledger):
    """Blue Tracker hint (off by default): only says which topics to read; the post itself is read from the topic."""
    t = cfg.get('tracker', {})
    if not t.get('enabled'):
        return []
    hint = []
    for region, fc in cfg['forums'].items():
        cats = set(cfg.get('forever_categories', {}).get(region, []))
        d = f.get(f'{region}:tracker', fc['base'] + t['path'])
        for p in (d or {}).get('posts', []):
            if p.get('category_id') in cats or 'forever' in (p.get('topic_title') or '').lower():
                hint.append((region, p['topic_id']))
    for region, tid in hint:
        cfg['watch_topics'].setdefault(region, [])
        if tid not in cfg['watch_topics'][region]:
            cfg['watch_topics'][region].append(tid)
    return []


def kind_of(rec):
    t = rec['title'].lower()
    if 'development notes' in t or 'dev notes' in t:
        return 'dev-notes'
    if 'patch notes' in t:
        return 'patch-notes'
    if 'hotfix' in t:
        return 'hotfixes'
    return 'article' if rec['source'] == 'article' else 'post'


def short_news(rec):
    """Level 1 draft: date, link, English title, kind, beta flag. The 9 languages come from fixed templates (stage 3)."""
    d = when(rec['created_at']) or now_utc()
    return {'date': d.strftime('%Y-%m-%d'), 'at': iso(d), 'url': rec['url'], 'title_en': rec['title'], 'kind': kind_of(rec), 'beta': bool(rec['beta'])}


def evaluate(rec, old=None):
    items = np.changes(rec['cooked'])
    st = np.structured(items)
    prev = set(old.get('lines', [])) if old else set()
    cur = {c['h'] for c in st}       # the ledger keeps the hashes of the structured lines: compare like with like
    new_lines = [c for c in items if c['h'] in cur and c['h'] not in prev] if old else items
    gone = sorted(prev - cur) if old else []
    rep = nc.check(new_lines)
    out, chk = nc.outdated_pages(rep)
    return {'changes': st, 'new_lines': [c['h'] for c in new_lines], 'gone_lines': gone, 'check': rep,
            'outdated': sorted(out), 'to_check': sorted(chk), 'summary': nc.render(rep)}


def twins(events):
    """The same text posted in US and EU is one story: the EU copy points to the US one."""
    by = {}
    for e in sorted(events, key=lambda e: (e['rec']['region'] != 'us', e['rec']['created_at'] or '')):
        lines = frozenset(c['h'] for c in e['res']['changes'])
        title = np.norm(e['rec']['title'])
        twin = next((p for p in by.values() if (p['rec']['sha'] == e['rec']['sha'] and e['rec']['sha'] != EMPTY) or
                     (lines and len(lines & p['lines']) >= 0.8 * max(len(lines), len(p['lines']))) or
                     (title == np.norm(p['rec']['title']) and p['rec']['source'] != e['rec']['source'])), None)
        if twin and (twin['rec']['region'] != e['rec']['region'] or twin['rec']['source'] != e['rec']['source']):
            twin['also'].append(e['rec']['url'])
            e['twin_of'] = twin['rec']['key']
        else:
            by[e['rec']['key']] = {'rec': e['rec'], 'lines': lines, 'also': e.setdefault('also', [])}
    return events


def run(cfg, ledger, since_h=None, fetcher=None):
    f = fetcher or Fetcher(ledger)
    first = not ledger.get('posts')
    tracker_records(f, cfg, ledger)
    recs = []
    for region in cfg['forums']:
        recs += forum_records(f, cfg, ledger, region)
    recs += article_records(f, cfg, ledger)
    seen = ledger.setdefault('posts', {})
    events, t = [], now_utc()
    for r in recs:
        r['sha'] = np.digest(r['cooked'])
        old = seen.get(r['key'])
        if old and old['sha'] == r['sha']:
            old['checked'] = iso(t)
            continue
        ev = 'edit' if old else 'new'
        fresh = since_h is not None and r['created_at'] and (t - when(r['created_at'])) <= timedelta(hours=since_h)
        res = evaluate(r, old)
        if first and not fresh and not old:
            ev = 'baseline'
        quiet = ev == 'edit' and r['source'] == 'article' and r['title'] == old.get('title') and not res['new_lines'] and not res['gone_lines']
        # an article page differs between fetches outside its change lines (art-24315203 went 3b822bb2 -> ... -> 3b822bb2,
        # 'edits' every 6 h): same title and no change line moved = no event, the new hash is only remembered
        if not quiet:
            events.append({'event': ev, 'rec': r, 'res': res})
        seen[r['key']] = {'sha': r['sha'], 'url': r['url'], 'title': r['title'], 'seen': (old or {}).get('seen', iso(t)), 'checked': iso(t),
                          'updated_at': r['updated_at'], 'version': r['version'], 'lines': [c['h'] for c in res['changes']]}
    ledger['last_run'] = iso(t)
    ledger['requests'] = f.count
    return twins([e for e in events])


def entry(e):
    r = e['rec']
    keep = {k: r[k] for k in ('key', 'source', 'region', 'topic', 'post', 'url', 'title', 'author', 'role', 'created_at', 'updated_at', 'version', 'category', 'beta', 'sha')}
    return {'event': e['event'], **keep, 'twin_of': e.get('twin_of'), 'also': e.get('also', []), 'short_news': short_news(r),
            'changes': e['res']['changes'], 'new_lines': e['res']['new_lines'], 'gone_lines': e['res']['gone_lines'],
            'outdated': e['res']['outdated'], 'to_check': e['res']['to_check'], 'check': e['res']['check'],
            'detected_at': iso(now_utc())}


def entry_name(r):
    return f"{(r['created_at'] or iso(now_utc()))[:10]}-{r['key']}-{r['sha'][:8]}.json"


def save(state, ledger, events, test=False):
    os.makedirs(os.path.join(state, 'entries'), exist_ok=True)
    written = []
    with open(os.path.join(state, 'log.jsonl'), 'a', encoding='utf-8', newline='\n') as log:
        for e in events:
            r = e['rec']
            log.write(json.dumps({'at': iso(now_utc()), 'event': e['event'], 'key': r['key'], 'sha': r['sha'][:16], 'url': r['url'],
                                  'twin_of': e.get('twin_of'), 'outdated': len(e['res']['outdated']), **({'test': True} if test else {})},
                                 ensure_ascii=False) + '\n')
            if e['event'] == 'baseline':
                continue
            name = entry_name(r)
            p = os.path.join(state, 'entries', name)
            with open(p, 'w', encoding='utf-8', newline='\n') as fh:
                json.dump(entry(e), fh, ensure_ascii=False, indent=1)
                fh.write('\n')
            written.append(p)
    with open(os.path.join(state, 'ledger.json'), 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(ledger, fh, ensure_ascii=False, indent=1, sort_keys=True)
        fh.write('\n')
    return written


def issue_body(e):
    r, s = e['rec'], short_news(e['rec'])
    head = (f"Blizzard ({r['role'] or r['author']}), {'правка поста' if e['event'] == 'edit' else 'новый пост'}: {r['url']}\n"
            f"Пост: {s['at'].replace('T', ' ').rstrip('Z')} UTC · тип {s['kind']}{' · бета' if s['beta'] else ''} · хэш {r['sha'][:16]}\n"
            + (f"Тот же текст: {', '.join(e.get('also', []))}\n" if e.get('also') else ''))
    facts = [c for c in e['res']['changes'] if not e['res']['new_lines'] or c['h'] in set(e['res']['new_lines'])]
    lines = []
    for c in facts:
        subj = c['subject'].get('id', 'general') + ('/' + c['subject']['spec'] if c['subject'].get('spec') else '')
        pr = ', '.join(f"{p['old']}{p['old_unit']} → {p['new']}{p['unit']}" for p in c['pairs'])
        lines.append(f"- `{subj}` · {', '.join(c['abilities']) or '—'} · {c['kind']}{' · ' + pr if pr else ''}\n  > {c['text']}")
    data = {'key': r['key'], 'sha': r['sha'], 'url': r['url'], 'title': r['title'], 'at': s['at'], 'kind': s['kind'], 'beta': s['beta'],
            'event': e['event'], 'facts': [{k: c[k] for k in ('h', 'subject', 'abilities', 'kind', 'pairs', 'nums', 'text')} for c in facts],
            'outdated': e['res']['outdated'], 'to_check': e['res']['to_check'], 'entry': 'news-data:entries/' + entry_name(r)}
    body = (head + '\n' + (e['res']['summary'] or 'Изменений с названиями нет.')
            + f"\n\n## Факты поста ({len(facts)})\nСписок изменений из поста Blizzard (для правки сайта; первоисточник — ссылка выше, на сайт идут наши слова и сверенные числа).\n\n"
            + '\n'.join(lines))
    blob = '\n\n<details><summary>news-facts (для tools/news_gate.py)</summary>\n\n```json\n' + json.dumps(data, ensure_ascii=False) + '\n```\n</details>\n'
    if len(blob) > 50000:      # a huge patch: the facts stay in the entry of the news-data branch (git show origin/news-data:entries/…)
        data['facts'] = None
        blob = '\n\n<details><summary>news-facts (для tools/news_gate.py)</summary>\n\n```json\n' + json.dumps(data, ensure_ascii=False) + '\n```\n</details>\n'
    if len(body) + len(blob) > 64000:
        body = body[:64000 - len(blob) - 40] + '\n…(список обрезан, полный — в блоке news-facts)'
    return body + blob


def facts_from_issue(body):
    """The news-facts JSON block of an issue body (the editor and the gate read the facts from here, not from the forum)."""
    m = re.search(r'```json\n(\{.*?\})\n```', body or '', re.S)
    return json.loads(m.group(1)) if m else None


def gh(method, path, token, body=None):
    req = urllib.request.Request(f'https://api.github.com{path}', method=method, data=json.dumps(body).encode() if body is not None else None,
                                 headers={'Authorization': f'Bearer {token}', 'Accept': 'application/vnd.github+json', **UA})
    return json.load(urllib.request.urlopen(req, timeout=30))


def make_issues(events, token):
    have = {k for i in gh('GET', f'/repos/{REPO}/issues?labels={LABEL}&state=all&per_page=100', token)
            for k in re.findall(r'\[([a-z]+-[\w-]+@[0-9a-f]{8})\]', i['title'])}
    for e in events:
        if e['event'] == 'baseline' or e.get('twin_of'):
            continue
        tag = f"{e['rec']['key']}@{e['rec']['sha'][:8]}"
        if tag in have:
            continue
        title = f"[{tag}] {'Правка: ' if e['event'] == 'edit' else ''}{e['rec']['title']}"[:200]
        gh('POST', f'/repos/{REPO}/issues', token, {'title': title, 'body': issue_body(e)[:60000], 'labels': [LABEL]})
        print('issue:', title)


def print_events(events):
    for e in events:
        r = e['rec']
        if e['event'] == 'baseline':
            continue
        print(f"{e['event']:5} [{r['key']}] {r['title'][:70]} {r['url']} sha={r['sha'][:12]}"
              + (f" twin_of={e['twin_of']}" if e.get('twin_of') else '') + f" changes={len(e['res']['changes'])} new_lines={len(e['res']['new_lines'])}"
              + f" outdated={len(e['res']['outdated'])}")
        if not e.get('twin_of') and e['res']['summary']:
            print('   ' + e['res']['summary'].replace('\n', '\n   '))


def main(argv):
    ap = argparse.ArgumentParser(description='Official Blizzard news watcher for WoW Forever')
    ap.add_argument('--state', default=os.path.join(ROOT, '.news-state'))
    ap.add_argument('--sources', default=os.path.join(ROOT, 'tools', 'news_sources.json'))
    ap.add_argument('--dry-run', action='store_true', help='read the state, write nothing')
    ap.add_argument('--since', type=float, help='on the first run, posts of the last H hours are events')
    ap.add_argument('--issues', action='store_true', help='create a GitHub issue per story (needs GITHUB_TOKEN)')
    ap.add_argument('--test', action='store_true', help='mark log lines as test')
    ap.add_argument('--report', help='write the events as JSON here (also in dry-run)')
    a = ap.parse_args(argv)
    cfg = json.load(open(a.sources, encoding='utf-8'))
    lp = os.path.join(a.state, 'ledger.json')
    ledger = json.load(open(lp, encoding='utf-8')) if os.path.exists(lp) else {}
    events = run(cfg, ledger, a.since)
    print_events(events)
    base = sum(e['event'] == 'baseline' for e in events)
    print(f"{len(events) - base} events, {base} marked as seen, {ledger.get('requests', 0)} requests"
          + (' (dry run: nothing written)' if a.dry_run else ''))
    for name, s in sorted(ledger.get('sources', {}).items()):
        if s.get('fails'):
            print(f'source {name}: {s["fails"]} failed runs in a row, last: {s.get("err")}')
    if a.report:
        with open(a.report, 'w', encoding='utf-8', newline='\n') as fh:
            json.dump([entry(e) for e in events if e['event'] != 'baseline'], fh, ensure_ascii=False, indent=1)
    if a.dry_run:
        return 0
    for p in save(a.state, ledger, events, a.test):
        print('entry:', os.path.relpath(p, a.state))
    if a.issues:
        token = os.environ.get('GITHUB_TOKEN')
        if not token:
            print('no GITHUB_TOKEN: issues skipped')
        else:
            try:
                make_issues(events, token)
            except Exception as e:   # noqa: BLE001
                print(f'skip issues: {type(e).__name__}', file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main(sys.argv[1:]))
