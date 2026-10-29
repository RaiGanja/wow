"""Gear up to level 30 for the spec cheat sheets -> data/gear30.json (content/spec_cheats.py reads it, the build has no network).

Two inputs, one schema. Nothing here goes to the network.

  1) Saved guide pages, until the client data (05.11):
       python tools/gear_import.py --pages <folder>
     One page per spec, saved by hand from the browser («HTML only»): <class>-<spec>.html (druid-balance.html,
     hunter-beast-mastery.html, ...). The same page of another site language may sit next to it as <class>-<spec>.<lang>.html
     (ru, de, fr, es, pt, it): the item names of that language are taken from it. Only facts are kept: item id, name, slot,
     required level, quality, stats, and where it comes from (boss and dungeon, quest and faction, profession). No text,
     no pictures. Items marked provenance "wowhead-forever-guide".
  2) The dump of the GabellaGear addon (tools/gear_dump), from 05.11:
       python tools/gear_import.py --addon "<WoW>/_forever_/WTF/Account/<account>/SavedVariables/GabellaGear.lua"
     The client gives the items (name in every dumped language, slot, levels, quality, stats); the sources are what the
     addon saw while playing (loot of a dungeon boss, quest rewards, recipes of the open profession window). The picks for
     each spec are made here by the spec's stat priority (content/spec_cheats.STATS). Items marked provenance "client-dump".

  --date YYYY-MM-DD   the day of the data (default today);  --fixture   test data (tests/fixtures): tests refuse it in data/.

Schema (data/gear30.json):
  {"schema": 1, "date": "2026-10-30", "fixture": false,
   "items": {"<id>": {"slot": "head|neck|shoulder|back|chest|wrist|hands|waist|legs|feet|finger|trinket|main|two|off|ranged",
                      "lvl": <required level 1-30 or null>, "il": <item level or null>, "q": <quality 0-5>,
                      "names": {"en": ..., "ru": ...}, "stats": {"int": 2, "spi": 2, ...}, "provenance": "..."}},
   "specs": {"<class>-<spec>": [{"id": <id>, "src": [{"kind": "drop", "boss": {names}, "dungeon": {names}},
                                                     {"kind": "quest", "quest": {names}, "faction": "alliance|horde|null"},
                                                     {"kind": "craft", "prof": "tailoring"}]}]}}
  Stat keys: str agi sta int spi armor sp (spell damage) hp (healing) mp5 hit crit def ap dps (percent stats as numbers)."""
import argparse, datetime, html as H, json, os, re, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
OUT = os.path.join(HERE, 'data', 'gear30.json')
LANGS = ('en', 'ru', 'de', 'fr', 'es', 'pt', 'it')
MAX_LVL = 30
SLOTS = ('head', 'neck', 'shoulder', 'back', 'chest', 'wrist', 'hands', 'waist', 'legs', 'feet', 'finger', 'trinket',
         'main', 'two', 'off', 'ranged')
# inventory type number (the game's, as in the item data of the pages) -> our slot; shirt, tabard, bags, ammo and relics are left out
INV = {1: 'head', 2: 'neck', 3: 'shoulder', 16: 'back', 5: 'chest', 20: 'chest', 9: 'wrist', 10: 'hands', 6: 'waist', 7: 'legs',
       8: 'feet', 11: 'finger', 12: 'trinket', 13: 'main', 21: 'main', 17: 'two', 14: 'off', 22: 'off', 23: 'off',
       15: 'ranged', 25: 'ranged', 26: 'ranged'}
INVTYPE = {'INVTYPE_HEAD': 1, 'INVTYPE_NECK': 2, 'INVTYPE_SHOULDER': 3, 'INVTYPE_CLOAK': 16, 'INVTYPE_CHEST': 5, 'INVTYPE_ROBE': 20,
           'INVTYPE_WRIST': 9, 'INVTYPE_HAND': 10, 'INVTYPE_WAIST': 6, 'INVTYPE_LEGS': 7, 'INVTYPE_FEET': 8, 'INVTYPE_FINGER': 11,
           'INVTYPE_TRINKET': 12, 'INVTYPE_WEAPON': 13, 'INVTYPE_WEAPONMAINHAND': 21, 'INVTYPE_2HWEAPON': 17, 'INVTYPE_SHIELD': 14,
           'INVTYPE_WEAPONOFFHAND': 22, 'INVTYPE_HOLDABLE': 23, 'INVTYPE_RANGED': 15, 'INVTYPE_THROWN': 25, 'INVTYPE_RANGEDRIGHT': 26}
# stat fields of the page item data -> our keys
WH_STATS = {'str': 'str', 'agi': 'agi', 'sta': 'sta', 'int': 'int', 'spi': 'spi', 'armor': 'armor', 'spldmg': 'sp', 'splpwr': 'sp',
            'splheal': 'hp', 'manargn': 'mp5', 'mlehitpct': 'hit', 'rgdhitpct': 'hit', 'splhitpct': 'hit', 'hitpct': 'hit',
            'mlecritstrkpct': 'crit', 'rgdcritstrkpct': 'crit', 'splcritstrkpct': 'crit', 'critstrkpct': 'crit', 'def': 'def',
            'defrtng': 'def', 'mleatkpwr': 'ap', 'atkpwr': 'ap', 'dps': 'dps', 'mledps': 'dps', 'rgddps': 'dps'}
# GetItemStats keys of the client -> our keys
CL_STATS = {'ITEM_MOD_STRENGTH_SHORT': 'str', 'ITEM_MOD_AGILITY_SHORT': 'agi', 'ITEM_MOD_STAMINA_SHORT': 'sta',
            'ITEM_MOD_INTELLECT_SHORT': 'int', 'ITEM_MOD_SPIRIT_SHORT': 'spi', 'RESISTANCE0_NAME': 'armor',
            'ITEM_MOD_SPELL_POWER_SHORT': 'sp', 'ITEM_MOD_SPELL_DAMAGE_DONE_SHORT': 'sp', 'ITEM_MOD_SPELL_HEALING_DONE_SHORT': 'hp',
            'ITEM_MOD_MANA_REGENERATION_SHORT': 'mp5', 'ITEM_MOD_POWER_REGEN0_SHORT': 'mp5', 'ITEM_MOD_HIT_RATING_SHORT': 'hit',
            'ITEM_MOD_HIT_SPELL_RATING_SHORT': 'hit', 'ITEM_MOD_CRIT_RATING_SHORT': 'crit', 'ITEM_MOD_CRIT_SPELL_RATING_SHORT': 'crit',
            'ITEM_MOD_DEFENSE_SKILL_RATING_SHORT': 'def', 'ITEM_MOD_ATTACK_POWER_SHORT': 'ap', 'ITEM_MOD_DAMAGE_PER_SECOND_SHORT': 'dps'}
# «Equip:» lines of the English tooltip the client stat table may miss (Classic-style items)
TIP_STATS = [(r'damage and healing done by magical spells and effects by up to (\d+)', ('sp', 'hp')),
             (r'healing done by spells and effects by up to (\d+)', ('hp',)),
             (r'chance to hit (?:with spells )?by (\d+)%', ('hit',)), (r'critical strike (?:with spells )?by (\d+)%', ('crit',)),
             (r'Restores (\d+) mana per 5 sec', ('mp5',)), (r'\+(\d+) Attack Power', ('ap',)), (r'Increased Defense \+(\d+)', ('def',))]
PROFS = {'blacksmithing': 164, 'leatherworking': 165, 'tailoring': 197, 'engineering': 202, 'enchanting': 333, 'alchemy': 171,
         'firstaid': 129, 'cooking': 185}
PROF_WORDS = {'blacksmithing': 'blacksmith', 'leatherworking': 'leatherwork', 'tailoring': 'tailor', 'engineering': 'engineer',
              'enchanting': 'enchant', 'alchemy': 'alchem', 'firstaid': 'first aid', 'cooking': 'cooking'}
SKILL_ID = {v: k for k, v in PROFS.items()}
LOC = {'enUS': 'en', 'enGB': 'en', 'ruRU': 'ru', 'deDE': 'de', 'frFR': 'fr', 'esES': 'es', 'esMX': 'es', 'ptBR': 'pt', 'itIT': 'it'}
NAME_KEY = {'en': 'name_enus', 'ru': 'name_ruru', 'de': 'name_dede', 'fr': 'name_frfr', 'es': 'name_eses', 'pt': 'name_ptbr', 'it': 'name_itit'}


# ---------- saved guide pages ----------

def gatherer(src):
    """Every WH.Gatherer.addData(type, env, {...}) of a page: {type: {id: data}} (1 npc, 3 item, 5 quest, 7 zone)."""
    out, dec = {}, json.JSONDecoder()
    for m in re.finditer(r'(?:WH\.)?Gatherer\.addData\(\s*(\d+)\s*,\s*\d+\s*,\s*', src):
        try:
            obj, _ = dec.raw_decode(src, m.end())
        except ValueError:
            continue
        if isinstance(obj, dict):
            out.setdefault(int(m.group(1)), {}).update({int(k): v for k, v in obj.items() if str(k).isdigit()})
    return out


def markup(src):
    """The guide body as tag markup: the string a page hands to WH.markup.printHtml, or else the rendered HTML turned into the same tags."""
    dec = json.JSONDecoder()
    for m in re.finditer(r'markup\.printHtml\(\s*', src):
        try:
            s, _ = dec.raw_decode(src, m.end())
        except ValueError:
            continue
        if isinstance(s, str) and len(s) > 200:
            return s
    body = src
    i = body.find('guide-body')
    if i >= 0:
        body = body[i:]
    body = re.sub(r'(?is)<(script|style)\b.*?</\1>', ' ', body)
    names = {}

    def link(m):
        kind, num, text = m.group(1), m.group(2), re.sub(r'<[^>]+>', '', m.group(3)).strip()
        if text:
            names[(kind, int(num))] = H.unescape(text)
        return f'[{kind}={num}]'
    body = re.sub(r'(?is)<a\b[^>]*href="[^"]*?/(item|npc|quest|zone|skill)=(\d+)[^"]*"[^>]*>(.*?)</a>', link, body)
    body = re.sub(r'(?i)<(/?)(h[1-4]|tr|td|th|table)\b[^>]*>', lambda m: f'[{m.group(1)}{m.group(2).lower().replace("th", "td")}]', body)
    body = re.sub(r'<[^>]+>', ' ', body)
    return H.unescape(body), names


def _txt(s):
    return re.sub(r'\s+', ' ', re.sub(r'\[/?[a-z0-9]+(?:[= ][^\]]*)?\]', ' ', s)).strip()


KIND_WORDS = (('drop', ('dungeon drop', 'dungeon loot', 'drops')), ('quest', ('quest reward', 'quest')), ('craft', ('crafted', 'craft', 'profession')))


def page_rows(src):
    """(kind, heading text, faction, row tags, row plain cells) for every table row with an item, in page order."""
    got = markup(src)
    text, anchor = (got, {}) if isinstance(got, str) else got
    kind, sub, rows = None, '', []
    for part in re.split(r'(\[h[1-4][^\]]*\].*?\[/h[1-4]\]|\[tr\].*?\[/tr\])', text, flags=re.S | re.I):
        if re.match(r'\[h[1-4]', part, re.I):
            level = int(part[2])
            title = _txt(part)
            low = title.lower()
            k = next((k for k, words in KIND_WORDS if any(w in low for w in words)), None)
            if level <= 2:                                         # a new part of the guide: one of the three tables or the end of them
                kind, sub = (k if k else 'stop' if kind else None), ''
            elif kind not in (None, 'stop'):
                sub = part
            continue
        if not part.lower().startswith('[tr]') or kind in (None, 'stop') or '[item=' not in part:
            continue
        cells = re.findall(r'\[td[^\]]*\](.*?)\[/td\]', part, flags=re.S | re.I) or [part]
        rows.append((kind, sub, cells))
    return rows, anchor


def faction_of(*texts):
    low = ' '.join(texts).lower()
    a, h = 'alliance' in low, 'horde' in low
    return 'alliance' if a and not h else 'horde' if h and not a else None


def prof_of(*texts):
    low = ' '.join(texts).lower()
    m = re.search(r'\[skill=(\d+)\]', low)
    if m and int(m.group(1)) in SKILL_ID:
        return SKILL_ID[int(m.group(1))]
    return next((p for p, w in PROF_WORDS.items() if w in low), None)


def names_of(kind, num, by_lang, anchor):
    """{lang: name} of an npc/quest/zone/item from the gatherer data of every saved language, then the link text."""
    t = {'npc': 1, 'item': 3, 'quest': 5, 'zone': 7}[kind]
    out = {}
    for lang, (g, _) in by_lang.items():
        d = g.get(t, {}).get(num) or {}
        n = d.get(NAME_KEY[lang]) or d.get('name_enus' if lang == 'en' else '') or (d.get('name') if lang == 'en' else None)
        if n:
            out[lang] = n
    if 'en' not in out and anchor.get((kind, num)):
        out['en'] = anchor[(kind, num)]
    return out


def item_of(num, by_lang, provenance):
    g = by_lang['en'][0] if 'en' in by_lang else next(iter(by_lang.values()))[0]
    d = g.get(3, {}).get(num)
    if not d:
        return None
    eq = d.get('jsonequip') or {}
    slot = INV.get(eq.get('slotbak') or eq.get('slot') or d.get('slot') or d.get('slotbak'))
    lvl = eq.get('reqlevel') or d.get('reqlevel')
    if not slot or (lvl and lvl > MAX_LVL):
        return None
    stats = {}
    for k, v in eq.items():
        if k in WH_STATS and isinstance(v, (int, float)) and v:
            stats[WH_STATS[k]] = max(stats.get(WH_STATS[k], 0), round(v, 1))
    return {'slot': slot, 'lvl': lvl or None, 'il': d.get('level') or eq.get('level') or None, 'q': d.get('quality', eq.get('quality', 1)),
            'names': names_of('item', num, by_lang, {}), 'stats': stats, 'provenance': provenance}


def from_pages(folder):
    """{spec: [entries]}, {id: item} from the saved guide pages of the folder."""
    files = {}
    for f in sorted(os.listdir(folder)):
        m = re.fullmatch(r'([a-z]+-[a-z-]+?)(?:\.([a-z]{2}))?\.html?', f)
        if m:
            files.setdefault(m.group(1), {})[m.group(2) or 'en'] = os.path.join(folder, f)
    items, specs = {}, {}
    for spec, by_file in files.items():
        by_lang = {}
        for lang, path in by_file.items():
            src = open(path, encoding='utf-8', errors='replace').read()
            by_lang[lang] = (gatherer(src), src)
        rows, anchor = page_rows(by_lang.get('en', next(iter(by_lang.values())))[1])
        got = {}
        for kind, sub, cells in rows:
            row = ' '.join(cells)
            ids = [int(x) for x in re.findall(r'\[item=(\d+)', row)]
            tag = lambda k, s=row + ' ' + sub: [int(x) for x in re.findall(rf'\[{k}=(\d+)', s)]  # noqa: E731
            if kind == 'drop':
                zone = tag('zone')
                boss = [int(x) for x in re.findall(r'\[npc=(\d+)', row)]
                plain = next((_txt(c) for c in cells if '[item=' not in c and _txt(c)), '')
                src = {'kind': 'drop', 'boss': names_of('npc', boss[0], by_lang, anchor) if boss else ({'en': plain} if plain else {}),
                       'dungeon': names_of('zone', zone[0], by_lang, anchor) if zone else ({'en': _txt(sub)} if _txt(sub) else {})}
            elif kind == 'quest':
                q = [int(x) for x in re.findall(r'\[quest=(\d+)', row)]
                plain = next((_txt(c) for c in cells if '[item=' not in c and _txt(c)), '')
                src = {'kind': 'quest', 'quest': names_of('quest', q[0], by_lang, anchor) if q else ({'en': plain} if plain else {}),
                       'faction': faction_of(row, sub)}
            else:
                src = {'kind': 'craft', 'prof': prof_of(row, sub)}
            for num in ids:
                if num not in items:
                    it = item_of(num, by_lang, 'wowhead-forever-guide')
                    if not it:
                        continue
                    items[num] = it
                e = got.setdefault(num, {'id': num, 'src': []})
                if src not in e['src']:
                    e['src'].append(src)
        specs[spec] = list(got.values())
    return specs, items


# ---------- the addon dump ----------

ARMOR_MAX = {'warrior': 3, 'paladin': 3, 'hunter': 2, 'shaman': 2, 'rogue': 2, 'druid': 2, 'mage': 1, 'priest': 1, 'warlock': 1}
WEAPONS = {'warrior': {0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 13, 15, 16, 18}, 'paladin': {0, 1, 4, 5, 6, 7, 8},
           'hunter': {0, 1, 2, 3, 6, 7, 8, 10, 13, 15, 18}, 'rogue': {2, 3, 4, 7, 13, 15, 16, 18}, 'priest': {4, 10, 15, 19},
           'shaman': {0, 1, 4, 5, 10, 13, 15}, 'mage': {7, 10, 15, 19}, 'warlock': {7, 10, 15, 19}, 'druid': {4, 5, 10, 13, 15}}
SHIELD = {'warrior', 'paladin', 'shaman'}
ROLE_W = {'tank': 'sta armor def str agi', 'heal': 'hp int spi mp5 crit', 'caster': 'sp hit crit int spi', 'str': 'dps hit crit str agi',
          'agi': 'dps hit agi crit'}
HEALERS = {'priest-holy', 'priest-discipline', 'paladin-holy', 'shaman-restoration', 'druid-restoration'}
TANKS = {'warrior-protection', 'paladin-protection'}
PCT = {'hit', 'crit'}


def weights(spec):
    """Stat weights of a spec from its priority in spec_cheats.STATS (first 1.0, then down); no order there: the role's."""
    from content import spec_cheats
    st = spec_cheats.STATS.get(spec)
    cls = spec.split('-')[0]
    if isinstance(st, tuple):
        keys = st[0].split()
    else:
        role = ('tank' if spec in TANKS else 'heal' if spec in HEALERS else 'caster' if cls in ('mage', 'warlock') or spec in
                ('priest-shadow', 'shaman-elemental', 'druid-balance') else 'agi' if cls in ('rogue', 'hunter') or spec == 'druid-feral' else 'str')
        keys = ROLE_W[role].split()
    keys = ['dps' if k == 'wd' else k for k in keys if k not in ('exp', 'haste')]
    w = {k: max(0.3, 1 - 0.15 * i) for i, k in enumerate(keys)}
    w.setdefault('sta', 0.1)
    return w


def score(it, w):
    s = 0.0
    for k, v in it['stats'].items():
        x = w.get(k, 0) * v
        s += x * 10 if k in PCT else x * 0.02 if k == 'armor' else x
    return s


def allowed(it, cls):
    c, sub = it.get('cls'), it.get('sub')
    if c == 4:                                                     # armor: cloth 1, leather 2, mail 3, plate 4, shield 6, misc 0
        if sub == 6:
            return cls in SHIELD
        return it['slot'] == 'back' or sub in (0, None) or sub <= ARMOR_MAX[cls]
    if c == 2:
        return sub in WEAPONS[cls]
    return True


def pick(spec, pool, per_slot=4):
    """The best item at its own required level for every slot (nothing at a lower level beats it), the last per_slot of them."""
    cls, w = spec.split('-')[0], weights(spec)
    out = []
    for slot in SLOTS:
        cand = sorted((it for it in pool.values() if it['slot'] == slot and allowed(it, cls) and score(it, w) > 0),
                      key=lambda it: (it['lvl'] or 0, -score(it, w)))
        best, keep = 0.0, []
        for it in cand:
            s = score(it, w)
            if s > best:
                best = s
                keep.append(it)
        out += keep[-per_slot:]
    return out


def tip_stats(lines, stats):
    for line in lines or ():
        for rx, keys in TIP_STATS:
            m = re.search(rx, line)
            if m:
                for k in keys:
                    stats.setdefault(k, int(m.group(1)))


def from_addon(path):
    sys.path.insert(0, os.path.join(HERE, 'tools'))
    from talent_import import parse_lua                       # the same SavedVariables reader as the talents
    db = parse_lua(open(path, encoding='utf-8').read())['GabellaGearDB']
    by_id = lambda t: t.items() if isinstance(t, dict) else ((i, v) for i, v in enumerate(t or [], 1) if v is not None)  # noqa: E731  an int-keyed table reads as a list
    names = json.load(open(os.path.join(HERE, 'i18n', 'names.json'), encoding='utf-8'))
    prof_any = {n.lower(): p for p in PROFS for en in [p.title().replace('Firstaid', 'First Aid')] for n in [en, *names.get(en, {}).values()]}
    pool = {}
    for num, d in by_id(db.get('items')):
        slot = INV.get(INVTYPE.get(d.get('slot')))
        if not slot or (d.get('req') or 0) > MAX_LVL:
            continue
        stats = {}
        for k, v in (d.get('stats') or {}).items():
            if k in CL_STATS and v:
                stats[CL_STATS[k]] = round(v, 1)
        tip_stats((d.get('tip') or {}).get('enUS') or (d.get('tip') or {}).get('enGB'), stats)
        pool[int(num)] = {'id': int(num), 'slot': slot, 'lvl': d.get('req') or None, 'il': d.get('ilvl') or None, 'q': d.get('q', 1),
                          'names': {LOC[loc]: n for loc, n in (d.get('name') or {}).items() if loc in LOC}, 'stats': stats,
                          'provenance': 'client-dump', 'cls': d.get('cls'), 'sub': d.get('sub')}
    srcs = {}
    for num, recs in by_id(db.get('src')):
        out = []
        for r in (recs.values() if isinstance(recs, dict) else recs):
            nm = lambda x: {LOC[l]: v for l, v in (x or {}).items() if l in LOC}  # noqa: E731
            if r.get('kind') == 'drop':
                out.append({'kind': 'drop', 'boss': nm(r.get('name')), 'dungeon': nm(r.get('zone'))})
            elif r.get('kind') == 'quest':
                f = (r.get('faction') or '').lower()
                out.append({'kind': 'quest', 'quest': nm(r.get('name')), 'faction': f if f in ('alliance', 'horde') else None})
            elif r.get('kind') == 'craft':
                got = [prof_any.get((n or '').lower()) or prof_of(n or '') for n in (r.get('name') or {}).values()]
                out.append({'kind': 'craft', 'prof': next((p for p in got if p), None)})
        srcs[int(num)] = out
    from content.spec_cheats import CHEATS
    items, specs = {}, {}
    for c, s in CHEATS:
        spec = f'{c}-{s}'
        chosen = pick(spec, pool)
        specs[spec] = [{'id': it['id'], 'src': srcs.get(it['id'], [])} for it in chosen]
        for it in chosen:
            items[it['id']] = {k: v for k, v in it.items() if k not in ('id', 'cls', 'sub')}
    return specs, items


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--pages')
    g.add_argument('--addon')
    ap.add_argument('--out', default=OUT)
    ap.add_argument('--date', default=datetime.date.today().isoformat())
    ap.add_argument('--fixture', action='store_true')
    a = ap.parse_args()
    specs, items = from_pages(a.pages) if a.pages else from_addon(a.addon)
    data = {'schema': 1, 'date': a.date, 'fixture': bool(a.fixture),
            'items': {str(k): items[k] for k in sorted(items)}, 'specs': {k: specs[k] for k in sorted(specs)}}
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    for k in sorted(specs):
        slots = {items[e['id']]['slot'] for e in specs[k]}
        print(f'{k}: {len(specs[k])} items, {len(slots)} slots')
    print(f'{len(items)} items -> {a.out}')


if __name__ == '__main__':
    main()
