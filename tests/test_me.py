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
        assert f.get('rank') in ranks or f.get('ach') in ach or f.get('admin') or f.get('unlock'), f
    assert set(G['titles']) <= ach | {'pioneer'}
    assert 'pioneer' in G['titles'] and {'id': 's1', 'unlock': 's1'} in G['frames']


def test_progression_catalog():
    P = G['progression']
    assert P['glory'] == {'max': 60, 'a': 60, 'b': 14, 'p': 1.15}
    assert set(P['sources']) == {'visit', 'radio', 'page', 'tool'}
    ids = [t['id'] for t in P['weekly']]
    assert len(ids) == len(set(ids)) and len(ids) >= 30
    for t in P['weekly']:
        assert t['cat'] in P['weekly_cats']
        assert t['key'] in G['sets'] or t['key'] in G['flags'] or t['key'] in ('visit', 'radio_min', 'lfg')
        if t.get('item') is not None:
            assert t['item'] in G['sets'][t['key']], t
    for c in P['weekly_cats']:
        assert sum(t['cat'] == c for t in P['weekly']) >= 4, c   # 4 недели без повторов
    steps = P['track']['s1']
    assert len(steps) == 30 and [s['stars'] for s in steps] == sorted(s['stars'] for s in steps)
    rewards = [s['reward'] for s in steps if s.get('reward')]
    assert {'badge:s1', 'title:pioneer', 'frame:s1', 'bg:s1-1', 'bg:s1-2'} <= set(rewards)
    assert [c for c, _ in P['name_colors']] == ['poor', 'common', 'uncommon', 'rare', 'epic', 'legendary']


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
        m = re.search(r'<script src="[^"]*assets/me/me\.js\?v=\w{10}" data-root="([^"]*)" data-home="([^"]*)" data-lang="(\w+)" data-teaser="([^"]+)" data-close="([^"]+)" data-page="([^"]*)"( data-solo="1")? defer>', html)
        assert m, p
        page = m.group(6)
        # only a language-only guide (uk «ukrainian») is marked: it is not in the guide set, so me.js does not track it
        assert bool(m.group(7)) == (page == 'guides/ukrainian/'), p
        name = os.path.relpath(p, ROOT).replace(os.sep, '/')
        if name.endswith('404.html'):
            assert page == '404', name
        else:
            assert name.endswith(page + 'index.html'), (name, page)


def check_growth_texts(lang, t):
    """Growth texts (section g): the same keys everywhere, same placeholders as the Russian source, a title for each non-achievement title,
    a name for each season background and every weekly task (templates for the station, guide and class ones)."""
    import build_me
    g = t['g']
    assert set(g) == set(build_me.GROWTH), lang
    for k, ru in build_me.GROWTH.items():
        assert g[k], (lang, k)
        assert sorted(re.findall(r'\{\w+\}', g[k])) == sorted(re.findall(r'\{\w+\}', ru)), (lang, k, g[k])
        if lang != 'ru' and lang != 'uk' and re.search('[А-Яа-яЁё]', ru):
            assert g[k] != ru and not re.search('[А-Яа-яЁё]', g[k]), (lang, k, g[k])
    ach = {a['id'] for a in G['achievements']}
    assert set(t['titles']) == set(G['titles']) - ach and 'pioneer' in t['titles'], lang
    assert set(t['bg']) == {'s1-1', 's1-2'}, lang   # ids of the season backgrounds (R17)
    # me.js sends repeats of a key that feeds an open weekly task (R15): task id -> key comes with the texts
    assert t['wk'] == {w['id']: w['key'] for w in G['progression']['weekly']}, lang
    for w in G['progression']['weekly']:
        assert 'task_' + w['id'] in g or w['id'].split('_')[0] in ('st', 'g', 'c') and 'task_' + w['id'].split('_')[0] in g, (lang, w['id'])


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
        check_growth_texts(lang, t)
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


def test_roster_in_navigation():
    """Every full page links roster/ in the top menu and roster/ + profile/ in the sections sheet; privacy covers accounts."""
    for p in built_pages():
        html = open(p, encoding='utf-8').read()
        if 'class="mainnav"' not in html:
            continue
        nav = re.search(r'<nav class="mainnav".*?</nav>', html, re.S).group(0)
        toc = re.search(r'<nav class="toc".*?</nav>', html, re.S).group(0)
        assert re.search(r'href="[^"]*roster/"', nav), p
        assert re.search(r'href="[^"]*roster/"', toc) and re.search(r'href="[^"]*profile/"', toc), p
    from langs import LANGS
    for lang in LANGS:
        html = open(os.path.join(ROOT, '' if lang == 'ru' else lang, 'privacy', 'index.html'), encoding='utf-8').read()
        for sec in ('account', 'storage', 'delete'):
            assert f'id="{sec}"' in html, (lang, sec)
        assert 'https://discord.com/privacy' in html, lang


def test_me_js_growth_hooks():
    """R15: known() lets weekly-task keys and tool flags through; Glory and season toasts; the teaser costs no request."""
    me = open(os.path.join(ROOT, 'assets', 'me', 'me.js'), encoding='utf-8').read()
    assert 'party5|raid40|compare3|share_team' in me and 'T.wk' in me and 'state.week' in me
    for k in ("kind: 'glory'", "kind: 'step'", 'gabella-me-xp1', 'gabella-me-teaser', 'slice(0, 3)'):
        assert k in me, k
    teaser = me[me.index('function teaser()'):me.index("if (PAGE === 'tools/') toolsHooks();")]
    assert 'fetch(' not in teaser and 'api(' not in teaser and 'D.teaser' in teaser
    # signed-out visitors: nothing but the teaser runs before the login check
    assert me.index('teaser();') < me.index('if (logged() || AUTH_PAGE) me()')


def test_radio_tells_me_js():
    js = open(os.path.join(ROOT, 'assets', 'radio', 'radio.js'), encoding='utf-8').read()
    for ev in ("emit('on')", "emit('minute')", "emit('station', id)", "emit('sleep')"):
        assert ev in js, ev
    me = open(os.path.join(ROOT, 'assets', 'me', 'me.js'), encoding='utf-8').read()
    for key in ('radio_on', 'radio_min', 'sleep_timer', "'station'", 'party5', 'raid40', 'share_team', 'compare3', 'play_page'):
        assert key in me, key
    for egg in G['sets']['egg']:
        assert f"'{egg}'" in me, egg


def _lum(h):
    v = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    v = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in v]
    return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]


def contrast(a, b):
    x, y = sorted((_lum(a), _lum(b)), reverse=True)
    return (x + 0.05) / (y + 0.05)


def test_guilds_catalog():
    Gd = G['guilds']
    L = Gd['limits']
    assert L['members'] == 1000 and L['officers'] == 5 and L['create_glory'] == 5 and L['top'] == 10
    assert Gd['shapes'] == ['heater', 'round', 'kite', 'banner']
    assert Gd['fields'] == ['plain', 'pale', 'fess', 'quarterly', 'chevron', 'bend']
    assert len(Gd['palette']) == 12 and all(len(v) == 7 and v[0] == '#' for v in Gd['palette'].values())
    ids = [c['id'] for c in Gd['charges']]
    assert len(ids) == len(set(ids)) and sum(not c['lock'] for c in Gd['charges']) >= 24
    locked = {'charge:' + c['id'] for c in Gd['charges'] if c['lock']}
    assert locked <= set(Gd['banner_unlocks'])
    d = Gd['default_crest']
    assert d['i'] in ids and d['s'] in Gd['shapes'] and contrast(Gd['palette'][d['ic']], Gd['palette'][d['c'][0]]) >= L['contrast_min']
    # every colour has at least 4 readable charge colours: the constructor never runs out of choices
    for k, v in Gd['palette'].items():
        assert sum(contrast(v, w) >= L['contrast_min'] for w in Gd['palette'].values()) >= 4, k


def test_guild_authors():
    import guilds
    a = guilds.authors()
    assert len(a) == len(set(a)) and set(a) == {path.split('/')[0] for _, path, _ in guilds.CHARGES}
    assert a[0] == guilds.CHARGES[0][1].split('/')[0]
    for lang in ('', 'en/', 'uk/', 'de/', 'fr/', 'es/', 'pt/', 'it/', 'pl/'):
        html = open(os.path.join(ROOT, *(lang + 'privacy/index.html').split('/')), encoding='utf-8').read()
        assert 'game-icons.net' in html and ', '.join(a) in html, lang


def test_guild_texts():
    import build_me
    from langs import LANGS
    for lang in LANGS:
        with open(os.path.join(ROOT, 'assets', 'me', f'i18n-{lang}.json'), encoding='utf-8') as f:
            t = json.load(f)
        assert set(t['gl']) == set(build_me.GUILD), lang


def test_guild_page_built():
    from langs import LANGS
    for lang in LANGS:
        p = os.path.join(ROOT, *(([] if lang == 'ru' else [lang]) + ['g', 'index.html']))
        html = open(p, encoding='utf-8').read()
        assert 'noindex' in html and 'id="gl-head"' in html, lang
        assert re.search(r'assets/me/crest/charges\.svg\?v=\w{10}#c-', html), lang   # the sprite is versioned like me.js
        assert not re.search(r'assets/me/crest/charges\.svg(?!\?v=)', html), lang
    sm = open(os.path.join(ROOT, 'sitemap.xml'), encoding='utf-8').read()
    assert '/g/' not in sm


def test_crest_sprite():
    sprite = open(os.path.join(ROOT, 'assets', 'me', 'crest', 'charges.svg'), encoding='utf-8').read()
    ids = set(re.findall(r'<symbol id="c-([\w-]+)"', sprite))
    assert ids == {c['id'] for c in G['guilds']['charges']}
    assert 'fill=' not in sprite and len(sprite) < 120_000


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_'):
            fn()
    print('OK')
