"""Talent icons for content/talents/<class>.json: pictures from Blizzard's render CDN, one sprite per class
(assets/talents/<class>.webp, one row of 56 x 56 cells: the CDN has no bigger size).

    python tools/talent_icons.py [paladin ...]            # by the client's icon file id (from the addon), API as a fallback
    python tools/talent_icons.py paladin --map icons.json  # icon names from a file {talent id: icon name} (tests)
    python tools/talent_icons.py --retail                  # before the dump: refresh tools/talent_icons_api.json first

The CDN serves an icon by its file id as well as by name (render.worldofwarcraft.com/eu/icons/56/135972.jpg, checked 26.10),
so the addon's file id is enough and needs no key. The Game Data API knows only retail spells (11 of the 147 talents of our
tables on 26.10), so it is only the fallback for a talent without a file id, and it fills the de/es/fr/it/pt names it knows.
The key file (~/.gabella-keys/blizzard.env: BLIZZARD_CLIENT_ID=, BLIZZARD_CLIENT_SECRET=) is the site's Battle.net client:
read-only client_credentials calls only, never print the values, never touch the client on develop.battle.net (it signs readers in).
Not found -> no icon: talents.py draws two letters on a plate, the list is printed.
Never from wow.zamimg.com (Wowhead) or Icy Veins: their terms forbid it."""
import argparse, base64, io, json, os, sys, urllib.error, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY = os.environ.get('GABELLA_BNET_KEY') or os.path.join(os.path.expanduser('~'), '.gabella-keys', 'blizzard.env')
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
        if e.code in (403, 404):                                # the CDN answers 403 for an unknown icon
            return None
        raise


def token():
    env = dict(l.strip().split('=', 1) for l in open(KEY, encoding='utf-8') if '=' in l)
    cid, sec = env.get('BLIZZARD_CLIENT_ID') or env['BNET_ID'], env.get('BLIZZARD_CLIENT_SECRET') or env['BNET_SECRET']
    auth = base64.b64encode(f'{cid}:{sec}'.encode()).decode()
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


RETAIL_MAP = os.path.join(HERE, 'tools', 'talent_icons_api.json')
SHIP = ('same-id', 'class-tree', 'name-unique')     # sources of tools/talent_icons_api.json that are drawn
CLASS_NAME = {'druid': 'Druid', 'hunter': 'Hunter', 'mage': 'Mage', 'paladin': 'Paladin', 'priest': 'Priest',
              'rogue': 'Rogue', 'shaman': 'Shaman', 'warlock': 'Warlock', 'warrior': 'Warrior'}


def api_json(path, tok):
    b = get(f'{API}{path}{"&" if "?" in path else "?"}locale=en_US', tok)
    return json.loads(b) if b else None


def retail(cids, data_dir, tok):
    """Before the addon dump, for talents with no icon name: the Game Data API's own icon (static-eu, the only namespace
    with spells; static-classic*-eu have items but no spell or talent endpoints, checked 30.10). In order:
      same-id      the talent's spell id exists in the API;
      class-tree   a talent of the same class in the API's talent trees has the same English name;
      name-unique  the spell search finds this exact English name and all hits share one icon. The search does not say
                   whose spell it is, so only an icon of the original client (file id < 200000: the old art the classic
                   clients share) is used; a modern icon is kept in the file as 'name-modern' and NOT drawn (a mage icon
                   for a druid talent would be worse than the plate).
    Writes tools/talent_icons_api.json {class:talent id: {file, src, spell}}; the CDN serves the picture by that file id.
    Several icons for one name or no hit -> nothing (two letters on a plate)."""
    norm = lambda s: s.replace('’', "'").strip().lower()
    media = {}

    def icon(sid):
        if sid not in media:
            j = api_json(f'/data/wow/media/spell/{sid}?namespace=static-eu', tok)
            a = next((a for a in (j or {}).get('assets', []) if a['key'] == 'icon'), None)
            media[sid] = a.get('file_data_id') if a else None
        return media[sid]

    def walk(o, names):
        if isinstance(o, dict):
            sp = (o.get('spell_tooltip') or {}).get('spell')
            if sp:
                names.setdefault(norm(sp['name']), sp['id'])
            for v in o.values():
                walk(v, names)
        elif isinstance(o, list):
            for v in o:
                walk(v, names)

    idx = api_json('/data/wow/talent-tree/index?namespace=static-eu', tok)
    out = json.load(open(RETAIL_MAP, encoding='utf-8')) if os.path.isfile(RETAIL_MAP) else {}
    for cid in cids:
        names = {}
        tree = next((c for c in idx['class_talent_trees'] if c['name'] == CLASS_NAME[cid]), None)
        if tree:
            tid = tree['key']['href'].split('talent-tree/')[1].split('?')[0]
            for s in idx['spec_talent_trees']:
                if f'talent-tree/{tid}/' in s['key']['href']:
                    walk(api_json(s['key']['href'].split('eu.api.blizzard.com')[1].split('?')[0] + '?namespace=static-eu', tok), names)
        data = json.load(open(os.path.join(data_dir, f'{cid}.json'), encoding='utf-8'))
        for t in (t for tr in data['trees'] for t in tr['talents']):
            out.pop(f'{cid}:{t["id"]}', None)
            if t.get('iname0'):
                continue
            en = t['n']['en'].replace('’', "'")
            hit = next(((f, 'same-id', s) for s in t.get('spells') or [] if (f := icon(s))), None)
            if not hit and names.get(norm(en)) and icon(names[norm(en)]):
                hit = (icon(names[norm(en)]), 'class-tree', names[norm(en)])
            if not hit:
                j = api_json('/data/wow/search/spell?namespace=static-eu&_pageSize=100&name.en_US=' + urllib.parse.quote(en), tok)
                ids = [r['data']['id'] for r in (j or {}).get('results', []) if norm(r['data']['name'].get('en_US', '')) == norm(en)]
                files = {icon(s): s for s in ids[:30] if icon(s)}
                if len(files) == 1:
                    f, s = next(iter(files.items()))
                    hit = (f, 'name-unique' if f < 200000 else 'name-modern', s)
                elif files:
                    print(f'  {cid} {en}: {len(files)} icons for one name, left as a plate')
            if hit:
                out[f'{cid}:{t["id"]}'] = {'file': hit[0], 'src': hit[1], 'spell': hit[2], 'en': t['n']['en']}
    json.dump(dict(sorted(out.items())), open(RETAIL_MAP, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
    return out


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
    ap.add_argument('--retail', action='store_true', help='refresh tools/talent_icons_api.json from the Game Data API first')
    a = ap.parse_args()
    cids = a.classes or sorted(f[:-5] for f in os.listdir(a.data) if f.endswith('.json'))
    tok = None
    if a.retail:
        tok = token()
        retail(cids, a.data, tok)
    api_map = json.load(open(RETAIL_MAP, encoding='utf-8')) if os.path.isfile(RETAIL_MAP) else {}
    for cid in cids:
        p = os.path.join(a.data, f'{cid}.json')
        data = json.load(open(p, encoding='utf-8'))
        if a.map:
            icons = {k: v for k, v in json.load(open(a.map, encoding='utf-8')).items() if v}
        elif data.get('basis'):                               # before launch (tools/talent_beta.py): icon names, CDN by name
            talents = [t for tr in data['trees'] for t in tr['talents']]
            icons = {t['id']: t['iname0'] for t in talents if t.get('iname0') and picture(t['iname0'])}
            for t in talents:
                if t.get('iname0') and t['id'] not in icons:
                    print(f'  {cid}: CDN has no icon {t["iname0"]} ({t["n"]["en"]})')
                x = api_map.get(f'{cid}:{t["id"]}')                # no name in the layout: the API's icon, if proven
                if not t.get('iname0') and x and x['src'] in SHIP and picture(str(x['file'])):
                    icons[t['id']] = str(x['file'])
        else:
            talents = [t for tr in data['trees'] for t in tr['talents']]
            icons = {t['id']: str(t['file']) for t in talents if t.get('file') and picture(str(t['file']))}
            if len(icons) < len(talents):                     # no file id or the CDN does not have it: ask the API
                tok = tok or token()
                icons = {**from_api(data, tok)[0], **icons}
        n, size = sprite(cid, data, icons, a.assets)
        json.dump(data, open(p, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
        left = [f'{t["id"]} {t["n"].get("en") or t["n"].get("ru")}' for tr in data['trees'] for t in tr['talents'] if t.get('icon') is None]
        print(f'{cid}: {n} icons, sprite {size // 1024} KB; no icon: {len(left)}')
        for x in left:
            print('   ', x)


if __name__ == '__main__':
    sys.exit(main())
