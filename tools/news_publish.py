"""Level 1 of the news automation: a short note «Blizzard published developer notes of 26.10 (beta)» right away, in 9 languages.

No model and no site build: fixed templates per kind of post, the date in the format of the language, the English title of Blizzard
as it is, a link. Written to data/official.json (outside assets/: Cloudflare caches assets for 30 days; data/ is not cached), read by
the home «Fresh» block and by /guides/news/. An edited post updates its note and gets «updated <date>».
A note once published is remembered in the ledger (published = sha): a reverted commit does not come back on the next run.

    python tools/news_publish.py --state DIR [--out data/official.json] [--dry-run]"""
import argparse, json, os, re, sys
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'data', 'official.json')
LANGS = ['ru', 'en', 'uk', 'de', 'fr', 'es', 'pt', 'it', 'pl']
KEEP = 40
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
    return {'id': e['key'], 'sha': e['sha'][:8], 'date': s['date'], 'at': s['at'], 'url': s['url'], 'kind': s['kind'], 'beta': s['beta'],
            'title_en': s['title_en'], **({'upd': upd} if upd else {}), 't': texts(s['kind'], s['beta'], s['at'], upd, s['title_en'])}


def apply(entries, current, ledger):
    """New notes on top, edits update their note; returns (notes, [(key, sha8, title)] changed)."""
    by = {n['id']: n for n in current}
    pub = ledger.setdefault('published', {})
    changed = []
    for e in sorted(entries, key=lambda e: e['short_news']['at']):
        if not publishable(e):
            continue
        k = e['key']
        if k in pub and pub[k] == e['sha'][:8]:
            continue
        if k in pub and k not in by and e['event'] != 'edit':
            continue          # published before and removed by a revert: stays removed
        if e['event'] == 'edit' and k not in by:
            continue          # an edit of a post we never showed (or reverted): no note
        by[k] = item(e, by.get(k))
        pub[k] = e['sha'][:8]
        changed.append((k, e['sha'][:8], e['title']))
    notes = sorted(by.values(), key=lambda n: n['at'], reverse=True)[:KEEP]
    return notes, changed


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('--state', required=True)
    ap.add_argument('--out', default=OUT)
    ap.add_argument('--entries', help='JSON list of entries (default: entries/ of the state written in this run, see --since-log)')
    ap.add_argument('--dry-run', action='store_true')
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
    notes, changed = apply(entries, current, ledger)
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
