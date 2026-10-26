"""Talent icons for content/talents/<class>.json: the icon name from the Blizzard Game Data API, the picture from Blizzard's
render CDN, one sprite per class (assets/talents/<class>.webp, one row of 56 x 56 cells: the CDN has no bigger size).

    python tools/talent_icons.py [paladin ...]            # icon names from the API (key in ~/.secrets/bnet.env)
    python tools/talent_icons.py paladin --map icons.json  # icon names from a file {talent id: icon name} (tests)

The key file holds two lines, BNET_ID=... and BNET_SECRET=... (a client of develop.battle.net); its values are never printed.
A talent is matched by the spell ids we know (the client's, i18n/names_ids.json); the API answer also carries the icon's file id,
which must be the client's own (from the addon), so a wrong spell id does not slip in. The API's names in de/es/fr/it/pt fill
the languages the client dump lacks. Not found -> no icon: talents.py draws two letters on a plate, the list is printed.
Never from wow.zamimg.com (Wowhead) or Icy Veins: their terms forbid it."""
import argparse, base64, io, json, os, sys, urllib.error, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY = os.path.join(os.path.expanduser('~'), '.secrets', 'bnet.env')
CACHE = os.path.join(HERE, 'tools', '.talent-icons')
CDN = 'https://render.worldofwarcraft.com/eu/icons/56/{}.jpg'
API = 'https://eu.api.blizzard.com'
API_LANGS = {'de_DE': 'de', 'es_ES': 'es', 'fr_FR': 'fr', 'it_IT': 'it', 'pt_BR': 'pt', 'ru_RU': 'ru', 'en_US': 'en'}
CELL = 56


def get(url, token=None):
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {token}'} if token else {})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


def token():
    env = dict(l.strip().split('=', 1) for l in open(KEY, encoding='utf-8') if '=' in l)
    auth = base64.b64encode(f'{env["BNET_ID"]}:{env["BNET_SECRET"]}'.encode()).decode()
    req = urllib.request.Request('https://oauth.battle.net/token', data=b'grant_type=client_credentials',
                                 headers={'Authorization': f'Basic {auth}', 'Content-Type': 'application/x-www-form-urlencoded'})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)['access_token']


def from_api(data, tok):
    """{talent id: icon name}; also fills missing names of the API languages. Prints what it could not prove."""
    ids = json.load(open(os.path.join(HERE, 'i18n', 'names_ids.json'), encoding='utf-8'))
    by_file, out, miss = {}, {}, []
    talents = [t for tr in data['trees'] for t in tr['talents']]
    for t in talents:
        cand = list(t.get('spells') or [])
        x = ids.get(t['n'].get('en', ''))
        if isinstance(x, dict) and x.get('type') == 'spell' and x['id'] not in cand:
            cand.append(x['id'])
        for sid in cand:
            m = get(f'{API}/data/wow/media/spell/{sid}?namespace=static-eu', tok)
            a = next((a for a in json.loads(m)['assets'] if a['key'] == 'icon'), None) if m else None
            if not a:
                continue
            if t.get('file') and a.get('file_data_id') != t['file']:
                print(f'  {t["id"]} {t["n"].get("en")}: spell {sid} has another icon ({a.get("file_data_id")} != {t["file"]})')
                continue
            name = a['value'].rsplit('/', 1)[1].rsplit('.', 1)[0]
            out[t['id']] = name
            by_file[a.get('file_data_id')] = name
            s = get(f'{API}/data/wow/spell/{sid}?namespace=static-eu', tok)
            if s:
                for loc, lang in API_LANGS.items():
                    v = (json.loads(s).get('name') or {}).get(loc)
                    if v and lang not in t['n']:
                        t['n'][lang] = v
            break
    for t in talents:                                         # the same picture as a talent we did prove
        if t['id'] not in out and t.get('file') in by_file:
            out[t['id']] = by_file[t['file']]
    miss = [f'{t["id"]} {t["n"].get("en") or t["n"].get("ru")}' for t in talents if t['id'] not in out]
    return out, miss


def picture(name):
    os.makedirs(CACHE, exist_ok=True)
    p = os.path.join(CACHE, f'{name}.jpg')
    if not os.path.isfile(p):
        b = get(CDN.format(urllib.parse.quote(name)))
        if not b:
            return None
        open(p, 'wb').write(b)
    return p


def sprite(cid, data, icons, out_dir):
    from PIL import Image
    names = []
    for tr in data['trees']:
        for t in tr['talents']:
            n = icons.get(t['id'])
            p = picture(n) if n else None
            t.pop('icon', None), t.pop('iname', None)
            if not p:
                continue
            if n not in names:
                names.append(n)
            t['icon'], t['iname'] = names.index(n), n
    img = Image.new('RGB', (CELL * max(len(names), 1), CELL), (22, 24, 28))
    for i, n in enumerate(names):
        img.paste(Image.open(picture(n)).convert('RGB').resize((CELL, CELL), Image.LANCZOS), (i * CELL, 0))
    os.makedirs(out_dir, exist_ok=True)
    buf = io.BytesIO()
    img.save(buf, 'WEBP', quality=82, method=6)
    open(os.path.join(out_dir, f'{cid}.webp'), 'wb').write(buf.getvalue())
    data['sprite'] = len(names)
    return len(names), len(buf.getvalue())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('classes', nargs='*')
    ap.add_argument('--data', default=os.path.join(HERE, 'content', 'talents'))
    ap.add_argument('--assets', default=os.path.join(HERE, 'assets', 'talents'))
    ap.add_argument('--map')
    a = ap.parse_args()
    cids = a.classes or sorted(f[:-5] for f in os.listdir(a.data) if f.endswith('.json'))
    tok = None if a.map else token()
    for cid in cids:
        p = os.path.join(a.data, f'{cid}.json')
        data = json.load(open(p, encoding='utf-8'))
        if a.map:
            icons, miss = json.load(open(a.map, encoding='utf-8')), []
            icons = {k: v for k, v in icons.items() if v}
        else:
            icons, miss = from_api(data, tok)
        n, size = sprite(cid, data, icons, a.assets)
        json.dump(data, open(p, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
        left = [f'{t["id"]} {t["n"].get("en") or t["n"].get("ru")}' for tr in data['trees'] for t in tr['talents'] if t.get('icon') is None]
        print(f'{cid}: {n} icons, sprite {size // 1024} KB; no icon: {len(left)}')
        for x in left:
            print('   ', x)


if __name__ == '__main__':
    sys.exit(main())
