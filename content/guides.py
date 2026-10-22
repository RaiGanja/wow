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
ORDER = ['leveling', 'dungeons', 'professions', 'faq', 'news']   # порядок плиток на хабе и в «Другие гайды»


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
                 t('Доступ был у владельцев наборов Epic и Collection. Blizzard продлила бету до 23.10, она отключается в 10:00 по тихоокеанскому времени. 08.10 в бету добавили City of Dalaran и примерно на 20% больше опыта за врагов в подземельях.',
                   'Access was for Epic and Collection owners. Blizzard extended the beta to 23.10, it goes offline at 10:00 Pacific time. On 08.10 the beta got City of Dalaran and about 20% more experience for enemies in dungeons.',
                   'Доступ мали власники наборів Epic і Collection. Blizzard продовжила бету до 23.10, вона вимикається о 10:00 за тихоокеанським часом. 08.10 у бету додали City of Dalaran і приблизно на 20% більше досвіду за ворогів у підземеллях.')],
                ['15.10', t('Крупный патч беты', 'Major beta patch', 'Великий патч бети'),
                 t('Переделаны способности рас (оружейные специализации заменены критами) и настроены почти все классы.',
                   'Racial abilities were reworked (weapon specializations replaced with crits) and almost all classes were tuned.',
                   'Переробили здібності рас (спеціалізації зброї замінили критами) і налаштували майже всі класи.')],
                ['27.10 – 03.11', t('Ранняя резервация имён', 'Early name reservation', 'Рання резервація імен'),
                 t('Входит в наборы Heroic, Epic и Collection. До трёх персонажей на аккаунт, кто первым пришёл, тот и занял. Это не ранний доступ в игру. Точное время открытия Blizzard пока не назвала.',
                   'Included in the Heroic, Epic and Collection packs. Up to three characters per account, first come, first served. This is not early access to the game. Blizzard has not yet named the exact opening time.',
                   'Входить у набори Heroic, Epic і Collection. До трьох персонажів на акаунт, хто перший прийшов, той і зайняв. Це не ранній доступ до гри. Точний час відкриття Blizzard поки не назвала.')],
                ['04.11', t('Релиз WoW Forever', 'WoW Forever release', 'Реліз WoW Forever'),
                 t('Нужна подписка или игровое время. Forever постоянная игра рядом с Retail и Classic, не сезон. Точное время старта Blizzard пока не подтвердила. Если это 15:00 по тихоокеанскому, как пишут некоторые сайты, в Киеве будет уже 01:00 5 ноября.',
                   'Requires a subscription or game time. Forever is a permanent game next to Retail and Classic, not a season. Blizzard has not yet confirmed the exact launch time. If it is 15:00 Pacific, as some sites say, it will already be 01:00 on 5 November in Kyiv.',
                   'Потрібна підписка або ігровий час. Forever постійна гра поруч із Retail і Classic, не сезон. Точний час старту Blizzard поки не підтвердила. Якщо це 15:00 за тихоокеанським, як пишуть деякі сайти, у Києві буде вже 01:00 5 листопада.')],
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
                 t('Восточные королевства и Калимдор, прокачка до 60. Постоянная игра, а не сезон. Нет летающих скакунов и нет масштабирования уровней, как и в Classic.',
                   'Eastern Kingdoms and Kalimdor, leveling to 60. A permanent game, not a season. No flying mounts and no level scaling, as in Classic.',
                   'Східні королівства та Калімдор, прокачування до 60. Постійна гра, а не сезон. Немає літаючих скакунів і масштабування рівнів, як і в Classic.')],
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
                 'a': [t('04.11.2026. Точное время старта Blizzard пока не подтвердила. Если это 15:00 по тихоокеанскому, как пишут некоторые сайты, в Киеве будет уже 01:00 5 ноября.',
                         '04.11.2026. Blizzard has not yet confirmed the exact launch time. If it is 15:00 Pacific, as some sites say, it will already be 01:00 on 5 November in Kyiv.',
                         '04.11.2026. Точний час старту Blizzard поки не підтвердила. Якщо це 15:00 за тихоокеанським, як пишуть деякі сайти, у Києві буде вже 01:00 5 листопада.')]},
                {'id': 'subscription', 'q': t('Нужна ли подписка?', 'Do I need a subscription?', 'Чи потрібна підписка?'),
                 'a': [t('Да, подписка или игровое время. Forever постоянная игра рядом с Retail и Classic, а не сезон.',
                         'Yes, a subscription or game time. Forever is a permanent game next to Retail and Classic, not a season.',
                         'Так, підписка або ігровий час. Forever постійна гра поруч із Retail і Classic, а не сезон.')]},
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
                 'a': [t('До 60, в Восточных королевствах и Калимдоре. Летающих скакунов и масштабирования уровней нет, как и в Classic.',
                         'Up to 60, in the Eastern Kingdoms and Kalimdor. No flying mounts and no level scaling, as in Classic.',
                         'До 60, у Східних королівствах і Калімдорі. Літаючих скакунів і масштабування рівнів немає, як і в Classic.')]},
                {'id': 'together', 'q': t('Можно ли играть вместе, если выбрали разные режимы?', 'Can we play together in different modes?', 'Чи можна грати разом, якщо обрали різні режими?'),
                 'a': [t('Нет: группироваться можно только внутри одного режима. Режимы на старте: обычный, PvP и RP, Hardcore запустят позже. В PvP на аккаунте может быть только одна фракция.',
                         'No: you can only group within one mode. Modes at launch: Normal, PvP and RP, Hardcore comes later. In PvP an account can have only one faction.',
                         'Ні: групуватися можна лише в межах одного режиму. Режими на старті: звичайний, PvP і RP, Hardcore запустять пізніше. У PvP на акаунті може бути лише одна фракція.')]},
                {'id': 'raids', 'q': t('Когда откроются рейды?', 'When do raids open?', 'Коли відкриються рейди?'),
                 'a': [t('09.12: Barrow Deeps (10 игроков), Hyjal Summit (20), Onyxia’s Lair (40). До этого есть пять недель на прокачку и подземелья.',
                         '09.12: Barrow Deeps (10 players), Hyjal Summit (20), Onyxia’s Lair (40). Until then you have five weeks for leveling and dungeons.',
                         '09.12: Barrow Deeps (10 гравців), Hyjal Summit (20), Onyxia’s Lair (40). До цього є п’ять тижнів на прокачування та підземелля.')]},
                {'id': 'beta', 'q': t('Можно ли ещё попасть в бету?', 'Can I still get into the beta?', 'Чи можна ще потрапити в бету?'),
                 'a': [t('Доступ был у владельцев Epic и Collection. Blizzard продлила бету до 23.10, она отключается в 10:00 по тихоокеанскому времени.',
                         'Access was for Epic and Collection owners. Blizzard extended the beta to 23.10, it goes offline at 10:00 Pacific time.',
                         'Доступ мали власники Epic і Collection. Blizzard продовжила бету до 23.10, вона вимикається о 10:00 за тихоокеанським часом.')]},
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

GUIDES.sort(key=lambda g: ORDER.index(g['slug']))
