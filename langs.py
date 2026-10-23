"""Языки гида.
Старые три (ru, en, uk) переводятся как раньше: i18n/{ru,en,uk}.txt строка в строку и t(ru, en, uk) в контенте.
Новые — по английскому ключу: i18n/<lang>.json = {английская строка: перевод}. Язык собирается, когда его json есть.
Официальные игровые названия (Wowhead) — i18n/names.json = {английское: {de, fr, es, pt, it, ru}}; у pl — английские, как у uk.
ru берёт их в build.ru_names: «Оргриммар (Orgrimmar)» при первом упоминании, падежи — разметкой [[Оргриммаре|Orgrimmar]].
Заготовка для переводчика: python build.py --missing <lang>  (JSON {английская строка: ""} всего, что ещё не переведено)."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ALL = ('ru', 'en', 'uk', 'de', 'fr', 'es', 'pt', 'it', 'pl')
OLD = ALL[:3]
NAMED = ('de', 'fr', 'es', 'pt', 'it')        # languages with an official game client: ability names localized + English
HREFLANG = {l: l for l in ALL} | {'pt': 'pt-BR'}
LOCALE = {'ru': 'ru_RU', 'en': 'en_US', 'uk': 'uk_UA', 'de': 'de_DE', 'fr': 'fr_FR', 'es': 'es_ES', 'pt': 'pt_BR', 'it': 'it_IT', 'pl': 'pl_PL'}
AUTONYM = {'ru': 'Русский', 'en': 'English', 'uk': 'Українська', 'de': 'Deutsch', 'fr': 'Français', 'es': 'Español',
           'pt': 'Português (Brasil)', 'it': 'Italiano', 'pl': 'Polski'}
BAD = set('\'"`<>{}')                         # break the Russian-segment parser and JS strings unless the source has them


def _json(name):
    path = os.path.join(HERE, 'i18n', name)
    if not os.path.exists(path):
        return None
    with open(path, encoding='utf-8') as f:
        return json.load(f)


OV = {l: _json(f'{l}.json') for l in ALL[3:]}
_force = os.environ.get('WF_LANG')            # build.py --missing <lang>: build a language that has no json yet
if _force in OV and OV[_force] is None:
    OV[_force] = {}
LANGS = OLD + tuple(l for l in ALL[3:] if OV[l] is not None)
NEW = LANGS[3:]
NAMES = _json('names.json') or {}
MISSING = {l: [] for l in ALL[3:]}


def check_chars(en, text):
    """False when the translation brings quote/bracket characters the English source does not have."""
    return not ((set(text) & BAD) - set(en))


def ov(en, lang):
    """Translation of an English string into a new language; English (and a MISSING record) when there is none."""
    text = (OV.get(lang) or {}).get(en)
    if not text:
        MISSING[lang].append(en)
        return en
    return text


def name(en, lang):
    """Official in-game name: localized for de/fr/es/pt/it, English for the rest."""
    return NAMES.get(en, {}).get(lang) or en if lang in NAMED else en


def _map(x, lang):
    if isinstance(x, str):
        return x if not x.strip() or x.endswith('/') or x.startswith(('http', '#', 'mailto:')) else ov(x, lang)
    if isinstance(x, (list, tuple)):
        return type(x)(_map(v, lang) for v in x)
    if isinstance(x, dict):
        return {k: _map(v, lang) for k, v in x.items()}
    return x


def derive(d):
    """{'ru': …, 'en': …, 'uk': …} of any shape (strings, tuples, dicts): add the new languages from the English value.
    Strings that look like links ('guides/', 'https://…') stay as they are."""
    for l in ALL[3:]:
        if l not in d:
            d[l] = _map(d['en'], l)
    return d


def fill(obj):
    """Walk content (guides, SEO texts): every {'ru','en','uk'} string dict gets the new languages via derive()."""
    if isinstance(obj, dict):
        if set(OLD) <= set(obj) <= set(ALL):
            return derive(obj)
        for v in obj.values():
            fill(v)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            fill(v)
    return obj


def missing_json(lang, english):
    """Template for a translator: every English string of the site the language still lacks."""
    have = OV.get(lang) or {}
    return json.dumps({e: '' for e in dict.fromkeys(english) if e.strip() and e not in have}, ensure_ascii=False, indent=1)
