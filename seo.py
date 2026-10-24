"""SEO-обвязка гида: последний шаг сборки (build.py зовёт seo.main() после всех страниц).
Шаблоны и контент не трогает: правит уже собранные index.html —
  * <title>, meta description, og:title/og:description/og:image:alt под поисковые запросы (тексты ниже, на трёх языках);
  * og:locale:alternate; JSON-LD (WebSite + Organization на главной, BreadcrumbList на разделах/классах/расах/гайдах,
    Article с датой обновления на гайдах, FAQPage на FAQ); метка подтверждения Bing (VERIFY);
  * сниппет Cloudflare Web Analytics, если задан CF_BEACON_TOKEN;
и пишет sitemap.xml со всеми страницами и hreflang-альтернативами.
robots.txt живёт в корне домена — репо RaiGanja/raiganja.github.io (gabella-hub), не здесь.
Если запускаете build_tools.py или build_guides.py отдельно, потом запустите и python seo.py.
Запуск: python seo.py"""
import json, os, re, sys
from html import escape

import build
from build import CLASSES, LANGS, RACES_PAGE, SITE, page_dir, tr
import langs
from langs import HREFLANG, LOCALE
from content.guides import GUIDES, HUB, HUBS

HERE = build.HERE

# Cloudflare Web Analytics: токен сайта gabella.site (Analytics → Web analytics → gabella.site → Manage site, режим «Enable with JS Snippet installation» — DNS only, автовставки нет).
# Пусто — сниппет не вставляется.
CF_BEACON_TOKEN = 'ee1d216e690040389063e8d72384c2c7'

# Подтверждение прав в поисковиках (Яндекс не используем — решение 23.10): значение content= из метатега, который выдаёт кабинет. Пусто — метатег не вставляется.
# Та же метка — в хабе (gabella-hub, content.VERIFY): кабинеты проверяют корень домена gabella.site.
# Bing Webmaster Tools подключён импортом из Search Console и метки не требует; msvalidate.01 — запасной путь.
VERIFY = {
    'msvalidate.01': '',         # Bing Webmaster Tools → Settings → Verification → HTML Meta Tag
}

BRAND = 'Gabella'
HOME_NAME = {'ru': 'Главная', 'en': 'Home', 'uk': 'Головна'}
SITE_NAME = {'ru': 'Гид WoW Forever', 'en': 'WoW Forever Guide', 'uk': 'Гід WoW Forever'}
TOOLS_NAME = {'ru': 'Инструменты', 'en': 'Tools', 'uk': 'Інструменти'}
PRIVACY_NAME = {'ru': 'Конфиденциальность', 'en': 'Privacy', 'uk': 'Конфіденційність'}
PLAY_NAME = {'ru': 'В игре', 'en': 'In game', 'uk': 'У грі'}
ROSTER_NAME = {'ru': 'Состав', 'en': 'Roster', 'uk': 'Склад'}
PROFILE_NAME = {'ru': 'Мой профиль', 'en': 'My profile', 'uk': 'Мій профіль'}
PLAYER_NAME = {'ru': 'Игрок Gabella Team', 'en': 'Gabella Team player', 'uk': 'Гравець Gabella Team'}
GUILD_NAME = {'ru': 'Гильдия', 'en': 'Guild', 'uk': 'Гільдія'}
NOINDEX = {'profile/', 'u/', 'g/'}   # personal pages: noindex in the page (build_me.py), left out of sitemap.xml


def t(ru, en, uk):
    return {'ru': ru, 'en': en, 'uk': uk}


# ---------- titles and descriptions: by page path (site-relative, without language prefix) ----------
# Под реальные запросы, по факту содержимого страницы. Длина: title до ~65, description 120–160 символов.

META = {
    '': (t('Гид WoW Forever: классы, расы, прокачка и подземелья',
           'WoW Forever Guide: Classes, Races, Leveling and Dungeons',
           'Гід WoW Forever: класи, раси, прокачка та підземелля'),
         t('Гид по WoW Forever (ВоВ Форевер): кем играть, подборщик расы и класса, сборка группы и гайды по прокачке, подземельям и профессиям.',
           'WoW Forever guide: who to play, a race and class picker, a group builder and guides to leveling, dungeons and professions.',
           'Гід по WoW Forever (ВоВ Форевер): ким грати, підбір раси й класу, збір групи і гайди з прокачки, підземель і професій.')),
    'classes/': (t('Классы WoW Forever: какой класс выбрать, сравнение всех 9',
                   'WoW Forever Classes: Best Class to Play, All 9 Compared',
                   'Класи WoW Forever: який клас обрати, порівняння всіх 9'),
                 t('Какой класс выбрать в WoW Forever: девять классов по три специализации, роли танк/лекарь/урон, кто качается быстрее и чем каждый полезен рейду.',
                   'Which class to pick in WoW Forever: nine classes with three specs each, tank/healer/DPS roles, which level fastest and what each brings to a raid.',
                   'Який клас обрати у WoW Forever: дев’ять класів по три спеціалізації, ролі танк/лікар/шкода, хто качається швидше і чим кожен корисний рейду.')),
    'races/': (t('Расы и классы WoW Forever: все 10 рас и расовые способности',
                 'WoW Forever Races: Racials and Race/Class Combos for All 10',
                 'Раси й класи WoW Forever: усі 10 рас і расові здібності'),
               t('Пять рас за Альянс и пять за Орду, включая новых Скайборнов: какие классы доступны каждой расе и что дают её четыре расовые способности.',
                 'Five races per faction, including the new Skyborne: which classes each race can play and what its four racial abilities do.',
                 'П’ять рас за Альянс і п’ять за Орду, разом із новими Скайборнами: які класи доступні кожній расі та що дають її чотири расові здібності.')),
    'tools/': (t('Инструменты WoW Forever: сравнение классов и рас, рамки группы',
                 'WoW Forever Tools: Class and Race Compare, Party Frames',
                 'Інструменти WoW Forever: порівняння класів і рас, рамки групи'),
               t('Сравнение классов и рас WoW Forever бок о бок, рамки группы и рейдовая сетка как в игре, поиск по всему гиду.',
                 'Compare WoW Forever classes and races side by side, in-game style party frames and raid grid, and search across the whole guide.',
                 'Порівняння класів і рас WoW Forever пліч-о-пліч, рамки групи та рейдова сітка як у грі, пошук по всьому гіду.')),
    'guides/': (t('Гайды WoW Forever: прокачка, подземелья, профессии, FAQ',
                  'WoW Forever Guides: Leveling, Dungeons, Professions, FAQ',
                  'Гайди WoW Forever: прокачка, підземелля, професії, FAQ'),
                t('Все гайды по WoW Forever в одном месте: маршрут прокачки 1–60, список подземелий и рейдов, профессии под класс, ответы на вопросы и новости.',
                  'All WoW Forever guides in one place: a 1–60 leveling route, the dungeon and raid list, professions for your class, answers to common questions and news.',
                  'Усі гайди по WoW Forever (ВоВ Форевер) в одному місці: маршрут прокачки 1–60, список підземель і рейдів, професії під клас, відповіді на питання та новини.')),
    'guides/leveling/': (t('Гайд по прокачке WoW Forever 1–60: зоны по уровням',
                           'WoW Forever Leveling Guide 1–60: Zones by Level',
                           'Гайд з прокачки WoW Forever 1–60: зони за рівнями'),
                         t('Прокачка в WoW Forever с 1 до 60: маршрут по зонам за Альянс и Орду, отдых и бонусы опыта, советы соло, вдвоём и группой, Legacy и лагерь.',
                           'Level 1 to 60 in WoW Forever: a zone-by-zone route for Alliance and Horde, rested XP and experience bonuses, solo, duo and group tips, Legacy and the camp.',
                           'Прокачка у WoW Forever з 1 до 60: маршрут зонами за Альянс і Орду, відпочинок і бонуси досвіду, поради соло, удвох і групою, Legacy та табір.')),
    'guides/dungeons/': (t('Подземелья WoW Forever по уровням: все 35 и рейды',
                           'WoW Forever Dungeons by Level: All 35 Dungeons and Raids',
                           'Підземелля WoW Forever за рівнями: усі 35 і рейди'),
                         t('Все 35 подземелий WoW Forever по уровням и где вход, с фильтром под уровень вашего персонажа, три рейда с датами открытия и состав группы.',
                           'All 35 WoW Forever dungeons by level with entrance locations and a filter for your level, the three raids with opening dates, and group composition.',
                           'Усі 35 підземель WoW Forever за рівнями та де вхід, з фільтром під рівень вашого героя, три рейди з датами відкриття та склад групи.')),
    'guides/professions/': (t('Профессии WoW Forever: лучшие пары для каждого класса',
                              'WoW Forever Professions Guide: Best Pairs for Every Class',
                              'Професії WoW Forever: найкращі пари для кожного класу'),
                            t('Какие две профессии взять в WoW Forever под каждый класс, что каждая профессия ставит в лагерь и как прокачать навык до 300.',
                              'Which two professions to take in WoW Forever for each class, what every profession places in the camp, and how to raise your skill to 300.',
                              'Які дві професії взяти у WoW Forever під кожен клас, що кожна професія ставить у табір і як прокачати навичку до 300.')),
    'guides/faq/': (t('WoW Forever FAQ: дата и время выхода, цена, подписка',
                      'WoW Forever FAQ: Release Date and Time, Price, Subscription',
                      'WoW Forever FAQ: дата й час виходу, ціна, підписка'),
                    t('Когда выходит WoW Forever, нужна ли подписка, сколько стоят наборы, какие режимы игры, когда занимать имя и чем Forever отличается от Classic Era.',
                      'When WoW Forever launches, whether you need a subscription, pack prices, game modes, when to reserve a name and how Forever differs from Classic Era.',
                      'Коли виходить WoW Forever, чи потрібна підписка, скільки коштують набори, які режими гри, коли бронювати ім’я та чим Forever відрізняється від Classic Era.')),
    'guides/news/': (t('Новости WoW Forever: бета, релиз и патчи',
                       'WoW Forever News: Beta, Launch and Patches',
                       'Новини WoW Forever: бета, реліз і патчі'),
                     t('Новости WoW Forever перед релизом: закрытие беты и резерв имён с 27.10, изменения рас и классов в патчах беты, Даларан и свежая лента Wowhead.',
                       'WoW Forever news before launch: the beta closing and name reservations from 27.10, race and class changes in beta patches, Dalaran and the latest Wowhead feed.',
                       'Новини WoW Forever перед релізом: закриття бети й бронювання імен з 27.10, зміни рас і класів у патчах бети, Даларан і свіжа стрічка Wowhead.')),
    'guides/ukrainian/': ({'uk': 'WoW Forever українською: аддони UA_Forever і UALL Forever'},   # only uk
                          {'uk': 'Української мови у WoW Forever немає. Який аддон перекладу обрати, як встановити його через CurseForge чи вручну і як побачити оригінал.'}),
    'play/': (t('WoW Forever: второй экран — радио, зоны по уровню, таймеры',
                'WoW Forever Second Screen: Radio, Zones by Level, Timers',
                'WoW Forever: другий екран — радіо, зони за рівнем, таймери'),
              t('Держите открытым во время игры: фэнтези-радио, куда идти на вашем уровне за Альянс или Орду, подземелья под уровень и таймеры с сигналом.',
                'Keep it open while you play: fantasy radio, where to level next for Alliance or Horde, dungeons for your level and timers with an alert.',
                'Тримайте відкритим під час гри: фентезі-радіо, куди йти на вашому рівні за Альянс чи Орду, підземелля під рівень і таймери із сигналом.')),
    'roster/': (t('Состав Gabella Team в WoW Forever: кто кем играет',
                  'Gabella Team Roster in WoW Forever: Who Plays What',
                  'Склад Gabella Team у WoW Forever: хто ким грає'),
                t('Персонажи участников Gabella Team в WoW Forever: фракция, раса, класс, роль, профессии и время игры. Кто сейчас ищет группу и лента достижений.',
                  'Characters of Gabella Team members in WoW Forever: faction, race, class, role, professions and play time. Who is looking for a group and the achievement feed.',
                  'Персонажі учасників Gabella Team у WoW Forever: фракція, раса, клас, роль, професії та час гри. Хто зараз шукає групу і стрічка досягнень.')),
    'profile/': (t('Мой профиль — гид WoW Forever', 'My Profile — WoW Forever Guide', 'Мій профіль — гід WoW Forever'),
                 t('Персонажи, достижения, ранги и рамки портрета участника Gabella Team. Вход через Discord, Google, Battle.net, Telegram или почту.',
                   'Characters, achievements, ranks and portrait frames of a Gabella Team member. Log in with Discord, Google, Battle.net, Telegram or email.',
                   'Персонажі, досягнення, ранги й рамки портрета учасника Gabella Team. Вхід через Discord, Google, Battle.net, Telegram або пошту.')),
    'u/': (t('Игрок Gabella Team — гид WoW Forever', 'Gabella Team Player — WoW Forever Guide', 'Гравець Gabella Team — гід WoW Forever'),
           t('Карточка игрока Gabella Team: персонажи в WoW Forever, ранг, рамка и достижения.',
             'Gabella Team player card: WoW Forever characters, rank, frame and achievements.',
             'Картка гравця Gabella Team: персонажі у WoW Forever, ранг, рамка й досягнення.')),
    'g/': (t('Гильдия — гид WoW Forever', 'Guild — WoW Forever Guide', 'Гільдія — гід WoW Forever'),
           t('Страница гильдии Gabella: герб, состав и хроника.', 'Gabella guild page: crest, roster and chronicle.', 'Сторінка гільдії Gabella: герб, склад і хроніка.')),
    'privacy/': (t('Конфиденциальность — гид WoW Forever',
                   'Privacy — WoW Forever Guide',
                   'Конфіденційність — гід WoW Forever'),
                 t('Какие данные собирает гид WoW Forever от Gabella: профиль после входа, статистика без cookies, что хранится в браузере, как скачать и удалить данные.',
                   'What data the Gabella WoW Forever guide collects: the profile after sign-in, cookieless statistics, what is stored in your browser, how to download and delete your data.',
                   'Які дані збирає гід WoW Forever від Gabella: профіль після входу, статистика без cookies, що зберігається в браузері, як завантажити й видалити дані.')),
}

CLASS_T = t('{n} в WoW Forever: гайд, специализации и расы', 'WoW Forever {n} Guide: Specs, Abilities and Races', '{n} у WoW Forever: гайд, спеціалізації та раси')
CLASS_T_SHORT = t('{n} в WoW Forever: {specs}', 'WoW Forever {n}: {specs}', '{n} у WoW Forever: {specs}')   # when the full one is over 65
CLASS_D = t('{n} в WoW Forever: {specs} — ключевые способности, расы, польза в группе, плюсы, минусы и что нового.',
            'WoW Forever {n} guide: {specs} specs, key abilities, races, group value, pros and cons, and what is new.',
            '{n} у WoW Forever: {specs} — ключові здібності, раси, користь у групі, плюси, мінуси та що нового.')
RACE_T = t('{n} в WoW Forever: расовые способности и классы', 'WoW Forever {n} Racials and Classes Guide', '{n} у WoW Forever: расові здібності та класи')
RACE_D = t('{n} в WoW Forever: четыре расовые способности, доступные и лучшие классы, столица {cap}, стартовая зона {zone}.',
           'WoW Forever {n} guide: four racial abilities, available and best classes, capital {cap}, starting zone {zone}.',
           '{n} у WoW Forever: чотири расові здібності, доступні та найкращі класи, столиця {cap}, стартова зона {zone}.')
AND = {'ru': ' и ', 'en': ' and ', 'uk': ' і '}
langs.fill([HOME_NAME, SITE_NAME, TOOLS_NAME, PRIVACY_NAME, PLAY_NAME, ROSTER_NAME, PROFILE_NAME, PLAYER_NAME, GUILD_NAME, META, CLASS_T, CLASS_T_SHORT, CLASS_D, RACE_T, RACE_D, AND])   # new languages: i18n/<lang>.json


def listing(xs, lang):
    return ', '.join(xs[:-1]) + AND[lang] + xs[-1]


def page_meta():
    """path -> {lang: (title, description)} for every page of the site."""
    out = {p: {l: (ti[l], de[l]) for l in LANGS if l in ti} for p, (ti, de) in META.items()}   # one-language page: its language
    for c in CLASSES:
        out[f'classes/{c["id"]}/'] = {}
        for l in LANGS:
            n = tr(c['n'], l)
            specs = [s['en'] if l == 'en' else tr(s['n'], l) for s in c['specs']]
            sp = ', '.join(specs) if l == 'en' else listing(specs, l)
            title = CLASS_T[l].format(n=n, specs=sp)
            if len(title) > 65:
                title = CLASS_T_SHORT[l].format(n=n, specs=sp)
            out[f'classes/{c["id"]}/'][l] = (title, CLASS_D[l].format(n=n, specs=listing(specs, l)))
    names = race_names()
    for rp in RACES_PAGE:
        facts = dict(rp['facts'])
        p = f'races/{rp["slug"]}/'
        out[p] = {}
        for l in LANGS:
            n = tr(names[rp['id']], l)
            fact = lambda k: build.ru_word(build.fact_ru(k, facts[k])) if l == 'ru' else tr(facts[k], l)   # places as the ruRU client shows them
            out[p][l] = (RACE_T[l].format(n=n), RACE_D[l].format(n=n, cap=fact('Столица'), zone=fact('Стартовая зона')))
    return out


# ---------- JSON-LD ----------

_RACES = None


def race_names():
    global _RACES
    if _RACES is None:
        src = open(os.path.join(HERE, 'index.src.html'), encoding='utf-8').read()
        _RACES = {r['id']: r['n'] for r in build.parse_races(src)}
    return _RACES


def crumbs(path, lang):
    """BreadcrumbList items [(name, url)] for a page path, or None for the home page."""
    if not path:
        return None
    base = SITE + page_dir(lang)
    items = [(HOME_NAME[lang], base)]
    sec = {'classes/': HUBS[0], 'races/': HUBS[1], 'guides/': HUB}
    parts = path.strip('/').split('/')
    top = parts[0] + '/'
    names = {'tools/': TOOLS_NAME, 'privacy/': PRIVACY_NAME, 'play/': PLAY_NAME, 'roster/': ROSTER_NAME, 'profile/': PROFILE_NAME}
    if top in ('u/', 'g/'):
        items += [(ROSTER_NAME[lang], base + 'roster/'), ((PLAYER_NAME if top == 'u/' else GUILD_NAME)[lang], base + top)]
        return items
    if top in names:
        items.append((names[top][lang], base + top))
        return items
    items.append((sec[top]['title'][lang], base + top))
    if len(parts) > 1:
        if top == 'guides/':
            g = next(x for x in GUIDES if x['slug'] == parts[1])
            name = g['title'][lang]
        elif top == 'classes/':
            name = tr(next(c['n'] for c in CLASSES if c['id'] == parts[1]), lang)
        else:
            rid = next(r['id'] for r in RACES_PAGE if r['slug'] == parts[1])
            name = tr(race_names()[rid], lang)
        items.append((name, base + path))
    return items


def faq_ld(lang):
    faq = next(g for g in GUIDES if g['slug'] == 'faq')
    qs = [q for s in faq['sections'] for k, d in s['blocks'] if k == 'faq' for q in d]
    text = build.ru_plain if lang == 'ru' else str                 # ru: game names as the ruRU client shows them
    return {'@context': 'https://schema.org', '@type': 'FAQPage', 'inLanguage': HREFLANG[lang],
            'mainEntity': [{'@type': 'Question', 'name': text(q['q'][lang]),
                            'acceptedAnswer': {'@type': 'Answer', 'text': ' '.join(text(a[lang]) for a in q['a'])}} for q in qs]}


ORG = {'@type': 'Organization', 'name': BRAND, 'url': 'https://gabella.site/', 'logo': SITE + 'assets/icons/icon-512.png',
       'sameAs': [build.DISCORD]}


def guide_updated(path):
    """'2026-10-23' for a guide page with an update date (news refreshes itself and has none), else None."""
    g = next((g for g in GUIDES if path == f'guides/{g["slug"]}/' and g['slug'] != 'news'), None)
    d = g and g.get('updated')
    return '-'.join(reversed(d.split('.'))) if d else None


def json_ld(path, lang, desc, title='', image=''):
    blocks = []
    if not path:
        blocks.append({'@context': 'https://schema.org', '@type': 'WebSite', 'name': SITE_NAME[lang],
                       'alternateName': BRAND, 'url': SITE + page_dir(lang), 'inLanguage': HREFLANG[lang], 'description': desc,
                       'publisher': ORG})
        blocks.append({'@context': 'https://schema.org'} | ORG)
    else:
        items = crumbs(path, lang)
        blocks.append({'@context': 'https://schema.org', '@type': 'BreadcrumbList',
                       'itemListElement': [{'@type': 'ListItem', 'position': i, 'name': n, 'item': u}
                                           for i, (n, u) in enumerate(items, 1)]})
    updated = guide_updated(path)
    if updated:
        art = {'@context': 'https://schema.org', '@type': 'Article', 'headline': title, 'description': desc,
               'inLanguage': HREFLANG[lang], 'url': SITE + page_dir(lang, path), 'dateModified': updated,
               'author': ORG, 'publisher': ORG, 'isPartOf': {'@type': 'WebSite', 'url': SITE + page_dir(lang)}}
        if image:
            art['image'] = image
        blocks.append(art)
    if path == 'guides/faq/':
        blocks.append(faq_ld(lang))
    dump = lambda b: json.dumps(b, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    return ''.join(f'<script type="application/ld+json">{dump(b)}</script>\n' for b in blocks)


# ---------- page rewrite ----------

def set_attr(html, rx, value, path):
    new, n = re.subn(rx, lambda m: m[1] + value + m[2], html, count=1)
    assert n == 1, (path, rx)
    return new


def apply(html, path, lang, title, desc):
    a = escape(title, quote=True)
    d = escape(desc, quote=True)
    html = set_attr(html, r'(<title>).*?(</title>)', a, path)
    html = set_attr(html, r'(<meta name="description" content=")[^"]*(">)', d, path)
    html = set_attr(html, r'(<meta property="og:title" content=")[^"]*(">)', a, path)
    html = set_attr(html, r'(<meta property="og:description" content=")[^"]*(">)', d, path)
    if 'og:image:alt' in html:
        html = set_attr(html, r'(<meta property="og:image:alt" content=")[^"]*(">)', a, path)
    else:
        html = html.replace('<meta name="twitter:card"', f'<meta property="og:image:alt" content="{a}">\n<meta name="twitter:card"', 1)
    alt = ''.join(f'<meta property="og:locale:alternate" content="{LOCALE[l]}">\n' for l in LANGS if l != lang and not build.only_lang(path))
    html = re.sub(r'<meta property="og:locale:alternate"[^>]*>\n', '', html)
    html = html.replace('<meta property="og:site_name"', alt + '<meta property="og:site_name"', 1)
    html = re.sub(r'<script type="application/ld\+json">.*?</script>\n', '', html, flags=re.S)
    html = re.sub(r'<meta name="(?:%s)" content="[^"]*">\n' % '|'.join(map(re.escape, VERIFY)), '', html)
    verify = ''.join(f'<meta name="{k}" content="{escape(v, quote=True)}">\n' for k, v in VERIFY.items() if v)
    og = re.search(r'<meta property="og:image" content="([^"]+)"', html)
    html = html.replace('</head>', verify + json_ld(path, lang, desc, title, og and og[1]) + '</head>', 1)
    html = re.sub(r'<script type="module" src="https://static.cloudflareinsights.com/[^>]*></script>\n', '', html)
    if CF_BEACON_TOKEN:
        beacon = json.dumps({'token': CF_BEACON_TOKEN})
        html = html.replace('</body>', f'<script type="module" src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon=\'{beacon}\'></script>\n</body>', 1)
    return html


def sitemap(paths):
    urls = []
    for p, by_lang in paths.items():
        ls = [l for l in LANGS if l in by_lang]
        alts = ''.join(f'<xhtml:link rel="alternate" hreflang="{HREFLANG[l]}" href="{SITE}{page_dir(l, p)}"/>' for l in ls)
        alts += f'<xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{p if len(ls) > 1 else page_dir(ls[0], p)}"/>'
        urls += [f'<url><loc>{SITE}{page_dir(l, p)}</loc>{alts}</url>' for l in ls]
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            + '\n'.join(urls) + '\n</urlset>\n')


def main():
    meta = page_meta()
    if '--list' in sys.argv:                 # build.py --list / --missing: texts collected, pages were not written
        return
    for path, by_lang in meta.items():
        for lang, (title, desc) in by_lang.items():
            if lang != 'ru':
                cyr = re.findall(r'[А-Яа-яЁё]', title + desc) if lang not in ('ru', 'uk') else []
                assert not cyr, (path, lang, title, desc)
            full = os.path.join(HERE, page_dir(lang, path), 'index.html')
            html = open(full, encoding='utf-8').read()
            open(full, 'w', encoding='utf-8', newline='\n').write(apply(html, path, lang, title, desc))
    with open(os.path.join(HERE, 'sitemap.xml'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(sitemap({p: v for p, v in meta.items() if p not in NOINDEX}))
    print(f'seo: {sum(map(len, meta.values()))} pages, sitemap.xml, analytics {"on" if CF_BEACON_TOKEN else "off (CF_BEACON_TOKEN empty)"}', file=sys.stderr)


if __name__ == '__main__':
    main()
