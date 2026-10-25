"""Поиск по сайту (Ctrl+K): индекс на каждый язык -> assets/search/<lang>.json. build.py зовёт search.main() после seo.py.
Читает уже собранные страницы:
  * страница — заголовок h1, раздел из хлебных крошек, title и description для совпадений;
  * разделы <section id> с h2 — ссылка с якорем, текст раздела для совпадений и выдержки;
  * вопросы FAQ <details id>; подземелья из DUNGEONS (на en/uk/pl англ. названия, на ru и de/fr/es/pt/it официальные + английское).
Запись индекса: [заголовок, где (страница/раздел), путь от корня гида, вид 0 страница/1 раздел/2 вопрос/3 подземелье, ключи, текст
(строка на блок: абзац, пункт, карточка; выдержка в поиске берётся из одной строки-предложения)];
«где» тоже ищется наравне с ключами: «паладин танк» находит разделы страницы паладина.
Затем ставит ?v=<хэш> скриптам поиска во всех страницах: Cloudflare держит /wow/assets/ 30 дней, новый адрес обходит кэш.
Запуск: python search.py"""
import hashlib, json, os, re, sys, unicodedata
from html import unescape

import build
from build import LANGS, page_dir
import seo

HERE = build.HERE
OUT = os.path.join(HERE, 'assets', 'search')
SKIP = {'top', 'more', 'others'}          # шапка страницы и плитки «Другие …» — не разделы
TEXT_MAX = 1500                            # хватает на совпадения и выдержку, индекс языка ~150 КБ


BLOCK = re.compile(r'<br\b[^>]*>|</?(?:p|li|ul|ol|h[1-6]|div|dl|dt|dd|tr|td|th|table|section|header|footer|nav|figure|figcaption|summary|details|article|aside|blockquote)\b[^>]*>')


def text(html, lines=False):
    """Plain text of a fragment. lines=True: one line per block (paragraph, list item, card), so that the excerpt in the
    search dialog is a whole sentence, not card labels run together ("Урон Огонь Урон Лёд")."""
    html = re.sub(r'<(script|style|svg|template)\b.*?</\1>|<span class="src">.*?</span>', ' ', html, flags=re.S)
    if lines:
        html = BLOCK.sub('\n', html)
    s = unescape(re.sub(r'<[^>]+>', ' ', html)).replace('\xad', '')
    if not lines:
        return re.sub(r'\s+', ' ', s).strip()
    return '\n'.join(filter(None, (re.sub(r'[^\S\n]+', ' ', x).strip() for x in s.split('\n'))))


def page_entries(html, path, lang, crumb):
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.S)
    title = text(h1[1]) if h1 else crumb
    meta = re.search(r'<title>(.*?)</title>', html)[1] + ' ' + re.search(r'<meta name="description" content="([^"]*)"', html)[1]
    url = page_dir(lang, path)
    top = re.search(r'<section\b[^>]*\sid="top"[^>]*>(.*?)</section>', html, re.S)   # шапка: подзаголовок, роли, факты
    out = [[title, crumb, url, 0, unescape(meta), text(top[1], True)[:TEXT_MAX] if top else '']]
    for m in re.finditer(r'<section\b[^>]*\sid="([^"]+)"[^>]*>(.*?)</section>', html, re.S):
        sid, body = m[1], m[2]
        h2 = re.search(r'<h2[^>]*>(.*?)</h2>', body, re.S)
        if sid in SKIP or not h2:
            continue
        rest = body[h2.end():]
        out.append([text(h2[1]), title, f'{url}#{sid}', 1, '', text(re.sub(r'<details\b.*?</details>', ' ', rest, flags=re.S), True)[:TEXT_MAX]])
    for m in re.finditer(r'<details id="([^"]+)"><summary>(.*?)</summary>(.*?)</details>', html, re.S):
        out.append([text(m[2]), title, f'{url}#{m[1]}', 2, '', text(m[3], True)[:TEXT_MAX]])
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


def index(lang, meta):
    items = []
    for path in (p for p in meta if lang in meta[p]):
        html = open(os.path.join(HERE, page_dir(lang, path), 'index.html'), encoding='utf-8').read()
        cr = seo.crumbs(path, lang)
        items += page_entries(html, path, lang, cr[-2][0] if cr else '')
    dg = next(i for i in items if i[3] == 0 and i[2] == page_dir(lang, 'guides/dungeons/'))
    for name, en, lv, zone in dungeons(lang):
        keys = ' '.join(filter(None, [en if en != name else '', ru_alias(en) if lang in ('ru', 'uk') else '']))
        if re.search("['’]", name + keys):   # Zul'Farrak -> ZulFarrak: the query without the apostrophe finds it too
            keys = f'{keys} {re.sub("['’]", "", f"{name} {keys}")}'.strip()
        items.append([name, f'{dg[0]} · {lv} · {zone}', dg[2] + '#list', 3, keys, ''])
    return items


# Словари поиска. Ключи и фразы пишутся как люди печатают; engine.js сам приводит их к нижнему регистру без диакритики.
PROFESSIONS = {'Alchemy', 'Blacksmithing', 'Enchanting', 'Engineering', 'Herbalism', 'Leatherworking', 'Mining', 'Skinning',
               'Tailoring', 'Cooking', 'First Aid', 'Fishing'}
RAIDS = {'Molten Core': {'ru': 'Огненные Недра', 'de': 'Geschmolzener Kern', 'fr': 'Cœur du Magma', 'es': 'Núcleo de Magma',
                         'pt': 'Núcleo Derretido', 'it': 'Nucleo Fuso'},
         'Onyxia’s Lair': {'ru': 'Логово Ониксии', 'de': 'Onyxias Hort', 'fr': 'Repaire d’Onyxia', 'es': 'Guarida de Onyxia',
                           'pt': 'Covil da Onyxia', 'it': 'Antro di Onyxia'}}
# сокращения подземелий и рейдов — одни на всех языках; значение — английское название (names.json переводит)
ABBR = {'rfc': 'Ragefire Chasm', 'dm': 'The Deadmines', 'vc': 'The Deadmines', 'wc': 'Wailing Caverns', 'sfk': 'Shadowfang Keep',
        'bfd': 'Blackfathom Deeps', 'stocks': 'The Stockade', 'gnomer': 'Gnomeregan', 'rfk': 'Razorfen Kraul', 'rfd': 'Razorfen Downs',
        'sm': 'Scarlet Monastery', 'ulda': 'Uldaman', 'zf': "Zul'Farrak", 'mara': 'Maraudon', 'st': "Temple of Atal'Hakkar",
        'brd': 'Blackrock Depths', 'lbrs': 'Lower Blackrock Spire', 'ubrs': 'Upper Blackrock Spire', 'strat': 'Stratholme',
        'scholo': 'Scholomance', 'mc': 'Molten Core', 'ony': 'Onyxia’s Lair', 'рфк': 'Ragefire Chasm', 'мк': 'Molten Core',
        'брд': 'Blackrock Depths', 'стратх': 'Stratholme', 'шоло': 'Scholomance',
        'pally': 'Paladin', 'pala': 'Paladin', 'lock': 'Warlock', 'warr': 'Warrior', 'sham': 'Shaman', 'shammy': 'Shaman',
        'hunt': 'Hunter', 'nelf': 'Night Elf', 'paly': 'Paladin'}
# сленг и слова игроков -> слово на страницах этого языка
SLANG = {
    'ru': {'хил': 'лекарь', 'хилл': 'лекарь', 'хилер': 'лекарь', 'хиллер': 'лекарь', 'лекарь': 'лекарь', 'дд': 'урон', 'дпс': 'урон',
           'рога': 'разбойник', 'рогу': 'разбойник', 'лок': 'чернокнижник', 'варлок': 'чернокнижник', 'прист': 'жрец', 'хант': 'охотник',
           'хантер': 'охотник', 'шам': 'шаман', 'вар': 'воин', 'вара': 'воин', 'пал': 'паладин', 'пала': 'паладин', 'паля': 'паладин',
           'дру': 'друид', 'мейдж': 'маг', 'данж': 'подземелья', 'данжи': 'подземелья', 'данжей': 'подземелья', 'инст': 'подземелья',
           'инсты': 'подземелья', 'подземка': 'подземелья', 'профы': 'профессии', 'профа': 'профессии', 'тирлист': 'тир-лист',
           'тир лист': 'тир-лист', 'лвл': 'уровень', 'кач': 'прокачка', 'качаться': 'прокачка', 'голда': 'золото', 'голд': 'золото',
           'аддон': 'аддоны', 'ночник': 'ночной эльф', 'вор': 'разбойник', 'шп': 'жрец', 'качать': 'прокачка', 'нежить': 'нежить',
           'андед': 'нежить', 'хуман': 'человек', 'люди': 'человек', 'skyborne': 'скайборн'},
    'uk': {'хіл': 'цілитель', 'хілер': 'цілитель', 'лікар': 'цілитель', 'дд': 'шкода', 'дпс': 'шкода', 'рога': 'розбійник',
           'лок': 'чорнокнижник', 'варлок': 'чорнокнижник', 'прист': 'жрець', 'хант': 'мисливець', 'шам': 'шаман', 'вар': 'воїн',
           'пал': 'паладин', 'пала': 'паладин', 'дру': 'друїд', 'данж': 'підземелля', 'данжі': 'підземелля', 'інст': 'підземелля',
           'профи': 'професії', 'тірліст': 'тір-лист', 'тирлист': 'тір-лист', 'лвл': 'рівень', 'кач': 'прокачування',
           'голда': 'золото', 'андед': 'нежить', 'вор': 'розбійник', 'шп': 'жрець', 'качати': 'прокачування', 'люди': 'людина', 'skyborne': 'скайборн'},
    'en': {'pally': 'paladin', 'pal': 'paladin', 'pala': 'paladin', 'lock': 'warlock', 'wl': 'warlock', 'sham': 'shaman',
           'shammy': 'shaman', 'hunt': 'hunter', 'warr': 'warrior', 'heals': 'healer', 'healing': 'healer', 'dps': 'damage',
           'instance': 'dungeons', 'instances': 'dungeons', 'profs': 'professions', 'prof': 'professions', 'tierlist': 'tier list',
           'lvl': 'level', 'levelling': 'leveling', 'ui': 'interface', 'ne': 'night elf', 'ud': 'undead', 'nelf': 'night elf'},
    'de': {'pala': 'paladin', 'pally': 'paladin', 'hexer': 'hexenmeister', 'wl': 'hexenmeister', 'lock': 'hexenmeister',
           'schami': 'schamane', 'dudu': 'druide', 'heal': 'heiler', 'healer': 'heiler', 'dd': 'schaden', 'dps': 'schaden',
           'tierlist': 'tierliste', 'tier list': 'tierliste', 'instanz': 'dungeons', 'instanzen': 'dungeons', 'lvl': 'level',
           'leveling': 'leveln', 'rasse': 'volk', 'rassen': 'völker', 'beruf': 'berufe', 'ui': 'interface', 'untote': 'untoter'},
    'fr': {'demo': 'démoniste', 'lock': 'démoniste', 'war': 'guerrier', 'pal': 'paladin', 'pala': 'paladin', 'heal': 'soigneur',
           'healer': 'soigneur', 'heals': 'soigneur', 'dps': 'dégâts', 'rogue': 'voleur', 'instance': 'donjons',
           'instances': 'donjons', 'tierlist': 'tier list', 'lvl': 'niveau', 'leveling': 'progression', 'metier': 'métiers',
           'mv': 'mort-vivant'},
    'es': {'pala': 'paladín', 'lock': 'brujo', 'chami': 'chamán', 'heal': 'sanador', 'healer': 'sanador', 'curandero': 'sanador',
           'dps': 'daño', 'rogue': 'pícaro', 'picaro': 'pícaro', 'tanque': 'tanque', 'instancia': 'mazmorras', 'instancias': 'mazmorras',
           'banda': 'bandas', 'raid': 'bandas', 'tierlist': 'tier list', 'lvl': 'nivel', 'leveo': 'subir de nivel', 'profesion': 'profesiones'},
    'pt': {'pala': 'paladino', 'lock': 'bruxo', 'heal': 'curador', 'healer': 'curador', 'curandeiro': 'curador', 'dps': 'dano',
           'rogue': 'ladino', 'instancia': 'masmorras', 'dungeon': 'masmorras', 'raid': 'raides', 'tierlist': 'tier list',
           'lvl': 'nível', 'upar': 'evolução', 'leveling': 'evolução', 'profissao': 'profissões'},
    'it': {'pala': 'paladino', 'lock': 'stregone', 'heal': 'guaritore', 'healer': 'guaritore', 'tank': 'difensore', 'dps': 'assaltatore',
           'rogue': 'ladro', 'dungeon': 'spedizioni', 'istanza': 'spedizioni', 'raid': 'incursioni', 'tierlist': 'tier list',
           'lvl': 'livello', 'leveling': 'livellamento', 'livellare': 'livellamento', 'professione': 'professioni'},
    'pl': {'wojownik': 'warrior', 'paladyn': 'paladin', 'łowca': 'hunter', 'lowca': 'hunter', 'łotr': 'rogue', 'lotr': 'rogue',
           'łotrzyk': 'rogue', 'lotrzyk': 'rogue', 'kapłan': 'priest', 'kaplan': 'priest', 'szaman': 'shaman', 'czarnoksiężnik': 'warlock',
           'czarnoksieznik': 'warlock', 'druid': 'druid', 'człowiek': 'human', 'czlowiek': 'human', 'krasnolud': 'dwarf',
           'nocny elf': 'night elf', 'gnom': 'gnome', 'ork': 'orc', 'nieumarły': 'undead', 'nieumarly': 'undead', 'pally': 'paladin',
           'lock': 'warlock', 'heal': 'healer', 'uzdrowiciel': 'healer', 'lochy': 'dungeony', 'instancja': 'dungeony',
           'tierlist': 'tier lista', 'lvl': 'poziom', 'expienie': 'levelowanie', 'zawód': 'profesje', 'zawody': 'profesje'},
}
# служебные слова: не обязаны совпадать (вопрос «какой класс выбрать» ищет «класс выбрать»)
STOP = {
    'ru': 'и в во на с со для по о об от до за из к у как какой какая какое какие каким какую ли есть не что такое такой такая это мне я а но же бы или где когда кто кем чем сколько можно нужно нужен нужна стоит лучше',
    'uk': 'і й та в у на з із зі для по про від до за як який яка яке які яким яку чи є не що це таке такий така мені я а але де коли хто ким чим скільки можна треба',
    'en': 'a an the of for to in on and or is are be do does did i my me we you it its what which who when where how should can there with vs',
    'de': 'der die das den dem des ein eine einen und oder ist sind für mit von zu im in am an auf ich du wie was welche welcher welches wann wo gibt es soll kann',
    'fr': 'le la les l un une des de du d et ou est sont pour avec en au aux dans je tu quel quelle quels quelles quand comment que qui',
    'es': 'el la los las un una de del y o es son para con en al que qué cual cuál cuando cuándo como cómo donde dónde hay a',
    'pt': 'o a os as um uma de do da dos das e ou é são para com em no na que qual quando como onde tem há',
    'it': 'il lo la i gli le un una di del della e o è sono per con in nel che quale quando come dove c',
    'pl': 'i w we na z ze do dla o od po jak jaki jaka jakie jaką czy jest są co to kiedy gdzie ile',
}
# название игры и «список» — шум на всех языках: «когда релиз вов форевер» спрашивает о релизе, «dungeon list» — о подземельях
GAME = 'wow forever world warcraft вов форевер ворлд варкрафт'
LIST = {'ru': 'список', 'uk': 'список', 'en': 'list', 'de': 'liste', 'fr': 'liste', 'es': 'lista', 'pt': 'lista', 'it': 'elenco lista', 'pl': 'lista'}
STOP = {lang: f'{words} {GAME} {LIST[lang]}' for lang, words in STOP.items()}
# вопросы новичка -> ответ: фраза срабатывает, когда каждое её слово — начало слова запроса
ASK = {
    'ru': [('classes/', ['какой класс', 'каким классом', 'кем играть', 'за кого играть', 'лучший класс', 'класс для новичк', 'выбрать класс', 'выбор класса']),
           ('guides/faq/#raids', ['когда рейд', 'когда откроют рейд']),
           ('guides/faq/#release', ['когда старт', 'когда выйд', 'когда выход', 'когда релиз', 'когда запуск', 'дата выход', 'дата релиз', 'дата старт', 'релиз']),
           ('guides/faq/#trial', ['бесплатн']),
           ('guides/faq/#price', ['сколько стои', 'цена', 'цены', 'стоимост', 'платн']),
           ('guides/best-race/', ['лучшая раса', 'лучшую расу', 'какую расу', 'какая раса', 'раса для']),
           ('guides/leveling/', ['как качат', 'как прокач', 'быстро кач', 'быстро прокач']),
           ('guides/faq/#levels', ['максимальн уров', 'макс уров', 'до какого уровня', 'какой уровень']),
           ('guides/faq/#language', ['русский язык', 'на русском', 'русск локализ', 'русификац', 'есть ли русск']),
           ('guides/faq/#servers', ['русские сервер', 'русский сервер']),
           ('guides/requirements/', ['требовани', 'пойдет ли', 'потянет'])],
    'uk': [('classes/', ['який клас', 'яким класом', 'ким грати', 'кращий клас', 'найкращий клас', 'клас для новачк', 'обрати клас', 'вибрати клас']),
           ('guides/faq/#raids', ['коли рейд']),
           ('guides/faq/#release', ['коли старт', 'коли вийд', 'коли вихід', 'коли реліз', 'дата виход', 'реліз']),
           ('guides/faq/#trial', ['безкоштовн']),
           ('guides/faq/#price', ['скільки кошт', 'ціна', 'ціни', 'вартіст']),
           ('guides/best-race/', ['найкраща раса', 'краща раса', 'яку расу', 'яка раса', 'раса для']),
           ('guides/leveling/', ['як качат', 'як прокач', 'швидко кач']),
           ('guides/faq/#levels', ['максимальн рів', 'який рівень']),
           ('guides/ukrainian/', ['українськ', 'локалізац', 'переклад гри']),
           ('guides/requirements/', ['вимоги'])],
    'en': [('classes/', ['which class', 'what class', 'best class', 'class for beginn', 'choose class', 'class to play', 'who to play']),
           ('guides/faq/#raids', ['when raid']),
           ('guides/faq/#release', ['release', 'launch', 'when start', 'start date', 'when come out', 'when out']),
           ('guides/faq/#trial', ['free']),
           ('guides/faq/#price', ['how much', 'price', 'cost']),
           ('guides/best-race/', ['best race', 'which race', 'what race', 'race for']),
           ('guides/leveling/', ['how level', 'level fast', 'leveling guide']),
           ('guides/faq/#levels', ['level cap', 'max level']),
           ('guides/faq/#servers', ['russian', 'language']),
           ('guides/requirements/', ['requirement', 'can i run'])],
    'de': [('classes/', ['welche klasse', 'beste klasse', 'klasse anfang', 'klasse wahl', 'was spielen', 'wen spielen']),
           ('guides/faq/#raids', ['wann raid']),
           ('guides/faq/#release', ['release', 'erscheinung', 'wann start', 'wann erschein', 'wann kommt', 'starttermin', 'launch']),
           ('guides/faq/#trial', ['kostenlos', 'gratis']),
           ('guides/faq/#price', ['was kostet', 'kosten', 'preis', 'abo']),
           ('guides/best-race/', ['bestes volk', 'beste rasse', 'welches volk', 'welche rasse']),
           ('guides/leveling/', ['wie level', 'schnell level']),
           ('guides/faq/#levels', ['maximal level', 'max level', 'levelcap']),
           ('guides/faq/#servers', ['deutsch', 'sprache']),
           ('guides/requirements/', ['anforderung'])],
    'fr': [('classes/', ['quelle classe', 'meilleure classe', 'classe debut', 'choisir classe', 'que jouer']),
           ('guides/faq/#raids', ['quand raid']),
           ('guides/faq/#release', ['date sortie', 'sortie', 'quand sort', 'quand commence', 'lancement']),
           ('guides/faq/#trial', ['gratuit']),
           ('guides/faq/#price', ['prix', 'combien coute', 'cout']),
           ('guides/best-race/', ['meilleure race', 'quelle race']),
           ('guides/leveling/', ['monter niveau', 'comment level']),
           ('guides/faq/#levels', ['niveau max']),
           ('guides/faq/#servers', ['francais', 'langue']),
           ('guides/requirements/', ['configuration', 'requise'])],
    'es': [('classes/', ['que clase', 'cual clase', 'mejor clase', 'clase princip', 'elegir clase', 'quien jugar']),
           ('guides/faq/#raids', ['cuando banda', 'cuando raid']),
           ('guides/faq/#release', ['fecha lanzamiento', 'fecha salida', 'cuando sale', 'cuando empieza', 'lanzamiento']),
           ('guides/faq/#trial', ['gratis']),
           ('guides/faq/#price', ['precio', 'cuanto cuesta', 'cuesta']),
           ('guides/best-race/', ['mejor raza', 'que raza', 'cual raza']),
           ('guides/leveling/', ['como subir', 'subir rapido']),
           ('guides/faq/#levels', ['nivel max']),
           ('guides/faq/#servers', ['espanol', 'idioma']),
           ('guides/requirements/', ['requisito'])],
    'pt': [('classes/', ['qual classe', 'melhor classe', 'classe inic', 'escolher classe', 'quem jogar']),
           ('guides/faq/#raids', ['quando raide', 'quando raid']),
           ('guides/faq/#release', ['data lancamento', 'quando lanca', 'quando sai', 'quando comeca', 'lancamento']),
           ('guides/faq/#trial', ['gratis', 'gratuito']),
           ('guides/faq/#price', ['preco', 'quanto custa', 'custa']),
           ('guides/best-race/', ['melhor raca', 'qual raca']),
           ('guides/leveling/', ['como upar', 'upar rapido']),
           ('guides/faq/#levels', ['nivel max']),
           ('guides/faq/#servers', ['portugues', 'idioma']),
           ('guides/requirements/', ['requisito'])],
    'it': [('classes/', ['quale classe', 'migliore classe', 'classe migliore', 'classe princip', 'scegliere classe', 'chi giocare']),
           ('guides/faq/#raids', ['quando incursion', 'quando raid']),
           ('guides/faq/#release', ['data uscita', 'quando esce', 'quando inizia', 'uscita', 'lancio']),
           ('guides/faq/#trial', ['gratis', 'gratuito']),
           ('guides/faq/#price', ['prezzo', 'quanto costa', 'costa']),
           ('guides/best-race/', ['razza migliore', 'migliore razza', 'quale razza']),
           ('guides/leveling/', ['come livell']),
           ('guides/faq/#levels', ['livello max']),
           ('guides/faq/#servers', ['italiano', 'lingua']),
           ('guides/requirements/', ['requisiti'])],
    'pl': [('classes/', ['jaka klase', 'jaka klasa', 'najlepsza klasa', 'klasa dla poczatk', 'wybrac klase', 'kim grac']),
           ('guides/faq/#raids', ['kiedy raid']),
           ('guides/faq/#release', ['data premiery', 'premiera', 'kiedy start', 'kiedy wychodzi', 'kiedy premier']),
           ('guides/faq/#trial', ['darmow', 'za darmo']),
           ('guides/faq/#price', ['cena', 'ile kosztuje', 'koszt']),
           ('guides/best-race/', ['najlepsza rasa', 'jaka rase', 'jaka rasa']),
           ('guides/leveling/', ['jak levelowac', 'jak expic']),
           ('guides/faq/#levels', ['maksymaln poziom', 'max poziom']),
           ('guides/faq/#servers', ['polsk', 'jezyk']),
           ('guides/requirements/', ['wymagania'])],
}
# пустой поиск и «ничего не нашлось»: шесть частых вопросов, один порядок на всех языках —
# класс, старт, раса, прокачка, цена, язык (ru и uk — язык клиента, остальные — серверы и языки)
TOP_URLS = ['classes/', 'guides/faq/#release', 'guides/best-race/', 'guides/leveling/', 'guides/faq/#editions']
TOP = {lang: list(zip(t, TOP_URLS + [u])) for lang, (t, u) in {
    'ru': (['Какой класс выбрать', 'Когда старт', 'Лучшая раса', 'Прокачка 1–60', 'Цена и подписка', 'Русский язык'], 'guides/faq/#language'),
    'uk': (['Який клас обрати', 'Коли старт', 'Найкраща раса', 'Прокачування 1–60', 'Ціна й підписка', 'Українська мова'], 'guides/ukrainian/'),
    'en': (['Which class to play', 'Release date', 'Best race', 'Leveling 1–60', 'Price and subscription', 'Servers and languages'], 'guides/faq/#servers'),
    'de': (['Welche Klasse spielen', 'Release-Termin', 'Bestes Volk', 'Leveln 1–60', 'Preis und Abo', 'Server und Sprachen'], 'guides/faq/#servers'),
    'fr': (['Quelle classe jouer', 'Date de sortie', 'Meilleure race', 'Progression 1–60', 'Prix et abonnement', 'Serveurs et langues'], 'guides/faq/#servers'),
    'es': (['Qué clase elegir', 'Fecha de lanzamiento', 'Mejor raza', 'Subir de nivel 1–60', 'Precio y suscripción', 'Servidores e idiomas'], 'guides/faq/#servers'),
    'pt': (['Qual classe jogar', 'Data de lançamento', 'Melhor raça', 'Evolução 1–60', 'Preço e assinatura', 'Servidores e idiomas'], 'guides/faq/#servers'),
    'it': (['Quale classe scegliere', 'Data di uscita', 'Razza migliore', 'Livellamento 1–60', 'Prezzo e abbonamento', 'Server e lingue'], 'guides/faq/#servers'),
    'pl': (['Jaką klasę wybrać', 'Data premiery', 'Najlepsza rasa', 'Levelowanie 1–60', 'Cena i subskrypcja', 'Serwery i języki'], 'guides/faq/#servers'),
}.items()}


def norm(s):
    """The same as norm() in engine.js: lower case without accents, ё -> е, ї -> і."""
    o = ''
    for ch in s.lower():
        c = unicodedata.normalize('NFD', ch)[0]
        o += {'ё': 'е', 'ї': 'і'}.get(c, c)
    return o


WORDS = re.compile(r'[^\s\-–—.,:;!?()«»"“”„\'’/·]+')


def aliases(lang, idx):
    """Other names a reader may type -> the name on this language's pages: the English game names of classes, races, specs,
    zones, professions and raids (names.json; Russian ones too on ru/en/uk), class and race names of every language (page
    titles), abbreviations (ABBR) and slang (SLANG). Only names whose every word is on the pages of the language get in:
    an alias that finds nothing only weighs the index."""
    vocab = {w for it in idx[lang] for w in WORDS.findall(norm(f'{it[0]} {it[1]} {it[4]} {it[5]}'))}
    out = {}

    def add(alias, local):
        a, loc = ' '.join(WORDS.findall(norm(alias))), ' '.join(WORDS.findall(norm(local)))
        if a and loc and a != loc and all(w in vocab for w in loc.split()):
            out[a] = loc if out.get(a, loc) == loc else f'{out[a]}|{loc}'
    names = json.load(open(os.path.join(HERE, 'i18n', 'names.json'), encoding='utf-8'))
    ids = json.load(open(os.path.join(HERE, 'i18n', 'names_ids.json'), encoding='utf-8'))
    for en, tr in names.items():
        if 'manual' in ids.get(en, {}) or ids.get(en, {}).get('type') == 'zone' or en in PROFESSIONS:
            local = tr.get(lang, en) if lang not in ('en', 'uk', 'pl') else en
            for alias in (en, tr.get('ru') if lang in ('ru', 'en', 'uk') else None):   # Russian names where Russian readers are
                if alias:
                    add(alias, local)
    for en, tr in RAIDS.items():
        for alias in (en, tr.get('ru')):
            add(alias, tr.get(lang, en))
    titles = {}
    for l in LANGS:   # class and race pages: the title in every language
        p = len(page_dir(l))
        for it in idx[l]:
            if it[3] == 0 and re.fullmatch(r'(classes|races)/[\w-]+/', it[2][p:]):
                titles.setdefault(it[2][p:], {})[l] = it[0]
    for by in titles.values():
        for t in by.values():
            if lang in by:
                add(t, by[lang])
    local = {by['en']: by[lang] for by in titles.values() if 'en' in by and lang in by}   # Warrior -> Воїн on uk
    for alias, en in ABBR.items():
        add(alias, local.get(en) or (names.get(en, {}).get(lang, en) if lang not in ('en', 'uk', 'pl') else en))
    for alias, local in SLANG[lang].items():
        add(alias, local)
    return out


def main():
    meta = seo.page_meta()
    os.makedirs(OUT, exist_ok=True)
    h = hashlib.sha1()
    idx = {lang: index(lang, meta) for lang in LANGS}
    for lang in LANGS:
        urls = {it[2] for it in idx[lang]}
        ask = [[page_dir(lang, u), '|'.join(ph)] for u, ph in ASK[lang]]
        top = [[t, page_dir(lang, u)] for t, u in TOP[lang]]
        miss = [u for u, _ in ask + [x[::-1] for x in top] if u not in urls]
        assert not miss, f'search {lang}: no such entry {miss}'
        data = {'i': idx[lang], 'a': aliases(lang, idx), 'q': ask, 'p': top, 's': STOP[lang]}
        data = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
        open(os.path.join(OUT, f'{lang}.json'), 'w', encoding='utf-8', newline='\n').write(data + '\n')
        h.update(data.encode())
    for f in ('search.js', 'engine.js', 'search.css'):
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
