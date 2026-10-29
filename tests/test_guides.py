"""Юнит-тесты сборки гайдов. Запуск: python tests/test_guides.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import build_guides as bg
from content import guides as cg

T = {'ru': 'Привет', 'en': 'Hello', 'uk': 'Привіт'}

def test_hubs_complete_and_pathed():
    assert [h['path'] for h in cg.HUBS] == ['classes/', 'races/']
    for h in cg.HUBS:
        assert bg.check_langs(h) == [], bg.check_langs(h)[:5]

def test_ref_js_translated():
    js_en = bg.ref_js(bg.home_src(), 'en')
    assert 'function renderClassRef' in js_en and 'function renderRaceRef' in js_en
    assert 'Прокачка' not in js_en and '@@RACE_SLUG@@' not in js_en
    assert 'const $' not in js_en and 'function esc' not in js_en   # the guide template defines them

def test_news_block_newest_first():
    html = bg.render_block('news', None, 'en', '')
    assert html.count('class="nitem"') == len(cg.NEWS) > 0
    dates = [n['date'] for n in cg.NEWS]
    first = '.'.join(reversed(max(dates).split('-')))
    assert html.index(first) < html.index('.'.join(reversed(min(dates).split('-'))))

def test_L():
    assert bg.L(T, 'uk') == 'Привіт'
    assert bg.L('Blackrock Depths', 'ru') == 'Blackrock Depths'

def test_text_escapes():
    html = bg.render_block('text', [{'ru': 'a < b', 'en': 'a < b', 'uk': 'a < b'}], 'ru', '')
    assert '<p>a &lt; b</p>' in html

def test_steps_numbered():
    html = bg.render_block('steps', [{'t': T, 'd': T}, {'t': T, 'd': T}], 'en', '')
    assert 'steps-c' in html and '<span class="n">1</span>' in html and '<span class="n">2</span>' in html and 'Hello' in html
    assert '01' not in html   # plain figures, not the 01-06 landing cards

def test_table_has_labels_for_mobile():
    html = bg.render_block('table', {'head': [T, 'Lvl'], 'rows': [['Deadmines', '15–22']]}, 'en', '')
    assert 'data-l="Hello"' in html and 'data-l="Lvl"' in html and '<table' in html

def test_faq_details_with_id():
    html = bg.render_block('faq', [{'id': 'release', 'q': T, 'a': [T]}], 'ru', '')
    assert '<details' in html and 'id="release"' in html and 'Привет' in html

def test_tip_uses_fire_and_word():
    html = bg.render_block('tip', T, 'ru', '')
    assert 'tipbox' in html and '#i-fire' in html and 'Совет' in html
    assert 'Tip' in bg.render_block('tip', T, 'en', '')

def test_tabs():
    html = bg.render_block('tabs', [{'id': 'alliance', 't': T, 'blocks': [('text', [T])]},
                                    {'id': 'horde', 't': T, 'blocks': [('text', [T])]}], 'ru', '')
    assert 'role="tablist"' in html and 'data-tab="horde"' in html and html.count('role="tabpanel"') == 2

def test_tiles_link_and_art():
    html = bg.render_block('tiles', [{'t': T, 'd': T, 'href': 'guides/faq/', 'art': 'mage'}], 'uk', '../')
    assert 'href="../guides/faq/"' in html and '@@ROOT@@assets/art/mage-600.webp' in html and 'Привіт' in html

def test_raw_by_lang():
    assert bg.render_block('raw', T, 'en', '') == 'Hello'
    assert bg.render_block('raw', '<div id="x"></div>', 'uk', '') == '<div id="x"></div>'

def test_unknown_block_fails():
    try:
        bg.render_block('nope', [], 'ru', '')
    except ValueError:
        return
    raise AssertionError('unknown block must raise ValueError')

def test_check_langs_finds_gap():
    bad = {'title': {'ru': 'x', 'en': '', 'uk': 'y'}, 'blocks': [('text', [{'ru': 'a', 'en': 'b'}])]}
    gaps = bg.check_langs(bad)
    assert any('title' in g for g in gaps) and len(gaps) == 2

def test_content_complete():
    assert bg.check_langs(cg.HUB) == []
    for g in cg.GUIDES:
        assert bg.check_langs(g) == [], (g['slug'], bg.check_langs(g)[:5])
    for n in cg.NEWS:
        assert bg.check_langs(n) == []

def test_ids_unique():
    taken = {'top', 'more', 'sources', 'all', 'topbar', 'moreDlg', 'moreClose'}   # ids of the template itself
    for g in cg.GUIDES:
        ids = bg.page_ids(g)
        assert len(ids) == len(set(ids)), (g['slug'], sorted(i for i in ids if ids.count(i) > 1))
        assert not taken & set(ids), (g['slug'], taken & set(ids))

def test_profs_table():
    src = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'index.src.html'), encoding='utf-8').read()
    rows = bg.profs_table(src)
    assert len(rows) == 12, len(rows)
    assert [bg.L(c, 'ru') for c in rows[0]] == ['Алхимия', 'Mana Well', 'как Благословение мудрости'], rows[0]
    assert bg.L(rows[0][2], 'en') == 'like Blessing of Wisdom'
    html = bg.render_block('profs', None, 'uk', '')
    assert 'Mana Well' in html and 'Алхімія' in html and 'data-l=' in html

def test_sources_translated():
    for g in cg.GUIDES:
        assert g['sources'], g['slug']
        for n, u in g['sources']:
            assert u.startswith('https://'), u
            assert g.get('only') or bg.L(n, 'en').isascii(), (g['slug'], n)

def test_play_route_from_leveling():
    route, tip = bg.leveling_parts()
    assert set(route) == {'alliance', 'horde'}
    for f, rows in route.items():
        assert rows[0][0] == 1 and rows[-1][1] == 60, (f, rows[0][:2], rows[-1][:2])
        for (lo, hi, _), (lo2, _h, _d) in zip(rows, rows[1:]):
            assert lo < hi and lo2 <= hi, (f, lo, hi, lo2)   # no gap in levels between brackets
    assert bg.check_langs(tip) == []

def test_play_data_per_language():
    import json, re
    src = bg.home_src()
    for lang in ('ru', 'en', 'uk'):
        js = bg.play_data(src, lang)
        assert js.startswith('const DUNGEONS = [')
        p = json.loads(js[js.index('const P = ') + 10:].rstrip().rstrip(';'))
        assert p['racef']['human'] == 'alliance' and p['racef']['orc'] == 'horde', p['racef']
        assert len(p['cn']) == 9 and len(p['rn']) == 10 and all(p['tx'].values())
        assert [m[0] for m in p['miles']] == sorted(m[0] for m in p['miles'])
        if lang == 'en':
            text = json.dumps([p['route'], p['miles'], p['tx'], p['cn'], p['rn']], ensure_ascii=False)
            assert not re.search('[А-Яа-яЁё]', text), re.findall('[А-Яа-яЁё]+', text)[:5]

def test_play_page_built():
    for d in ('', 'en/', 'uk/'):
        html = open(os.path.join(bg.HERE, d + 'play', 'index.html'), encoding='utf-8').read()
        assert 'id="radioDock"' in html and 'const P = ' in html and '<body class="compact">' in html
        assert 'class="stband ghero"' not in html and 'wakeLock' not in html and 'wakeBtn' not in html
        assert 'assets/radio/radio.js' in html

def test_next_block():
    nb = bg.build.next_block
    assert nb(None, 'en', '../') == '' and nb([], 'ru', '') == ''   # no field, no block
    items = [('guides/builds/', T), ('guides/leveling/', T), ('guides/dungeons/', T), ('guides/faq/', T)]
    html = nb(items, 'en', '../')
    assert html.count('<a href="../guides/') == 3 and 'faq' not in html   # three links at most
    assert '>Next step<' in html and '<span>Hello</span>' in html
    assert '>Nächster Schritt<' in nb(items[:1], 'de', '')
    for d in ('', 'en/', 'de/'):   # the placeholder never reaches a page
        for p in ('guides/leveling/', 'classes/mage/', 'races/orc/'):
            assert '@@NEXT@@' not in open(os.path.join(bg.HERE, d + p, 'index.html'), encoding='utf-8').read()

FIX = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')


def gear_problems(data, min_slots):
    """The rules of data/gear30.json: names, slot, level up to 30, a provenance, sources of a known kind, no item twice in a spec."""
    from content import spec_cheats as sc
    bad = []
    for k, it in data.get('items', {}).items():
        if not it.get('names', {}).get('en') or not it['names'].get('ru'):
            bad.append(f'{k}: en and ru names')
        if it.get('slot') not in sc.GSLOTS:
            bad.append(f'{k}: slot {it.get("slot")}')
        if it.get('lvl') is not None and not 1 <= it['lvl'] <= 30:
            bad.append(f'{k}: level {it["lvl"]}')
        if it.get('provenance') not in ('wowhead-forever-guide', 'client-dump'):
            bad.append(f'{k}: provenance {it.get("provenance")}')
    for spec, entries in data.get('specs', {}).items():
        if spec not in sc.HAS_CHEAT:
            bad.append(f'{spec}: no such spec')
        ids = [e['id'] for e in entries]
        if len(ids) != len(set(ids)):
            bad.append(f'{spec}: an item twice')
        if entries and len({data['items'][str(i)]['slot'] for i in ids if str(i) in data['items']}) < min_slots:
            bad.append(f'{spec}: fewer than {min_slots} slots')
        bad += [f'{spec} {e["id"]}: source {s.get("kind")}' for e in entries for s in e.get('src', []) if s.get('kind') not in ('drop', 'quest', 'craft')]
        bad += [f'{spec} {e["id"]}: not in items' for e in entries if str(e['id']) not in data['items']]
    return bad


def test_gear30_data():
    """The real file: never test data, every spec it has on 6+ slots. No file or an empty one: fine (the section stays hidden)."""
    from content import spec_cheats as sc
    p = os.path.join(bg.HERE, 'data', 'gear30.json')
    if os.path.isfile(p):
        data = sc.load_gear30(p)
        assert not data.get('fixture'), 'test data in data/gear30.json'
        assert gear_problems(data, 6) == [], gear_problems(data, 6)[:10]
    fx = sc.load_gear30(os.path.join(FIX, 'gear30.json'))
    assert fx['fixture'] and gear_problems(fx, 5) == [], gear_problems(fx, 5)


def test_gear_import_pages():
    """Saved guide pages -> items with names of both languages, required level up to 30, the three kinds of source."""
    sys.path.insert(0, os.path.join(bg.HERE, 'tools'))
    import gear_import as gi
    specs, items = gi.from_pages(os.path.join(FIX, 'gear_pages'))
    ids = [e['id'] for e in specs['mage-frost']]
    assert len(ids) == 11 and 900022 not in ids and 900012 not in ids   # over level 30; a table after the three parts
    assert items[900001]['names'] == {'en': 'Test Sorcerer Collar', 'ru': 'Тестовый воротник чародея'}
    assert items[900001]['slot'] == 'neck' and items[900001]['lvl'] == 17 and items[900001]['stats'] == {'int': 2, 'spi': 2}
    assert items[900004]['slot'] == 'two' and items[900004]['stats']['dps'] == 18.5 and items[900002]['stats']['sp'] == 6
    src = {e['id']: e['src'][0] for e in specs['mage-frost']}
    assert src[900002] == {'kind': 'drop', 'boss': {'en': 'Test Boss Glacius', 'ru': 'Тестовый босс Гласиус'}, 'dungeon': {'en': 'Test Hollow', 'ru': 'Тестовая пещера'}}
    assert src[900001]['faction'] == 'alliance' and src[900007]['faction'] == 'horde'
    assert src[900010] == {'kind': 'craft', 'prof': 'tailoring'} and src[900011]['prof'] == 'tailoring'   # by word and by [skill=]
    assert {e['id']: e['src'][0] for e in specs['paladin-holy']}[900001]['faction'] is None              # «Both factions»
    assert all(it['provenance'] == 'wowhead-forever-guide' for it in items.values())


def test_gear_import_addon():
    """The addon dump: no item over level 30, armor of the class only, sources kept, provenance client-dump."""
    sys.path.insert(0, os.path.join(bg.HERE, 'tools'))
    import gear_import as gi
    specs, items = gi.from_addon(os.path.join(FIX, 'gear_dump.lua'))
    assert 900105 not in items and 900102 not in items                       # level 35; plate before 40
    war = [e['id'] for e in specs['warrior-protection']]
    assert 900103 in war and 900102 not in war
    holy = {e['id']: e['src'] for e in specs['priest-holy']}
    assert 900103 not in holy and holy[900106] == [{'kind': 'craft', 'prof': 'tailoring'}]    # mail is not for a priest; a recipe in Russian
    assert items[900101]['stats']['hp'] == 9 and items[900101]['provenance'] == 'client-dump'   # the «Equip:» line of the tooltip


def test_gear_section():
    """With data: the table by slot, one slot name per group, the faction of the quests, the source line, the answer row.
    Without: no section and no answer row."""
    from content import spec_cheats as sc
    fx = sc.load_gear30(os.path.join(FIX, 'gear30.json'))
    tr = lambda s, l: s   # noqa: E731
    fn = {'alliance': 'Альянс', 'horde': 'Орда'}
    html = sc.gear_html('mage-frost', 'ru', tr, fn, fx)
    assert html.count('<tr data-s=') == 11 and 'class="gtest"' in html and 'Wowhead Forever, временно, до данных клиента' in html
    assert 'data-f="horde"' in html and 'data-p="tailoring"' in html and 'Квест: Тестовый квест: прах к праху' in html
    assert sc.gear_html('mage-frost', 'ru', tr, fn, {'items': {}, 'specs': {}}) == ''
    assert sc.gear_html('rogue-combat', 'ru', tr, fn, fx) == ''
    assert 'Предметов: 11 · ур. 17–28.' in sc.gear_answer('mage-frost', 'ru', fx)
    empty = not sc.GEAR30.get('specs')
    for d in ('', 'en/', 'uk/'):
        page = os.path.join(bg.HERE, d + 'guides', 'spec-mage-frost', 'index.html')
        if os.path.isfile(page) and empty:
            assert 'id="gearBox"' not in open(page, encoding='utf-8').read()


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_'):
            fn()
    print('OK')
