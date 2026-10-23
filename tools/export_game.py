"""Game data and achievement rules for profiles -> assets/game.json (read by the site and by the gabella-api Worker,
which copies it with `npm run sync`). Only ids and rules, no texts: texts are translated by build_me.py.
Run: python tools/export_game.py  (build.py runs it too)"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'content'))
sys.path.insert(0, ROOT)
from classes import CLASSES  # noqa: E402
from races import RACES_PAGE  # noqa: E402
from guides import GUIDES  # noqa: E402
import achievements as A  # noqa: E402
import progression as P  # noqa: E402
import langs  # noqa: E402

SCENES = ['hero_dawn', 'hero_campfire']   # card backgrounds besides the race arts
OUT = os.path.join(ROOT, 'assets', 'game.json')


def home_races():
    """id, faction and classes from RACES in index.src.html (the * marks a combination new in Forever)."""
    src = open(os.path.join(ROOT, 'index.src.html'), encoding='utf-8').read()
    block = src[src.index('const RACES = ['):]
    block = block[:block.index('\n];')]
    out = {}
    for m in re.finditer(r"\{ id:'(\w+)',[^\n]*?f:'(alliance|horde)'[^\n]*\n\s*cls:\[([^\]]*)\]", block):
        out[m.group(1)] = {'f': m.group(2), 'cls': [c.strip().strip("'").rstrip('*') for c in m.group(3).split(',')]}
    return out


def home_profs():
    src = open(os.path.join(ROOT, 'index.src.html'), encoding='utf-8').read()
    block = src[src.index('const PROFS = ['):]
    block = block[:block.index('\n];')]
    return [m.group(1) for m in re.finditer(r"\['(\w+)', '[^']*', 1,", block)]


def stations():
    src = open(os.path.join(ROOT, 'tools', 'make_radio.py'), encoding='utf-8').read()
    block = src[src.index('STATIONS = ['):src.index('\n]', src.index('STATIONS = ['))]
    return re.findall(r"\{'id': '(\w+)'", block)


def game():
    races = home_races()
    slug = {r['id']: r['slug'] for r in RACES_PAGE}
    for rid, r in races.items():
        r['slug'] = slug[rid]
    sets = {
        'guide': [g['slug'] for g in GUIDES if g['slug']],
        'class': [c['id'] for c in CLASSES],
        'race': [r['slug'] for r in RACES_PAGE],
        'lang': list(langs.ALL),
        'station': stations(),
        'egg': list(A.EGGS),
        'hour': list(range(24)),
    }
    achs = []
    for row in A.ACH:
        aid, cat, pts, kind, rule = row[:5]
        achs.append({'id': aid, 'cat': cat, 'pts': pts, 'kind': kind, 'rule': rule, 'secret': cat == 'secrets' or len(row) > 7})
    return {
        'races': races,
        'classes': {c['id']: {'roles': [r.rstrip('?') for r in c['roles']]} for c in CLASSES},
        'profs': home_profs(),
        'playtimes': ['morning', 'evening', 'night'],
        'sets': sets,
        'flags': sorted({a['rule']['key'] for a in achs if a['rule'] and 'key' in a['rule'] and a['rule']['key'] not in sets}),
        'cats': [c for c, _ in A.CATS],
        'achievements': achs,
        'ranks': [{'id': r, 'pts': p} for r, p, _ in A.RANKS],
        'frames': [dict(id=f, **rule) for f, rule, _ in A.FRAMES],
        'titles': list(A.TITLES),
        'backgrounds': [r['wt'] if r['wt'] != 'skyborne' else r['slug'] for r in RACES_PAGE] + SCENES,
        'deadline_founder': '2026-11-03T21:00:00Z',
        'progression': {
            'glory': P.GLORY, 'sources': {k: {'xp': v[0], 'cap': v[1], 'rested': v[2]} for k, v in P.SOURCES.items()},
            'ach_xp': P.ACH_XP, 'weekly_xp': P.WEEKLY_XP, 'weekly_all_xp': P.WEEKLY_ALL_XP, 'rested': P.RESTED,
            'week_anchor': P.WEEK_ANCHOR, 'weekly_cats': P.WEEKLY_CATS, 'weekly': P.weekly(sets),
            'seasons': P.SEASONS, 'star_xp': P.STAR_XP, 'week_stars': P.WEEK_STARS, 'track': P.TRACK,
            'name_colors': P.NAME_COLORS, 'motto_glory': P.MOTTO_GLORY, 'report_glory': P.REPORT_GLORY, 'reports_hide': P.REPORTS_HIDE,
        },
    }


def main():
    data = game()
    text = json.dumps(data, ensure_ascii=False, indent=1) + '\n'
    with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
    print(f'game.json: {len(data["achievements"])} achievements, {len(data["races"])} races', file=sys.stderr)


if __name__ == '__main__':
    main()
