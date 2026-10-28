"""Discord posts of the news automation: the only source of WoW Forever news for the Gabella bot.

Input: data/official.json (level 1 notes, our own text in 9 languages built from the facts of an official Blizzard post) — a file or
https://gabella.site/wow/data/official.json. Output: one message per target of tools/news_discord.json (layout current = channels of
today, new = 📣news + forum threads of 🌍languages). Each message: our heading, up to 6 fact lines (names and numbers), a link to the
Blizzard original, a link to the site. The text of Blizzard is never copied.
One optional hint feed outside Blizzard (Wowhead RSS, only 'forever' items): English title and link as they are, footer «Source: Wowhead»,
only to targets with "hints": true, skipped when it is the same story as an official note of the last day.
An edited post edits its messages in place (message ids in the state), a reverted note is not posted again.
Webhook URLs come only from the environment (names in the config); they are never printed.

    python tools/news_discord.py --feed data/official.json --state discord_state.json [--layout current|new] [--live]
Without --live: dry run, prints the payloads, sends nothing, writes nothing. First live run with an empty state: marks all as seen."""
import argparse, html, json, os, re, sys, time, urllib.request
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from xml.etree import ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG = os.path.join(ROOT, 'tools', 'news_discord.json')
UA = {'User-Agent': 'gabella-wow-guide (+https://gabella.site/wow/)', 'Content-Type': 'application/json'}
LOGO = 'https://gabella.site/wow/assets/logo.png?v=6443c40d'
GOLD, GREY = 0xC9A54A, 0x2B2D31
ICON = {'dev-notes': '🛠', 'patch-notes': '🛠', 'hotfixes': '🛠', 'article': '📰', 'post': '📰'}
FLAG = {'ru': '🇷🇺', 'uk': '🇺🇦', 'en': '🇬🇧', 'pl': '🇵🇱', 'de': '🇩🇪', 'fr': '🇫🇷', 'es': '🇪🇸', 'it': '🇮🇹', 'pt': '🇵🇹'}
HINT_SRC = 'Source: {name}'
STOP = set('this that with from have will what when your about their into after over game games video more says just than they been first like also '
           'some only could would which there other world warcraft forever'.split())


def read(src):
    if re.match(r'https?://', src):
        req = urllib.request.Request(src, headers={'User-Agent': UA['User-Agent'], 'Cache-Control': 'no-cache'})
        return urllib.request.urlopen(req, timeout=25).read().decode('utf-8')
    return open(src, encoding='utf-8').read()


def embed(note, lang, lines=()):
    """One embed in one language: heading (link to Blizzard), fact lines, «N more», link to the site; footer with the source."""
    t = note['t'].get(lang) or note['t']['en']
    desc = list(t.get('sum', []))
    if t.get('more'):
        desc.append(t['more'])
    for other in lines:                                     # 📣news of the new layout: one post, other languages as heading lines
        o = note['t'].get(other)
        if o:
            desc.append(f"{FLAG.get(other, '')} [{o['h']}]({o.get('site', note['url'])})")
    if t.get('site'):
        desc.append(f"[{t.get('site_t', 'gabella.site')}]({t['site']})")
    foot = f"WoW Forever · {t.get('src', 'Blizzard')}" + (f" · {t['upd']}" if t.get('upd') else '') + ' · gabella.site'
    return {'title': f"{ICON.get(note.get('kind'), '📰')} {t['h']}"[:256], 'url': note['url'], 'description': '\n'.join(desc)[:4000],
            'color': GOLD, 'thumbnail': {'url': LOGO}, 'footer': {'text': foot[:2048]}, 'timestamp': note['at'].replace('Z', '+00:00') if note.get('at') else None}


def hint_embed(h, name):
    return {'title': h['title'][:256], 'url': h['url'], 'color': GREY, 'footer': {'text': HINT_SRC.format(name=name)},
            'timestamp': h['at']}


def payload(target, embeds):
    return {'username': target.get('username', 'Gabella'), 'avatar_url': LOGO, 'embeds': [{k: v for k, v in e.items() if v} for e in embeds],
            'allowed_mentions': {'parse': []}}


def tokens(s):
    return {w for w in re.findall(r"[a-z0-9']{4,}", (s or '').lower()) if w not in STOP}


def same_story(a, b):
    ta, tb = tokens(a), tokens(b)
    common = ta & tb
    return bool(common) and len(common) >= max(2, 0.5 * min(len(ta), len(tb)))


NOTES = {'dev-notes', 'patch-notes', 'hotfixes'}
WRITEUP = re.compile(r'racial|class|tuning|patch|hotfix|notes|changes|nerf|buff|talent', re.I)


def covered(h, n):
    """A hint repeats an official note: the same title, or written within 3 h after it and either sharing two words of the title
    or being a write-up of official notes (Wowhead «Racial Ability Tuning Pass» 3 min after the developer notes of 26.10)."""
    if same_story(h['title'], n.get('title_en', '')):
        return True
    try:
        dt = datetime.fromisoformat(h['at']) - datetime.fromisoformat(n['at'].replace('Z', '+00:00'))
    except (KeyError, ValueError):
        return False
    if not timedelta(hours=-1) <= dt <= timedelta(hours=3):
        return False
    return len(tokens(h['title']) & tokens(n.get('title_en', ''))) >= 2 or (n.get('kind') in NOTES and bool(WRITEUP.search(h['title'])))


def fetch_hints(cfg, now):
    """Wowhead items about Forever of the last max_age_h hours: id, title, url, at. No description: their text stays theirs."""
    root = ET.fromstring(read(cfg['rss']))
    out = []
    for it in root.iter('item'):
        title = html.unescape(it.findtext('title') or '').strip()
        url = (it.findtext('link') or '').strip()
        cats = ' '.join(c.text or '' for c in it.findall('category'))
        if not title or not url.startswith('https://www.wowhead.com/') or cfg['match'] not in (title + ' ' + cats).lower():
            continue
        at = parsedate_to_datetime(it.findtext('pubDate')).astimezone(timezone.utc)
        if now - at > timedelta(hours=cfg.get('max_age_h', 24)):
            continue
        out.append({'id': url, 'title': title, 'url': url, 'at': at.isoformat()})
    return out


def plan(notes, hints, state, targets, now):
    """[(target, kind, key, payload, edit_message_id)] to send, and the new state. Notes oldest first."""
    posted = state.setdefault('posted', {})          # note id -> {sha, sent: sha of the text sent, msgs: {target name: message id | 'seen'}}
    seen_h = state.setdefault('hints', [])
    jobs = []
    for n in sorted(notes, key=lambda n: n.get('at') or ''):
        if not re.match(r'https://', n.get('url', '')) or not n.get('t'):
            continue
        rec = posted.setdefault(n['id'], {'sha': n['sha'], 'msgs': {}})
        changed = rec['sha'] != n['sha']
        age = now - datetime.fromisoformat(n['at'].replace('Z', '+00:00')) if n.get('at') else timedelta(0)
        for tg in targets:
            if tg.get('thread_id', 0) is None:
                continue                                  # a language thread that does not exist yet
            mid = rec['msgs'].get(tg['name'])
            if mid is None and age <= timedelta(hours=48):
                jobs.append((tg, 'note', n['id'], payload(tg, [embed(n, tg['lang'], tg.get('lines', ()))]), None))   # new (or a retry)
            elif mid and mid != 'seen' and changed:
                jobs.append((tg, 'note', n['id'], payload(tg, [embed(n, tg['lang'], tg.get('lines', ()))]), mid))    # the post was edited
        rec['sha'] = n['sha']
    recent = [n for n in notes if n.get('at') and now - datetime.fromisoformat(n['at'].replace('Z', '+00:00')) <= timedelta(hours=24)]
    fresh = [h for h in hints if h['id'] not in seen_h and not any(covered(h, n) for n in recent)]
    for h in fresh[:state.get('_per_run', 2)]:
        for tg in targets:
            if tg.get('hints'):
                jobs.append((tg, 'hint', h['id'], payload(tg, [hint_embed(h, state.get('_hint_name', 'Wowhead'))]), None))
    state['hints'] = ([h['id'] for h in hints] + [x for x in seen_h if x not in {h['id'] for h in hints}])[:200]
    return jobs


def send(url, body, thread_id=None, edit=None):
    q = []
    if thread_id:
        q.append(f'thread_id={thread_id}')
    if not edit:
        q.append('wait=true')
    full = (f'{url}/messages/{edit}' if edit else url) + ('?' + '&'.join(q) if q else '')
    req = urllib.request.Request(full, method='PATCH' if edit else 'POST', data=json.dumps(body).encode('utf-8'), headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            raw = r.read()
            return r.status, (json.loads(raw).get('id') if raw else edit)
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception:          # noqa: BLE001  (the error text could carry the webhook address)
        return 0, None


def delete(state, key, cfg, layout, env=None, live=False):
    """Rollback in Discord: delete the messages of one note (by its id) through the same webhooks."""
    env = env if env is not None else os.environ
    rec = state.get('posted', {}).get(key, {})
    for tg in cfg['layouts'][layout]:
        mid, hook = rec.get('msgs', {}).get(tg['name']), (env.get(tg['secret']) or '').strip()
        if not mid or mid == 'seen':
            continue
        if not live or not hook:
            print(f"{'dry' if not live else 'skip (no secret)'}: delete {tg['name']} {key}")
            continue
        q = f"?thread_id={tg['thread_id']}" if tg.get('thread_id') else ''
        try:
            st = urllib.request.urlopen(urllib.request.Request(f'{hook}/messages/{mid}{q}', method='DELETE', headers=UA), timeout=20).status
        except urllib.error.HTTPError as e:
            st = e.code
        except Exception:      # noqa: BLE001
            st = 0
        print(f"delete {tg['name']} {key}: {st}")
        if st in (204, 404):
            rec['msgs'][tg['name']] = 'seen'


def run(notes, hints, state, cfg, layout, live, env=None, sender=send, now=None):
    env = env if env is not None else os.environ
    now = now or datetime.now(timezone.utc)
    targets = cfg['layouts'][layout]
    first = 'posted' not in state
    state['_per_run'] = cfg.get('hints', {}).get('per_run', 2)
    state['_hint_name'] = cfg.get('hints', {}).get('name', 'Wowhead')
    jobs = plan(notes, hints, state, targets, now)
    for k in ('_per_run', '_hint_name'):
        state.pop(k, None)
    if first:
        for rec in state['posted'].values():
            rec['msgs'] = {tg['name']: 'seen' for tg in targets}
        print(f'first run: {len(notes)} notes and {len(hints)} hints marked as seen, nothing sent')
        return []
    sent = []
    for tg, kind, key, body, edit in jobs:
        hook = (env.get(tg['secret']) or '').strip()
        label = f"{tg['name']} {kind} {key}" + (' (edit)' if edit else '')
        if not live:
            print(f'dry: {label}\n' + json.dumps(body, ensure_ascii=False, indent=1))
            continue
        if not hook:
            print(f'skip {label}: secret {tg["secret"]} is not set')
            continue
        st, mid = sender(hook, body, tg.get('thread_id'), edit)
        print(f'{label}: {st}')
        if 200 <= st < 300 and kind == 'note' and mid:
            state['posted'][key]['msgs'][tg['name']] = mid
        sent.append((tg['name'], kind, key, st))
        time.sleep(0.6 if sender is send else 0)
    return sent


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('--feed', default='https://gabella.site/wow/data/official.json')
    ap.add_argument('--state', required=True)
    ap.add_argument('--config', default=CONFIG)
    ap.add_argument('--layout')
    ap.add_argument('--live', action='store_true')
    ap.add_argument('--delete', metavar='NOTE_ID', help='rollback: delete the Discord messages of this note (us-2360696-7)')
    a = ap.parse_args(argv)
    cfg = json.load(open(a.config, encoding='utf-8'))
    layout = a.layout or os.environ.get('NEWS_DISCORD_LAYOUT') or cfg['layout']
    if a.delete:
        state = json.load(open(a.state, encoding='utf-8')) if os.path.exists(a.state) else {}
        delete(state, a.delete, cfg, layout, live=a.live)
        if a.live:
            with open(a.state, 'w', encoding='utf-8', newline='\n') as fh:
                json.dump(state, fh, ensure_ascii=False, indent=1)
                fh.write('\n')
        return 0
    try:
        notes = json.loads(read(a.feed))
    except Exception as e:     # noqa: BLE001
        print(f'skip: feed not read ({type(e).__name__})')
        return 0
    hints = []
    if cfg.get('hints', {}).get('enabled'):
        try:
            hints = fetch_hints(cfg['hints'], datetime.now(timezone.utc))
        except Exception as e:  # noqa: BLE001
            print(f'hints skipped ({type(e).__name__})')
    state = json.load(open(a.state, encoding='utf-8')) if os.path.exists(a.state) else {}
    run(notes, hints, state, cfg, layout, a.live)
    if a.live:
        with open(a.state, 'w', encoding='utf-8', newline='\n') as fh:
            json.dump(state, fh, ensure_ascii=False, indent=1)
            fh.write('\n')
    return 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main(sys.argv[1:]))
