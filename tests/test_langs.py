"""Юнит-тесты языков (langs.py). Запуск: python tests/test_langs.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import langs


def with_overlay(fn):
    def run():
        ov, names, miss = dict(langs.OV), dict(langs.NAMES), {k: list(v) for k, v in langs.MISSING.items()}
        langs.OV['de'] = {'Hello': 'Hallo', 'Tip': 'Tipp', 'Guides': 'Guides DE'}
        langs.NAMES.clear()
        langs.NAMES['Mortal Strike'] = {'de': 'Tödlicher Stoß', 'fr': 'Frappe mortelle'}
        try:
            fn()
        finally:
            langs.OV.clear(); langs.OV.update(ov)
            langs.NAMES.clear(); langs.NAMES.update(names)
            langs.MISSING.clear(); langs.MISSING.update(miss)
    run.__name__ = fn.__name__
    return run


@with_overlay
def test_ov_and_missing():
    assert langs.ov('Hello', 'de') == 'Hallo'
    assert langs.ov('Nope', 'de') == 'Nope' and 'Nope' in langs.MISSING['de']


@with_overlay
def test_fill_adds_new_languages_by_english():
    d = langs.fill({'title': {'ru': 'Привет', 'en': 'Hello', 'uk': 'Привіт'}, 'n': 3})
    assert d['title']['de'] == 'Hallo' and d['title']['pl'] == 'Hello' and d['n'] == 3


@with_overlay
def test_derive_keeps_links():
    d = langs.derive({'ru': [('Гайды', 'guides/')], 'en': [('Guides', 'guides/')], 'uk': [('Гайди', 'guides/')]})
    assert d['de'] == [('Guides DE', 'guides/')], d['de']


@with_overlay
def test_official_names():
    assert langs.name('Mortal Strike', 'de') == 'Tödlicher Stoß'
    assert langs.name('Mortal Strike', 'pl') == 'Mortal Strike'      # no Polish client: English
    assert langs.name('Mortal Strike', 'es') == 'Mortal Strike'      # not in names.json yet: English
    assert langs.name('Unknown', 'de') == 'Unknown'


def test_check_chars():
    assert langs.check_chars('Tip', 'l’arme')
    assert not langs.check_chars('Tip', "l'arme")
    assert langs.check_chars('a "b"', 'x "y"')
    assert not langs.check_chars('Level {n}', 'Stufe <n>')


def test_tables():
    assert set(langs.HREFLANG) == set(langs.LOCALE) == set(langs.AUTONYM) == set(langs.ALL)
    assert langs.HREFLANG['pt'] == 'pt-BR' and langs.LOCALE['pt'] == 'pt_BR'
    assert langs.LANGS[:3] == ('ru', 'en', 'uk')


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_'):
            fn()
    print('OK')
