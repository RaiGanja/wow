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
    assert '<base href="/wow/">' in root and "fetch('/wow/' + m[1] + '/404.html')" in root
    for lang in LANGS[1:]:
        nf = page(lang, '404.html')
        assert f'<base href="/wow/{lang}/">' in nf and 'noindex' in nf and 'fetch(' not in nf, lang


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
