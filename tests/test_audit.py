"""Проверки собранных страниц: язык браузера на корне, ссылки на классы и расы без JS, время старта,
404 на языке адреса, шрифты под письмо языка. Запуск после python build.py: python tests/test_audit.py"""
import os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from langs import LANGS  # noqa: E402


def page(*parts):
    if not parts or not parts[-1].endswith('.html'):
        parts += ('index.html',)
    return open(os.path.join(ROOT, *parts), encoding='utf-8').read()


def lang_dir(lang):
    return () if lang == 'ru' else (lang,)


def test_auto_lang_only_on_russian_root():
    ru = page('index.html')
    assert ru.index("getItem('gabella-lang')") < ru.index('<title>')
    assert all(f'"{l}": "{"./" if l == "ru" else l + "/"}"' in ru for l in LANGS)
    for lang in LANGS[1:]:
        assert "getItem('gabella-lang')" not in page(lang), lang
    assert "getItem('gabella-lang')" not in page('classes', 'mage')


def test_language_menu_saves_choice():
    assert "localStorage.setItem('gabella-lang', l)" in page('guides', 'faq')


def test_class_and_race_links_without_js():
    for lang in LANGS:
        home = page(*lang_dir(lang))
        roster = re.search(r'id="roster">(.*?)</div>', home).group(1)
        assert roster.count('href="classes/') == 9, lang
        assert re.search(r'id="rosterA">(.*?)</div>', home).group(1).count('href="races/') == 5, lang
        assert page(*lang_dir(lang), 'classes').count('href="../classes/') >= 9, lang
        assert page(*lang_dir(lang), 'races').count('href="../races/') >= 10, lang


def test_launch_time_local_not_kyiv():
    for lang in LANGS:
        faq = page(*lang_dir(lang), 'guides', 'faq')
        assert faq.count('<time class="lt" datetime="2026-11-04T23:00:00Z">') == 2, lang
        assert "querySelectorAll('time.lt')" in faq
        assert not re.search(r'01:00[^<]{0,40}(Kyiv|Kiew|Kijowie|Киеве|Києві)', faq), lang


def test_not_found_per_language():
    root = page('404.html')
    assert '<base href="/wow/">' in root and "location.replace('/wow/' + m[1] + '/404.html')" in root
    assert 'document.write' not in root                       # writing over the page clashes with its globals
    for lang in LANGS[1:]:
        nf = page(lang, '404.html')
        assert f'<base href="/wow/{lang}/">' in nf and 'noindex' in nf and 'location.replace(' not in nf, lang
        assert "history.replaceState(null, '', p)" in nf, lang
    for lang in LANGS:                                         # "where next": absolute links to every home, not ./en/ under <base>
        nf = page(*lang_dir(lang), '404.html')
        links = re.search(r'<p class="nf-langs">(.*?)</p>', nf).group(1)
        assert re.findall(r'href="([^"]+)"', links) == ['/wow/'] + [f'/wow/{l}/' for l in LANGS[1:]], lang


def test_launch_countdown_at_23_utc():
    for lang in LANGS:
        home = page(*lang_dir(lang))
        assert "rel = new Date('2026-11-04T23:00:00Z')" in home and "const D_REL = new Date('2026-11-04T23:00:00Z')" in home, lang
        assert 'data-d="2026-11-04T23:00:00Z"' in home, lang
    for lang in LANGS:
        faq = page(*lang_dir(lang), 'guides', 'faq')
        assert not re.search(r'(не подтвердила|not yet confirmed|не підтвердила)', faq), lang


def test_guide_heroes_own_scenes():
    for slug, fx in (('', 'guides'), ('dungeons', 'dungeons'), ('faq', 'faq'), ('professions', 'professions')):
        for lang in LANGS:
            html = page(*lang_dir(lang), 'guides', *((slug,) if slug else ()))
            assert f'<picture class="thero-art" aria-hidden="true" data-fx="{fx}"' in html, (lang, slug)
            assert '@@HERO@@' not in html and 'assets/living/living.js' in html, (lang, slug)


def test_share_card_not_the_old_one():
    for lang in LANGS:
        for sub in ('profile', 'roster', 'g', 'u'):
            html = page(*lang_dir(lang), sub)
            assert 'assets/og.png' not in html and f'assets/og-{lang}.jpg' in html, (lang, sub)


def test_no_tool_names_in_sources():
    import codecs, subprocess
    files = subprocess.run(['git', 'ls-files'], cwd=ROOT, capture_output=True, text=True, encoding='utf-8').stdout.splitlines()
    bad = re.compile(codecs.decode(r'trzvav|anab onanan|naguebcvp|bcranv|(?<!\.)pynhqr|pb-nhguberq-ol', 'rot13'), re.I)   # tool names stay out of the public sources, this list too
    hits = []
    for f in files:
        if not f.endswith(('.py', '.txt', '.json', '.md', '.js', '.css', '.sh', '.yml', '.mjs', '.webmanifest')) and not f.endswith('.src.html'):
            continue
        try:
            text = open(os.path.join(ROOT, f), encoding='utf-8').read()
        except (OSError, UnicodeDecodeError):
            continue
        hits += [f for _ in bad.finditer(text)][:1]
    assert not hits, hits


def test_fonts_preloaded_for_the_script():
    for lang in LANGS:
        head = page(*lang_dir(lang))[:6000]
        want, other = ('cyrillic', 'latin') if lang in ('ru', 'uk') else ('latin', 'cyrillic')
        assert f'golos-text-{want}.woff2" as="font"' in head and f'golos-text-{other}.woff2" as="font"' not in head, lang


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_'):
            fn()
    print('OK')
