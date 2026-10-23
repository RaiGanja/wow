"""Профили: тексты для assets/me/me.js -> assets/me/i18n-<lang>.json (названия и описания достижений, подсказки секретов,
ранги, рамки, категории, очки, подписи тоста и шапки) и страницы «Состав» (roster/), «Мой профиль» (profile/), игрок (u/).
Страницы: оболочка me.src.html + общие me-pages.src.css/js + фрагмент roster|profile|player.src.html (style, body, script).
Русский исходник — content/achievements.py, UI ниже и русский текст страниц; en/uk — i18n/me.{ru,en,uk}.txt (строка в строку),
новые языки — i18n/<lang>.json по английской строке (как весь сайт).
Запуск: python build_me.py [--list]  (build.py запускает его сам; --list печатает русские фрагменты страниц без перевода)"""
import json, os, re, sys

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
      'lvlAsk': 'На странице «В игре» у вас {n} уровень. Обновить персонажа {name}?', 'update': 'Обновить', 'notNow': 'Не сейчас',
      'menu': 'Меню профиля', 'myPage': 'Моя страница ↗', 'chars': 'Персонажи', 'look': 'Внешний вид', 'account': 'Аккаунт',
      'newChar': 'Создать персонажа', 'noChar': 'Персонажа пока нет', 'logout': 'Выйти'}


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


PAGES = [('roster/', 'roster.src.html'), ('profile/', 'profile.src.html'), ('u/', 'player.src.html')]
NOINDEX = {'profile/', 'u/'}
INVITE = build.DISCORD   # кнопка «Вступить в Gabella Team» на экране «не участник»


def page_data(lang):
    """Game data the pages draw with: races and classes with names and colours, professions, achievement rules, ranks."""
    sys.path.insert(0, os.path.join(HERE, 'tools'))
    import export_game
    g = export_game.game()
    src = open(os.path.join(HERE, 'index.src.html'), encoding='utf-8').read()
    rn = {r['id']: r['n'] for r in build.parse_races(src)}
    block = src[src.index('const PROFS = ['):]
    pn = dict(re.findall(r"\['(\w+)', '([^']+)', 1,", block[:block.index('\n];')]))
    t = lambda s: build.tr(s, lang)   # noqa: E731
    return {
        'races': {rid: {'f': r['f'], 'cls': r['cls'], 'slug': r['slug'], 'n': t(rn[rid])} for rid, r in g['races'].items()},
        'classes': {c['id']: {'roles': g['classes'][c['id']]['roles'], 'n': t(c['n']), 'color': build.COLOR[c['id']]} for c in build.CLASSES},
        'profs': {p: t(pn[p]) for p in g['profs']},
        'sets': g['sets'], 'cats': g['cats'], 'ach': g['achievements'], 'ranks': g['ranks'], 'frames': g['frames'],
        'titles': g['titles'], 'backgrounds': g['backgrounds'], 'deadline': g['deadline_founder'], 'invite': INVITE,
    }


def part(src, rx, name):
    m = re.search(rx, src, re.S)
    assert m, name
    return m.group(1).strip('\n')


def build_page(lang, sub, frag, shell, base_css, sprite, me_css, me_js):
    here = build.page_dir(lang, sub)
    root, home = build.rel(here, ''), build.rel(here, build.page_dir(lang))
    html = shell.replace('@@BASE_CSS@@', base_css).replace('@@SPRITE@@', sprite).replace('@@ME_CSS@@', me_css)
    html = html.replace('@@P_CSS@@', part(frag, r'<style>(.*?)</style>', 'style'))
    html = html.replace('@@P_BODY@@', part(frag, r'<!--body-->(.*?)<!--/body-->', 'body'))
    html = html.replace('@@ME_JS@@', me_js).replace('@@P_JS@@', part(frag, r'<script>(.*?)</script>', 'script'))
    name = part(frag, r'<h1[^>]*>(.*?)</h1>', 'h1')
    html = html.replace('@@P_NAME@@', re.sub('<[^>]+>', '', name))
    html = html.replace('@@P_ROBOTS@@', '<meta name="robots" content="noindex">\n' if sub in NOINDEX else '')
    html = html.replace('@@NAV_ROSTER@@', ' aria-current="true"' if sub == 'roster/' else '')
    html = html.replace('@@NAV_PROFILE@@', ' aria-current="true"' if sub == 'profile/' else '')
    html, missing = build.translate(html, lang)
    html = html.replace('@@GD@@', json.dumps(page_data(lang), ensure_ascii=False, separators=(',', ':')))
    html = html.replace('@@LANG@@', lang).replace('@@HOME@@', home).replace('@@CANON@@', build.SITE + here)
    html = html.replace('@@ALTERNATES@@', build.alternates(sub))
    html = build.localize(html, lang, here)
    return here + 'index.html', html, missing


def build_pages():
    src = open(os.path.join(HERE, 'index.src.html'), encoding='utf-8').read()
    base_css = src[src.index('<style>') + 7:src.index('</style>')].strip('\n')
    s0 = src.index('<svg width="0" height="0"')
    sprite = src[s0:src.index('</svg>', s0) + 6]
    read = lambda n: open(os.path.join(HERE, n), encoding='utf-8').read()   # noqa: E731
    shell, me_css, me_js = read('me.src.html'), read('me-pages.src.css'), read('me-pages.src.js')
    out, missing = [], []
    for lang in LANGS:
        for sub, name in PAGES:
            path, html, miss = build_page(lang, sub, read(name), shell, base_css, sprite, me_css, me_js)
            assert '@@' not in html, (path, re.findall(r'@@\w+@@', html)[:5])
            out.append((path, html))
            missing += miss
    return out, missing


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
    pages, missing = build_pages()
    uniq = list(dict.fromkeys(missing))
    if '--list' in sys.argv:          # build.py --list / --missing: report, write nothing
        if '--missing' not in sys.argv:
            print('\n'.join(uniq))
        return
    for path, html in pages:
        full = os.path.join(HERE, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        open(full, 'w', encoding='utf-8', newline='\n').write(html)
    print(f'build_me: pages {len(pages)}, missing {len(uniq)}', file=sys.stderr)
    if uniq:
        sys.exit(1)


if __name__ == '__main__':
    main()
