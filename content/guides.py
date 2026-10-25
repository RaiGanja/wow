"""Гайды: тексты сразу на трёх языках. Строка = {'ru': …, 'en': …, 'uk': …}.
Названия игровых объектов на EN/UK английские. Факты — только из источников в 'sources'.
Блок = (тип, данные):
  ('text', [строка, …])                                 абзацы
  ('steps', [{'t': строка, 'd': строка}, …])           нумерованный список 1/2/3
  ('tiles', [{'t', 'd', 'href', 'art'}, …])            плитки с артом; href относительно корня гида, art = имя без размера
  ('play', {'h', 'd', 'go'})                           строка-ссылка на «В игре» (гайд «Прокачка»)
  ('table', {'head': [строка, …], 'rows': [[строка|str, …], …]})
  ('tabs', [{'id': 'alliance', 't': строка, 'blocks': [блок, …]}, …])
  ('faq', [{'id': 'release', 'q': строка, 'a': [строка, …], 'link': (строка, url)?}, …])   link — кнопка под ответом
  ('tip', строка)
  ('raw', 'html')   только для живых частей, разметка с data-атрибутами для JS"""


def t(ru, en, uk):
    return {'ru': ru, 'en': en, 'uk': uk}


HUB = {
    'slug': '', 'art': 'hero_campfire', 'hero': 'hero_guides',
    'title': t('Гайды', 'Guides', 'Гайди'),
    'lead': t('Прокачка, подземелья, профессии, ответы на вопросы и новости WoW Forever.',
              'Leveling, dungeons, professions, answers and news for WoW Forever.',
              'Прокачка, підземелля, професії, відповіді на питання та новини WoW Forever.'),
}

GUIDES = []   # наполняется в задачах 3, 5, 6, 7, 9; каждый гайд дописывается ниже через GUIDES.append

NEWS = []     # ручные записи: {'date': '2026-10-23', 'title': t(...), 'text': t(...), 'url': 'https://…'}
from build import DISCORD_AT  # noqa: E402  (у каждого места ссылки своё приглашение)

ORDER = ['leveling', 'leveling-warrior', 'leveling-paladin', 'leveling-hunter', 'leveling-rogue', 'leveling-priest', 'leveling-shaman', 'leveling-mage', 'leveling-warlock', 'leveling-druid', 'best-race', 'tier-list', 'legacy', 'dungeons', 'professions', 'faq', 'requirements', 'news', 'ukrainian']   # порядок плиток на хабе и в «Другие гайды»


# ---------- FAQ: даты и наборы, режимы, имена, отличия от Era (переехали с главной) + частые вопросы ----------

GUIDES.append({
    'slug': 'faq', 'art': 'mage', 'hero': 'hero_faq', 'js': 'faq',
    'title': t('FAQ и даты', 'FAQ and dates', 'FAQ і дати'),
    'lead': t('Даты до и после релиза, цены и подписка, режимы и серверы, имена, графика и ответы на частые вопросы.',
              'Dates before and after release, prices and subscription, modes and servers, names, graphics and answers to common questions.',
              'Дати до й після релізу, ціни та підписка, режими та сервери, імена, графіка та відповіді на часті питання.'),
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
        (t('Battle.net: Forever, наборы, регионы', 'Battle.net: Forever, packs, regions', 'Battle.net: Forever, набори, регіони'),
         'https://eu.shop.battle.net/en-gb/product/world-of-warcraft-forever'),
        (t('Battle.net: цены подписки', 'Battle.net: subscription prices', 'Battle.net: ціни підписки'),
         'https://us.shop.battle.net/en-us/product/world-of-warcraft-subscription'),
        (t('Blizzard: старт и коды Invite-A-Friend', 'Blizzard: launch and Invite-A-Friend codes', 'Blizzard: старт і коди Invite-A-Friend'),
         'https://news.blizzard.com/en-us/article/24301508'),
        (t('Blizzard: режим RP-PvP к старту', 'Blizzard: RP-PvP mode for launch', 'Blizzard: режим RP-PvP до старту'),
         'https://us.forums.blizzard.com/en/wow/t/the-roleplay-pvp-ruleset-is-coming-to-wow-forever/2389502'),
        (t('Method: серверы и режимы', 'Method: servers and modes', 'Method: сервери та режими'),
         'https://www.method.gg/wow-forever/choosing-your-character-name-and-ruleset-in-wow-forever'),
        (t('Conquest Capped: Classic или Enhanced', 'Conquest Capped: Classic or Enhanced', 'Conquest Capped: Classic чи Enhanced'),
         'https://conquestcapped.com/guides/wow-forever/wow-forever-classic-look/'),
    ],
    'sections': [
        {'id': 'dates', 'title': t('Даты', 'Dates', 'Дати'), 'blocks': [
            ('table', {'head': [t('Когда', 'When', 'Коли'), t('Событие', 'Event', 'Подія'), t('Что важно', 'What matters', 'Що важливо')], 'rows': [
                ['17.09 – 23.10', t('Закрытая бета', 'Closed beta', 'Закрита бета'),
                 t('Доступ был у владельцев наборов Epic и Collection. Бета завершилась 23.10 в 10:00 по тихоокеанскому времени. 08.10 в бету добавили [[Даларан|City of Dalaran]] и примерно на 20% больше опыта за врагов в подземельях.',
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
                 t('Нужна подписка или игровое время. Forever — постоянная игра рядом с Retail и Classic, а не сезон. Старт в 15:00 по тихоокеанскому, это 23:00 UTC.',
                   'Requires a subscription or game time. Forever is a permanent game next to Retail and Classic, not a season. Launch is at 15:00 Pacific, which is 23:00 UTC.',
                   'Потрібна підписка або ігровий час. Forever — постійна гра поруч із Retail і Classic, а не сезон. Старт о 15:00 за тихоокеанським, це 23:00 UTC.')],
                ['09.12', t('Открываются рейды', 'Raids open', 'Відкриваються рейди'),
                 t('Barrow Deeps (10 игроков), Hyjal Summit (20), Onyxia’s Lair (40). До этого есть пять недель на прокачку и подземелья.',
                   'Barrow Deeps (10 players), Hyjal Summit (20), Onyxia’s Lair (40). Until then you have five weeks for leveling and dungeons.',
                   'Barrow Deeps (10 гравців), Hyjal Summit (20), Onyxia’s Lair (40). До цього є п’ять тижнів на прокачування та підземелля.')],
            ]}),
            ('text', [t('Старт 04.11 в 23:00 UTC по часовым поясам:', 'Launch on 04.11 at 23:00 UTC by time zone:', 'Старт 04.11 о 23:00 UTC за часовими поясами:')]),
            ('table', {'head': [t('Где', 'Where', 'Де'), t('Старт', 'Launch', 'Старт')], 'rows': [
                [t('Лос-Анджелес', 'Los Angeles', 'Лос-Анджелес'), '04.11, 15:00'],
                [t('Нью-Йорк', 'New York', 'Нью-Йорк'), '04.11, 18:00'],
                [t('Сан-Паулу', 'São Paulo', 'Сан-Паулу'), '04.11, 20:00'],
                [t('UTC, Лондон, Лиссабон', 'UTC, London, Lisbon', 'UTC, Лондон, Лісабон'), '04.11, 23:00'],
                [t('Берлин, Париж, Мадрид, Рим, Варшава', 'Berlin, Paris, Madrid, Rome, Warsaw', 'Берлін, Париж, Мадрид, Рим, Варшава'), '05.11, 00:00'],
                [t('Киев', 'Kyiv', 'Київ'), '05.11, 01:00'],
                [t('Алматы', 'Almaty', 'Алмати'), '05.11, 04:00'],
                [t('Сидней', 'Sydney', 'Сідней'), '05.11, 10:00'],
            ]}),
        ]},
        {'id': 'editions', 'title': t('Цены и подписка', 'Prices and subscription', 'Ціни та підписка'), 'blocks': [
            ('text', [t('Forever входит в обычную подписку WoW или игровое время: одна подписка открывает WoW, Classic и Forever. Отдельно игру покупать не нужно.',
                        'Forever is included in the regular WoW subscription or game time: one subscription opens WoW, Classic and Forever. You do not buy the game separately.',
                        'Forever входить у звичайну підписку WoW або ігровий час: одна підписка відкриває WoW, Classic і Forever. Окремо гру купувати не потрібно.')]),
            ('table', {'head': [t('Подписка', 'Subscription', 'Підписка'), t('США, в месяц', 'US, per month', 'США, на місяць'), t('Европа, в месяц', 'Europe, per month', 'Європа, на місяць')], 'rows': [
                [t('1 месяц', '1 month', '1 місяць'), '$14.99', '€12.99'],
                [t('3 месяца', '3 months', '3 місяці'), '$13.99', '€11.99'],
                [t('6 или 12 месяцев', '6 or 12 months', '6 або 12 місяців'), '$12.99', '€10.99'],
            ]}),
            ('text', [t('Цены магазина Battle.net на 24.10, с НДС. В других валютах и регионах цена своя.',
                        'Battle.net shop prices as of 24.10, VAT included. Other currencies and regions have their own price.',
                        'Ціни магазину Battle.net на 24.10, з ПДВ. В інших валютах і регіонах ціна своя.')]),
            ('table', {'head': [t('Набор', 'Pack', 'Набір'), t('Цена', 'Price', 'Ціна'), t('Что даёт', 'What you get', 'Що дає')], 'rows': [
                ['Heroic Pack', '$29.99', t('Расу Скайборн, её стартовую зону и раннюю резервацию имён.',
                                            'The Skyborne race, its starting zone and early name reservation.',
                                            'Расу Скайборн, її стартову зону та ранню резервацію імен.')],
                ['Epic Pack', '$59.99', t('То же плюс 30 дней игрового времени: их начислят в день старта.',
                                          'The same plus 30 days of game time, added on launch day.',
                                          'Те саме плюс 30 днів ігрового часу: їх нарахують у день старту.')],
                ['Warcraft Forever Collection', '$79.99', t('Epic Pack плюс Warcraft III: Reforged с кампанией Forsaken Kingdom. Продаётся до 11.01.2027.',
                                                            'The Epic Pack plus Warcraft III: Reforged with the Forsaken Kingdom campaign. On sale until 11.01.2027.',
                                                            'Epic Pack плюс Warcraft III: Reforged з кампанією Forsaken Kingdom. Продається до 11.01.2027.')],
            ]}),
            ('text', [t('Остальные восемь рас и все девять классов докупать не нужно.',
                        'The other eight races and all nine classes do not need to be bought.',
                        'Решту восьми рас і всі дев’ять класів докуповувати не потрібно.')]),
            ('steps', [
                {'t': t('Неделя для друга', 'A week for a friend', 'Тиждень для друга'),
                 'd': t('К набору прилагается код Invite-A-Friend: по нему друг играет с 04.11 по 11.11 без подписки. Heroic даёт 1 код, Epic и Collection — 3. Коды приходят на почту с 20.10, к подарочным покупкам их нет.',
                        'A pack comes with Invite-A-Friend codes: with one, a friend plays from 04.11 to 11.11 without a subscription. Heroic gives 1 code, Epic and Collection give 3. Codes arrive by email from 20.10, gift purchases get none.',
                        'До набору додається код Invite-A-Friend: з ним друг грає з 04.11 по 11.11 без підписки. Heroic дає 1 код, Epic і Collection — 3. Коди приходять на пошту з 20.10, до подарункових покупок їх немає.')},
            ]),
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
        {'id': 'modes', 'title': t('Режимы и серверы', 'Modes and servers', 'Режими та сервери'), 'blocks': [
            ('steps', [
                {'t': t('Обычный, PvP, RP и RP-PvP', 'Normal, PvP, RP and RP-PvP', 'Звичайний, PvP, RP і RP-PvP'),
                 'd': t('RP-PvP Blizzard добавила к старту 22.10, выбрать его можно уже при резерве имён. Hardcore запустят позже со своими правилами.',
                        'Blizzard added RP-PvP for launch on 22.10, and you can pick it as early as name reservation. Hardcore will launch later with its own rules.',
                        'RP-PvP Blizzard додала до старту 22.10, обрати його можна вже під час резерву імен. Hardcore запустять пізніше зі своїми правилами.')},
                {'t': t('Один сервер на режим', 'One server per mode', 'Один сервер на режим'),
                 'd': t('Реалмов нет: в каждом регионе по одному большому серверу на режим, нагрузку делят слои. Регионы: Америка и Океания, Европа, Корея, Тайвань.',
                        'There are no realms: each region has one large server per mode, and layers share the load. Regions: Americas and Oceania, Europe, Korea, Taiwan.',
                        'Реалмів немає: у кожному регіоні по одному великому серверу на режим, навантаження ділять шари. Регіони: Америка й Океанія, Європа, Корея, Тайвань.')},
                {'t': t('Режим выбирают один раз', 'The mode is chosen once', 'Режим обирають один раз'),
                 'd': t('Перенести персонажа в другой режим нельзя. Исключение — погибший персонаж Hardcore: он продолжает в другом режиме.',
                        'You cannot move a character to another mode. The exception is a Hardcore character who has died: it carries on in another mode.',
                        'Перенести персонажа в інший режим не можна. Виняток — загиблий персонаж Hardcore: він продовжує в іншому режимі.')},
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
                 t('Новые зоны, задания, 9 новых подземелий, 2 новых рейда и Onyxia’s Lair, новое поле боя, новая раса Скайборн.',
                   'New zones, quests, 9 new dungeons, 2 new raids plus Onyxia’s Lair, a new battleground, the new Skyborne race.',
                   'Нові зони, завдання, 9 нових підземель, 2 нові рейди та Onyxia’s Lair, нове поле бою, нова раса Скайборн.')],
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
        {'id': 'graphics', 'title': t('Classic или Enhanced', 'Classic or Enhanced', 'Classic чи Enhanced'), 'blocks': [
            ('text', [t('При первом входе игра предлагает набор настроек: Classic или Enhanced. Это только старт: экран выбора больше не появится, но каждую настройку можно поменять отдельно.',
                        'On first login the game offers a set of settings: Classic or Enhanced. It is only a starting point: the choice screen will not come back, but every setting can be changed on its own.',
                        'Під час першого входу гра пропонує набір налаштувань: Classic або Enhanced. Це лише старт: екран вибору більше не з’явиться, але кожне налаштування можна змінити окремо.')]),
            ('table', {'head': [t('Настройка', 'Setting', 'Налаштування'), 'Classic', 'Enhanced', t('Где поменять', 'Where to change', 'Де змінити')], 'rows': [
                [t('Модели персонажей', 'Character models', 'Моделі персонажів'), t('Обычные (SD)', 'Standard (SD)', 'Звичайні (SD)'), t('Высокой чёткости (HD)', 'High definition (HD)', 'Високої чіткості (HD)'),
                 t('Настройки графики', 'Graphics settings', 'Налаштування графіки')],
                [t('Цели заданий на карте', 'Quest objectives on the map', 'Цілі завдань на мапі'), t('Нет', 'Off', 'Ні'), t('Есть', 'On', 'Є'),
                 t('Фильтр карты мира', 'World map filter', 'Фільтр мапи світу')],
                [t('Одна общая сумка', 'One combined bag', 'Одна спільна сумка'), t('Нет', 'Off', 'Ні'), t('Есть', 'On', 'Є'),
                 t('Настройки управления', 'Controls settings', 'Налаштування керування')],
                [t('Трансмогрификация', 'Transmog', 'Трансмогрифікація'), t('Выключена', 'Off', 'Вимкнена'), t('Включена', 'On', 'Увімкнена'),
                 t('У трансмогрификатора в городе', 'At a transmogrifier in a city', 'У трансмогрифікатора в місті')],
                [t('Клавиши A и D', 'A and D keys', 'Клавіші A і D'), t('Поворот', 'Turn', 'Поворот'), t('Шаг в сторону', 'Strafe', 'Крок убік'),
                 t('Назначение клавиш', 'Key bindings', 'Призначення клавіш')],
                [t('Расположение интерфейса', 'Interface layout', 'Розташування інтерфейсу'), t('Классическое', 'Classic', 'Класичне'), t('По центру', 'Centred', 'По центру'),
                 t('Режим редактирования', 'Edit Mode', 'Режим редагування')],
            ]}),
            ('tip', t('Режим редактирования возвращает рамкам старые места, но не старый рисунок: классический вид интерфейса дают только аддоны.',
                      'Edit Mode puts the frames back in their old places, but not their old look: the classic interface art comes only with addons.',
                      'Режим редагування повертає рамкам старі місця, але не старий вигляд: класичний вигляд інтерфейсу дають лише аддони.')),
        ]},
        {'id': 'questions', 'title': t('Частые вопросы', 'Common questions', 'Часті питання'), 'blocks': [
            ('raw', t('<label class="gsearch"><span class="sr">Поиск по вопросам</span><input type="search" id="faqQ" autocomplete="off" placeholder="Поиск по вопросам"></label><p class="note" id="faqNone" hidden>Ничего не нашлось. Попробуйте другое слово или поиск по сайту (Ctrl+K).</p>',
                      '<label class="gsearch"><span class="sr">Search questions</span><input type="search" id="faqQ" autocomplete="off" placeholder="Search questions"></label><p class="note" id="faqNone" hidden>Nothing found. Try another word or the site search (Ctrl+K).</p>',
                      '<label class="gsearch"><span class="sr">Пошук по питаннях</span><input type="search" id="faqQ" autocomplete="off" placeholder="Пошук по питаннях"></label><p class="note" id="faqNone" hidden>Нічого не знайшлося. Спробуйте інше слово або пошук по сайту (Ctrl+K).</p>')),
            ('faq', [
                {'id': 'release', 'q': t('Когда выходит WoW Forever?', 'When does WoW Forever launch?', 'Коли виходить WoW Forever?'),
                 'a': [t('04.11.2026 в 15:00 по тихоокеанскому, это 23:00 UTC.',
                         '04.11.2026 at 15:00 Pacific, which is 23:00 UTC.',
                         '04.11.2026 о 15:00 за тихоокеанським, це 23:00 UTC.')]},
                {'id': 'subscription', 'q': t('Нужна ли подписка?', 'Do I need a subscription?', 'Чи потрібна підписка?'),
                 'a': [t('Да, подписка или игровое время, та же, что для WoW и Classic: от $14.99 или €12.99 в месяц, дешевле при оплате на 3–12 месяцев. Forever — постоянная игра рядом с Retail и Classic, а не сезон.',
                         'Yes, a subscription or game time, the same one as for WoW and Classic: from $14.99 or €12.99 a month, cheaper when paid for 3–12 months. Forever is a permanent game next to Retail and Classic, not a season.',
                         'Так, підписка або ігровий час, та сама, що для WoW і Classic: від $14.99 або €12.99 на місяць, дешевше при оплаті на 3–12 місяців. Forever — постійна гра поруч із Retail і Classic, а не сезон.')]},
                {'id': 'trial', 'q': t('Можно ли попробовать бесплатно?', 'Can I try it for free?', 'Чи можна спробувати безкоштовно?'),
                 'a': [t('Только по коду друга. Владелец набора получает коды Invite-A-Friend, по такому коду играют с 04.11 по 11.11 без подписки. Heroic даёт 1 код, Epic и Collection — 3.',
                         'Only with a friend’s code. Pack owners get Invite-A-Friend codes, and with one you play from 04.11 to 11.11 without a subscription. Heroic gives 1 code, Epic and Collection give 3.',
                         'Лише за кодом друга. Власник набору отримує коди Invite-A-Friend, з таким кодом грають з 04.11 по 11.11 без підписки. Heroic дає 1 код, Epic і Collection — 3.')]},
                {'id': 'price', 'q': t('Сколько стоят наборы и нужны ли они?', 'How much are the packs, and do I need one?', 'Скільки коштують набори і чи потрібні вони?'),
                 'a': [t('Heroic Pack $29.99, Epic Pack $59.99, Warcraft Forever Collection $79.99. Набор нужен только ради расы Скайборн и ранней резервации имён: остальные восемь рас и все девять классов докупать не нужно.',
                         'Heroic Pack $29.99, Epic Pack $59.99, Warcraft Forever Collection $79.99. A pack is only needed for the Skyborne race and early name reservation: the other eight races and all nine classes do not need to be bought.',
                         'Heroic Pack $29.99, Epic Pack $59.99, Warcraft Forever Collection $79.99. Набір потрібен лише заради раси Скайборн і ранньої резервації імен: решту восьми рас і всі дев’ять класів докуповувати не потрібно.')]},
                {'id': 'reserve', 'q': t('Когда занимать имя?', 'When can I reserve a name?', 'Коли бронювати ім’я?'),
                 'a': [t('С 27.10 по 03.11, если у вас Heroic, Epic или Collection. До трёх персонажей на аккаунт, кто первым пришёл, тот и занял. Это не ранний доступ в игру.',
                         'From 27.10 to 03.11 if you own Heroic, Epic or Collection. Up to three characters per account, first come, first served. This is not early access to the game.',
                         'З 27.10 по 03.11, якщо у вас Heroic, Epic або Collection. До трьох персонажів на акаунт, хто перший прийшов, той і зайняв. Це не ранній доступ до гри.')]},
                {'id': 'surname', 'q': t('Зачем фамилия и можно ли взять то же имя, что у друга?', 'Why a surname, and can two people share a name?', 'Навіщо прізвище і чи можна взяти те саме ім’я, що в друга?'),
                 'a': [t('Реалмов нет, поэтому уникальным должно быть полное имя во всём регионе. Одно имя у двоих возможно, если фамилии разные. Фамилию можно скрыть: Esc → Options → Nameplates → My Secondary Name.',
                         'There are no realms, so the full name must be unique across the whole region. Two players can share a first name if their surnames differ. You can hide the surname: Esc → Options → Nameplates → My Secondary Name.',
                         'Реалмів немає, тому унікальним має бути повне ім’я у всьому регіоні. Одне ім’я у двох можливе, якщо прізвища різні. Прізвище можна приховати: Esc → Options → Nameplates → My Secondary Name.')]},
                {'id': 'skyborne', 'q': t('Что такое Скайборн?', 'What is Skyborne?', 'Що таке Скайборн?'),
                 'a': [t('Новая раса Forever, открывается любым из трёх наборов. Доступна обеим фракциям, фракция выбирается при создании. Обе ветки знают дарнасский, а стартовая зона Zephras Isle общая.',
                         'The new Forever race, unlocked by any of the three packs. Playable for both factions, the faction is chosen at character creation. Both branches know Darnassian and share the Zephras Isle starting zone.',
                         'Нова раса Forever, відкривається будь-яким із трьох наборів. Доступна за обидві фракції, фракцію обирають під час створення. Обидві гілки знають дарнаську, а стартова зона Zephras Isle спільна.')]},
                {'id': 'levels', 'q': t('До какого уровня качаться и где?', 'What is the level cap, and where do we level?', 'До якого рівня качатися і де?'),
                 'a': [t('До 60, в [[Восточных королевствах|Eastern Kingdoms]] и [[Калимдоре|Kalimdor]]. Летающих скакунов и масштабирования уровней нет, как и в Classic.',
                         'Up to 60, in the Eastern Kingdoms and Kalimdor. No flying mounts and no level scaling, as in Classic.',
                         'До 60, у Eastern Kingdoms і Kalimdor. Літаючих скакунів і масштабування рівнів немає, як і в Classic.')]},
                {'id': 'together', 'q': t('Можно ли играть вместе, если выбрали разные режимы?', 'Can we play together in different modes?', 'Чи можна грати разом, якщо обрали різні режими?'),
                 'a': [t('Нет: группироваться можно только внутри одного режима. Режимы на старте: обычный, PvP, RP и RP-PvP, Hardcore запустят позже. В PvP на аккаунте может быть только одна фракция.',
                         'No: you can only group within one mode. Modes at launch: Normal, PvP, RP and RP-PvP, Hardcore comes later. In PvP an account can have only one faction.',
                         'Ні: групуватися можна лише в межах одного режиму. Режими на старті: звичайний, PvP, RP і RP-PvP, Hardcore запустять пізніше. У PvP на акаунті може бути лише одна фракція.')]},
                {'id': 'group-choice', 'q': t('Какой регион, режим и фракцию выбрать, чтобы играть с друзьями?', 'Which region, mode and faction should we pick to play with friends?', 'Який регіон, режим і фракцію обрати, щоб грати з друзями?'),
                 'a': [t('Одни и те же на всех. Регионы разделены, межрегиональной игры нет, поэтому берите регион с лучшим пингом для большинства. Группа собирается только внутри одного режима, а Альянс и Орда не встают в одну группу ни в каком режиме. В PvP на аккаунте одна фракция, так что договоритесь о ней до резерва имён 27.10.',
                         'The same for everyone. Regions are separate and there is no cross-region play, so pick the region with the best ping for most of you. Groups form only within one mode, and Alliance and Horde cannot group in any mode. In PvP an account has only one faction, so agree on it before name reservation opens on 27.10.',
                         'Однакові для всіх. Регіони розділені, міжрегіональної гри немає, тож беріть регіон із найкращим пінгом для більшості. Група збирається лише в межах одного режиму, а Альянс і Орда не стають в одну групу в жодному режимі. У PvP на акаунті одна фракція, тож домовтеся про неї до бронювання імен 27.10.')]},
                {'id': 'servers', 'q': t('Какие серверы и есть ли русские?', 'Which servers are there, and are there language servers?', 'Які сервери і чи є окремі мовні?'),
                 'a': [t('Реалмов нет: в каждом регионе по одному серверу на режим (обычный, PvP, RP, RP-PvP), игроков разводят слои. Регионы: Америка и Океания, Европа, Корея, Тайвань. Отдельных русских серверов нет, русский язык выбирают в настройках клиента.',
                         'There are no realms: each region has one server per mode (Normal, PvP, RP, RP-PvP), and layers split the players. Regions: Americas and Oceania, Europe, Korea, Taiwan. There are no separate language servers: the language is set in the client.',
                         'Реалмів немає: у кожному регіоні по одному серверу на режим (звичайний, PvP, RP, RP-PvP), гравців розводять шари. Регіони: Америка й Океанія, Європа, Корея, Тайвань. Окремих мовних серверів немає, мову обирають у налаштуваннях клієнта.')]},
                {'id': 'where', 'q': t('Где найти группу?', 'Where do I find a group?', 'Де знайти групу?'),
                 'a': [t('На сайте и в Discord. Войдите, добавьте персонажа и отметьте в профиле «Ищу группу»: на 3 часа он появится в полосе «Сейчас ищут группу» на странице «Игроки». На Discord-сервере Gabella Team собирают группы на старт 04.11 и договариваются о регионе, режиме и фракции.',
                         'On this site and on Discord. Log in, add a character and turn on “Looking for group” in your profile: for 3 hours it shows in the “Looking for a group now” strip on the Players page. On the Gabella Team Discord server groups form for the 04.11 launch, and players agree on region, mode and faction.',
                         'На сайті та в Discord. Увійдіть, додайте персонажа й позначте в профілі «Шукаю групу»: на 3 години він з’явиться в смузі «Зараз шукають групу» на сторінці «Гравці». На Discord-сервері Gabella Team збирають групи на старт 04.11 і домовляються про регіон, режим і фракцію.')],
                 'link': (t('Discord Gabella Team', 'Gabella Team Discord', 'Discord Gabella Team'), DISCORD_AT['faq'])},
                {'id': 'profile', 'q': t('Что такое ранг и рамки в профиле?', 'What are rank and frames in the profile?', 'Що таке ранг і рамки в профілі?'),
                 'a': [t('Это ваш профиль на сайте, к самой игре он не относится.',
                         'This is your profile on the site; it has nothing to do with the game itself.',
                         'Це ваш профіль на сайті, до самої гри він не стосується.'),
                       t('Ранг растёт от очков достижений и открывает рамки портрета. Особые рамки дают особые достижения.',
                         'Rank grows from achievement points and unlocks portrait frames. Special frames come from special achievements.',
                         'Ранг росте від очок досягнень і відкриває рамки портрета. Особливі рамки дають особливі досягнення.')]},
                {'id': 'raids', 'q': t('Когда откроются рейды?', 'When do raids open?', 'Коли відкриються рейди?'),
                 'a': [t('09.12: Barrow Deeps (10 игроков), Hyjal Summit (20), Onyxia’s Lair (40). До этого есть пять недель на прокачку и подземелья.',
                         '09.12: Barrow Deeps (10 players), Hyjal Summit (20), Onyxia’s Lair (40). Until then you have five weeks for leveling and dungeons.',
                         '09.12: Barrow Deeps (10 гравців), Hyjal Summit (20), Onyxia’s Lair (40). До цього є п’ять тижнів на прокачування та підземелля.')]},
                {'id': 'beta', 'q': t('Можно ли ещё попасть в бету?', 'Can I still get into the beta?', 'Чи можна ще потрапити в бету?'),
                 'a': [t('Нет. Доступ был у владельцев Epic и Collection. Бета завершилась 23.10 в 10:00 по тихоокеанскому времени.',
                         'No. Access was for Epic and Collection owners. The beta ended on 23.10 at 10:00 Pacific time.',
                         'Ні. Доступ мали власники Epic і Collection. Бета завершилася 23.10 о 10:00 за тихоокеанським часом.')]},
                {'id': 'classic-guides', 'q': t('Подойдут ли старые гайды по Classic?', 'Are old Classic guides still useful?', 'Чи підійдуть старі гайди по Classic?'),
                 'a': [t('Только частично. Характеристики и предметы изменены, поэтому старые списки добычи ненадёжны. Добавлены 9 новых подземелий, 2 новых рейда и Onyxia’s Lair, новые зоны и задания, у классов обновлены таланты.',
                         'Only partly. Stats and items were changed, so old loot lists are unreliable. There are 9 new dungeons, 2 new raids plus Onyxia’s Lair, new zones and quests, and class talents were updated.',
                         'Лише частково. Характеристики та предмети змінено, тому старі списки здобичі ненадійні. Додано 9 нових підземель, 2 нові рейди та Onyxia’s Lair, нові зони та завдання, у класів оновлено таланти.')]},
                {'id': 'visuals', 'q': t('Будет ли современная графика и геймпад?', 'Is there modern graphics and gamepad support?', 'Чи буде сучасна графіка та геймпад?'),
                 'a': [t('Да: при первом входе выбирают набор Classic или Enhanced (модели HD, цели заданий на карте, одна сумка, трансмогрификация), потом каждую настройку можно поменять. Есть официальная поддержка геймпада.',
                         'Yes: on first login you pick the Classic or Enhanced set (HD models, quest objectives on the map, one bag, transmog), and each setting can be changed later. There is official gamepad support.',
                         'Так: під час першого входу обирають набір Classic або Enhanced (моделі HD, цілі завдань на мапі, одна сумка, трансмогрифікація), потім кожне налаштування можна змінити. Є офіційна підтримка геймпада.')]},
                {'id': 'requirements', 'q': t('Какие системные требования?', 'What are the system requirements?', 'Які системні вимоги?'),
                 'a': [t('Минимум: Windows 10 64-bit, 4 ядра 3,0 ГГц, 8 ГБ ОЗУ, видеокарта DirectX 12 на 4 ГБ (GeForce GTX 10, RDNA 1) и 128 ГБ на SSD. На Mac — macOS 12 и Apple M2. Полная таблица — на странице требований.',
                         'Minimum: Windows 10 64-bit, 4 cores at 3.0 GHz, 8 GB RAM, a DirectX 12 GPU with 4 GB (GeForce GTX 10, RDNA 1) and 128 GB on an SSD. On Mac: macOS 12 and Apple M2. The full table is on the requirements page.',
                         'Мінімум: Windows 10 64-bit, 4 ядра 3,0 ГГц, 8 ГБ ОЗП, відеокарта DirectX 12 на 4 ГБ (GeForce GTX 10, RDNA 1) і 128 ГБ на SSD. На Mac — macOS 12 і Apple M2. Повна таблиця — на сторінці вимог.')],
                 'link': (t('Системные требования', 'System requirements', 'Системні вимоги'), '../requirements/')},
            ]),
        ]},
    ],
})

# ---------- Системные требования: по магазину Battle.net, видеокарты — по новости Blizzard ----------

SHOP = 'https://eu.shop.battle.net/en-gb/product/world-of-warcraft-forever'
SSD = t('SSD, 128 ГБ свободно', 'SSD, 128 GB free', 'SSD, 128 ГБ вільно')
RAM8, RAM16 = t('8 ГБ', '8 GB', '8 ГБ'), t('16 ГБ', '16 GB', '16 ГБ')
REQ_HEAD = ['', t('Минимум', 'Minimum', 'Мінімум'), t('Рекомендуется', 'Recommended', 'Рекомендовано')]

GUIDES.append({
    'slug': 'requirements', 'art': 'hero_requirements', 'hero': 'hero_requirements',
    'title': t('Системные требования', 'System requirements', 'Системні вимоги'),
    'lead': t('Минимальные и рекомендуемые требования WoW Forever для Windows и Mac по магазину Battle.net и какие видеокарты больше не поддерживаются.',
              'Minimum and recommended WoW Forever requirements for Windows and Mac from the Battle.net shop, and which graphics cards are no longer supported.',
              'Мінімальні й рекомендовані вимоги WoW Forever для Windows і Mac за магазином Battle.net і які відеокарти більше не підтримуються.'),
    'tile': t('ПК и Mac: минимум, рекомендуемые, видеокарты', 'PC and Mac: minimum, recommended, graphics cards', 'ПК і Mac: мінімум, рекомендовані, відеокарти'),
    'pills': [t('SSD 128 ГБ', 'SSD 128 GB', 'SSD 128 ГБ'), t('Минимум 8 ГБ ОЗУ', '8 GB RAM minimum', 'Мінімум 8 ГБ ОЗП'),
              t('Windows и Mac', 'Windows and Mac', 'Windows і Mac')],
    'sources': [
        (t('Battle.net: системные требования WoW Forever', 'Battle.net: WoW Forever system requirements', 'Battle.net: системні вимоги WoW Forever'), SHOP),
        (t('Blizzard: требования к видеокартам', 'Blizzard: graphics card requirements', 'Blizzard: вимоги до відеокарт'),
         'https://news.blizzard.com/en-us/article/24301512'),
        (t('Warcraft Tavern: установка Forever', 'Warcraft Tavern: installing Forever', 'Warcraft Tavern: встановлення Forever'),
         'https://www.warcrafttavern.com/forever/guides/beta/'),
    ],
    'sections': [
        {'id': 'windows', 'title': 'Windows', 'blocks': [
            ('table', {'head': REQ_HEAD, 'rows': [
                [t('Система', 'System', 'Система'),
                 t('Windows 10 64-bit (обновление May 2019 или новее)', 'Windows 10 64-bit (May 2019 Update or newer)', 'Windows 10 64-bit (оновлення May 2019 або новіше)'), 'Windows 11'],
                [t('Процессор', 'Processor', 'Процесор'),
                 t('4 ядра, 3,0 ГГц: Intel Core Haswell, AMD Ryzen Zen', '4 cores, 3.0 GHz: Intel Core Haswell, AMD Ryzen Zen', '4 ядра, 3,0 ГГц: Intel Core Haswell, AMD Ryzen Zen'),
                 t('8 производительных ядер до 5,2 ГГц: Intel Core Ultra (Series 2), AMD Ryzen Zen 5',
                   '8 performance cores, 5.2 GHz boost: Intel Core Ultra (Series 2), AMD Ryzen Zen 5',
                   '8 продуктивних ядер до 5,2 ГГц: Intel Core Ultra (Series 2), AMD Ryzen Zen 5')],
                [t('Видеокарта', 'Graphics', 'Відеокарта'),
                 t('DirectX 12, 4 ГБ: GeForce GTX 10, AMD RDNA 1, Intel Iris Xe2 (Lunar Lake)', 'DirectX 12, 4 GB: GeForce GTX 10, AMD RDNA 1, Intel Iris Xe2 (Lunar Lake)',
                   'DirectX 12, 4 ГБ: GeForce GTX 10, AMD RDNA 1, Intel Iris Xe2 (Lunar Lake)'),
                 t('DirectX 12, 8 ГБ: GeForce RTX 40, AMD RDNA 3, Intel Arc B', 'DirectX 12, 8 GB: GeForce RTX 40, AMD RDNA 3, Intel Arc B',
                   'DirectX 12, 8 ГБ: GeForce RTX 40, AMD RDNA 3, Intel Arc B')],
                [t('Память', 'Memory', 'Пам’ять'), RAM8, RAM16],
                [t('Диск', 'Storage', 'Диск'), SSD, SSD],
                [t('Экран', 'Display', 'Екран'), '1280 × 720', '1280 × 720'],
                [t('Управление', 'Input', 'Керування'), t('Клавиатура и мышь', 'Keyboard and mouse', 'Клавіатура й миша'),
                 t('Мышь с колесом и доп. кнопками', 'Multi-button mouse with a wheel', 'Миша з колесом і дод. кнопками')],
            ]}),
        ]},
        {'id': 'mac', 'title': 'Mac', 'blocks': [
            ('table', {'head': REQ_HEAD, 'rows': [
                [t('Система', 'System', 'Система'), 'macOS 12', 'macOS 15'],
                [t('Процессор', 'Processor', 'Процесор'),
                 t('Apple M2 или Intel Core 9-го поколения (Coffee Lake)', 'Apple M2 or 9th generation Intel Core (Coffee Lake)', 'Apple M2 або Intel Core 9-го покоління (Coffee Lake)'), 'Apple M4'],
                [t('Видеокарта', 'Graphics', 'Відеокарта'), t('Metal, 4 ГБ; Apple M2 с 8 ГБ', 'Metal, 4 GB; Apple M2 with 8 GB', 'Metal, 4 ГБ; Apple M2 з 8 ГБ'),
                 t('Apple M4 с 16 ГБ', 'Apple M4 with 16 GB', 'Apple M4 з 16 ГБ')],
                [t('Память', 'Memory', 'Пам’ять'), RAM8, RAM16],
                [t('Диск', 'Storage', 'Диск'), SSD, SSD],
            ]}),
        ]},
        {'id': 'gpu', 'title': t('Старые видеокарты', 'Older graphics cards', 'Старі відеокарти'), 'blocks': [
            ('text', [t('Новому виду мира нужна функция, которой нет у старых видеокарт, поэтому с выходом Forever их поддержка закончилась. Видеокарта должна быть на одной из этих архитектур или новее:',
                        'The new look of the world needs a feature that older graphics cards lack, so their support ends with the Forever launch. Your card must be on one of these architectures or newer:',
                        'Новому вигляду світу потрібна функція, якої немає у старих відеокарт, тому з виходом Forever їх підтримка закінчується. Відеокарта має бути на одній із цих архітектур або новішій:')]),
            ('table', {'head': [t('Производитель', 'Maker', 'Виробник'), t('Не старше', 'This or newer', 'Не старша'), t('Запустится', 'Will start', 'Запуститься'),
                                t('Не запустится', 'Will not start', 'Не запуститься')], 'rows': [
                ['AMD', 'Graphics Core Next 1 (2012)', 'Radeon HD 7850', 'Radeon HD 6950'],
                ['NVIDIA', 'Maxwell (2014)', '—', 'GeForce GTX 760'],
                ['Intel', 'Skylake (2015)', 'HD Graphics 530', '—'],
            ]}),
            ('tip', t('Такая видеокарта только запускает игру, до минимума выше ей далеко. Покупать железо стоит по столбцу «Минимум».',
                      'Such a card only starts the game and is still far below the minimum above. When buying hardware, go by the Minimum column.',
                      'Така відеокарта лише запускає гру, до мінімуму вище їй далеко. Купувати залізо варто за стовпцем «Мінімум».')),
            ('text', [t('Для игры нужны интернет, учётная запись и приложение Battle.net. Forever ставится отдельно, даже если другие версии WoW уже установлены.',
                        'You need an internet connection, a Battle.net account and the Battle.net app. Forever installs separately even if other WoW versions are already installed.',
                        'Для гри потрібні інтернет, обліковий запис і застосунок Battle.net. Forever встановлюється окремо, навіть якщо інші версії WoW уже встановлено.')]),
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
    'slug': 'dungeons', 'art': 'warlock', 'hero': 'hero_dungeons', 'js': 'dungeons',
    'title': t('Подземелья и рейды', 'Dungeons and raids', 'Підземелля та рейди'),
    'lead': t('Все 35 подземелий по уровням с фильтром под вашего персонажа, три рейда и состав группы под любое число друзей.',
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
                 'd': t('Подземелья рассчитаны на свои уровни, а протаскивать отставшего друга Blizzard сделала невыгодным.', 'Dungeons are built for their own levels, and Blizzard made boosting a friend who lags behind unprofitable.',
                        'Підземелля розраховані на свої рівні, а протягувати друга, що відстав, Blizzard зробила невигідним.')},
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
    'slug': 'leveling', 'art': 'hero_leveling', 'hero': 'hero_leveling',
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
        {'id': 'first', 'title': t('Первый час', 'First hour', 'Перша година'), 'blocks': [
            ('steps', [
                {'t': t('До старта', 'Before launch', 'До старту'),
                 'd': t('Решите с друзьями регион, режим и фракцию: группа собирается только внутри режима, регионы разделены. Владельцы наборов занимают имена с 27.10.',
                        'Agree on region, mode and faction with your friends: groups form only within a mode, and regions are separate. Pack owners can claim names from 27.10.',
                        'Вирішіть із друзями регіон, режим і фракцію: група збирається лише всередині режиму, регіони розділені. Власники наборів займають імена з 27.10.')},
                {'t': t('Старт', 'Launch', 'Старт'),
                 'd': t('04.11 в 15:00 по тихоокеанскому, это 23:00 UTC.', '04.11 at 15:00 Pacific, which is 23:00 UTC.', '04.11 о 15:00 за тихоокеанським, це 23:00 UTC.')},
                {'t': t('Стартовая зона', 'Starting zone', 'Стартова зона'),
                 'd': t('Задания стартовой зоны своей расы до 10 уровня, дальше — маршрут ниже. Таланты открываются на 10 уровне.',
                        'Your race’s starting zone quests up to level 10, then the route below. Talents unlock at level 10.',
                        'Завдання стартової зони своєї раси до 10 рівня, далі — маршрут нижче. Таланти відкриваються на 10 рівні.')},
                {'t': t('Кулинария сразу', 'Cooking right away', 'Кулінарія одразу'),
                 'd': t('Костёр по Кулинарии становится лагерем: 140 навыка дают 5 мест, 220 — 10. Готовая еда даёт +5% опыта за врагов.',
                        'A Cooking campfire becomes a camp: 140 skill gives 5 slots, 220 gives 10. Cooked food gives +5% experience from enemies.',
                        'Вогнище з Кулінарії стає табором: 140 навички дають 5 місць, 220 — 10. Готова їжа дає +5% досвіду за ворогів.')},
                {'t': t('Две профессии', 'Two professions', 'Дві професії'),
                 'd': t('Травничество, Горное дело и Снятие шкур кормят деньгами и ставят свои объекты в лагере. Пары под класс — в гайде по профессиям.',
                        'Herbalism, Mining and Skinning bring in money and place their own camp objects. Pairs for your class are in the professions guide.',
                        'Травництво, Гірництво та Знімання шкур дають гроші й ставлять свої об’єкти в таборі. Пари під клас — у гайді з професій.')},
                {'t': t('Выход из игры', 'Logging out', 'Вихід із гри'),
                 'd': t('В таверне или столице: копится отдых, и следующий вечер начнётся с двойного опыта за врагов.',
                        'In an inn or a capital: rest builds up, and the next evening starts with double experience from enemies.',
                        'У таверні чи столиці: накопичується відпочинок, і наступний вечір почнеться з подвійного досвіду за ворогів.')},
            ]),
        ]},
        {'id': 'route', 'title': t('Маршрут по зонам', 'Zone route', 'Маршрут зонами'), 'blocks': [
            ('play', {'h': t('Играете прямо сейчас?', 'Playing right now?', 'Граєте просто зараз?'),
                      'd': t('Откройте «В игре» на телефоне или втором мониторе: зоны под ваш уровень, подземелья, таймеры и радио.',
                             'Open “In game” on your phone or a second monitor: zones for your level, dungeons, timers and radio.',
                             'Відкрийте «У грі» на телефоні або другому моніторі: зони під ваш рівень, підземелля, таймери й радіо.'),
                      'go': t('Открыть «В игре»', 'Open “In game”', 'Відкрити «У грі»')}),
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
                 'd': t('С 40 уровня: обучение 100 золотых и скакун 20 (скорость +60%). На 60: 1000 и 200 золотых (+100%). При Почёте у своей фракции скидка 10%. Паладин и Чернокнижник получают скакуна заданиями класса.',
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
                                'href': 'guides/dungeons/', 'art': 'hero_dungeons'}]),
                ]},
            ]),
            ('tiles', [{'t': t('Тир-лист классов WoW Forever', 'WoW Forever Class Tier List', 'Тір-лист класів WoW Forever'), 'd': t('Сильные классы и спеки по данным беты', 'Strong classes and specs by beta data', 'Сильні класи й спеціалізації за даними бети'), 'href': 'guides/tier-list/', 'art': 'hero_classes'}]),
        ]},
        {'id': 'legacy', 'title': t('Система Legacy', 'Legacy system', 'Система Legacy'), 'blocks': [
            ('text', [t('Legacy — прогресс на весь аккаунт Battle.net. Очки дают за испытания: уровни, профессии, PvP, подземелья и рейды. Тратите их на перки отдельно на каждом персонаже, на старте до 16 очков.', 'Legacy is progress shared across your whole Battle.net account. Challenges give you points: levels, professions, PvP, dungeons and raids. You spend them on perks separately on each character, up to 16 points at launch.', 'Legacy — прогрес на весь обліковий запис Battle.net. Очки дають за випробування: рівні, професії, PvP, підземелля та рейди. Витрачаєте їх на перки окремо на кожному персонажі, на старті до 16.')]),
            ('tiles', [{'t': t('Система Legacy', 'The Legacy System', 'Система Legacy'), 'd': t('Очки, испытания, перки и награды', 'Points, challenges, perks and rewards', 'Очки, випробування, перки та нагороди'), 'href': 'guides/legacy/', 'art': 'hero_guides'}]),
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
                {'t': t('Места', 'Slots', 'Місця'),
                 'd': t('Базовый костёр доступен без Кулинарии, на 3 объекта. Кулинария 140 даёт 5 мест, 220 — 10.',
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
                [t('Инженерное дело', 'Engineering', 'Інженерія'), 'Reagent Bot', t('торговец, на 2 уровне ремонт (Repair Bot)', 'a vendor, at level 2 repairs (Repair Bot)', 'торговець, на 2 рівні ремонт (Repair Bot)')],
                [t('Кулинария', 'Cooking', 'Кулінарія'), 'Basic Campfire', t('без баффа, добавляет места в лагере', 'no buff, adds camp slots', 'без баффа, додає слоти табору')],
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
    'eng': (t('Инженерное дело + Горное дело', 'Engineering + Mining', 'Інженерія + Гірництво'),
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
    ('druid', t('Друид', 'Druid', 'Друїд'), [('alch', None), ('lw', None)]),
]


def _pair_tabs():
    return [{'id': cid, 't': name, 'blocks': [('steps', [{'t': PAIRS[p][0], 'd': why or PAIRS[p][1]} for p, why in pairs])]}
            for cid, name, pairs in CLASS_PAIRS]


GUIDES.append({
    'slug': 'professions', 'art': 'hero_campfire', 'hero': 'hero_professions', 'js': 'professions',
    'title': t('Профессии', 'Professions', 'Професії'),
    'lead': t('Какие две профессии взять под ваш класс, что каждая ставит в лагерь и как прокачать навык до 300.',
              'Which two professions suit your class, what each one places in camp and how to raise the skill to 300.',
              'Які дві професії взяти під ваш клас, що кожна ставить у табір і як прокачати навичку до 300.'),
    'tile': t('Пары под класс, объекты лагеря, навык до 300', 'Pairs for your class, camp objects, skill to 300', 'Пари під клас, об’єкти табору, навичка до 300'),
    'pills': [t('2 основные + 3 вспомогательные', '2 primary + 3 secondary', '2 основні + 3 допоміжні'), t('Навык до 300', 'Skill to 300', 'Навичка до 300'),
              t('36 объектов лагеря', '36 camp objects', '36 об’єктів табору')],
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
            ('tip', t('Кулинарию, Первую помощь и Рыбалку берут все: это вспомогательные профессии, можно взять все три, и забыть их нельзя. Пусть кто-то в группе поднимет Кулинарию до 220 ради 10 мест в лагере.',
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
            ('table', {'head': [t('Ступень', 'Rank', 'Ступінь'), t('С уровня персонажа', 'From hero level', 'З рівня персонажа'), t('Навык до', 'Skill up to', 'Навичка до')], 'rows': [
                [t('Ученик', 'Apprentice', 'Apprentice'), t('1 для сбора, 5 для ремёсел', '1 for gathering, 5 for crafts', '1 для збирання, 5 для ремесел'), '75'],
                [t('Подмастерье', 'Journeyman', 'Journeyman'), '10', '150'],
                [t('Умелец', 'Expert', 'Expert'), '20', '225'],
                [t('Искусник', 'Artisan', 'Artisan'), '35', '300'],
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
                {'t': t('Искусник', 'Artisan', 'Artisan'),
                 'd': t('Ступень Искусника даёт только особый учитель, а у вспомогательных профессий — особое задание.',
                        'Artisan comes only from special trainers, or from a special quest for secondary professions.',
                        'Ступінь Artisan дають лише особливі вчителі, а для допоміжних професій особливе завдання.')},
                {'t': t('Окно профессий', 'Professions window', 'Вікно професій'),
                 'd': t('Своё окно на клавише K: рецепты можно искать, фильтровать и отслеживать как список покупок. Для сумки с реагентами есть отдельная ячейка.',
                        'Its own window on the K key: recipes can be searched, filtered and tracked as a shopping list. Reagent bags have their own slot.',
                        'Своє вікно на клавіші K: рецепти можна шукати, фільтрувати й відстежувати як список покупок. Для сумки з реагентами є окремий слот.')},
            ]),
            ('tip', t('Если отказаться от профессии, весь её прогресс пропадёт, а игра просит подтвердить это вводом слова. Пассивных бонусов у профессий в Forever нет: польза в том, что вы делаете и собираете, и в баффах лагеря.',
                      'Unlearning a profession wipes all its progress, and the game asks you to type a confirmation. Professions in Forever have no passive bonuses: the value is in what you craft and gather, and in camp buffs.',
                      'Розучивши професію, ви втрачаєте весь її прогрес, а гра просить підтвердити це введенням слова. Пасивних бонусів у професій у Forever немає: користь у тому, що ви робите й збираєте, і в баффах табору.')),
        ]},
    ],
})

# ---------- Новости: наши записи (новые сверху) + автолента Wowhead из assets/news.json ----------

NEWS += [
    {'date': '2026-10-23', 'url': 'https://teamoverpowered.com/forever/guides/name-reservation/',
     'title': t('Бета закрыта, дальше — имена с 27.10', 'Beta closed, next up: names from 27.10', 'Бету закрито, далі — імена з 27.10'),
     'text': t('Закрытая бета закрылась 23.10 в 10:00 по тихоокеанскому времени (17:00 UTC). С 27.10 по 03.11 владельцы Heroic, Epic и Collection резервируют до трёх имён на аккаунт, кто первым пришёл, тот и занял.',
               'The closed beta went offline on 23.10 at 10:00 Pacific time (17:00 UTC). From 27.10 to 03.11 Heroic, Epic and Collection owners reserve up to three names per account, first come, first served.',
               'Закрита бета вимкнулася 23.10 о 10:00 за тихоокеанським часом (17:00 UTC). З 27.10 по 03.11 власники Heroic, Epic і Collection резервують до трьох імен на акаунт, хто перший прийшов, той і зайняв.')},
    {'date': '2026-10-15', 'url': 'https://www.warcrafttavern.com/forever/news/racial-class-ability-changes-in-the-wow-forever-beta/',
     'title': t('Крупный патч беты: расы и классы', 'Major beta patch: races and classes', 'Великий патч бети: раси та класи'),
     'text': t('Способности рас переделаны (оружейные специализации заменены критами), настроены почти все классы. Таблицы рас и классов на сайте уже по этому патчу.',
               'Racial abilities were reworked (weapon specializations replaced with crits), almost all classes were tuned. The race and class tables on this site already follow this patch.',
               'Здібності рас перероблено (спеціалізації зброї замінено критами), налаштовано майже всі класи. Таблиці рас і класів на сайті вже за цим патчем.')},
    {'date': '2026-10-08', 'url': 'https://classicwow.gg/forever',
     'title': t('В бете Даларан и больше опыта в подземельях', 'Dalaran and more dungeon experience in the beta', 'У беті Даларан і більше досвіду в підземеллях'),
     'text': t('В бету добавили [[Даларан|City of Dalaran]] и примерно на 20% больше опыта за врагов в подземельях.',
               'The beta got City of Dalaran and about 20% more experience for enemies in dungeons.',
               'У бету додали City of Dalaran і приблизно на 20% більше досвіду за ворогів у підземеллях.')},
]

GUIDES.append({
    'slug': 'news', 'art': 'paladin', 'hero': 'hero_news', 'js': 'news',
    'title': t('Новости', 'News', 'Новини'),
    'lead': t('Главное о WoW Forever и свежая лента Wowhead.',
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
# Факты: CurseForge и README аддонов (23.10.2026). Без версий и числа скачиваний — они быстро устаревают.

def u(s):
    return {'uk': s}


UAF = 'https://www.curseforge.com/wow/addons/ua-forever'
UALL = 'https://www.curseforge.com/wow/addons/uall-forever-ukrainian-localization'

GUIDES.append({
    'slug': 'ukrainian', 'only': 'uk', 'art': 'hero_ukrainian', 'hero': 'hero_ukrainian',
    'title': u('Як грати українською'),
    'lead': u('Української мови у WoW Forever немає, перекладає гру аддон. Який обрати, як встановити й налаштувати, де побачити оригінал.'),
    'tile': u('Аддони перекладу: який обрати й як встановити'),
    'pills': [u('UA_Forever'), u('UALL Forever'), u('Shift — оригінал')],
    'sources': [
        (u('CurseForge: UA_Forever'), UAF),
        (u('UA_Forever на GitHub: опис і команди'), 'https://github.com/sysrover/UA_Forever'),
        (u('CurseForge: UALL Forever'), UALL),
        (u('ClassicUA на GitHub'), 'https://github.com/greenya/ClassicUA'),
        (u('WoWGuide: мови WoW Forever'), 'https://wowguide.net/en/guides/wow-forever-supported-languages'),
    ],
    'sections': [
        {'id': 'short', 'title': u('Коротко'), 'blocks': [
            ('text', [u('Ставте UA_Forever. Він перекладає завдання, підказки, предмети, заклинання, імена NPC і вікна гри, а речення узгоджує з родом героя: «ви дав» чи «ви дала», залежно від персонажа.'),
                      u('Встановлення через CurseForge займає кілька хвилин. Оригінал англійською завжди під рукою: затисніть Shift.')]),
            ('raw', u(f'<p class="gbtns"><a class="btn" href="{UAF}" target="_blank" rel="noopener">UA_Forever на CurseForge ↗</a>'
                      '<a class="btn ghost" href="#install">Як встановити</a></p>')),
        ]},
        {'id': 'client', 'title': u('Мова гри'), 'blocks': [
            ('text', [u('Клієнт WoW Forever доступний десятьма мовами, серед них англійська та російська. Української серед них немає.'),
                      u('Аддон підміняє тексти лише на вашому екрані. Інші гравці бачать гру своєю мовою, на правила й бої переклад не впливає.'),
                      u('UALL Forever працює лише з англійським клієнтом. Мову змінюють у лаунчері Battle.net: налаштування гри, мова тексту.')]),
        ]},
        {'id': 'choose', 'title': u('UA_Forever чи UALL Forever'), 'blocks': [
            ('text', [u('На CurseForge два аддони українізації Forever з майже однаковою кількістю завантажень. Відрізняються вони сильно.')]),
            ('table', {'head': [u(''), u('UA_Forever'), u('UALL Forever')], 'rows': [
                [u('Основа'), u('ClassicUA: переклад спільноти, над ним працювали понад 30 перекладачів і редакторів'), u('Власний переклад автора')],
                [u('Обсяг'), u('Завдання, предмети, заклинання, аури, репліки NPC, книги, вікна'), u('Те саме, але предметів перекладено майже вчетверо менше')],
                [u('Рід героя'), u('Форми за статтю персонажа: «дав» або «дала»'), u('Завжди чоловічий рід')],
                [u('Назви'), u('Перекладені: Залізогарт, Підмістя, Молотобій'), u('Транслітерація: Айронфордж, Андерсіті, Гаммерфолл')],
                [u('Оригінал'), u('Shift у підказці, EN/UA у діалогах завдань'), u('Shift')],
                [u('Мова клієнта'), u('Вимог не вказано'), u('Лише англійська')],
                [u('Налаштування'), u('Налаштування → Додатки → UA Forever, команда /uaf'), u('Esc → Options → AddOns → UALLF, команда /uallfua')],
                [u('Код'), u('Відкритий, ліцензія GPLv3'), u('Закритий')],
            ]}),
            ('text', [u('UA_Forever перекладає більше й звучить природніше завдяки родам і перекладеним назвам. Слабкі місця: місцями дослівний текст, поодинокі помилки, у цілях завдань звертання на «ви» при «ти» в самому тексті.'),
                      u('UALL Forever читається рівніше, але назви транслітом, у предметах трапляються Англійські Великі Літери, а переклад і транслітерація змішуються: Пустограй поруч зі Срібноліссям.')]),
            ('tip', u('На цьому сайті ігрові назви англійською, як в оригінальному клієнті: так їх пишуть Wowhead, гайди й гравці в групі. Затисніть Shift на підказці, щоб звірити назву з аддоном.')),
        ]},
        {'id': 'install', 'title': u('Встановлення'), 'blocks': [
            ('steps', [
                {'t': u('CurseForge'), 'd': u('Встановіть застосунок CurseForge, оберіть World of Warcraft і версію Forever. Знайдіть UA_Forever і натисніть Install, оновлення застосунок ставитиме сам.')},
                {'t': u('Або вручну'), 'd': u('Завантажте архів зі сторінки аддона й розпакуйте так, щоб папка UA_Forever опинилася в Interface\\AddOns у теці гри Forever.')},
                {'t': u('Увімкнення'), 'd': u('На екрані вибору персонажа відкрийте AddOns і поставте позначку. Якщо аддон позначено застарілим, увімкніть Load out of date AddOns.')},
                {'t': u('Перевірка'), 'd': u('Якщо гра вже запущена, введіть /reload у чаті. Підказки й вікна завдань мають стати українськими.')},
            ]),
            ('tip', u('Вмикайте один аддон перекладу. Обидва підміняють ті самі вікна й заважають один одному.')),
        ]},
        {'id': 'setup', 'title': u('Налаштування й оригінал'), 'blocks': [
            ('table', {'head': [u(''), u('UA_Forever'), u('UALL Forever')], 'rows': [
                [u('Побачити оригінал'), u('Затиснути Shift на підказці'), u('Затиснути Shift')],
                [u('Діалог завдання англійською'), u('Перемикач EN/UA у вікні діалогу'), u('Shift')],
                [u('Увімкнути чи вимкнути переклад'), u('/uaf on, /uaf off'), u('Перемикачі в Esc → Options → AddOns → UALLF')],
                [u('Стан перекладу'), u('/uaf status'), u('/uallfua')],
                [u('Вимкнути окремі частини'), u('Налаштування → Додатки → UA Forever'), u('/uallfua list')],
            ]}),
        ]},
        {'id': 'help', 'title': u('Неперекладений текст'), 'blocks': [
            ('text', [u('Forever змінює частину класичних завдань і заклинань, тому старий переклад місцями відстає, а нові тексти з’являються з оновленнями аддона.'),
                      u('UA_Forever збирає неперекладене сам. У налаштуваннях аддона увімкніть автоскан і пограйте. Там само відкрийте зібрані дані, скопіюйте їх і надішліть через форму, посилання на яку є на сторінці аддона на GitHub. Без вас нічого не відправляється.')]),
        ]},
        {'id': 'questions', 'title': u('Часті питання'), 'blocks': [
            ('faq', [
                {'id': 'ban', 'q': u('Чи можуть заблокувати за аддон перекладу?'),
                 'a': [u('Аддони інтерфейсу Blizzard дозволяє. Перекладач лише змінює текст на вашому екрані й не автоматизує гру.')]},
                {'id': 'others', 'q': u('Чи побачать переклад інші гравці?'),
                 'a': [u('Ні, переклад працює тільки у вас. Назви в чаті групи пишіть англійською: так їх зрозуміють усі.')]},
                {'id': 'outdated', 'q': u('Після патча аддон позначено застарілим. Що робити?'),
                 'a': [u('Увімкніть Load out of date AddOns на екрані вибору персонажа й оновіть аддон через CurseForge, коли вийде нова версія.')]},
                {'id': 'russian', 'q': u('Чи працює UA_Forever з російським клієнтом?'),
                 'a': [u('Автор вимог до мови клієнта не вказує. Якщо частина тексту лишається неперекладеною, поставте англійську мову в лаунчері Battle.net.')]},
            ]),
        ]},
    ],
})

# ---------- Лучшая раса, тир-лист и Legacy (тексты 25.10.2026, переводы в i18n/*.json) ----------

# ---------- best-race ----------

GUIDES.append({
    'slug': 'best-race', 'art': 'hero_races', 'hero': 'hero_races',
    'title': t('Лучшая раса для каждого класса', 'Best Race for Every Class', 'Найкраща раса для кожного класу'),
    'lead': t('За Альянс чаще всего выигрывают Человек, Гном и Ночной эльф, за Орду — Орк в PvE и Нежить в PvP. Разница между расами — несколько процентов: класс, спек и экипировка важнее.', 'On the Alliance side Human, Gnome and Night Elf win most often; on the Horde side it is Orc in PvE and Undead in PvP. The gap between races is a few percent: class, spec and gear matter more.', 'За Альянс найчастіше перемагають Людина, Гном і Нічний ельф, за Орду — Орк у PvE та Нежить у PvP. Різниця між расами становить кілька відсотків: клас, спеціалізація й екіпірування важать більше.'),
    'tile': t('Какая раса сильнее для вашего класса', 'Which race is stronger for your class', 'Яка раса сильніша для вашого класу'),
    'pills': [t('56 пар класс и раса', '56 class and race pairs', '56 пар клас і раса'), t('PvE и PvP', 'PvE and PvP', 'PvE та PvP'), t('По бете', 'Beta data', 'За бетою')],
    'sources': [
        (t('Warcraft Tavern: расовые способности', 'Warcraft Tavern: racial abilities', 'Warcraft Tavern: расові здібності'), 'https://www.warcrafttavern.com/forever/guides/races/'),
        (t('Warcraft Tavern: изменения беты от 15 октября', 'Warcraft Tavern: Oct 15 beta changes', 'Warcraft Tavern: зміни бети від 15 жовтня'), 'https://www.warcrafttavern.com/forever/news/racial-class-ability-changes-in-the-wow-forever-beta/'),
        (t('RankedBoost: расы по классам', 'RankedBoost: races by class', 'RankedBoost: раси за класами'), 'https://rankedboost.com/world-of-warcraft/forever/tier-list/'),
        (t('wowforevertierlist: лучшая раса для класса', 'wowforevertierlist: best race for each class', 'wowforevertierlist: найкраща раса для класу'), 'https://wowforevertierlist.com/races/best-race-for-each-class'),
        (t('ConquestCapped: тир-лист рас', 'ConquestCapped: race tier list', 'ConquestCapped: тір-лист рас'), 'https://conquestcapped.com/guides/wow-forever/wow-forever-race-tier-list/'),
        (t('mmonster: тир-лист рас', 'mmonster: race tier list', 'mmonster: тір-лист рас'), 'https://mmonster.co/wow-forever/guides/tier-lists/race-tier-list'),
        (t('GamesFuze: лучшая раса для класса', 'GamesFuze: best race for each class', 'GamesFuze: найкраща раса для класу'), 'https://gamesfuze.com/tier-list/world-of-warcraft-forever-best-race-for-every-class/'),
        (t('gamer-guides: тир-лист беты', 'gamer-guides: beta tier list', 'gamer-guides: тір-лист бети'), 'https://gamer-guides.com/warcraft-forever/tier-list-beta/'),
        (t('Wowhead Classic: Blood Fury (числа Classic)', 'Wowhead Classic: Blood Fury (Classic numbers)', 'Wowhead Classic: Blood Fury (числа Classic)'), 'https://www.wowhead.com/classic/spell=20572/blood-fury'),
        (t('Wowhead Classic: Hardiness (числа Classic)', 'Wowhead Classic: Hardiness (Classic numbers)', 'Wowhead Classic: Hardiness (числа Classic)'), 'https://www.wowhead.com/classic/spell=20573/hardiness'),
        (t('LFCarry: изменения классов', 'LFCarry: class changes', 'LFCarry: зміни класів'), 'https://lfcarry.com/guides/wow-forever-class-changes'),
    ],
    'sections': [
        {'id': 'table', 'title': t('Сводная таблица', 'Summary table', 'Зведена таблиця'), 'blocks': [
            ('text', [t('Данные по бете (уровень 30, сборки до 15.10). Полей боя на бете не было, поэтому PvP оценено по дуэлям и мировому PvP. «Или» — источники спорят, одного победителя нет.', 'Beta data (level 30, builds up to Oct 15). There were no battlegrounds in the beta, so PvP is judged by duels and world PvP. “Or” means the sources disagree and there is no single winner.', 'Дані за бетою (30 рівень, збірки до 15 жовтня). Полів бою в бета-версії не було, тож PvP оцінено за дуелями та світовим PvP. «Або» означає, що джерела сперечаються і єдиного переможця немає.')]),
            ('table', {'head': [t('Класс', 'Class', 'Клас'), t('Альянс, PvE', 'Alliance, PvE', 'Альянс, PvE'), t('Орда, PvE', 'Horde, PvE', 'Орда, PvE'), t('Альянс, PvP', 'Alliance, PvP', 'Альянс, PvP'), t('Орда, PvP', 'Horde, PvP', 'Орда, PvP')], 'rows': [
                [t('Воин', 'Warrior', 'Воїн'), t('Человек или Ночной эльф; танк — Дворф', 'Human or Night Elf; tank: Dwarf', 'Людина або Нічний ельф; танк — Дворф'), t('Орк; танк — Таурен', 'Orc; tank: Tauren', 'Орк; танк — Таурен'), t('Человек', 'Human', 'Людина'), t('Орк', 'Orc', 'Орк')],
                [t('Паладин', 'Paladin', 'Паладин'), t('Человек; танк — Дворф', 'Human; tank: Dwarf', 'Людина; танк — Дворф'), t('Нежить (единственная)', 'Undead (the only option)', 'Нежить (єдина)'), t('Человек или Дворф', 'Human or Dwarf', 'Людина або Дворф'), t('Нежить', 'Undead', 'Нежить')],
                [t('Охотник', 'Hunter', 'Мисливець'), t('Человек или Ночной эльф', 'Human or Night Elf', 'Людина або Нічний ельф'), t('Орк или Тролль', 'Orc or Troll', 'Орк або Троль'), t('Человек', 'Human', 'Людина'), t('Орк', 'Orc', 'Орк')],
                [t('Разбойник', 'Rogue', 'Розбійник'), t('Ночной эльф', 'Night Elf', 'Нічний ельф'), t('Орк', 'Orc', 'Орк'), t('Человек или Гном', 'Human or Gnome', 'Людина або Гном'), t('Нежить или Орк', 'Undead or Orc', 'Нежить або Орк')],
                [t('Жрец', 'Priest', 'Жрець'), t('Гном', 'Gnome', 'Гном'), t('Нежить или Тролль', 'Undead or Troll', 'Нежить або Троль'), t('Гном или Человек', 'Gnome or Human', 'Гном або Людина'), t('Нежить', 'Undead', 'Нежить')],
                [t('Шаман', 'Shaman', 'Шаман'), t('Дворф (единственный)', 'Dwarf (the only option)', 'Дворф (єдиний)'), t('Орк; лекарь — Тролль', 'Orc; healer: Troll', 'Орк; цілитель — Троль'), t('Дворф (единственный)', 'Dwarf (the only option)', 'Дворф (єдиний)'), t('Орк, Таурен или Тролль', 'Orc, Tauren or Troll', 'Орк, Таурен або Троль')],
                [t('Маг', 'Mage', 'Маг'), t('Гном', 'Gnome', 'Гном'), t('Орк', 'Orc', 'Орк'), t('Гном', 'Gnome', 'Гном'), t('Нежить', 'Undead', 'Нежить')],
                [t('Чернокнижник', 'Warlock', 'Чорнокнижник'), t('Гном или Человек', 'Gnome or Human', 'Гном або Людина'), t('Орк или Нежить', 'Orc or Undead', 'Орк або Нежить'), t('Человек', 'Human', 'Людина'), t('Нежить', 'Undead', 'Нежить')],
                [t('Друид', 'Druid', 'Друїд'), t('Ночной эльф', 'Night Elf', 'Нічний ельф'), t('Таурен', 'Tauren', 'Таурен'), t('Ночной эльф', 'Night Elf', 'Нічний ельф'), t('Таурен', 'Tauren', 'Таурен')],
            ]}),
            ('tip', t('Не можете выбрать — берите расу, которая нравится: несколько процентов урона не заменят персонажа, которым приятно играть до 60.', 'Can’t decide? Take the race you like: a few percent of damage won’t replace a character you enjoy playing all the way to 60.', 'Не можете обрати — беріть расу, яка подобається: кілька відсотків шкоди не замінять персонажа, за якого приємно грати до 60 рівня.')),
        ]},
        {'id': 'classes', 'title': t('По классам', 'By class', 'За класами'), 'blocks': [
            ('steps', [
                {'id': 'warrior', 't': t('Воин', 'Warrior', 'Воїн'),
                 'd': t('Человек: Беспощадность даёт +2% крита любым оружием, Воля к жизни снимает оглушения. Ночной эльф: Свет Элуны, +10% крита на 15 сек. Источники делятся почти поровну. Танку — Дворф: Каменная форма снижает физический урон на 10% и снимает кровотечения. За Орду Орка ставят первым все источники: Кровавое неистовство (+10% силы атаки на 15 сек), Дикость (+1% крита), Твердость (оглушения короче на 20%). Танку — Таурен: Закалка (+5% здоровья) и Громовая поступь.', 'Human: Ruthless gives +2% crit with any weapon, Will to Survive removes stuns. Night Elf: Elune’s Light, +10% crit for 15 sec. The sources are almost evenly split. For a tank, take Dwarf: Stoneform cuts physical damage by 10% and removes bleeds. On the Horde side every source puts Orc first: Blood Fury (+10% attack power for 15 sec), Savage (+1% crit), Hardiness (stuns 20% shorter). For a tank, take Tauren: Endurance (+5% health) and War Stomp.', 'Людина: Ruthless дає +2% криту будь-якою зброєю, Will to Survive знімає приголомшення. Нічний ельф: Elune’s Light, +10% криту на 15 с. Джерела розділилися майже порівну. Танку — Дворф: Stoneform зменшує фізичну шкоду на 10% і знімає кровотечі. За Орду всі джерела ставлять першим Орка: Blood Fury (+10% сили атаки на 15 с), Savage (+1% криту), Hardiness (приголомшення коротші на 20%). Танку — Таурен: Endurance (+5% здоров’я) і War Stomp.')},
                {'id': 'paladin', 't': t('Паладин', 'Paladin', 'Паладин'),
                 'd': t('Человек: Беспощадность усиливает и удары, и заклинания, Воля к жизни снимает оглушения. Для Защиты — Дворф: Каменная форма и Ярость земли (+2% к силе крита). В PvP один источник из четырёх выбирает Дворфа. За Орду паладином может быть только Нежить, это новое сочетание Forever. Каннибализм возвращает ману, Воля Отрекшихся снимает страх.', 'Human: Ruthless boosts both strikes and spells, Will to Survive removes stuns. For Protection, take Dwarf: Stoneform and Earth Fury (+2% crit damage). In PvP one source out of four picks Dwarf. On the Horde side only Undead can be a paladin; this is a new Forever combination. Cannibalize restores mana, Will of the Forsaken removes fear.', 'Людина: Ruthless підсилює і удари, і закляття, Will to Survive знімає приголомшення. Для Захисту — Дворф: Stoneform і Earth Fury (+2% до шкоди криту). У PvP одне джерело з чотирьох обирає Дворфа. За Орду паладином може бути лише Нежить, це нова комбінація Forever. Cannibalize повертає ману, Will of the Forsaken знімає страх.')},
                {'id': 'hunter', 't': t('Охотник', 'Hunter', 'Мисливець'),
                 'd': t('Охотник-человек — новое сочетание Forever: Беспощадность даёт +2% крита, и питомец наследует крит. Ночной эльф отвечает Светом Элуны и Слиться с тенью. Один свежий источник (24.10) ставит первым Дворфа за Охотника на крупную дичь: +5% урона по зверям. За Орду — Орк (Кровавое неистовство, Дикость) или Тролль (Убийство животных, +5% по зверям). В PvP Таурену помогает Громовая поступь.', 'The human hunter is a new Forever combination: Ruthless gives +2% crit, and the pet inherits the crit. Night Elf answers with Elune’s Light and Shadowmeld. One recent source (Oct 24) puts Dwarf first for its Big Game Hunter: +5% damage against beasts. On the Horde side it is Orc (Blood Fury, Savage) or Troll (Beast Slaying, +5% against beasts). In PvP, War Stomp helps Tauren.', 'Мисливець-людина — нова комбінація Forever: Ruthless дає +2% криту, а улюбленець успадковує кріт. Нічний ельф відповідає Elune’s Light і Shadowmeld. Одне свіже джерело (24 жовтня) ставить першим Дворфа за Big Game Hunter: +5% шкоди по звірах. За Орду — Орк (Blood Fury, Savage) або Троль (Beast Slaying, +5% по звірах). У PvP Тауренові допомагає War Stomp.')},
                {'id': 'rogue', 't': t('Разбойник', 'Rogue', 'Розбійник'),
                 'd': t('Ночной эльф: Слиться с тенью теперь снижает угрозу и в бою, плюс Свет Элуны и Расторопность. Человек: крит любым оружием, Внимательность вскрывает чужих разбойников. В PvP Альянса единого ответа нет: Гном снимает корни и замедления Мастером побега. За Орду — Орк в PvE. В PvP чаще Нежить: Воля Отрекшихся снимает страх жрецов и чернокнижников.', 'Night Elf: Shadowmeld now lowers threat in combat too, plus Elune’s Light and Quickness. Human: crit with any weapon, and Perception reveals enemy rogues. In Alliance PvP there is no single answer: Gnome breaks roots and slows with Escape Artist. On the Horde side it is Orc in PvE. In PvP it is more often Undead: Will of the Forsaken removes fear from priests and warlocks.', 'Нічний ельф: Shadowmeld тепер знижує загрозу і в бою, плюс Elune’s Light і Quickness. Людина: кріт будь-якою зброєю, а Perception виявляє чужих розбійників. У PvP Альянсу єдиної відповіді немає: Гном знімає корені та уповільнення через Escape Artist. За Орду — Орк у PvE. У PvP частіше Нежить: Will of the Forsaken знімає страх жерців і чорнокнижників.')},
                {'id': 'priest', 't': t('Жрец', 'Priest', 'Жрець'),
                 'd': t('Жрец-гном — новое сочетание Forever и выбор всех источников в PvE: Эврика! усиливает и Слово силы: Щит, Пытливый ум даёт +5% маны, у гнома два своих заклинания: Confounding Flash и Contingency Plan. Для Темной магии один источник берёт Ночного эльфа. За Орду — Нежить или Тролль. Нежить сильнее в PvP: Воля Отрекшихся снимает страх, сон и очарование.', 'The gnome priest is a new Forever combination and the pick of every source in PvE: Eureka! also boosts Power Word: Shield, Expansive Mind gives +5% mana, and the gnome has two spells of its own (Confounding Flash, Contingency Plan). For Shadow, one source takes Night Elf. On the Horde side it is Undead or Troll. Undead is stronger in PvP: Will of the Forsaken removes fear, sleep and charm.', 'Жрець-гном — нова комбінація Forever і вибір усіх джерел у PvE: Eureka! підсилює й Power Word: Shield, Expansive Mind дає +5% мани, а в гнома є два власні закляття (Confounding Flash, Contingency Plan). Для Темряви одне джерело бере Нічного ельфа. За Орду — Нежить або Троль. Нежить сильніша в PvP: Will of the Forsaken знімає страх, сон і підкорення.')},
                {'id': 'shaman', 't': t('Шаман', 'Shaman', 'Шаман'),
                 'd': t('За Альянс шаманом может быть только Дворф, это новое сочетание Forever: Каменная форма и Ярость земли (+2% к силе крита). За Орду — Орк: Кровавое неистовство даёт и силу атаки, и силу заклинаний, поэтому подходит и Стихиям, и Совершенствованию. Лекарю один источник советует Тролля за Боевое исступление. В PvP три источника дают три разных ответа: Орк, Таурен, Тролль.', 'On the Alliance side only Dwarf can be a shaman; this is a new Forever combination: Stoneform and Earth Fury (+2% crit damage). On the Horde side it is Orc: Blood Fury gives both attack power and spell power, so it suits Elemental and Enhancement alike. For a healer one source recommends Troll for Berserking. In PvP three sources give three different answers: Orc, Tauren, Troll.', 'За Альянс шаманом може бути лише Дворф, це нова комбінація Forever: Stoneform і Earth Fury (+2% до шкоди криту). За Орду — Орк: Blood Fury дає і силу атаки, і силу заклять, тож підходить і Стихіям, і Вдосконаленню. Цілителю одне джерело радить Троля за Berserking. У PvP три джерела дають три різні відповіді: Орк, Таурен, Троль.')},
                {'id': 'mage', 't': t('Маг', 'Mage', 'Маг'),
                 'd': t('Гном: Эврика! на 8 сек, Пытливый ум (+5% маны), Мастер побега от корней. Один источник ставит первым Высшего скайборна за +3% к скорости заклинаний, остальные — нет. Маг-орк — новое сочетание Forever: Кровавое неистовство теперь даёт силу заклинаний. В PvP — Нежить: Воля Отрекшихся снимает страх, сон и очарование.', 'Gnome: Eureka! for 8 sec, Expansive Mind (+5% mana), Escape Artist against roots. One source puts High Order Skyborne first for +3% spell speed; the others don’t. The orc mage is a new Forever combination: Blood Fury now gives spell power. In PvP it is Undead: Will of the Forsaken removes fear, sleep and charm.', 'Гном: Eureka! на 8 с, Expansive Mind (+5% мани), Escape Artist від коренів. Одне джерело ставить першим Високого скайборна за +3% до швидкості заклять, решта — ні. Маг-орк — нова комбінація Forever: Blood Fury тепер дає силу заклять. У PvP — Нежить: Will of the Forsaken знімає страх, сон і підкорення.')},
                {'id': 'warlock', 't': t('Чернокнижник', 'Warlock', 'Чорнокнижник'),
                 'd': t('Гном (Эврика!, Пытливый ум) или Человек: периодический урон в Forever критует, а Беспощадность даёт +2% крита. В PvP чаще берут Человека: Воля к жизни снимает оглушения. За Орду — Орк в PvE (Кровавое неистовство даёт силу заклинаний) и Нежить в PvP. Тролль-чернокнижник — новое сочетание, но в лидеры не попадает.', 'Gnome (Eureka!, Expansive Mind) or Human: damage over time can crit in Forever, and Ruthless gives +2% crit. In PvP Human is the more common pick: Will to Survive removes stuns. On the Horde side it is Orc in PvE (Blood Fury gives spell power) and Undead in PvP. The troll warlock is a new combination but does not make the lead.', 'Гном (Eureka!, Expansive Mind) або Людина: періодична шкода у Forever може бути критичною, а Ruthless дає +2% криту. У PvP частіше беруть Людину: Will to Survive знімає приголомшення. За Орду — Орк у PvE (Blood Fury дає силу заклять) і Нежить у PvP. Чорнокнижник-троль — нова комбінація, але до лідерів не потрапляє.')},
                {'id': 'druid', 't': t('Друид', 'Druid', 'Друїд'),
                 'd': t('Ночной эльф: Свет Элуны (+10% крита) и Расторопность. Таурен: Закалка (+5% здоровья и +2% к силе крита), Громовая поступь работает и в формах. Скайборн-друид — новое сочетание Forever: Благословение ветра даёт +3% к скорости заклинаний и ударов в облике кошки. Часть источников ставит его первым для Силы зверя и Баланса, другие — в середину. Для скайборна нужен платный набор Heroic Pack.', 'Night Elf: Elune’s Light (+10% crit) and Quickness. Tauren: Endurance (+5% health and +2% crit damage), and War Stomp works in forms too. The Skyborne druid is a new Forever combination: Wind Blessed gives +3% spell and melee speed in cat form. Some sources put it first for Feral and Balance, others in the middle. Skyborne needs the paid Heroic Pack.', 'Нічний ельф: Elune’s Light (+10% криту) і Quickness. Таурен: Endurance (+5% здоров’я і +2% до шкоди криту), War Stomp працює й у формах. Скайборн-друїд — нова комбінація Forever: Wind Blessed дає +3% до швидкості заклять і ударів у подобі кота. Частина джерел ставить його першим для Сили звіра й Балансу, інші — в середину. Для скайборна потрібен платний набір Heroic Pack.')},
            ]),
        ]},
        {'id': 'forever', 'title': t('Что изменилось против Classic', 'What changed from Classic', 'Що змінилося порівняно з Classic'), 'blocks': [
            ('text', [t('Старые гайды Classic по расам устарели: у рас убраны оружейные специализации и сопротивления, часть способностей заменена.', 'Old Classic race guides are out of date: weapon specializations and resistances are gone from the races, and some abilities were replaced.', 'Старі гайди Classic з рас застаріли: у рас прибрали спеціалізації зброї та опір магії, частину здібностей замінили.')]),
            ('table', {'head': [t('Раса', 'Race', 'Раса'), t('В Classic', 'In Classic', 'У Classic'), t('В Forever', 'In Forever', 'У Forever')], 'rows': [
                [t('Все', 'All', 'Усі'), t('Специализации оружия, сопротивления', 'Weapon specializations, resistances', 'Спеціалізації зброї, опір магії'), t('Убраны, вместо них новые способности', 'Removed, replaced by new abilities', 'Прибрано, замість них нові здібності')],
                [t('Человек', 'Human', 'Людина'), t('Специализация на мечах и булавах', 'Sword and mace specialization', 'Спеціалізація на мечах і булавах'), t('Беспощадность: +2% крита всем умениям', 'Ruthless: +2% crit on all abilities', 'Ruthless: +2% криту всім умінням')],
                [t('Орк', 'Orc', 'Орк'), t('Кровавое неистовство: +25% базовой силы атаки, получаемое лечение −50% на 25 сек', 'Blood Fury: +25% base attack power, healing received −50% for 25 sec', 'Blood Fury: +25% базової сили атаки, отримане лікування −50% на 25 с'), t('Даёт и силу заклинаний, штрафа к лечению нет, откат 3 мин', 'Gives spell power too, no healing penalty, 3 min cooldown', 'Дає й силу заклять, штрафу до лікування немає, відкат 3 хв')],
                [t('Орк', 'Orc', 'Орк'), t('Command: +5% урона питомцев', 'Command: +5% pet damage', 'Command: +5% шкоди улюбленців'), t('Дикость: +1% крита. Питомцы больше не повод брать Орка', 'Savage: +1% crit. Pets are no longer a reason to pick Orc', 'Savage: +1% криту. Улюбленці більше не привід брати Орка')],
                [t('Орк', 'Orc', 'Орк'), t('Твердость: +25% к шансу сопротивиться оглушению', 'Hardiness: +25% chance to resist stuns', 'Hardiness: +25% до шансу опиратися приголомшенню'), t('Оглушения короче на 20%', 'Stuns 20% shorter', 'Приголомшення коротші на 20%')],
                [t('Тролль', 'Troll', 'Троль'), t('Боевое исступление до +30% при низком здоровье', 'Berserking: up to +30% when at low health', 'Berserking: до +30% за низького здоров’я'), t('Ровно +10% скорости атак и заклинаний на 10 сек', 'A flat +10% attack and spell speed for 10 sec', 'Рівно +10% до швидкості атак і заклять на 10 с')],
                [t('Дворф', 'Dwarf', 'Дворф'), t('Каменная форма: +10% брони', 'Stoneform: +10% armor', 'Stoneform: +10% броні'), t('−10% физического урона', '−10% physical damage', '−10% фізичної шкоди')],
                [t('Гном', 'Gnome', 'Гном'), '—', t('Эврика!: 8 сек, способности дешевле и на 10% сильнее', 'Eureka!: 8 sec, abilities cost less and are 10% stronger', 'Eureka!: 8 с, здібності дешевші й на 10% сильніші')],
                [t('Таурен', 'Tauren', 'Таурен'), t('Громовая поступь раз в 2 мин', 'War Stomp once every 2 min', 'War Stomp раз на 2 хв'), t('Раз в 90 сек, плюс Закалка и Бег по равнинам', 'Once every 90 sec, plus Endurance and Plainsrunning', 'Раз на 90 с, плюс Endurance і Plainsrunning')],
                [t('Нежить', 'Undead', 'Нежить'), '—', t('Могильное касание: шанс вытянуть здоровье', 'Touch of the Grave: chance to drain health', 'Touch of the Grave: шанс витягнути здоров’я')],
            ]}),
            ('text', [t('Новые сочетания: охотник-человек, шаман-дворф, жрец-гном, паладин-нежить, маг-орк, чернокнижник-тролль, друид-скайборн.', 'New combinations: human hunter, dwarf shaman, gnome priest, undead paladin, orc mage, troll warlock, Skyborne druid.', 'Нові комбінації: мисливець-людина, шаман-дворф, жрець-гном, паладин-нежить, маг-орк, чорнокнижник-троль, друїд-скайборн.')]),
        ]},
        {'id': 'disputed', 'title': t('Где источники спорят', 'Where the sources disagree', 'Де джерела сперечаються'), 'blocks': [
            ('steps', [
                {'t': t('Воин и Охотник за Альянс', 'Alliance Warrior and Hunter', 'Воїн і Мисливець за Альянс'),
                 'd': t('Человек или Ночной эльф, голоса делятся почти поровну. Охотнику один источник советует Дворфа.', 'Human or Night Elf, the votes are almost evenly split. For Hunter one source recommends Dwarf.', 'Людина або Нічний ельф, голоси розділилися майже порівну. Мисливцеві одне джерело радить Дворфа.')},
                {'t': t('Чернокнижник за Альянс', 'Alliance Warlock', 'Чорнокнижник за Альянс'),
                 'd': t('Гном или Человек.', 'Gnome or Human.', 'Гном або Людина.')},
                {'t': t('Шаман Орды в PvP', 'Horde Shaman in PvP', 'Шаман Орди в PvP'),
                 'd': t('три источника, три ответа.', 'three sources, three answers.', 'три джерела, три відповіді.')},
                {'t': t('Скайборн-друид и скайборн-маг', 'Skyborne druid and Skyborne mage', 'Скайборн-друїд і скайборн-маг'),
                 'd': t('от «лучшей расы» до «худшей в PvP» в разных списках.', 'from “best race” to “worst in PvP” depending on the list.', 'від «найкращої раси» до «найгіршої в PvP» залежно від списку.')},
                {'t': t('PvP целиком', 'PvP as a whole', 'PvP загалом'),
                 'd': t('полей боя на бете не было, уровни 31–60 никто не проверял. Обновим после старта 4 ноября.', 'there were no battlegrounds in the beta and nobody has tested levels 31–60. We’ll update after the Nov 4 launch.', 'полів бою в бета-версії не було, рівні 31–60 ніхто не перевіряв. Оновимо після старту 4 листопада.')},
            ]),
        ]},
        {'id': 'faq', 'title': t('Частые вопросы', 'Common questions', 'Часті питання'), 'blocks': [
            ('faq', [
                {'id': 'q1', 'q': t('Какая раса лучше для воина в WoW Forever?', 'Which race is best for a warrior in WoW Forever?', 'Яка раса найкраща для воїна у WoW Forever?'),
                 'a': [t('За Альянс — Человек или Ночной эльф, источники делятся почти поровну, танку — Дворф. За Орду — Орк, танку — Таурен.', 'On the Alliance side, Human or Night Elf; the sources are almost evenly split, and a tank should take Dwarf. On the Horde side, Orc; a tank should take Tauren.', 'За Альянс — Людина або Нічний ельф, джерела розділилися майже порівну, танку — Дворф. За Орду — Орк, танку — Таурен.')]},
                {'id': 'q2', 'q': t('Сильно ли раса влияет на игру?', 'Does race make a big difference?', 'Чи сильно раса впливає на гру?'),
                 'a': [t('Несколько процентов урона или живучести. Класс, спек и экипировка важнее, поэтому берите расу, которая нравится.', 'A few percent of damage or survivability. Class, spec and gear matter more, so take the race you like.', 'Це кілька відсотків шкоди або живучості. Клас, спеціалізація й екіпірування важать більше, тож беріть расу, яка подобається.')]},
                {'id': 'q3', 'q': t('Какие сочетания расы и класса новые в Forever?', 'Which race and class combinations are new in Forever?', 'Які поєднання раси й класу нові у Forever?'),
                 'a': [t('Охотник-человек, шаман-дворф, жрец-гном, паладин-нежить, маг-орк, чернокнижник-тролль и друид-скайборн.', 'Human hunter, dwarf shaman, gnome priest, undead paladin, orc mage, troll warlock and Skyborne druid.', 'Мисливець-людина, шаман-дворф, жрець-гном, паладин-нежить, маг-орк, чорнокнижник-троль і друїд-скайборн.')]},
                {'id': 'q4', 'q': t('Подходят ли гайды Classic по расам для Forever?', 'Do Classic race guides still apply to Forever?', 'Чи годяться гайди Classic з рас для Forever?'),
                 'a': [t('Нет. У рас убраны оружейные специализации и сопротивления, Кровавое неистовство, Боевое исступление и Каменная форма работают иначе.', 'No. Weapon specializations and resistances are gone from the races, and Blood Fury, Berserking and Stoneform work differently.', 'Ні. У рас прибрали спеціалізації зброї та опір магії, а Blood Fury, Berserking і Stoneform працюють інакше.')]},
                {'id': 'q5', 'q': t('Какую расу взять паладину за Орду?', 'Which race should a Horde paladin take?', 'Яку расу взяти паладину за Орду?'),
                 'a': [t('Только Нежить: другие расы Орды паладином быть не могут.', 'Only Undead: no other Horde race can be a paladin.', 'Лише Нежить: інші раси Орди паладинами бути не можуть.')]},
            ]),
        ]},
        {'id': 'related', 'title': t('Смотрите также', 'See also', 'Дивіться також'), 'blocks': [
            ('tiles', [{'t': t('Классы', 'Classes', 'Класи'), 'd': t('Какой класс выбрать и сравнение', 'Which class to pick, compared', 'Який клас обрати й порівняння'), 'href': 'classes/', 'art': 'hero_classes'}, {'t': t('Расы', 'Races', 'Раси'), 'd': t('Сравнение всех рас', 'All races compared', 'Порівняння всіх рас'), 'href': 'races/', 'art': 'hero_races'}]),
        ]},
    ],
})

# ---------- tier-list ----------

GUIDES.append({
    'slug': 'tier-list', 'art': 'hero_classes', 'hero': 'hero_classes',
    'title': t('Тир-лист классов WoW Forever', 'WoW Forever Class Tier List', 'Тір-лист класів WoW Forever'),
    'lead': t('На бете сильнее всех Паладин в PvE, Охотник и Маг на прокачке, Чернокнижник и Разбойник в PvP. Это срез беты 30 уровня, обновим после старта 4 ноября.', 'In the beta the strongest picks are Paladin in PvE, Hunter and Mage for leveling, Warlock and Rogue in PvP. This is a level 30 beta snapshot; we’ll update it after the Nov 4 launch.', 'У бета-версії найсильніші Паладин у PvE, Мисливець і Маг на прокачуванні, Чорнокнижник і Розбійник у PvP. Це зріз бети на 30 рівні, оновимо його після старту 4 листопада.'),
    'tile': t('Сильные классы и спеки по данным беты', 'Strong classes and specs by beta data', 'Сильні класи й спеціалізації за даними бети'),
    'pills': [t('По бете', 'Beta data', 'За бетою'), t('27 спеков', '27 specs', '27 спеціалізацій'), t('Обновим после 04.11', 'Updated after Nov 4', 'Оновимо після 4 листопада')],
    'sources': [
        (t('RankedBoost: тир-лист Forever', 'RankedBoost: Forever tier list', 'RankedBoost: тір-лист Forever'), 'https://rankedboost.com/world-of-warcraft/forever/tier-list/'),
        (t('Noobtoboss: тир-лист', 'Noobtoboss: tier list', 'Noobtoboss: тір-лист'), 'https://noobtoboss.com/wowforever-tierlist/'),
        (t('Noobtoboss: прокачка', 'Noobtoboss: leveling', 'Noobtoboss: прокачування'), 'https://noobtoboss.com/wowforever-leveling-tierlist/'),
        (t('gamer-guides: тир-лист беты', 'gamer-guides: beta tier list', 'gamer-guides: тір-лист бети'), 'https://gamer-guides.com/warcraft-forever/tier-list-beta/'),
        (t('Kami-labs: все 9 классов', 'Kami-labs: all 9 classes', 'Kami-labs: усі 9 класів'), 'https://kami-labs.fr/en/wow-forever/quelle-classe-choisir-wow-forever/'),
        (t('Warcraft Tavern: итоги Forever Open', 'Warcraft Tavern: Forever Open results', 'Warcraft Tavern: підсумки Forever Open'), 'https://www.warcrafttavern.com/forever/news/warlockguy-wins-the-wow-forever-open-1v1-dueling-tournament/'),
        (t('LFCarry: изменения классов', 'LFCarry: class changes', 'LFCarry: зміни класів'), 'https://lfcarry.com/guides/wow-forever-class-changes'),
        (t('games.gg: какой класс выбрать', 'games.gg: which class to pick', 'games.gg: який клас обрати'), 'https://games.gg/news/wow-forever-best-class-returning-paladin/'),
        (t('LFCarry: классы и темп прокачки (оценка по Classic, перепроверена на бете)', 'LFCarry: classes and leveling pace (Classic-based estimate, rechecked on the beta)', 'LFCarry: класи й темп прокачування (оцінка за Classic, перевірена на бета-версії)'), 'https://lfcarry.com/guides/wow-forever-classes'),
    ],
    'sections': [
        {'id': 'how', 'title': t('Как читать', 'How to read it', 'Як читати'), 'blocks': [
            ('text', [t('Тир — сводка нескольких источников, а не оценка одного сайта. S — лучшие в своей роли, C — слабее, но играть можно. Звёздочка (*) — источники расходятся на две буквы и больше.', 'The tier is a summary of several sources, not one site’s rating. S is the best in its role, C is weaker but playable. An asterisk (*) means the sources differ by two letters or more.', 'Тір — це зведення кількох джерел, а не оцінка одного сайту. S — найкращі у своїй ролі, C — слабші, але грати можна. Зірочка (*) означає, що джерела розходяться на дві літери й більше.')]),
            ('tip', t('По бете. Бета шла с 17.09 по 21.10 на уровне 30: рейдов, полей боя и уровней 31–60 там не было. Обновим после старта 4 ноября.', 'Beta data. The beta ran from Sep 17 to Oct 21 at level 30: no raids, battlegrounds or levels 31–60. We’ll update after the Nov 4 launch.', 'За бетою. Бета тривала з 17 вересня по 21 жовтня на 30 рівні: рейдів, полів бою та рівнів 31–60 там не було. Оновимо після старту 4 листопада.')),
        ]},
        {'id': 'classes', 'title': t('Классы целиком', 'Whole classes', 'Класи загалом'), 'blocks': [
            ('table', {'head': [t('Класс', 'Class', 'Клас'), t('Прокачка', 'Leveling', 'Прокачування'), 'PvE', 'PvP', t('Почему', 'Why', 'Чому')], 'rows': [
                [t('Паладин', 'Paladin', 'Паладин'), 'A', 'S', 'B', t('Защита — лучший танк беты, даже после ослабления 15.10.', 'Protection is the best tank of the beta, even after the Oct 15 nerf.', 'Захист — найкращий танк бети, навіть після послаблення 15 жовтня.')],
                [t('Охотник', 'Hunter', 'Мисливець'), 'S', 'A*', 'A', t('Самая быстрая прокачка и самый простой урон.', 'The fastest leveling and the simplest damage.', 'Найшвидше прокачування й найпростіша шкода.')],
                [t('Маг', 'Mage', 'Маг'), 'S', 'A', 'A*', t('Быстрая прокачка за Лёд, сильный бурст Тайной магии.', 'Fast leveling as Frost, strong Arcane burst.', 'Швидке прокачування за Лід, потужний бурст Тайної магії.')],
                [t('Чернокнижник', 'Warlock', 'Чорнокнижник'), 'A', 'A', 'S', t('Периодический урон критует; чернокнижники заняли два первых места на турнире Forever Open.', 'Damage over time can crit; warlocks took the top two places at the Forever Open tournament.', 'Періодична шкода може бути критичною; чорнокнижники зайняли два перші місця на турнірі Forever Open.')],
                [t('Разбойник', 'Rogue', 'Розбійник'), 'B', 'A', 'S', t('Скрытность и контроль: в PvP самый надёжный выбор.', 'Stealth and control: the most reliable pick in PvP.', 'Непомітність і контроль: у PvP найнадійніший вибір.')],
                [t('Жрец', 'Priest', 'Жрець'), 'C*', 'A', 'A*', t('Нужен любой группе; Послушание сильно и в PvP, Свет — нет.', 'Every group needs one; Discipline is strong in PvP too, Holy is not.', 'Потрібен будь-якій групі; Послух сильний і в PvP, Світло — ні.')],
                [t('Шаман', 'Shaman', 'Шаман'), 'B', 'A', 'B*', t('Исцеление и Совершенствование сильные, Стихии усилены 15.10 после слабого старта.', 'Restoration and Enhancement are strong, Elemental was buffed on Oct 15 after a weak start.', 'Зцілення та Вдосконалення сильні, Стихії підсилили 15 жовтня після слабкого старту.')],
                [t('Воин', 'Warrior', 'Воїн'), 'C', 'A', 'B', t('Самая медленная прокачка, зато Защита — сильный танк.', 'The slowest leveling, but Protection is a strong tank.', 'Найповільніше прокачування, зате Захист — сильний танк.')],
                [t('Друид', 'Druid', 'Друїд'), 'A*', 'B', 'B*', t('Нет ведущего спека, многие ключевые умения открываются после 30 уровня.', 'No leading spec; many key abilities unlock after level 30.', 'Провідної спеціалізації немає, багато ключових умінь відкривається після 30 рівня.')],
            ]}),
        ]},
        {'id': 'leveling', 'title': t('Прокачка', 'Leveling\xa0', 'Прокачування'), 'blocks': [
            ('text', [t('Источники оценивают прокачку по классу, поэтому здесь один спек на класс. Проценты темпа — оценка LFCarry по Classic, перепроверенная на бете.', 'Sources rate leveling per class, so this table has one spec per class. The pace percentages are LFCarry’s estimate based on Classic, rechecked on the beta.', 'Джерела оцінюють прокачування за класом, тому тут одна спеціалізація на клас. Відсотки темпу — оцінка LFCarry за Classic, перевірена на бета-версії.')]),
            ('table', {'head': [t('Тир', 'Tier', 'Тір'), t('Класс · спек', 'Class · spec', 'Клас · спеціалізація'), t('Почему', 'Why', 'Чому'), t('Где расходятся', 'Where sources differ', 'Де розходяться')], 'rows': [
                ['S', (t('Охотник · Повелитель зверей', 'Hunter · Beast Mastery', 'Мисливець · Володіння звірами'), 'guides/leveling-hunter/'), t('Питомец танкует, примерно на 8% быстрее среднего.', 'The pet tanks; about 8% faster than average.', 'Улюбленець танкує, приблизно на 8% швидше за середнє.'), 'gamer-guides: A'],
                ['S', (t('Маг · Лёд', 'Mage · Frost', 'Маг · Лід'), 'guides/leveling-mage/'), t('Урон по площади, замедления, своя еда и вода, примерно на 8% быстрее среднего.', 'Area damage, slows, its own food and water; about 8% faster than average.', 'Шкода по площі, уповільнення, власні їжа й вода, приблизно на 8% швидше за середнє.'), t('gamer-guides берёт Тайную магию', 'gamer-guides picks Arcane', 'gamer-guides бере Тайну магію')],
                ['A', (t('Чернокнижник · Колдовство', 'Warlock · Affliction', 'Чорнокнижник · Прокляття'), 'guides/leveling-warlock/'), t('Питомец держит врага, пока работает периодический урон.', 'The pet holds the enemy while damage over time works.', 'Улюбленець тримає ворога, поки діє періодична шкода.'), 'gamer-guides: S'],
                ['A', (t('Паладин · Воздаяние', 'Paladin · Retribution', 'Паладин · Відплата'), 'guides/leveling-paladin/'), t('Легко фармит группы врагов по площади.', 'Farms groups of enemies easily with area damage.', 'Легко фармить групи ворогів шкодою по площі.'), 'gamer-guides: B'],
                ['A*', (t('Друид · Сила зверя', 'Druid · Feral', 'Друїд · Сила звіра'), 'guides/leveling-druid/'), t('Много ключевых умений открывается после 30, примерно на 5% медленнее среднего.', 'Many key abilities unlock after 30; about 5% slower than average.', 'Багато ключових умінь відкривається після 30, приблизно на 5% повільніше за середнє.'), 'gamer-guides: C'],
                ['B', (t('Шаман · Совершенствование', 'Shaman · Enhancement', 'Шаман · Вдосконалення'), 'guides/leveling-shaman/'), t('До 30 уровня не хватает маны; Призрачный волк с 20 уровня.', 'Short on mana until level 30; Ghost Wolf from level 20.', 'До 30 рівня не вистачає мани; Ghost Wolf з 20 рівня.'), '—'],
                ['B', (t('Разбойник · Ликвидация или Бой', 'Rogue · Assassination or Combat', 'Розбійник · Ліквідація або Бій'), 'guides/leveling-rogue/'), t('Средний темп.', 'Average pace.', 'Середній темп.'), 'gamer-guides: A'],
                ['C*', (t('Жрец · Темная магия', 'Priest · Shadow', 'Жрець · Темрява'), 'guides/leveling-priest/'), t('Примерно на 5% медленнее среднего.', 'About 5% slower than average.', 'Приблизно на 5% повільніше за середнє.'), t('gamer-guides: S для Послушания', 'gamer-guides: S for Discipline', 'gamer-guides: S для Послуху')],
                ['C', (t('Воин · Оружие или Неистовство', 'Warrior · Arms or Fury', 'Воїн · Зброя або Лють'), 'guides/leveling-warrior/'), t('Самый медленный, примерно на 12% дольше среднего.', 'The slowest, about 12% longer than average.', 'Найповільніший, приблизно на 12% довше за середнє.'), '—'],
            ]}),
        ]},
        {'id': 'pve', 'title': t('PvE по ролям', 'PvE by role', 'PvE за ролями'), 'blocks': [
            ('text', [t('Сравнение внутри роли: танк с танками, лекарь с лекарями. Рейдовых логов нет, рейды откроются 09.12.', 'Comparison within a role: tank with tanks, healer with healers. There are no raid logs; raids open on Dec 9.', 'Порівняння всередині ролі: танк з танками, цілитель з цілителями. Рейдових логів немає, рейди відкриються 9 грудня.')]),
            ('tabs', [
                {'id': 'tank', 't': t('Танк', 'Tank', 'Танк'), 'blocks': [
                    ('table', {'head': [t('Тир', 'Tier', 'Тір'), t('Спек', 'Spec', 'Спеціалізація'), t('Почему', 'Why', 'Чому'), t('Где расходятся', 'Where sources differ', 'Де розходяться')], 'rows': [
                ['S', t('Паладин · Защита', 'Paladin · Protection', 'Паладин · Захист'), t('Лучший танк беты, Печать ярости даёт провокацию.', 'The best tank of the beta; Seal of Fury gives a taunt.', 'Найкращий танк бети, Seal of Fury дає провокацію.'), t('Ослаблен 15.10, RankedBoost (17.10) всё равно ставит S', 'Nerfed Oct 15, RankedBoost (Oct 17) still gives S', 'Послаблений 15 жовтня, RankedBoost (17 жовтня) усе одно ставить S')],
                ['A', t('Воин · Защита', 'Warrior · Protection', 'Воїн · Захист'), t('Сильный танк для подземелий.', 'A strong dungeon tank.', 'Сильний танк для підземель.'), '—'],
                ['B', t('Друид · Сила зверя (медведь)', 'Druid · Feral (bear)', 'Друїд · Сила звіра (ведмідь)'), t('Медведь танкует, но уступает Паладину и Воину.', 'The bear tanks, but trails Paladin and Warrior.', 'Ведмідь танкує, але поступається Паладину й Воїну.'), '—'],
            ]}),
                ]},
                {'id': 'healer', 't': t('Лекарь', 'Healer', 'Цілитель'), 'blocks': [
                    ('table', {'head': [t('Тир', 'Tier', 'Тір'), t('Спек', 'Spec', 'Спеціалізація'), t('Почему', 'Why', 'Чому'), t('Где расходятся', 'Where sources differ', 'Де розходяться')], 'rows': [
                ['S', t('Жрец · Послушание', 'Priest · Discipline', 'Жрець · Послух'), t('Покаяние и щиты: лучший лекарь беты по двум источникам.', 'Penance and shields: the best healer of the beta according to two sources.', 'Penance і щити: найкращий цілитель бети за двома джерелами.'), '—'],
                ['S', t('Шаман · Исцеление', 'Shaman · Restoration', 'Шаман · Зцілення'), t('Быстрина, первое место среди лекарей у RankedBoost.', 'Riptide; first among healers at RankedBoost.', 'Riptide; перше місце серед цілителів у RankedBoost.'), '—'],
                ['A', t('Паладин · Свет', 'Paladin · Holy', 'Паладин · Світло'), t('Сильное лечение по одной цели.', 'Strong single-target healing.', 'Сильне лікування однієї цілі.'), '—'],
                ['A', t('Друид · Исцеление', 'Druid · Restoration', 'Друїд · Зцілення'), t('Буйный рост; Kami называет спек исключительным.', 'Wild Growth; Kami calls the spec exceptional.', 'Wild Growth; Kami називає спеціалізацію винятковою.'), 'gamer-guides: S'],
                ['B*', t('Жрец · Свет', 'Priest · Holy', 'Жрець · Світло'), t('Лучшее лечение по площади, раскрывается к 60 уровню.', 'The best area healing, comes into its own by level 60.', 'Найкраще лікування по площі, розкривається до 60 рівня.'), t('RankedBoost: B для лекаря; Noobtoboss и gamer-guides называют сильным рейдовым лекарем', 'RankedBoost: B as a healer; Noobtoboss and gamer-guides call it a strong raid healer', 'RankedBoost: B для цілителя; Noobtoboss і gamer-guides називають його сильним рейдовим цілителем')],
            ]}),
                ]},
                {'id': 'dps', 't': t('Урон', 'Damage', 'Шкода'), 'blocks': [
                    ('table', {'head': [t('Тир', 'Tier', 'Тір'), t('Спек', 'Spec', 'Спеціалізація'), t('Почему', 'Why', 'Чому'), t('Где расходятся', 'Where sources differ', 'Де розходяться')], 'rows': [
                ['A', t('Паладин · Воздаяние', 'Paladin · Retribution', 'Паладин · Відплата'), t('Сильный, хотя ослаблен 15.10.', 'Strong, though nerfed on Oct 15.', 'Сильний, хоч і послаблений 15 жовтня.'), '—'],
                ['A*', t('Охотник · Стрельба', 'Hunter · Marksmanship', 'Мисливець · Стрільба'), t('Лучший урон охотника, но источники спорят.', 'The hunter’s best damage, but the sources disagree.', 'Найкраща шкода мисливця, але джерела сперечаються.'), 'Noobtoboss: S, RankedBoost: A'],
                ['A*', t('Охотник · Повелитель зверей', 'Hunter · Beast Mastery', 'Мисливець · Володіння звірами'), t('Урон делит с питомцем.', 'Shares damage with the pet.', 'Ділить шкоду з улюбленцем.'), 'Noobtoboss: S, RankedBoost: A'],
                ['A', t('Охотник · Выживание', 'Hunter · Survival', 'Мисливець · Виживання'), t('Лидер по симуляциям, но его ждут выравнивать.', 'Leads in simulations, but a rebalance is expected.', 'Лідер за симуляціями, але його чекають вирівнювати.'), '—'],
                ['A', t('Разбойник · Ликвидация', 'Rogue · Assassination', 'Розбійник · Ліквідація'), t('Яды.', 'Poisons.', 'Отрути.'), '—'],
                ['A*', t('Разбойник · Бой', 'Rogue · Combat', 'Розбійник · Бій'), t('Хорош по одной цели.', 'Good against a single target.', 'Хороший по одній цілі.'), 'RankedBoost: B'],
                ['A', t('Воин · Неистовство', 'Warrior · Fury', 'Воїн · Лють'), t('Сильный урон по нескольким целям.', 'Strong damage against several targets.', 'Сильна шкода по кількох цілях.'), '—'],
                ['A*', t('Шаман · Совершенствование', 'Shaman · Enhancement', 'Шаман · Вдосконалення'), t('Один из лучших по урону у Noobtoboss.', 'One of the best for damage at Noobtoboss.', 'Один із найкращих за шкодою у Noobtoboss.'), 'RankedBoost: B'],
                ['A', t('Маг · Тайная магия', 'Mage · Arcane', 'Маг · Тайна магія'), t('Чародейская вспышка переработана 15.10.', 'Arcane Blast was reworked on Oct 15.', 'Arcane Blast переробили 15 жовтня.'), '—'],
                ['A*', t('Маг · Огонь', 'Mage · Fire', 'Маг · Вогонь'), t('Криты и поджоги.', 'Crits and ignites.', 'Криті та підпали.'), t('Noobtoboss: B для подземелий', 'Noobtoboss: B for dungeons', 'Noobtoboss: B для підземель')],
                ['A', t('Чернокнижник · Колдовство', 'Warlock · Affliction', 'Чорнокнижник · Прокляття'), t('Периодический урон, сильнее всех соло.', 'Damage over time, the strongest solo.', 'Періодична шкода, найсильніший наодинці.'), '—'],
                ['A', t('Чернокнижник · Демонология', 'Warlock · Demonology', 'Чорнокнижник · Демонологія'), t('Лучший спек подземелий по Noobtoboss.', 'The best dungeon spec according to Noobtoboss.', 'Найкраща спеціалізація підземель за Noobtoboss.'), '—'],
                ['A', t('Чернокнижник · Разрушение', 'Warlock · Destruction', 'Чорнокнижник · Руйнування'), t('Бурст, данных мало.', 'Burst, little data.', 'Бурст, даних мало.'), t('только RankedBoost', 'RankedBoost only', 'лише RankedBoost')],
                ['B', t('Воин · Оружие', 'Warrior · Arms', 'Воїн · Зброя'), t('Двуручное оружие, ветка под PvP.', 'Two-handed weapons, a PvP-oriented tree.', 'Дворучна зброя, гілка під PvP.'), '—'],
                ['B*', t('Жрец · Темная магия', 'Priest · Shadow', 'Жрець · Темрява'), t('Усилена 15.10.', 'Buffed on Oct 15.', 'Підсилена 15 жовтня.'), t('RankedBoost: A, Noobtoboss: отстаёт', 'RankedBoost: A, Noobtoboss: lags behind', 'RankedBoost: A, Noobtoboss: відстає')],
                ['B*', t('Шаман · Стихии', 'Shaman · Elemental', 'Шаман · Стихії'), t('Выброс лавы и Покорение стихий усилены 15.10.', 'Lava Burst and Elemental Mastery were buffed on Oct 15.', 'Lava Burst і Elemental Mastery підсилили 15 жовтня.'), 'RankedBoost: A'],
                ['B', t('Маг · Лёд', 'Mage · Frost', 'Маг · Лід'), t('Сильнее на прокачке, чем в подземельях.', 'Stronger for leveling than in dungeons.', 'Сильніший на прокачуванні, ніж у підземеллях.'), '—'],
                ['B', t('Друид · Сила зверя (кошка)', 'Druid · Feral (cat)', 'Друїд · Сила звіра (кіт)'), t('Масштабируется с оружием.', 'Scales with weapons.', 'Масштабується зі зброєю.'), '—'],
                ['C', t('Разбойник · Скрытность', 'Rogue · Subtlety', 'Розбійник · Непомітність'), t('Ветка для PvP.', 'A PvP tree.', 'Гілка для PvP.'), '—'],
                ['C', t('Друид · Баланс', 'Druid · Balance', 'Друїд · Баланс'), t('Затмение пока выглядит слабо.', 'Eclipse still looks weak.', 'Eclipse поки виглядає слабко.'), '—'],
            ]}),
                ]},
            ]),
        ]},
        {'id': 'pvp', 'title': 'PvP', 'blocks': [
            ('text', [t('Полей боя и арен на бете не было: оценки по дуэлям, мировому PvP и турниру Forever Open (18.10, только Орда, бой 1 на 1, уровень 30).', 'There were no battlegrounds or arenas in the beta: ratings come from duels, world PvP and the Forever Open tournament (Oct 18, Horde only, 1v1, level 30).', 'Полів бою й арен у бета-версії не було: оцінки за дуелями, світовим PvP і турніром Forever Open (18 жовтня, лише Орда, бій 1 на 1, 30 рівень).')]),
            ('table', {'head': [t('Тир', 'Tier', 'Тір'), t('Спек', 'Spec', 'Спеціалізація'), t('Почему', 'Why', 'Чому'), t('Где расходятся', 'Where sources differ', 'Де розходяться')], 'rows': [
                ['S', t('Разбойник · Ликвидация', 'Rogue · Assassination', 'Розбійник · Ліквідація'), t('Яды и контроль из скрытности.', 'Poisons and control from stealth.', 'Отрути й контроль із невидимості.'), '—'],
                ['S', t('Разбойник · Скрытность', 'Rogue · Subtlety', 'Розбійник · Непомітність'), t('Лучшая PvP-ветка разбойника.', 'The rogue’s best PvP tree.', 'Найкраща PvP-гілка розбійника.'), '—'],
                ['S', t('Жрец · Послушание', 'Priest · Discipline', 'Жрець · Послух'), t('Покаяние и щиты.', 'Penance and shields.', 'Penance і щити.'), '—'],
                ['S', t('Чернокнижник · Колдовство', 'Warlock · Affliction', 'Чорнокнижник · Прокляття'), t('Сильнее всех кастеров соло; Kami ждёт его сильным на полях боя.', 'The strongest caster solo; Kami expects it to be strong in battlegrounds.', 'Сильніший за всіх кастерів наодинці; Kami чекає, що він буде сильним на полях бою.'), 'RankedBoost: A'],
                ['A', t('Паладин · Воздаяние', 'Paladin · Retribution', 'Паладин · Відплата'), '—', '—'],
                ['A', t('Охотник · Стрельба', 'Hunter · Marksmanship', 'Мисливець · Стрільба'), t('Kami считает её очень сильной.', 'Kami considers it very strong.', 'Kami вважає її дуже сильною.'), '—'],
                ['A*', t('Охотник · Выживание', 'Hunter · Survival', 'Мисливець · Виживання'), t('Ближний бой у охотника слабее в PvP.', 'The hunter’s melee is weaker in PvP.', 'Ближній бій мисливця слабший у PvP.'), '—'],
                ['A*', t('Разбойник · Бой', 'Rogue · Combat', 'Розбійник · Бій'), '—', t('RankedBoost: S, Kami: слабее в PvP', 'RankedBoost: S, Kami: weaker in PvP', 'RankedBoost: S, Kami: слабший у PvP')],
                ['A', t('Жрец · Темная магия', 'Priest · Shadow', 'Жрець · Темрява'), t('Переживает бой 1 на 1.', 'Survives a 1v1 fight.', 'Переживає бій 1 на 1.'), '—'],
                ['A*', t('Шаман · Совершенствование', 'Shaman · Enhancement', 'Шаман · Вдосконалення'), t('Мобильный, Призрачный волк.', 'Mobile, Ghost Wolf.', 'Мобільний, Ghost Wolf.'), '—'],
                ['A*', t('Маг · Тайная магия', 'Mage · Arcane', 'Маг · Тайна магія'), t('Бурст.', 'Burst.', 'Бурст.'), 'RankedBoost: S'],
                ['A', t('Маг · Лёд', 'Mage · Frost', 'Маг · Лід'), t('Контроль и замедления.', 'Control and slows.', 'Контроль і уповільнення.'), '—'],
                ['A*', t('Чернокнижник · Демонология', 'Warlock · Demonology', 'Чорнокнижник · Демонологія'), t('Kami ждёт его сильным на полях боя.', 'Kami expects it to be strong in battlegrounds.', 'Kami чекає, що він буде сильним на полях бою.'), 'RankedBoost: B'],
                ['A', t('Чернокнижник · Разрушение', 'Warlock · Destruction', 'Чорнокнижник · Руйнування'), t('Бурст.', 'Burst.', 'Бурст.'), t('только RankedBoost', 'RankedBoost only', 'лише RankedBoost')],
                ['A', t('Друид · Баланс', 'Druid · Balance', 'Друїд · Баланс'), t('В PvP сильнее, чем в PvE.', 'Stronger in PvP than in PvE.', 'У PvP сильніший, ніж у PvE.'), '—'],
                ['A*', t('Друид · Сила зверя', 'Druid · Feral', 'Друїд · Сила звіра'), t('Берсерк, масштабируется с оружием.', 'Berserk, scales with weapons.', 'Berserk, масштабується зі зброєю.'), 'RankedBoost: S'],
                ['B', t('Воин · Оружие', 'Warrior · Arms', 'Воїн · Зброя'), t('В дуэлях беты слаб.', 'Weak in beta duels.', 'У дуелях бети слабкий.'), 'gamer-guides: A'],
                ['B*', t('Воин · Неистовство', 'Warrior · Fury', 'Воїн · Лють'), '—', 'RankedBoost: A'],
                ['B*', t('Паладин · Свет', 'Paladin · Holy', 'Паладин · Світло'), '—', 'RankedBoost: A'],
                ['B', t('Паладин · Защита', 'Paladin · Protection', 'Паладин · Захист'), '—', '—'],
                ['B', t('Охотник · Повелитель зверей', 'Hunter · Beast Mastery', 'Мисливець · Володіння звірами'), '—', '—'],
                ['B*', t('Шаман · Стихии', 'Shaman · Elemental', 'Шаман · Стихії'), t('Усилены 15.10.', 'Buffed on Oct 15.\xa0', 'Підсилені 15 жовтня.'), 'RankedBoost: A'],
                ['B', t('Шаман · Исцеление', 'Shaman · Restoration', 'Шаман · Зцілення'), '—', '—'],
                ['—', t('Маг · Огонь', 'Mage · Fire', 'Маг · Вогонь'), t('Нет PvP-оценок источников', 'No source PvP ratings', 'Немає PvP-оцінок джерел'), '—'],
                ['B*', t('Друид · Исцеление', 'Druid · Restoration', 'Друїд · Зцілення'), '—', 'gamer-guides: A'],
                ['C', t('Воин · Защита', 'Warrior · Protection', 'Воїн · Захист'), '—', '—'],
                ['C*', t('Жрец · Свет', 'Priest · Holy', 'Жрець · Світло'), t('Без иммунитетов.', 'No immunities.', 'Без імунітетів.'), 'RankedBoost: D'],
            ]}),
            ('tip', t('Воин в дуэлях беты внизу, но турнир 1 на 1 — не поле боя. Kami ждёт, что на полях боя воин поднимется.', 'Warrior sits at the bottom in beta duels, but a 1v1 tournament is not a battleground. Kami expects warriors to rise in battlegrounds.', 'Воїн у дуелях бети внизу, але турнір 1 на 1 — не поле бою. Kami чекає, що на полях бою воїн підніметься.')),
        ]},
        {'id': 'disputed', 'title': t('Где источники расходятся', 'Where sources disagree', 'Де джерела розходяться'), 'blocks': [
            ('steps', [
                {'t': t('Охотник в PvE', 'Hunter in PvE', 'Мисливець у PvE'),
                 'd': t('Noobtoboss ставит S, RankedBoost — A.', 'Noobtoboss gives S, RankedBoost gives A.', 'Noobtoboss ставить S, RankedBoost — A.')},
                {'t': t('Кто сильнее, Паладин или Охотник', 'Which is stronger, Paladin or Hunter', 'Хто сильніший, Паладин чи Мисливець'),
                 'd': t('в одном списке S только у Паладина, в другом у обоих.', 'one list gives S only to Paladin, another to both.', 'в одному списку S лише в Паладина, в іншому в обох.')},
                {'t': t('Жрец на прокачке', 'Priest while leveling', 'Жрець на прокачуванні'),
                 'd': t('Noobtoboss — C, gamer-guides — S для Послушания.', 'Noobtoboss says C, gamer-guides says S for Discipline.', 'Noobtoboss — C, gamer-guides — S для Послуху.')},
                {'t': t('Жрец, Свет', 'Priest, Holy', 'Жрець, Світло'),
                 'd': t('RankedBoost в одном списке ставит его в S, B и D.', 'RankedBoost puts it in S, B and D in a single list.', 'RankedBoost в одному списку ставить його в S, B і D.')},
                {'t': t('Маг в PvP', 'Mage in PvP', 'Маг у PvP'),
                 'd': t('RankedBoost ставит Тайную магию в S.', 'RankedBoost puts Arcane in S.', 'RankedBoost ставить Тайну магію в S.')},
            ]),
        ]},
        {'id': 'gabella', 'title': t('Оценка Gabella', 'Gabella’s view', 'Оцінка Gabella'), 'blocks': [
            ('text', [t('Мы сверили буквы источников со способностями спеков: контроль, баффы, лечение, живучесть. Урон не мерили, поэтому своих букв не ставим. Показываем только сдвиг: где по способностям спек выше или ниже, чем у источников.', 'We checked the sources’ letters against each spec’s abilities: control, buffs, healing, survivability. We haven’t measured damage, so we don’t give letters of our own. We only show the shift: where a spec’s abilities put it higher or lower than the sources do.', 'Ми звірили літери джерел зі здібностями спеціалізацій: контроль, бафи, лікування, живучість. Шкоду не міряли, тому власних літер не ставимо. Показуємо лише зсув: де за здібностями спеціалізація вища чи нижча, ніж у джерел.'),
                      t('Спеки, которых здесь нет, — без сдвига. Спеков урона в PvE здесь нет вовсе: их место решает урон.', 'Specs not listed here have no shift. Damage specs in PvE are left out entirely: damage decides their place.', 'Спеціалізації, яких тут немає, — без зсуву. Спеціалізацій шкоди в PvE тут немає взагалі: їхнє місце визначає шкода.')]),
            ('tip', t('По бете. После старта 4 ноября заменим живыми данными: логи, время прокачки, поля боя.', 'Beta data. After the Nov 4 launch we’ll replace it with live data: logs, leveling times, battlegrounds.', 'За бетою. Після старту 4 листопада замінимо живими даними: логи, час прокачування, поля бою.')),
            ('tabs', [
                {'id': 'g-leveling', 't': t('Прокачка соло', 'Solo leveling', 'Прокачування соло'), 'blocks': [
                    ('table', {'head': [t('Спек', 'Spec', 'Спеціалізація'), 'Gabella', t('Почему', 'Why', 'Чому')], 'rows': [
                [t('Охотник · Повелитель зверей', 'Hunter · Beast Mastery', 'Мисливець · Володіння звірами'), t('↓\xa0ниже', '↓\xa0lower', '↓\xa0нижче'), t('Нет самолечения; скорость убийства мы не мерили.', 'No self-healing; we haven’t measured kill speed.', 'Немає самолікування; швидкість убивства ми не міряли.')],
                [t('Маг · Лёд', 'Mage · Frost', 'Маг · Лід'), t('↓\xa0ниже', '↓\xa0lower', '↓\xa0нижче'), t('Урон по площади на прокачке ослаблен, мана — слабое место.', 'Area damage is nerfed for leveling, and mana is a weak spot.', 'Шкоду по площі на прокачуванні послаблено, мана — слабке місце.')],
                [t('Разбойник · Ликвидация или Бой', 'Rogue · Assassination or Combat', 'Розбійник · Ліквідація або Бій'), t('↓\xa0ниже', '↓\xa0lower', '↓\xa0нижче'), t('Нет самолечения: после каждого боя отдых.', 'No self-healing: rest after every fight.', 'Немає самолікування: після кожного бою відпочинок.')],
                [t('Жрец · Темная магия', 'Priest · Shadow', 'Жрець · Темрява'), t('↑\xa0выше', '↑\xa0higher', '↑\xa0вище'), t('Самолечение и дешёвые заклинания в Облике Тьмы.', 'Self-healing and cheap spells in Shadowform.', 'Самолікування й дешеві заклинання в Shadowform.')],
            ]}),
                ]},
                {'id': 'g-pve', 't': t('Танки и лекари', 'Tanks and healers', 'Танки й цілителі'), 'blocks': [
                    ('table', {'head': [t('Спек', 'Spec', 'Спеціалізація'), 'Gabella', t('Почему', 'Why', 'Чому')], 'rows': [
                [t('Воин · Защита', 'Warrior · Protection', 'Воїн · Захист'), t('↑\xa0выше в рейде', '↑\xa0higher in raids', '↑\xa0вище в рейді'), t('Полный набор танка, ярость не кончается в долгом бою.', 'A full tank toolkit; rage doesn’t run out in long fights.', 'Повний набір танка, ярість не закінчується в довгому бою.')],
                [t('Друид · Сила зверя (медведь)', 'Druid · Feral (bear)', 'Друїд · Сила звіра (ведмідь)'), t('↑\xa0выше в подземельях', '↑\xa0higher in dungeons', '↑\xa0вище в підземеллях'), t('Первый медведь в группе: Вожак стаи и воскрешение в бою.', 'The first bear in a group: Leader of the Pack and a combat resurrection.', 'Перший ведмідь у групі: Leader of the Pack і воскресіння в бою.')],
                [t('Друид · Исцеление', 'Druid · Restoration', 'Друїд · Зцілення'), t('↑\xa0выше', '↑\xa0higher', '↑\xa0вище'), t('Буйный рост, эффекты лечения складываются.', 'Wild Growth; healing effects stack.', 'Wild Growth, ефекти лікування складаються.')],
                [t('Жрец · Свет', 'Priest · Holy', 'Жрець · Світло'), t('↑\xa0выше', '↑\xa0higher', '↑\xa0вище'), t('Полный набор лекаря: лечение по площади и возврат маны.', 'A full healer toolkit: area healing and mana return.', 'Повний набір цілителя: лікування по площі й повернення мани.')],
            ]}),
                ]},
                {'id': 'g-pvp', 't': 'PvP', 'blocks': [
                    ('text', [t('Сдвиг считаем по контролю и бурсту. Живучесть — в колонке «Почему».', 'The shift is based on control and burst. Survivability is in the “Why” column.', 'Зсув рахуємо за контролем і бурстом. Живучість — у колонці «Чому».')]),
                    ('table', {'head': [t('Спек', 'Spec', 'Спеціалізація'), 'Gabella', t('Почему', 'Why', 'Чому')], 'rows': [
                [t('Охотник · Стрельба', 'Hunter · Marksmanship', 'Мисливець · Стрільба'), t('↑\xa0выше', '↑\xa0higher', '↑\xa0вище'), t('Ловушки в бою и сильное окно урона; живучесть низкая.', 'Traps in combat and a strong damage window; low survivability.', 'Пастки в бою й сильне вікно шкоди; живучість низька.')],
                [t('Охотник · Повелитель зверей', 'Hunter · Beast Mastery', 'Мисливець · Володіння звірами'), t('↑\xa0выше', '↑\xa0higher', '↑\xa0вище'), t('Ловушки в бою и Устрашение; живучесть низкая.', 'Traps in combat and Intimidation; low survivability.', 'Пастки в бою й Intimidation; живучість низька.')],
                [t('Маг · Тайная магия', 'Mage · Arcane', 'Маг · Тайна магія'), t('↑\xa0выше', '↑\xa0higher', '↑\xa0вище'), t('Контроль мага и сильный бурст.', 'Mage control and strong burst.', 'Контроль мага й потужний бурст.')],
                [t('Чернокнижник · Разрушение', 'Warlock · Destruction', 'Чорнокнижник · Руйнування'), t('↑\xa0выше', '↑\xa0higher', '↑\xa0вище'), t('Контроль и сильный бурст; живучесть низкая.', 'Control and strong burst; low survivability.', 'Контроль і потужний бурст; живучість низька.')],
                [t('Жрец · Свет', 'Priest · Holy', 'Жрець · Світло'), t('↑\xa0выше', '↑\xa0higher', '↑\xa0вище'), t('Контроль, урон и живучесть средние.', 'Average control, damage and survivability.', 'Контроль, шкода й живучість середні.')],
                [t('Жрец · Послушание', 'Priest · Discipline', 'Жрець · Послух'), t('↓\xa0ниже', '↓\xa0lower', '↓\xa0нижче'), t('Сила в щитах и Покаянии, а не в контроле; здесь источники, вероятно, точнее.', 'Its strength is shields and Penance, not control; here the sources are probably closer.', 'Сила в щитах і Penance, а не в контролі; тут джерела, імовірно, точніші.')],
                [t('Паладин · Воздаяние', 'Paladin · Retribution', 'Паладин · Відплата'), t('↓\xa0ниже', '↓\xa0lower', '↓\xa0нижче'), t('Контроль и бурст средние.', 'Average control and burst.', 'Контроль і бурст середні.')],
                [t('Жрец · Темная магия', 'Priest · Shadow', 'Жрець · Темрява'), t('↓\xa0ниже', '↓\xa0lower', '↓\xa0нижче'), t('Контроль и бурст средние, живучесть низкая.', 'Average control and burst; low survivability.', 'Контроль і бурст середні, живучість низька.')],
                [t('Шаман · Совершенствование', 'Shaman · Enhancement', 'Шаман · Вдосконалення'), t('↓\xa0ниже', '↓\xa0lower', '↓\xa0нижче'), t('Контроль и бурст средние; живучесть высокая.', 'Average control and burst; high survivability.', 'Контроль і бурст середні; живучість висока.')],
                [t('Друид · Баланс', 'Druid · Balance', 'Друїд · Баланс'), t('↓\xa0ниже', '↓\xa0lower', '↓\xa0нижче'), t('Контроль средний, одно окно урона; живучесть высокая.', 'Average control, one damage window; high survivability.', 'Контроль середній, одне вікно шкоди; живучість висока.')],
                [t('Друид · Сила зверя', 'Druid · Feral', 'Друїд · Сила звіра'), t('↓\xa0ниже', '↓\xa0lower', '↓\xa0нижче'), t('Контроль средний, одно окно урона; живучесть высокая.', 'Average control, one damage window; high survivability.', 'Контроль середній, одне вікно шкоди; живучість висока.')],
                [t('Воин · Неистовство', 'Warrior · Fury', 'Воїн · Лють'), t('↓\xa0ниже', '↓\xa0lower', '↓\xa0нижче'), t('Мало контроля, живучесть низкая.', 'Little control; low survivability.', 'Мало контролю, живучість низька.')],
                [t('Паладин · Свет', 'Paladin · Holy', 'Паладин · Світло'), t('↓\xa0ниже', '↓\xa0lower', '↓\xa0нижче'), t('Ветка лечения: урона мало, зато трудно убить.', 'A healing tree: little damage, but hard to kill.', 'Гілка лікування: шкоди мало, зате важко вбити.')],
                [t('Паладин · Защита', 'Paladin · Protection', 'Паладин · Захист'), t('↓\xa0ниже', '↓\xa0lower', '↓\xa0нижче'), t('Ветка танка: мало урона и контроля.', 'A tank tree: little damage and control.', 'Гілка танка: мало шкоди й контролю.')],
                [t('Шаман · Исцеление', 'Shaman · Restoration', 'Шаман · Зцілення'), t('↓\xa0ниже', '↓\xa0lower', '↓\xa0нижче'), t('Ветка лечения: урона мало, зато трудно убить.', 'A healing tree: little damage, but hard to kill.', 'Гілка лікування: шкоди мало, зате важко вбити.')],
                [t('Друид · Исцеление', 'Druid · Restoration', 'Друїд · Зцілення'), t('↓\xa0ниже', '↓\xa0lower', '↓\xa0нижче'), t('Ветка лечения: урона мало, зато трудно убить.', 'A healing tree: little damage, but hard to kill.', 'Гілка лікування: шкоди мало, зате важко вбити.')],
            ]}),
                ]},
            ]),
        ]},
        {'id': 'after', 'title': t('Что изменится после старта', 'What will change after launch', 'Що зміниться після старту'), 'blocks': [
            ('steps', [
                {'t': t('Уровни 31–60', 'Levels 31–60', 'Рівні 31–60'),
                 'd': t('на бете их не было, многие таланты и умения открываются выше 30.', 'they weren’t in the beta, and many talents and abilities unlock above 30.', 'у бета-версії їх не було, а багато талантів і умінь відкривається вище 30.')},
                {'t': t('Рейды с 09.12', 'Raids from Dec 9', 'Рейди з 9 грудня'),
                 'd': t('оценки рейдовых спеков пока без логов.', 'raid spec ratings have no logs yet.', 'оцінки рейдових спеціалізацій поки що без логів.')},
                {'t': t('Поля боя', 'Battlegrounds', 'Поля бою'),
                 'd': t('все PvP-оценки сейчас по дуэлям.', 'all PvP ratings are currently based on duels.', 'усі PvP-оцінки наразі за дуелями.')},
                {'t': t('Правки баланса', 'Balance changes', 'Правки балансу'),
                 'd': t('15.10 ослаблены Воздаяние и Защита паладина, усилены Стихии, Совершенствование и Темная магия. Noobtoboss ждёт ослабления Охотника и Паладина.', 'on Oct 15 Retribution and Paladin Protection were nerfed; Elemental, Enhancement and Shadow were buffed. Noobtoboss expects nerfs for Hunter and Paladin.', '15 жовтня послабили Відплату й Захист паладина, підсилили Стихії, Вдосконалення й Темряву. Noobtoboss чекає послаблення Мисливця та Паладина.')},
            ]),
        ]},
        {'id': 'faq', 'title': t('Частые вопросы', 'Common questions', 'Часті питання'), 'blocks': [
            ('faq', [
                {'id': 'q1', 'q': t('Какой класс самый сильный в WoW Forever?', 'Which class is the strongest in WoW Forever?', 'Який клас найсильніший у WoW Forever?'),
                 'a': [t('По бете — Паладин в PvE, Чернокнижник и Разбойник в PvP. Это данные 30 уровня, обновим после старта 4 ноября.', 'By beta data: Paladin in PvE, Warlock and Rogue in PvP. This is level 30 data; we’ll update it after the Nov 4 launch.', 'За бетою — Паладин у PvE, Чорнокнижник і Розбійник у PvP. Це дані 30 рівня, оновимо після старту 4 листопада.')]},
                {'id': 'q2', 'q': t('Какой класс быстрее всех качается?', 'Which class levels fastest?', 'Який клас прокачується найшвидше?'),
                 'a': [t('Охотник и Маг, примерно на 8% быстрее среднего. Медленнее всех Воин.', 'Hunter and Mage, about 8% faster than average. Warrior is the slowest.', 'Мисливець і Маг, приблизно на 8% швидше за середнє. Найповільніший — Воїн.')]},
                {'id': 'q3', 'q': t('Какой лекарь лучший?', 'Which healer is the best?', 'Який цілитель найкращий?'),
                 'a': [t('Жрец Послушания и Шаман Исцеления.', 'Discipline Priest and Restoration Shaman.', 'Жрець Послуху та Шаман Зцілення.')]},
                {'id': 'q4', 'q': t('Какой танк лучший?', 'Which tank is the best?', 'Який танк найкращий?'),
                 'a': [t('Паладин Защиты, следом Воин Защиты.', 'Protection Paladin, followed by Protection Warrior.', 'Паладин Захисту, далі Воїн Захисту.')]},
                {'id': 'q5', 'q': t('Можно ли верить тир-листу до релиза?', 'Can I trust the tier list before release?', 'Чи можна вірити тір-листу до релізу?'),
                 'a': [t('Как ориентиру: на бете не было уровней 31–60, рейдов и полей боя, к 60 уровню расклад может измениться.', 'As a guide: the beta had no levels 31–60, raids or battlegrounds, so the picture may change by level 60.', 'Як орієнтиру: у бета-версії не було рівнів 31–60, рейдів і полів бою, тож до 60 рівня розклад може змінитися.')]},
            ]),
        ]},
        {'id': 'related', 'title': t('Смотрите также', 'See also', 'Дивіться також'), 'blocks': [
            ('tiles', [{'t': t('Лучшая раса для каждого класса', 'Best Race for Every Class', 'Найкраща раса для кожного класу'), 'd': t('Какая раса сильнее для вашего класса', 'Which race is stronger for your class', 'Яка раса сильніша для вашого класу'), 'href': 'guides/best-race/', 'art': 'hero_races'}, {'t': t('Классы', 'Classes', 'Класи'), 'd': t('Какой класс выбрать и сравнение', 'Which class to pick, compared', 'Який клас обрати й порівняння'), 'href': 'classes/', 'art': 'hero_classes'}]),
        ]},
    ],
})

# ---------- legacy ----------

GUIDES.append({
    'slug': 'legacy', 'art': 'hero_guides', 'hero': 'hero_guides',
    'title': t('Система Legacy', 'The Legacy System', 'Система Legacy'),
    'lead': t('Legacy — прогресс на весь аккаунт Battle.net. Очки дают за испытания: уровни, профессии, PvP, подземелья и рейды. Тратите их на перки отдельно на каждом персонаже, на старте до 16 очков.', 'Legacy is progress shared across your whole Battle.net account. Challenges give you points: levels, professions, PvP, dungeons and raids. You spend them on perks separately on each character, up to 16 points at launch.', 'Legacy — прогрес на весь обліковий запис Battle.net. Очки дають за випробування: рівні, професії, PvP, підземелля та рейди. Витрачаєте їх на перки окремо на кожному персонажі, на старті до 16.'),
    'tile': t('Очки, испытания, перки и награды', 'Points, challenges, perks and rewards', 'Очки, випробування, перки та нагороди'),
    'pills': [t('65 испытаний', '65 challenges', '65 випробувань'), t('16 очков на персонажа', '16 points per character', '16 очок на персонажа'), t('Открывается на 25 уровне', 'Unlocks at level 25', 'Відкривається на 25 рівні')],
    'sources': [
        (t('Blizzard: система Legacy', 'Blizzard: Legacy system', 'Blizzard: система Legacy'), 'https://news.blizzard.com/en-gb/article/24307383'),
        ('Warcraft Tavern: Legacy', 'https://www.warcrafttavern.com/forever/guides/legacy/'),
    ],
    'sections': [
        {'id': 'start', 'title': t('Как открыть', 'How to unlock it', 'Як відкрити'), 'blocks': [
            ('steps', [
                {'t': t('Первое очко', 'First point', 'Перше очко'),
                 'd': t('Legacy открывается с первым очком: 25 уровень на персонаже, 150 в основной профессии (не сбор) или исследование всей карты.', 'Legacy unlocks with your first point: level 25 on a character, 150 in a main profession (not gathering) or exploring the entire map.', 'Legacy відкривається з першим очком: 25 рівень на персонажі, 150 в основній професії (не збирання) або дослідження всієї мапи.')},
                {'t': t('Окно', 'Window', 'Вікно'),
                 'd': t('Горячая клавиша Y или значок щита в меню.', 'Hotkey Y or the shield icon in the menu.', 'Гаряча клавіша Y або значок щита в меню.')},
                {'t': t('На весь аккаунт', 'Account-wide', 'На весь обліковий запис'),
                 'd': t('Очки общие для всех персонажей аккаунта не-Hardcore, тратит их каждый персонаж по-своему.', 'Points are shared by all non-Hardcore characters on the account; each character spends them its own way.', 'Очки спільні для всіх персонажів облікового запису, крім Hardcore, а витрачає їх кожен персонаж по-своєму.')},
                {'t': t('Лимит на старте', 'Limit at launch', 'Ліміт на старті'),
                 'd': t('На персонажа не больше 16 очков. Остальные копятся на аккаунте и открывают награды.', 'No more than 16 points per character. The rest pile up on the account and unlock rewards.', 'На персонажа не більше 16 очок. Решта накопичується на обліковому записі й відкриває нагороди.')},
            ]),
            ('tip', t('Альты не обязательны: один персонаж без твинков может набрать до 29 очков, а потратить нужно 16.', 'Alts aren’t required: a single character without alts can earn up to 29 points, and you only need to spend 16.', 'Твінки не обов’язкові: один персонаж без твінків може набрати до 29 очок, а витратити потрібно 16.')),
        ]},
        {'id': 'challenges', 'title': t('Испытания: где взять очки', 'Challenges: where to get points', 'Випробування: де брати очки'), 'blocks': [
            ('text', [t('Каждое испытание даёт 1 очко. Всего их 65 в шести категориях.', 'Each challenge gives 1 point. There are 65 of them in six categories.', 'Кожне випробування дає 1 очко. Усього їх 65 у шести категоріях.')]),
            ('table', {'head': [t('Категория', 'Category', 'Категорія'), t('Очки', 'Points', 'Очки'), t('За что', 'For what', 'За що')], 'rows': [
                [t('Классы', 'Classes', 'Класи'), '27', t('25, 45 и 60 уровень на каждом из 9 классов', 'Levels 25, 45 and 60 on each of the 9 classes', '25, 45 і 60 рівень на кожному з 9 класів')],
                [t('Профессии', 'Professions', 'Професії'), '18', t('150, 225 и 300 навыка в каждой основной профессии, кроме сбора: Алхимия, Кузнечное дело, Наложение чар, Инженерное дело, Кожевничество, Портняжное дело', '150, 225 and 300 skill in each main profession except gathering: Alchemy, Blacksmithing, Enchanting, Engineering, Leatherworking, Tailoring', '150, 225 і 300 очок навички в кожній основній професії, крім збирання: Алхімія, Ковальство, Зачарування, Інженерія, Шкіряництво, Кравецтво')],
                ['PvP', '12', t('звания 3, 7, 10, 13 и 14; «Превознесение» с репутацией каждого поля боя (Alterac Valley, Arathi Basin, Warsong Gulch, Darkspear Islands); 4, 7 и 10 неделя сезонного пути Field of Honor', 'Ranks 3, 7, 10, 13 and 14; Exalted reputation with each battleground (Alterac Valley, Arathi Basin, Warsong Gulch, Darkspear Islands); weeks 4, 7 and 10 of the seasonal Field of Honor path', 'Звання 3, 7, 10, 13 і 14; репутація Exalted на кожному полі бою (Alterac Valley, Arathi Basin, Warsong Gulch, Darkspear Islands); 4, 7 і 10 тиждень сезонного шляху Field of Honor')],
                [t('Подземелья', 'Dungeons', 'Підземелля'), '3', t('последний босс во всех подземельях 15–25, 26–45 и 46–60 уровня', 'The last boss in all dungeons of levels 15–25, 26–45 and 46–60', 'Останній бос у всіх підземеллях 15–25, 26–45 і 46–60 рівня')],
                [t('Рейды', 'Raids', 'Рейди'), '3', t('Onyxia; все 13 боссов Hyjal Summit; все 8 боссов Barrow Deeps', 'Onyxia; all 13 bosses of Hyjal Summit; all 8 bosses of Barrow Deeps', 'Onyxia; усі 13 босів Hyjal Summit; усі 8 босів Barrow Deeps')],
                [t('Приключения', 'Adventures', 'Пригоди'), '2', t('вся карта мира на одном персонаже; цепочка заданий Lord Valthalak', 'The whole world map on one character; the Lord Valthalak quest chain', 'Уся мапа світу на одному персонажі; ланцюжок завдань Lord Valthalak')],
            ]}),
            ('tip', t('Если до 25 уровня далеко, доведите ремесло до 150: Legacy откроется раньше. Сбор (травы, руда, шкуры) очков не даёт, но кормит ремесло.', 'If level 25 is far off, get a craft to 150: Legacy will unlock sooner. Gathering (herbs, ore, hides) gives no points, but it feeds your craft.', 'Якщо до 25 рівня ще далеко, доведіть ремесло до 150: Legacy відкриється раніше. Збирання (трави, руда, шкури) очок не дає, але годує ремесло.')),
        ]},
        {'id': 'perks', 'title': t('Перки', 'Perks', 'Перки'), 'blocks': [
            ('text', [t('Три дерева: Профессии, Приключения, Ресурсы. Числа рангов — по Warcraft Tavern. На бете в каждом дереве скрыты ещё два перка.', 'Three trees: Professions, Adventures, Resources. Rank counts are from Warcraft Tavern. In the beta each tree has two more hidden perks.', 'Три дерева: Професії, Пригоди, Ресурси. Числа рангів — за Warcraft Tavern. На бета-версії в кожному дереві приховано ще по два перки.')]),
            ('table', {'head': [t('Дерево', 'Tree', 'Дерево'), t('Перки (рангов)', 'Perks (ranks)', 'Перки (рангів)')], 'rows': [
                [t('Профессии', 'Professions', 'Професії'), t('Working Overtime (5): чаще растут навыки, включая классовые вроде Взлома замков. Bountiful Harvest (5): на 20% больше редких материалов при сборе. Master Chef (5): шанс лишнего блюда. Luremaster (2): шанс лишней рыбы с приманкой. Performance Bonus (3): шанс получить больше Merchant’s Favor за сданный ящик. Bartering (2): цены у торговцев ниже на 5%. Dedicated Study (1): раз в день +1 к самому низкому навыку профессии.', 'Working Overtime (5): skills improve more often, including class skills such as Lockpicking. Bountiful Harvest (5): 20% more rare materials when gathering. Master Chef (5): a chance for an extra dish. Luremaster (2): a chance for extra fish when using bait. Performance Bonus (3): a chance for more Merchant’s Favor for a delivered crate. Bartering (2): vendor prices 5% lower. Dedicated Study (1): once a day, +1 to your lowest profession skill.', 'Working Overtime (5): навички зростають частіше, зокрема класові, як-от злом замків. Bountiful Harvest (5): на 20% більше рідкісних матеріалів під час збирання. Master Chef (5): шанс на зайву страву. Luremaster (2): шанс на зайву рибу з принадою. Performance Bonus (3): шанс отримати більше Merchant’s Favor за зданий ящик. Bartering (2): ціни в торговців нижчі на 5%. Dedicated Study (1): раз на день +1 до найнижчої навички професії.')],
                [t('Приключения', 'Adventures', 'Пригоди'), t('Well Rested (5): быстрее копится отдых и выше его потолок. Thrill of Adventure (5): здоровье и мана за убийство вне подземелий. Talented (5): очки талантов с 9 уровня, на 5 рангах с 5. Field Guide (3): короче откат объектов лагеря. High Alert (2): лучше видно врагов в незаметности, кроме полей боя. Field Medicine (2): короче дебафф после бинта. Frequent Flier (1): перелёты на 50% дешевле и на 20% быстрее.', 'Well Rested (5): rest builds up faster and its cap is higher. Thrill of Adventure (5): health and mana for kills outside dungeons. Talented (5): talent points from level 9, from level 5 at rank 5. Field Guide (3): shorter cooldown on camp objects. High Alert (2): enemies in stealth are easier to see, except in battlegrounds. Field Medicine (2): shorter debuff after a bandage. Frequent Flier (1): flights 50% cheaper and 20% faster.', 'Well Rested (5): швидше накопичується відпочинок і вища його стеля. Thrill of Adventure (5): здоров’я та мана за вбивство поза підземеллями. Talented (5): очки талантів з 9 рівня, на 5 рангах з 5. Field Guide (3): коротший відкат об’єктів табору. High Alert (2): краще видно ворогів у невидимості, крім полів бою. Field Medicine (2): коротший дебаф після бинта. Frequent Flier (1): перельоти на 50% дешевші й на 20% швидші.')],
                [t('Ресурсы', 'Resources', 'Ресурси'), t('Gourmand (3): еда действует на 33% дольше. Permanence (2): баффы класса на группу и баффы лагеря длятся на 50% дольше. Reagent Economy (1): способностям класса не нужны покупные реагенты, объекты лагеря 1 уровня не требуют материалов. Reinforce (5): на 8% меньше потеря прочности. Diplomat (5): +2% репутации. For Great Honor (5): +2% Чести. The Quick and the Dead (2): быстрее бег призраком, а после воскрешения способности поддержки бесплатны минуту.', 'Gourmand (3): food lasts 33% longer. Permanence (2): class buffs on the group and camp buffs last 50% longer. Reagent Economy (1): class abilities need no bought reagents, level 1 camp objects need no materials. Reinforce (5): 8% less durability loss. Diplomat (5): +2% reputation. For Great Honor (5): +2% Honor. The Quick and the Dead (2): faster running as a ghost, and after resurrection support abilities are free for a minute.', 'Gourmand (3): їжа діє на 33% довше. Permanence (2): бафи класу на групу та бафи табору тривають на 50% довше. Reagent Economy (1): здібностям класу не потрібні куплені реагенти, об’єкти табору 1 рівня не потребують матеріалів. Reinforce (5): на 8% менша втрата міцності. Diplomat (5): +2% репутації. For Great Honor (5): +2% Честі. The Quick and the Dead (2): швидший біг привидом, а після воскресіння здібності підтримки безкоштовні протягом хвилини.')],
            ]}),
            ('tip', t('Первыми берите перки опыта и лагеря: Well Rested, Field Guide, Permanence. Reagent Economy ценен классам с реагентами, Talented — твинкам.', 'Take the experience and camp perks first: Well Rested, Field Guide, Permanence. Reagent Economy is worth it for classes with reagents, Talented for alts.', 'Першими беріть перки досвіду й табору: Well Rested, Field Guide, Permanence. Reagent Economy цінний класам із реагентами, Talented — твінкам.')),
            ('text', [t('Warcraft Tavern пишет про лимит 25 очков на дерево, Blizzard лимита на дерево не называет.', 'Warcraft Tavern mentions a limit of 25 points per tree; Blizzard names no per-tree limit.', 'Warcraft Tavern пише про ліміт 25 очок на дерево, Blizzard ліміту на дерево не називає.')]),
        ]},
        {'id': 'rewards', 'title': t('Награды', 'Rewards', 'Нагороди'), 'blocks': [
            ('text', [t('Награды открывает общее число очков на аккаунте, как бы вы их ни потратили. Забирать у Innkeeper Wiley в Ratchet.', 'Rewards unlock by the total number of points on the account, however you spent them. Collect them from Innkeeper Wiley in Ratchet.', 'Нагороди відкриває загальна кількість очок на обліковому записі, як би ви їх не витратили. Забирати в Innkeeper Wiley у Ratchet.')]),
            ('table', {'head': [t('Очки', 'Points', 'Очки'), t('Награда', 'Reward', 'Нагорода')], 'rows': [
                ['15', t('игрушка Holstered Replica Ironforge Air Rifle: оглушает других игроков и ведёт счёт попаданий', 'Toy: Holstered Replica Ironforge Air Rifle, which stuns other players and keeps a count of hits', 'іграшка Holstered Replica Ironforge Air Rifle: приголомшує інших гравців і веде лік влучань')],
                ['25', t('питомец Spectral Bear Cub', 'Pet: Spectral Bear Cub', 'улюбленець Spectral Bear Cub')],
                ['40', t('табард Spectral Bear Tabard', 'Tabard: Spectral Bear Tabard', 'табард Spectral Bear Tabard')],
                ['55', t('скакун Reins of the Spectral Bear, скорость +100%', 'Mount: Reins of the Spectral Bear, +100% speed', 'скакун Reins of the Spectral Bear, швидкість +100%')],
            ]}),
            ('text', [t('Это косметика, преимуществ в игре она не даёт. Новые награды, испытания и перки Blizzard обещает с каждым обновлением.', 'These are cosmetic and give no in-game advantage. Blizzard promises new rewards, challenges and perks with each update.', 'Це косметика, переваг у грі вона не дає. Нові нагороди, випробування та перки Blizzard обіцяє з кожним оновленням.')]),
        ]},
        {'id': 'hardcore', 'title': 'Hardcore', 'blocks': [
            ('text', [t('Hardcore на старте не будет. Когда он выйдет, испытания с обычных серверов в нём не засчитаются, а испытания из Hardcore засчитаются везде. PvP-испытания в Hardcore заменят 12 своих.', 'Hardcore won’t be available at launch. When it arrives, challenges from regular realms won’t count in it, while Hardcore challenges will count everywhere. Hardcore’s own PvP challenges will replace the 12 standard ones.', 'Hardcore на старті не буде. Коли він вийде, випробування зі звичайних серверів у ньому не зараховуватимуться, а випробування з Hardcore зараховуватимуться всюди. PvP-випробування в Hardcore замінять 12 власних.')]),
        ]},
        {'id': 'faq', 'title': t('Частые вопросы', 'Common questions', 'Часті питання'), 'blocks': [
            ('faq', [
                {'id': 'q1', 'q': t('Как открыть Legacy в WoW Forever?', 'How do I unlock Legacy in WoW Forever?', 'Як відкрити Legacy у WoW Forever?'),
                 'a': [t('Получите первое очко: 25 уровень, 150 в основной профессии (не сбор) или исследование всей карты. Окно открывается клавишей Y.', 'Earn your first point: level 25, 150 in a main profession (not gathering) or exploring the whole map. The window opens with the Y key.', 'Отримайте перше очко: 25 рівень, 150 в основній професії (не збирання) або дослідження всієї мапи. Вікно відкривається клавішею Y.')]},
                {'id': 'q2', 'q': t('Сколько очков Legacy можно потратить?', 'How many Legacy points can I spend?', 'Скільки очок Legacy можна витратити?'),
                 'a': [t('На старте до 16 на персонажа. Лишние копятся на аккаунте и открывают награды.', 'Up to 16 per character at launch. The extra points pile up on the account and unlock rewards.', 'На старті до 16 на персонажа. Зайві накопичуються на обліковому записі й відкривають нагороди.')]},
                {'id': 'q3', 'q': t('Нужно ли качать альтов ради Legacy?', 'Do I need to level alts for Legacy?', 'Чи потрібно качати твінків заради Legacy?'),
                 'a': [t('Нет. Один персонаж может набрать до 29 очков, а потратить нужно 16.', 'No. One character can earn up to 29 points, and you only need to spend 16.', 'Ні. Один персонаж може набрати до 29 очок, а витратити потрібно 16.')]},
                {'id': 'q4', 'q': t('Общие ли очки Legacy для всех персонажей?', 'Are Legacy points shared across all characters?', 'Чи спільні очки Legacy для всіх персонажів?'),
                 'a': [t('Да, на весь аккаунт Battle.net, кроме Hardcore. Перки каждый персонаж выбирает сам.', 'Yes, across the whole Battle.net account, except Hardcore. Each character picks its own perks.', 'Так, на весь обліковий запис Battle.net, крім Hardcore. Перки кожен персонаж обирає сам.')]},
                {'id': 'q5', 'q': t('Какие перки Legacy брать первыми?', 'Which Legacy perks should I take first?', 'Які перки Legacy брати першими?'),
                 'a': [t('Перки опыта и лагеря: Well Rested, Field Guide, Permanence. Классам с реагентами — Reagent Economy.', 'Experience and camp perks: Well Rested, Field Guide, Permanence. Reagent Economy for classes with reagents.', 'Перки досвіду й табору: Well Rested, Field Guide, Permanence. Класам із реагентами — Reagent Economy.')]},
            ]),
        ]},
    ],
})


GUIDES.sort(key=lambda g: ORDER.index(g['slug']))


# ---------- Разделы /classes/ и /races/: таблицы сравнения с главной (JS — из index.src.html, ref:start…ref:end) ----------

HUBS = [
    {'slug': 'classes', 'path': 'classes/', 'art': 'hero_classes', 'hero': 'hero_classes', 'js': 'classref',
     'title': t('Классы', 'Classes', 'Класи'),
     'lead': t('Какой класс выбрать в WoW Forever: короткий ответ под вашу цель, темп прокачки по бете и сравнение девяти классов.',
               'Which class to pick in WoW Forever: a short answer for your goal, leveling pace from the beta and all nine classes compared.',
               'Який клас обрати у WoW Forever: коротка відповідь під вашу мету, темп прокачки за бетою та порівняння дев’яти класів.'),
     'tile': t('Какой класс выбрать и сравнение', 'Which class to pick, compared', 'Який клас обрати й порівняння'),
     'sources': [('Warcraft Tavern', 'https://www.warcrafttavern.com/forever/guides/classes/'),
                 ('LFCarry', 'https://lfcarry.com/guides/wow-forever-classes')],
     'sections': [
        {'id': 'choose', 'title': t('Какой класс выбрать', 'Which class to pick', 'Який клас обрати'), 'blocks': [
            ('text', [t('Впервые в Classic — маг или охотник: они быстрее всех качаются, бьют издалека и уверенно играют одни. Дальше выбирайте по роли, которую хотите в группе.',
                        'New to Classic: mage or hunter. They level fastest, fight at range and do well solo. Beyond that, pick by the role you want in a group.',
                        'Вперше в Classic — маг або мисливець: вони найшвидше качаються, б’ють здалеку й упевнено грають самі. Далі обирайте за роллю, яку хочете в групі.')]),
            ('picks', {'head': [t('Что хотите', 'What you want', 'Що хочете'), t('Класс', 'Class', 'Клас'), t('Почему', 'Why', 'Чому')], 'rows': [
                (t('Быстрее до 60', 'Reach 60 fastest', 'Швидше до 60'), ['mage', 'hunter'],
                 t('Самая быстрая прокачка по прогнозам беты, примерно на 8% быстрее среднего.',
                   'The fastest leveling in beta projections, about 8% faster than average.',
                   'Найшвидша прокачка за прогнозами бети, приблизно на 8% швидше за середню.')),
                (t('Играть одному', 'Play solo', 'Грати самому'), ['hunter', 'warlock', 'mage'],
                 t('У охотника и чернокнижника питомец держит врага, у чернокнижника ещё Жизнеотвод. Маг сам делает еду и воду.',
                   'The hunter and warlock pet holds the enemy, and the warlock also has Life Tap. The mage conjures their own food and water.',
                   'У мисливця й чорнокнижника вихованець тримає ворога, у чорнокнижника ще Life Tap. Маг сам робить їжу та воду.')),
                (t('Лечить', 'Heal', 'Лікувати'), ['priest', 'paladin', 'druid', 'shaman'],
                 t('Жрец всегда нужен группе. Паладин и друид могут сменить роль, шаман лечит и ставит тотемы для группы.',
                   'A priest is always wanted in a group. The paladin and druid can switch roles, the shaman heals and drops totems for the group.',
                   'Жрець завжди потрібен групі. Паладин і друїд можуть змінити роль, шаман лікує й ставить тотеми для групи.')),
                (t('Танковать', 'Tank', 'Танкувати'), ['warrior', 'paladin', 'druid'],
                 t('Воин — лучший танк, но качается медленнее всех. Паладин и друид танкуют и могут лечить.',
                   'The warrior is the best tank but levels the slowest. The paladin and druid tank and can heal.',
                   'Воїн — найкращий танк, але качається найповільніше. Паладин і друїд танкують і можуть лікувати.')),
                (t('Урон в ближнем бою', 'Melee damage', 'Шкода в ближньому бою'), ['rogue', 'warrior', 'shaman'],
                 t('Разбойник: очень высокий урон, скрытность и контроль. Воин: ветки Оружие и Неистовство. Шаман: Совершенствование.',
                   'Rogue: very high damage, stealth and control. Warrior: the Arms and Fury trees. Shaman: Enhancement.',
                   'Розбійник: дуже висока шкода, скритність і контроль. Воїн: гілки Зброя і Лють. Шаман: Вдосконалення.')),
                (t('Урон издалека', 'Ranged damage', 'Шкода здалеку'), ['mage', 'warlock', 'hunter', 'priest'],
                 t('Маг: порталы и еда для всех. Чернокнижник: урон со временем. Жрец: ветка Темная магия.',
                   'Mage: portals and food for everyone. Warlock: damage over time. Priest: the Shadow tree.',
                   'Маг: портали та їжа для всіх. Чорнокнижник: шкода з часом. Жрець: гілка Темрява.')),
                (t('Все роли на одном персонаже', 'Every role on one character', 'Усі ролі на одному персонажі'), ['paladin', 'druid'],
                 t('Танк, лекарь и урон в одном классе.', 'Tank, healer and damage in one class.', 'Танк, лікар і шкода в одному класі.')),
            ]}),
            ('tip', t('Сначала класс, потом раса: раса даёт четыре способности, но не меняет роль. Строка таблицы ниже открывает страницу класса с подходящими расами.',
                      'Class first, race second: a race gives four abilities but does not change your role. A row of the table below opens the class page with the races that suit it.',
                      'Спершу клас, потім раса: раса дає чотири здібності, але не змінює роль. Рядок таблиці нижче відкриває сторінку класу з расами, що йому пасують.')),
        ]},
        {'id': 'pace', 'title': t('Темп прокачки', 'Leveling pace', 'Темп прокачки'), 'blocks': [
            ('text', [t('Прогноз по бете: в бете был потолок 30 уровня, выше оценки проектные. Разница между самым быстрым и самым медленным классом — около 20% времени до 60.',
                        'A beta projection: the beta was capped at level 30, figures above that are estimates. The gap between the fastest and slowest class is about 20% of the time to 60.',
                        'Прогноз за бетою: у беті була стеля 30 рівня, вище оцінки проєктні. Різниця між найшвидшим і найповільнішим класом — близько 20% часу до 60.')]),
            ('picks', {'head': [t('Темп', 'Pace', 'Темп'), t('Классы', 'Classes', 'Класи')], 'rows': [
                (t('Быстрее среднего, около 8%', 'Faster than average, about 8%', 'Швидше за середній, близько 8%'), ['mage', 'hunter']),
                (t('Средний', 'Average', 'Середній'), ['paladin', 'rogue', 'shaman', 'warlock']),
                (t('Медленнее среднего, около 5%', 'Slower than average, about 5%', 'Повільніше за середній, близько 5%'), ['priest', 'druid']),
                (t('Медленнее всех, около 12%', 'Slowest, about 12%', 'Найповільніше, близько 12%'), ['warrior']),
            ]}),
        ]},
        {'id': 'compare', 'title': t('Сравнение', 'Comparison', 'Порівняння'), 'blocks': [
         ('text', [t('Темп прокачки взят из прогнозов по бете: в бете был потолок 30 уровня, выше оценки проектные. Строка открывает страницу класса.',
                     'Leveling pace comes from beta projections: the beta was capped at level 30, figures above that are estimates. A row opens the class page.',
                     'Темп прокачки взято з прогнозів по беті: у беті була стеля 30 рівня, вище оцінки проєктні. Рядок відкриває сторінку класу.')]),
         ('raw', '<div class="cmp cls" id="classRef"></div>'),
     ]}]},
    {'slug': 'races', 'path': 'races/', 'art': 'hero_races', 'hero': 'hero_races', 'js': 'raceref',
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
         ('tip', t('Скайборн доступна обеим фракциям, выбор фракции делается при создании. Обе ветки знают дарнасский, а стартовая зона Zephras Isle общая, враги там не встречаются из-за слоёв.',
                   'Skyborne is playable for both factions; the faction is chosen at creation. Both branches know Darnassian, and the Zephras Isle starting zone is shared, with no enemies meeting there because of layers.',
                   'Скайборн ігрова за обидві фракції, фракцію обирають під час створення. Обидві гілки знають дарнаську, а стартова зона Zephras Isle спільна, вороги там не зустрічаються через шари.')),
     ]}]},
]


# ---------- Служебные страницы: /privacy/ и 404.html. Не гайды: в список гайдов и плитки не попадают ----------
# Политика описывает то, что сайт делает на самом деле. Появится реклама, форма или новый сторонний скрипт — сначала поправить её.

from build import CONTACT  # noqa: E402  (адрес один на весь сайт, подвал берёт его оттуда же)
_mail = f'<a href="mailto:{CONTACT}">{CONTACT}</a>'
_cf = 'https://www.cloudflare.com/privacypolicy/'
_dc = 'https://discord.com/privacy'
_ways = (('Discord', _dc), ('Google', 'https://policies.google.com/privacy'),
         ('Blizzard', 'https://www.blizzard.com/en-us/legal/a4380ee5-5c8d-4e3b-83b7-ea26d01a9918/blizzard-entertainment-online-privacy-policy'),
         ('Telegram', 'https://telegram.org/privacy'), ('Resend', 'https://resend.com/legal/privacy-policy'),
         ('Cloudflare Turnstile', 'https://www.cloudflare.com/turnstile-privacy-policy/'))
_waylinks = ' · '.join(f'<a href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u in _ways)
_lic = ', '.join(f'<a href="{u}" target="_blank" rel="noopener">Creative Commons {n}</a>' for n, u in (
    ('BY 4.0', 'https://creativecommons.org/licenses/by/4.0/'), ('BY 3.0', 'https://creativecommons.org/licenses/by/3.0/'),
    ('CC0', 'https://creativecommons.org/publicdomain/zero/1.0/')))
_gh = 'https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement'

PAGES = [
    {'slug': 'privacy', 'path': 'privacy/', 'og': 'guides', 'art': 'hero_campfire',
     'title': t('Конфиденциальность', 'Privacy', 'Конфіденційність'),
     'lead': t('Какие данные собирает сайт и что хранится у вас в браузере. Коротко: без входа мы о вас ничего не знаем, после входа храним только профиль.',
               'What data the site collects and what is stored in your browser. In short: without signing in we know nothing about you; after signing in we keep only your profile.',
               'Які дані збирає сайт і що зберігається у вашому браузері. Коротко: без входу ми нічого про вас не знаємо, після входу зберігаємо лише профіль.'),
     'pills': [t('Обновлено 24.10.2026', 'Updated 24.10.2026', 'Оновлено 24.10.2026')],
     'sections': [
         {'id': 'short', 'title': t('Коротко', 'In short', 'Коротко'), 'blocks': [
             ('text', [t('Гид читается без входа: тогда сайт не ставит cookies и не знает, кто вы. Вход нужен только для профиля и «Состава». Рекламы и комментариев на сайте нет.',
                         'The guide works without signing in: then the site sets no cookies and does not know who you are. Signing in is only needed for a profile and the Roster. The site has no ads or comments.',
                         'Гід читається без входу: тоді сайт не ставить cookies і не знає, хто ви. Вхід потрібен лише для профілю і «Складу». Реклами й коментарів на сайті немає.')])]},
         {'id': 'account', 'title': t('Профиль', 'Profile', 'Профіль'), 'blocks': [
             ('text', [t('Войти можно через Discord, Google, Battle.net, Telegram или по почте. Пароль мы не получаем, ключи доступа этих сервисов не храним. От каждого способа берём минимум:',
                         'You can sign in with Discord, Google, Battle.net, Telegram or by email. We never receive your password and do not keep these services’ access keys. From each way we take the minimum:',
                         'Увійти можна через Discord, Google, Battle.net, Telegram або поштою. Пароль ми не отримуємо, ключі доступу цих сервісів не зберігаємо. Від кожного способу беремо мінімум:')]),
             ('list', [t('Discord — ID и ник. Участникам сервера Gabella Team — ещё дату вступления: от неё значок команды и достижения за стаж.',
                         'Discord: ID and nickname. For members of the Gabella Team server, also the date they joined: it gives the team mark and the achievements for time on the server.',
                         'Discord — ID і нік. Учасникам сервера Gabella Team — ще дату вступу: від неї значок команди й досягнення за стаж.'),
                       t('Google — только номер аккаунта. Почту и имя не запрашиваем.',
                         'Google: only the account number. We ask for neither your email nor your name.',
                         'Google — лише номер акаунта. Пошту й ім’я не запитуємо.'),
                       t('Battle.net — номер аккаунта и BattleTag.',
                         'Battle.net: account number and BattleTag.',
                         'Battle.net — номер акаунта й BattleTag.'),
                       t('Telegram — ID и @username, если он есть. Имя не храним.',
                         'Telegram: ID and @username, if you have one. We do not keep your name.',
                         'Telegram — ID та @username, якщо він є. Ім’я не зберігаємо.'),
                       t('Почта — только отпечаток адреса, посчитанный с секретным ключом: по нему адрес не восстановить. Сам адрес не храним: письмо со ссылкой входа отправляет сервис Resend. Пока ссылка действует (15 минут), храним маску адреса вида li***@g***.com: её показываем, если ссылку откроют в другом браузере.',
                         'Email: only a fingerprint of the address computed with a secret key: the address cannot be recovered from it. We do not keep the address itself: the sign-in link is sent by the Resend service. While the link is valid (15 minutes) we keep a mask of the address like li***@g***.com and show it if the link is opened in another browser.',
                         'Пошта — лише відбиток адреси, обчислений із секретним ключем: за ним адресу не відновити. Саму адресу не зберігаємо: лист із посиланням для входу надсилає сервіс Resend. Поки посилання діє (15 хвилин), зберігаємо маску адреси на кшталт li***@g***.com: її показуємо, якщо посилання відкриють в іншому браузері.'),
                       t('Если вы подписались на письма — храним адрес (зашифрованным), язык и дату согласия; отписка удаляет их сразу. Письма отправляет Resend.',
                         'If you subscribed to emails, we keep the address (encrypted), the language and the date of consent; unsubscribing deletes them at once. Emails are sent by Resend.',
                         'Якщо ви підписалися на листи — зберігаємо адресу (зашифрованою), мову й дату згоди; відписка видаляє їх одразу. Листи надсилає Resend.')]),
             ('text', [t('Аккаунт один, а входов может быть несколько: привязать и отвязать их можно в кабинете, раздел «Аккаунт». Сами по себе входы не склеиваются: вход новым способом без привязки создаёт новый аккаунт.',
                         'One account can have several ways to sign in: link and unlink them in your profile, under Account. Ways are never merged on their own: signing in a new way without linking it creates a new account.',
                         'Акаунт один, а входів може бути кілька: прив’язати й відв’язати їх можна в кабінеті, розділ «Акаунт». Самі входи не склеюються: вхід новим способом без прив’язки створює новий акаунт.'),
                       t('Ещё храним то, что вы указали сами: персонажей (имя, раса, класс, роль, уровень, профессии, время игры, облик: пол и фон портрета), рамку профиля, отметку «Ищу группу» и того, кто вас пригласил, если вы пришли по его ссылке.',
                         'We also keep what you entered yourself: your characters (name, race, class, role, level, professions, play time, look: gender and portrait background), your profile frame, the Looking for group mark and who invited you, if you came by their link.',
                         'Також зберігаємо те, що ви вказали самі: персонажів (ім’я, раса, клас, роль, рівень, професії, час гри, вигляд: стать і тло портрета), рамку профілю, позначку «Шукаю групу» і того, хто вас запросив, якщо ви прийшли за його посиланням.'),
                       t('Для достижений сайт ведёт счётчики: какие разделы гида вы открывали, сколько слушали радио, в какие дни заходили. Счётчики идут только после входа.',
                         'For achievements the site keeps counters: which guide sections you opened, how long you listened to the radio, which days you visited. Counters run only after you sign in.',
                         'Для досягнень сайт веде лічильники: які розділи гіда ви відкривали, скільки слухали радіо, в які дні заходили. Лічильники працюють лише після входу.'),
                       t('В списке игроков и на вашей странице всем видны персонажи, достижения и рамка. Ник виден, только если вы включили его показ: у новых профилей он скрыт. Ник берётся у первого способа входа (ник Discord, BattleTag, @username в Telegram) и потом сам не меняется. В ссылке на вашу страницу — внутренний номер профиля вида u_…, он не связан с Discord ID.',
                         'In the player list and on your page everyone can see your characters, achievements and frame. Your nickname is shown only if you turned it on: new profiles keep it hidden. The nickname comes from your first way to sign in (Discord nickname, BattleTag, Telegram @username) and never changes by itself later. The link to your page carries an internal profile number like u_…, unrelated to your Discord ID.',
                         'У списку гравців і на вашій сторінці всім видно персонажів, досягнення й рамку. Нік видно, лише якщо ви ввімкнули його показ: у нових профілів він прихований. Нік береться з першого способу входу (нік Discord, BattleTag, @username у Telegram) і потім сам не змінюється. У посиланні на вашу сторінку — внутрішній номер профілю на кшталт u_…, він не пов’язаний із Discord ID.'),
                       t('После входа сайт ставит cookie — ключ сессии на 30 дней. Её получает только сервер профилей api.gabella.site; в базе лежит не сам ключ, а его хэш. Выход удаляет сессию. На время входа добавляются короткие метки: при входе через Discord, Google или Battle.net — защитная на 10 минут, при входе по почте — «вход начат в этом браузере» на 15 минут.',
                         'After you sign in, the site sets a cookie: a session key for 30 days. Only the profile server api.gabella.site receives it; the database stores a hash of the key, not the key itself. Signing out deletes the session. While you sign in, short marks are added: a protective one for 10 minutes with Discord, Google or Battle.net, and “sign-in started in this browser” for 15 minutes with email.',
                         'Після входу сайт ставить cookie — ключ сесії на 30 днів. Її отримує лише сервер профілів api.gabella.site; у базі лежить не сам ключ, а його хеш. Вихід видаляє сесію. На час входу додаються короткі позначки: під час входу через Discord, Google або Battle.net — захисна на 10 хвилин, під час входу поштою — «вхід почато в цьому браузері» на 15 хвилин.'),
                       t('При входе по почте, создании первого персонажа и подписке на письма сайт загружает проверку «не робот» Cloudflare Turnstile: Cloudflare получает IP-адрес и сведения о браузере, чтобы отличить человека от программы.',
                         'When you sign in by email, create your first character or subscribe to emails, the site loads the Cloudflare Turnstile “not a robot” check: Cloudflare receives your IP address and browser details to tell a person from a program.',
                         'Під час входу поштою, створення першого персонажа та підписки на листи сайт завантажує перевірку «не робот» Cloudflare Turnstile: Cloudflare отримує IP-адресу й відомості про браузер, щоб відрізнити людину від програми.'),
                       t('Против спама и перегрузки сервер до часа помнит число попыток по отпечатку почты и по IP-адресу — писем входа, новых аккаунтов, частых изменений профиля, — потом стирает.',
                         'Against spam and overload the server remembers the number of attempts by email fingerprint and by IP address for up to an hour (sign-in emails, new accounts, frequent profile changes), then erases it.',
                         'Проти спаму й перевантаження сервер до години пам’ятає кількість спроб за відбитком пошти та за IP-адресою — листів входу, нових акаунтів, частих змін профілю, — потім стирає.')]),
             ('raw', t(f'<p>Политики конфиденциальности: {_waylinks}</p>',
                       f'<p>Privacy policies: {_waylinks}</p>',
                       f'<p>Політики конфіденційності: {_waylinks}</p>'))]},
         {'id': 'storage', 'title': t('Где и сколько хранится', 'Where and how long', 'Де й скільки зберігається'), 'blocks': [
             ('text', [t('Профили хранятся в Cloudflare (Workers и база D1): Cloudflare обрабатывает их по нашему поручению. Письма входа отправляет Resend (серверы в Ирландии) — тоже по нашему поручению. Храним, пока вы не удалите профиль. Не продаём и не передаём, кроме уведомления о жалобе в закрытый канал команды в Discord (см. ниже).',
                         'Profiles are stored with Cloudflare (Workers and the D1 database), which processes them on our behalf. Sign-in emails are sent by Resend (servers in Ireland), also on our behalf. We keep profiles until you delete them. We do not sell or share them, except a report notice sent to the team’s private Discord channel (see below).',
                         'Профілі зберігаються в Cloudflare (Workers і база D1): Cloudflare обробляє їх за нашим дорученням. Листи входу надсилає Resend (сервери в Ірландії) — теж за нашим дорученням. Зберігаємо, доки ви не видалите профіль. Не продаємо й не передаємо, окрім сповіщення про скаргу в закритий канал команди в Discord (див. нижче).'),
                       t('Администратор может скрыть персонажа, нарушающего правила, и закрыть вход аккаунту за спам или оскорбления.',
                         'An administrator can hide a character that breaks the rules and close sign-in for an account that spams or insults people.',
                         'Адміністратор може приховати персонажа, що порушує правила, і закрити вхід акаунту за спам чи образи.'),
                       t('Если вы пожаловались на игрока, мы храним, кто пожаловался, на кого, на что, причину и пояснение, если вы его написали. Запись остаётся со статусом решения и удаляется вместе с профилем любой из сторон. В закрытый канал команды в Discord уходит уведомление: что не так, причина и ссылка на игрока, без имени автора жалобы. Игрок не видит, кто пожаловался.',
                         'If you report a player, we keep who reported, whom, what about, the reason and the note, if you wrote one. The record stays with the decision status and is deleted together with the profile of either side. A notice goes to the team’s private Discord channel: what is wrong, the reason and a link to the player, without the reporter’s name. The player does not see who reported.',
                         'Якщо ви поскаржилися на гравця, ми зберігаємо, хто поскаржився, на кого, на що, причину й пояснення, якщо ви його написали. Запис лишається зі статусом рішення й видаляється разом із профілем будь-якої зі сторін. У закритий канал команди в Discord надходить сповіщення: що не так, причина й посилання на гравця, без імені автора скарги. Гравець не бачить, хто поскаржився.')])]},
         {'id': 'delete', 'title': t('Скачать и удалить', 'Download and delete', 'Завантажити й видалити'), 'blocks': [
             ('text', [t('В кабинете «Мой профиль», раздел «Аккаунт», можно скачать всё, что мы о вас храним, одним файлом — вместе со способами входа и сроками сессий — и удалить профиль. Вместе с ним сразу удаляются персонажи, достижения, счётчики, записи в ленте и сессии. Восстановить профиль нельзя.',
                         'In My profile, under Account, you can download everything we keep about you as one file, including your ways to sign in and session end dates, and delete your profile. Your characters, achievements, counters, feed entries and sessions are deleted with it at once. A deleted profile cannot be restored.',
                         'У кабінеті «Мій профіль», розділ «Акаунт», можна завантажити все, що ми про вас зберігаємо, одним файлом — разом зі способами входу й строками сесій — і видалити профіль. Разом із ним одразу видаляються персонажі, досягнення, лічильники, записи в стрічці й сесії. Відновити профіль не можна.')])]},
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
             ('text', [t('В памяти браузера (localStorage) сайт запоминает выбранную тему, вашего персонажа — расу, класс, уровень и профессии, если вы их указали, — и настройки радио: станцию, трек, очередь треков, громкость, таймер сна и звуки вокруг, а на странице «В игре» — ваши таймеры, фракцию и выбранного персонажа. Чтобы гид открывался без сети, браузер хранит копии страниц. После входа добавляются отметка о входе и выключатель звука достижений, а копия профиля для быстрой загрузки лежит в памяти вкладки (sessionStorage) и стирается с её закрытием. Ещё сайт помнит выбранный язык, кто вас пригласил, если вы пришли по ссылке, страницу, на которую вернуться после входа, и время начала входа через Telegram.',
                         'In browser storage (localStorage) the site remembers your chosen theme, your hero (race, class, level and professions) if you entered them, and the radio settings: station, track, the queue of tracks, volume, sleep timer and ambient sounds, and on the In game page your timers, faction and chosen character. To open the guide offline, the browser keeps copies of the pages. After you sign in, it also keeps a signed-in mark and the achievement sound switch, while a copy of your profile for faster loading lives in the tab’s memory (sessionStorage) and is erased when you close it. The site also remembers your chosen language, who invited you if you came by their link, the page to return to after signing in, and when a Telegram sign-in was started.',
                         'У пам’яті браузера (localStorage) сайт запам’ятовує вибрану тему, вашого героя — расу, клас, рівень і професії, якщо ви їх вказали, — і налаштування радіо: станцію, трек, чергу треків, гучність, таймер сну і звуки довкола, а на сторінці «У грі» — ваші таймери, фракцію та вибраного персонажа. Щоб гід відкривався без мережі, браузер зберігає копії сторінок. Після входу додаються позначка входу й вимикач звуку досягнень, а копія профілю для швидкого завантаження лежить у пам’яті вкладки (sessionStorage) і стирається з її закриттям. Ще сайт пам’ятає вибрану мову, хто вас запросив, якщо ви прийшли за посиланням, сторінку, на яку повернутися після входу, і час початку входу через Telegram.'),
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
             ('text', [t('С вопросами о данных, ошибками в гайде и претензиями правообладателей пишите на почту ниже. Если не можете войти, профиль удалим по письму: укажите имя основного персонажа и способ входа.',
                         'For questions about data, mistakes in the guide or copyright concerns, write to the address below. If you cannot sign in, we will delete your profile on request: include your main character’s name and how you signed in.',
                         'З питаннями про дані, помилками в гіді та претензіями правовласників пишіть на пошту нижче. Якщо не можете увійти, профіль видалимо за листом: вкажіть ім’я основного персонажа і спосіб входу.')]),
             ('raw', f'<p>{_mail}</p>'),
             ('text', [t('Если что-то изменится, например появится реклама, мы обновим эту страницу и дату вверху.',
                         'If anything changes, for example if ads appear, we will update this page and the date at the top.',
                         'Якщо щось зміниться, наприклад з’явиться реклама, ми оновимо цю сторінку й дату вгорі.')])]},
     ]},
]

from langs import AUTONYM, HREFLANG, LANGS  # noqa: E402

# 404.html в корне гида: GitHub Pages отдаёт её на любой несуществующий адрес под /wow/. Одна страница на все языки.
NOT_FOUND = {
    'slug': '404', 'path': '', 'og': 'guides', 'art': 'hero_campfire', 'more': False,
    'title': t('Страница не найдена', 'Page not found', 'Сторінку не знайдено'),
    'lead': t('Такой страницы нет: ссылка устарела или в адресе опечатка. Разделы гида ниже.',
              'This page does not exist: the link is outdated or the address has a typo. The guide sections are below.',
              'Такої сторінки немає: посилання застаріло або в адресі помилка. Розділи гіда нижче.'),
    'sections': [{'id': 'where', 'title': t('Куда дальше', 'Where next', 'Куди далі'), 'blocks': [
        ('raw', '<p class="nf-langs">' + '<span aria-hidden="true"> · </span>'.join(   # the guide home in every language
            f'<a href="/wow/{"" if l == "ru" else l + "/"}" lang="{HREFLANG[l]}">{AUTONYM[l]}</a>' for l in LANGS) + '</p>'),
    ]}],
}

# ---------- /play/ «В игре»: второй экран на время игры. Сборка — build_guides.play_body + JS['play'] ----------
# Маршрут по зонам и совет про отдых страница берёт из гайда «Прокачка» (секции route и pace), тут только подписи и рубежи.
PLAY = {
    'slug': 'play', 'path': 'play/', 'og': 'guides', 'art': 'hero_campfire', 'compact': True, 'more': False, 'js': 'play',
    'title': t('В игре', 'In game', 'У грі'),
    'lead': t('Второй экран на время игры: радио, зоны и подземелья под ваш уровень, таймеры. После входа — персонажи из профиля.',
              'A second screen while you play: radio, zones and dungeons for your level, timers. After you log in: characters from your profile.',
              'Другий екран під час гри: радіо, зони й підземелля під ваш рівень, таймери. Після входу — персонажі з профілю.'),
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
    'guest': t('Войдите — уровень и персонажи сохранятся в профиле.',
               'Log in to keep your level and characters in your profile.',
               'Увійдіть — рівень і персонажі збережуться в профілі.'),
    'login': t('Войти', 'Log in', 'Увійти'),
    'profile': t('Профиль', 'Profile', 'Профіль'),
    'chars': t('Персонажи', 'Characters', 'Персонажі'),
    'addChar': t('Добавить персонажа', 'Add a character', 'Додати персонажа'),
}
PAGES.append(PLAY)


# ---------- Гайды прокачки по классам: девять страниц, раздел «Прокачка по классам» в гайде прокачки, плитка хаба (content/class_guides.py) ----------

from content import class_guides  # noqa: E402

class_guides.attach(GUIDES, HUBS, ORDER)
CLASS_HUB_TILE = class_guides.HUB_TILE   # на хабе гайдов вместо девяти плиток: одна, ведёт на раздел «Прокачка по классам»
