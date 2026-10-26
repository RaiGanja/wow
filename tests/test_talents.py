"""Talent trees (talents.py, tools/talent_import.py). Run: python tests/test_talents.py"""
import json, os, sys, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import build_guides  # noqa: F401  (attaches the tree blocks to the spec pages)
import talents
import talent_import
from content.spec_builds import SPEC_BUILDS

FIX = os.path.join(ROOT, 'tests', 'fixtures', 'talents', 'GabellaTalents.lua')


def fixture():
    db = talent_import.parse_lua(open(FIX, encoding='utf-8').read())['GabellaTalentsDB']
    return talent_import.convert('paladin', db['PALADIN'], fixture=True)


def tree_blocks(cid=None):
    for g in SPEC_BUILDS:
        for s in g['sections']:
            for k, x in s['blocks']:
                if k == 'tree' and (cid is None or x['cls'] == cid):
                    yield s, x


def test_one_tree_per_spec():
    import importlib
    from content import guides
    importlib.reload(guides)                                     # build.py and build_guides both load the guides: no second tree
    for g in SPEC_BUILDS:
        for s in g['sections']:
            assert sum(k == 'tree' for k, _ in s['blocks']) <= 1, (g['slug'], s['id'])


def test_import_fixture():
    d = fixture()
    assert [t['key'] for t in d['trees']] == ['holy', 'protection', 'retribution']
    assert sum(len(t['talents']) for t in d['trees']) == 51
    prot = {t['n']['en']: t for t in d['trees'][1]['talents']}
    assert prot['Redoubt']['n']['ru'] == 'Оплот' and (prot['Redoubt']['r'], prot['Redoubt']['c'], prot['Redoubt']['m']) == (1, 3, 5)
    assert prot['Shield Specialization']['req'] == prot['Redoubt']['id']
    assert prot['Holy Shield']['req'] == prot['Blessing of Sanctuary']['id']


def test_plan_protection():
    d = fixture()
    s, x = next(tree_blocks('paladin'))
    picked, steps, spent, unknown = talents.plan(d, [(r[0], r[1]) for r in x['rows']])
    assert unknown == []
    got = [(t['n']['en'] if t else None, n, a, b) for t, n, a, b in steps]
    assert got == [('Redoubt', 5, 10, 14), ('Precision', 3, 15, 17), ('Improved Seal of Fury', 1, 18, 18), (None, 1, 19, 19),
                   ('Shield Specialization', 3, 20, 22), (None, 8, 23, 30)], got   # row 3 needs 10 points: one point is free


def test_render_fixture():
    d = fixture()
    real = talents.load
    talents.load = lambda cid: d
    try:
        s, x = next(tree_blocks('paladin'))
        html = talents.render('paladin', s['id'], x['rows'], x['titles'], 'ru', '../../')
    finally:
        talents.load = real
    assert html.count('role="group"') == 3 and '<section' not in html          # search.py cuts sections at the first </section>
    assert 'class="tt-tree on" data-t="protection"' in html
    assert html.count('class="tt-t on"') == 4 + 4                                # 4 talents in the tree, 4 in the order by level
    assert '>Защита<span class=on>12</span>' in html and '@@BETA@@' in html
    assert '<span>10–14</span>' in html and '&quot;protection-2&quot;:[5,10,14,&quot;Шанс блока после ударов по вам&quot;]' in html
    assert talents.PAGE[('paladin', 'ru')]['t']['protection-2'][:3] == ['Оплот', 5, 1]
    assert talents.PAGE[('paladin', 'ru')]['u']['lv'] == 'ур. {a}'
    assert 'assets/talents/paladin.webp' in html


def test_no_data_no_tree():
    real = talents.load
    talents.load = lambda cid: None
    try:
        s, x = next(tree_blocks('paladin'))
        assert talents.render('paladin', s['id'], x['rows'], x['titles'], 'ru', '') == ''
    finally:
        talents.load = real


def test_lua_parser():
    db = talent_import.parse_lua('A = {\n ["x"] = { 1, 2, nil, 4, }, -- [1]\n ["s"] = "a\\"b",\n y = true,\n}\n')
    assert db == {'A': {'x': [1, 2, None, 4], 's': 'a"b', 'y': True}}


def test_shipped_data():
    """content/talents: client data only, every row of our tables found, the order ends by level 30, the sprite in place."""
    for f in sorted(os.listdir(talents.DATA)) if os.path.isdir(talents.DATA) else []:
        cid = f[:-5]
        d = talents.load(cid)
        assert not d.get('fixture'), f'{f}: test data must not ship'
        assert [t['key'] for t in d['trees']] == talents.TREES[cid], f
        for s, x in tree_blocks(cid):
            _, steps, _, unknown = talents.plan(d, [(r[0], r[1]) for r in x['rows']])
            assert unknown == [], (cid, s['id'], unknown)
            assert steps[-1][3] <= talents.CAP_LEVEL, (cid, s['id'], steps[-1])
        icons = [t['icon'] for tr in d['trees'] for t in tr['talents'] if t.get('icon') is not None]
        assert all(0 <= i < d['sprite'] for i in icons), f
        if icons:
            assert os.path.isfile(os.path.join(ROOT, 'assets', 'talents', f'{cid}.webp')), cid


if __name__ == '__main__':
    n = 0
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
            n += 1
    print(f'talents: {n} tests OK')
