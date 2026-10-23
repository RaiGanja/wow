"""Профили: правила достижений и игровые данные (assets/game.json). Запуск: python tests/test_me.py"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import export_game

G = export_game.game()


def test_races_and_classes():
    assert len(G['races']) == 10 and len(G['classes']) == 9
    for rid, r in G['races'].items():
        assert r['f'] in ('alliance', 'horde'), rid
        assert r['cls'] and set(r['cls']) <= set(G['classes']), (rid, r['cls'])
    for cid, c in G['classes'].items():
        assert c['roles'] and set(c['roles']) <= {'tank', 'heal', 'dps'}, cid
    assert len(G['profs']) == 9


def test_achievements_rules():
    ids = [a['id'] for a in G['achievements']]
    assert len(ids) == len(set(ids)), 'duplicate achievement id'
    keys = set(G['sets']) | set(G['flags'])
    for a in G['achievements']:
        assert a['pts'] in (5, 10, 25, 50), a
        assert a['cat'] in G['cats'], a
        assert a['kind'] in ('auto', 'progress', 'admin'), a
        r = a['rule']
        if a['kind'] == 'progress':
            assert r and r['key'] in keys, a
            assert r.get('all') or r.get('goal', 0) > 0 or r.get('items'), a
            for it in r.get('items', []):
                assert it in G['sets'][r['key']], a


def test_frames_titles_ranks():
    ach = {a['id'] for a in G['achievements']}
    ranks = [r['id'] for r in G['ranks']]
    pts = [r['pts'] for r in G['ranks']]
    assert pts == sorted(pts) and pts[0] == 0
    for f in G['frames']:
        assert f.get('rank') in ranks or f.get('ach') in ach or f.get('admin'), f
    assert set(G['titles']) <= ach


def test_backgrounds_have_art():
    for b in G['backgrounds']:
        name = b + ('-bg.webp' if not b.startswith('hero_') else '-960.webp')
        assert os.path.exists(os.path.join(ROOT, 'assets', 'art', name)), name


def test_exported_file_is_fresh():
    with open(os.path.join(ROOT, 'assets', 'game.json'), encoding='utf-8') as f:
        assert json.load(f) == json.loads(json.dumps(G)), 'run python tools/export_game.py'


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_'):
            fn()
    print('OK')
