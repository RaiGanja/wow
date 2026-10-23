"""Профили: правила достижений и игровые данные (assets/game.json). Запуск: python tests/test_me.py"""
import json, os, re, sys
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


def built_pages():
    out = []
    for d, dirs, fs in os.walk(ROOT):
        dirs[:] = [x for x in dirs if not x.startswith(('.', 'mock-', 'node_modules'))]
        out += [os.path.join(d, f) for f in fs if f.endswith('.html') and not f.endswith('.src.html')]
    return out


def test_me_script_on_every_page_after_radio():
    pages = built_pages()
    assert len(pages) >= 270, len(pages)
    for p in pages:
        html = open(p, encoding='utf-8').read()
        if 'assets/radio/radio.js' not in html:      # tools/index.html of the repo root is a redirect stub
            continue
        assert html.count('assets/me/me.js') == 1 and html.count('assets/me/me.css') == 1, p
        assert html.index('assets/radio/radio.js') < html.index('assets/me/me.js'), p
        m = re.search(r'<script src="[^"]*assets/me/me\.js" data-root="([^"]*)" data-home="([^"]*)" data-lang="(\w+)" data-page="([^"]*)" defer>', html)
        assert m, p
        page = m.group(4)
        name = os.path.relpath(p, ROOT).replace(os.sep, '/')
        if name.endswith('404.html'):
            assert page == '404', name
        else:
            assert name.endswith(page + 'index.html'), (name, page)


def test_texts_for_every_language():
    from langs import LANGS
    ach = {a['id'] for a in G['achievements']}
    for lang in LANGS:
        with open(os.path.join(ROOT, 'assets', 'me', f'i18n-{lang}.json'), encoding='utf-8') as f:
            t = json.load(f)
        assert set(t['ach']) == ach, lang
        assert set(t['ranks']) == {r['id'] for r in G['ranks']}, lang
        assert set(t['frames']) == {f['id'] for f in G['frames']}, lang
        assert all(t['ui'][k] for k in ('got', 'rankUp', 'profile', 'login', 'lvlAsk', 'update', 'notNow')), lang
        assert '{n}' in t['ui']['lvlAsk'] and '{name}' in t['ui']['lvlAsk'], lang
        for a in G['achievements']:
            assert len(t['ach'][a['id']]) == (3 if a['secret'] else 2), (lang, a['id'])
            if lang != 'ru':
                assert not re.search('[А-Яа-яЁё]', ' '.join(t['ach'][a['id']])) or lang == 'uk', (lang, a['id'])


def test_profile_pages():
    """roster/, profile/, u/ on every language: game data inlined, the personal ones noindex and out of the sitemap."""
    from langs import LANGS
    sitemap = open(os.path.join(ROOT, 'sitemap.xml'), encoding='utf-8').read()
    for lang in LANGS:
        for sub in ('roster/', 'profile/', 'u/'):
            rel = ('' if lang == 'ru' else lang + '/') + sub
            html = open(os.path.join(ROOT, rel, 'index.html'), encoding='utf-8').read()
            m = re.search(r'const GD = (\{.*?\});\n', html)
            assert m, rel
            gd = json.loads(m.group(1))
            assert set(gd['races']) == set(G['races']) and len(gd['classes']) == 9 and len(gd['profs']) == 9, rel
            assert all(r['n'] for r in gd['races'].values()) and all(c['n'] for c in gd['classes'].values()), rel
            assert f"LANG = '{lang}'" in html and 'window.GabellaMe' in html, rel
            hidden = sub != 'roster/'
            assert ('<meta name="robots" content="noindex">' in html) == hidden, rel
            assert (f'<loc>https://gabella.site/wow/{rel}</loc>' in sitemap) != hidden, rel
            if lang != 'ru':   # Russian left only in the language menu autonyms
                body = re.sub(r'<a [^>]*\blang="(ru|uk)"[^>]*>.*?</a>', '', html, flags=re.S)
                body = re.sub(r'const H = \{.*?\}, cur', '', body)   # the language hint speaks every language
                if lang != 'uk':
                    assert not re.search('[А-Яа-яЁё]', re.sub(r'"n":"[^"]*"', '', body)), (rel, re.findall('[А-Яа-яЁё][^<\n]{0,30}', body)[:3])


def test_radio_tells_me_js():
    js = open(os.path.join(ROOT, 'assets', 'radio', 'radio.js'), encoding='utf-8').read()
    for ev in ("emit('on')", "emit('minute')", "emit('station', id)", "emit('sleep')"):
        assert ev in js, ev
    me = open(os.path.join(ROOT, 'assets', 'me', 'me.js'), encoding='utf-8').read()
    for key in ('radio_on', 'radio_min', 'sleep_timer', "'station'", 'party5', 'raid40', 'share_team', 'compare3', 'play_page'):
        assert key in me, key
    for egg in G['sets']['egg']:
        assert f"'{egg}'" in me, egg


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_'):
            fn()
    print('OK')
