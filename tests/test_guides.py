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
    assert 'steps-c' in html and '01' in html and '02' in html and 'Hello' in html

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
            assert bg.L(n, 'en').isascii(), (g['slug'], n)

if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_'):
            fn()
    print('OK')
