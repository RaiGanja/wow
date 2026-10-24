"""Поиск по сайту (Ctrl+K): индекс на каждый язык -> assets/search/<lang>.json. build.py зовёт search.main() после seo.py.
Читает уже собранные страницы:
  * страница — заголовок h1, раздел из хлебных крошек, title и description для совпадений;
  * разделы <section id> с h2 — ссылка с якорем, текст раздела для совпадений и выдержки;
  * вопросы FAQ <details id>; подземелья из DUNGEONS (на en/uk/pl англ. названия, на ru и de/fr/es/pt/it официальные + английское).
Запись индекса: [заголовок, где (страница/раздел), путь от корня гида, вид 0 страница/1 раздел/2 вопрос/3 подземелье, ключи, текст];
«где» тоже ищется наравне с ключами: «паладин танк» находит разделы страницы паладина.
Затем ставит ?v=<хэш> скриптам поиска во всех страницах: Cloudflare держит /wow/assets/ 30 дней, новый адрес обходит кэш.
Запуск: python search.py"""
import hashlib, json, os, re, sys
from html import unescape

import build
from build import LANGS, page_dir
import seo

HERE = build.HERE
OUT = os.path.join(HERE, 'assets', 'search')
SKIP = {'top', 'more', 'others'}          # шапка страницы и плитки «Другие …» — не разделы
TEXT_MAX = 1500                            # хватает на совпадения и выдержку, индекс языка ~150 КБ


def text(html):
    html = re.sub(r'<(script|style|svg|template)\b.*?</\1>|<span class="src">.*?</span>', ' ', html, flags=re.S)
    s = unescape(re.sub(r'<[^>]+>', ' ', html)).replace('\xad', '')
    return re.sub(r'\s+', ' ', s).strip()


def page_entries(html, path, lang, crumb):
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.S)
    title = text(h1[1]) if h1 else crumb
    meta = re.search(r'<title>(.*?)</title>', html)[1] + ' ' + re.search(r'<meta name="description" content="([^"]*)"', html)[1]
    url = page_dir(lang, path)
    top = re.search(r'<section\b[^>]*\sid="top"[^>]*>(.*?)</section>', html, re.S)   # шапка: подзаголовок, роли, факты
    out = [[title, crumb, url, 0, unescape(meta), text(top[1])[:TEXT_MAX] if top else '']]
    for m in re.finditer(r'<section\b[^>]*\sid="([^"]+)"[^>]*>(.*?)</section>', html, re.S):
        sid, body = m[1], m[2]
        h2 = re.search(r'<h2[^>]*>(.*?)</h2>', body, re.S)
        if sid in SKIP or not h2:
            continue
        rest = body[h2.end():]
        out.append([text(h2[1]), title, f'{url}#{sid}', 1, '', text(re.sub(r'<details\b.*?</details>', ' ', rest, flags=re.S))[:TEXT_MAX]])
    for m in re.finditer(r'<details id="([^"]+)"><summary>(.*?)</summary>(.*?)</details>', html, re.S):
        out.append([text(m[2]), title, f'{url}#{m[1]}', 2, '', text(m[3])[:TEXT_MAX]])
    return out


Q = r"""(?:'([^']*)'|"([^"]*)")"""
DG_RX = re.compile(rf"^  \[{Q}, (\d+), (\d+), {Q}", re.M)


# русские названия классических подземелий (клиент ruRU) — ключи поиска на ru/uk (uk пишет английские, ru — русские + английское)
RU_DG = {'Ragefire Chasm': 'Огненная пропасть', 'The Deadmines': 'Мертвые копи', 'Wailing Caverns': 'Пещеры Стенаний',
         'Shadowfang Keep': 'Крепость Темного Клыка', 'Blackfathom Deeps': 'Непроглядная Пучина', 'The Stockade': 'Тюрьма Штормграда',
         'Gnomeregan': 'Гномреган', 'Razorfen Kraul': 'Лабиринты Иглошкурых', 'Razorfen Downs': 'Курганы Иглошкурых',
         'Scarlet Monastery': 'Монастырь Алого ордена', 'Graveyard': 'Кладбище', 'Library': 'Библиотека', 'Armory': 'Оружейная',
         'Cathedral': 'Собор', 'Uldaman': 'Ульдаман', "Zul'Farrak": "Зул'Фаррак", 'Maraudon': 'Мародон',
         "Temple of Atal'Hakkar": "Храм Атал'Хаккара Затонувший храм", 'Blackrock Depths': 'Глубины Черной горы',
         'Lower Blackrock Spire': 'Нижняя часть пика Черной горы', 'Upper Blackrock Spire': 'Верхняя часть пика Черной горы',
         'Dire Maul': 'Забытый город', 'East': 'Восток', 'West': 'Запад', 'North': 'Север', 'Stratholme': 'Стратхольм',
         'Scholomance': 'Некроситет', 'City of Dalaran': 'Даларан', 'Ruins of Lordaeron': 'Руины Лордерона'}


def ru_alias(en):
    return ' '.join(RU_DG[w] for w in dict.fromkeys([en] + en.split(': ')) if w in RU_DG)


def dungeons(lang):
    """DUNGEONS из собранной страницы подземелий: [(название, английское, уровни, зона)]."""
    def rows(l):
        html = open(os.path.join(HERE, page_dir(l, 'guides/dungeons/'), 'index.html'), encoding='utf-8').read()
        return [(a or b, int(lo), int(hi), c or d) for a, b, lo, hi, c, d in DG_RX.findall(html)]
    en = rows('en')
    return [(n, e[0], f'{a}–{b}' if a != b else str(a), z) for (n, a, b, z), e in zip(rows(lang), en)]


def en_title(path):
    """h1 of the English page: players type class, race and dungeon names in English on any language (mage, warlock)."""
    f = os.path.join(HERE, page_dir('en', path), 'index.html')
    h1 = os.path.isfile(f) and re.search(r'<h1[^>]*>(.*?)</h1>', open(f, encoding='utf-8').read(), re.S)
    return text(h1[1]) if h1 else ''


def index(lang, meta):
    items = []
    for path in (p for p in meta if lang in meta[p]):
        html = open(os.path.join(HERE, page_dir(lang, path), 'index.html'), encoding='utf-8').read()
        cr = seo.crumbs(path, lang)
        rows = page_entries(html, path, lang, cr[-2][0] if cr else '')
        en = en_title(path) if lang != 'en' else ''
        if en and en.lower() != rows[0][0].lower():
            rows[0][4] = f'{en} {rows[0][4]}'
        items += rows
    dg = next(i for i in items if i[3] == 0 and i[2] == page_dir(lang, 'guides/dungeons/'))
    for name, en, lv, zone in dungeons(lang):
        keys = ' '.join(filter(None, [en if en != name else '', ru_alias(en) if lang in ('ru', 'uk') else '']))
        if re.search("['’]", name + keys):   # Zul'Farrak -> ZulFarrak: the query without the apostrophe finds it too
            keys = f'{keys} {re.sub("['’]", "", f"{name} {keys}")}'.strip()
        items.append([name, f'{dg[0]} · {lv} · {zone}', dg[2] + '#list', 3, keys, ''])
    return items


def main():
    meta = seo.page_meta()
    os.makedirs(OUT, exist_ok=True)
    h = hashlib.sha1()
    for lang in LANGS:
        data = json.dumps(index(lang, meta), ensure_ascii=False, separators=(',', ':'))
        open(os.path.join(OUT, f'{lang}.json'), 'w', encoding='utf-8', newline='\n').write(data + '\n')
        h.update(data.encode())
    for f in ('search.js', 'search.css'):
        h.update(build.read_norm(os.path.join(OUT, f)))   # the same version on LF and CRLF checkouts
    v = h.hexdigest()[:10]
    n = 0
    for d, dirs, files in os.walk(HERE):
        dirs[:] = [x for x in dirs if not x.startswith('.') and x not in ('assets', 'content', 'i18n', 'tests', 'node_modules')]   # tools/ is a page too
        for f in files:
            if f.endswith('.html') and not f.endswith('.src.html'):
                p = os.path.join(d, f)
                html = open(p, encoding='utf-8').read()
                new = re.sub(r'(assets/search/search\.(?:js|css))(?:\?v=\w+)?', rf'\1?v={v}', html)
                if new != html:
                    open(p, 'w', encoding='utf-8', newline='\n').write(new)
                    n += 1
    print(f'search: {len(LANGS)} languages, {n} pages, v={v}', file=sys.stderr)


if __name__ == '__main__':
    main()
