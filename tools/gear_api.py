"""Item facts for data/gear30.json from Blizzard's Game Data API, before the addon dump of 05.11.

    python tools/gear_api.py            # fills slot, levels, quality, names, stats and the icon of every item; writes the file
    python tools/gear_api.py --dry      # only prints what would change

The list of items and their sources stays what tools/gear_import.py took from the saved guide pages (ids and places only);
everything about an item itself comes from the API, namespace static-classic1x-eu (the Classic Era client, the vanilla
values Forever starts from; static-classic-eu is the Mists client with Cataclysm item changes, so it is not used). Forever is
neither: on 30.10 the quality of 23 of 173 items on the Forever pages differed from Era (15 from Mists), so the levels and
stats here are the Classic client's, a reference until the dump; the page's quality is kept. An item the
API does not have (Forever's own new items, ids 200000+) or one that needs a level above 30 is taken out of the specs and
listed in "dropped" with the reason. The icon is the API's file id; the build draws it from one sprite (assets/gear/icons.webp)
made here from Blizzard's render CDN (render.worldofwarcraft.com). Raw answers are cached in tools/.gear-api.
Key file and rules as in tools/talent_icons.py: read-only client_credentials calls, never print the values.
Never Wowhead (wow.zamimg.com) or other sites: their terms forbid it."""
import argparse, io, json, os, re, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'tools'))
import talent_icons as ti  # noqa: E402  token(), get(), the CDN
from gear_import import TIP_STATS, MAX_LVL  # noqa: E402

OUT = os.path.join(HERE, 'data', 'gear30.json')
CACHE = os.path.join(HERE, 'tools', '.gear-api')
SPRITE = os.path.join(HERE, 'assets', 'gear', 'icons.webp')
NS = 'static-classic1x-eu'
CELL = 36                                        # drawn at 18 px (2x for sharp screens)
LOCS = {'en': 'en_US', 'ru': 'ru_RU', 'de': 'de_DE', 'fr': 'fr_FR', 'es': 'es_ES', 'pt': 'pt_BR', 'it': 'it_IT'}
SLOT = {'HEAD': 'head', 'NECK': 'neck', 'SHOULDER': 'shoulder', 'CLOAK': 'back', 'CHEST': 'chest', 'ROBE': 'chest',
        'WRIST': 'wrist', 'HAND': 'hands', 'WAIST': 'waist', 'LEGS': 'legs', 'FEET': 'feet', 'FINGER': 'finger',
        'TRINKET': 'trinket', 'WEAPON': 'main', 'WEAPONMAINHAND': 'main', 'TWOHWEAPON': 'two', 'SHIELD': 'off',
        'WEAPONOFFHAND': 'off', 'HOLDABLE': 'off', 'RANGED': 'ranged', 'THROWN': 'ranged', 'RANGEDRIGHT': 'ranged'}
QUAL = {'POOR': 0, 'COMMON': 1, 'UNCOMMON': 2, 'RARE': 3, 'EPIC': 4, 'LEGENDARY': 5}
STAT = {'STRENGTH': 'str', 'AGILITY': 'agi', 'STAMINA': 'sta', 'INTELLECT': 'int', 'SPIRIT': 'spi'}


def cached(kind, iid, tok):
    os.makedirs(CACHE, exist_ok=True)
    p = os.path.join(CACHE, f'{kind.replace("/", "-")}-{iid}.json')
    if os.path.isfile(p):
        return json.load(open(p, encoding='utf-8'))
    b = ti.get(f'{ti.API}/data/wow/{kind}/{iid}?namespace={NS}', tok)
    j = json.loads(b) if b else None
    json.dump(j, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
    return j


def facts(j, m):
    """One API item -> our item fields, or (None, reason)."""
    inv = (j.get('inventory_type') or {}).get('type')
    slot = SLOT.get(inv)
    if not slot:
        return None, f'slot {inv}'
    req = j.get('required_level') or 0
    if req > MAX_LVL:
        return None, f'level {req}'
    p = j.get('preview_item') or {}
    st = {}
    for s in p.get('stats') or []:
        k = STAT.get((s.get('type') or {}).get('type'))
        if k and s.get('value'):
            st[k] = st.get(k, 0) + s['value']
    if (p.get('armor') or {}).get('value'):
        st['armor'] = p['armor']['value']
    dps = ((p.get('weapon') or {}).get('dps') or {}).get('value')
    if dps:
        st['dps'] = round(dps, 1)
    for sp in p.get('spells') or []:
        d = sp.get('description') or ''
        d = d.get('en_US', '') if isinstance(d, dict) else d
        for rx, keys in TIP_STATS:
            x = re.search(rx, d)
            if x:
                for k in keys:
                    st[k] = max(st.get(k, 0), int(x.group(1)))
    names = {l: (j.get('name') or {}).get(loc) for l, loc in LOCS.items()}
    icon = next((a.get('file_data_id') for a in (m or {}).get('assets', []) if a.get('key') == 'icon'), None)
    return {'slot': slot, 'lvl': req or 1, 'il': j.get('level'), 'q': QUAL.get((j.get('quality') or {}).get('type')),
            'names': {l: v for l, v in names.items() if v}, 'stats': st, 'icon': icon}, None


def sprite(files):
    """One row of icons for the whole section, in the order of `files`; returns {file id: index}."""
    from PIL import Image
    img = Image.new('RGB', (CELL * max(len(files), 1), CELL), (22, 24, 28))
    for i, f in enumerate(files):
        img.paste(Image.open(ti.picture(str(f))).convert('RGB').resize((CELL, CELL), Image.LANCZOS), (i * CELL, 0))
    os.makedirs(os.path.dirname(SPRITE), exist_ok=True)
    buf = io.BytesIO()
    img.save(buf, 'WEBP', quality=80, method=6)
    open(SPRITE, 'wb').write(buf.getvalue())
    return {f: i for i, f in enumerate(files)}, len(buf.getvalue())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry', action='store_true')
    a = ap.parse_args()
    data = json.load(open(OUT, encoding='utf-8'))
    tok = ti.token()
    dropped, changed = {}, []
    for k, it in list(data['items'].items()):
        j = cached('item', k, tok)
        if not j:
            dropped[k] = {'en': it['names'].get('en'), 'why': 'not in the API (a Forever item)'}
            continue
        f, why = facts(j, cached('media/item', k, tok))
        if not f:
            dropped[k] = {'en': it['names'].get('en'), 'why': why}
            continue
        if it.get('q') is not None and f['q'] != it['q']:          # the page shows Forever's quality: keep it, note the gap
            changed.append(f'{k} {f["names"]["en"]}: quality {it["q"]} on the page, {f["q"]} in the API')
            f['q'] = it['q']
        if it['names'].get('en') and it['names']['en'] != f['names'].get('en'):
            changed.append(f'{k}: name «{it["names"]["en"]}» on the page, «{f["names"].get("en")}» in the API')
        it.update(f)
        it['api'] = NS
    for k in dropped:
        data['items'].pop(k, None)
    for spec, entries in data['specs'].items():
        data['specs'][spec] = [e for e in entries if str(e['id']) in data['items']]
    files = list(dict.fromkeys(it['icon'] for it in data['items'].values() if it.get('icon') and ti.picture(str(it['icon']))))
    print(f'items: {len(data["items"])} kept, {len(dropped)} dropped; icons: {len(files)}')
    for x in changed:
        print('  ', x)
    for k, d in sorted(dropped.items(), key=lambda x: x[1]['why']):
        print(f'   dropped {k} {d["en"]}: {d["why"]}')
    for spec, entries in sorted(data['specs'].items()):
        print(f'  {spec}: {len(entries)} items, {len({data["items"][str(e["id"])]["slot"] for e in entries})} slots')
    if a.dry:
        return
    idx, size = sprite(files)
    for it in data['items'].values():
        it['ic'] = idx.get(it.pop('icon', None))
        if it['ic'] is None:
            it.pop('ic')
    data['sprite'] = len(files)
    data['dropped'] = dict(sorted(dropped.items()))
    data['issues'] = [x for x in data.get('issues', []) if 'quality' not in x] + [f'api {x}' for x in changed]
    data['missing'] = [m for m in data.get('missing', []) if not m.startswith(('slot', 'lvl'))]
    data['provenance'] = {**data.get('provenance', {}), 'details': f'Blizzard Game Data API, {NS} (slot, levels, quality, names, stats, icon)'}
    json.dump(data, open(OUT, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
    print(f'sprite {len(files)} icons, {size // 1024} KB -> {SPRITE}')


if __name__ == '__main__':
    sys.exit(main())
