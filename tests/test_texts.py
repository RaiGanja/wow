"""Русские тексты собранных страниц: подстановка официальных названий без скобки в скобке и единые слова глоссария.
Запуск после python build.py: python tests/test_texts.py"""
import glob, html, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from langs import LANGS  # noqa: E402

SKIP = set(LANGS[1:]) | {'assets', 'tools', 'tests', 'node_modules'}
# слово глоссария -> запретные варианты (роль «Лекарь», «резерв имён», «Инженерное дело», «места» в лагере, «персонаж»)
BANNED = {
    'Лекарь': r'\bХил\b|\bхила\b',
    'резерв имён': r'\bбронь\b|\bброни имён|\bбронир\w*',
    'Инженерное дело': r'\bИнженери[яию]\b',
    'места в лагере': r'\bслот\w*',
    'персонаж': r'\bгеро(й|я|ю|ем)\b',
    'Classic': r'\bVanilla\b',
    'урон по площади': r'\bАОЕ\b',
    'списки изменений': r'\bпатчноут\w*',
    'доступна обеим фракциям': r'\bиграбельн\w*',
    'Почёт': r'\bHonored\b',
    'забыть профессию': r'\bразучи\w*',
}


def ru_pages():
    for p in glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True):
        rel = os.path.relpath(p, ROOT).replace(os.sep, '/')
        if rel.split('/')[0] not in SKIP and not rel.startswith('.') and '.src.' not in rel:
            yield rel, open(p, encoding='utf-8').read()


def visible(page):
    page = re.sub(r'<head\b.*?</head>|<script\b.*?</script>|<style\b.*?</style>', ' ', page, flags=re.S)
    return html.unescape(re.sub(r'<[^>]+>', '', page))


def test_names_without_nested_brackets():
    bad = []
    for rel, page in ru_pages():
        text = visible(page)
        bad += [f'{rel}: …{text[max(0, m.start() - 50):m.end() + 20]}…' for m in re.finditer(r'\)\s*\(|\)\)', text)]
    assert not bad, '\n'.join(bad)


def test_ru_glossary():
    texts = list(ru_pages()) + [(f, open(os.path.join(ROOT, f), encoding='utf-8').read())
                                for f in ('assets/me/i18n-ru.json', 'assets/search/ru.json')]
    bad = [f'{rel}: «{m[0]}» → {word}' for rel, page in texts
           for word, rx in BANNED.items() for m in re.finditer(rx, page)]
    assert not bad, '\n'.join(bad[:40])


def test_en_dates_month_first():
    """04.11 reads as April 11 in the US: English pages say «Nov 4»."""
    import build
    assert build.en_dates('Launch 04.11.2026, names 27.10 – 03.11, $29.99, v1.12') == 'Launch Nov 4, 2026, names Oct 27 – Nov 3, $29.99, v1.12'
    bad = []
    for p in glob.glob(os.path.join(ROOT, 'en', '**', '*.html'), recursive=True):
        text = re.sub(r'<style\b.*?</style>', '', open(p, encoding='utf-8').read(), flags=re.S)
        bad += [f'{os.path.relpath(p, ROOT)}: {m[0]}' for m in build.EN_DATE.finditer(text)]
    assert not bad, '\n'.join(bad[:20])


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_'):
            fn()
    print('OK')
