"""Level 1 of the news automation: a short note «Blizzard published developer notes of 26.10 (beta)» right away, in 9 languages.

No model and no site build: fixed templates per kind of post, the date in the format of the language, the English title of Blizzard
as it is, a link. Written to data/official.json (outside assets/: Cloudflare caches assets for 30 days; data/ is not cached), read by
the home «Fresh» block and by /guides/news/. An edited post updates its note and gets «updated <date>».
A note once published is remembered in the ledger (published = sha): a reverted commit does not come back on the next run.

    python tools/news_publish.py --state DIR [--out data/official.json] [--dry-run]"""
import argparse, json, os, re, sys
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from news_parse import norm     # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'data', 'official.json')
LANGS = ['ru', 'en', 'uk', 'de', 'fr', 'es', 'pt', 'it', 'pl']
KEEP = 40
MAX_AGE_H = 48     # entries/ keeps every story since the first run: older ones are history, not news (the first live run had 33)
PER_RUN = 3        # at most this many notes per run, the newest first; the rest of the fresh ones go in the next runs
MONTHS_EN = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# {d}: date of the post in the language format
HEAD = {
    'dev-notes': {'ru': 'Заметки разработчиков от {d}', 'en': 'Developer notes of {d}', 'uk': 'Нотатки розробників від {d}',
                  'de': 'Entwicklerhinweise vom {d}', 'fr': 'Notes des développeurs du {d}', 'es': 'Notas de los desarrolladores del {d}',
                  'pt': 'Notas dos desenvolvedores de {d}', 'it': 'Note degli sviluppatori del {d}', 'pl': 'Notatki deweloperów z {d}'},
    'patch-notes': {'ru': 'Описание обновления от {d}', 'en': 'Patch notes of {d}', 'uk': 'Опис оновлення від {d}',
                    'de': 'Patchnotes vom {d}', 'fr': 'Notes de mise à jour du {d}', 'es': 'Notas del parche del {d}',
                    'pt': 'Notas da atualização de {d}', 'it': 'Note della patch del {d}', 'pl': 'Opis zmian z {d}'},
    'hotfixes': {'ru': 'Хотфиксы от {d}', 'en': 'Hotfixes of {d}', 'uk': 'Хотфікси від {d}', 'de': 'Hotfixes vom {d}',
                 'fr': 'Correctifs du {d}', 'es': 'Correcciones del {d}', 'pt': 'Hotfixes de {d}', 'it': 'Hotfix del {d}', 'pl': 'Hotfixy z {d}'},
    'article': {'ru': 'Новость Blizzard от {d}', 'en': 'Blizzard news of {d}', 'uk': 'Новина Blizzard від {d}', 'de': 'Blizzard-News vom {d}',
                'fr': 'Actualité Blizzard du {d}', 'es': 'Noticia de Blizzard del {d}', 'pt': 'Notícia da Blizzard de {d}',
                'it': 'Notizia Blizzard del {d}', 'pl': 'Wiadomość Blizzarda z {d}'},
    'post': {'ru': 'Сообщение Blizzard от {d}', 'en': 'Blizzard post of {d}', 'uk': 'Повідомлення Blizzard від {d}', 'de': 'Blizzard-Beitrag vom {d}',
             'fr': 'Message de Blizzard du {d}', 'es': 'Mensaje de Blizzard del {d}', 'pt': 'Mensagem da Blizzard de {d}',
             'it': 'Messaggio Blizzard del {d}', 'pl': 'Wpis Blizzarda z {d}'},
}
BETA = {'ru': 'бета', 'en': 'beta', 'uk': 'бета', 'de': 'Beta', 'fr': 'bêta', 'es': 'beta', 'pt': 'beta', 'it': 'beta', 'pl': 'beta'}
UPD = {'ru': 'обновлено {d}', 'en': 'updated {d}', 'uk': 'оновлено {d}', 'de': 'aktualisiert am {d}', 'fr': 'mis à jour le {d}',
       'es': 'actualizado el {d}', 'pt': 'atualizado em {d}', 'it': 'aggiornato il {d}', 'pl': 'zaktualizowano {d}'}
SRC = {'ru': 'Blizzard, на английском', 'en': 'Blizzard', 'uk': 'Blizzard, англійською', 'de': 'Blizzard, auf Englisch',
       'fr': 'Blizzard, en anglais', 'es': 'Blizzard, en inglés', 'pt': 'Blizzard, em inglês', 'it': 'Blizzard, in inglese', 'pl': 'Blizzard, po angielsku'}
# technical posts are not news for players (the old rule of news-3h: realm restarts, short maintenance)
SKIP = re.compile(r'realm restart|restarts? today|maintenance|will return shortly|server (?:issues|status)|known issues', re.I)


def day(iso, lang):
    d = datetime.fromisoformat(iso.replace('Z', '+00:00'))
    return f'{MONTHS_EN[d.month - 1]} {d.day}' if lang == 'en' else f'{d.day:02d}.{d.month:02d}'


TITLED = {'article', 'post'}    # an article or a single post: its own English title says more than «Blizzard news of 26.10»


def texts(kind, beta, at, upd=None, title=None):
    out = {}
    for lang in LANGS:
        if kind in TITLED and title:
            out[lang] = {'h': title, 'en': 1, 'src': SRC[lang], **({'upd': UPD[lang].format(d=day(upd, lang))} if upd else {})}
            continue
        h = HEAD.get(kind, HEAD['post'])[lang].format(d=day(at, lang))
        if beta:
            h += f' ({BETA[lang]})'
        out[lang] = {'h': h, 'src': SRC[lang], **({'upd': UPD[lang].format(d=day(upd, lang))} if upd else {})}
    return out


# ---------- our own short account of the facts (Discord, the news page): names and numbers, never the sentences of the post ----------
MORE = {'ru': 'Ещё изменений: {n}', 'en': '{n} more changes', 'uk': 'Ще змін: {n}', 'de': 'Weitere Änderungen: {n}', 'fr': 'Autres changements : {n}',
        'es': 'Más cambios: {n}', 'pt': 'Mais mudanças: {n}', 'it': 'Altre modifiche: {n}', 'pl': 'Więcej zmian: {n}'}
REMOVED = {'ru': 'убрано', 'en': 'removed', 'uk': 'прибрано', 'de': 'entfernt', 'fr': 'supprimé', 'es': 'eliminado', 'pt': 'removido',
           'it': 'rimosso', 'pl': 'usunięte'}
ADDED = {'ru': 'новое', 'en': 'new', 'uk': 'нове', 'de': 'neu', 'fr': 'nouveau', 'es': 'nuevo', 'pt': 'novo', 'it': 'nuovo', 'pl': 'nowe'}
NOLONGER = {'ru': 'ограничено', 'en': 'narrowed', 'uk': 'обмежено', 'de': 'eingeschränkt', 'fr': 'restreint', 'es': 'limitado',
            'pt': 'restrito', 'it': 'limitato', 'pl': 'ograniczone'}
MORE_SITE = {'ru': 'Подробнее на сайте', 'en': 'More on the site', 'uk': 'Детальніше на сайті', 'de': 'Mehr auf der Seite', 'fr': 'Plus sur le site',
             'es': 'Más en la web', 'pt': 'Mais no site', 'it': 'Di più sul sito', 'pl': 'Więcej na stronie'}
UNIT = {'s': {'ru': 'с', 'uk': 'с', 'en': 'sec', 'de': 'Sek.'}, 'min': {'ru': 'мин', 'uk': 'хв', 'de': 'Min.'}, 'h': {'ru': 'ч', 'uk': 'год', 'de': 'Std.', 'pl': 'godz.'},
        'yd': {'ru': 'м', 'uk': 'м', 'en': 'yd'}}
SKYBORNE = {'ru': 'Скайборн', 'uk': 'Skyborne'}
SITE_NEWS = 'https://gabella.site/wow/{p}guides/news/'
LIMIT = 6
_NAMES = {}


def names(lang):
    """Race and class names of the site (assets/hero/<lang>.json) and ability names (i18n/names.json)."""
    if lang not in _NAMES:
        hero = os.path.join(ROOT, 'assets', 'hero', f'{lang}.json')
        h = json.load(open(hero, encoding='utf-8')) if os.path.exists(hero) else {}
        _NAMES[lang] = {**h.get('rn', {}), **h.get('cn', {}), 'skyborne': SKYBORNE.get(lang, 'Skyborne')}
        if 'abil' not in _NAMES:
            _NAMES['abil'] = json.load(open(os.path.join(ROOT, 'i18n', 'names.json'), encoding='utf-8'))
    return _NAMES[lang]


def num(v, u, lang):
    s = str(v)
    if lang != 'en':
        s = s.replace('.', ',')
    if u == '%':
        return s + '%'
    if not u:
        return s
    return f"{s} {UNIT.get(u, {}).get(lang, u)}"


def ability(name, lang):
    loc = names(lang) and _NAMES['abil'].get(name, {}).get(lang)
    if lang == 'ru' and loc and loc != name:
        return f'{loc} ({name})'
    return loc or name


def summary(changes, lang):
    """Up to LIMIT lines «Subject · Ability: 2% → 1%» from the facts, number changes first; the rest is a count."""
    nm = names(lang)
    rank = {'changed': 0, 'removed': 1, 'replaced': 1, 'added': 2, 'no_longer': 3}
    useful = [c for c in changes if c.get('abilities') and c['kind'] in rank and (c['kind'] != 'changed' or c.get('pairs'))]
    useful.sort(key=lambda c: rank[c['kind']])
    lines = []
    for c in useful[:LIMIT]:
        subj = nm.get(c['subject'].get('id'), '') if c['subject'].get('type') in ('race', 'class') else ''
        what = ability(c['abilities'][0], lang)
        if c['kind'] == 'changed':
            tail = ', '.join(f"{num(p['old'], p['old_unit'], lang)} → {num(p['new'], p['unit'], lang)}" for p in c['pairs'])
        else:
            tail = {'removed': REMOVED, 'replaced': REMOVED, 'added': ADDED, 'no_longer': NOLONGER}[c['kind']][lang]
        lines.append(f"{subj + ' · ' if subj else ''}{what}: {tail}")
    rest = len(changes) - len(lines)
    return {'sum': lines, **({'more': MORE[lang].format(n=rest)} if rest > 0 and lines else {}),
            'site': SITE_NEWS.format(p='' if lang == 'ru' else lang + '/'), 'site_t': MORE_SITE[lang]}


def publishable(e):
    """A primary story (not the EU copy, not the first-run baseline) that players care about.
    Replies of developers inside topics go to the editor's issue only; posts and articles with a technical title are skipped."""
    if e.get('event') == 'baseline' or e.get('twin_of') or SKIP.search(e.get('title') or ''):
        return False
    kind = e['short_news']['kind']
    if kind == 'post' and e.get('source') == 'forum' and (e.get('post') or 1) > 1:
        return False
    return True


def item(e, old=None):
    s = e['short_news']
    upd = e['detected_at'] if old and e['event'] == 'edit' else (old or {}).get('upd')
    t = texts(s['kind'], s['beta'], s['at'], upd, s['title_en'])
    changes = [c for c in e.get('changes', []) if c.get('kind') not in ('note', 'fix')]
    for lang in LANGS:
        t[lang].update(summary(changes, lang))
    return {'id': e['key'], 'sha': e['sha'][:8], 'date': s['date'], 'at': s['at'], 'url': s['url'], 'kind': s['kind'], 'beta': s['beta'],
            'title_en': s['title_en'], 'n': len(changes), **({'upd': upd} if upd else {}), 't': t}


def when(s):
    return datetime.fromisoformat(s.replace('Z', '+00:00'))


def apply(entries, current, ledger, now=None, max_age_h=MAX_AGE_H, limit=PER_RUN):
    """New notes on top, edits update their note; returns (notes, [(key, sha8, title)] changed).
    entries/ holds every version of every story ever seen: only the latest version of each post counts, a new note only for a post
    of the last max_age_h hours, an edit only if found in that time, and at most limit notes per run."""
    now = now or datetime.now(timezone.utc)
    by = {n['id']: n for n in current}
    pub = ledger.setdefault('published', {})
    last = {}
    for e in entries:
        if publishable(e) and (e['key'] not in last or (e.get('detected_at') or '') >= (last[e['key']].get('detected_at') or '')):
            last[e['key']] = e
    todo = []
    for k, e in last.items():
        if pub.get(k) == e['sha'][:8]:
            continue
        if k in by:
            since = e.get('detected_at') or e['short_news']['at']      # an edit of a note on the site
        elif k in pub:
            continue          # published before and removed by a revert: stays removed
        else:
            since = e['short_news']['at']                               # a new note: the post itself must be fresh
        if now - when(since) <= timedelta(hours=max_age_h):
            todo.append(e)
    # the same story as a news article and a forum post, seen in different runs (twin_of links only one run): one note, the article
    titles = {norm(n.get('title_en')): n['id'] for n in current}
    one = {}
    for e in sorted(todo, key=lambda e: (e.get('source') != 'article', e['short_news']['at'])):
        t = norm(e['title'])
        if titles.get(t, e['key']) == e['key'] and t not in one:
            one[t] = e
    todo = sorted(one.values(), key=lambda e: e['short_news']['at'], reverse=True)[:max(limit, 0)]
    changed = []
    for e in sorted(todo, key=lambda e: e['short_news']['at']):
        k = e['key']
        by[k] = item(e, by.get(k))
        pub[k] = e['sha'][:8]
        changed.append((k, e['sha'][:8], e['title']))
    notes = sorted(by.values(), key=lambda n: n['at'], reverse=True)[:KEEP]
    return notes, changed


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('--state', required=True)
    ap.add_argument('--out', default=OUT)
    ap.add_argument('--entries', help='JSON list of entries (default: all of entries/ in the state; apply() keeps the fresh latest versions)')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--max-age-h', type=float, default=MAX_AGE_H, help='only posts (and edits) of the last H hours')
    ap.add_argument('--limit', type=int, default=PER_RUN, help='at most N notes per run')
    ap.add_argument('--unmark', action='store_true', help='the push failed: forget the notes of published.txt, the next run retries')
    a = ap.parse_args(argv)
    lp = os.path.join(a.state, 'ledger.json')
    ledger = json.load(open(lp, encoding='utf-8')) if os.path.exists(lp) else {}
    if a.unmark:
        pf = os.path.join(a.state, 'published.txt')
        keys = [l.split('@')[0] for l in open(pf, encoding='utf-8').read().split('\n') if l.strip()] if os.path.exists(pf) else []
        for k in keys:
            ledger.get('published', {}).pop(k, None)
        with open(lp, 'w', encoding='utf-8', newline='\n') as fh:
            json.dump(ledger, fh, ensure_ascii=False, indent=1, sort_keys=True)
            fh.write('\n')
        print(f'unmarked {len(keys)}')
        return 0
    if a.entries:
        entries = json.load(open(a.entries, encoding='utf-8'))
    else:
        d = os.path.join(a.state, 'entries')
        entries = [json.load(open(os.path.join(d, f), encoding='utf-8')) for f in sorted(os.listdir(d))] if os.path.isdir(d) else []
    current = json.load(open(a.out, encoding='utf-8')) if os.path.exists(a.out) else []
    notes, changed = apply(entries, current, ledger, max_age_h=a.max_age_h, limit=a.limit)
    for k, sha, title in changed:
        print(f'note: {k}@{sha} {title}')
    print(f'{len(changed)} notes changed' + (' (dry run)' if a.dry_run else ''))
    if a.dry_run or not changed:
        return 0
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with open(a.out, 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(notes, fh, ensure_ascii=False, indent=1)
        fh.write('\n')
    with open(lp, 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(ledger, fh, ensure_ascii=False, indent=1, sort_keys=True)
        fh.write('\n')
    with open(os.path.join(a.state, 'published.txt'), 'w', encoding='utf-8', newline='\n') as fh:   # for the commit and its tag
        fh.write('\n'.join(f'{k}@{sha}\t{t}' for k, sha, t in changed) + '\n')
    return 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main(sys.argv[1:]))
