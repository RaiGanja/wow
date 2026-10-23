"""Official in-game names for de/fr/es/pt/it, taken from the Wowhead tooltip API.

Reads i18n/names_ids.json and writes i18n/names.json:
    {"<English name>": {"de": ..., "fr": ..., "es": ..., "pt": ..., "it": ...}}

names_ids.json entry kinds:
    {"type": "spell|zone|npc|item|object|quest", "id": 123}
        optional "env": Wowhead dataEnv for en/fr/de/es/pt (default 4 = Classic Era;
                 8 = Wrath Classic, 1 = retail) for things that never existed in Classic Era
        optional "en": the exact English name on Wowhead when the site spells it differently
        optional "it": {"type": ..., "id": ...} retail entity for Italian when the id differs there
        optional "note"
    {"forever": true}                    new in WoW Forever: all five values = English name
    {"manual": {"de": ...}, "note": ""}  no Wowhead entity (class/spec/race names, compositions)

Every id is verified: its English name (locale 0) must equal the expected English name.
Italian does not exist in Classic, so it comes from retail (dataEnv=1, locale=9); the retail
entity is verified the same way, otherwise Italian falls back to English and is reported.

Usage: python tools/wowhead_names.py [--cache FILE]   (stdlib only; <= 4 requests/second)
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'i18n', 'names_ids.json')
OUT = os.path.join(ROOT, 'i18n', 'names.json')
LOCALES = {'en': 0, 'fr': 2, 'de': 3, 'es': 6, 'pt': 8, 'it': 9}
LANGS = ('de', 'fr', 'es', 'pt', 'it')
URL = 'https://nether.wowhead.com/tooltip/{type}/{id}?dataEnv={env}&locale={loc}'
DELAY = 0.25

_cache = {}
_last = [0.0]


def norm(s):
    return (s or '').replace('’', "'").replace('‘', "'").strip().lower()


def fetch(typ, ident, env, loc):
    """Return the entity name, or None when Wowhead has no such entity."""
    key = '%s/%s/%s/%s' % (typ, ident, env, loc)
    if key in _cache:
        return _cache[key]
    url = URL.format(type=typ, id=ident, env=env, loc=loc)
    name = None
    for attempt in range(5):
        wait = DELAY - (time.time() - _last[0])
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.time()
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'wfpages-names/1.0'})
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.loads(r.read().decode('utf-8'))
            name = data.get('name') if not data.get('error') else None
            break
        except urllib.error.HTTPError as e:
            if e.code == 404:
                break
            time.sleep(2 + attempt * 3)
        except Exception:
            time.sleep(2 + attempt * 3)
    else:
        raise RuntimeError('Wowhead unreachable: ' + url)
    _cache[key] = name
    return name


def resolve(en_name, e, report):
    typ, ident, env = e['type'], e['id'], e.get('env', 4)
    want = e.get('en', en_name)
    got = fetch(typ, ident, env, LOCALES['en'])
    if norm(got) != norm(want):
        report['unresolved'].append('%s: %s/%s env %s is "%s"' % (en_name, typ, ident, env, got))
        return None
    out = {}
    for lang in ('de', 'fr', 'es', 'pt'):
        n = fetch(typ, ident, env, LOCALES[lang])
        if not n:
            report['warn'].append('%s: no %s name, kept English' % (en_name, lang))
            n = en_name
        out[lang] = n
    it = e.get('it', {'type': typ, 'id': ident})
    it_en = fetch(it['type'], it['id'], 1, LOCALES['en'])
    it_name = fetch(it['type'], it['id'], 1, LOCALES['it']) if norm(it_en) == norm(want) else None
    if not it_name:
        report['it_english'].append('%s (retail %s/%s is "%s")' % (en_name, it['type'], it['id'], it_en))
        it_name = en_name
    elif norm(it_name) == norm(want) and any(norm(out[l]) != norm(want) for l in ('de', 'fr', 'es', 'pt')):
        report['it_english'].append('%s (retail Italian equals English)' % en_name)
    out['it'] = it_name
    report['wowhead'] += 1
    return out


def main():
    if '--cache' in sys.argv:
        path = sys.argv[sys.argv.index('--cache') + 1]
        if os.path.exists(path):
            _cache.update(json.load(open(path, encoding='utf-8')))
    else:
        path = None
    ids = json.load(open(SRC, encoding='utf-8'))
    report = {'wowhead': 0, 'manual': 0, 'forever': 0, 'unresolved': [], 'warn': [], 'it_english': []}
    names = {}
    try:
        for en_name in sorted(ids):
            e = ids[en_name]
            if e.get('forever'):
                names[en_name] = {l: en_name for l in LANGS}
                report['forever'] += 1
            elif 'manual' in e:
                m = e['manual']
                missing = [l for l in LANGS if not m.get(l)]
                if missing:
                    report['unresolved'].append('%s: manual without %s' % (en_name, ','.join(missing)))
                    continue
                names[en_name] = {l: m[l] for l in LANGS}
                report['manual'] += 1
            elif 'type' in e and 'id' in e:
                r = resolve(en_name, e, report)
                if r:
                    names[en_name] = r
            else:
                report['unresolved'].append('%s: no type/id, manual or forever' % en_name)
    finally:
        if path:
            json.dump(_cache, open(path, 'w', encoding='utf-8'), ensure_ascii=False)
    with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
        json.dump({k: names[k] for k in sorted(names)}, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('total %d, wowhead %d, manual %d, forever %d, unresolved %d'
          % (len(ids), report['wowhead'], report['manual'], report['forever'], len(report['unresolved'])))
    for k in ('unresolved', 'warn', 'it_english'):
        for line in report[k]:
            print('%s: %s' % (k, line))
    return 1 if report['unresolved'] else 0


if __name__ == '__main__':
    sys.exit(main())
