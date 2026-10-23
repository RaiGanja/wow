"""Гайды: тексты сразу на трёх языках. Строка = {'ru': …, 'en': …, 'uk': …}.
Названия игровых объектов на EN/UK английские. Факты — только из источников в 'sources'.
Блок = (тип, данные):
  ('text', [строка, …])                                 абзацы
  ('steps', [{'t': строка, 'd': строка}, …])           карточки 01/02/03
  ('tiles', [{'t', 'd', 'href', 'art'}, …])            плитки с артом; href относительно корня гида, art = имя без размера
  ('table', {'head': [строка, …], 'rows': [[строка|str, …], …]})
  ('tabs', [{'id': 'alliance', 't': строка, 'blocks': [блок, …]}, …])
  ('faq', [{'id': 'release', 'q': строка, 'a': [строка, …]}, …])
  ('tip', строка)
  ('raw', 'html')   только для живых частей, разметка с data-атрибутами для JS"""


def t(ru, en, uk):
    return {'ru': ru, 'en': en, 'uk': uk}


HUB = {
    'slug': '', 'art': 'hero_campfire', 'updated': '23.10.2026',
    'title': t('Гайды', 'Guides', 'Гайди'),
    'lead': t('Прокачка, подземелья, профессии, ответы на вопросы и новости WoW Forever.',
              'Leveling, dungeons, professions, answers and news for WoW Forever.',
              'Прокачка, підземелля, професії, відповіді на питання та новини WoW Forever.'),
}

GUIDES = []   # наполняется в задачах 3, 5, 6, 7, 9; каждый гайд дописывается ниже через GUIDES.append

NEWS = []     # ручные записи: {'date': '2026-10-23', 'title': t(...), 'text': t(...), 'url': 'https://…'}
ORDER = ['leveling', 'dungeons', 'professions', 'faq', 'news', 'ukrainian']   # порядок плиток на хабе и в «Другие гайды»


# ---------- FAQ: даты и наборы, режимы, имена, отличия от Era (переехали с главной) + частые вопросы ----------

GUIDES.append({
    'slug': 'faq', 'art': 'mage', 'updated': '23.10.2026', 'js': 'faq',
    'title': t('FAQ и даты', 'FAQ and dates', 'FAQ і дати'),
    'lead': t('Даты до и после релиза, наборы и цены, режимы, имена и ответы на частые вопросы.',
              'Dates before and after release, packs and prices, modes, names and answers to common questions.',
              'Дати до й після релізу, набори та ціни, режими, імена та відповіді на часті питання.'),
    'tile': t('Даты, наборы, режимы и ответы на вопросы', 'Dates, packs, modes and answers', 'Дати, набори, режими та відповіді'),
    'pills': [t('Релиз 04.11.2026', 'Release 04.11.2026', 'Реліз 04.11.2026'),
              t('Имена с 27.10', 'Names from 27.10', 'Імена з 27.10'),
              t('Рейды 09.12', 'Raids 09.12', 'Рейди 09.12')],
    'sources': [
        (t('ClassicWoW.gg: даты беты, имён, рейдов, отличия от Era', 'ClassicWoW.gg: beta, names, raids, Era differences',
           'ClassicWoW.gg: дати бети, імен, рейдів, відмінності від Era'), 'https://classicwow.gg/forever'),
        (t('Warcraft Tavern: наборы и цены', 'Warcraft Tavern: editions and prices', 'Warcraft Tavern: набори та ціни'),
         'https://www.warcrafttavern.com/news/world-of-warcraft-forever-editions-skyborne-race-unlock-beta-access/'),
        (t('Warcraft Tavern: изменения беты от 15 октября', 'Warcraft Tavern: 15 October beta changes', 'Warcraft Tavern: зміни бети від 15 жовтня'),
         'https://www.warcrafttavern.com/forever/news/racial-class-ability-changes-in-the-wow-forever-beta/'),
        (t('Warcraft Tavern: расы', 'Warcraft Tavern: races', 'Warcraft Tavern: раси'), 'https://www.warcrafttavern.com/forever/guides/races/'),
        (t('Team Overpowered: имена и фамилии', 'Team Overpowered: names and surnames', 'Team Overpowered: імена та прізвища'),
         'https://teamoverpowered.com/forever/guides/name-reservation/'),
    ],
    'sections': [
        {'id': 'dates', 'title': t('Даты', 'Dates', 'Дати'), 'blocks': [
            ('table', {'head': [t('Когда', 'When', 'Коли'), t('Событие', 'Event', 'Подія'), t('Что важно', 'What matters', 'Що важливо')], 'rows': [
                ['17.09 – 23.10', t('Закрытая бета', 'Closed beta', 'Закрита бета'),
                 t('Доступ был у владельцев наборов Epic и Collection. Бета завершилась 23.10 в 10:00 по тихоокеанскому времени. 08.10 в бету добавили City of Dalaran и примерно на 20% больше опыта за врагов в подземельях.',
                   'Access was for Epic and Collection owners. The beta ended on 23.10 at 10:00 Pacific time. On 08.10 the beta got City of Dalaran and about 20% more experience for enemies in dungeons.',
                   'Доступ мали власники наборів Epic і Collection. Бета завершилася 23.10 о 10:00 за тихоокеанським часом. 08.10 у бету додали City of Dalaran і приблизно на 20% більше досвіду за ворогів у підземеллях.')],
                ['15.10', t('Крупный патч беты', 'Major beta patch', 'Великий патч бети'),
                 t('Переделаны способности рас (оружейные специализации заменены критами) и настроены почти все классы.',
                   'Racial abilities were reworked (weapon specializations replaced with crits) and almost all classes were tuned.',
                   'Переробили здібності рас (спеціалізації зброї замінили критами) і налаштували майже всі класи.')],
                ['27.10 – 03.11', t('Ранняя резервация имён', 'Early name reservation', 'Рання резервація імен'),
                 t('Входит в наборы Heroic, Epic и Collection. До трёх персонажей на аккаунт, кто первым пришёл, тот и занял. Это не ранний доступ в игру. Точное время открытия Blizzard пока не назвала.',
                   'Included in the Heroic, Epic and Collection packs. Up to three characters per account, first come, first served. This is not early access to the game. Blizzard has not yet named the exact opening time.',
                   'Входить у набори Heroic, Epic і Collection. До трьох персонажів на акаунт, хто перший прийшов, той і зайняв. Це не ранній доступ до гри. Точний час відкриття Blizzard поки не назвала.')],
                ['04.11', t('Релиз WoW Forever', 'WoW Forever release', 'Реліз WoW Forever'),
                 t('Нужна подписка или игровое время. Forever — постоянная игра рядом с Retail и Classic, а не сезон. Точное время старта Blizzard пока не подтвердила. Некоторые сайты называют 15:00 по тихоокеанскому, это 23:00 UTC.',
                   'Requires a subscription or game time. Forever is a permanent game next to Retail and Classic, not a season. Blizzard has not yet confirmed the exact launch time. Some sites name 15:00 Pacific, which is 23:00 UTC.',
                   'Потрібна підписка або ігровий час. Forever — постійна гра поруч із Retail і Classic, а не сезон. Точний час старту Blizzard поки не підтвердила. Деякі сайти називають 15:00 за тихоокеанським, це 23:00 UTC.')],
                ['09.12', t('Открываются рейды', 'Raids open', 'Відкриваються рейди'),
                 t('Barrow Deeps (10 игроков), Hyjal Summit (20), Onyxia’s Lair (40). До этого есть пять недель на прокачку и подземелья.',
                   'Barrow Deeps (10 players), Hyjal Summit (20), Onyxia’s Lair (40). Until then you have five weeks for leveling and dungeons.',
                   'Barrow Deeps (10 гравців), Hyjal Summit (20), Onyxia’s Lair (40). До цього є п’ять тижнів на прокачування та підземелля.')],
            ]}),
        ]},
        {'id': 'editions', 'title': t('Наборы и цены', 'Packs and prices', 'Набори та ціни'), 'blocks': [
            ('table', {'head': [t('Набор', 'Pack', 'Набір'), t('Цена', 'Price', 'Ціна'), t('Что даёт', 'What you get', 'Що дає')], 'rows': [
                ['Heroic Pack', '$29.99', t('Расу Скайборн, её стартовую зону и раннюю резервацию имён.',
                                            'The Skyborne race, its starting zone and early name reservation.',
                                            'Расу Скайборн, її стартову зону та ранню резервацію імен.')],
                ['Epic Pack', '$59.99', t('То же плюс доступ к бете.', 'The same plus beta access.', 'Те саме плюс доступ до бети.')],
                ['Warcraft Forever Collection', '$79.99', t('Продаётся до 11.01.2027, с доступом к бете.',
                                                            'On sale until 11.01.2027, with beta access.',
                                                            'Продається до 11.01.2027, з доступом до бети.')],
            ]}),
            ('text', [t('Остальные восемь рас и все девять классов докупать не нужно.',
                        'The other eight races and all nine classes do not need to be bought.',
                        'Решту восьми рас і всі дев’ять класів докуповувати не потрібно.')]),
        ]},
        {'id': 'language', 'langs': ('ru', 'uk'),   # только ru и uk: язык клиента и аддоны перевода
         'title': {'ru': 'Играть на русском', 'uk': 'Грати українською'}, 'blocks': [
            ('raw', {
                'ru': '<p>У WoW Forever есть русский клиент. В лаунчере Battle.net откройте настройки игры и выберите язык «Русский». Русификатор не нужен.</p>'
                      '<p>Русская озвучка заданий, истории зон и книг — аддон Wayfarer — Russian VoiceOver. Работает только с русским клиентом. Запасной вариант — Russian Quests Voiceover.</p>'
                      '<p class="gbtns"><a class="btn ghost" href="https://www.curseforge.com/wow/addons/wayfarer-russian-voiceover" target="_blank" rel="noopener">Wayfarer на CurseForge ↗</a>'
                      '<a class="btn ghost" href="https://www.curseforge.com/wow/addons/wowvoice-classic" target="_blank" rel="noopener">Russian Quests Voiceover ↗</a></p>',
                'uk': '<p>Українського клієнта у WoW Forever немає. Українською грають з аддоном UA_Forever: він перекладає завдання, підказки й вікна поверх клієнта.</p>'
                      '<p class="gbtns"><a class="btn ghost" href="https://www.curseforge.com/wow/addons/ua-forever" target="_blank" rel="noopener">Відкрити на CurseForge ↗</a>'
                      '<a class="btn ghost" href="../ukrainian/">Як грати українською</a></p>',
            }),
        ]},
        {'id': 'modes', 'title': t('Режимы игры', 'Game modes', 'Режими гри'), 'blocks': [
            ('steps', [
                {'t': t('Обычный, PvP и RP', 'Normal, PvP and RP', 'Звичайний, PvP і RP'),
                 'd': t('Hardcore запустят позже со своими правилами.', 'Hardcore will launch later with its own rules.',
                        'Hardcore запустять пізніше зі своїми правилами.')},
                {'t': t('Группа только в одном режиме', 'Groups stay within one mode', 'Група лише в одному режимі'),
                 'd': t('Группироваться можно только внутри одного режима. В PvP при создании доступна одна фракция.',
                        'You can only group within one mode. In PvP only one faction is available at character creation.',
                        'Групуватися можна лише в межах одного режиму. У PvP під час створення доступна одна фракція.')},
            ]),
            ('tip', t('Договоритесь заранее: одна фракция, один режим, одни и те же дни на старт.',
                      'Agree in advance: one faction, one mode, the same days for launch.',
                      'Домовтеся заздалегідь: одна фракція, один режим, одні й ті самі дні на старт.')),
        ]},
        {'id': 'names', 'title': t('Имена и фамилии', 'Names and surnames', 'Імена та прізвища'), 'blocks': [
            ('steps', [
                {'t': t('Имя и фамилия', 'First name and surname', 'Ім’я та прізвище'),
                 'd': t('У каждого персонажа есть имя и фамилия.', 'Every character has a first name and a surname.',
                        'Кожен персонаж має ім’я та прізвище.')},
                {'t': t('Реалмов нет', 'No realms', 'Реалмів немає'),
                 'd': t('Полное имя должно быть уникальным во всём регионе. Одно имя у двоих возможно, если фамилии разные.',
                        'The full name must be unique across the whole region. Two players can share a first name if their surnames differ.',
                        'Повне ім’я має бути унікальним у всьому регіоні. Одне ім’я у двох можливе, якщо прізвища різні.')},
                {'t': t('Фамилию можно скрыть', 'The surname can be hidden', 'Прізвище можна приховати'),
                 'd': 'Esc → Options → Nameplates → My Secondary Name.'},
                {'t': t('Одна фракция в PvP', 'One faction in PvP', 'Одна фракція в PvP'),
                 'd': t('В PvP-режиме на аккаунте может быть только одна фракция.', 'In PvP mode an account can have only one faction.',
                        'У PvP-режимі на акаунті може бути лише одна фракція.')},
            ]),
            ('tip', t('Подготовьте до 27.10 имя, фамилию и два-три запасных варианта: короткие имена разберут первыми.',
                      'Prepare a name, a surname and two or three backups before 27.10: short names will go first.',
                      'Підготуйте до 27.10 ім’я, прізвище й два-три запасні варіанти: короткі імена розберуть першими.')),
        ]},
        {'id': 'era', 'title': t('Чем Forever отличается от Classic Era', 'How Forever differs from Classic Era', 'Чим Forever відрізняється від Classic Era'), 'blocks': [
            ('table', {'head': [t('Тема', 'Topic', 'Тема'), t('Что в Forever', 'What Forever has', 'Що у Forever')], 'rows': [
                [t('Общее', 'General', 'Загальне'),
                 t('Eastern Kingdoms и Kalimdor, прокачка до 60. Постоянная игра, а не сезон. Нет летающих скакунов и нет масштабирования уровней, как и в Classic.',
                   'Eastern Kingdoms and Kalimdor, leveling to 60. A permanent game, not a season. No flying mounts and no level scaling, as in Classic.',
                   'Eastern Kingdoms та Kalimdor, прокачування до 60. Постійна гра, а не сезон. Немає літаючих скакунів і масштабування рівнів, як і в Classic.')],
                [t('Контент', 'Content', 'Контент'),
                 t('Новые зоны, задания, 9 новых подземелий, 3 новых рейда, новое поле боя, новая раса Скайборн.',
                   'New zones, quests, 9 new dungeons, 3 new raids, a new battleground, the new Skyborne race.',
                   'Нові зони, завдання, 9 нових підземель, 3 нові рейди, нове поле бою, нова раса Скайборн.')],
                [t('Классы и расы', 'Classes and races', 'Класи та раси'),
                 t('Обновлены таланты и способности классов, новые сочетания рас и классов, у рас убраны сопротивления и добавлены свои способности.',
                   'Class talents and abilities were updated, there are new race and class combinations, and races lost resistances and gained their own abilities.',
                   'Оновлено таланти та здібності класів, нові поєднання рас і класів, у рас прибрано опори й додано свої здібності.')],
                [t('Системы', 'Systems', 'Системи'),
                 t('Legacy, лагерь, опциональная трансмогрификация и выбор визуального стиля (Classic или современный), официальная поддержка геймпада.',
                   'Legacy, camp, optional transmog and a choice of visual style (Classic or modern), official gamepad support.',
                   'Legacy, табір, опціональна трансмогрифікація та вибір візуального стилю (Classic або сучасний), офіційна підтримка геймпада.')],
                [t('Предметы', 'Items', 'Предмети'),
                 t('Характеристики и предметы изменены, поэтому старые списки добычи из Classic ненадёжны.',
                   'Stats and items were changed, so old Classic loot lists are unreliable.',
                   'Характеристики та предмети змінено, тому старі списки здобичі з Classic ненадійні.')],
            ]}),
        ]},
        {'id': 'questions', 'title': t('Частые вопросы', 'Common questions', 'Часті питання'), 'blocks': [
            ('raw', t('<label class="gsearch"><span class="sr">Поиск по вопросам</span><input type="search" id="faqQ" autocomplete="off" placeholder="Поиск по вопросам"></label>',
                      '<label class="gsearch"><span class="sr">Search questions</span><input type="search" id="faqQ" autocomplete="off" placeholder="Search questions"></label>',
                      '<label class="gsearch"><span class="sr">Пошук по питаннях</span><input type="search" id="faqQ" autocomplete="off" placeholder="Пошук по питаннях"></label>')),
            ('faq', [
                {'id': 'release', 'q': t('Когда выходит WoW Forever?', 'When does WoW Forever launch?', 'Коли виходить WoW Forever?'),
                 'a': [t('04.11.2026. Точное время старта Blizzard пока не подтвердила. Некоторые сайты называют 15:00 по тихоокеанскому, это 23:00 UTC.',
                         '04.11.2026. Blizzard has not yet confirmed the exact launch time. Some sites name 15:00 Pacific, which is 23:00 UTC.',
                         '04.11.2026. Точний час старту Blizzard поки не підтвердила. Деякі сайти називають 15:00 за тихоокеанським, це 23:00 UTC.')]},
                {'id': 'subscription', 'q': t('Нужна ли подписка?', 'Do I need a subscription?', 'Чи потрібна підписка?'),
                 'a': [t('Да, подписка или игровое время. Forever — постоянная игра рядом с Retail и Classic, а не сезон.',
                         'Yes, a subscription or game time. Forever is a permanent game next to Retail and Classic, not a season.',
                         'Так, підписка або ігровий час. Forever — постійна гра поруч із Retail і Classic, а не сезон.')]},
                {'id': 'price', 'q': t('Сколько стоят наборы и нужны ли они?', 'How much are the packs, and do I need one?', 'Скільки коштують набори і чи потрібні вони?'),
                 'a': [t('Heroic Pack $29.99, Epic Pack $59.99, Warcraft Forever Collection $79.99. Набор нужен только ради расы Скайборн и ранней резервации имён: остальные восемь рас и все девять классов докупать не нужно.',
                         'Heroic Pack $29.99, Epic Pack $59.99, Warcraft Forever Collection $79.99. A pack is only needed for the Skyborne race and early name reservation: the other eight races and all nine classes do not need to be bought.',
                         'Heroic Pack $29.99, Epic Pack $59.99, Warcraft Forever Collection $79.99. Набір потрібен лише заради раси Скайборн і ранньої резервації імен: решту восьми рас і всі дев’ять класів докуповувати не потрібно.')]},
                {'id': 'reserve', 'q': t('Когда бронировать имя?', 'When can I reserve a name?', 'Коли бронювати ім’я?'),
                 'a': [t('С 27.10 по 03.11, если у вас Heroic, Epic или Collection. До трёх персонажей на аккаунт, кто первым пришёл, тот и занял. Это не ранний доступ в игру.',
                         'From 27.10 to 03.11 if you own Heroic, Epic or Collection. Up to three characters per account, first come, first served. This is not early access to the game.',
                         'З 27.10 по 03.11, якщо у вас Heroic, Epic або Collection. До трьох персонажів на акаунт, хто перший прийшов, той і зайняв. Це не ранній доступ до гри.')]},
                {'id': 'surname', 'q': t('Зачем фамилия и можно ли взять то же имя, что у друга?', 'Why a surname, and can two people share a name?', 'Навіщо прізвище і чи можна взяти те саме ім’я, що в друга?'),
                 'a': [t('Реалмов нет, поэтому уникальным должно быть полное имя во всём регионе. Одно имя у двоих возможно, если фамилии разные. Фамилию можно скрыть: Esc → Options → Nameplates → My Secondary Name.',
                         'There are no realms, so the full name must be unique across the whole region. Two players can share a first name if their surnames differ. You can hide the surname: Esc → Options → Nameplates → My Secondary Name.',
                         'Реалмів немає, тому унікальним має бути повне ім’я у всьому регіоні. Одне ім’я у двох можливе, якщо прізвища різні. Прізвище можна приховати: Esc → Options → Nameplates → My Secondary Name.')]},
                {'id': 'skyborne', 'q': t('Что такое Скайборн?', 'What is Skyborne?', 'Що таке Скайборн?'),
                 'a': [t('Новая раса Forever, открывается любым из трёх наборов. Играбельна за обе фракции, фракция выбирается при создании. Обе ветки говорят на общем языке, а стартовая зона Zephras Isle общая.',
                         'The new Forever race, unlocked by any of the three packs. Playable for both factions, the faction is chosen at character creation. Both branches speak a common language and share the Zephras Isle starting zone.',
                         'Нова раса Forever, відкривається будь-яким із трьох наборів. Доступна за обидві фракції, фракцію обирають під час створення. Обидві гілки говорять спільною мовою, а стартова зона Zephras Isle спільна.')]},
                {'id': 'levels', 'q': t('До какого уровня качаться и где?', 'What is the level cap, and where do we level?', 'До якого рівня качатися і де?'),
                 'a': [t('До 60, в [[Восточных королевствах|Eastern Kingdoms]] и [[Калимдоре|Kalimdor]]. Летающих скакунов и масштабирования уровней нет, как и в Classic.',
                         'Up to 60, in the Eastern Kingdoms and Kalimdor. No flying mounts and no level scaling, as in Classic.',
                         'До 60, у Eastern Kingdoms і Kalimdor. Літаючих скакунів і масштабування рівнів немає, як і в Classic.')]},
                {'id': 'together', 'q': t('Можно ли играть вместе, если выбрали разные режимы?', 'Can we play together in different modes?', 'Чи можна грати разом, якщо обрали різні режими?'),
                 'a': [t('Нет: группироваться можно только внутри одного режима. Режимы на старте: обычный, PvP и RP, Hardcore запустят позже. В PvP на аккаунте может быть только одна фракция.',
                         'No: you can only group within one mode. Modes at launch: Normal, PvP and RP, Hardcore comes later. In PvP an account can have only one faction.',
                         'Ні: групуватися можна лише в межах одного режиму. Режими на старті: звичайний, PvP і RP, Hardcore запустять пізніше. У PvP на акаунті може бути лише одна фракція.')]},
                {'id': 'group-choice', 'q': t('Какой регион, режим и фракцию выбрать, чтобы играть с друзьями?', 'Which region, mode and faction should we pick to play with friends?', 'Який регіон, режим і фракцію обрати, щоб грати з друзями?'),
                 'a': [t('Одни и те же на всех. Регионы разделены, межрегиональной игры нет, поэтому берите регион с лучшим пингом для большинства. Группа собирается только внутри одного режима, а Альянс и Орда не встают в одну группу ни в каком режиме. В PvP на аккаунте одна фракция, так что договоритесь о ней до брони имён 27.10.',
                         'The same for everyone. Regions are separate and there is no cross-region play, so pick the region with the best ping for most of you. Groups form only within one mode, and Alliance and Horde cannot group in any mode. In PvP an account has only one faction, so agree on it before name reservation opens on 27.10.',
                         'Однакові для всіх. Регіони розділені, міжрегіональної гри немає, тож беріть регіон із найкращим пінгом для більшості. Група збирається лише в межах одного режиму, а Альянс і Орда не стають в одну групу в жодному режимі. У PvP на акаунті одна фракція, тож домовтеся про неї до бронювання імен 27.10.')]},
                {'id': 'raids', 'q': t('Когда откроются рейды?', 'When do raids open?', 'Коли відкриються рейди?'),
                 'a': [t('09.12: Barrow Deeps (10 игроков), Hyjal Summit (20), Onyxia’s Lair (40). До этого есть пять недель на прокачку и подземелья.',
                         '09.12: Barrow Deeps (10 players), Hyjal Summit (20), Onyxia’s Lair (40). Until then you have five weeks for leveling and dungeons.',
                         '09.12: Barrow Deeps (10 гравців), Hyjal Summit (20), Onyxia’s Lair (40). До цього є п’ять тижнів на прокачування та підземелля.')]},
                {'id': 'beta', 'q': t('Можно ли ещё попасть в бету?', 'Can I still get into the beta?', 'Чи можна ще потрапити в бету?'),
                 'a': [t('Нет. Доступ был у владельцев Epic и Collection. Бета завершилась 23.10 в 10:00 по тихоокеанскому времени.',
                         'No. Access was for Epic and Collection owners. The beta ended on 23.10 at 10:00 Pacific time.',
                         'Ні. Доступ мали власники Epic і Collection. Бета завершилася 23.10 о 10:00 за тихоокеанським часом.')]},
                {'id': 'classic-guides', 'q': t('Подойдут ли старые гайды по Classic?', 'Are old Classic guides still useful?', 'Чи підійдуть старі гайди по Classic?'),
                 'a': [t('Только частично. Характеристики и предметы изменены, поэтому старые списки добычи ненадёжны. Добавлены 9 новых подземелий, 3 новых рейда, новые зоны и задания, у классов обновлены таланты.',
                         'Only partly. Stats and items were changed, so old loot lists are unreliable. There are 9 new dungeons, 3 new raids, new zones and quests, and class talents were updated.',
                         'Лише частково. Характеристики та предмети змінено, тому старі списки здобичі ненадійні. Додано 9 нових підземель, 3 нові рейди, нові зони та завдання, у класів оновлено таланти.')]},
                {'id': 'visuals', 'q': t('Будет ли современная графика и геймпад?', 'Is there modern graphics and gamepad support?', 'Чи буде сучасна графіка та геймпад?'),
                 'a': [t('Да: можно выбрать визуальный стиль (Classic или современный), есть опциональная трансмогрификация и официальная поддержка геймпада.',
                         'Yes: you can pick a visual style (Classic or modern), there is optional transmog and official gamepad support.',
                         'Так: можна обрати візуальний стиль (Classic або сучасний), є опціональна трансмогрифікація та офіційна підтримка геймпада.')]},
            ]),
        ]},
    ],
})

# ---------- Подземелья и рейды (переехали #dungeons и #group главной) ----------

def _dg_filter():
    """Filter bar + table shell for the dungeons list; rows are drawn by JS['dungeons'] from DUNGEONS."""
    out = {}
    for l, (flt, all_, mine, new, my, lo, hi, cols) in {
        'ru': ('Фильтр подземелий', 'Все', 'Мой уровень ±3', 'Новые', 'Мой уровень', 'Уровень ниже', 'Уровень выше', ('Подземелье', 'Уровни', 'Где вход')),
        'en': ('Dungeon filter', 'All', 'My level ±3', 'New', 'My level', 'Lower level', 'Higher level', ('Dungeon', 'Levels', 'Entrance')),
        'uk': ('Фільтр підземель', 'Усі', 'Мій рівень ±3', 'Нові', 'Мій рівень', 'Нижчий рівень', 'Вищий рівень', ('Підземелля', 'Рівні', 'Де вхід')),
    }.items():
        ths = ''.join(f'<th scope="col">{c}</th>' for c in cols)
        out[l] = (f'<div id="dgBox"><div class="filters" role="group" aria-label="{flt}">'
                  f'<div class="seg" id="segD"><button type="button" data-v="all" aria-pressed="true">{all_}</button>'
                  f'<button type="button" data-v="mine" aria-pressed="false">{mine}</button>'
                  f'<button type="button" data-v="new" aria-pressed="false">{new}</button></div>'
                  f'<div class="fgroup"><span class="flabel" id="ldgLvl">{my}</span><div class="stepper" role="group" aria-labelledby="ldgLvl">'
                  f'<button type="button" class="lvm" aria-label="{lo}">−</button>'
                  f'<input class="lvin" id="dgLvl" type="number" min="1" max="60" inputmode="numeric" aria-labelledby="ldgLvl" placeholder="—">'
                  f'<button type="button" class="lvp" aria-label="{hi}">+</button></div></div>'
                  f'<span class="small" id="dgCount" role="status"></span></div>'
                  f'<table class="gtable dgt"><thead><tr>{ths}</tr></thead>'
                  f'<tbody id="dgBody"></tbody></table></div>')
    return out


GUIDES.append({
    'slug': 'dungeons', 'art': 'warlock', 'updated': '23.10.2026', 'js': 'dungeons',
    'title': t('Подземелья и рейды', 'Dungeons and raids', 'Підземелля та рейди'),
    'lead': t('Все 35 подземелий по уровням с фильтром под вашего героя, три рейда и состав группы под любое число друзей.',
              'All 35 dungeons by level with a filter for your hero, three raids and a group lineup for any number of friends.',
              'Усі 35 підземель за рівнями з фільтром під вашого героя, три рейди та склад групи під будь-яку кількість друзів.'),
    'tile': t('35 подземелий по уровням, рейды, состав группы', '35 dungeons by level, raids, group lineup', '35 підземель за рівнями, рейди, склад групи'),
    'pills': [t('35 подземелий', '35 dungeons', '35 підземель'), t('9 новых', '9 new', '9 нових'),
              t('Рейды с 09.12', 'Raids from 09.12', 'Рейди з 09.12')],
    'sources': [
        (t('Warcraft Tavern: подземелья', 'Warcraft Tavern: dungeons', 'Warcraft Tavern: підземелля'), 'https://www.warcrafttavern.com/forever/guides/dungeons/'),
        (t('Sportskeeda: подземелья по уровням', 'Sportskeeda: dungeons by level', 'Sportskeeda: підземелля за рівнями'),
         'https://www.sportskeeda.com/mmo/world-warcraft-forever-all-dungeons-order-level-range'),
        (t('Icy Veins: обзор подземелий', 'Icy Veins: dungeons overview', 'Icy Veins: огляд підземель'), 'https://www.icy-veins.com/wow-forever/dungeons-overview'),
        (t('ClassicWoW.gg: подземелья', 'ClassicWoW.gg: dungeons', 'ClassicWoW.gg: підземелля'), 'https://classicwow.gg/forever/dungeons'),
        (t('Warcraft Tavern: Legacy', 'Warcraft Tavern: Legacy', 'Warcraft Tavern: Legacy'), 'https://www.warcrafttavern.com/forever/guides/legacy/'),
        (t('LFCarry: классы и темп прокачки', 'LFCarry: classes and leveling pace', 'LFCarry: класи та темп прокачування'), 'https://lfcarry.com/guides/wow-forever-classes'),
    ],
    'sections': [
        {'id': 'list', 'title': t('Подземелья по уровням', 'Dungeons by level', 'Підземелля за рівнями'), 'blocks': [
            ('text', [t('Все 35 подземелий, из них 9 новых. Уровни по Warcraft Tavern, Sportskeeda даёт те же. Где другие сайты называют иной диапазон, он подписан мелко. Жёстких ограничений по уровню Blizzard не публиковала.',
                        'All 35 dungeons, 9 of them new. Levels are from Warcraft Tavern, Sportskeeda gives the same. Where other sites list a different range, it is shown in small print. Blizzard has not published hard level limits.',
                        'Усі 35 підземель, з них 9 нових. Рівні за Warcraft Tavern, Sportskeeda дає ті самі. Де інші сайти називають інший діапазон, він підписаний дрібно. Жорстких обмежень за рівнем Blizzard не публікувала.')]),
            ('raw', _dg_filter()),
            ('text', [t('Основной опыт за подземелье дают его цепочки заданий, повторные заходы приносят заметно меньше. Любая выпавшая вещь открывает свой облик всем в группе, кто может её надеть. Ещё по два подземелья Blizzard обещает весной и летом.',
                        'Most dungeon experience comes from its quest chains, repeat runs give noticeably less. Every item that drops unlocks its appearance for everyone in the group who can wear it. Blizzard promises two more dungeons in spring and two in summer.',
                        'Основний досвід за підземелля дають його ланцюжки завдань, повторні заходи дають помітно менше. Будь-яка річ, що випала, відкриває свій вигляд усім у групі, хто може її вдягнути. Ще по два підземелля Blizzard обіцяє навесні та влітку.')]),
        ]},
        {'id': 'raids', 'title': t('Рейды (с 09.12.2026)', 'Raids (from 09.12.2026)', 'Рейди (з 09.12.2026)'), 'blocks': [
            ('steps', [
                {'t': 'Barrow Deeps', 'd': t('10 игроков', '10 players', '10 гравців')},
                {'t': 'Hyjal Summit', 'd': t('20 игроков', '20 players', '20 гравців')},
                {'t': 'Onyxia’s Lair', 'd': t('40 игроков, в [[Пылевых топях|Dustwallow Marsh]]', '40 players, in Dustwallow Marsh', '40 гравців, у Dustwallow Marsh')},
            ]),
            ('text', [t('За прохождение каждого из этих рейдов в Legacy даётся по очку.', 'Completing each of these raids gives one Legacy point.',
                        'За проходження кожного з цих рейдів у Legacy дається по одному очку.')]),
        ]},
        {'id': 'pvp', 'title': 'PvP', 'blocks': [
            ('steps', [
                {'t': 'Darkspear Islands', 'd': t('Новое поле боя 15 на 15 у побережья [[Пылевых топей|Dustwallow Marsh]].', 'New 15v15 battleground off the coast of Dustwallow Marsh.',
                                                  'Нове поле бою 15 на 15 біля узбережжя Dustwallow Marsh.')},
                {'t': t('Звания и Честь', 'Ranks and Honor', 'Звання та Честь'),
                 'd': t('Звания с недельным лимитом, улучшение экипировки за Честь, сезонные цели Legacy.', 'Ranks with a weekly limit, gear upgrades for Honor, seasonal Legacy goals.',
                        'Звання з тижневим лімітом, покращення екіпірування за Честь, сезонні цілі Legacy.')},
            ]),
        ]},
        {'id': 'group', 'title': t('Состав группы', 'Group composition', 'Склад групи'), 'blocks': [
            ('steps', [
                {'t': t('Подземелья на 5', 'Dungeons for 5', 'Підземелля на 5'),
                 'd': t('Подземелья рассчитаны на 5 игроков: танк, лекарь, трое с уроном.', 'Dungeons are designed for 5 players: a tank, a healer and three damage dealers.',
                        'Підземелля розраховані на 5 гравців: танк, цілитель, троє зі шкодою.')},
                {'t': t('Рейды на 10, 20 и 40', 'Raids for 10, 20 and 40', 'Рейди на 10, 20 і 40'),
                 'd': t('Если своих меньше, недостающих добирают из гильдии.', 'If your own group is smaller, the rest are filled from a guild.',
                        'Якщо своїх менше, решту добирають із гільдії.')},
                {'t': t('Кто танкует и лечит', 'Who tanks and heals', 'Хто танкує й лікує'),
                 'd': t('Танковать могут Воин, Паладин и Друид, лечить Паладин, Жрец, Шаман и Друид.', 'Warriors, Paladins and Druids can tank; Paladins, Priests, Shamans and Druids can heal.',
                        'Танкувати можуть Воїн, Паладин і Друїд, лікувати Паладин, Жрець, Шаман і Друїд.')},
                {'t': t('Паладин и Друид', 'Paladin and Druid', 'Паладин і Друїд'),
                 'd': t('Паладин и Друид умеют все три роли. Это самые гибкие классы, когда игроков мало.', 'Paladins and Druids can do all three roles. They are the most flexible classes when players are few.',
                        'Паладин і Друїд вміють усі три ролі. Це найгнучкіші класи, коли гравців мало.')},
                {'t': t('Баффы классов', 'Class buffs', 'Баффи класів'),
                 'd': t('Группа и рейд получают баффы классов: Королей от паладина, тотемы шамана, Боевой крик воина, ауры охотника и друида. Порталы, еду и воду делает маг.',
                        'Groups and raids receive class buffs: Kings from the paladin, shaman totems, the warrior’s Battle Shout, hunter and druid auras. Portals, food and water come from the mage.',
                        'Група й рейд отримують баффи класів: Королів від паладина, тотеми шамана, Бойовий клич воїна, аури мисливця та друїда. Портали, їжу та воду робить маг.')},
            ]),
            ('tabs', [
                {'id': 'solo', 't': t('Соло', 'Solo', 'Соло'), 'blocks': [
                    ('tip', t('Легче всего Охотнику и Чернокнижнику, у них питомец держит врага. Паладин и Друид тоже живучи и в подземелье пойдут на любую роль.',
                              'Hunters and Warlocks have it easiest, their pet holds the enemy. Paladins and Druids are also sturdy and can fill any role in a dungeon.',
                              'Найлегше Мисливцю й Чорнокнижнику, у них вихованець тримає ворога. Паладин і Друїд теж живучі й у підземеллі підуть на будь-яку роль.'))]},
                {'id': 'p2-4', 't': t('2–4 игрока', '2–4 players', '2–4 гравці'), 'blocks': [
                    ('tip', t('Пусть хотя бы один умеет танковать или лечить (Воин, Паладин, Друид, Жрец, Шаман), остальных до пяти добирайте в подземелье.',
                              'Make sure at least one of you can tank or heal (Warrior, Paladin, Druid, Priest, Shaman), and fill the dungeon group up to five.',
                              'Нехай хоча б один уміє танкувати або лікувати (Воїн, Паладин, Друїд, Жрець, Шаман), решту до п’яти добирайте в підземелля.'))]},
                {'id': 'p5', 't': t('5 игроков', '5 players', '5 гравців'), 'blocks': [
                    ('tip', t('Танк, лекарь и трое в урон, например Воин, Жрец, Маг, Охотник и Разбойник.',
                              'A tank, a healer and three damage dealers, for example Warrior, Priest, Mage, Hunter and Rogue.',
                              'Танк, цілитель і троє в шкоду, наприклад Воїн, Жрець, Маг, Мисливець і Розбійник.'))]},
                {'id': 'p6-9', 't': t('6–9 игроков', '6–9 players', '6–9 гравців'), 'blocks': [
                    ('tip', t('Две группы для подземелий, в каждой нужны свой танк и лекарь. Тут особенно ценны гибриды: Паладин, Друид, Шаман.',
                              'Two dungeon groups, each needs its own tank and healer. Hybrids are especially valuable here: Paladin, Druid, Shaman.',
                              'Дві групи для підземель, у кожній потрібні свій танк і цілитель. Тут особливо цінні гібриди: Паладин, Друїд, Шаман.'))]},
                {'id': 'p10', 't': t('10 и больше', '10 or more', '10 і більше'), 'blocks': [
                    ('tip', t('Хватает на 10-местный рейд Barrow Deeps: два танка, два-три лекаря, остальные в урон.',
                              'Enough for the 10-player Barrow Deeps raid: two tanks, two or three healers, the rest on damage.',
                              'Вистачає на 10-місний рейд Barrow Deeps: два танки, два-три цілителі, решта в шкоду.'))]},
            ]),
            ('tip', t('Берите разные классы: баффы разных классов складываются, а одинаковые перекрываются. Кто-то в группе берёт Кулинарию ради костра на 10 объектов, остальные по профессии под баффы лагеря.',
                      'Take different classes: buffs of different classes stack, while identical ones overlap. Someone in the group takes Cooking for a campfire with 10 objects, the others pick professions for camp buffs.',
                      'Беріть різні класи: баффи різних класів складаються, а однакові перекриваються. Хтось у групі бере Кулінарію заради вогнища на 10 об’єктів, решта за професією під баффи табору.')),
        ]},
        {'id': 'together', 'title': t('Прокачка вместе', 'Leveling together', 'Прокачування разом'), 'blocks': [
            ('steps', [
                {'t': t('Темп классов', 'Class pace', 'Темп класів'),
                 'd': t('По прогнозам Охотник и Маг прокачиваются быстрее всего (примерно на 8% быстрее среднего), Воин медленнее всех (около 12%), Друид и Жрец чуть медленнее среднего. Это оценки для беты, цифры могут измениться.',
                        'By forecasts, Hunter and Mage level fastest (about 8% faster than average), Warrior slowest (about 12%), Druid and Priest slightly slower than average. These are beta estimates, the figures may change.',
                        'За прогнозами Мисливець і Маг прокачуються найшвидше (приблизно на 8% швидше за середнє), Воїн повільніше за всіх (близько 12%), Друїд і Жрець трохи повільніше за середнє. Це оцінки для бети, цифри можуть змінитися.')},
                {'t': t('Без масштабирования', 'No level scaling', 'Без масштабування'),
                 'd': t('Подземелья для своих уровней, их нельзя пройти «подтянув» слабого друга.', 'Dungeons are for their own levels, and you cannot run them by “pulling up” a weaker friend.',
                        'Підземелля для своїх рівнів, їх не можна пройти «підтягнувши» слабкого друга.')},
                {'t': t('Копите отдых', 'Save up rest', 'Копіть відпочинок'),
                 'd': t('Спальник, Well Rested и еда с бонусом опыта складываются.', 'The bedroll, Well Rested and food with an experience bonus stack.',
                        'Спальник, Well Rested і їжа з бонусом досвіду складаються.')},
                {'t': t('Лагерь на прокачке', 'Camp while leveling', 'Табір на прокачуванні'),
                 'd': t('Лагерь можно ставить прямо на прокачке, пять минут на костёр окупаются баффами на группу.',
                        'You can set up camp right while leveling; five minutes for a campfire pays off with buffs for the group.',
                        'Табір можна ставити просто на прокачуванні, п’ять хвилин на вогнище окупаються баффами на групу.')},
            ]),
            ('tip', t('С 4 ноября по 9 декабря прокачайтесь вместе по подземельям и заранее решите, кто за какой класс, чтобы не дублироваться.',
                      'From 4 November to 9 December, level up together through dungeons, and decide in advance who plays which class so you do not duplicate.',
                      'З 4 листопада по 9 грудня прокачайтеся разом по підземеллях і заздалегідь вирішіть, хто за який клас, щоб не дублюватися.')),
        ]},
    ],
})

# ---------- Прокачка 1–60 (переехали #legacy и #camp главной) ----------

GUIDES.append({
    'slug': 'leveling', 'art': 'hero_dawn', 'updated': '23.10.2026',
    'title': t('Прокачка 1–60', 'Leveling 1–60', 'Прокачування 1–60'),
    'lead': t('Маршрут по зонам для Альянса и Орды, отдых и бонусы опыта, советы соло, вдвоём и группой, Legacy и лагерь.',
              'A zone route for Alliance and Horde, rest and experience bonuses, tips for solo, duo and group play, Legacy and the camp.',
              'Маршрут зонами для Альянсу та Орди, відпочинок і бонуси досвіду, поради соло, удвох і групою, Legacy та табір.'),
    'tile': t('Зоны по уровням, отдых, Legacy и лагерь', 'Zones by level, rest, Legacy and the camp', 'Зони за рівнями, відпочинок, Legacy і табір'),
    'pills': [t('Альянс и Орда', 'Alliance and Horde', 'Альянс і Орда'), t('Ездовое с 40', 'Mount at 40', 'Їздова тварина з 40'),
              t('4 084 700 опыта до 60', '4,084,700 XP to 60', '4 084 700 досвіду до 60')],
    'sources': [
        (t('Mobalytics: зоны по уровням и маршруты', 'Mobalytics: zones by level and routes', 'Mobalytics: зони за рівнями та маршрути'),
         'https://mobalytics.gg/wow-forever/guides/zone-map-level-ranges'),
        (t('Icy Veins: новые зоны', 'Icy Veins: new zones', 'Icy Veins: нові зони'), 'https://www.icy-veins.com/wow-forever/zones-and-maps'),
        (t('Warcraft Tavern: опыт и отдых', 'Warcraft Tavern: experience and rested XP', 'Warcraft Tavern: досвід і відпочинок'),
         'https://www.warcrafttavern.com/forever/guides/experience/'),
        (t('Warcraft Tavern: верховая езда', 'Warcraft Tavern: riding', 'Warcraft Tavern: верхова їзда'), 'https://www.warcrafttavern.com/forever/guides/riding/'),
        (t('Blizzard: Legacy', 'Blizzard: Legacy', 'Blizzard: Legacy'), 'https://news.blizzard.com/en-gb/article/24307383'),
        (t('Warcraft Tavern: Legacy', 'Warcraft Tavern: Legacy', 'Warcraft Tavern: Legacy'), 'https://www.warcrafttavern.com/forever/guides/legacy/'),
        (t('Warcraft Tavern: лагерь', 'Warcraft Tavern: camping', 'Warcraft Tavern: табір'), 'https://www.warcrafttavern.com/forever/guides/camping/'),
    ],
    'sections': [
        {'id': 'route', 'title': t('Маршрут по зонам', 'Zone route', 'Маршрут зонами'), 'blocks': [
            ('text', [t('Диапазоны уровней по карте Mobalytics, новые зоны сверены с Icy Veins. Это ориентир для беты: Blizzard может сдвинуть уровни к релизу. Масштабирования нет, у каждой зоны свои уровни.',
                        'Level ranges are from the Mobalytics map, new zones checked against Icy Veins. This is a beta guideline: Blizzard may shift levels by release. There is no level scaling, each zone has its own levels.',
                        'Діапазони рівнів за мапою Mobalytics, нові зони звірені з Icy Veins. Це орієнтир для бети: Blizzard може зсунути рівні до релізу. Масштабування немає, кожна зона має свої рівні.')]),
            ('tabs', [
                {'id': 'alliance', 't': t('Альянс', 'Alliance', 'Альянс'), 'blocks': [
                    ('steps', [
                        {'t': '1–10', 'd': t('Люди: Elwynn Forest. Дворфы и гномы: Dun Morogh. Ночные эльфы: Teldrassil, до 11. Высшие скайборны: Zephras Isle, до 12.',
                                             'Human: Elwynn Forest. Dwarf and Gnome: Dun Morogh. Night Elf: Teldrassil (to 11). High Order Skyborne: Zephras Isle (to 12).',
                                             'Human: Elwynn Forest. Dwarf і Gnome: Dun Morogh. Night Elf: Teldrassil (до 11). High Order Skyborne: Zephras Isle (до 12).')},
                        {'t': '10–18', 'd': t('Westfall или Loch Modan, ночные эльфы обычно в [[Темных берегах|Darkshore]]. С 15 подходит Redridge Mountains.',
                                              'Westfall or Loch Modan, Night Elves usually go to Darkshore. From 15, Redridge Mountains fit.',
                                              'Westfall або Loch Modan, нічні ельфи зазвичай у Darkshore. З 15 підходять Redridge Mountains.')},
                        {'t': '18–30', 'd': t('Duskwood, Redridge Mountains и Wetlands, в [[Калимдоре|Kalimdor]] Stonetalon Mountains и Ashenvale.',
                                              'Duskwood, Redridge Mountains and Wetlands; in Kalimdor, Stonetalon Mountains and Ashenvale.',
                                              'Duskwood, Redridge Mountains і Wetlands, у Kalimdor Stonetalon Mountains і Ashenvale.')},
                        {'t': '30–45', 'd': t('Desolace или Arathi Highlands, Stranglethorn Vale. С 35: новая зона Riverglades между [[Красногорьем|Redridge Mountains]] и [[Пылающими степями|Burning Steppes]], Dustwallow Marsh, Badlands, Swamp of Sorrows.',
                                              'Desolace or Arathi Highlands, Stranglethorn Vale. From 35: the new Riverglades zone between Redridge and Burning Steppes, Dustwallow Marsh, Badlands, Swamp of Sorrows.',
                                              'Desolace або Arathi Highlands, Stranglethorn Vale. З 35: нова зона Riverglades між Redridge і Burning Steppes, Dustwallow Marsh, Badlands, Swamp of Sorrows.')},
                        {'t': '40–55', 'd': t('Tanaris, Feralas, The Hinterlands, затем Searing Gorge, Blasted Lands, Azshara, с 48 [[Кратер Ун’Горо|Un’Goro Crater]] и Felwood.',
                                              'Tanaris, Feralas, The Hinterlands, then Searing Gorge, Blasted Lands, Azshara, from 48 Un’Goro Crater and Felwood.',
                                              'Tanaris, Feralas, The Hinterlands, далі Searing Gorge, Blasted Lands, Azshara, з 48 Un’Goro Crater і Felwood.')},
                        {'t': '50–60', 'd': t('Burning Steppes, Western Plaguelands, Eastern Plaguelands, Winterspring, Silithus. На 60 открыта Mount Hyjal.',
                                              'Burning Steppes, Western and Eastern Plaguelands, Winterspring, Silithus. Mount Hyjal opens at 60.',
                                              'Burning Steppes, Western і Eastern Plaguelands, Winterspring, Silithus. На 60 відкритий Mount Hyjal.')},
                    ]),
                ]},
                {'id': 'horde', 't': t('Орда', 'Horde', 'Орда'), 'blocks': [
                    ('steps', [
                        {'t': '1–10', 'd': t('Орки и тролли: Durotar. Таурены: Mulgore. Нежить: Tirisfal Glades. Скайборны-ветрорезы: Zephras Isle, до 12.',
                                             'Orc and Troll: Durotar. Tauren: Mulgore. Undead: Tirisfal Glades. Windshaper Skyborne: Zephras Isle (to 12).',
                                             'Orc і Troll: Durotar. Tauren: Mulgore. Undead: Tirisfal Glades. Windshaper Skyborne: Zephras Isle (до 12).')},
                        {'t': '10–18', 'd': t('The Barrens или Silverpine Forest.', 'The Barrens or Silverpine Forest.', 'The Barrens або Silverpine Forest.')},
                        {'t': '18–30', 'd': t('Stonetalon Mountains и The Barrens, затем Ashenvale или Hillsbrad Foothills, с 25 Thousand Needles.',
                                              'Stonetalon Mountains and The Barrens, then Ashenvale or Hillsbrad Foothills, from 25 Thousand Needles.',
                                              'Stonetalon Mountains і The Barrens, далі Ashenvale або Hillsbrad Foothills, з 25 Thousand Needles.')},
                        {'t': '30–45', 'd': t('Desolace или Arathi Highlands, Stranglethorn Vale. С 35: новая зона Riverglades, Dustwallow Marsh, Badlands, Swamp of Sorrows.',
                                              'Desolace or Arathi Highlands, Stranglethorn Vale. From 35: the new Riverglades zone, Dustwallow Marsh, Badlands, Swamp of Sorrows.',
                                              'Desolace або Arathi Highlands, Stranglethorn Vale. З 35: нова зона Riverglades, Dustwallow Marsh, Badlands, Swamp of Sorrows.')},
                        {'t': '40–55', 'd': t('Tanaris, Feralas, The Hinterlands, затем Searing Gorge, Blasted Lands, Azshara, с 48 [[Кратер Ун’Горо|Un’Goro Crater]] и Felwood.',
                                              'Tanaris, Feralas, The Hinterlands, then Searing Gorge, Blasted Lands, Azshara, from 48 Un’Goro Crater and Felwood.',
                                              'Tanaris, Feralas, The Hinterlands, далі Searing Gorge, Blasted Lands, Azshara, з 48 Un’Goro Crater і Felwood.')},
                        {'t': '50–60', 'd': t('Burning Steppes, Western Plaguelands, Eastern Plaguelands, Winterspring, Silithus. На 60 открыта Mount Hyjal.',
                                              'Burning Steppes, Western and Eastern Plaguelands, Winterspring, Silithus. Mount Hyjal opens at 60.',
                                              'Burning Steppes, Western і Eastern Plaguelands, Winterspring, Silithus. На 60 відкритий Mount Hyjal.')},
                    ]),
                ]},
            ]),
            ('tip', t('Новая зона Shen’Dralas лежит между [[Пустошами|Desolace]] и [[Фераласом|Feralas]], в ней задания для [[Мародона|Maraudon]] и [[Курганов Иглошкурых|Razorfen Downs]]. Уровень зоны источники пока не называют.',
                      'The new Shen’Dralas zone lies between Desolace and Feralas and has quests for Maraudon and Razorfen Downs. Sources do not give its level yet.',
                      'Нова зона Shen’Dralas лежить між Desolace і Feralas, у ній завдання для Maraudon і Razorfen Downs. Рівень зони джерела поки не називають.')),
        ]},
        {'id': 'pace', 'title': t('Темп и отдых', 'Pace and rest', 'Темп і відпочинок'), 'blocks': [
            ('steps', [
                {'t': t('Сколько опыта', 'How much experience', 'Скільки досвіду'),
                 'd': t('До 60 уровня нужно 4 084 700 опыта: 499 000 до 30 и 2 306 100 до 50.',
                        'Reaching level 60 takes 4,084,700 experience: 499,000 to 30 and 2,306,100 to 50.',
                        'До 60 рівня потрібно 4 084 700 досвіду: 499 000 до 30 і 2 306 100 до 50.')},
                {'t': t('Отдых', 'Rested XP', 'Відпочинок'),
                 'd': t('Отдых удваивает опыт за врагов, на задания он не действует. В таверне или столице копится 5% уровня за 8 часов, потолок 150% (около 10 дней вне игры).',
                        'Rested XP doubles experience from enemies and does not affect quests. In an inn or capital it builds 5% of a level per 8 hours, capped at 150% (about 10 days offline).',
                        'Відпочинок подвоює досвід за ворогів, на завдання він не діє. У таверні чи столиці накопичується 5% рівня за 8 годин, стеля 150% (близько 10 днів поза грою).')},
                {'t': t('Еда и спальник', 'Food and bedroll', 'Їжа і спальник'),
                 'd': t('Большая часть готовой еды даёт +5% опыта за врагов примерно на 15 минут. Cozy Sleeping Bag даёт до 3% и не пропадает после смерти, а лёжа на нём копится отдых даже вне игры.',
                        'Most cooked food gives +5% experience from enemies for about 15 minutes. The Cozy Sleeping Bag gives up to 3% and stays after death, and lying on it builds rest even while offline.',
                        'Більша частина готової їжі дає +5% досвіду за ворогів приблизно на 15 хвилин. Cozy Sleeping Bag дає до 3% і не зникає після смерті, а лежачи на ньому накопичується відпочинок навіть поза грою.')},
                {'t': t('Задания по уровню', 'Quests at your level', 'Завдання за рівнем'),
                 'd': t('Задания на 5 и больше уровней ниже теряют по 10–20% опыта за каждый лишний уровень, серые враги опыта не дают.',
                        'Quests 5 or more levels below you lose 10–20% experience per extra level, grey enemies give no experience.',
                        'Завдання на 5 і більше рівнів нижче втрачають по 10–20% досвіду за кожен зайвий рівень, сірі вороги досвіду не дають.')},
                {'t': t('Ездовое животное', 'Riding', 'Їздова тварина'),
                 'd': t('С 40 уровня: обучение 100 золотых и скакун 20 (скорость +60%). На 60: 1000 и 200 золотых (+100%). При Honored со своей фракцией скидка 10%. Паладин и Чернокнижник получают скакуна заданиями класса.',
                        'From level 40: training 100 gold and a mount 20 (+60% speed). At 60: 1,000 and 200 gold (+100%). Honored with your faction gives 10% off. Paladins and Warlocks get their mount through class quests.',
                        'З 40 рівня: навчання 100 золотих і скакун 20 (швидкість +60%). На 60: 1000 і 200 золотих (+100%). На Honored зі своєю фракцією знижка 10%. Паладин і Чорнокнижник отримують скакуна завданнями класу.')},
            ]),
            ('tip', t('Выходите из игры в таверне, столице или на спальнике: следующий вечер начнётся с двойного опыта за врагов. Еда, спальник и отдых складываются.',
                      'Log out in an inn, a capital or on the bedroll: the next evening starts with double experience from enemies. Food, the bedroll and rest stack.',
                      'Виходьте з гри в таверні, столиці або на спальнику: наступний вечір почнеться з подвійного досвіду за ворогів. Їжа, спальник і відпочинок складаються.')),
        ]},
        {'id': 'group', 'title': t('Соло, вдвоём или группой', 'Solo, duo or group', 'Соло, удвох чи групою'), 'blocks': [
            ('tabs', [
                {'id': 'solo', 't': t('Соло', 'Solo', 'Соло'), 'blocks': [
                    ('text', [t('Основа прокачки — задания: их опыт не зависит от группы. Отдых работает только на врагов, поэтому начинайте вечер с убийств, пока он есть.',
                                'Quests are the core of leveling: their experience does not depend on a group. Rest only works on enemies, so start the evening with kills while you have it.',
                                'Основа прокачування — завдання: їхній досвід не залежить від групи. Відпочинок працює лише на ворогів, тому починайте вечір із вбивств, поки він є.')]),
                    ('tip', t('Легче всего соло Охотнику и Чернокнижнику, у них питомец держит врага.',
                              'Hunters and Warlocks have the easiest time solo, their pet holds the enemy.',
                              'Найлегше соло Мисливцю й Чорнокнижнику, у них вихованець тримає ворога.')),
                ]},
                {'id': 'duo', 't': t('Вдвоём', 'Duo', 'Удвох'), 'blocks': [
                    ('text', [t('За сданное задание каждый получает полный опыт, а опыт за врагов делится. Держите уровни рядом: в Forever у игрока выше уровнем штраф к опыту в группе больше, а «протаскивать» друга Blizzard сделала невыгодным.',
                                'Each player gets full experience for a quest turn-in, while experience from enemies is shared. Keep your levels close: in Forever a higher-level group member gets a bigger experience penalty, and Blizzard made boosting a friend unprofitable.',
                                'За здане завдання кожен отримує повний досвід, а досвід за ворогів ділиться. Тримайте рівні поруч: у Forever у гравця з вищим рівнем штраф до досвіду в групі більший, а «протягувати» друга Blizzard зробила невигідним.')]),
                    ('tip', t('Берите задания вместе и сдавайте одновременно. Если один ушёл вперёд, пусть отстающий доберёт уровень соло.',
                              'Pick up quests together and turn them in at the same time. If one of you gets ahead, let the other catch up solo.',
                              'Беріть завдання разом і здавайте одночасно. Якщо один пішов уперед, нехай відсталий добере рівень соло.')),
                ]},
                {'id': 'party', 't': t('Группой', 'Group', 'Групою'), 'blocks': [
                    ('text', [t('Чем больше группа, тем меньше опыта за врага достаётся каждому, а задания по-прежнему дают полный опыт. Большой группой выгодно ходить в подземелья и на элитные задания, а между ними разбиваться на пары.',
                                'The bigger the group, the less experience each member gets per enemy, while quests still give full experience. A big group pays off in dungeons and on elite quests, and between them you can split into pairs.',
                                'Що більша група, то менше досвіду за ворога дістається кожному, а завдання й далі дають повний досвід. Великою групою вигідно ходити в підземелля та на елітні завдання, а між ними розбиватися на пари.')]),
                    ('tiles', [{'t': t('Подземелья и рейды', 'Dungeons and raids', 'Підземелля та рейди'),
                                'd': t('Какое подземелье под ваш уровень и кого взять в группу', 'Which dungeon fits your level and who to bring',
                                       'Яке підземелля під ваш рівень і кого взяти в групу'),
                                'href': 'guides/dungeons/', 'art': 'warlock'}]),
                ]},
            ]),
        ]},
        {'id': 'legacy', 'title': t('Система Legacy', 'Legacy system', 'Система Legacy'), 'blocks': [
            ('text', [t('Прогресс на весь аккаунт Battle.net. Очки получают за испытания, а тратят на перки отдельно на каждом персонаже.',
                        'Progress for the whole Battle.net account. Points are earned from challenges and spent on perks separately on each character.',
                        'Прогрес на весь акаунт Battle.net. Очки отримують за випробування, а витрачають на перки окремо на кожному персонажі.')]),
            ('steps', [
                {'t': t('Первое очко', 'First point', 'Перше очко'),
                 'd': t('Система открывается с первым очком: уровень 25 на персонаже, либо 150 в профессии (не сбор), либо исследование всей карты.',
                        'The system unlocks with the first point: level 25 on a character, or 150 in a profession (not gathering), or exploring the whole map.',
                        'Система відкривається з першим очком: 25 рівень на персонажі, або 150 у професії (не збирання), або дослідження всієї мапи.')},
                {'t': t('Испытания', 'Challenges', 'Випробування'),
                 'd': t('Каждое испытание даёт 1 очко. По данным Blizzard испытаний 65 в шести категориях: классы 27, профессии 18, PvP 12, подземелья 3, рейды 3, приключения 2.',
                        'Each challenge gives 1 point. According to Blizzard there are 65 challenges in six categories: classes 27, professions 18, PvP 12, dungeons 3, raids 3, adventures 2.',
                        'Кожне випробування дає 1 очко. За даними Blizzard випробувань 65 у шести категоріях: класи 27, професії 18, PvP 12, підземелля 3, рейди 3, пригоди 2.')},
                {'t': t('На весь аккаунт', 'Account-wide', 'На весь акаунт'),
                 'd': t('Очки действуют на всех персонажах не-Hardcore. Горячая клавиша окна: Y.', 'Points apply to all non-Hardcore characters. Window hotkey: Y.',
                        'Очки діють на всіх персонажах не-Hardcore. Гаряча клавіша вікна: Y.')},
                {'t': t('Лимит на запуске', 'Limit at launch', 'Ліміт на запуску'),
                 'd': t('На персонаже можно потратить не более 16 очков. Лишние идут в трек наград.', 'You can spend no more than 16 points on a character. The excess goes to the rewards track.',
                        'На персонажі можна витратити не більше 16 очок. Зайві йдуть у трек нагород.')},
            ]),
            ('table', {'head': [t('Дерево', 'Tree', 'Дерево'), t('Примеры перков (рангов)', 'Example perks (ranks)', 'Приклади перків (рангів)')], 'rows': [
                [t('Профессии', 'Professions', 'Професії'),
                 t('Working Overtime (5): чаще растут навыки. Bountiful Harvest (5): на 20% больше редких материалов. Master Chef (5): шанс лишнего блюда. Bartering (2): цены у торговцев ниже на 5%.',
                   'Working Overtime (5): skills increase faster. Bountiful Harvest (5): 20% more rare materials. Master Chef (5): chance of an extra dish. Bartering (2): vendor prices are 5% lower.',
                   'Working Overtime (5): частіше ростуть навички. Bountiful Harvest (5): на 20% більше рідкісних матеріалів. Master Chef (5): шанс зайвої страви. Bartering (2): ціни в торговців нижчі на 5%.')],
                [t('Приключения', 'Adventures', 'Пригоди'),
                 t('Well Rested (5): быстрее копится отдых и выше его потолок. Thrill of Adventure (5): здоровье и мана за убийство вне подземелий. Talented (5): таланты с 9 уровня вместо 10. Field Guide (3): короче откат объектов лагеря. Frequent Flier (1): перелёты на 50% дешевле.',
                   'Well Rested (5): rest accumulates faster and its cap is higher. Thrill of Adventure (5): health and mana for kills outside dungeons. Talented (5): talents from level 9 instead of 10. Field Guide (3): shorter cooldown of camp objects. Frequent Flier (1): flights are 50% cheaper.',
                   'Well Rested (5): швидше накопичується відпочинок і вища його стеля. Thrill of Adventure (5): здоров’я та мана за вбивство поза підземеллями. Talented (5): таланти з 9 рівня замість 10. Field Guide (3): коротше відновлення об’єктів табору. Frequent Flier (1): перельоти на 50% дешевші.')],
                [t('Ресурсы', 'Resources', 'Ресурси'),
                 t('Gourmand (3): еда действует на 33% дольше. Reinforce (5): на 8% меньше потеря прочности. Diplomat (5): +2% репутации. Permanence (2): дольше баффы лагеря. Reagent Economy (1): способностям класса не нужны покупные реагенты.',
                   'Gourmand (3): food lasts 33% longer. Reinforce (5): 8% less durability loss. Diplomat (5): +2% reputation. Permanence (2): camp buffs last longer. Reagent Economy (1): class abilities need no purchased reagents.',
                   'Gourmand (3): їжа діє на 33% довше. Reinforce (5): на 8% менше втрата міцності. Diplomat (5): +2% репутації. Permanence (2): довше баффи табору. Reagent Economy (1): здібностям класу не потрібні куповані реагенти.')],
            ]}),
            ('table', {'head': [t('Очки', 'Points', 'Очки'), t('Награда трека', 'Track reward', 'Нагорода треку')], 'rows': [
                ['15', t('игрушка Holstered Replica Ironforge Air Rifle', 'toy Holstered Replica Ironforge Air Rifle', 'іграшка Holstered Replica Ironforge Air Rifle')],
                ['25', t('питомец Spectral Bear Cub', 'pet Spectral Bear Cub', 'улюбленець Spectral Bear Cub')],
                ['40', t('табард Spectral Bear', 'tabard Spectral Bear', 'табард Spectral Bear')],
                ['55', t('скакун Reins of the Spectral Bear', 'mount Reins of the Spectral Bear', 'скакун Reins of the Spectral Bear')],
            ]}),
            ('text', [t('Это косметика, преимуществ в игре она не даёт.', 'These are cosmetics and give no advantage in the game.', 'Це косметика, переваг у грі вона не дає.')]),
            ('tip', t('В первую очередь ценны перки лагеря и опыта (Well Rested, Field Guide, Permanence) и Reagent Economy для классов с реагентами. Один источник пишет про лимит 25 очков на дерево, Blizzard лимита на дерево не называет.',
                      'Camp and experience perks come first (Well Rested, Field Guide, Permanence), plus Reagent Economy for classes that use reagents. One source mentions a 25-point cap per tree, Blizzard names no per-tree cap.',
                      'Насамперед цінні перки табору й досвіду (Well Rested, Field Guide, Permanence) і Reagent Economy для класів із реагентами. Одне джерело пише про ліміт 25 очок на дерево, Blizzard ліміту на дерево не називає.')),
        ]},
        {'id': 'camp', 'title': t('Лагерь и профессии', 'Camp and professions', 'Табір і професії'), 'blocks': [
            ('text', [t('Костёр по профессии Кулинария превращается в общий лагерь: рядом можно отдыхать, получать баффы и ставить объекты своих профессий.',
                        'A campfire made with the Cooking profession becomes a shared camp: you can rest nearby, get buffs and place objects of your professions.',
                        'Вогнище за професією Кулінарія перетворюється на спільний табір: поруч можна відпочивати, отримувати баффи та ставити об’єкти своїх професій.')]),
            ('steps', [
                {'t': t('Костёр', 'Campfire', 'Вогнище'),
                 'd': t('Костёр одноразовый: строится несколько секунд, горит около 10 минут, откат на постановку 5 минут.',
                        'The campfire is single-use: it takes a few seconds to build, burns for about 10 minutes, with a 5 minute cooldown to place.',
                        'Вогнище одноразове: будується кілька секунд, горить близько 10 хвилин, відновлення на встановлення 5 хвилин.')},
                {'t': t('Слоты', 'Slots', 'Слоти'),
                 'd': t('Базовый костёр доступен без Кулинарии, на 3 объекта. Кулинария 140 даёт 5 слотов, 220 даёт 10.',
                        'A basic campfire is available without Cooking, with 3 objects. Cooking 140 gives 5 slots, 220 gives 10.',
                        'Базове вогнище доступне без Кулінарії, на 3 об’єкти. Кулінарія 140 дає 5 слотів, 220 дає 10.')},
                {'t': t('Общий лагерь', 'Shared camp', 'Спільний табір'),
                 'd': t('Каждый персонаж ставит один объект, откат на объект 1 час. Вместе делают общий лагерь.',
                        'Each character places one object, with a 1 hour cooldown per object. Together you make a shared camp.',
                        'Кожен персонаж ставить один об’єкт, відновлення на об’єкт 1 година. Разом роблять спільний табір.')},
                {'t': t('Баффы', 'Buffs', 'Баффи'),
                 'd': t('Чтобы получить баффы, сядьте (/sit) рядом минимум на 1 минуту. Они суммируются в один бафф «Camp Benefits». Баффы лагеря немного слабее классовых и не складываются с ними.',
                        'To get the buffs, sit (/sit) nearby for at least 1 minute. They stack into one buff, “Camp Benefits”. Camp buffs are slightly weaker than class buffs and do not stack with them.',
                        'Щоб отримати баффи, сядьте (/sit) поруч щонайменше на 1 хвилину. Вони підсумовуються в один бафф «Camp Benefits». Баффи табору трохи слабші за класові й не складаються з ними.')},
            ]),
            ('table', {'head': [t('Профессия', 'Profession', 'Професія'), t('Объект (1 уровень)', 'Object (level 1)', 'Об’єкт (1 рівень)'), t('Эффект', 'Effect', 'Ефект')], 'rows': [
                [t('Алхимия', 'Alchemy', 'Алхімія'), 'Mana Well', t('больше восстановление маны', 'more mana regeneration', 'більше відновлення мани')],
                [t('Кузнечное дело', 'Blacksmithing', 'Ковальство'), 'Sharpening Wheel', t('больше силы', 'more strength', 'більше сили')],
                [t('Наложение чар', 'Enchanting', 'Зачарування'), 'Enchanted Lute', t('больше основных характеристик и сопротивлений', 'more primary stats and resistances', 'більше основних характеристик і опорів')],
                [t('Первая помощь', 'First Aid', 'Перша допомога'), 'First Aid Kit', t('больше выносливости', 'more stamina', 'більше витривалості')],
                [t('Рыбалка', 'Fishing', 'Рибальство'), 'Fish Bowl', t('больше основных характеристик', 'more primary stats', 'більше основних характеристик')],
                [t('Травничество', 'Herbalism', 'Травництво'), 'Incense Candle', t('больше интеллекта', 'more intellect', 'більше інтелекту')],
                [t('Кожевничество', 'Leatherworking', 'Шкіряництво'), 'Camp Tent', t('отдых и опыт (Boosted Rest)', 'rest and experience (Boosted Rest)', 'відпочинок і досвід (Boosted Rest)')],
                [t('Горное дело', 'Mining', 'Гірництво'), 'Lodestone', t('больше силы атаки', 'more attack power', 'більше сили атаки')],
                [t('Снятие шкур', 'Skinning', 'Знімання шкур'), 'Camp Chair', t('больше шанс критического удара', 'higher critical strike chance', 'більший шанс критичного удару')],
                [t('Портняжное дело', 'Tailoring', 'Кравецтво'), 'Faction Banner', t('больше духа', 'more spirit', 'більше духу')],
                [t('Инженерия', 'Engineering', 'Інженерія'), 'Reagent Bot', t('торговец, во 2 уровне ремонт (Repair Bot)', 'a vendor, at level 2 repairs (Repair Bot)', 'торговець, на 2 рівні ремонт (Repair Bot)')],
                [t('Кулинария', 'Cooking', 'Кулінарія'), 'Basic Campfire', t('без баффа, добавляет слоты лагеря', 'no buff, adds camp slots', 'без баффа, додає слоти табору')],
            ]}),
            ('text', [t('Каждая профессия делает по три объекта, по одному на уровень. Источники расходятся в навыке для объектов 2 и 3 уровня (один пишет 140 и 300), поэтому сверяйте в игре.',
                        'Each profession makes three objects, one per level. Sources disagree on the skill needed for level 2 and 3 objects (one says 140 and 300), so check in the game.',
                        'Кожна професія робить по три об’єкти, по одному на рівень. Джерела розходяться в навичці для об’єктів 2 і 3 рівня (одне пише 140 і 300), тому звіряйте в грі.')]),
            ('tip', t('Палатка Camp Tent от кожевника даёт отдых, как в таверне, на час и не пропадает после смерти. Перки Legacy Field Guide, Permanence и Reagent Economy улучшают лагерь.',
                      'The leatherworker’s Camp Tent gives rest like an inn for an hour and stays after death. The Legacy perks Field Guide, Permanence and Reagent Economy improve the camp.',
                      'Намет Camp Tent від шкіряника дає відпочинок, як у таверні, на годину й не зникає після смерті. Перки Legacy Field Guide, Permanence і Reagent Economy покращують табір.')),
        ]},
    ],
})

# ---------- Профессии ----------

# Пары по Warcraft Tavern («Best for»); у класса своя причина там, где её даёт content/classes.py
PAIRS = {
    'bs': (t('Кузнечное дело + Горное дело', 'Blacksmithing + Mining', 'Ковальство + Гірництво'),
           t('Для латников и ближнего боя: оружие и доспехи себе сами.', 'For plate wearers and melee: make your own weapons and armor.',
             'Для латників і ближнього бою: зброя та обладунки собі самі.')),
    'eng': (t('Инженерия + Горное дело', 'Engineering + Mining', 'Інженерія + Гірництво'),
            t('Для PvP, полезных устройств и веселья. В лагере Reagent Bot продаёт реагенты, на 2 уровне чинит экипировку.',
              'For PvP, useful gadgets and fun. In camp the Reagent Bot sells reagents and repairs gear at tier 2.',
              'Для PvP, корисних пристроїв і розваги. У таборі Reagent Bot продає реагенти, на 2 рівні лагодить спорядження.')),
    'lw': (t('Кожевничество + Снятие шкур', 'Leatherworking + Skinning', 'Шкіряництво + Знімання шкур'),
           t('Для тех, кто носит кожу и кольчугу. Кожевник ставит в лагере Camp Tent, она даёт отдых.',
             'For leather and mail wearers. A leatherworker places the Camp Tent in camp, which gives rest.',
             'Для тих, хто носить шкіру й кольчугу. Шкіряник ставить у таборі Camp Tent, він дає відпочинок.')),
    'tail': (t('Портняжное дело + Наложение чар', 'Tailoring + Enchanting', 'Кравецтво + Зачарування'),
             t('Для тех, кто носит ткань, и заклинателей.', 'For cloth wearers and spellcasters.', 'Для тих, хто носить тканину, і заклинателів.')),
    'alch': (t('Алхимия + Травничество', 'Alchemy + Herbalism', 'Алхімія + Травництво'),
             t('Зелья для себя и группы и заработок золота. Подходит любому классу.', 'Potions for yourself and the group, and gold making. Fits any class.',
               'Зілля для себе й групи та заробіток золота. Підходить будь-якому класу.')),
}
CLASS_PAIRS = [   # (id, имя класса, [(пара, своя причина или None), …])
    ('warrior', t('Воин', 'Warrior', 'Воїн'), [('bs', None), ('eng', None)]),
    ('paladin', t('Паладин', 'Paladin', 'Паладин'), [('bs', None), ('alch', None)]),
    ('hunter', t('Охотник', 'Hunter', 'Мисливець'), [('lw', None), ('eng', t('Инженер делает себе ружья и патроны.', 'An engineer makes their own guns and ammo.',
                                                                        'Інженер робить собі рушниці й набої.'))]),
    ('rogue', t('Разбойник', 'Rogue', 'Розбійник'), [('lw', None), ('eng', None)]),
    ('priest', t('Жрец', 'Priest', 'Жрець'), [('tail', None), ('alch', None)]),
    ('shaman', t('Шаман', 'Shaman', 'Шаман'), [('lw', None), ('alch', None)]),
    ('mage', t('Маг', 'Mage', 'Маг'), [('tail', None), ('alch', None)]),
    ('warlock', t('Чернокнижник', 'Warlock', 'Чорнокнижник'), [('tail', t('Знамя Faction Banner от портного даёт дух для [[Жизнеотвода|Life Tap]].', 'The tailor’s Faction Banner gives Spirit for Life Tap.',
                                                                           'Прапор Faction Banner від кравця дає дух для Life Tap.')), ('alch', None)]),
    ('druid', t('Друид', 'Druid', 'Друїд'), [('alch', t('Травы друид собирает прямо в облике путешествия.', 'A druid gathers herbs right in Travel Form.',
                                                     'Трави друїд збирає просто в подобі подорожі.')), ('lw', None)]),
]


def _pair_tabs():
    return [{'id': cid, 't': name, 'blocks': [('steps', [{'t': PAIRS[p][0], 'd': why or PAIRS[p][1]} for p, why in pairs])]}
            for cid, name, pairs in CLASS_PAIRS]


GUIDES.append({
    'slug': 'professions', 'art': 'hero_campfire', 'updated': '23.10.2026', 'js': 'professions',
    'title': t('Профессии', 'Professions', 'Професії'),
    'lead': t('Какие две профессии взять под ваш класс, что каждая ставит в лагерь и как прокачать навык до 300.',
              'Which two professions suit your class, what each one places in camp and how to raise the skill to 300.',
              'Які дві професії взяти під ваш клас, що кожна ставить у табір і як прокачати навичку до 300.'),
    'tile': t('Пары под класс, объекты лагеря, навык до 300', 'Pairs for your class, camp objects, skill to 300', 'Пари під клас, об’єкти табору, навичка до 300'),
    'pills': [t('2 основные + 3 вспомогательные', '2 primary + 3 secondary', '2 основні + 3 допоміжні'), t('Навык до 300', 'Skill to 300', 'Навичка до 300'),
              t('12 объектов лагеря', '12 camp objects', '12 об’єктів табору')],
    'sources': [
        (t('Warcraft Tavern: профессии', 'Warcraft Tavern: professions', 'Warcraft Tavern: професії'), 'https://www.warcrafttavern.com/forever/guides/professions/'),
        (t('Warcraft Tavern: объекты и баффы лагеря', 'Warcraft Tavern: camp objects and buffs', 'Warcraft Tavern: об’єкти та баффи табору'),
         'https://www.warcrafttavern.com/forever/guides/camping-objects-buffs/'),
        (t('Warcraft Tavern: лагерь', 'Warcraft Tavern: camping', 'Warcraft Tavern: табір'), 'https://www.warcrafttavern.com/forever/guides/camping/'),
    ],
    'sections': [
        {'id': 'pairs', 'title': t('Пары под класс', 'Pairs for your class', 'Пари під клас'), 'blocks': [
            ('text', [t('Основных профессий у персонажа две. Обычно ремесло берут вместе с подходящим сбором, чтобы добывать материалы самому. Если вы заполнили «Мой персонаж» на главной, сразу откроется ваш класс.',
                        'A character has two primary professions. A craft is usually paired with its matching gathering profession so you collect materials yourself. If you filled in “My hero” on the home page, your class opens right away.',
                        'Основних професій у персонажа дві. Зазвичай ремесло беруть разом із відповідним збиранням, щоб добувати матеріали самому. Якщо ви заповнили «Мій персонаж» на головній, одразу відкриється ваш клас.')]),
            ('tabs', _pair_tabs()),
            ('tip', t('Кулинарию, Первую помощь и Рыбалку берут все: это вспомогательные профессии, их может быть все три сразу, и разучить их нельзя. Пусть кто-то в группе поднимет Кулинарию до 220 ради 10 мест в лагере.',
                      'Everyone takes Cooking, First Aid and Fishing: they are secondary professions, you can have all three and they cannot be unlearned. Let someone in the group raise Cooking to 220 for 10 camp slots.',
                      'Кулінарію, Першу допомогу та Рибальство беруть усі: це допоміжні професії, їх може бути всі три одразу, і розучити їх не можна. Нехай хтось у групі підніме Кулінарію до 220 заради 10 місць у таборі.')),
        ]},
        {'id': 'camp', 'title': t('Объекты лагеря', 'Camp objects', 'Об’єкти табору'), 'blocks': [
            ('text', [t('У каждой профессии три объекта лагеря, по одному на уровень. Ниже объект первого уровня и бафф класса, на который похож его эффект.',
                        'Each profession has three camp objects, one per tier. Below is the tier 1 object and the class buff its effect resembles.',
                        'Кожна професія має три об’єкти табору, по одному на рівень. Нижче об’єкт першого рівня та бафф класу, на який схожий його ефект.')]),
            ('profs', None),
            ('tip', t('Баффы лагеря немного слабее классовых и не складываются с ними: Благословение королей даёт 10% ко всем характеристикам, а Fish Bowl в лагере 8%. Ставьте объекты, которых нет у классов вашей группы.',
                      'Camp buffs are slightly weaker than class buffs and do not stack with them: Blessing of Kings gives 10% to all stats, the camp Fish Bowl 8%. Place objects whose buffs no class in your group provides.',
                      'Баффи табору трохи слабші за класові й не складаються з ними: Благословення королів дає 10% до всіх характеристик, а Fish Bowl у таборі 8%. Ставте об’єкти, яких немає в класів вашої групи.')),
        ]},
        {'id': 'leveling', 'title': t('Прокачка навыка', 'Raising your skill', 'Прокачування навички'), 'blocks': [
            ('table', {'head': [t('Ступень', 'Rank', 'Ступінь'), t('С уровня героя', 'From hero level', 'З рівня героя'), t('Навык до', 'Skill up to', 'Навичка до')], 'rows': [
                ['Apprentice', t('1 для сбора, 5 для ремёсел', '1 for gathering, 5 for crafts', '1 для збирання, 5 для ремесел'), '75'],
                ['Journeyman', '10', '150'],
                ['Expert', '20', '225'],
                ['Artisan', '35', '300'],
            ]}),
            ('steps', [
                {'t': t('Первое задание', 'First quest', 'Перше завдання'),
                 'd': t('Стартовое задание предлагает Горное дело, Снятие шкур или Травничество, учит профессии и сразу даёт 2 очка навыка.',
                        'A starter quest offers Mining, Skinning or Herbalism, teaches the profession and gives 2 skill points right away.',
                        'Стартове завдання пропонує Гірництво, Знімання шкур або Травництво, вчить професії й одразу дає 2 очки навички.')},
                {'t': t('Цвет рецепта', 'Recipe colour', 'Колір рецепта'),
                 'd': t('Оранжевые рецепты и залежи всегда дают очко, жёлтые часто, зелёные редко, серые никогда.',
                        'Orange recipes and nodes always give a point, yellow often, green rarely, grey never.',
                        'Помаранчеві рецепти й поклади завжди дають очко, жовті часто, зелені рідко, сірі ніколи.')},
                {'t': t('Artisan', 'Artisan', 'Artisan'),
                 'd': t('Ступень Artisan дают только особые учители, а для вспомогательных профессий особое задание.',
                        'Artisan comes only from special trainers, or from a special quest for secondary professions.',
                        'Ступінь Artisan дають лише особливі вчителі, а для допоміжних професій особливе завдання.')},
                {'t': t('Окно профессий', 'Professions window', 'Вікно професій'),
                 'd': t('Своё окно на клавише K: рецепты можно искать, фильтровать и отслеживать как список покупок. Для сумки с реагентами есть отдельный слот.',
                        'Its own window on the K key: recipes can be searched, filtered and tracked as a shopping list. Reagent bags have their own slot.',
                        'Своє вікно на клавіші K: рецепти можна шукати, фільтрувати й відстежувати як список покупок. Для сумки з реагентами є окремий слот.')},
            ]),
            ('tip', t('Разучив профессию, вы теряете весь её прогресс, а игра просит подтвердить это вводом слова. Пассивных бонусов у профессий в Forever нет: польза в том, что вы делаете и собираете, и в баффах лагеря.',
                      'Unlearning a profession wipes all its progress, and the game asks you to type a confirmation. Professions in Forever have no passive bonuses: the value is in what you craft and gather, and in camp buffs.',
                      'Розучивши професію, ви втрачаєте весь її прогрес, а гра просить підтвердити це введенням слова. Пасивних бонусів у професій у Forever немає: користь у тому, що ви робите й збираєте, і в баффах табору.')),
        ]},
    ],
})

# ---------- Новости: наши записи (новые сверху) + автолента Wowhead из assets/news.json ----------

NEWS += [
    {'date': '2026-10-23', 'url': 'https://teamoverpowered.com/forever/guides/name-reservation/',
     'title': t('Бета закрывается, следующий шаг — имена с 27.10', 'Beta closes, next up: names from 27.10', 'Бета закривається, наступний крок — імена з 27.10'),
     'text': t('Закрытая бета отключается 23.10 в 10:00 по тихоокеанскому времени (20:00 по Киеву). С 27.10 по 03.11 владельцы Heroic, Epic и Collection резервируют до трёх имён на аккаунт, кто первым пришёл, тот и занял.',
               'The closed beta goes offline on 23.10 at 10:00 Pacific time (20:00 in Kyiv). From 27.10 to 03.11 Heroic, Epic and Collection owners reserve up to three names per account, first come, first served.',
               'Закрита бета вимикається 23.10 о 10:00 за тихоокеанським часом (20:00 за Києвом). З 27.10 по 03.11 власники Heroic, Epic і Collection резервують до трьох імен на акаунт, хто перший прийшов, той і зайняв.')},
    {'date': '2026-10-15', 'url': 'https://www.warcrafttavern.com/forever/news/racial-class-ability-changes-in-the-wow-forever-beta/',
     'title': t('Крупный патч беты: расы и классы', 'Major beta patch: races and classes', 'Великий патч бети: раси та класи'),
     'text': t('Способности рас переделаны (оружейные специализации заменены критами), настроены почти все классы. Таблицы рас и классов на сайте уже по этому патчу.',
               'Racial abilities were reworked (weapon specializations replaced with crits), almost all classes were tuned. The race and class tables on this site already follow this patch.',
               'Здібності рас перероблено (спеціалізації зброї замінено критами), налаштовано майже всі класи. Таблиці рас і класів на сайті вже за цим патчем.')},
    {'date': '2026-10-08', 'url': 'https://classicwow.gg/forever',
     'title': t('В бете Даларан и больше опыта в подземельях', 'Dalaran and more dungeon experience in the beta', 'У беті Даларан і більше досвіду в підземеллях'),
     'text': t('В бету добавили City of Dalaran и примерно на 20% больше опыта за врагов в подземельях.',
               'The beta got City of Dalaran and about 20% more experience for enemies in dungeons.',
               'У бету додали City of Dalaran і приблизно на 20% більше досвіду за ворогів у підземеллях.')},
]

GUIDES.append({
    'slug': 'news', 'art': 'paladin', 'updated': '23.10.2026', 'js': 'news',
    'title': t('Новости', 'News', 'Новини'),
    'lead': t('Что важно для нашей игры в WoW Forever, и свежая лента Wowhead.',
              'What matters for our game in WoW Forever, plus the latest Wowhead feed.',
              'Що важливо для нашої гри у WoW Forever, і свіжа стрічка Wowhead.'),
    'tile': t('Наши записи и лента Wowhead', 'Our notes and the Wowhead feed', 'Наші записи та стрічка Wowhead'),
    'pills': [t('Лента обновляется каждые 6 часов', 'Feed updates every 6 hours', 'Стрічка оновлюється кожні 6 годин')],
    'sources': [
        ('Wowhead News', 'https://www.wowhead.com/news'),
        (t('Warcraft Tavern: изменения рас и классов', 'Warcraft Tavern: racial and class changes', 'Warcraft Tavern: зміни рас і класів'),
         'https://www.warcrafttavern.com/forever/news/racial-class-ability-changes-in-the-wow-forever-beta/'),
        ('ClassicWoW.gg', 'https://classicwow.gg/forever'),
        ('Team Overpowered', 'https://teamoverpowered.com/forever/guides/name-reservation/'),
    ],
    'sections': [
        {'id': 'ours', 'title': t('Наши записи', 'Our notes', 'Наші записи'), 'blocks': [('news', None)]},
        {'id': 'feed', 'title': t('Лента Wowhead', 'Wowhead feed', 'Стрічка Wowhead'), 'blocks': [
            ('text', [t('Новости про Forever с Wowhead, на английском. Список обновляется сам.',
                        'Forever news from Wowhead, in English. The list updates by itself.',
                        'Новини про Forever з Wowhead, англійською. Список оновлюється сам.')]),
            ('raw', t('<div class="nlist" id="feedList" hidden></div><p><a class="more-l" href="https://www.wowhead.com/news" target="_blank" rel="noopener">Все новости Wowhead</a></p>',
                      '<div class="nlist" id="feedList" hidden></div><p><a class="more-l" href="https://www.wowhead.com/news" target="_blank" rel="noopener">All Wowhead news</a></p>',
                      '<div class="nlist" id="feedList" hidden></div><p><a class="more-l" href="https://www.wowhead.com/news" target="_blank" rel="noopener">Усі новини Wowhead</a></p>')),
        ]},
    ],
})


# ---------- Як грати українською: только uk ('only'), тексты — словари {'uk': …} ----------

def u(s):
    return {'uk': s}


GUIDES.append({
    'slug': 'ukrainian', 'only': 'uk', 'art': 'priest', 'updated': '23.10.2026',
    'title': u('Як грати українською'),
    'lead': u('Української мови у WoW Forever немає. Порівняння аддонів UA_Forever і UALL Forever, встановлення та перегляд оригіналу.'),
    'tile': u('Аддони перекладу: який обрати й як встановити'),
    'pills': [u('UA_Forever'), u('UALL Forever'), u('Shift — оригінал')],
    'sources': [
        (u('CurseForge: UA_Forever'), 'https://www.curseforge.com/wow/addons/ua-forever'),
        (u('CurseForge: UALL Forever'), 'https://www.curseforge.com/wow/addons/uall-forever-ukrainian-localization'),
        (u('ClassicUA на GitHub'), 'https://github.com/greenya/ClassicUA'),
        (u('WoWGuide: мови WoW Forever'), 'https://wowguide.net/en/guides/wow-forever-supported-languages'),
    ],
    'sections': [
        {'id': 'client', 'title': u('Мова клієнта'), 'blocks': [
            ('text', [u('Клієнт WoW Forever доступний десятьма мовами, серед них англійська та російська. Української серед них немає.'),
                      u('Українською грають з аддоном: він підміняє тексти завдань, підказок і вікон поверх клієнта. Аддони неофіційні, їх роблять гравці, тож після патчів переклад може відставати.')]),
        ]},
        {'id': 'choose', 'title': u('Який аддон обрати'), 'blocks': [
            ('table', {'head': [u(''), u('UA_Forever'), u('UALL Forever')], 'rows': [
                [u('Основа'), u('Переклад спільноти ClassicUA, ведеться з 2021 року'), u('Власний переклад')],
                [u('Завдання'), '6209', '4389'],
                [u('Предмети'), '24 025', '6097'],
                [u('Заклинання'), '32 939', '29 743'],
                [u('Рід героя'), u('«дав» або «дала» за статтю персонажа'), u('Завжди чоловічий рід')],
                [u('Назви'), u('Перекладені: Залізогарт, Підмістя'), u('Транслітерація: Айронфордж, Андерсіті')],
                [u('Оригінал'), u('Shift у підказці, EN/UA у діалогах завдань'), u('Shift')],
                [u('Клієнт'), u('Клієнт Forever'), u('Лише англійський')],
                [u('Версія'), u('0.22.0 від 22.10.2026'), u('1.0.10 від 13.10.2026')],
            ]}),
            ('text', [u('Обирайте UA_Forever. Перекладено більше, назви українською, речення узгоджені з родом героя. Слабкі місця: місцями дослівний текст і поодинокі помилки.'),
                      u('UALL Forever читається рівніше, але назви в ньому транслітом, а предметів перекладено вчетверо менше.')]),
            ('tip', u('На цьому сайті ігрові назви англійською, як в оригінальному клієнті. Так їх пишуть Wowhead, гайди й гравці в групі. Затисніть Shift на підказці, щоб звірити назву.')),
        ]},
        {'id': 'install', 'title': u('Встановлення'), 'blocks': [
            ('steps', [
                {'t': u('CurseForge'), 'd': u('У застосунку CurseForge оберіть World of Warcraft і версію Forever, знайдіть аддон і натисніть Install.')},
                {'t': u('Або вручну'), 'd': u('Завантажте архів зі сторінки аддона й розпакуйте папку в Interface\\AddOns у теці гри Forever. У беті це була тека _classic_beta_.')},
                {'t': u('Увімкнення'), 'd': u('На екрані вибору персонажа відкрийте AddOns і поставте позначку. Якщо аддон позначено застарілим, увімкніть Load out of date AddOns.')},
                {'t': u('Перезавантаження'), 'd': u('Якщо гра вже запущена, введіть /reload у чаті.')},
            ]),
            ('tip', u('Вмикайте один аддон перекладу. Обидва підміняють ті самі вікна.')),
        ]},
        {'id': 'original', 'title': u('Оригінал англійською'), 'blocks': [
            ('text', [u('UA_Forever: затисніть Shift, і підказка покаже англійський текст. У діалогах завдань є перемикач EN/UA. Окремі частини перекладу вимикаються в налаштуваннях аддона.'),
                      u('UALL Forever: Shift показує англійський текст. /uallfua виводить стан перекладу, /uallfua list — частини, які можна вимкнути. Ті самі перемикачі: Esc → Options → AddOns → UALLF.')]),
        ]},
    ],
})

GUIDES.sort(key=lambda g: ORDER.index(g['slug']))


# ---------- Разделы /classes/ и /races/: таблицы сравнения с главной (JS — из index.src.html, ref:start…ref:end) ----------

HUBS = [
    {'slug': 'classes', 'path': 'classes/', 'art': 'warrior', 'js': 'classref', 'updated': '23.10.2026',
     'title': t('Классы', 'Classes', 'Класи'),
     'lead': t('Девять классов по три специализации: роли, темп прокачки и польза в рейде в одной таблице.',
               'Nine classes, three specs each: roles, leveling pace and raid value in one table.',
               'Дев’ять класів по три спеціалізації: ролі, темп прокачки та користь у рейді в одній таблиці.'),
     'tile': t('Сравнение всех классов', 'All classes compared', 'Порівняння всіх класів'),
     'sources': [('Warcraft Tavern', 'https://www.warcrafttavern.com/forever/guides/classes/'),
                 ('LFCarry', 'https://lfcarry.com/guides/wow-forever-classes')],
     'sections': [{'id': 'compare', 'title': t('Сравнение', 'Comparison', 'Порівняння'), 'blocks': [
         ('text', [t('Темп прокачки взят из прогнозов по бете: в бете был потолок 30 уровня, выше оценки проектные. Строка открывает страницу класса.',
                     'Leveling pace comes from beta projections: the beta was capped at level 30, figures above that are estimates. A row opens the class page.',
                     'Темп прокачки взято з прогнозів по беті: у беті була стеля 30 рівня, вище оцінки проєктні. Рядок відкриває сторінку класу.')]),
         ('raw', '<div class="cmp cls" id="classRef"></div>'),
     ]}]},
    {'slug': 'races', 'path': 'races/', 'art': 'human', 'js': 'raceref', 'updated': '23.10.2026',
     'title': t('Расы', 'Races', 'Раси'),
     'lead': t('Пять рас за каждую фракцию: доступные классы и четыре расовые способности.',
               'Five races per faction: available classes and four racial abilities.',
               'П’ять рас за кожну фракцію: доступні класи та чотири расові здібності.'),
     'tile': t('Сравнение всех рас', 'All races compared', 'Порівняння всіх рас'),
     'sources': [('Method', 'https://www.method.gg/wow-forever/all-new-racial-abilities-in-world-of-warcraft-forever'),
                 ('Warcraft Tavern', 'https://www.warcrafttavern.com/forever/guides/races/')],
     'sections': [{'id': 'compare', 'title': t('Сравнение', 'Comparison', 'Порівняння'), 'blocks': [
         ('text', [t('У каждой расы по четыре способности: две активные и две пассивные. Часть старых способностей заменена новыми, сопротивления убраны.',
                     'Each race has four abilities: two active and two passive. Some old abilities were replaced with new ones, resistances were removed.',
                     'У кожної раси по чотири здібності: дві активні та дві пасивні. Частину старих здібностей замінено новими, опори прибрано.')]),
         ('raw', '<div class="cmp rac" id="raceRef"></div>'),
         ('tip', t('Скайборн играбельна за обе фракции, выбор фракции делается при создании. Обе ветки говорят на общем языке, а стартовая зона Zephras Isle общая, враги там не встречаются из-за слоёв.',
                   'Skyborne is playable for both factions; the faction is chosen at creation. Both branches speak a common language, and the Zephras Isle starting zone is shared, with no enemies meeting there because of layers.',
                   'Скайборн ігрова за обидві фракції, фракцію обирають під час створення. Обидві гілки говорять спільною мовою, а стартова зона Zephras Isle спільна, вороги там не зустрічаються через шари.')),
     ]}]},
]


# ---------- Служебные страницы: /privacy/ и 404.html. Не гайды: в список гайдов и плитки не попадают ----------
# Политика описывает то, что сайт делает на самом деле. Появится реклама, форма или новый сторонний скрипт — сначала поправить её.

from build import CONTACT  # noqa: E402  (адрес один на весь сайт, подвал берёт его оттуда же)
_mail = f'<a href="mailto:{CONTACT}">{CONTACT}</a>'
_cf = 'https://www.cloudflare.com/privacypolicy/'
_dc = 'https://discord.com/privacy'
_lic = ', '.join(f'<a href="{u}" target="_blank" rel="noopener">Creative Commons {n}</a>' for n, u in (
    ('BY 4.0', 'https://creativecommons.org/licenses/by/4.0/'), ('BY 3.0', 'https://creativecommons.org/licenses/by/3.0/'),
    ('CC0', 'https://creativecommons.org/publicdomain/zero/1.0/')))
_gh = 'https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement'

PAGES = [
    {'slug': 'privacy', 'path': 'privacy/', 'og': 'guides', 'art': 'hero_campfire', 'updated': '23.10.2026',
     'title': t('Конфиденциальность', 'Privacy', 'Конфіденційність'),
     'lead': t('Какие данные собирает сайт и что хранится у вас в браузере. Коротко: без входа мы о вас ничего не знаем, после входа через Discord храним только профиль.',
               'What data the site collects and what is stored in your browser. In short: without signing in we know nothing about you; after signing in with Discord we keep only your profile.',
               'Які дані збирає сайт і що зберігається у вашому браузері. Коротко: без входу ми нічого про вас не знаємо, після входу через Discord зберігаємо лише профіль.'),
     'pills': [t('Обновлено 23.10.2026', 'Updated 23.10.2026', 'Оновлено 23.10.2026')],
     'sections': [
         {'id': 'short', 'title': t('Коротко', 'In short', 'Коротко'), 'blocks': [
             ('text', [t('Гид читается без входа: тогда сайт не ставит cookies и не знает, кто вы. Вход через Discord нужен только для профиля участника Gabella Team и «Состава». Рекламы, форм и комментариев на сайте нет.',
                         'The guide works without signing in: then the site sets no cookies and does not know who you are. Signing in with Discord is only needed for a Gabella Team member profile and the Roster. The site has no ads, forms or comments.',
                         'Гід читається без входу: тоді сайт не ставить cookies і не знає, хто ви. Вхід через Discord потрібен лише для профілю учасника Gabella Team і «Складу». Реклами, форм і коментарів на сайті немає.')])]},
         {'id': 'account', 'title': t('Профиль участника', 'Member profile', 'Профіль учасника'), 'blocks': [
             ('text', [t('Войти может только участник Discord-сервера Gabella Team. При входе Discord передаёт нам ваш Discord ID, ник на сервере и дату вступления. Пароль и почту мы не получаем, ключ доступа Discord не храним.',
                         'Only members of the Gabella Team Discord server can sign in. On sign-in Discord gives us your Discord ID, your server nickname and the date you joined. We do not receive your password or email and do not keep the Discord access key.',
                         'Увійти може лише учасник Discord-сервера Gabella Team. Під час входу Discord передає нам ваш Discord ID, нік на сервері й дату вступу. Пароль і пошту ми не отримуємо, ключ доступу Discord не зберігаємо.'),
                       t('Ещё храним то, что вы указали сами: персонажей (имя, раса, класс, роль, уровень, профессии, время игры), внешний вид профиля, девиз, отметку «Ищу группу» и того, кто вас пригласил, если вы пришли по его ссылке.',
                         'We also keep what you entered yourself: your characters (name, race, class, role, level, professions, play time), the look of your profile, your motto, the Looking for group mark and who invited you, if you came by their link.',
                         'Також зберігаємо те, що ви вказали самі: персонажів (ім’я, раса, клас, роль, рівень, професії, час гри), вигляд профілю, девіз, позначку «Шукаю групу» і того, хто вас запросив, якщо ви прийшли за його посиланням.'),
                       t('Для достижений сайт ведёт счётчики: какие разделы гида вы открывали, сколько слушали радио, в какие дни заходили. Счётчики идут только после входа.',
                         'For achievements the site keeps counters: which guide sections you opened, how long you listened to the radio, which days you visited. Counters run only after you sign in.',
                         'Для досягнень сайт веде лічильники: які розділи гіда ви відкривали, скільки слухали радіо, в які дні заходили. Лічильники працюють лише після входу.'),
                       t('В «Составе» и на вашей странице всем видны персонажи, достижения, рамка, девиз и ник Discord, если вы не выключили его показ.',
                         'In the Roster and on your page everyone can see your characters, achievements, frame, motto and Discord nickname, unless you turned it off.',
                         'У «Складі» і на вашій сторінці всім видно персонажів, досягнення, рамку, девіз і нік Discord, якщо ви не вимкнули його показ.'),
                       t('После входа сайт ставит одну cookie — ключ сессии на 30 дней. Она нужна только для входа; в базе лежит не сам ключ, а его хэш. Выход удаляет сессию.',
                         'After you sign in, the site sets one cookie: a session key for 30 days. It is used only to keep you signed in; the database stores a hash of the key, not the key itself. Signing out deletes the session.',
                         'Після входу сайт ставить одну cookie — ключ сесії на 30 днів. Вона потрібна лише для входу; у базі лежить не сам ключ, а його хеш. Вихід видаляє сесію.')]),
             ('raw', t(f'<p><a href="{_dc}" target="_blank" rel="noopener">Политика конфиденциальности Discord</a></p>',
                       f'<p><a href="{_dc}" target="_blank" rel="noopener">Discord privacy policy</a></p>',
                       f'<p><a href="{_dc}" target="_blank" rel="noopener">Політика конфіденційності Discord</a></p>'))]},
         {'id': 'storage', 'title': t('Где и сколько хранится', 'Where and how long', 'Де й скільки зберігається'), 'blocks': [
             ('text', [t('Профили хранятся в Cloudflare (Workers и база D1): Cloudflare обрабатывает их по нашему поручению. Храним, пока вы не удалите профиль. Никому не передаём и не продаём.',
                         'Profiles are stored with Cloudflare (Workers and the D1 database), which processes them on our behalf. We keep them until you delete your profile. We do not share or sell them.',
                         'Профілі зберігаються в Cloudflare (Workers і база D1): Cloudflare обробляє їх за нашим дорученням. Зберігаємо, доки ви не видалите профіль. Нікому не передаємо й не продаємо.'),
                       t('Администратор может скрыть персонажа или девиз, если они нарушают правила сервера.',
                         'An administrator can hide a character or motto that breaks the server rules.',
                         'Адміністратор може приховати персонажа або девіз, якщо вони порушують правила сервера.')])]},
         {'id': 'delete', 'title': t('Скачать и удалить', 'Download and delete', 'Завантажити й видалити'), 'blocks': [
             ('text', [t('В кабинете «Мой профиль», раздел «Аккаунт», можно скачать всё, что мы о вас храним, одним файлом и удалить профиль. Вместе с ним сразу удаляются персонажи, достижения, счётчики, записи в ленте и сессии. Восстановить профиль нельзя.',
                         'In My profile, under Account, you can download everything we keep about you as one file and delete your profile. Your characters, achievements, counters, feed entries and sessions are deleted with it at once. A deleted profile cannot be restored.',
                         'У кабінеті «Мій профіль», розділ «Акаунт», можна завантажити все, що ми про вас зберігаємо, одним файлом і видалити профіль. Разом із ним одразу видаляються персонажі, досягнення, лічильники, записи в стрічці й сесії. Відновити профіль не можна.')])]},
         {'id': 'analytics', 'title': t('Статистика посещений', 'Visit statistics', 'Статистика відвідувань'), 'blocks': [
             ('text', [t('Чтобы понимать, какие страницы читают, сайт использует Cloudflare Web Analytics. Он работает без cookies, не снимает отпечаток браузера и не следит за вами на других сайтах.',
                         'To see which pages people read, the site uses Cloudflare Web Analytics. It works without cookies, does not fingerprint your browser and does not track you across other sites.',
                         'Щоб розуміти, які сторінки читають, сайт використовує Cloudflare Web Analytics. Він працює без cookies, не знімає відбиток браузера і не стежить за вами на інших сайтах.'),
                       t('Мы видим только сводные цифры: сколько раз открывали страницу, из какой страны, с какого типа устройства и с какого сайта пришли. Отдельного посетителя в них не различить.',
                         'We only see totals: how many times a page was opened, from which country, on what kind of device and from which site. Individual visitors cannot be told apart.',
                         'Ми бачимо лише зведені цифри: скільки разів відкривали сторінку, з якої країни, з якого типу пристрою і з якого сайту прийшли. Окремого відвідувача в них не розрізнити.')]),
             ('raw', t(f'<p><a href="{_cf}" target="_blank" rel="noopener">Политика конфиденциальности Cloudflare</a></p>',
                       f'<p><a href="{_cf}" target="_blank" rel="noopener">Cloudflare privacy policy</a></p>',
                       f'<p><a href="{_cf}" target="_blank" rel="noopener">Політика конфіденційності Cloudflare</a></p>'))]},
         {'id': 'hosting', 'title': t('Хостинг', 'Hosting', 'Хостинг'), 'blocks': [
             ('text', [t('Сайт размещён на GitHub Pages. Как любой веб-сервер, GitHub получает IP-адрес вашего устройства, чтобы отдать страницу, и может хранить его в журналах для защиты от атак. У нас доступа к этим журналам нет.',
                         'The site is hosted on GitHub Pages. Like any web server, GitHub receives your device’s IP address to deliver the page and may keep it in logs to protect against attacks. We have no access to those logs.',
                         'Сайт розміщено на GitHub Pages. Як будь-який вебсервер, GitHub отримує IP-адресу вашого пристрою, щоб віддати сторінку, і може зберігати її в журналах для захисту від атак. Ми доступу до цих журналів не маємо.')]),
             ('raw', t(f'<p><a href="{_gh}" target="_blank" rel="noopener">Политика конфиденциальности GitHub</a></p>',
                       f'<p><a href="{_gh}" target="_blank" rel="noopener">GitHub privacy statement</a></p>',
                       f'<p><a href="{_gh}" target="_blank" rel="noopener">Політика конфіденційності GitHub</a></p>'))]},
         {'id': 'device', 'title': t('Что хранится у вас', 'Stored on your device', 'Що зберігається у вас'), 'blocks': [
             ('text', [t('В памяти браузера (localStorage) сайт запоминает выбранную тему, вашего героя — расу, класс, уровень и профессии, если вы их указали, — и настройки радио: станцию, трек, очередь треков, громкость, таймер сна и звуки вокруг, а на странице «В игре» — ваши таймеры и фракцию. Чтобы гид открывался без сети, браузер хранит копии страниц. После входа добавляются отметка о входе, копия профиля для быстрой загрузки и выключатель звука достижений.',
                         'In browser storage (localStorage) the site remembers your chosen theme, your hero (race, class, level and professions) if you entered them, and the radio settings: station, track, the queue of tracks, volume, sleep timer and ambient sounds, and on the In game page your timers and faction. To open the guide offline, the browser keeps copies of the pages. After you sign in, it also keeps a signed-in mark, a copy of your profile for faster loading and the achievement sound switch.',
                         'У пам’яті браузера (localStorage) сайт запам’ятовує вибрану тему, вашого героя — расу, клас, рівень і професії, якщо ви їх вказали, — і налаштування радіо: станцію, трек, чергу треків, гучність, таймер сну і звуки довкола, а на сторінці «У грі» — ваші таймери та фракцію. Щоб гід відкривався без мережі, браузер зберігає копії сторінок. Після входу додаються позначка входу, копія профілю для швидкого завантаження й вимикач звуку досягнень.'),
                       t('Эти данные остаются на вашем устройстве и никуда не отправляются. Удалить их можно, очистив данные сайта в настройках браузера.',
                         'This data stays on your device and is not sent anywhere. You can delete it by clearing the site data in your browser settings.',
                         'Ці дані залишаються на вашому пристрої й нікуди не надсилаються. Видалити їх можна, очистивши дані сайту в налаштуваннях браузера.')])]},
         {'id': 'links', 'title': t('Шрифты, музыка и ссылки', 'Fonts, music and links', 'Шрифти, музика та посилання'), 'blocks': [
             ('text', [t('Шрифты и картинки загружаются с нашего же сайта, без сторонних сервисов. Музыка радио лежит в хранилище Cloudflare R2 и загружается с нашего адреса media.gabella.site, только когда вы включили радио; как и при открытии страниц, Cloudflare получает IP-адрес вашего устройства. Звуки костра, дождя и ветра создаёт сам браузер. Ссылки на источники ведут на другие сайты, у них свои правила конфиденциальности.',
                         'Fonts and images load from this site, with no third-party services. Radio music is stored in Cloudflare R2 and loads from our address media.gabella.site, only when you turn the radio on; as with the pages, Cloudflare receives your device’s IP address. The campfire, rain and wind sounds are made by the browser itself. Links to sources lead to other sites, which have their own privacy rules.',
                         'Шрифти й зображення завантажуються з нашого ж сайту, без сторонніх сервісів. Музика радіо лежить у сховищі Cloudflare R2 і завантажується з нашої адреси media.gabella.site, лише коли ви ввімкнули радіо; як і під час відкриття сторінок, Cloudflare отримує IP-адресу вашого пристрою. Звуки багаття, дощу й вітру створює сам браузер. Посилання на джерела ведуть на інші сайти, у них свої правила конфіденційності.')]),
             ('raw', t(f'<p>Музыка радио: Kevin MacLeod (incompetech.com) и другие авторы с opengameart.org, лицензии {_lic}. Звук перекодирован и выровнен по громкости. Автор и лицензия каждого трека — в панели радио.</p>',
                       f'<p>Radio music: Kevin MacLeod (incompetech.com) and other authors from opengameart.org, licensed under {_lic}. The audio is re-encoded and levelled in loudness. The author and license of every track are in the radio panel.</p>',
                       f'<p>Музика радіо: Kevin MacLeod (incompetech.com) та інші автори з opengameart.org, ліцензії {_lic}. Звук перекодовано й вирівняно за гучністю. Автор і ліцензія кожного треку — у панелі радіо.</p>'))]},
         {'id': 'contact', 'title': t('Связь', 'Contact', 'Зв’язок'), 'blocks': [
             ('text', [t('С вопросами о данных, ошибками в гайде и претензиями правообладателей пишите на почту ниже. Если не можете войти, профиль удалим по письму: укажите ник в Discord.',
                         'For questions about data, mistakes in the guide or copyright concerns, write to the address below. If you cannot sign in, we will delete your profile on request: include your Discord nickname.',
                         'З питаннями про дані, помилками в гіді та претензіями правовласників пишіть на пошту нижче. Якщо не можете увійти, профіль видалимо за листом: вкажіть нік у Discord.')]),
             ('raw', f'<p>{_mail}</p>'),
             ('text', [t('Если что-то изменится, например появится реклама, мы обновим эту страницу и дату вверху.',
                         'If anything changes, for example if ads appear, we will update this page and the date at the top.',
                         'Якщо щось зміниться, наприклад з’явиться реклама, ми оновимо цю сторінку й дату вгорі.')])]},
     ]},
]

# 404.html в корне гида: GitHub Pages отдаёт её на любой несуществующий адрес под /wow/. Одна страница на все языки.
NOT_FOUND = {
    'slug': '404', 'path': '', 'og': 'guides', 'art': 'hero_campfire', 'more': False,
    'title': t('Страница не найдена', 'Page not found', 'Сторінку не знайдено'),
    'lead': t('Такой страницы нет: ссылка устарела или в адресе опечатка. Разделы гида ниже.',
              'This page does not exist: the link is outdated or the address has a typo. The guide sections are below.',
              'Такої сторінки немає: посилання застаріло або в адресі помилка. Розділи гіда нижче.'),
    'sections': [{'id': 'where', 'title': t('Куда дальше', 'Where next', 'Куди далі'), 'blocks': [
        ('raw', '<p class="nf-langs"><a href="./">Главная гида</a><span aria-hidden="true"> · </span>'
                '<a href="en/" lang="en">Page not found — English guide</a><span aria-hidden="true"> · </span>'
                '<a href="uk/" lang="uk">Сторінку не знайдено — гід українською</a></p>'),
    ]}],
}

# ---------- /play/ «В игре»: второй экран на время игры. Сборка — build_guides.play_body + JS['play'] ----------
# Маршрут по зонам и совет про отдых страница берёт из гайда «Прокачка» (секции route и pace), тут только подписи и рубежи.
PLAY = {
    'slug': 'play', 'path': 'play/', 'og': 'guides', 'art': 'hero_campfire', 'compact': True, 'more': False, 'js': 'play',
    'title': t('В игре', 'In game', 'У грі'),
    'lead': t('Второй экран на время игры: радио, что делать на вашем уровне, подземелья и таймеры.',
              'A second screen while you play: radio, what to do at your level, dungeons and timers.',
              'Другий екран під час гри: радіо, що робити на вашому рівні, підземелля й таймери.'),
    'sections': [],
}
# Рубежи по уровню — только факты из гайдов (ездовое — секция pace «Прокачки», Хиджал — маршрут, рейды — «Подземелья и рейды»)
PLAY_MILESTONES = [
    (40, t('Ездовое животное: обучение 100 золотых и скакун 20 (+60% скорости).',
           'Riding: training 100 gold and a mount 20 (+60% speed).',
           'Їздова тварина: навчання 100 золотих і скакун 20 (+60% швидкості).')),
    (60, t('Быстрое ездовое: 1000 и 200 золотых (+100%). Открыт Mount Hyjal, рейды — с 09.12.2026.',
           'Fast riding: 1,000 and 200 gold (+100%). Mount Hyjal opens, raids from 09.12.2026.',
           'Швидка їздова: 1000 і 200 золотих (+100%). Відкритий Mount Hyjal, рейди — з 09.12.2026.')),
]
PLAY_TX = {
    'radio': t('Радио', 'Radio', 'Радіо'),
    'lvl': t('Уровень', 'Level', 'Рівень'),
    'lvDown': t('Уровень ниже', 'Level down', 'Рівень нижче'),
    'lvUp': t('Уровень выше', 'Level up', 'Рівень вище'),
    'noHero': t('Персонаж не выбран', 'No hero set', 'Персонажа не вибрано'),
    'edit': t('Настроить персонажа', 'Set up your hero', 'Налаштувати персонажа'),
    'fac': t('Фракция', 'Faction', 'Фракція'),
    'alliance': t('Альянс', 'Alliance', 'Альянс'),
    'horde': t('Орда', 'Horde', 'Орда'),
    'needLvl': t('Укажите уровень кнопкой «+» — подскажем зоны и подземелья.',
                 'Set your level with “+” to see zones and dungeons.',
                 'Вкажіть рівень кнопкою «+» — підкажемо зони й підземелля.'),
    'now': t('Сейчас', 'Now', 'Зараз'),
    'next': t('Дальше', 'Next', 'Далі'),
    'from': t('с', 'from', 'з'),
    'at': t('на', 'at', 'на'),
    'route': t('Весь маршрут', 'Full route', 'Весь маршрут'),
    'dung': t('Подземелья под', 'Dungeons for level', 'Підземелля під'),
    'dungNone': t('Под этот уровень подземелий нет.', 'No dungeons for this level.', 'Під цей рівень підземель немає.'),
    'all': t('Все подземелья', 'All dungeons', 'Усі підземелля'),
    'new': t('новое', 'new', 'нове'),
    'timers': t('Таймеры', 'Timers', 'Таймери'),
    'food': t('Еда', 'Food', 'Їжа'),
    'foodNote': t('+5% опыта за врагов', '+5% experience from enemies', '+5% досвіду за ворогів'),
    'min': t('мин', 'min', 'хв'),
    'custom': t('Своё', 'Custom', 'Своє'),
    'name': t('Название', 'Name', 'Назва'),
    'minutes': t('Минут', 'Minutes', 'Хвилин'),
    'start': t('Старт', 'Start', 'Старт'),
    'timer': t('Таймер', 'Timer', 'Таймер'),
    'done': t('Время вышло', 'Time is up', 'Час вийшов'),
    'again': t('Ещё раз', 'Again', 'Ще раз'),
    'remove': t('Убрать', 'Remove', 'Прибрати'),
    'noTimers': t('Нажмите на заготовку или задайте своё время. Таймеры идут и после перезагрузки страницы.',
                  'Tap a preset or set your own time. Timers keep running after the page reloads.',
                  'Натисніть заготовку або задайте свій час. Таймери йдуть і після перезавантаження сторінки.'),
    'notify': t('Уведомление, когда вкладка в фоне', 'Notify when the tab is in the background', 'Сповіщення, коли вкладка у фоні'),
    'wake': t('Экран не гаснет', 'Keep screen on', 'Екран не гасне'),
}
PAGES.append(PLAY)
