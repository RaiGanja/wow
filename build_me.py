"""Профили: тексты для assets/me/me.js -> assets/me/i18n-<lang>.json (названия и описания достижений, подсказки секретов,
ранги, рамки, категории, очки, подписи тоста и шапки). Страницы «Состав», «Мой профиль», /u/ берут их же.
Русский исходник — content/achievements.py и UI ниже; en/uk — i18n/me.{ru,en,uk}.txt (строка в строку),
новые языки — i18n/<lang>.json по английской строке (как весь сайт).
Запуск: python build_me.py  (build.py запускает его сам)"""
import json, os, sys

import build
import langs
from langs import LANGS

HERE = build.HERE
sys.path.insert(0, os.path.join(HERE, 'content'))
import achievements as A  # noqa: E402

_ru, _en, _uk = (build.load(f'me.{l}.txt') for l in langs.OLD)
assert len(_ru) == len(_en) == len(_uk), (len(_ru), len(_en), len(_uk))
build.T.update({r: (e, u) for r, e, u in zip(_ru, _en, _uk)})

UI = {'got': 'Достижение получено', 'rankUp': 'Новый ранг', 'profile': 'Мой профиль', 'login': 'Войти', 'pts': 'очков',
      'lvlAsk': 'На странице «В игре» у вас {n} уровень. Обновить персонажа {name}?', 'update': 'Обновить', 'notNow': 'Не сейчас'}


def strings():
    """Every Russian string me.js and the profile pages show, in a stable order (the line files follow it)."""
    out = list(UI.values()) + [c[1] for c in A.CATS] + [r[2] for r in A.RANKS] + [f[2] for f in A.FRAMES]
    for a in A.ACH:
        out += [a[5], a[6]] + ([a[7]] if len(a) > 7 else [])
    return [s for s in dict.fromkeys(out) if any('А' <= ch <= 'я' or ch in 'Ёё' for ch in s)]


def texts(lang):
    missing = [s for s in strings() if s not in build.T]
    t = lambda s: build.tr(s, lang)   # noqa: E731
    ach = {}
    for a in A.ACH:
        ach[a[0]] = [t(a[5]), t(a[6])] + ([t(a[7])] if len(a) > 7 else [])
    return {
        'ui': {k: t(v) for k, v in UI.items()},
        'cats': {c[0]: t(c[1]) for c in A.CATS},
        'ranks': {r[0]: t(r[2]) for r in A.RANKS},
        'frames': {f[0]: t(f[2]) for f in A.FRAMES},
        'ach': ach,
        'pts': {a[0]: a[2] for a in A.ACH},
        'secret': [a[0] for a in A.ACH if len(a) > 7],
    }, missing


def main():
    os.makedirs(os.path.join(HERE, 'assets', 'me'), exist_ok=True)
    allmissing = []
    for lang in LANGS:
        data, missing = texts(lang)
        allmissing += missing
        with open(os.path.join(HERE, 'assets', 'me', f'i18n-{lang}.json'), 'w', encoding='utf-8', newline='\n') as f:
            json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
            f.write('\n')
    uniq = list(dict.fromkeys(allmissing))
    if uniq:
        print('build_me: no en/uk line for:\n' + '\n'.join(uniq), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
