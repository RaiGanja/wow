"""Поиск по сайту на живых запросах: опечатки, название на чужом языке, сленг, вопросы новичка — на 9 языках.
Запрос верен, если нужная страница в первых трёх ответах. Движок — сам assets/search/search.js в node (tests/search_eval.js)
на собранном индексе. Запуск: python tests/test_search_queries.py [-v] [search.js [папка индекса]]  (-v: печатает и верные)
Ожидание: путь без языковой папки; 'x/' — страница x/ или её якорь (не глубже), 'x/#a' — ровно этот якорь, '' — главная."""
import json, os, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLASS = ['classes/', '#classes', 'tools/#picker', 'guides/tier-list/']           # «какой класс выбрать»: любой из выборов класса
START = ['guides/faq/#release', 'guides/faq/#dates']
PRICE = ['guides/faq/#price', 'guides/faq/#editions', 'guides/faq/#subscription']

Q = [
    # опечатки
    ('ru', 'палодин', ['classes/paladin/']), ('ru', 'чернокнижнек', ['classes/warlock/']), ('ru', 'друит', ['classes/druid/']),
    ('ru', 'разбийник', ['classes/rogue/']), ('ru', 'таурэн', ['races/tauren/']), ('ru', 'подземеля', ['guides/dungeons/']),
    ('ru', 'професии', ['guides/professions/']), ('ru', 'оргримар', ['races/orc/']), ('ru', 'шамаан', ['classes/shaman/']),
    ('en', 'wariror', ['classes/warrior/']), ('en', 'palladin', ['classes/paladin/']), ('en', 'warior', ['classes/warrior/']),
    ('en', 'orgrimar', ['races/orc/']), ('en', 'preist', ['classes/priest/']), ('en', 'rouge', ['classes/rogue/']),
    ('en', 'shamman', ['classes/shaman/']), ('en', 'proffesions', ['guides/professions/']), ('en', 'nigth elf', ['races/night-elf/']),
    ('en', 'warlok', ['classes/warlock/']),
    ('uk', 'чорнокнижнік', ['classes/warlock/']), ('uk', 'паладін', ['classes/paladin/']),
    ('de', 'kriger', ['classes/warrior/']), ('de', 'hexenmeiser', ['classes/warlock/']), ('fr', 'guerier', ['classes/warrior/']),
    ('fr', 'chasseurr', ['classes/hunter/']), ('es', 'guerero', ['classes/warrior/']), ('it', 'stregome', ['classes/warlock/']),
    ('pt', 'guereiro', ['classes/warrior/']), ('pl', 'wojownk', ['classes/warrior/']),
    # название на чужом языке и сленг
    ('ru', 'warrior', ['classes/warrior/']), ('ru', 'warlock', ['classes/warlock/']), ('ru', 'pally', ['classes/paladin/']),
    ('ru', 'mage', ['classes/mage/']), ('ru', 'night elf', ['races/night-elf/']), ('ru', 'rogue', ['classes/rogue/']),
    ('ru', 'хил', ['guides/tier-list/', '#classes', 'classes/priest/', 'classes/druid/', 'classes/shaman/', 'classes/paladin/']),
    ('ru', 'рога', ['classes/rogue/']), ('ru', 'лок', ['classes/warlock/']), ('ru', 'прист', ['classes/priest/']),
    ('ru', 'хант', ['classes/hunter/']), ('ru', 'шам', ['classes/shaman/']), ('ru', 'вар', ['classes/warrior/']),
    ('ru', 'данжи', ['guides/dungeons/']), ('ru', 'профы', ['guides/professions/']), ('ru', 'тирлист', ['guides/tier-list/']),
    ('ru', 'sfk', ['guides/dungeons/']), ('en', 'brd', ['guides/dungeons/']), ('de', 'brd', ['guides/dungeons/']),
    ('en', 'маг', ['classes/mage/']), ('en', 'воин', ['classes/warrior/']), ('en', 'ночной эльф', ['races/night-elf/']),
    ('en', 'pally', ['classes/paladin/']), ('en', 'lock', ['classes/warlock/']), ('en', 'tierlist', ['guides/tier-list/']),
    ('en', 'healer', ['guides/tier-list/', '#classes', 'classes/priest/', 'classes/druid/', 'classes/shaman/', 'classes/paladin/']),
    ('uk', 'warrior', ['classes/warrior/']), ('uk', 'воин', ['classes/warrior/']), ('uk', 'чернокнижник', ['classes/warlock/']),
    ('uk', 'хіл', ['guides/tier-list/', '#classes', 'classes/priest/', 'classes/druid/', 'classes/shaman/', 'classes/paladin/']),
    ('de', 'warrior', ['classes/warrior/']), ('de', 'rogue', ['classes/rogue/']), ('de', 'pally', ['classes/paladin/']),
    ('fr', 'warrior', ['classes/warrior/']), ('fr', 'rogue', ['classes/rogue/']), ('es', 'warlock', ['classes/warlock/']),
    ('es', 'rogue', ['classes/rogue/']), ('pt', 'priest', ['classes/priest/']), ('it', 'warlock', ['classes/warlock/']),
    ('pl', 'mage', ['classes/mage/']), ('pl', 'night elf', ['races/night-elf/']), ('de', 'маг', ['classes/mage/']),
    # вопросы новичка
    ('ru', 'какой класс выбрать', CLASS), ('ru', 'лучший класс для новичка', CLASS), ('ru', 'за кого играть', CLASS),
    ('ru', 'когда старт', START), ('ru', 'когда выйдет', START), ('ru', 'дата выхода', START),
    ('ru', 'есть ли русский язык', ['guides/faq/#language', 'guides/faq/#servers']), ('ru', 'лучшая раса для мага', ['guides/best-race/']),
    ('ru', 'подземелья 20 уровень', ['guides/dungeons/']), ('ru', 'сколько стоит', PRICE), ('ru', 'цена', PRICE),
    ('ru', 'как быстро качаться', ['guides/leveling/']), ('ru', 'когда рейды', ['guides/faq/#raids']),
    ('ru', 'какой максимальный уровень', ['guides/faq/#levels']),
    ('en', 'which class to choose', CLASS), ('en', 'best class for beginners', CLASS), ('en', 'what class should i play', CLASS),
    ('en', 'when does it start', START), ('en', 'release date', START), ('en', 'russian language', ['guides/faq/#servers']),
    ('en', 'best race for mage', ['guides/best-race/']), ('en', 'how much does it cost', PRICE),
    ('en', 'system requirements', ['guides/requirements/', 'guides/faq/#requirements']), ('en', 'how to level fast', ['guides/leveling/']),
    ('uk', 'який клас обрати', CLASS), ('uk', 'коли старт', START), ('uk', 'українська мова', ['guides/ukrainian/', 'guides/faq/#language']),
    ('uk', 'найкраща раса', ['guides/best-race/']),
    ('de', 'welche klasse soll ich spielen', CLASS), ('de', 'wann ist release', START), ('de', 'beste rasse', ['guides/best-race/']),
    ('de', 'was kostet', PRICE),
    ('fr', 'quelle classe choisir', CLASS), ('fr', 'date de sortie', START), ('fr', 'meilleure race', ['guides/best-race/']),
    ('es', 'que clase elegir', CLASS), ('es', 'fecha de lanzamiento', START), ('es', 'mejor raza', ['guides/best-race/']),
    ('pt', 'qual classe escolher', CLASS), ('pt', 'data de lançamento', START),
    ('it', 'quale classe scegliere', CLASS), ('it', 'data di uscita', START),
    ('pl', 'jaką klasę wybrać', CLASS), ('pl', 'data premiery', START),
]
# отложенный набор: написан после настройки словарей и под него не подгонялся; плюс то, что работало и до правок
RAID = ['guides/dungeons/', 'guides/faq/#raids']
SKY = ['races/skyborne-alliance/', 'races/skyborne-horde/', 'guides/faq/#skyborne']
HOLD = [
    ('ru', 'жрец', ['classes/priest/']), ('ru', 'паладин танк', ['classes/paladin/']), ('ru', 'варлак', ['classes/warlock/']),
    ('ru', 'охотнек', ['classes/hunter/']), ('ru', 'shadowfang keep', ['guides/dungeons/']), ('ru', 'крепость темного клыка', ['guides/dungeons/']),
    ('ru', 'рейд', RAID), ('ru', 'аддоны', ['guides/addons/']), ('ru', 'тир лист', ['guides/tier-list/']),
    ('ru', 'русский язык', ['guides/faq/#language']), ('ru', 'скайборн', SKY), ('ru', 'skyborne', SKY), ('ru', 'hunter', ['classes/hunter/']),
    ('ru', 'undead', ['races/undead/']), ('ru', 'gnome', ['races/gnome/']), ('ru', 'нужна ли подписка', ['guides/faq/#subscription']),
    ('ru', 'как занять имя', ['guides/faq/#reserve']), ('ru', 'требования к пк', ['guides/requirements/', 'guides/faq/#requirements']),
    ('ru', 'когда откроются рейды', ['guides/faq/#raids']), ('ru', 'палладин', ['classes/paladin/']), ('ru', 'прокачка мага', ['guides/leveling-mage/']),
    ('ru', 'билд воина', ['guides/builds-warrior/']), ('ru', 'билды паладина', ['guides/builds-paladin/']), ('ru', 'профессии', ['guides/professions/']),
    ('ru', 'цена', PRICE), ('ru', 'какой класс выбрать', CLASS),
    ('en', 'priest', ['classes/priest/']), ('en', 'paladin tank', ['classes/paladin/']), ('en', 'huntr', ['classes/hunter/']),
    ('en', 'druide', ['classes/druid/']), ('en', 'mage leveling', ['guides/leveling-mage/']), ('en', 'warrior build', ['guides/builds-warrior/']),
    ('en', 'addons', ['guides/addons/']), ('en', 'raid', RAID), ('en', 'subscription', ['guides/faq/#subscription']),
    ('en', 'free trial', ['guides/faq/#trial']), ('en', 'жрец', ['classes/priest/']), ('en', 'orc', ['races/orc/']),
    ('en', 'undaed', ['races/undead/']), ('en', 'deadmines', ['guides/dungeons/']), ('en', 'skyborne', SKY),
    ('en', 'reserve name', ['guides/faq/#reserve']), ('en', 'tier list', ['guides/tier-list/']), ('en', 'professions', ['guides/professions/']),
    ('en', 'price', PRICE),
    ('uk', 'мисливець', ['classes/hunter/']), ('uk', 'охотник', ['classes/hunter/']), ('uk', 'розбійнік', ['classes/rogue/']),
    ('uk', 'прокачування', ['guides/leveling/']), ('uk', 'рейди', RAID),
    ('de', 'jäger', ['classes/hunter/']), ('de', 'jager', ['classes/hunter/']), ('de', 'schurke', ['classes/rogue/']),
    ('de', 'hunter', ['classes/hunter/']), ('de', 'krieger leveln', ['guides/leveling-warrior/']), ('de', 'magier', ['classes/mage/']),
    ('de', 'priest', ['classes/priest/']), ('de', 'nachtelf', ['races/night-elf/']), ('de', 'night elf', ['races/night-elf/']),
    ('de', 'untoter', ['races/undead/']),
    ('fr', 'voleur', ['classes/rogue/']), ('fr', 'priest', ['classes/priest/']), ('fr', 'demoniste', ['classes/warlock/']),
    ('fr', 'warlock', ['classes/warlock/']), ('fr', 'elfe de la nuit', ['races/night-elf/']),
    ('es', 'picaro', ['classes/rogue/']), ('es', 'warrior', ['classes/warrior/']), ('es', 'chaman', ['classes/shaman/']),
    ('es', 'brujo', ['classes/warlock/']), ('es', 'sacerdote', ['classes/priest/']),
    ('pt', 'ladino', ['classes/rogue/']), ('pt', 'warrior', ['classes/warrior/']), ('pt', 'bruxo', ['classes/warlock/']), ('pt', 'xama', ['classes/shaman/']),
    ('it', 'ladro', ['classes/rogue/']), ('it', 'rogue', ['classes/rogue/']), ('it', 'sciamano', ['classes/shaman/']),
    ('it', 'warrior', ['classes/warrior/']), ('it', 'sacerdote', ['classes/priest/']),
    ('pl', 'kapłan', ['classes/priest/']), ('pl', 'łowca', ['classes/hunter/']), ('pl', 'czarnoksiężnik', ['classes/warlock/']),
    ('pl', 'warrior', ['classes/warrior/']), ('pl', 'krasnolud', ['races/dwarf/']),
]
KNOWN = set()   # запросы, которые пока не находят нужное: [(lang, query)]


def ok(url, lang, want):
    pre = '' if lang == 'ru' else lang + '/'
    rel = url[len(pre):] if url.startswith(pre) else url
    page, _, anchor = rel.partition('#')
    for w in want:
        wp, _, wa = w.partition('#')
        if page == wp and (not wa or anchor == wa):
            return True
    return False


def run(js=os.path.join(ROOT, 'assets', 'search', 'search.js'), index=os.path.join(ROOT, 'assets', 'search')):
    node = shutil.which('node')
    if not node:
        print('SKIP: нет node')
        sys.exit(0)
    r = subprocess.run([node, os.path.join(ROOT, 'tests', 'search_eval.js'), js, index],
                       input=json.dumps([[l, q] for l, q, _ in Q + HOLD]), capture_output=True, text=True, encoding='utf-8', check=True)
    return json.loads(r.stdout)


if __name__ == '__main__':
    res = run(*[a for a in sys.argv[1:] if not a.startswith('-')])   # [search.js [index dir]]: another engine, e.g. the old one
    good, bad, first = [], [], 0
    for i, ((lang, q, want), urls) in enumerate(zip(Q + HOLD, res)):
        (good if any(ok(u, lang, want) for u in urls[:3]) else bad).append((lang, q, urls[:3], i < len(Q)))
        first += bool(urls) and ok(urls[0], lang, want)
    if '-v' in sys.argv:
        for x in good:
            print('+', *x[:3])
    for x in bad:
        print('-', *x[:3])
    new = [b for b in bad if b[:2] not in KNOWN]
    main = sum(g[3] for g in good)
    print(f'набор {main}/{len(Q)}, отложенный {len(good) - main}/{len(HOLD)}, всего {len(good)}/{len(Q) + len(HOLD)} '
          f'({100 * len(good) // (len(Q) + len(HOLD))}%), первым {first}')
    assert not new, f'не нашлось: {len(new)}'
