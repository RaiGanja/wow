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


def test_js_names_zones():
    import build
    js = """const DUNGEONS = [
  ['The Deadmines', 15, 22, 'Westfall', 0],
  ["Shaper's Terrace", 58, 60, "Un'Goro Crater", 1],
  ['Nowhere Hall', 1, 2, 'Nowhere', 0]
];"""
    fr = build.js_names(js, 'fr')
    assert "'Marche de l’Ouest'" in fr and '"Cratère d’Un’Goro"' in fr               # double-quoted names localized too
    assert "'Nowhere'" in fr                                                         # unknown name stays English
    assert all(build.js_names(js, l) == js for l in ('uk', 'en', 'pl'))            # English client: names as in game
    ru = build.js_names(js, 'ru')                                                    # ruRU client: Russian, dungeon + (English)
    assert "'Мертвые копи (The Deadmines)'" in ru and "'Западный Край'" in ru and "'Nowhere'" in ru, ru


def test_ru_names():
    import build
    html = ('<html><head><title>Durotar</title></head><body><p>Столица Orgrimmar, путь в [[Дуротаре|Durotar]]. '
            'Снова Orgrimmar и Durotar.</p><span lang="en">Thunder Bluff</span><p>Thunder Bluff, '
            'Holstered Replica Ironforge Air Rifle</p><script>const T = "у [[Пылевых топей|Dustwallow Marsh]], Orgrimmar", E = "Orgrimmar";</script></body></html>')
    out = build.ru_names(html)
    assert '<title>Durotar</title>' in out                                           # head untouched
    assert 'Столица Оргриммар (Orgrimmar), путь в Дуротаре (Durotar). Снова Оргриммар и Дуротар.' in out, out
    assert '<p>Громовой Утес, Holstered Replica Ironforge Air Rifle</p>' in out, out  # English shown before; no partial names
    assert '"у Пылевых топей, Оргриммар", E = "Orgrimmar"' in out, out                # script: Russian strings only, no (English)
    assert '[[' not in out
    assert build.ru_plain('Мертвые копи (The Deadmines), Orgrimmar') == 'Мертвые копи (The Deadmines), Оргриммар'   # English in brackets stays


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_'):
            fn()
    print('OK')
