"""Сборка гида: index.src.html (русский исходник) + i18n/{ru,en,uk}.txt (переводы, строка в строку) -> index.html, en/index.html, uk/index.html.
Запуск: python build.py [--list]  (--list печатает русские фрагменты без перевода)"""
import os, re, sys


def load(name):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'i18n', name), encoding='utf-8') as f:
        return f.read().splitlines()


_ru, _en, _uk = load('ru.txt'), load('en.txt'), load('uk.txt')
assert len(_ru) == len(_en) == len(_uk), (len(_ru), len(_en), len(_uk))
T = {r: (e, u) for r, e, u in zip(_ru, _en, _uk)}

HERE = os.path.dirname(os.path.abspath(__file__))
CYR = r'А-Яа-яЁё'
SEG = re.compile(r'(?:(?!\$\{)[^<>"\'`{}\n])*[' + CYR + r'](?:(?!\$\{)[^<>"\'`{}\n])*')


def split_ws(seg):
    core = seg.strip()
    i = seg.index(core)
    return seg[:i], core, seg[i + len(core):]


def translate(src, lang):
    missing = []

    def sub(m):
        lead, core, tail = split_ws(m.group(0))
        if lang == 'ru':
            return m.group(0)
        if core not in T:
            missing.append(core)
            return m.group(0)
        return lead + T[core][0 if lang == 'en' else 1] + tail
    return SEG.sub(sub, src), missing


def main():
    src = open(os.path.join(HERE, 'index.src.html'), encoding='utf-8').read()
    listing = '--list' in sys.argv
    outs = {'ru': 'index.html', 'en': 'en/index.html', 'uk': 'uk/index.html'}
    links = {'ru': ('../', '', 'en/', 'uk/'), 'en': ('../', '', '', '../uk/'), 'uk': ('../', '', '../en/', '')}
    allmissing = []
    for lang, rel in outs.items():
        html, missing = translate(src, lang)
        allmissing += missing
        ru_l = {'ru': './', 'en': '../', 'uk': '../'}[lang]
        en_l = {'ru': 'en/', 'en': './', 'uk': '../en/'}[lang]
        uk_l = {'ru': 'uk/', 'en': '../uk/', 'uk': './'}[lang]
        html = html.replace('@@RU@@', ru_l).replace('@@EN@@', en_l).replace('@@UK@@', uk_l)
        html = html.replace('@@ROOT@@', '' if lang == 'ru' else '../')
        if lang != 'ru':
            code = lang
            html = html.replace('<html lang="ru">', f'<html lang="{code}">')
            html = html.replace('content="ru_RU"', 'content="en_US"' if lang == 'en' else 'content="uk_UA"')
            for tag in ('rel="canonical" href', 'property="og:url" content'):
                html = html.replace(tag + '="https://raiganja.github.io/wow/"', tag + f'="https://raiganja.github.io/wow/{lang}/"')
            html = html.replace('rel="canonical" href="https://raiganja.github.io/wow/"', f'rel="canonical" href="https://raiganja.github.io/wow/{lang}/"')
            html = html.replace('assets/og.png', f'assets/og-{lang}.png')
            html = html.replace('data-lang="ru" hreflang="ru" lang="ru" aria-current="true"', 'data-lang="ru" hreflang="ru" lang="ru" aria-current="false"')
            html = html.replace(f'data-lang="{lang}" hreflang="{lang}" lang="{lang}" aria-current="false"', f'data-lang="{lang}" hreflang="{lang}" lang="{lang}" aria-current="true"')
        path = os.path.join(HERE, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if not listing:
            open(path, 'w', encoding='utf-8', newline='\n').write(html)
    uniq = sorted(set(allmissing), key=lambda x: src.find(x))
    if listing:
        import json
        print(json.dumps(uniq, ensure_ascii=False, indent=0))
    print(f'missing: {len(set(allmissing))}', file=sys.stderr)
    if allmissing and not listing:
        sys.exit(1)


if __name__ == '__main__':
    main()
