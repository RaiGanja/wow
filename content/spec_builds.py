"""Гайды «Билды <класса>»: страницы guides/builds-<класс>/, у каждого спека свой раздел с якорем (#protection, #fury…).
Строка = t(ru, en, uk); de, es, fr, it, pl, pt берутся из i18n/<lang>.json по английской строке (как в class_guides.py).
Названия: ru — как в клиенте ruRU (i18n/names.json, Wowhead ruRU), новые таланты Forever без ruRU — английские
(список: docs/wow/specs/texts-2026-10-25-spec-builds/names-todo.md); en/uk/pl — английские.
Правило текста: бета закрыта на 30 уровне, поэтому в таблицах только таланты и очки, в которых сходятся
Icy Veins и Wowhead (их билды 30 уровня, сверены по калькуляторам 25.10). Где они расходятся — это сказано словами,
без очков; если оба берут талант с разным числом очков, в таблице меньшее, а большее названо в тексте.
Раскладку на 51 очко к 60 дадим после старта 05.11.
Источник текстов: docs/wow/specs/texts-2026-10-25-spec-builds (не в репо). attach() подключает страницы к GUIDES,
раздел «Билды по классам» в тир-листе, ссылки из тир-листа на разделы спеков и плитку хаба."""
from content.class_guides import t, tx, bt

SPEC_BUILDS = []

BETA = tx('По бете', 'Beta data', 'За бетою', de='Betadaten', fr='Données de la bêta', pt='Dados da beta')
SPECS3 = t('3 спека', '3 specs', '3 спеціалізації')
LATER = t('Обновим после 05.11', 'Updated after Nov 4–5', 'Оновимо після 5 листопада')
H_TAL = [t('Талант', 'Talent', 'Талант'), t('Очки', 'Points', 'Очки'),
         tx('Зачем', 'Why', 'Навіщо', de='Wozu', es='Para qué', it='A cosa serve', pl='Po co', pt='Para quê')]
H_ROLES = [tx('Спек', 'Spec', 'Спек', de='Skillung', es='Espec.', fr='Spé', it='Spec.', pl='Spec', pt='Espec.'),
           t('Роль', 'Role', 'Роль'), t('Тир PvE', 'PvE tier', 'Тір PvE'), t('Главное', 'Key point', 'Головне')]
TANK, HEALER, DPS = t('Танк', 'Tank', 'Танк'), t('Лекарь', 'Healer', 'Цілитель'), t('Урон', 'Damage', 'Шкода')
FAQ_T = t('Вопросы', 'Questions', 'Питання')
WHEN_Q = t('Когда будет полный билд на 60?', 'When will the full level 60 build be out?', 'Коли буде повний білд на 60?')
WHEN_A = t('После старта 5 ноября: на бете был открыт только 30 уровень, рейды откроются 09.12. Тогда добавим раскладку на все 51 очко.',
           'After the Nov 4–5 launch: the beta only went up to level 30, and raids open on Dec 9. Then we will add the layout for all 51 points.',
           'Після старту 5 листопада: у беті був відкритий лише 30 рівень, рейди відкриються 9 грудня. Тоді додамо розкладку на всі 51 очко.')
ROLES_NOTE = t('Тиры — из тир-листа беты. В таблицах талантов только то, в чём сходятся Icy Veins и Wowhead; у каждого спека сказано, где они расходятся.',
               'Tiers come from the beta tier list. The talent tables show only what Icy Veins and Wowhead agree on; each spec says where they differ.',
               'Тіри — з тір-листа бети. У таблицях талантів лише те, у чому сходяться Icy Veins і Wowhead; для кожної спеціалізації сказано, де вони розходяться.')

BUILDS_TITLE = tx('Билды по классам', 'Builds by class', 'Білди за класами',
                  de='Builds nach Klasse', es='Builds por clase', fr='Builds par classe',
                  it='Build per classe', pl='Buildy według klas', pt='Builds por classe')
BUILDS_LEAD = tx('Таланты, приоритет и характеристики спеков всех девяти классов. Порядок на уровни 31–60 добавим после старта, по данным игры.',
                 'Talents, priorities and stats for every spec of all nine classes. The order for levels 31–60 will follow after launch, from the game’s data.',
                 'Таланти, пріоритет і характеристики спеціалізацій усіх дев’яти класів. Порядок для рівнів 31–60 додамо після старту, за даними гри.',
                 de='Talente, Prioritäten und Werte für jede Skillung aller neun Klassen. Die Reihenfolge für die Stufen 31–60 folgt nach dem Start, aus den Spieldaten.',
                 es='Talentos, prioridades y atributos de cada especialización de las nueve clases. El orden de los niveles 31–60 llegará tras el lanzamiento, con los datos del juego.',
                 fr='Talents, priorités et caractéristiques de chaque spécialisation des neuf classes. L’ordre des niveaux 31–60 suivra après la sortie, d’après les données du jeu.',
                 it='Talenti, priorità e statistiche di ogni specializzazione delle nove classi. L’ordine per i livelli 31–60 arriverà dopo l’uscita, dai dati del gioco.',
                 pl='Talenty, priorytety i statystyki każdej specjalizacji wszystkich dziewięciu klas. Kolejność na levele 31–60 dodamy po starcie, na podstawie danych gry.',
                 pt='Talentos, prioridades e atributos de cada especialização das nove classes. A ordem dos níveis 31–60 virá após o lançamento, com os dados do jogo.')
BUILDS_TILE = tx('Таланты и приоритет спеков к 60', 'Spec talents and priorities for 60', 'Таланти й пріоритет спеціалізацій до 60',
                 de='Talente und Prioritäten der Skillungen für 60', es='Talentos y prioridades de especialización para 60',
                 fr='Talents et priorités des spécialisations pour le 60', it='Talenti e priorità delle specializzazioni per il 60',
                 pl='Talenty i priorytety specjalizacji na 60', pt='Talentos e prioridades das especializações para o 60')
HUB_TILE = {'t': BUILDS_TITLE, 'd': BUILDS_TILE, 'href': 'guides/tier-list/#builds', 'art': 'paladin'}   # the hub has warrior (leveling by class)


def _related(cid, labels):
    """End-of-page tiles: the class page, the class leveling guide, the best race (anchor of the class), the tier list. 'd' is filled by attach()."""
    return [{'t': labels[0], 'd': None, 'href': f'classes/{cid}/', 'art': cid},
            {'t': labels[1], 'd': None, 'href': f'guides/leveling-{cid}/', 'art': 'hero_dawn'},   # hero_leveling is this page's own hero
            {'t': t('Лучшая раса', 'Best race', 'Найкраща раса'), 'd': None, 'href': f'guides/best-race/#{cid}', 'art': 'hero_bestrace'},
            {'t': t('Тир-лист', 'Tier list', 'Тір-лист'), 'd': None, 'href': 'guides/tier-list/', 'art': 'hero_tierlist'}]


# ---------- paladin ----------

SPEC_BUILDS.append({
    'slug': 'builds-paladin', 'art': 'paladin', 'hero': 'hero_leveling', 'hub': False,
    'title': t('Билды Паладина', 'Paladin Builds', 'Білди Паладина'),
    'lead': t('Таланты, приоритет и характеристики Защиты, Света и Воздаяния. Здесь только то, в чём сходятся Icy Veins и Wowhead.',
              'Talents, priorities and stats for Protection, Holy and Retribution. This page shows only what Icy Veins and Wowhead agree on.',
              'Таланти, пріоритет і характеристики Захисту, Світла й Відплати. Тут лише те, у чому сходяться Icy Veins і Wowhead.'),
    'tile': t('Защита, Свет, Воздаяние: таланты и приоритет', 'Protection, Holy, Retribution: talents and priorities', 'Захист, Світло, Відплата: таланти й пріоритет'),
    'pills': [BETA, SPECS3, LATER],
    'sources': [
        ('Icy Veins: Protection Paladin Guide', 'https://www.icy-veins.com/wow-forever/protection-paladin-tank-pve-guide'),
        ('Icy Veins: Holy Paladin Guide', 'https://www.icy-veins.com/wow-forever/holy-paladin-healer-pve-guide'),
        ('Icy Veins: Retribution Paladin Guide', 'https://www.icy-veins.com/wow-forever/retribution-paladin-melee-dps-pve-guide'),
        ('Icy Veins: Paladin Talent Calculator', 'https://www.icy-veins.com/wow-forever/paladin-talent-calculator'),
        ('Wowhead: Level 30 Protection Paladin', 'https://www.wowhead.com/forever/guide/classes/paladin/protection/level-30-tank-overview'),
        ('Wowhead: Level 30 Holy Paladin', 'https://www.wowhead.com/forever/guide/classes/paladin/holy/level-30-healer-overview'),
        ('Wowhead: Level 30 Retribution Paladin', 'https://www.wowhead.com/forever/guide/classes/paladin/retribution/level-30-dps-overview'),
        ('Wowhead: Paladin Talent Calculator', 'https://www.wowhead.com/forever/talent-calc/paladin'),
        ('Mobalytics: Protection Paladin Guide', 'https://mobalytics.gg/wow-forever/classes/protection-paladin-guide'),
    ],
    'sections': [
        {'id': 'roles', 'title': t('Спеки и роли', 'Specs and roles', 'Спеціалізації та ролі'), 'blocks': [
            ('table', {'head': H_ROLES, 'rows': [
                [t('Защита', 'Protection', 'Захист'), TANK, 'S',
                 t('Провокация через Правосудие, Освящение держит угрозу на группе', 'A taunt through Judgement; Consecration holds threat on a group', 'Провокація через Judgement, Consecration тримає загрозу на групі')],
                [t('Свет', 'Holy', 'Світло'), HEALER, 'A',
                 t('Сильное лечение одной цели', 'Strong single-target healing', 'Сильне лікування однієї цілі')],
                [t('Воздаяние', 'Retribution', 'Відплата'), DPS, 'A',
                 t('Двуручное оружие, печати, сила заклинаний', 'Two-handed weapon, seals, spell power', 'Дворучна зброя, печатки, сила заклинань')],
            ]}),
            ('text', [ROLES_NOTE]),
        ]},
        {'id': 'protection', 'title': t('Защита: танк', 'Protection: tank', 'Захист: танк'), 'blocks': [
            ('text', [
                t('Защита — лучший танк беты. Провокацию даёт Правосудие при активной Печати ярости, угрозу на группе держит Освящение: оно у тренера с 20 уровня. Мана возвращается за блоки, поэтому щит обязателен.',
                  'Protection is the best tank of the beta. Judgement with Seal of Fury active is a taunt, and Consecration holds threat on a group: it comes from the trainer at level 20. Mana comes back from blocks, so a shield is a must.',
                  'Захист — найкращий танк бети. Провокацію дає Judgement з активною Seal of Fury, загрозу на групі тримає Consecration: вона в тренера з 20 рівня. Мана повертається за блоки, тож щит обов’язковий.'),
            ]),
            ('table', {'head': H_TAL, 'rows': [
                [t('Оплот (Redoubt)', 'Redoubt', 'Redoubt'), '5', t('Шанс блока после ударов по вам', 'Block chance after you are hit', 'Шанс блоку після ударів по вас')],
                [t('Точность (Precision)', 'Precision', 'Precision'), '3', t('Меткость: промах срывает угрозу', 'Hit: a miss loses threat', 'Влучність: промах зриває загрозу')],
                [t('Специализация на щитах (Shield Specialization)', 'Shield Specialization', 'Shield Specialization'), '3', t('Мана за блок, щит поглощает больше', 'Mana on block; the shield absorbs more', 'Мана за блок, щит поглинає більше')],
                ['Improved Seal of Fury', '1', t('Мана, когда щит Печати ярости поглотил удар целиком', 'Mana when the Seal of Fury shield absorbs a hit in full', 'Мана, коли щит Seal of Fury повністю поглинув удар')],
            ]}),
            ('text', [
                t('Эти таланты берут и Icy Veins, и Wowhead. Дальше они расходятся: Icy Veins добирает Предчувствие (Anticipation) и Holy Conduit в Воздаянии (Освящение дешевле), Wowhead — Специализацию на одноручном оружии и Templar’s Bulwark. Порядок характеристик тоже спорный: Icy Veins ставит первой выносливость, Mobalytics — силу.',
                  'Both Icy Veins and Wowhead take these talents. After that they differ: Icy Veins adds Anticipation and Holy Conduit in Retribution (cheaper Consecration), Wowhead adds One-Handed Weapon Specialization and Templar’s Bulwark. The stat order is disputed too: Icy Veins puts Stamina first, Mobalytics puts Strength first.',
                  'Ці таланти беруть і Icy Veins, і Wowhead. Далі вони розходяться: Icy Veins добирає Anticipation і Holy Conduit у Відплаті (дешевша Consecration), Wowhead — One-Handed Weapon Specialization і Templar’s Bulwark. Порядок характеристик теж спірний: Icy Veins ставить першою витривалість, Mobalytics — силу.'),
            ]),
            ('steps', [
                {'t': t('Перед боем', 'Before the pull', 'Перед боєм'),
                 'd': t('Праведное неистовство, аура и Печать ярости.', 'Righteous Fury, an aura and Seal of Fury.', 'Righteous Fury, аура і Seal of Fury.')},
                {'t': t('Одна цель', 'Single target', 'Одна ціль'),
                 'd': t('Правосудие, Священный удар, Освящение, если хватает маны.', 'Judgement, Holy Strike, and Consecration if mana allows.', 'Judgement, Holy Strike, Consecration, якщо вистачає мани.')},
                {'t': t('Группа', 'Group of enemies', 'Група'),
                 'd': t('Сначала Освящение, затем Правосудие и Священный удар.', 'Consecration first, then Judgement and Holy Strike.', 'Спершу Consecration, потім Judgement і Holy Strike.')},
                {'t': t('Нежить и демоны', 'Undead and demons', 'Нежить і демони'),
                 'd': t('Экзорцизм.', 'Exorcism.', 'Exorcism.')},
                {'t': t('Враг ушёл на другого', 'An enemy turns away', 'Ворог пішов на іншого'),
                 'd': t('Правосудие как провокация: держите его готовым.', 'Judgement as a taunt: keep it ready.', 'Judgement як провокація: тримайте її напоготові.')},
            ]),
            ('tip', t('В Forever Правосудие больше не тратит печать. На 30 уровне появляется Templar’s Bulwark: щит на весь запас здоровья на 8 секунд. Освящение в полную силу бьёт только 4 цели: больше врагов — не больше угрозы от силы заклинаний.',
                      'In Forever, Judgement no longer consumes the seal. Templar’s Bulwark arrives at level 30: a shield for your full health for 8 seconds. Consecration hits only 4 targets at full power: more enemies do not add spell power threat.',
                      'У Forever Judgement більше не витрачає печатку. На 30 рівні з’являється Templar’s Bulwark: щит на весь запас здоров’я на 8 секунд. Consecration на повну силу б’є лише 4 цілі: більше ворогів — не більше загрози від сили заклинань.')),
        ]},
        {'id': 'holy', 'title': t('Свет: лекарь', 'Holy: healer', 'Світло: цілитель'), 'blocks': [
            ('text', [
                t('Свет сильнее всего в лечении одной цели. Вспышка Света — быстро и дёшево, Свет небес — долго, дорого и сильно, Шок небес — мгновенно. Лечение по площади, Light’s Vigil, — талант 40 уровня.',
                  'Holy is strongest at single-target healing. Flash of Light is fast and cheap, Holy Light is slow, expensive and strong, Holy Shock is instant. Area healing, Light’s Vigil, is a level 40 talent.',
                  'Світло найсильніше в лікуванні однієї цілі. Flash of Light — швидко й дешево, Holy Light — довго, дорого й сильно, Holy Shock — миттєво. Лікування по площі, Light’s Vigil, — талант 40 рівня.'),
            ]),
            ('table', {'head': H_TAL, 'rows': [
                [t('Божественный интеллект (Divine Intellect)', 'Divine Intellect', 'Divine Intellect'), '5', t('Больше маны', 'More mana', 'Більше мани')],
                [t('Исцеляющий Свет (Healing Light)', 'Healing Light', 'Healing Light'), '3', t('Сильнее Вспышка Света, Свет небес и Шок небес', 'Stronger Flash of Light, Holy Light and Holy Shock', 'Сильніші Flash of Light, Holy Light і Holy Shock')],
                [t('Благоговение (Reverence)', 'Reverence', 'Reverence'), '3', t('Часть восполнения маны идёт во время чтения', 'Part of mana regeneration continues while casting', 'Частина відновлення мани триває під час читання')],
                [t('Свечение (Illumination)', 'Illumination', 'Illumination'), '5', t('Мана за криты лечения', 'Mana from critical heals', 'Мана за крити лікування')],
                ['Voice of Truth', '1', t('6 секунд без немоты и прерываний', '6 seconds immune to silence and interrupts', '6 секунд без німоти й переривань')],
                [t('Шок небес (Holy Shock)', 'Holy Shock', 'Holy Shock'), '1', t('Мгновенное лечение или урон', 'Instant heal or damage', 'Миттєве лікування або шкода')],
            ]}),
            ('text', [
                t('Сходятся Icy Veins и Wowhead. Расходятся только в одном таланте: Icy Veins берёт Spiritual Focus, Wowhead — Improved Seals. С пятью очками перка Legacy Talented оба добавляют Прилив Света (Infusion of Light): криты Вспышки Света и Шока небес ускоряют следующий Свет небес.',
                  'Icy Veins and Wowhead agree. They differ in one slot: Icy Veins takes Spiritual Focus, Wowhead takes Improved Seals. With the five points of the Legacy Talented perk, both add Infusion of Light: Flash of Light and Holy Shock crits speed up the next Holy Light.',
                  'Сходяться Icy Veins і Wowhead. Розходяться лише в одному таланті: Icy Veins бере Spiritual Focus, Wowhead — Improved Seals. З п’ятьма очками перка Legacy Talented обидва додають Infusion of Light: крити Flash of Light і Holy Shock пришвидшують наступне Holy Light.'),
            ]),
            ('steps', [
                {'t': t('Вспышка Света', 'Flash of Light', 'Flash of Light'),
                 'd': t('Основное лечение: быстро и дёшево.', 'Your main heal: fast and cheap.', 'Основне лікування: швидко й дешево.')},
                {'t': t('Свет небес', 'Holy Light', 'Holy Light'),
                 'd': t('Когда урон большой и есть время на долгое чтение.', 'When damage is heavy and there is time for a long cast.', 'Коли шкода велика і є час на довге читання.')},
                {'t': t('Шок небес', 'Holy Shock', 'Holy Shock'),
                 'd': t('В опасный момент или на бегу.', 'In a dangerous moment or on the move.', 'У небезпечний момент або на бігу.')},
                {'t': t('Печать Света', 'Seal of Light', 'Seal of Light'),
                 'd': t('Правосудие с ней накладывает на врага эффект, который понемногу лечит группу. Опираться на него нельзя.', 'Judgement with it puts an effect on the enemy that heals the group a little. Do not rely on it.', 'Judgement з нею накладає на ворога ефект, що потроху лікує групу. Покладатися на нього не можна.')},
            ]),
            ('tip', t('Ищите снаряжение с силой лечения: интеллект даёт только запас маны и крит заклинаний, но не усиливает лечение (Wowhead). Icy Veins ставит силу лечения первой, затем интеллект и дух.',
                      'Look for gear with healing power: Intellect only gives a bigger mana pool and spell crit, it does not make heals stronger (Wowhead). Icy Veins puts healing power first, then Intellect and Spirit.',
                      'Шукайте спорядження з силою лікування: інтелект дає лише запас мани й крит заклинань, але не посилює лікування (Wowhead). Icy Veins ставить силу лікування першою, потім інтелект і дух.')),
        ]},
        {'id': 'retribution', 'title': t('Воздаяние: урон', 'Retribution: damage', 'Відплата: шкода'), 'blocks': [
            ('text', [
                t('Воздаяние бьёт двуручным оружием, а печати, Правосудие, Священный удар и Освящение растут от силы заклинаний. 15.10 спек ослабили, но в тир-листе беты он остался в A.',
                  'Retribution hits with a two-handed weapon, while seals, Judgement, Holy Strike and Consecration scale with spell power. The spec was nerfed on Oct 15 but stayed in tier A on the beta tier list.',
                  'Відплата б’є дворучною зброєю, а печатки, Judgement, Holy Strike і Consecration ростуть від сили заклинань. 15 жовтня спеціалізацію послабили, але в тір-листі бети вона лишилася в A.'),
            ]),
            ('table', {'head': H_TAL, 'rows': [
                [t('Благодарение (Benediction)', 'Benediction', 'Benediction'), '5', t('Мгновенные заклинания дешевле', 'Cheaper instant spells', 'Дешевші миттєві заклинання')],
                [t('Улучшенное правосудие (Improved Judgement)', 'Improved Judgement', 'Improved Judgement'), '2', t('Правосудие чаще', 'Judgement more often', 'Judgement частіше')],
                ['Holy Conduit', '2', t('Освящение и Экзорцизм дешевле', 'Cheaper Consecration and Exorcism', 'Дешевші Consecration і Exorcism')],
                [t('Приговор (Conviction)', 'Conviction', 'Conviction'), '4', t('Крит в ближнем бою', 'Melee crit', 'Крит у ближньому бою')],
                [t('Освящённое правосудие (Sanctified Judgement)', 'Sanctified Judgement', 'Sanctified Judgement'), '3', t('Правосудие возвращает часть маны печати', 'Judgement returns part of the seal’s mana', 'Judgement повертає частину мани печатки')],
                [t('Печать повиновения (Seal of Command)', 'Seal of Command', 'Seal of Command'), '1', t('Печать для медленного двуручного оружия', 'The seal for a slow two-hander', 'Печатка для повільної дворучної зброї')],
                [t('Погоня за справедливостью (Pursuit of Justice)', 'Pursuit of Justice', 'Pursuit of Justice'), '2', t('+15% к скорости бега: другой у паладина нет', '+15% movement speed: the Paladin has no other', '+15% до швидкості бігу: іншої в паладина немає')],
                ['Sacred Arbiter', '1', t('Священный удар сильнее и обновляет Правосудие на цели', 'Holy Strike hits harder and refreshes Judgement on the target', 'Holy Strike сильніший і оновлює Judgement на цілі')],
            ]}),
            ('text', [
                t('Здесь Icy Veins и Wowhead совпадают почти полностью. Остальные 6 очков из 26 (21 на 30 уровне и 5 от перка Legacy Talented) оба кладут так: Отмщение (Vengeance) 3 и одно очко Воитель Света (Champion of the Light) — часть интеллекта идёт в силу заклинаний. Последнее очко расходится: Icy Veins берёт Repentance, Wowhead — второе очко Специализации на двуручном оружии; первое берут оба. Завершающий талант ветки — Изгиб Света (Twist of Light): после смены печати следующий удар ещё раз применяет старую.',
                  'Here Icy Veins and Wowhead match almost fully. Both spend the other 6 of their 26 points (21 at level 30 plus 5 from the Legacy Talented perk) like this: Vengeance 3 and one point in Champion of the Light, which turns part of your Intellect into spell power. The last point differs: Icy Veins takes Repentance, Wowhead a second point in Two-Handed Weapon Specialization; both take the first. The last talent of the tree is Twist of Light: after you switch seals, your next hit applies the old one once more.',
                  'Тут Icy Veins і Wowhead збігаються майже повністю. Решту 6 очок із 26 (21 на 30 рівні та 5 від перка Legacy Talented) обидва кладуть так: Vengeance 3 і одне очко Champion of the Light — частина інтелекту йде в силу заклинань. Останнє очко розходиться: Icy Veins бере Repentance, Wowhead — друге очко Two-Handed Weapon Specialization; перше беруть обидва. Останній талант гілки — Twist of Light: після зміни печатки наступний удар ще раз застосовує стару.'),
            ]),
            ('steps', [
                {'t': t('Печать', 'Seal', 'Печатка'),
                 'd': t('Всегда активна: Печать повиновения с медленным оружием без эффектов при ударе, Печать праведности с быстрым оружием и большой силой заклинаний.', 'Always active: Seal of Command with a slow weapon without on-hit effects, Seal of Righteousness with a fast weapon and a lot of spell power.', 'Завжди активна: Seal of Command з повільною зброєю без ефектів при ударі, Seal of Righteousness зі швидкою зброєю та великою силою заклинань.')},
                {'t': t('Долгая цель', 'A long fight', 'Довга ціль'),
                 'd': t('Печать воина Света и Правосудие ради ослабления, затем обратно к печати урона.', 'Seal of the Crusader and Judgement for the debuff, then back to your damage seal.', 'Seal of the Crusader і Judgement заради ослаблення, потім назад до печатки шкоди.')},
                {'t': t('Правосудие и Священный удар', 'Judgement and Holy Strike', 'Judgement і Holy Strike'),
                 'd': t('По откату. С Печатью повиновения Правосудие по оглушённой цели бьёт сильнее: сначала Молот правосудия.', 'On cooldown. With Seal of Command, Judgement hits harder on a stunned target: Hammer of Justice first.', 'По відкату. З Seal of Command Judgement по оглушеній цілі б’є сильніше: спершу Hammer of Justice.')},
                {'t': t('Группа', 'Group of enemies', 'Група'),
                 'd': t('Освящение. По одной цели оно не стоит маны.', 'Consecration. Against a single target it is not worth the mana.', 'Consecration. По одній цілі вона не варта мани.')},
                {'t': t('Нежить и демоны', 'Undead and demons', 'Нежить і демони'),
                 'd': t('Экзорцизм.', 'Exorcism.', 'Exorcism.')},
            ]),
            ('tip', t('Характеристики по Icy Veins: урон оружия первым, затем меткость и крит. С 20 уровня полезна сила заклинаний: на ней растут почти все способности.',
                      'Stats according to Icy Veins: weapon damage first, then hit and crit. From level 20, spell power pays off: almost all abilities scale with it.',
                      'Характеристики за Icy Veins: шкода зброї першою, потім влучність і крит. З 20 рівня корисна сила заклинань: від неї ростуть майже всі здібності.')),
        ]},
        {'id': 'faq', 'title': FAQ_T, 'blocks': [
            ('faq', [
                {'id': 'q1', 'q': t('Может ли паладин танковать в WoW Forever?', 'Can a Paladin tank in WoW Forever?', 'Чи може паладин танкувати у WoW Forever?'),
                 'a': [t('Да. Правосудие с Печатью ярости — провокация, Освящение держит угрозу на группе. В тир-листе беты Защита — лучший танк.', 'Yes. Judgement with Seal of Fury is a taunt, and Consecration holds threat on a group. On the beta tier list Protection is the best tank.', 'Так. Judgement з Seal of Fury — провокація, Consecration тримає загрозу на групі. У тір-листі бети Захист — найкращий танк.')]},
                {'id': 'q2', 'q': t('Какую печать брать Воздаянию?', 'Which seal should Retribution use?', 'Яку печатку брати Відплаті?'),
                 'a': [t('Печать повиновения — с медленным двуручным оружием без эффектов при ударе, Печать праведности — с быстрым оружием и большой силой заклинаний. Так советуют и Icy Veins, и Wowhead.', 'Seal of Command with a slow two-hander without on-hit effects, Seal of Righteousness with a fast weapon and a lot of spell power. Both Icy Veins and Wowhead say so.', 'Seal of Command — з повільною дворучною зброєю без ефектів при ударі, Seal of Righteousness — зі швидкою зброєю та великою силою заклинань. Так радять і Icy Veins, і Wowhead.')]},
                {'id': 'q3', 'q': t('Какие расы могут быть паладином?', 'Which races can be a Paladin?', 'Які раси можуть бути паладином?'),
                 'a': [t('В Орде — только нежить, в Альянсе — человек и дворф.', 'In the Horde only Undead; in the Alliance, Human and Dwarf.', 'В Орді — лише нежить, в Альянсі — людина й дворф.')]},
                {'id': 'q4', 'q': WHEN_Q, 'a': [WHEN_A]},
            ]),
        ]},
        {'id': 'related', 'title': t('Смотрите также', 'See also', 'Дивіться також'), 'blocks': [
            ('tiles', _related('paladin', [t('Паладин', 'Paladin', 'Паладин'), t('Прокачка Паладина', 'Paladin leveling', 'Прокачування Паладина')])),
        ]},
    ],
})

# ---------- warrior ----------

SPEC_BUILDS.append({
    'slug': 'builds-warrior', 'art': 'warrior', 'hero': 'hero_leveling', 'hub': False,
    'title': t('Билды Воина', 'Warrior Builds', 'Білди Воїна'),
    'lead': t('Таланты, приоритет и характеристики Защиты, Неистовства и Оружия. Здесь только то, в чём сходятся Icy Veins и Wowhead.',
              'Talents, priorities and stats for Protection, Fury and Arms. This page shows only what Icy Veins and Wowhead agree on.',
              'Таланти, пріоритет і характеристики Захисту, Люті та Зброї. Тут лише те, у чому сходяться Icy Veins і Wowhead.'),
    'tile': t('Защита, Неистовство, Оружие: таланты и приоритет', 'Protection, Fury, Arms: talents and priorities', 'Захист, Лють, Зброя: таланти й пріоритет'),
    'pills': [BETA, SPECS3, LATER],
    'sources': [
        ('Icy Veins: Protection Warrior Guide', 'https://www.icy-veins.com/wow-forever/protection-warrior-tank-pve-guide'),
        ('Icy Veins: Fury Warrior Guide', 'https://www.icy-veins.com/wow-forever/fury-warrior-melee-dps-pve-guide'),
        ('Icy Veins: Arms Warrior Guide', 'https://www.icy-veins.com/wow-forever/arms-warrior-melee-dps-pve-guide'),
        ('Icy Veins: Warrior Talent Calculator', 'https://www.icy-veins.com/wow-forever/warrior-talent-calculator'),
        ('Wowhead: Level 30 Protection Warrior', 'https://www.wowhead.com/forever/guide/classes/warrior/protection/level-30-tank-overview'),
        ('Wowhead: Level 30 Fury Warrior', 'https://www.wowhead.com/forever/guide/classes/warrior/fury/level-30-dps-overview'),
        ('Wowhead: Level 30 Arms Warrior', 'https://www.wowhead.com/forever/guide/classes/warrior/arms/level-30-dps-overview'),
        ('Wowhead: Warrior Talent Calculator', 'https://www.wowhead.com/forever/talent-calc/warrior'),
        ('Blizzard: Warrior Updates in the Beta Build, Oct 2', 'https://us.forums.blizzard.com/en/wow/t/2369360'),
        ('Warcraft Tavern: Fury Warrior Guide', 'https://www.warcrafttavern.com/forever/guides/fury-warrior/'),
    ],
    'sections': [
        {'id': 'roles', 'title': t('Спеки и роли', 'Specs and roles', 'Спеціалізації та ролі'), 'blocks': [
            ('table', {'head': H_ROLES, 'rows': [
                [t('Защита', 'Protection', 'Захист'), TANK, 'A',
                 t('Ярость за блоки, уклонения и парирования со щитом', 'Rage from blocks, dodges and parries with a shield', 'Лють за блоки, ухилення й парирування зі щитом')],
                [t('Неистовство', 'Fury', 'Лють'), DPS, 'A',
                 t('Два оружия, урон по нескольким целям', 'Two weapons, damage to several targets', 'Дві зброї, шкода по кількох цілях')],
                [t('Оружие', 'Arms', 'Зброя'), DPS, 'B',
                 t('Двуручное оружие; ветка ближе к PvP', 'Two-handed weapon; a more PvP-oriented tree', 'Дворучна зброя; гілка ближча до PvP')],
            ]}),
            ('text', [ROLES_NOTE]),
        ]},
        {'id': 'protection', 'title': t('Защита: танк', 'Protection: tank', 'Захист: танк'), 'blocks': [
            ('text', [
                t('Защита держит угрозу Яростью: таланты дают Ярость за блок, уклонение и парирование со щитом. С Авангардом Рывок работает в оборонительной стойке, и Ярость между боями не пропадает.',
                  'Protection holds threat with Rage: its talents give Rage on blocks, dodges and parries with a shield. With Vanguard, Charge works in Defensive Stance, so you keep your Rage between pulls.',
                  'Захист тримає загрозу Люттю: таланти дають Лють за блок, ухилення й парирування зі щитом. З Vanguard ривок працює в оборонній стійці, і Лють між боями не зникає.'),
            ]),
            ('table', {'head': H_TAL, 'rows': [
                [t('Специализация на щитах (Shield Specialization)', 'Shield Specialization', 'Shield Specialization'), '5', t('Шанс блока и Ярость за блок', 'Block chance and Rage on block', 'Шанс блоку й Лють за блок')],
                [t('Улучшенный реванш (Improved Revenge)', 'Improved Revenge', 'Improved Revenge'), '3', t('+60% к урону Реванша', '+60% Revenge damage', '+60% до шкоди Revenge')],
                [t('Улучшенный удар грома (Improved Thunder Clap)', 'Improved Thunder Clap', 'Improved Thunder Clap'), '3', t('Удар грома дешевле на 6 Ярости', 'Thunder Clap costs 6 less Rage', 'Thunder Clap дешевший на 6 Люті')],
                [t('Мастер защиты (Master of Defense)', 'Master of Defense', 'Master of Defense'), '2', t('5 Ярости за уклонение или парирование со щитом', '5 Rage on a dodge or parry with a shield', '5 Люті за ухилення або парирування зі щитом')],
                [t('Авангард (Vanguard)', 'Vanguard', 'Vanguard'), '1', t('Рывок в оборонительной стойке', 'Charge in Defensive Stance', 'Ривок в оборонній стійці')],
                [t('Улучшенное кровопускание (Improved Rend)', 'Improved Rend', 'Improved Rend'), '3', t('Урон Кровопускания; талант ветки Оружия', 'Rend damage; an Arms tree talent', 'Шкода Rend; талант гілки Зброї')],
                [t('Неукротимость (Defiance)', 'Defiance', 'Defiance'), '3', t('Больше угрозы в оборонительной стойке со щитом', 'More threat in Defensive Stance with a shield', 'Більше загрози в оборонній стійці зі щитом')],
            ]}),
            ('text', [
                t('Сходятся Icy Veins и Wowhead; Неукротимость Icy Veins советует для подземелий. Расходятся: Icy Veins добирает Improved Bloodrage и Безжалостность (Cruelty), Wowhead — Ни шагу назад (Last Stand). Для подземелий на капе оба советуют [[Сосредоточенную ярость|Focused Rage]]: удары дешевле.',
                  'Icy Veins and Wowhead agree; Icy Veins recommends Defiance for dungeons. They differ elsewhere: Icy Veins adds Improved Bloodrage and Cruelty, Wowhead adds Last Stand. For dungeons at the cap, both recommend Focused Rage: cheaper attacks.',
                  'Сходяться Icy Veins і Wowhead; Defiance Icy Veins радить для підземель. Розходяться: Icy Veins добирає Improved Bloodrage і Cruelty, Wowhead — Last Stand. Для підземель на капі обидва радять Focused Rage: дешевші удари.'),
            ]),
            ('steps', [
                {'t': t('Вход', 'Opening', 'Вхід'),
                 'd': t('Рывок и Кровавая ярость; Боевой крик, если вы единственный воин в группе.', 'Charge and Bloodrage; Battle Shout if you are the only Warrior in the group.', 'Charge і Bloodrage; Battle Shout, якщо ви єдиний воїн у групі.')},
                {'t': t('Блок щитом', 'Shield Block', 'Shield Block'),
                 'd': t('По откату.', 'On cooldown.', 'По відкату.')},
                {'t': t('Реванш', 'Revenge', 'Revenge'),
                 'd': t('При каждом срабатывании.', 'Every time it procs.', 'При кожному спрацюванні.')},
                {'t': t('Удар грома и Деморализующий крик', 'Thunder Clap and Demoralizing Shout', 'Thunder Clap і Demoralizing Shout'),
                 'd': t('Держать на врагах.', 'Keep them up on the enemies.', 'Тримати на ворогах.')},
                {'t': t('Раскол брони', 'Sunder Armor', 'Sunder Armor'),
                 'd': t('5 зарядов на боссе.', '5 stacks on a boss.', '5 зарядів на босі.')},
                {'t': t('Удар героя', 'Heroic Strike', 'Heroic Strike'),
                 'd': t('Только при лишней Ярости; на группе — Рассекающий удар.', 'Only with spare Rage; Cleave against a group.', 'Лише за зайвої Люті; на групі — Cleave.')},
            ]),
            ('tip', t('Не меняйте стойку с полной Яростью: смена стойки её сжигает. Казнь требует выйти из оборонительной стойки. Меткость оба источника ставят высоко: промах не даёт ни урона, ни Ярости, ни угрозы.',
                      'Do not switch stances with a full Rage bar: switching burns it. Execute requires leaving Defensive Stance. Both sources rank hit highly: a miss gives no damage, no Rage and no threat.',
                      'Не міняйте стійку з повною Люттю: зміна стійки її спалює. Execute вимагає вийти з оборонної стійки. Влучність обидва джерела ставлять високо: промах не дає ні шкоди, ні Люті, ні загрози.')),
        ]},
        {'id': 'fury', 'title': t('Неистовство: урон', 'Fury: damage', 'Лють: шкода'), 'blocks': [
            ('text', [
                t('Неистовство бьёт двумя оружиями. У второго оружия штраф 19% к меткости: на бете общий шанс промаха доходил до 27% (Icy Veins), поэтому Furious Precision обязателен. Исступление в Forever срабатывает от любого удара по вам, а не только от крита (Wowhead).',
                  'Fury fights with two weapons. The off-hand has a 19% hit penalty: on the beta the total miss chance reached 27% (Icy Veins), so Furious Precision is a must. In Forever, Enrage triggers from any hit you take, not only from crits (Wowhead).',
                  'Лють б’є двома зброями. У другої зброї штраф 19% до влучності: у беті загальний шанс промаху сягав 27% (Icy Veins), тож Furious Precision обов’язковий. Enrage у Forever спрацьовує від будь-якого удару по вас, а не лише від крита (Wowhead).'),
            ]),
            ('table', {'head': H_TAL, 'rows': [
                [t('Безжалостность (Cruelty)', 'Cruelty', 'Cruelty'), '5', t('+5% к криту', '+5% crit', '+5% до криту')],
                [t('Необузданный гнев (Unbridled Wrath)', 'Unbridled Wrath', 'Unbridled Wrath'), '5', t('Шанс получить лишнюю Ярость с удара', 'A chance for extra Rage on hit', 'Шанс отримати зайву Лють з удару')],
                ['Furious Precision', '3', t('+10% меткости второму оружию', '+10% off-hand hit', '+10% влучності другій зброї')],
                [t('Специализация на бое двумя оружиями (Dual Wield Specialization)', 'Dual Wield Specialization', 'Dual Wield Specialization'), '5', t('Урон и Ярость второго оружия', 'Off-hand damage and Rage', 'Шкода й Лють другої зброї')],
                [t('Инстинкт смерти (Death Wish)', 'Death Wish', 'Death Wish'), '1', t('+20% к физическому урону на 30 секунд, но +5% к входящему; откат 3 минуты', '+20% physical damage for 30 seconds, but +5% damage taken; 3-minute cooldown', '+20% до фізичної шкоди на 30 секунд, але +5% до вхідної; відкат 3 хвилини')],
            ]}),
            ('text', [
                t('Сходятся Icy Veins и Wowhead. Расходятся: Icy Veins добирает Пронзительный вой (Piercing Howl) и одно очко Lingering Rage, Wowhead — два очка Lingering Rage. Кровожадность (Bloodthirst) — последний талант ветки, до него дойдут после 40 уровня.',
                  'Icy Veins and Wowhead agree. They differ: Icy Veins adds Piercing Howl and one point in Lingering Rage, Wowhead adds two points in Lingering Rage. Bloodthirst is the last talent of the tree; you reach it after level 40.',
                  'Сходяться Icy Veins і Wowhead. Розходяться: Icy Veins добирає Piercing Howl і одне очко Lingering Rage, Wowhead — два очки Lingering Rage. Bloodthirst — останній талант гілки, до нього дійдуть після 40 рівня.'),
            ]),
            ('steps', [
                {'t': t('Боевой крик', 'Battle Shout', 'Battle Shout'),
                 'd': t('Всегда активен.', 'Always up.', 'Завжди активний.')},
                {'t': t('Инстинкт смерти', 'Death Wish', 'Death Wish'),
                 'd': t('По откату, заранее накопив Ярость.', 'On cooldown, after pooling Rage.', 'По відкату, заздалегідь накопичивши Лють.')},
                {'t': t('Превосходство', 'Overpower', 'Overpower'),
                 'd': t('Когда доступно.', 'Whenever it is available.', 'Коли доступне.')},
                {'t': t('Казнь', 'Execute', 'Execute'),
                 'd': t('По цели с низким здоровьем.', 'On a target with low health.', 'По цілі з низьким здоров’ям.')},
                {'t': t('Удар героя или Рассекающий удар', 'Heroic Strike or Cleave', 'Heroic Strike або Cleave'),
                 'd': t('Тратить лишнюю Ярость.', 'Spend spare Rage.', 'Витрачати зайву Лють.')},
            ]),
            ('tip', t('Improved Cleave из старых гайдов в игре нет: Blizzard убрала его из Неистовства 02.10, в калькуляторах Icy Veins и Wowhead его тоже нет. Меткость и крит Icy Veins и Warcraft Tavern ставят выше силы.',
                      'Improved Cleave from older guides is not in the game: Blizzard removed it from Fury on Oct 2, and it is missing from the Icy Veins and Wowhead calculators too. Icy Veins and Warcraft Tavern rank hit and crit above Strength.',
                      'Improved Cleave зі старих гайдів у грі немає: Blizzard прибрала його з Люті 2 жовтня, у калькуляторах Icy Veins і Wowhead його теж немає. Влучність і крит Icy Veins і Warcraft Tavern ставлять вище за силу.')),
        ]},
        {'id': 'arms', 'title': t('Оружие: урон', 'Arms: damage', 'Зброя: шкода'), 'blocks': [
            ('text', [
                t('Оружие играет от двуручного оружия, Кровопускания и Превосходства. Смертельный удар — последний талант ветки, поэтому до 40 уровня главный расход Ярости — Spearing Strike. В тир-листе беты урон Оружия ниже, чем у Неистовства.',
                  'Arms plays around a two-handed weapon, Rend and Overpower. Mortal Strike is the last talent of the tree, so until level 40 your main Rage spender is Spearing Strike. On the beta tier list Arms deals less damage than Fury.',
                  'Зброя грає від дворучної зброї, Rend і Overpower. Mortal Strike — останній талант гілки, тож до 40 рівня головна витрата Люті — Spearing Strike. У тір-листі бети шкода Зброї нижча, ніж у Люті.'),
            ]),
            ('table', {'head': H_TAL, 'rows': [
                [t('Улучшенное кровопускание (Improved Rend)', 'Improved Rend', 'Improved Rend'), '3', t('Урон Кровопускания', 'Rend damage', 'Шкода Rend')],
                [t('Улучшенное превосходство (Improved Overpower)', 'Improved Overpower', 'Improved Overpower'), '2', t('+50% к шансу крита Превосходства', '+50% Overpower crit chance', '+50% до шансу криту Overpower')],
                ['Improved Tactical Mastery', '5', t('Больше Ярости остаётся при смене стойки; путь к Управлению злостью', 'More Rage kept when switching stances; the path to Anger Management', 'Більше Люті лишається при зміні стійки; шлях до Anger Management')],
                [t('Управление злостью (Anger Management)', 'Anger Management', 'Anger Management'), '1', t('1 Ярость каждые 3 секунды в бою', '1 Rage every 3 seconds in combat', '1 Лють кожні 3 секунди в бою')],
                [t('Глубокие раны (Deep Wounds)', 'Deep Wounds', 'Deep Wounds'), '3', t('Кровотечение после крита', 'A bleed after a crit', 'Кровотеча після криту')],
                ['Spearing Strike', '1', t('Дешёвый удар, сильнее по великанам и драконам', 'A cheap strike, stronger against giants and dragonkin', 'Дешевий удар, сильніший по велетнях і драконах')],
                [t('Специализация на двуручном оружии (Two-Handed Weapon Specialization)', 'Two-Handed Weapon Specialization', 'Two-Handed Weapon Specialization'), '3', t('Урон с двуручным оружием', 'Damage with a two-hander', 'Шкода з дворучною зброєю')],
                [t('Размашистые удары (Sweeping Strikes)', 'Sweeping Strikes', 'Sweeping Strikes'), '1', t('Следующие 5 атак бьют ещё одну цель рядом', 'Your next 5 attacks also hit a nearby target', 'Наступні 5 атак б’ють ще одну ціль поруч')],
            ]}),
            ('text', [
                t('Сходятся Icy Veins и Wowhead. Расходятся: Icy Veins берёт Отражение (Deflection), Wowhead — Improved Heroic Strike и Impale. Очки перка Legacy Talented оба отдают в Кровавый азарт (Bloodthrill): Icy Veins все 5, Wowhead 3, а 2 — в Специализацию на двуручном оружии. Удары по цели с Кровопусканием иногда открывают Превосходство.',
                  'Icy Veins and Wowhead agree. They differ: Icy Veins takes Deflection, Wowhead takes Improved Heroic Strike and Impale. Both spend the Legacy Talented points on Bloodthrill: Icy Veins all 5, Wowhead 3, with 2 into Two-Handed Weapon Specialization. Hits on a target with Rend sometimes enable Overpower.',
                  'Сходяться Icy Veins і Wowhead. Розходяться: Icy Veins бере Deflection, Wowhead — Improved Heroic Strike та Impale. Очки перка Legacy Talented обидва віддають у Bloodthrill: Icy Veins усі 5, Wowhead 3, а 2 — у Two-Handed Weapon Specialization. Удари по цілі з Rend іноді відкривають Overpower.'),
            ]),
            ('steps', [
                {'t': t('Боевой крик', 'Battle Shout', 'Battle Shout'),
                 'd': t('Всегда активен.', 'Always up.', 'Завжди активний.')},
                {'t': t('Кровопускание', 'Rend', 'Rend'),
                 'd': t('Держать на цели.', 'Keep it on the target.', 'Тримати на цілі.')},
                {'t': t('Превосходство', 'Overpower', 'Overpower'),
                 'd': t('Как только доступно.', 'As soon as it is available.', 'Щойно доступне.')},
                {'t': t('Раскол брони', 'Sunder Armor', 'Sunder Armor'),
                 'd': t('До 5 зарядов.', 'Up to 5 stacks.', 'До 5 зарядів.')},
                {'t': 'Spearing Strike',
                 'd': t('Главный расход Ярости до Смертельного удара.', 'Your main Rage spender before Mortal Strike.', 'Головна витрата Люті до Mortal Strike.')},
                {'t': t('Группа', 'Group of enemies', 'Група'),
                 'd': t('Кровопускание на всех, Размашистые удары, когда готово Превосходство; копите Ярость к их откату.', 'Rend on all of them, Sweeping Strikes when Overpower is ready; pool Rage for its cooldown.', 'Rend на всіх, Sweeping Strikes, коли готове Overpower; накопичуйте Лють до їхнього відкату.')},
            ]),
            ('tip', t('Сокрушение (Slam) жмите сразу после своего удара и только когда вас не бьют: иначе долгое чтение сбивается (Wowhead). Spearing Strike и Кровавый азарт — новые таланты Forever.',
                      'Use Slam right after your own swing and only when you are not being hit: otherwise the long cast gets pushed back (Wowhead). Spearing Strike and Bloodthrill are new Forever talents.',
                      'Slam тисніть одразу після свого удару й лише коли вас не б’ють: інакше довге читання збивається (Wowhead). Spearing Strike і Bloodthrill — нові таланти Forever.')),
        ]},
        {'id': 'faq', 'title': FAQ_T, 'blocks': [
            ('faq', [
                {'id': 'q1', 'q': t('Нужен ли воину-танку щит в WoW Forever?', 'Does a tank Warrior need a shield in WoW Forever?', 'Чи потрібен воїну-танку щит у WoW Forever?'),
                 'a': [t('Да. Специализация на щитах и Мастер защиты дают Ярость за блок, уклонение и парирование только со щитом.', 'Yes. Shield Specialization and Master of Defense give Rage on blocks, dodges and parries only with a shield.', 'Так. Shield Specialization і Master of Defense дають Лють за блок, ухилення й парирування лише зі щитом.')]},
                {'id': 'q2', 'q': t('Неистовство или Оружие для подземелий?', 'Fury or Arms for dungeons?', 'Лють чи Зброя для підземель?'),
                 'a': [t('Неистовство: в тир-листе беты оно в A, Оружие — в B.', 'Fury: it is in tier A on the beta tier list, Arms is in B.', 'Лють: у тір-листі бети вона в A, Зброя — в B.')]},
                {'id': 'q3', 'q': t('Есть ли Improved Cleave в Forever?', 'Is Improved Cleave in Forever?', 'Чи є Improved Cleave у Forever?'),
                 'a': [t('Нет. Blizzard убрала его из Неистовства 02.10. Билды, где он есть, устарели.', 'No. Blizzard removed it from Fury on Oct 2. Builds that include it are out of date.', 'Ні. Blizzard прибрала його з Люті 2 жовтня. Білди, де він є, застаріли.')]},
                {'id': 'q4', 'q': WHEN_Q, 'a': [WHEN_A]},
            ]),
        ]},
        {'id': 'related', 'title': t('Смотрите также', 'See also', 'Дивіться також'), 'blocks': [
            ('tiles', _related('warrior', [t('Воин', 'Warrior', 'Воїн'), t('Прокачка Воина', 'Warrior leveling', 'Прокачування Воїна')])),
        ]},
    ],
})

# ---------- mage ----------

SPEC_BUILDS.append({
    'slug': 'builds-mage', 'art': 'mage', 'hero': 'hero_leveling', 'hub': False,
    'title': t('Билды Мага', 'Mage Builds', 'Білди Мага'),
    'lead': t('Таланты, приоритет и характеристики Тайной магии, Огня и Льда. Здесь только то, в чём сходятся Icy Veins и Wowhead.',
              'Talents, priorities and stats for Arcane, Fire and Frost. This page shows only what Icy Veins and Wowhead agree on.',
              'Таланти, пріоритет і характеристики Тайної магії, Вогню та Льоду. Тут лише те, у чому сходяться Icy Veins і Wowhead.'),
    'tile': t('Тайная магия, Огонь, Лёд: таланты и приоритет', 'Arcane, Fire, Frost: talents and priorities', 'Тайна магія, Вогонь, Лід: таланти й пріоритет'),
    'pills': [BETA, SPECS3, LATER],
    'sources': [
        ('Icy Veins: Arcane Mage Guide', 'https://www.icy-veins.com/wow-forever/arcane-mage-ranged-dps-pve-guide'),
        ('Icy Veins: Fire Mage Guide', 'https://www.icy-veins.com/wow-forever/fire-mage-ranged-dps-pve-guide'),
        ('Icy Veins: Frost Mage Guide', 'https://www.icy-veins.com/wow-forever/frost-mage-ranged-dps-pve-guide'),
        ('Icy Veins: Mage Talent Calculator', 'https://www.icy-veins.com/wow-forever/mage-talent-calculator'),
        ('Wowhead: Level 30 Arcane Mage', 'https://www.wowhead.com/forever/guide/classes/mage/arcane/level-30-dps-overview'),
        ('Wowhead: Level 30 Fire Mage', 'https://www.wowhead.com/forever/guide/classes/mage/fire/level-30-dps-overview'),
        ('Wowhead: Level 30 Frost Mage', 'https://www.wowhead.com/forever/guide/classes/mage/frost/level-30-dps-overview'),
        ('Wowhead: Mage Talent Calculator', 'https://www.wowhead.com/forever/talent-calc/mage'),
        ('Warcraft Tavern: Frost Mage Guide', 'https://www.warcrafttavern.com/forever/guides/frost-mage/'),
        ('Noobtoboss: tier list', 'https://noobtoboss.com/wowforever-tierlist/'),
    ],
    'sections': [
        {'id': 'roles', 'title': t('Спеки и роли', 'Specs and roles', 'Спеціалізації та ролі'), 'blocks': [
            ('table', {'head': H_ROLES, 'rows': [
                [t('Тайная магия', 'Arcane', 'Тайна магія'), DPS, 'A',
                 t('Чародейская вспышка и срабатывания, быстро тратит ману', 'Arcane Blast and procs; burns mana fast', 'Arcane Blast і спрацювання, швидко витрачає ману')],
                [t('Огонь', 'Fire', 'Вогонь'), DPS, 'A*',
                 t('Криты ускоряют Огненную глыбу', 'Crits speed up Pyroblast', 'Крити пришвидшують Pyroblast')],
                [t('Лёд', 'Frost', 'Лід'), DPS, 'B',
                 t('Самый живучий, но урон ниже', 'The safest, but lower damage', 'Найживучіший, але шкода нижча')],
            ]}),
            ('text', [ROLES_NOTE, t('A* у Огня: Noobtoboss ставит его в B для подземелий.', 'A* for Fire: Noobtoboss puts it in B for dungeons.', 'A* у Вогню: Noobtoboss ставить його в B для підземель.')]),
        ]},
        {'id': 'arcane', 'title': t('Тайная магия: урон', 'Arcane: damage', 'Тайна магія: шкода'), 'blocks': [
            ('text', [
                t('В Classic у Тайной магии не было своей ротации. В Forever есть Чародейская вспышка: каждое применение добавляет силу заклинаний и делает следующую вспышку намного дороже. Заградительные стрелы дают срабатывание: следующие Чародейские снаряды быстрее и бесплатны.',
                  'In Classic, Arcane had no rotation of its own. In Forever it has Arcane Blast: each cast adds spell power and makes the next Blast much more expensive. Missile Barrage gives a proc: your next Arcane Missiles are faster and free.',
                  'У Classic у Тайної магії не було власної ротації. У Forever є Arcane Blast: кожне застосування додає силу заклинань і робить наступний Blast набагато дорожчим. Missile Barrage дає спрацювання: наступні Arcane Missiles швидші й безкоштовні.'),
            ]),
            ('table', {'head': H_TAL, 'rows': [
                [t('Чародейская вспышка (Arcane Blast)', 'Arcane Blast', 'Arcane Blast'), '1', t('Основное заклинание', 'Your main spell', 'Основне заклинання')],
                [t('Заградительные стрелы (Missile Barrage)', 'Missile Barrage', 'Missile Barrage'), '2', t('Срабатывания для Чародейских снарядов', 'Procs for Arcane Missiles', 'Спрацювання для Arcane Missiles')],
            ]}),
            ('text', [
                t('Остальное Icy Veins и Wowhead собирают по-разному, а встроенный билд в гайде Wowhead не открывается. Общее правило у обоих: Средоточие чар (Arcane Focus) нужно против врагов выше вашего уровня — в подземельях и на боссах; если бьёте только врагов своего уровня, вместо него Improved Channeling. Icy Veins ещё берёт [[Чародейскую сосредоточенность|Arcane Concentration]] 5 и Присутствие разума (Presence of Mind).',
                  'Icy Veins and Wowhead build the rest differently, and the embedded build in the Wowhead guide does not open. The rule both share: Arcane Focus is for enemies above your level, in dungeons and on bosses; if you only fight enemies of your level, take Improved Channeling instead. Icy Veins also takes Arcane Concentration 5 and Presence of Mind.',
                  'Решту Icy Veins і Wowhead збирають по-різному, а вбудований білд у гайді Wowhead не відкривається. Спільне правило в обох: Arcane Focus потрібне проти ворогів вище за ваш рівень — у підземеллях і на босах; якщо б’єте лише ворогів свого рівня, замість нього Improved Channeling. Icy Veins ще бере Arcane Concentration 5 і Presence of Mind.'),
            ]),
            ('steps', [
                {'t': t('Чародейская вспышка', 'Arcane Blast', 'Arcane Blast'),
                 'd': t('2–3 раза подряд. Дольше копить заряды — только на боссе.', '2–3 times in a row. Stack it longer only on a boss.', '2–3 рази поспіль. Довше накопичувати заряди — лише на босі.')},
                {'t': t('Заградительные стрелы', 'Missile Barrage', 'Missile Barrage'),
                 'd': t('Сработали — Чародейские снаряды.', 'When it procs, Arcane Missiles.', 'Спрацювало — Arcane Missiles.')},
                {'t': t('Нет срабатывания', 'Without a proc', 'Немає спрацювання'),
                 'd': t('После 2–3 вспышек — Огненный взрыв: заряды спадут, и мана перестанет утекать.', 'After 2–3 Blasts, Fire Blast: the stacks drop and the mana drain stops.', 'Після 2–3 Blast — Fire Blast: заряди спадуть, і мана перестане витікати.')},
                {'t': t('Группа под танком', 'A pack on the tank', 'Група під танком'),
                 'd': t('Чародейский взрыв; Огненный столб заранее, если хватает маны.', 'Arcane Explosion; Flamestrike first if you have the mana.', 'Arcane Explosion; Flamestrike заздалегідь, якщо вистачає мани.')},
            ]),
            ('tip', tx('Чародейская вспышка, Заградительные стрелы и Arcane Wrath — таланты, которых не было в Classic. Icy Veins пишет, что на 60 меткость станет заметно важнее из-за рейдовых боссов.', 'Arcane Blast, Missile Barrage and Arcane Wrath are talents that Classic did not have. Icy Veins says hit will matter much more at 60 because of raid bosses.', 'Arcane Blast, Missile Barrage і Arcane Wrath — таланти, яких не було в Classic. Icy Veins пише, що на 60 влучність стане помітно важливішою через рейдових босів.', de='Arkanschlag, Geschosssalve und Arcane Wrath sind Talente, die es in Classic nicht gab. Laut Icy Veins wird Treffer auf 60 wegen der Schlachtzugsbosse deutlich wichtiger.', es='Explosión Arcana, Tromba de misiles y Arcane Wrath son talentos que no existían en Classic. Según Icy Veins, el golpe importará mucho más a nivel 60 por los jefes de banda.', fr='Déflagration des arcanes, Barrage de projectiles et Arcane Wrath sont des talents qui n’existaient pas dans Classic. Selon Icy Veins, le toucher comptera beaucoup plus au niveau 60 à cause des boss de raid.', it='Detonazione Arcana, Raffica di Missili e Arcane Wrath sono talenti che in Classic non c’erano. Secondo Icy Veins, al 60 il colpire conterà molto di più per via dei boss delle incursioni.', pl='Arcane Blast, Missile Barrage i Arcane Wrath to talenty, których nie było w Classic. Icy Veins pisze, że na 60 hit stanie się dużo ważniejszy przez bossów raidowych.', pt='Impacto Arcano, Salva de Mísseis e Arcane Wrath são talentos que não existiam no Classic. Segundo Icy Veins, o acerto vai pesar muito mais no nível 60 por causa dos chefes de raide.')),
        ]},
        {'id': 'fire', 'title': t('Огонь: урон', 'Fire: damage', 'Вогонь: шкода'), 'blocks': [
            ('text', [
                t('Огонь живёт критами. Heating Up: криты Огненного шара, Огненного взрыва и Ожога сокращают чтение следующей Огненной глыбы, до трёх зарядов. Воспламенение добавляет урон после крита. Без крита спек проседает.',
                  'Fire lives on crits. Heating Up: crits from Fireball, Fire Blast and Scorch cut the cast time of your next Pyroblast, up to three stacks. Ignite adds damage after a crit. Without crit the spec falls behind.',
                  'Вогонь живе критами. Heating Up: крити Fireball, Fire Blast і Scorch скорочують читання наступного Pyroblast, до трьох зарядів. Ignite додає шкоду після криту. Без криту спеціалізація просідає.'),
            ]),
            ('table', {'head': H_TAL, 'rows': [
                [t('Улучшенный огненный шар (Improved Fireball)', 'Improved Fireball', 'Improved Fireball'), '5', t('Огненный шар читается быстрее', 'Faster Fireball cast', 'Fireball читається швидше')],
                [t('Метание пламени (Flame Throwing)', 'Flame Throwing', 'Flame Throwing'), '2', t('Дальность заклинаний огня', 'Fire spell range', 'Дальність заклинань вогню')],
                [t('Пылающая душа (Burning Soul)', 'Burning Soul', 'Burning Soul'), '3', t('Чтение реже сбивается уроном, меньше угрозы', 'Less cast pushback from damage, less threat', 'Читання рідше збивається шкодою, менше загрози')],
                [t('Огненная глыба (Pyroblast)', 'Pyroblast', 'Pyroblast'), '1', t('Главный удар', 'Your big hit', 'Головний удар')],
                ['Heating Up', '1', t('Заряды от критов ускоряют Огненную глыбу', 'Crit stacks speed up Pyroblast', 'Заряди від критів пришвидшують Pyroblast')],
            ]}),
            ('text', [
                t('Сходятся Icy Veins и Wowhead. Воспламенение (Ignite) берут оба, но с разным числом очков. Улучшенный ожог (Improved Scorch) Wowhead берёт уже на 30, Icy Veins называет его почти обязательным к 60 для PvE. Расходятся: Icy Veins берёт Master of Elements, Wowhead — Critical Mass и Точность стихии (Elemental Precision) из ветки Льда.',
                  'Icy Veins and Wowhead agree. Both take Ignite, but with a different number of points. Wowhead takes Improved Scorch at 30 already, and Icy Veins calls it close to mandatory for PvE at 60. They differ: Icy Veins takes Master of Elements, Wowhead takes Critical Mass and Elemental Precision from the Frost tree.',
                  'Сходяться Icy Veins і Wowhead. Ignite беруть обидва, але з різною кількістю очок. Improved Scorch Wowhead бере вже на 30, Icy Veins називає його майже обов’язковим до 60 для PvE. Розходяться: Icy Veins бере Master of Elements, Wowhead — Critical Mass і Elemental Precision з гілки Льоду.'),
            ]),
            ('steps', [
                {'t': t('Ожог', 'Scorch', 'Scorch'),
                 'd': t('До 5 зарядов Улучшенного ожога на цели с большим запасом здоровья.', 'Up to 5 Improved Scorch stacks on a target with a lot of health.', 'До 5 зарядів Improved Scorch на цілі з великим запасом здоров’я.')},
                {'t': t('Огненный шар', 'Fireball', 'Fireball'),
                 'd': t('Основное заклинание.', 'Your main spell.', 'Основне заклинання.')},
                {'t': t('Огненная глыба', 'Pyroblast', 'Pyroblast'),
                 'd': t('Когда набраны заряды Heating Up.', 'Once Heating Up has stacked.', 'Коли набрано заряди Heating Up.')},
                {'t': t('Огненный взрыв', 'Fire Blast', 'Fire Blast'),
                 'd': t('Добить цель.', 'To finish a target.', 'Добити ціль.')},
                {'t': t('Группа под танком', 'A pack on the tank', 'Група під танком'),
                 'd': t('Огненный столб, затем Взрывная волна, затем Чародейский взрыв.', 'Flamestrike, then Blast Wave, then Arcane Explosion.', 'Flamestrike, потім Blast Wave, потім Arcane Explosion.')},
            ]),
            ('tip', t('Heating Up — новый талант. В тексте гайда Icy Veins он ещё назван Hot Streak, а в калькуляторах Icy Veins и Wowhead — Heating Up. Крит Огню важнее, чем другим спекам мага: от него работают Heating Up и Воспламенение.',
                      'Heating Up is a new talent. The Icy Veins guide text still calls it Hot Streak, while the Icy Veins and Wowhead calculators call it Heating Up. Crit matters more for Fire than for the other Mage specs: Heating Up and Ignite run on it.',
                      'Heating Up — новий талант. У тексті гайда Icy Veins його ще названо Hot Streak, а в калькуляторах Icy Veins і Wowhead — Heating Up. Крит Вогню важливіший, ніж іншим спеціалізаціям мага: від нього працюють Heating Up та Ignite.')),
        ]},
        {'id': 'frost', 'title': t('Лёд: урон', 'Frost: damage', 'Лід: шкода'), 'blocks': [
            ('text', [
                t('Лёд — самый живучий спек мага, но в группе урон ниже, чем у Огня и Тайной магии. Ледяное копье бьёт замороженную цель втрое сильнее, а Ледяные пальцы позволяют бить им как по замороженной.',
                  'Frost is the safest Mage spec, but in a group it deals less damage than Fire and Arcane. Ice Lance hits a frozen target three times as hard, and Fingers of Frost lets you hit as if the target were frozen.',
                  'Лід — найживучіша спеціалізація мага, але в групі шкода нижча, ніж у Вогню й Тайної магії. Ice Lance б’є заморожену ціль утричі сильніше, а Fingers of Frost дозволяє бити ним як по замороженій.'),
            ]),
            ('table', {'head': H_TAL, 'rows': [
                [t('Улучшенная ледяная стрела (Improved Frostbolt)', 'Improved Frostbolt', 'Improved Frostbolt'), '5', t('Ледяная стрела читается быстрее', 'Faster Frostbolt cast', 'Frostbolt читається швидше')],
                [t('Ледяное копье (Ice Lance)', 'Ice Lance', 'Ice Lance'), '1', t('Удар по замороженной цели', 'A hit on a frozen target', 'Удар по замороженій цілі')],
                [t('Ледяные пальцы (Fingers of Frost)', 'Fingers of Frost', 'Fingers of Frost'), '2', t('Следующие 2 заклинания — как по замороженной цели', 'Your next 2 spells act as if the target were frozen', 'Наступні 2 заклинання — як по замороженій цілі')],
            ]}),
            ('text', [
                t('Сходятся Icy Veins и Wowhead. Точность стихии (Elemental Precision) берут оба, но с разным числом очков. Icy Veins ещё берёт Обморожение (Frostbite), Ледяные осколки (Ice Shards), Обледенение (Shatter) и [[Направленную силу льда|Frost Channeling]]; Wowhead в тексте гайда советует [[Ледяную глыбу|Ice Block]] и [[Холодную хватку|Cold Snap]], а его встроенный билд не открывается.',
                  'Icy Veins and Wowhead agree. Both take Elemental Precision, but with a different number of points. Icy Veins also takes Frostbite, Ice Shards, Shatter and Frost Channeling; the Wowhead guide text recommends Ice Block and Cold Snap, and its embedded build does not open.',
                  'Сходяться Icy Veins і Wowhead. Elemental Precision беруть обидва, але з різною кількістю очок. Icy Veins ще бере Frostbite, Ice Shards, Shatter і Frost Channeling; Wowhead у тексті гайда радить Ice Block і Cold Snap, а його вбудований білд не відкривається.'),
            ]),
            ('steps', [
                {'t': t('Ледяная стрела', 'Frostbolt', 'Frostbolt'),
                 'd': t('Основное заклинание.', 'Your main spell.', 'Основне заклинання.')},
                {'t': t('Сработали Ледяные пальцы', 'Fingers of Frost procs', 'Спрацювали Fingers of Frost'),
                 'd': t('Прервать чтение и сразу Ледяное копье.', 'Cancel the cast and use Ice Lance at once.', 'Перервати читання й одразу Ice Lance.')},
                {'t': t('Цель заморожена', 'The target is frozen', 'Ціль заморожена'),
                 'd': t('Ледяное копье, пока держится заморозка.', 'Ice Lance while the freeze lasts.', 'Ice Lance, поки тримається заморожування.')},
                {'t': t('Группа', 'Group of enemies', 'Група'),
                 'd': t('На 3+ врагах Конус холода и Ледяное копье, на 5+ Конус холода по откату и Снежная буря.', 'Against 3+ enemies, Cone of Cold and Ice Lance; against 5+, Cone of Cold on cooldown and Blizzard.', 'На 3+ ворогах Cone of Cold і Ice Lance, на 5+ Cone of Cold по відкату й Blizzard.')},
            ]),
            ('tip', t('Ледяное копье и Ледяные пальцы — новые таланты Forever. Порядок характеристик спорный: Icy Veins ставит первой меткость, Warcraft Tavern — силу заклинаний.',
                      'Ice Lance and Fingers of Frost are new Forever talents. The stat order is disputed: Icy Veins puts hit first, Warcraft Tavern puts spell power first.',
                      'Ice Lance і Fingers of Frost — нові таланти Forever. Порядок характеристик спірний: Icy Veins ставить першою влучність, Warcraft Tavern — силу заклинань.')),
        ]},
        {'id': 'faq', 'title': FAQ_T, 'blocks': [
            ('faq', [
                {'id': 'q1', 'q': t('Какой спек мага лучший для подземелий?', 'Which Mage spec is best for dungeons?', 'Яка спеціалізація мага найкраща для підземель?'),
                 'a': [t('В тир-листе беты Тайная магия — A, Огонь — A* (у Noobtoboss B для подземелий), Лёд — B.', 'On the beta tier list Arcane is A, Fire is A* (B for dungeons at Noobtoboss), Frost is B.', 'У тір-листі бети Тайна магія — A, Вогонь — A* (у Noobtoboss B для підземель), Лід — B.')]},
                {'id': 'q2', 'q': t('Heating Up или Hot Streak?', 'Heating Up or Hot Streak?', 'Heating Up чи Hot Streak?'),
                 'a': [t('Это один талант Огня. Калькуляторы Icy Veins и Wowhead называют его Heating Up, в тексте гайда Icy Veins осталось Hot Streak.', 'It is the same Fire talent. The Icy Veins and Wowhead calculators call it Heating Up; the Icy Veins guide text still says Hot Streak.', 'Це один талант Вогню. Калькулятори Icy Veins і Wowhead називають його Heating Up, у тексті гайда Icy Veins лишилося Hot Streak.')]},
                {'id': 'q3', 'q': t('Сколько раз жать Чародейскую вспышку?', 'How many Arcane Blasts should I cast?', 'Скільки разів тиснути Arcane Blast?'),
                 'a': [t('2–3 раза, затем Огненный взрыв, если не сработали Заградительные стрелы. Дольше — только на боссе.', '2–3 times, then Fire Blast if Missile Barrage has not procced. Longer only on a boss.', '2–3 рази, потім Fire Blast, якщо не спрацювали Missile Barrage. Довше — лише на босі.')]},
                {'id': 'q4', 'q': WHEN_Q, 'a': [WHEN_A]},
            ]),
        ]},
        {'id': 'related', 'title': t('Смотрите также', 'See also', 'Дивіться також'), 'blocks': [
            ('tiles', _related('mage', [t('Маг', 'Mage', 'Маг'), t('Прокачка Мага', 'Mage leveling', 'Прокачування Мага')])),
        ]},
    ],
})

# ---------- hunter ----------

SPEC_BUILDS.append({
    'slug': 'builds-hunter', 'art': 'hunter', 'hero': 'hero_leveling', 'hub': False,
    'title': t('Билды Охотника', 'Hunter Builds', 'Білди Мисливця'),
    'lead': t('Таланты, приоритет и характеристики Повелителя зверей, Стрельбы и Выживания. Здесь только то, в чём сходятся Icy Veins и Wowhead.',
              'Talents, priorities and stats for Beast Mastery, Marksmanship and Survival. This page shows only what Icy Veins and Wowhead agree on.',
              'Таланти, пріоритет і характеристики Володіння звірами, Стрільби та Виживання. Тут лише те, у чому сходяться Icy Veins і Wowhead.'),
    'tile': t('Повелитель зверей, Стрельба, Выживание: таланты и приоритет', 'Beast Mastery, Marksmanship, Survival: talents and priorities', 'Володіння звірами, Стрільба, Виживання: таланти й пріоритет'),
    'pills': [BETA, SPECS3, LATER],
    'sources': [
        ('Icy Veins: Beast Mastery Hunter Guide', 'https://www.icy-veins.com/wow-forever/beast-mastery-hunter-ranged-dps-pve-guide'),
        ('Icy Veins: Marksmanship Hunter Guide', 'https://www.icy-veins.com/wow-forever/marksmanship-hunter-ranged-dps-pve-guide'),
        ('Icy Veins: Survival Hunter Guide', 'https://www.icy-veins.com/wow-forever/survival-hunter-melee-dps-pve-guide'),
        ('Icy Veins: Hunter Talent Calculator', 'https://www.icy-veins.com/wow-forever/hunter-talent-calculator'),
        ('Wowhead: Level 30 Beast Mastery Hunter', 'https://www.wowhead.com/forever/guide/classes/hunter/beast-mastery/level-30-dps-overview'),
        ('Wowhead: Level 30 Marksmanship Hunter', 'https://www.wowhead.com/forever/guide/classes/hunter/marksmanship/level-30-dps-overview'),
        ('Wowhead: Level 30 Survival Hunter', 'https://www.wowhead.com/forever/guide/classes/hunter/survival/level-30-dps-overview'),
        ('Wowhead: Hunter Talent Calculator', 'https://www.wowhead.com/forever/talent-calc/hunter'),
    ],
    'sections': [
        {'id': 'roles', 'title': t('Спеки и роли', 'Specs and roles', 'Спеціалізації та ролі'), 'blocks': [
            ('table', {'head': H_ROLES, 'rows': [
                [t('Повелитель зверей', 'Beast Mastery', 'Володіння звірами'), DPS, 'A*',
                 t('Питомец и ястребы; питомец растёт от ваших характеристик', 'Pet and hawks; the pet scales with your stats', 'Улюбленець і яструби; улюбленець росте від ваших характеристик')],
                [t('Стрельба', 'Marksmanship', 'Стрільба'), DPS, 'A*',
                 t('Аура меткого выстрела для группы, урон по площади', 'Trueshot Aura for the group, area damage', 'Trueshot Aura для групи, шкода по площі')],
                [t('Выживание', 'Survival', 'Виживання'), DPS, 'A',
                 t('Ближний бой с 30 уровня', 'Melee from level 30', 'Ближній бій з 30 рівня')],
            ]}),
            ('text', [ROLES_NOTE, t('A* у Повелителя зверей и Стрельбы: Noobtoboss ставит их в S, RankedBoost — в A.', 'A* for Beast Mastery and Marksmanship: Noobtoboss puts them in S, RankedBoost in A.', 'A* у Володіння звірами й Стрільби: Noobtoboss ставить їх у S, RankedBoost — в A.')]),
        ]},
        {'id': 'beast-mastery', 'title': t('Повелитель зверей: урон', 'Beast Mastery: damage', 'Володіння звірами: шкода'), 'blocks': [
            ('text', [
                t('Повелитель зверей держится на питомце: в Forever он получает часть ваших характеристик и растёт вместе с вами. Summon Hawk открывается на 25 уровне (на 20 с очками Legacy): ястреб 18 секунд бьёт цели, одновременно их может быть два. Откат у него общий с Чародейским выстрелом.',
                  'Beast Mastery runs on the pet: in Forever it inherits part of your stats and grows with you. Summon Hawk unlocks at level 25 (20 with Legacy points): a hawk attacks your targets for 18 seconds, and two can be active at once. It shares a cooldown with Arcane Shot.',
                  'Володіння звірами тримається на улюбленці: у Forever він отримує частину ваших характеристик і росте разом із вами. Summon Hawk відкривається на 25 рівні (на 20 з очками Legacy): яструб 18 секунд б’є цілі, одночасно їх може бути два. Відкат у нього спільний з Arcane Shot.'),
            ]),
            ('table', {'head': H_TAL, 'rows': [
                ['Deadly Aspects', '5', t('С Духом ястреба Автоматическая стрельба может дать +30% к скорости стрельбы на 12 секунд', 'With Aspect of the Hawk, Auto Shot can grant +30% ranged attack speed for 12 seconds', 'З Aspect of the Hawk Auto Shot може дати +30% до швидкості стрільби на 12 секунд')],
                [t('Неудержимое неистовство (Unleashed Fury)', 'Unleashed Fury', 'Unleashed Fury'), '5', t('Урон питомца и ястребов', 'Pet and hawk damage', 'Шкода улюбленця і яструбів')],
                [t('Свирепость (Ferocity)', 'Ferocity', 'Ferocity'), '3', t('Крит питомца и ястребов', 'Pet and hawk crit', 'Крит улюбленця і яструбів')],
                ['Summon Hawk', '1', t('Ястреб-помощник, главная новая кнопка', 'A hawk helper, the key new button', 'Яструб-помічник, головна нова кнопка')],
                [t('Устрашение (Intimidation)', 'Intimidation', 'Intimidation'), '1', t('Питомец оглушает цель на 3 секунды', 'The pet stuns the target for 3 seconds', 'Улюбленець оглушує ціль на 3 секунди')],
                [t('Звериная стремительность (Bestial Swiftness)', 'Bestial Swiftness', 'Bestial Swiftness'), '1', t('+30% к скорости питомца', '+30% pet movement speed', '+30% до швидкості улюбленця')],
                [t('Улучшенное воскрешение питомца (Improved Revive Pet)', 'Improved Revive Pet', 'Improved Revive Pet'), '2', t('Воскрешение питомца быстрее и дешевле, им можно пользоваться в бою', 'A faster, cheaper Revive Pet you can use in combat', 'Воскресіння улюбленця швидше й дешевше, ним можна користуватися в бою')],
            ]}),
            ('text', [
                t('Эти таланты берут и Icy Veins, и Wowhead. Расходятся три очка: Icy Veins добирает второе очко [[Знания троп|Pathfinding]] — Дух гепарда быстрее — и [[Тренировку стойкости|Endurance Training]], Wowhead — одно очко Знания троп и Направленный огонь (Focused Fire): больше урона, пока призван питомец. С пятью очками перка Legacy Talented оба добирают одно и то же: Свирепость до 5, Беспрекословное послушание (Bestial Discipline) 2 и Бешенство (Frenzy) 1.',
                  'Both Icy Veins and Wowhead take these talents. Three points differ: Icy Veins adds a second point in Pathfinding (a faster Aspect of the Cheetah) and Endurance Training, Wowhead one point in Pathfinding and Focused Fire: more damage while your pet is out. With the five points of the Legacy Talented perk, both add the same: Ferocity to 5, Bestial Discipline 2 and Frenzy 1.',
                  'Ці таланти беруть і Icy Veins, і Wowhead. Розходяться три очки: Icy Veins добирає друге очко Pathfinding (швидший Aspect of the Cheetah) і Endurance Training, Wowhead — одне очко Pathfinding і Focused Fire: більше шкоди, поки улюбленця викликано. З п’ятьма очками перка Legacy Talented обидва добирають одне й те саме: Ferocity до 5, Bestial Discipline 2 і Frenzy 1.'),
            ]),
            ('steps', [
                {'t': t('Перед боем', 'Before the pull', 'Перед боєм'),
                 'd': t('Метка охотника; питомец атакует первым.', 'Hunter’s Mark; the pet attacks first.', 'Hunter’s Mark; улюбленець атакує першим.')},
                {'t': t('Укус змеи', 'Serpent Sting', 'Serpent Sting'),
                 'd': t('Когда питомец взял цель.', 'Once the pet has the target.', 'Коли улюбленець узяв ціль.')},
                {'t': 'Summon Hawk',
                 'd': t('По откату, держите двух ястребов.', 'On cooldown; keep two hawks out.', 'По відкату, тримайте двох яструбів.')},
                {'t': t('Прицельный выстрел', 'Aimed Shot', 'Aimed Shot'),
                 'd': t('По откату; против группы вместо него Залп.', 'On cooldown; Multi-Shot instead against a group.', 'По відкату; проти групи замість нього Multi-Shot.')},
                {'t': t('Чародейский выстрел', 'Arcane Shot', 'Arcane Shot'),
                 'd': t('Только при полной мане, если оба ястреба проживут ещё 6 секунд.', 'Only at full mana, when both hawks will last another 6 seconds.', 'Лише за повної мани, якщо обидва яструби проживуть ще 6 секунд.')},
                {'t': t('Враг ушёл на вас', 'An enemy turns to you', 'Ворог пішов на вас'),
                 'd': t('Отрыв.', 'Disengage.', 'Disengage.')},
            ]),
            ('tip', t('Характеристики по Icy Veins: урон оружия первым — медленное оружие лучше, Прицельный выстрел считается от урона оружия. Затем меткость, ловкость и крит: питомец наследует ваш шанс крита. Звериный гнев (Bestial Wrath) требует 31 очко в ветке, до старта его не взять.',
                      'Stats according to Icy Veins: weapon damage first — a slow weapon is better, since Aimed Shot is based on weapon damage. Then hit, Agility and crit: the pet inherits your crit chance. Bestial Wrath needs 31 points in the tree, so it is out of reach before launch.',
                      'Характеристики за Icy Veins: шкода зброї першою — повільна зброя краща, Aimed Shot рахується від шкоди зброї. Потім влучність, спритність і крит: улюбленець успадковує ваш шанс криту. Bestial Wrath потребує 31 очко в гілці, до старту його не взяти.')),
        ]},
        {'id': 'marksmanship', 'title': t('Стрельба: урон', 'Marksmanship: damage', 'Стрільба: шкода'), 'blocks': [
            ('text', [
                t('Стрельба на 30 уровне — спек для подземелий: Аура меткого выстрела даёт силу атаки дальнего боя всей группе. Icy Veins прямо пишет, что для прокачки лучше билд Повелителя зверей; Wowhead считает, что качаться в Стрельбе тоже можно.',
                  'At level 30 Marksmanship is a dungeon spec: Trueshot Aura gives ranged attack power to the whole group. Icy Veins says plainly that the Beast Mastery build is better for leveling; Wowhead says leveling as Marksmanship is fine too.',
                  'Стрільба на 30 рівні — спеціалізація для підземель: Trueshot Aura дає силу атаки дальнього бою всій групі. Icy Veins прямо пише, що для прокачування краще білд Володіння звірами; Wowhead вважає, що качатися в Стрільбі теж можна.'),
            ]),
            ('table', {'head': H_TAL, 'rows': [
                ['Lethal Attacks', '5', t('Шанс крита всех атак', 'Crit chance with all attacks', 'Шанс криту всіх атак')],
                [t('Верная цель (Careful Aim)', 'Careful Aim', 'Careful Aim'), '5', t('Сила атаки от интеллекта', 'Attack power from Intellect', 'Сила атаки від інтелекту')],
                [t('Аура меткого выстрела (Trueshot Aura)', 'Trueshot Aura', 'Trueshot Aura'), '1', t('Сила атаки дальнего боя всей группе', 'Ranged attack power for the whole group', 'Сила атаки дальнього бою всій групі')],
                [t('Смертоносные выстрелы (Mortal Shots)', 'Mortal Shots', 'Mortal Shots'), '4', t('Урон критов дальнего боя', 'Ranged crit damage', 'Шкода критів дальнього бою')],
            ]}),
            ('text', [
                t('Сходятся Icy Veins и Wowhead; Смертоносные выстрелы Icy Veins доводит до 5. Дальше расходятся. Icy Veins берёт [[Одинокого волка|Lone Wolf]] (+20% к урону без питомца) ради Залпа в подземельях, Быстрые убийства (Rapid Killing) и Эффективность (Efficiency). Wowhead на 21 очко Одинокого волка не берёт — питомец, по его словам, бьёт сильнее — и кладёт 5 очков в Улучшенный чародейский выстрел (Improved Arcane Shot) и одно в Дезориентирующий выстрел (Scatter Shot).',
                  'Icy Veins and Wowhead agree; Icy Veins takes Mortal Shots to 5. Beyond that they differ. Icy Veins takes Lone Wolf (+20% damage without a pet) for Multi-Shot in dungeons, Rapid Killing and Efficiency. With 21 points Wowhead skips Lone Wolf — in its view the pet hits harder — and puts 5 points into Improved Arcane Shot and one into Scatter Shot.',
                  'Сходяться Icy Veins і Wowhead; Mortal Shots Icy Veins доводить до 5. Далі розходяться. Icy Veins бере Lone Wolf (+20% до шкоди без улюбленця) заради Multi-Shot у підземеллях, Rapid Killing і Efficiency. Wowhead на 21 очко Lone Wolf не бере — улюбленець, за його словами, б’є сильніше — і кладе 5 очок в Improved Arcane Shot та одне в Scatter Shot.'),
            ]),
            ('steps', [
                {'t': t('Перед боем', 'Before the pull', 'Перед боєм'),
                 'd': t('Метка охотника; питомец атакует первым.', 'Hunter’s Mark; the pet attacks first.', 'Hunter’s Mark; улюбленець атакує першим.')},
                {'t': t('Укус змеи', 'Serpent Sting', 'Serpent Sting'),
                 'd': t('Когда питомец взял цель.', 'Once the pet has the target.', 'Коли улюбленець узяв ціль.')},
                {'t': t('Прицельный выстрел', 'Aimed Shot', 'Aimed Shot'),
                 'd': t('По откату; против группы вместо него Залп.', 'On cooldown; Multi-Shot instead against a group.', 'По відкату; проти групи замість нього Multi-Shot.')},
                {'t': t('Чародейский выстрел', 'Arcane Shot', 'Arcane Shot'),
                 'd': t('По откату, если хватает маны.', 'On cooldown if you have the mana.', 'По відкату, якщо вистачає мани.')},
                {'t': t('Автоматическая стрельба', 'Auto Shot', 'Auto Shot'),
                 'd': t('Всё остальное время: основной урон охотника — обычные атаки (Icy Veins).', 'The rest of the time: most of a Hunter’s damage comes from basic attacks (Icy Veins).', 'Увесь інший час: основна шкода мисливця — звичайні атаки (Icy Veins).')},
            ]),
            ('tip', t('Характеристики по Icy Veins те же, что у Повелителя зверей: урон оружия, меткость, ловкость, крит; от крита растут Смертоносные выстрелы. С очками Legacy Icy Veins советует 5 очков в Deadly Aspects, а на будущее — Rapid Recuperation от нехватки маны.',
                      'Stats according to Icy Veins are the same as for Beast Mastery: weapon damage, hit, Agility, crit; Mortal Shots scales with crit. With Legacy points, Icy Veins suggests 5 points in Deadly Aspects, and Rapid Recuperation later on for mana problems.',
                      'Характеристики за Icy Veins ті самі, що й у Володіння звірами: шкода зброї, влучність, спритність, крит; від криту ростуть Mortal Shots. З очками Legacy Icy Veins радить 5 очок у Deadly Aspects, а на майбутнє — Rapid Recuperation від нестачі мани.')),
        ]},
        {'id': 'survival', 'title': t('Выживание: урон', 'Survival: damage', 'Виживання: шкода'), 'blocks': [
            ('text', [
                t('Выживание в Forever — охотник ближнего боя. До 30 уровня ему не хватает инструментов: Icy Veins не советует эту ветку для быстрой прокачки, Wowhead — играть гибридно, пока нет Strider Kick. Strider Kick бьёт на 100% урона оружия и даёт +30% к скорости бега на 3 секунды: можно отойти и выстрелить, пока удары на откате (Wowhead).',
                  'In Forever, Survival is a melee Hunter. Until level 30 it lacks tools: Icy Veins advises against this tree for fast leveling, and Wowhead suggests a hybrid playstyle until you have Strider Kick. Strider Kick hits for 100% weapon damage and gives +30% movement speed for 3 seconds, so you can step out and shoot while your strikes are on cooldown (Wowhead).',
                  'Виживання у Forever — мисливець ближнього бою. До 30 рівня йому бракує інструментів: Icy Veins не радить цю гілку для швидкого прокачування, Wowhead — грати гібридно, поки немає Strider Kick. Strider Kick б’є на 100% шкоди зброї й дає +30% до швидкості бігу на 3 секунди: можна відійти й вистрілити, поки удари на відкаті (Wowhead).'),
            ]),
            ('table', {'head': H_TAL, 'rows': [
                ['Improved Tracking', '5', t('Урон по выслеживаемому типу существ', 'Damage to the tracked creature type', 'Шкода по типу істот, яких вистежуєте')],
                [t('Беспощадные удары (Savage Strikes)', 'Savage Strikes', 'Savage Strikes'), '2', t('Крит способностей ближнего боя', 'Melee ability crit', 'Крит здібностей ближнього бою')],
                [t('Верный шаг (Surefooted)', 'Surefooted', 'Surefooted'), '3', t('Меткость, короче замедления', 'Hit, shorter slows', 'Влучність, коротші сповільнення')],
                ['Predator’s Edge', '4', t('Урон критов ближнего боя и второго оружия', 'Melee crit damage and off-hand damage', 'Шкода критів ближнього бою й другої зброї')],
                ['Strider Kick', '1', t('Удар и +30% к скорости бега на 3 секунды', 'A strike and +30% movement speed for 3 seconds', 'Удар і +30% до швидкості бігу на 3 секунди')],
            ]}),
            ('text', [
                t('Сходятся Icy Veins и Wowhead; Predator’s Edge Icy Veins доводит до 5. Расходятся: Icy Veins берёт ловушки — Удержание (Entrapment) 3 и Хитрые ловушки (Clever Traps) 2, Wowhead — Отражение (Deflection) 4, Сдерживание (Deterrence) и [[Контратаку|Counterattack]]. Очки Legacy оба отдают в Находчивость (Resourcefulness) 2 — экономия маны — и Expose Prey 2: атаки по цели с Меткой охотника иногда открывают Укус мангуста.',
                  'Icy Veins and Wowhead agree; Icy Veins takes Predator’s Edge to 5. They differ: Icy Veins takes traps — Entrapment 3 and Clever Traps 2, Wowhead takes Deflection 4, Deterrence and Counterattack. Both spend the Legacy points on Resourcefulness 2, which saves mana, and Expose Prey 2: attacks on a target with Hunter’s Mark sometimes enable Mongoose Bite.',
                  'Сходяться Icy Veins і Wowhead; Predator’s Edge Icy Veins доводить до 5. Розходяться: Icy Veins бере пастки — Entrapment 3 і Clever Traps 2, Wowhead — Deflection 4, Deterrence і Counterattack. Очки Legacy обидва віддають у Resourcefulness 2 — економія мани — і Expose Prey 2: атаки по цілі з Hunter’s Mark іноді відкривають Mongoose Bite.'),
            ]),
            ('steps', [
                {'t': t('Перед боем', 'Before the pull', 'Перед боєм'),
                 'd': t('Метка охотника, питомец атакует первым, затем Укус змеи.', 'Hunter’s Mark, the pet attacks first, then Serpent Sting.', 'Hunter’s Mark, улюбленець атакує першим, потім Serpent Sting.')},
                {'t': t('Удар ящера', 'Raptor Strike', 'Raptor Strike'),
                 'd': t('По откату в ближнем бою.', 'On cooldown in melee.', 'По відкату в ближньому бою.')},
                {'t': t('Укус мангуста', 'Mongoose Bite', 'Mongoose Bite'),
                 'd': t('Как только доступен.', 'As soon as it is available.', 'Щойно доступний.')},
                {'t': 'Strider Kick',
                 'd': t('По откату.', 'On cooldown.', 'По відкату.')},
                {'t': t('Враг ушёл с питомца', 'An enemy leaves the pet', 'Ворог пішов з улюбленця'),
                 'd': t('Отрыв.', 'Disengage.', 'Disengage.')},
            ]),
            ('tip', t('Характеристики по Icy Veins: урон оружия, меткость, ловкость, крит, затем сила — она даёт силу атаки ближнего боя, но меньше, чем ловкость. Strider Kick, Predator’s Edge и Expose Prey — новые таланты Forever.',
                      'Stats according to Icy Veins: weapon damage, hit, Agility, crit, then Strength — it gives melee attack power, but less than Agility. Strider Kick, Predator’s Edge and Expose Prey are new Forever talents.',
                      'Характеристики за Icy Veins: шкода зброї, влучність, спритність, крит, потім сила — вона дає силу атаки ближнього бою, але менше, ніж спритність. Strider Kick, Predator’s Edge і Expose Prey — нові таланти Forever.')),
        ]},
        {'id': 'faq', 'title': FAQ_T, 'blocks': [
            ('faq', [
                {'id': 'q1', 'q': t('Какой спек охотника лучший в WoW Forever?', 'Which Hunter spec is best in WoW Forever?', 'Яка спеціалізація мисливця найкраща у WoW Forever?'),
                 'a': [t('Для прокачки оба источника советуют Повелителя зверей. Для подземелий в тир-листе беты Повелитель зверей и Стрельба — A*, Выживание — A.', 'For leveling, both sources recommend Beast Mastery. For dungeons, the beta tier list has Beast Mastery and Marksmanship at A* and Survival at A.', 'Для прокачування обидва джерела радять Володіння звірами. Для підземель у тір-листі бети Володіння звірами й Стрільба — A*, Виживання — A.')]},
                {'id': 'q2', 'q': t('Брать ли Одинокого волка?', 'Should I take Lone Wolf?', 'Чи брати Lone Wolf?'),
                 'a': [t('Только ради урона по площади в подземельях: +20% к урону без питомца. Icy Veins берёт его в билд Стрельбы, Wowhead на 21 очко — нет: питомец бьёт сильнее.', 'Only for area damage in dungeons: +20% damage without a pet. Icy Veins puts it in its Marksmanship build; with 21 points Wowhead does not, since the pet hits harder.', 'Лише заради шкоди по площі в підземеллях: +20% до шкоди без улюбленця. Icy Veins бере його в білд Стрільби, Wowhead на 21 очко — ні: улюбленець б’є сильніше.')]},
                {'id': 'q3', 'q': t('Какого питомца взять?', 'Which pet should I tame?', 'Якого улюбленця взяти?'),
                 'a': [t('Icy Veins советует медведя: его Размах бьёт по нескольким целям и держит их на питомце. Wowhead на бете называл лучшей быструю кошку, но из-за ошибок, которые могут исправить.', 'Icy Veins recommends a bear: its Swipe hits several targets and keeps them on the pet. On the beta Wowhead named a fast cat as the best pet, but because of bugs that may be fixed.', 'Icy Veins радить ведмедя: його Swipe б’є по кількох цілях і тримає їх на улюбленці. Wowhead у беті називав найкращою швидку кішку, але через помилки, які можуть виправити.')]},
                {'id': 'q4', 'q': WHEN_Q, 'a': [WHEN_A]},
            ]),
        ]},
        {'id': 'related', 'title': t('Смотрите также', 'See also', 'Дивіться також'), 'blocks': [
            ('tiles', _related('hunter', [t('Охотник', 'Hunter', 'Мисливець'), t('Прокачка Охотника', 'Hunter leveling', 'Прокачування Мисливця')])),
        ]},
    ],
})

# ---------- rogue ----------

SPEC_BUILDS.append({
    'slug': 'builds-rogue', 'art': 'rogue', 'hero': 'hero_leveling', 'hub': False,
    'title': t('Билды Разбойника', 'Rogue Builds', 'Білди Розбійника'),
    'lead': t('Таланты, приоритет и характеристики Ликвидации, Боя и Скрытности. Здесь только то, в чём сходятся Icy Veins и Wowhead.',
              'Talents, priorities and stats for Assassination, Combat and Subtlety. This page shows only what Icy Veins and Wowhead agree on.',
              'Таланти, пріоритет і характеристики Ліквідації, Бою та Непомітності. Тут лише те, у чому сходяться Icy Veins і Wowhead.'),
    'tile': t('Ликвидация, Бой, Скрытность: таланты и приоритет', 'Assassination, Combat, Subtlety: talents and priorities', 'Ліквідація, Бій, Непомітність: таланти й пріоритет'),
    'pills': [BETA, SPECS3, LATER],
    'sources': [
        ('Icy Veins: Assassination Rogue Guide', 'https://www.icy-veins.com/wow-forever/assassination-rogue-melee-dps-pve-guide'),
        ('Icy Veins: Combat Rogue Guide', 'https://www.icy-veins.com/wow-forever/combat-rogue-melee-dps-pve-guide'),
        ('Icy Veins: Subtlety Rogue Guide', 'https://www.icy-veins.com/wow-forever/subtlety-rogue-melee-dps-pve-guide'),
        ('Icy Veins: Rogue Talent Calculator', 'https://www.icy-veins.com/wow-forever/rogue-talent-calculator'),
        ('Wowhead: Level 30 Assassination Rogue', 'https://www.wowhead.com/forever/guide/classes/rogue/assassination/level-30-dps-overview'),
        ('Wowhead: Level 30 Combat Rogue', 'https://www.wowhead.com/forever/guide/classes/rogue/combat/level-30-dps-overview'),
        ('Wowhead: Level 30 Subtlety Rogue', 'https://www.wowhead.com/forever/guide/classes/rogue/subtlety/level-30-dps-overview'),
        ('Wowhead: Rogue Talent Calculator', 'https://www.wowhead.com/forever/talent-calc/rogue'),
    ],
    'sections': [
        {'id': 'roles', 'title': t('Спеки и роли', 'Specs and roles', 'Спеціалізації та ролі'), 'blocks': [
            ('table', {'head': H_ROLES, 'rows': [
                [t('Ликвидация', 'Assassination', 'Ліквідація'), DPS, 'A',
                 t('Расправа с двумя кинжалами, яды', 'Mutilate with two daggers, poisons', 'Mutilate з двома кинджалами, отрути')],
                [t('Бой', 'Combat', 'Бій'), DPS, 'A*',
                 t('Шквал клинков: урон по второй цели', 'Blade Flurry: damage to a second target', 'Blade Flurry: шкода по другій цілі')],
                [t('Скрытность', 'Subtlety', 'Непомітність'), DPS, 'C',
                 t('Ветка для PvP, в группе слабее', 'A PvP tree, weaker in a group', 'Гілка для PvP, у групі слабша')],
            ]}),
            ('text', [ROLES_NOTE, t('A* у Боя: RankedBoost ставит его в B.', 'A* for Combat: RankedBoost puts it in B.', 'A* у Бою: RankedBoost ставить його в B.')]),
        ]},
        {'id': 'assassination', 'title': t('Ликвидация: урон', 'Assassination: damage', 'Ліквідація: шкода'), 'blocks': [
            ('text', [
                t('Ликвидация на 30 уровне получает Расправу: удар обоими оружиями на 2 приёма серии, сильнее по отравленной цели. Нужны два кинжала (Icy Veins). Приёмы серии копятся Расправой и тратятся на Мясорубку и Потрошение; Рваную рану Wowhead советует против целей с крепкой бронёй.',
                  'Assassination gets Mutilate at level 30: a strike with both weapons for 2 combo points that hits harder on a poisoned target. It needs two daggers (Icy Veins). Mutilate builds combo points, Slice and Dice and Eviscerate spend them; Wowhead suggests Rupture against targets with heavy armor.',
                  'Ліквідація на 30 рівні отримує Mutilate: удар обома зброями на 2 прийоми серії, сильніший по отруєній цілі. Потрібні два кинджали (Icy Veins). Прийоми серії накопичує Mutilate, витрачають Slice and Dice та Eviscerate; Rupture Wowhead радить проти цілей із міцною бронею.'),
            ]),
            ('table', {'head': H_TAL, 'rows': [
                [t('Злоба (Malice)', 'Malice', 'Malice'), '5', t('Шанс крита атак и ядов', 'Crit chance with attacks and poisons', 'Шанс криту атак і отрут')],
                [t('Жестокость (Ruthlessness)', 'Ruthlessness', 'Ruthlessness'), '3', t('Завершающие приёмы иногда дают приём серии', 'Finishers sometimes add a combo point', 'Завершальні прийоми іноді дають прийом серії')],
                [t('Неослабевающие удары (Relentless Strikes)', 'Relentless Strikes', 'Relentless Strikes'), '1', t('Завершающие приёмы возвращают энергию', 'Finishers restore Energy', 'Завершальні прийоми повертають енергію')],
                [t('Хладнокровие (Cold Blood)', 'Cold Blood', 'Cold Blood'), '1', t('Следующий удар — гарантированный крит', 'A guaranteed crit on the next strike', 'Наступний удар — гарантований крит')],
                [t('Улучшенные яды (Improved Poisons)', 'Improved Poisons', 'Improved Poisons'), '4', t('Яды срабатывают чаще и реже тратят заряды', 'Poisons proc more often and use fewer charges', 'Отрути спрацьовують частіше й рідше витрачають заряди')],
                [t('Расправа (Mutilate)', 'Mutilate', 'Mutilate'), '1', t('Главный удар: оба оружия, 2 приёма серии', 'Your main strike: both weapons, 2 combo points', 'Головний удар: обидві зброї, 2 прийоми серії')],
            ]}),
            ('text', [
                t('Сходятся Icy Veins и Wowhead; Смертоносность (Lethality) берут оба, но с разным числом очков. Остальное расходится. Icy Veins доводит Смертоносность до 4 и берёт Беспощадные атаки (Remorseless Attacks) 2, а [[Улучшенную мясорубку|Improved Slice and Dice]] пропускает: враги на этих уровнях живут недолго. Wowhead берёт её 3 и Убийство (Murder) 2 — урон по гуманоидам и великанам. Очки Legacy тоже по-разному: у Icy Veins Улучшенные яды до 5 и Тлетворные яды (Vile Poisons), у Wowhead Улучшенное потрошение (Improved Eviscerate) 3 и Правильный момент (Opportunity) 2.',
                  'Icy Veins and Wowhead agree; both take Lethality, but with a different number of points. The rest differs. Icy Veins takes Lethality to 4 and adds Remorseless Attacks 2, skipping Improved Slice and Dice because enemies at these levels die fast. Wowhead takes it at 3 plus Murder 2, damage against humanoids and giants. The Legacy points differ too: Icy Veins takes Improved Poisons to 5 and adds Vile Poisons, Wowhead takes Improved Eviscerate 3 and Opportunity 2.',
                  'Сходяться Icy Veins і Wowhead; Lethality беруть обидва, але з різною кількістю очок. Решта розходиться. Icy Veins доводить Lethality до 4 і бере Remorseless Attacks 2, а Improved Slice and Dice пропускає: вороги на цих рівнях живуть недовго. Wowhead бере його 3 і Murder 2 — шкода по гуманоїдах і велетнях. Очки Legacy теж по-різному: в Icy Veins Improved Poisons до 5 і Vile Poisons, у Wowhead Improved Eviscerate 3 і Opportunity 2.'),
            ]),
            ('steps', [
                {'t': t('Перед боем', 'Before the pull', 'Перед боєм'),
                 'd': t('Быстродействующий яд на оба оружия, Незаметность.', 'Instant Poison on both weapons, Stealth.', 'Instant Poison на обидві зброї, Stealth.')},
                {'t': t('Начало', 'Opening', 'Початок'),
                 'd': t('Внезапный удар из незаметности.', 'Ambush from Stealth.', 'Ambush з невидимості.')},
                {'t': t('Расправа', 'Mutilate', 'Mutilate'),
                 'd': t('При 3 приёмах серии и меньше; на 4–5 не жмите (Wowhead).', 'At 3 combo points or fewer; never at 4–5 (Wowhead).', 'За 3 прийомів серії й менше; на 4–5 не тисніть (Wowhead).')},
                {'t': t('Мясорубка', 'Slice and Dice', 'Slice and Dice'),
                 'd': t('Держать, если цель проживёт.', 'Keep it up if the target will live long enough.', 'Тримати, якщо ціль проживе.')},
                {'t': t('Потрошение', 'Eviscerate', 'Eviscerate'),
                 'd': t('Тратить лишние приёмы серии; по цели с крепкой бронёй — Рваная рана.', 'Spend spare combo points; Rupture on a target with heavy armor.', 'Витрачати зайві прийоми серії; по цілі з міцною бронею — Rupture.')},
                {'t': t('Группа бьёт физическим уроном', 'A physical damage group', 'Група б’є фізичною шкодою'),
                 'd': t('Ослабление доспеха на долгую цель.', 'Expose Armor on a long-lived target.', 'Expose Armor на довгу ціль.')},
            ]),
            ('tip', t('Характеристики по Icy Veins (у всех спеков разбойника): урон оружия первым, затем меткость и мастерство (Expertise), ловкость, крит. Ошеломление в Forever не выводит из незаметности (Wowhead): его можно ставить перед боем.',
                      'Stats according to Icy Veins (for every Rogue spec): weapon damage first, then hit and Expertise, Agility, crit. In Forever Sap no longer breaks Stealth (Wowhead), so you can use it before a pull.',
                      'Характеристики за Icy Veins (у всіх спеціалізацій розбійника): шкода зброї першою, потім влучність і майстерність (Expertise), спритність, крит. Sap у Forever не виводить з невидимості (Wowhead): його можна ставити перед боєм.')),
        ]},
        {'id': 'combat', 'title': t('Бой: урон', 'Combat: damage', 'Бій: шкода'), 'blocks': [
            ('text', [
                t('Бой — самый собранный спек разбойника на 30 уровне. Шквал клинков на 15 секунд даёт +20% к скорости атак и бьёт ещё одну цель рядом; Выброса адреналина пока нет. Схема та же, что на 60: Коварный удар копит приёмы серии, Мясорубка и Потрошение их тратят (Wowhead).',
                  'Combat is the most complete Rogue spec at level 30. Blade Flurry gives +20% attack speed for 15 seconds and hits one more nearby target; Adrenaline Rush is not available yet. The pattern is the same as at 60: Sinister Strike builds combo points, Slice and Dice and Eviscerate spend them (Wowhead).',
                  'Бій — найзібраніша спеціалізація розбійника на 30 рівні. Blade Flurry на 15 секунд дає +20% до швидкості атак і б’є ще одну ціль поруч; Adrenaline Rush поки немає. Схема та сама, що на 60: Sinister Strike накопичує прийоми серії, Slice and Dice та Eviscerate їх витрачають (Wowhead).'),
            ]),
            ('table', {'head': H_TAL, 'rows': [
                [t('Улучшенное потрошение (Improved Eviscerate)', 'Improved Eviscerate', 'Improved Eviscerate'), '3', t('Урон Потрошения', 'Eviscerate damage', 'Шкода Eviscerate')],
                [t('Улучшенный коварный удар (Improved Sinister Strike)', 'Improved Sinister Strike', 'Improved Sinister Strike'), '2', t('Коварный удар дешевле', 'Cheaper Sinister Strike', 'Дешевший Sinister Strike')],
                [t('Отражение (Deflection)', 'Deflection', 'Deflection'), '3', t('Парирование; путь к Ответному удару', 'Parry; the path to Riposte', 'Парирування; шлях до Riposte')],
                [t('Точность (Precision)', 'Precision', 'Precision'), '3', t('Меткость', 'Hit', 'Влучність')],
                [t('Закалка (Endurance)', 'Endurance', 'Endurance'), '2', t('Короче откат Спринта и Ускользания', 'Shorter Sprint and Evasion cooldowns', 'Коротший відкат Sprint та Evasion')],
                [t('Ответный удар (Riposte)', 'Riposte', 'Riposte'), '1', t('Удар после парирования, обезоруживает', 'A strike after a parry that disarms', 'Удар після парирування, роззброює')],
                [t('Улучшенный спринт (Improved Sprint)', 'Improved Sprint', 'Improved Sprint'), '1', t('Спринт может снять замедления', 'Sprint can remove slows', 'Sprint може зняти сповільнення')],
                ['Flawless Execution', '1', t('Потрошение дешевле на 10 энергии', 'Eviscerate costs 10 less Energy', 'Eviscerate дешевший на 10 енергії')],
                [t('Специализация на бое двумя оружиями (Dual Wield Specialization)', 'Dual Wield Specialization', 'Dual Wield Specialization'), '4', t('Урон второго оружия', 'Off-hand damage', 'Шкода другої зброї')],
                [t('Шквал клинков (Blade Flurry)', 'Blade Flurry', 'Blade Flurry'), '1', t('+20% к скорости атак и удар по второй цели', '+20% attack speed and a hit on a second target', '+20% до швидкості атак і удар по другій цілі')],
            ]}),
            ('text', [
                t('Здесь Icy Veins и Wowhead совпадают полностью, во всех 21 очке. Очки Legacy оба отдают в Круши-руби (Hack and Slash) 5: с мечом или топором атаки иногда дают лишний удар. С хорошим кинжалом Icy Veins советует присмотреться к Puncturing Wounds, у Wowhead для кинжала отдельный билд.',
                  'Here Icy Veins and Wowhead match fully, all 21 points. Both spend the Legacy points on Hack and Slash 5: with a sword or an axe your attacks sometimes grant an extra hit. With a good dagger, Icy Veins suggests looking at Puncturing Wounds, and Wowhead has a separate dagger build.',
                  'Тут Icy Veins і Wowhead збігаються повністю, в усіх 21 очку. Очки Legacy обидва віддають у Hack and Slash 5: з мечем або сокирою атаки іноді дають зайвий удар. З добрим кинджалом Icy Veins радить придивитися до Puncturing Wounds, у Wowhead для кинджала окремий білд.'),
            ]),
            ('steps', [
                {'t': t('Начало', 'Opening', 'Початок'),
                 'd': t('Внезапный удар с кинжалом, без кинжала — Гаррота (Icy Veins).', 'Ambush with a dagger, Garrote without one (Icy Veins).', 'Ambush із кинджалом, без кинджала — Garrote (Icy Veins).')},
                {'t': t('Шквал клинков', 'Blade Flurry', 'Blade Flurry'),
                 'd': t('С запасом энергии: против нескольких врагов и на боссе.', 'With plenty of Energy: against several enemies and on a boss.', 'Із запасом енергії: проти кількох ворогів і на босі.')},
                {'t': t('Ответный удар', 'Riposte', 'Riposte'),
                 'd': t('Каждый раз, когда доступен.', 'Every time it is available.', 'Щоразу, коли доступний.')},
                {'t': t('Коварный удар', 'Sinister Strike', 'Sinister Strike'),
                 'd': t('Основной удар; с кинжалом из-за спины — Удар в спину.', 'Your main strike; Backstab with a dagger from behind.', 'Основний удар; з кинджалом з-за спини — Backstab.')},
                {'t': t('Мясорубка', 'Slice and Dice', 'Slice and Dice'),
                 'd': t('Держать; обновлять в последний момент (Wowhead).', 'Keep it up; refresh it at the last moment (Wowhead).', 'Тримати; оновлювати в останню мить (Wowhead).')},
                {'t': t('Потрошение', 'Eviscerate', 'Eviscerate'),
                 'd': t('Тратить лишние приёмы серии.', 'Spend spare combo points.', 'Витрачати зайві прийоми серії.')},
            ]),
            ('tip', t('В Forever приёмы серии остаются на цели, даже если вы переключились на другую, но перенести их нельзя (Icy Veins). Если цель вот-вот умрёт, Wowhead советует потратить приёмы серии на Мясорубку — она перейдёт на следующего врага.',
                      'In Forever, combo points stay on a target even if you switch to another one, but you cannot transfer them (Icy Veins). If the target is about to die, Wowhead suggests spending them on Slice and Dice, which carries over to the next enemy.',
                      'У Forever прийоми серії лишаються на цілі, навіть якщо ви переключилися на іншу, але перенести їх не можна (Icy Veins). Якщо ціль ось-ось загине, Wowhead радить витратити прийоми серії на Slice and Dice — він перейде на наступного ворога.')),
        ]},
        {'id': 'subtlety', 'title': t('Скрытность: урон', 'Subtlety: damage', 'Непомітність: шкода'), 'blocks': [
            ('text', [
                t('Скрытность в тир-листе беты — C для подземелий: это ветка для PvP. На 30 уровне есть Кровоизлияние: удар без требования стоять сзади, после которого Рваная рана на 15 секунд сильнее на 15%. Оно становится основным ударом, кроме Внезапного удара из незаметности.',
                  'On the beta tier list Subtlety is C for dungeons: it is a PvP tree. At level 30 it gets Hemorrhage, a strike with no need to stand behind the target that makes Rupture deal 15% more damage for 15 seconds. It becomes your main strike, except for Ambush from Stealth.',
                  'Непомітність у тір-листі бети — C для підземель: це гілка для PvP. На 30 рівні є Hemorrhage: удар без вимоги стояти позаду, після якого Rupture на 15 секунд сильніший на 15%. Він стає основним ударом, крім Ambush з невидимості.'),
            ]),
            ('table', {'head': H_TAL, 'rows': [
                [t('Умысел (Premeditation)', 'Premeditation', 'Premeditation'), '1', t('2 приёма серии перед боем', '2 combo points before the fight', '2 прийоми серії перед боєм')],
                [t('Кровоизлияние (Hemorrhage)', 'Hemorrhage', 'Hemorrhage'), '1', t('Основной удар, усиливает Рваную рану', 'Your main strike; boosts Rupture', 'Основний удар, посилює Rupture')],
                [t('Выучка (Setup)', 'Setup', 'Setup'), '3', t('Приём серии после уклонения', 'A combo point after a dodge', 'Прийом серії після ухилення')],
                [t('Зазубренные клинки (Serrated Blades)', 'Serrated Blades', 'Serrated Blades'), '3', t('Часть брони цели не учитывается, Рваная рана сильнее', 'Ignores part of the target’s armor; stronger Rupture', 'Частина броні цілі не враховується, Rupture сильніший')],
                [t('Инициатива (Initiative)', 'Initiative', 'Initiative'), '3', t('Лишний приём серии от Внезапного удара, Гарроты и Подлого трюка', 'An extra combo point from Ambush, Garrote and Cheap Shot', 'Зайвий прийом серії від Ambush, Garrote і Cheap Shot')],
                [t('Правильный момент (Opportunity)', 'Opportunity', 'Opportunity'), '2', t('Урон Удара в спину, Гарроты, Внезапного удара и Расправы', 'Backstab, Garrote, Ambush and Mutilate damage', 'Шкода Backstab, Garrote, Ambush і Mutilate')],
            ]}),
            ('text', [
                t('Сходятся Icy Veins и Wowhead; Камуфляж (Camouflage) берут оба, но Icy Veins 4 очка, Wowhead 1. Wowhead называет обязательными Правильный момент, Инициативу, Умысел, Зазубренные клинки и Кровоизлияние, остальное — по вкусу. Icy Veins добирает Улучшенный внезапный удар (Improved Ambush) и Призрачный удар (Ghostly Strike), Wowhead — Неуловимость (Elusiveness), Dirty Tricks и [[Мастера маскировки|Master of Deception]]. С очками Legacy оба берут [[Подготовку|Preparation]]: она сбрасывает откаты, то есть даёт второе Исчезновение.',
                  'Icy Veins and Wowhead agree; both take Camouflage, but Icy Veins puts 4 points into it and Wowhead 1. Wowhead calls Opportunity, Initiative, Premeditation, Serrated Blades and Hemorrhage mandatory and the rest a matter of taste. Icy Veins adds Improved Ambush and Ghostly Strike, Wowhead adds Elusiveness, Dirty Tricks and Master of Deception. With Legacy points both take Preparation: it resets your cooldowns, which means a second Vanish.',
                  'Сходяться Icy Veins і Wowhead; Camouflage беруть обидва, але Icy Veins 4 очки, Wowhead 1. Wowhead називає обов’язковими Opportunity, Initiative, Premeditation, Serrated Blades і Hemorrhage, решту — на смак. Icy Veins добирає Improved Ambush і Ghostly Strike, Wowhead — Elusiveness, Dirty Tricks і Master of Deception. З очками Legacy обидва беруть Preparation: вона скидає відкати, тобто дає другий Vanish.'),
            ]),
            ('steps', [
                {'t': t('Начало', 'Opening', 'Початок'),
                 'd': t('Гаррота или Внезапный удар из незаметности.', 'Garrote or Ambush from Stealth.', 'Garrote або Ambush з невидимості.')},
                {'t': t('Кровоизлияние', 'Hemorrhage', 'Hemorrhage'),
                 'd': t('Основной удар.', 'Your main strike.', 'Основний удар.')},
                {'t': t('Мясорубка', 'Slice and Dice', 'Slice and Dice'),
                 'd': t('Держать.', 'Keep it up.', 'Тримати.')},
                {'t': t('Рваная рана', 'Rupture', 'Rupture'),
                 'd': t('По крепкой цели, которая проживёт всё время раны.', 'On a sturdy target that will live through its full duration.', 'По міцній цілі, яка проживе весь час рани.')},
                {'t': t('Потрошение', 'Eviscerate', 'Eviscerate'),
                 'd': t('Тратить лишние приёмы серии.', 'Spend spare combo points.', 'Витрачати зайві прийоми серії.')},
                {'t': t('Враг ушёл на вас', 'An enemy turns to you', 'Ворог пішов на вас'),
                 'd': t('Ускользание или Исчезновение (Icy Veins).', 'Evasion or Vanish (Icy Veins).', 'Evasion або Vanish (Icy Veins).')},
            ]),
            ('tip', t('Для подземелий тир-лист беты советует Ликвидацию или Бой. Удар в спину в Скрытности требует и Кровоизлияния, и Puncturing Wounds, а на 30 уровне очков на оба не хватает (Wowhead).',
                      'For dungeons the beta tier list points to Assassination or Combat. A Subtlety Backstab build needs both Hemorrhage and Puncturing Wounds, and at level 30 there are not enough points for both (Wowhead).',
                      'Для підземель тір-лист бети радить Ліквідацію або Бій. Backstab у Непомітності потребує і Hemorrhage, і Puncturing Wounds, а на 30 рівні очок на обидва не вистачає (Wowhead).')),
        ]},
        {'id': 'faq', 'title': FAQ_T, 'blocks': [
            ('faq', [
                {'id': 'q1', 'q': t('Какой спек разбойника лучший для подземелий?', 'Which Rogue spec is best for dungeons?', 'Яка спеціалізація розбійника найкраща для підземель?'),
                 'a': [t('В тир-листе беты Ликвидация — A, Бой — A* (у RankedBoost B), Скрытность — C.', 'On the beta tier list Assassination is A, Combat is A* (B at RankedBoost), Subtlety is C.', 'У тір-листі бети Ліквідація — A, Бій — A* (у RankedBoost B), Непомітність — C.')]},
                {'id': 'q2', 'q': t('Нужны ли кинжалы для Ликвидации?', 'Does Assassination need daggers?', 'Чи потрібні кинджали для Ліквідації?'),
                 'a': [t('Да: Расправа требует два кинжала (Icy Veins). Бою подходят и мечи, и топоры; с кинжалом он бьёт Ударом в спину.', 'Yes: Mutilate needs two daggers (Icy Veins). Combat works with swords and axes too; with a dagger it uses Backstab.', 'Так: Mutilate потребує двох кинджалів (Icy Veins). Бою підходять і мечі, і сокири; з кинджалом він б’є Backstab.')]},
                {'id': 'q3', 'q': t('Какие яды ставить?', 'Which poisons should I use?', 'Які отрути ставити?'),
                 'a': [t('Icy Veins перед боем ставит Быстродействующий яд на оба оружия. Смертельный яд Ликвидация получает на 30 уровне (Wowhead).', 'Icy Veins puts Instant Poison on both weapons before a pull. Assassination gets Deadly Poison at level 30 (Wowhead).', 'Icy Veins перед боєм ставить Instant Poison на обидві зброї. Deadly Poison Ліквідація отримує на 30 рівні (Wowhead).')]},
                {'id': 'q4', 'q': WHEN_Q, 'a': [WHEN_A]},
            ]),
        ]},
        {'id': 'related', 'title': t('Смотрите также', 'See also', 'Дивіться також'), 'blocks': [
            ('tiles', _related('rogue', [t('Разбойник', 'Rogue', 'Розбійник'), t('Прокачка Разбойника', 'Rogue leveling', 'Прокачування Розбійника')])),
        ]},
    ],
})

# ---------- priest ----------

SPEC_BUILDS.append({
    'slug': 'builds-priest', 'art': 'priest', 'hero': 'hero_leveling', 'hub': False,
    'title': t('Билды Жреца', 'Priest Builds', 'Білди Жреця'),
    'lead': t('Таланты, приоритет и характеристики Послушания, Света и Темной магии. Здесь только то, в чём сходятся Icy Veins и Wowhead.',
              'Talents, priorities and stats for Discipline, Holy and Shadow. This page shows only what Icy Veins and Wowhead agree on.',
              'Таланти, пріоритет і характеристики Послуху, Світла й Темряви. Тут лише те, у чому сходяться Icy Veins і Wowhead.'),
    'tile': t('Послушание, Свет, Темная магия: таланты и приоритет', 'Discipline, Holy, Shadow: talents and priorities', 'Послух, Світло, Темрява: таланти й пріоритет'),
    'pills': [BETA, SPECS3, LATER],
    'sources': [
        ('Icy Veins: Discipline Priest Guide', 'https://www.icy-veins.com/wow-forever/discipline-priest-healer-pve-guide'),
        ('Icy Veins: Holy Priest Guide', 'https://www.icy-veins.com/wow-forever/holy-priest-healer-pve-guide'),
        ('Icy Veins: Shadow Priest Guide', 'https://www.icy-veins.com/wow-forever/shadow-priest-ranged-dps-pve-guide'),
        ('Icy Veins: Priest Talent Calculator', 'https://www.icy-veins.com/wow-forever/priest-talent-calculator'),
        ('Wowhead: Level 30 Discipline Priest', 'https://www.wowhead.com/forever/guide/classes/priest/discipline/level-30-healer-overview'),
        ('Wowhead: Level 30 Holy Priest', 'https://www.wowhead.com/forever/guide/classes/priest/holy/level-30-healer-overview'),
        ('Wowhead: Level 30 Shadow Priest', 'https://www.wowhead.com/forever/guide/classes/priest/shadow/level-30-dps-overview'),
        ('Wowhead: Priest Talent Calculator', 'https://www.wowhead.com/forever/talent-calc/priest'),
    ],
    'sections': [
        {'id': 'roles', 'title': t('Спеки и роли', 'Specs and roles', 'Спеціалізації та ролі'), 'blocks': [
            ('table', {'head': H_ROLES, 'rows': [
                [t('Послушание', 'Discipline', 'Послух'), HEALER, 'S',
                 t('Щиты и Исповедь', 'Shields and Penance', 'Щити й Penance')],
                [t('Свет', 'Holy', 'Світло'), HEALER, 'B*',
                 t('Лечение по площади, раскрывается к 60', 'Area healing; comes into its own by 60', 'Лікування по площі, розкривається до 60')],
                [t('Темная магия', 'Shadow', 'Темрява'), DPS, 'B*',
                 t('Периодический урон, Объятия вампира лечат группу', 'Damage over time; Vampiric Embrace heals the group', 'Періодична шкода, Vampiric Embrace лікує групу')],
            ]}),
            ('text', [ROLES_NOTE, t('B* у Света: Noobtoboss и gamer-guides называют его сильным рейдовым лекарем. B* у Темной магии: RankedBoost ставит её в A.', 'B* for Holy: Noobtoboss and gamer-guides call it a strong raid healer. B* for Shadow: RankedBoost puts it in A.', 'B* у Світла: Noobtoboss і gamer-guides називають його сильним рейдовим цілителем. B* у Темряви: RankedBoost ставить її в A.')]),
        ]},
        {'id': 'discipline', 'title': t('Послушание: лекарь', 'Discipline: healer', 'Послух: цілитель'), 'blocks': [
            ('text', [
                t('Послушание — лучший лекарь беты: щиты и Исповедь, которая лечит союзника или бьёт врага. Исповедь требует 20 очков в ветке. На 30 уровне у тренера Молитва исцеления и Божественный дух — второе усиление жреца для группы (Wowhead).',
                  'Discipline is the best healer of the beta: shields and Penance, which heals an ally or hits an enemy. Penance needs 20 points in the tree. At level 30 the trainer has Prayer of Healing and Divine Spirit, the Priest’s second group buff (Wowhead).',
                  'Послух — найкращий цілитель бети: щити й Penance, що лікує союзника або б’є ворога. Penance потребує 20 очок у гілці. На 30 рівні в тренера Prayer of Healing і Divine Spirit — друге посилення жерця для групи (Wowhead).'),
            ]),
            ('table', {'head': H_TAL, 'rows': [
                [t('Специализация на жезлах (Wand Specialization)', 'Wand Specialization', 'Wand Specialization'), '2', t('Урон жезлом: им добивают без маны', 'Wand damage: you finish enemies with it for no mana', 'Шкода жезлом: ним добивають без мани')],
                ['Power in Light', '3', t('Кара и Исповедь сильнее по цели со Священным огнём или Словом Тьмы: Болью', 'Stronger Smite and Penance on a target with Holy Fire or Shadow Word: Pain', 'Сильніші Smite і Penance по цілі з Holy Fire або Shadow Word: Pain')],
                [t('Улучшенное Слово силы: Щит (Improved Power Word: Shield)', 'Improved Power Word: Shield', 'Improved Power Word: Shield'), '3', t('Щит поглощает больше', 'The shield absorbs more', 'Щит поглинає більше')],
            ]}),
            ('text', [
                t('Это общее у Icy Veins и Wowhead. Оба берут [[Медитацию|Meditation]] — часть восполнения маны идёт во время чтения — и [[Силу мысли|Mental Strength]], но с разным числом очков. Главное расхождение — Исповедь: Wowhead берёт её уже на 30 уровне, а Icy Veins — только с пятью очками перка Legacy Talented, а на 21 очко отдаёт 5 в Захват духа (Spirit Tap) из ветки Темной магии. Встроенный билд гайда Wowhead показывает только 15 очков, поэтому его раскладку сверяли по тексту.',
                  'This is what Icy Veins and Wowhead share. Both take Meditation, which keeps part of your mana regeneration going while casting, and Mental Strength, but with a different number of points. The main difference is Penance: Wowhead takes it at level 30 already, while Icy Veins takes it only with the five points of the Legacy Talented perk and spends 5 of its 21 points on Spirit Tap from the Shadow tree. The embedded build in the Wowhead guide shows only 15 points, so its layout was checked against the text.',
                  'Це спільне в Icy Veins і Wowhead. Обидва беруть Meditation — частина відновлення мани триває під час читання — і Mental Strength, але з різною кількістю очок. Головна розбіжність — Penance: Wowhead бере його вже на 30 рівні, а Icy Veins — лише з п’ятьма очками перка Legacy Talented, а з 21 очка віддає 5 у Spirit Tap з гілки Темряви. Вбудований білд гайда Wowhead показує лише 15 очок, тож його розкладку звіряли за текстом.'),
            ]),
            ('steps', [
                {'t': t('Перед боем', 'Before the pull', 'Перед боєм'),
                 'd': t('Слово силы: Щит на танка. Не на воина и друида: щит может отнять у них Ярость (Wowhead; на бете это могут изменить).', 'Power Word: Shield on the tank. Not on a Warrior or Druid: the shield can starve them of Rage (Wowhead; this may change on the beta).', 'Power Word: Shield на танка. Не на воїна й друїда: щит може забрати в них Лють (Wowhead; у беті це можуть змінити).')},
                {'t': t('Обновление', 'Renew', 'Renew'),
                 'd': t('Держать на танке.', 'Keep it on the tank.', 'Тримати на танку.')},
                {'t': t('Исцеление', 'Heal', 'Heal'),
                 'd': t('Основное лечение.', 'Your main heal.', 'Основне лікування.')},
                {'t': t('Быстрое исцеление', 'Flash Heal', 'Flash Heal'),
                 'd': t('Только в опасный момент: оно дорогое.', 'Only in a dangerous moment: it is expensive.', 'Лише в небезпечний момент: воно дороге.')},
                {'t': t('Молитва исцеления', 'Prayer of Healing', 'Prayer of Healing'),
                 'd': t('Когда ранена вся группа.', 'When the whole group is hurt.', 'Коли поранена вся група.')},
                {'t': t('Свободная минута', 'A quiet moment', 'Вільна хвилина'),
                 'd': t('Жезл по врагам: мана восстанавливается.', 'Wand the enemies while your mana comes back.', 'Жезл по ворогах: мана відновлюється.')},
            ]),
            ('tip', t('Характеристики по Icy Veins: сила лечения первой, затем мана раз в 5 секунд, дух, интеллект, крит. В Forever мана восполняется, только если вы 5 секунд не читали заклинаний; Медитация оставляет часть восполнения и во время чтения.',
                      'Stats according to Icy Veins: healing power first, then mana per 5 seconds, Spirit, Intellect, crit. In Forever, mana regenerates only after 5 seconds without casting; Meditation keeps part of it going while you cast.',
                      'Характеристики за Icy Veins: сила лікування першою, потім мана раз на 5 секунд, дух, інтелект, крит. У Forever мана відновлюється, лише якщо ви 5 секунд не читали заклинань; Meditation лишає частину відновлення й під час читання.')),
        ]},
        {'id': 'holy', 'title': t('Свет: лекарь', 'Holy: healer', 'Світло: цілитель'), 'blocks': [
            ('text', [
                t('Свет раскрывается к 60: Молитва восстановления — последний талант ветки, ей нужно 31 очко. На 30 уровне у тренера Молитва исцеления: в Forever она достаёт союзников в 40 м от цели, а не в 30. Binding Heal (15 очков в ветке) лечит цель и вас одним заклинанием (Wowhead).',
                  'Holy comes into its own by 60: Prayer of Mending is the last talent of the tree and needs 31 points. At level 30 the trainer has Prayer of Healing: in Forever it reaches allies within 40 yards of the target instead of 30. Binding Heal (15 points in the tree) heals the target and you with one spell (Wowhead).',
                  'Світло розкривається до 60: Prayer of Mending — останній талант гілки, йому потрібне 31 очко. На 30 рівні в тренера Prayer of Healing: у Forever вона дістає союзників за 40 ярдів від цілі, а не за 30. Binding Heal (15 очок у гілці) лікує ціль і вас одним заклинанням (Wowhead).'),
            ]),
            ('table', {'head': H_TAL, 'rows': [
                [t('Улучшенное обновление (Improved Renew)', 'Improved Renew', 'Improved Renew'), '3', t('Обновление лечит сильнее', 'Stronger Renew', 'Renew лікує сильніше')],
                [t('Божественное неистовство (Divine Fury)', 'Divine Fury', 'Divine Fury'), '5', t('Кара, Священный огонь и Исцеление читаются быстрее', 'Faster Smite, Holy Fire and Heal', 'Smite, Holy Fire і Heal читаються швидше')],
                [t('Кольцо Света (Holy Nova)', 'Holy Nova', 'Holy Nova'), '1', t('Мгновенный урон и лечение вокруг вас без угрозы', 'Instant damage and healing around you with no threat', 'Миттєва шкода й лікування навколо вас без загрози')],
                [t('Специализация на магии Света (Holy Specialization)', 'Holy Specialization', 'Holy Specialization'), '2', t('Крит заклинаний Света', 'Holy spell crit', 'Крит заклинань Світла')],
            ]}),
            ('text', [
                t('Это общее у Icy Veins и Wowhead, дальше пути разные. Wowhead ведёт все 21 очко в Свет до [[Духа воздаяния|Spirit of Redemption]]: Специализация на магии Света до 5, Вдохновение (Inspiration) 3, Предел сил Света (Holy Reach) 2 и Binding Heal. Icy Veins собирает билд для прокачки: Специализация на жезлах 2, Захват духа 5 и Twilight Focus 3 — заклинания реже сбиваются уроном. С очками Legacy Icy Veins для групп снимает жезлы и берёт Духовное направление (Spiritual Guidance), Wowhead — Litany of Light: мана за смену лечащих заклинаний.',
                  'This is what Icy Veins and Wowhead share; after that their paths split. Wowhead takes all 21 points down the Holy tree to Spirit of Redemption: Holy Specialization to 5, Inspiration 3, Holy Reach 2 and Binding Heal. Icy Veins builds for leveling: Wand Specialization 2, Spirit Tap 5 and Twilight Focus 3, so damage interrupts your casts less often. With Legacy points, Icy Veins drops the wand points for group healing and takes Spiritual Guidance, Wowhead takes Litany of Light: mana back for switching between heals.',
                  'Це спільне в Icy Veins і Wowhead, далі шляхи різні. Wowhead веде всі 21 очко у Світло до Spirit of Redemption: Holy Specialization до 5, Inspiration 3, Holy Reach 2 і Binding Heal. Icy Veins збирає білд для прокачування: Wand Specialization 2, Spirit Tap 5 і Twilight Focus 3 — заклинання рідше збиваються шкодою. З очками Legacy Icy Veins для груп знімає жезли й бере Spiritual Guidance, Wowhead — Litany of Light: мана за зміну лікувальних заклинань.'),
            ]),
            ('steps', [
                {'t': t('Обновление', 'Renew', 'Renew'),
                 'd': t('Держать на танке.', 'Keep it on the tank.', 'Тримати на танку.')},
                {'t': t('Исцеление', 'Heal', 'Heal'),
                 'd': t('Основное лечение.', 'Your main heal.', 'Основне лікування.')},
                {'t': t('Быстрое исцеление', 'Flash Heal', 'Flash Heal'),
                 'd': t('Если союзник вот-вот умрёт.', 'When an ally is about to die.', 'Якщо союзник ось-ось загине.')},
                {'t': 'Binding Heal',
                 'd': t('Когда ранены и вы, и танк.', 'When both you and the tank are hurt.', 'Коли поранені і ви, і танк.')},
                {'t': t('Молитва исцеления', 'Prayer of Healing', 'Prayer of Healing'),
                 'd': t('Только когда ранена почти вся группа: 3 секунды чтения и много маны.', 'Only when most of the group is low: a 3-second cast that costs a lot of mana.', 'Лише коли поранена майже вся група: 3 секунди читання й багато мани.')},
                {'t': t('Кольцо Света', 'Holy Nova', 'Holy Nova'),
                 'd': t('При срабатывании Опаляющего света, если никто не в опасности (Icy Veins).', 'When Searing Light procs and nobody is in danger (Icy Veins).', 'Коли спрацював Searing Light і ніхто не в небезпеці (Icy Veins).')},
            ]),
            ('tip', t('Характеристики по Icy Veins те же, что у Послушания: сила лечения, мана раз в 5 секунд, дух, интеллект, крит. Дух воздаяния в Forever длится 15 секунд вместо 10 (Wowhead).',
                      'Stats according to Icy Veins are the same as for Discipline: healing power, mana per 5 seconds, Spirit, Intellect, crit. In Forever, Spirit of Redemption lasts 15 seconds instead of 10 (Wowhead).',
                      'Характеристики за Icy Veins ті самі, що в Послуху: сила лікування, мана раз на 5 секунд, дух, інтелект, крит. Spirit of Redemption у Forever триває 15 секунд замість 10 (Wowhead).')),
        ]},
        {'id': 'shadow', 'title': t('Темная магия: урон', 'Shadow: damage', 'Темрява: шкода'), 'blocks': [
            ('text', [
                t('Облик Тьмы откроется только на 40 уровне, поэтому на 30 урон дают Слово Тьмы: Боль, Взрыв разума и жезл. Объятия вампира 30 секунд лечат группу от вашего урона Тьмой и запускают Захват духа — главный источник маны. Захват духа срабатывает только от убийства, поэтому добивайте сами (Wowhead).',
                  'Shadowform only unlocks at level 40, so at 30 your damage comes from Shadow Word: Pain, Mind Blast and your wand. Vampiric Embrace heals the group from your Shadow damage for 30 seconds and triggers Spirit Tap, your main source of mana. Spirit Tap only triggers on a kill, so land the killing blows yourself (Wowhead).',
                  'Shadowform відкриється лише на 40 рівні, тож на 30 шкоду дають Shadow Word: Pain, Mind Blast і жезл. Vampiric Embrace 30 секунд лікує групу від вашої шкоди Темрявою й запускає Spirit Tap — головне джерело мани. Spirit Tap спрацьовує лише від вбивства, тож добивайте самі (Wowhead).'),
            ]),
            ('table', {'head': H_TAL, 'rows': [
                [t('Специализация на жезлах (Wand Specialization)', 'Wand Specialization', 'Wand Specialization'), '2', t('Урон жезлом', 'Wand damage', 'Шкода жезлом')],
                [t('Захват духа (Spirit Tap)', 'Spirit Tap', 'Spirit Tap'), '5', t('Дух после убийства; часть маны восполняется в бою', 'Spirit after a kill; part of your mana regenerates in combat', 'Дух після вбивства; частина мани відновлюється в бою')],
                [t('Улучшенное слово Тьмы: Боль (Improved Shadow Word: Pain)', 'Improved Shadow Word: Pain', 'Improved Shadow Word: Pain'), '2', t('Слово Тьмы: Боль длится дольше', 'Longer Shadow Word: Pain', 'Shadow Word: Pain триває довше')],
                [t('Пытка разума (Mind Flay)', 'Mind Flay', 'Mind Flay'), '1', t('Урон и замедление на 50%', 'Damage and a 50% slow', 'Шкода й сповільнення на 50%')],
                ['Improved Mind Flay', '2', t('Каждый тик Пытки разума сильнее предыдущего', 'Each Mind Flay tick hits harder than the last', 'Кожен тік Mind Flay сильніший за попередній')],
                [t('Объятия вампира (Vampiric Embrace)', 'Vampiric Embrace', 'Vampiric Embrace'), '1', t('Лечение группы от урона Тьмой', 'Group healing from your Shadow damage', 'Лікування групи від шкоди Темрявою')],
            ]}),
            ('text', [
                t('Это общее у Icy Veins и Wowhead; Improved Mind Flay у Wowhead посчитан по тексту: встроенный билд гайда показывает только 14 очков. Расходятся: Icy Veins берёт Улучшенный взрыв разума (Improved Mind Blast) 4, Предел Тьмы (Shadow Reach) и Dark Inspiration 3, Wowhead — Средоточие Тьмы (Shadow Focus) 5 и Плетение Тьмы (Shadow Weaving) 3. С очками Legacy оба берут Devouring Contagion 2: Всепожирающая чума дешевле и перескакивает на соседних врагов, если цель умерла.',
                  'This is what Icy Veins and Wowhead share; Wowhead’s Improved Mind Flay points come from its text, since the guide’s embedded build shows only 14 points. They differ: Icy Veins takes Improved Mind Blast 4, Shadow Reach and Dark Inspiration 3, Wowhead takes Shadow Focus 5 and Shadow Weaving 3. With Legacy points both take Devouring Contagion 2: a cheaper Devouring Plague that jumps to nearby enemies when the target dies.',
                  'Це спільне в Icy Veins і Wowhead; Improved Mind Flay у Wowhead пораховано за текстом: вбудований білд гайда показує лише 14 очок. Розходяться: Icy Veins бере Improved Mind Blast 4, Shadow Reach і Dark Inspiration 3, Wowhead — Shadow Focus 5 і Shadow Weaving 3. З очками Legacy обидва беруть Devouring Contagion 2: Devouring Plague дешевша й перескакує на сусідніх ворогів, якщо ціль загинула.'),
            ]),
            ('steps', [
                {'t': t('Перед боем', 'Before the pull', 'Перед боєм'),
                 'd': t('Слово силы: Стойкость, Внутренний огонь, Слово силы: Щит.', 'Power Word: Fortitude, Inner Fire, Power Word: Shield.', 'Power Word: Fortitude, Inner Fire, Power Word: Shield.')},
                {'t': t('Взрыв разума', 'Mind Blast', 'Mind Blast'),
                 'd': t('Начать бой.', 'To open the fight.', 'Почати бій.')},
                {'t': t('Слово Тьмы: Боль', 'Shadow Word: Pain', 'Shadow Word: Pain'),
                 'd': t('Затем Всепожирающая чума, если хватает маны.', 'Then Devouring Plague if you have the mana.', 'Потім Devouring Plague, якщо вистачає мани.')},
                {'t': t('Пытка разума', 'Mind Flay', 'Mind Flay'),
                 'd': t('Только при лишней мане: она сбрасывает пятисекундный отсчёт восполнения.', 'Only with spare mana: it resets the five-second regeneration timer.', 'Лише за зайвої мани: вона скидає п’ятисекундний відлік відновлення.')},
                {'t': t('Жезл', 'Wand', 'Жезл'),
                 'd': t('Добить цель.', 'To finish the target.', 'Добити ціль.')},
                {'t': t('Группа', 'Group of enemies', 'Група'),
                 'd': t('Слово Тьмы: Боль на всех врагах.', 'Shadow Word: Pain on every enemy.', 'Shadow Word: Pain на всіх ворогах.')},
            ]),
            ('tip', t('Характеристики по Icy Veins: сила заклинаний, крит, меткость, интеллект. В Forever периодический урон не запоминает характеристики на момент наложения, а пересчитывается, когда они меняются (Icy Veins).',
                      'Stats according to Icy Veins: spell power, crit, hit, Intellect. In Forever, damage over time does not snapshot your stats when applied: it updates as they change (Icy Veins).',
                      'Характеристики за Icy Veins: сила заклинань, крит, влучність, інтелект. У Forever періодична шкода не запам’ятовує характеристики на момент накладання, а перераховується, коли вони змінюються (Icy Veins).')),
        ]},
        {'id': 'faq', 'title': FAQ_T, 'blocks': [
            ('faq', [
                {'id': 'q1', 'q': t('Какой спек жреца лучший лекарь?', 'Which Priest spec is the best healer?', 'Яка спеціалізація жерця найкращий цілитель?'),
                 'a': [t('Послушание: в тир-листе беты оно в S. Свет — B*, он раскрывается к 60.', 'Discipline: it is in tier S on the beta tier list. Holy is B* and comes into its own by 60.', 'Послух: у тір-листі бети він в S. Світло — B*, воно розкривається до 60.')]},
                {'id': 'q2', 'q': t('Когда у жреца Исповедь?', 'When does a Priest get Penance?', 'Коли в жерця Penance?'),
                 'a': [t('Исповедь требует 20 очков в ветке Послушания, то есть 21-е очко на 30 уровне. Wowhead берёт её на 30, Icy Veins — с очками перка Legacy Talented.', 'Penance needs 20 points in the Discipline tree, so it is your 21st point at level 30. Wowhead takes it at 30, Icy Veins with the Legacy Talented points.', 'Penance потребує 20 очок у гілці Послуху, тобто 21-ше очко на 30 рівні. Wowhead бере його на 30, Icy Veins — з очками перка Legacy Talented.')]},
                {'id': 'q3', 'q': t('Можно ли качаться Темной магией?', 'Can I level as Shadow?', 'Чи можна качатися Темрявою?'),
                 'a': [t('Да, оба источника дают билд Темной магии для прокачки: жезл, Захват духа и Слово Тьмы: Боль. Облик Тьмы откроется только на 40 уровне.', 'Yes, both sources give a Shadow leveling build: wand, Spirit Tap and Shadow Word: Pain. Shadowform only unlocks at level 40.', 'Так, обидва джерела дають білд Темряви для прокачування: жезл, Spirit Tap і Shadow Word: Pain. Shadowform відкриється лише на 40 рівні.')]},
                {'id': 'q4', 'q': WHEN_Q, 'a': [WHEN_A]},
            ]),
        ]},
        {'id': 'related', 'title': t('Смотрите также', 'See also', 'Дивіться також'), 'blocks': [
            ('tiles', _related('priest', [t('Жрец', 'Priest', 'Жрець'), t('Прокачка Жреца', 'Priest leveling', 'Прокачування Жреця')])),
        ]},
    ],
})

# ---------- shaman ----------

SPEC_BUILDS.append({
    'slug': 'builds-shaman', 'art': 'shaman', 'hero': 'hero_leveling', 'hub': False,
    'title': t('Билды Шамана', 'Shaman Builds', 'Білди Шамана'),
    'lead': t('Таланты, приоритет и характеристики Стихий, Совершенствования и Исцеления. Здесь только то, в чём сходятся Icy Veins и Wowhead.',
              'Talents, priorities and stats for Elemental, Enhancement and Restoration. This page shows only what Icy Veins and Wowhead agree on.',
              'Таланти, пріоритет і характеристики Стихій, Вдосконалення та Зцілення. Тут лише те, у чому сходяться Icy Veins і Wowhead.'),
    'tile': t('Стихии, Совершенствование, Исцеление: таланты и приоритет', 'Elemental, Enhancement, Restoration: talents and priorities', 'Стихії, Вдосконалення, Зцілення: таланти й пріоритет'),
    'pills': [BETA, SPECS3, LATER],
    'sources': [
        ('Icy Veins: Elemental Shaman Guide', 'https://www.icy-veins.com/wow-forever/elemental-shaman-ranged-dps-pve-guide'),
        ('Icy Veins: Enhancement Shaman Guide', 'https://www.icy-veins.com/wow-forever/enhancement-shaman-melee-dps-pve-guide'),
        ('Icy Veins: Restoration Shaman Guide', 'https://www.icy-veins.com/wow-forever/restoration-shaman-healer-pve-guide'),
        ('Icy Veins: Shaman Talent Calculator', 'https://www.icy-veins.com/wow-forever/shaman-talent-calculator'),
        ('Wowhead: Level 30 Elemental Shaman', 'https://www.wowhead.com/forever/guide/classes/shaman/elemental/level-30-dps-overview'),
        ('Wowhead: Level 30 Enhancement Shaman', 'https://www.wowhead.com/forever/guide/classes/shaman/enhancement/level-30-dps-overview'),
        ('Wowhead: Level 30 Restoration Shaman', 'https://www.wowhead.com/forever/guide/classes/shaman/restoration/level-30-healer-overview'),
        ('Wowhead: Shaman Talent Calculator', 'https://www.wowhead.com/forever/talent-calc/shaman'),
    ],
    'sections': [
        {'id': 'roles', 'title': t('Спеки и роли', 'Specs and roles', 'Спеціалізації та ролі'), 'blocks': [
            ('table', {'head': H_ROLES, 'rows': [
                [t('Стихии', 'Elemental', 'Стихії'), DPS, 'B*',
                 t('Выброс лавы, урон по площади Кольцом огня', 'Lava Burst; area damage with Fire Nova', 'Lava Burst, шкода по площі через Fire Nova')],
                [t('Совершенствование', 'Enhancement', 'Вдосконалення'), DPS, 'A*',
                 t('Удар бури и Оружие неистовства ветра', 'Stormstrike and Windfury Weapon', 'Stormstrike і Windfury Weapon')],
                [t('Исцеление', 'Restoration', 'Зцілення'), HEALER, 'S',
                 t('Волна исцеления, Тотем прилива маны', 'Healing Wave, Mana Tide Totem', 'Healing Wave, Mana Tide Totem')],
            ]}),
            ('text', [ROLES_NOTE, t('A* у Совершенствования: RankedBoost ставит его в B. B* у Стихий: RankedBoost ставит их в A.', 'A* for Enhancement: RankedBoost puts it in B. B* for Elemental: RankedBoost puts it in A.', 'A* у Вдосконалення: RankedBoost ставить його в B. B* у Стихій: RankedBoost ставить їх в A.')]),
        ]},
        {'id': 'elemental', 'title': t('Стихии: урон', 'Elemental: damage', 'Стихії: шкода'), 'blocks': [
            ('text', [
                t('В Forever у заклинаний меньше базового урона, а сила заклинаний есть на снаряжении из подземелий и профессий: без него Стихии до 40 уровня слабы (Wowhead). Сильная сторона спека — урон по площади. Кольцо огня теперь заклинание: оно взрывается вокруг вашего тотема огня (Icy Veins).',
                  'In Forever, spells have lower base damage, while spell power comes from dungeon and profession gear: without it Elemental is weak before level 40 (Wowhead). The spec’s strength is area damage. Fire Nova is now a spell that explodes around your active Fire Totem (Icy Veins).',
                  'У Forever у заклинань менша базова шкода, а сила заклинань є на спорядженні з підземель і професій: без нього Стихії до 40 рівня слабкі (Wowhead). Сильна сторона спеціалізації — шкода по площі. Fire Nova тепер заклинання: воно вибухає навколо вашого тотема вогню (Icy Veins).'),
            ]),
            ('table', {'head': H_TAL, 'rows': [
                [t('Сотрясение мозга (Concussion)', 'Concussion', 'Concussion'), '5', t('Урон Молнии, Цепной молнии и Земного шока', 'Lightning Bolt, Chain Lightning and Earth Shock damage', 'Шкода Lightning Bolt, Chain Lightning і Earth Shock')],
                ['Elemental Alacrity', '3', t('Молния, Цепная молния и Выброс лавы читаются быстрее', 'Faster Lightning Bolt, Chain Lightning and Lava Burst casts', 'Lightning Bolt, Chain Lightning і Lava Burst читаються швидше')],
                [t('Зов пламени (Call of Flame)', 'Call of Flame', 'Call of Flame'), '3', t('Урон тотемов огня, Огненного шока, Кольца огня и Выброса лавы', 'Fire Totem, Flame Shock, Fire Nova and Lava Burst damage', 'Шкода тотемів вогню, Flame Shock, Fire Nova і Lava Burst')],
                [t('Концентрация стихий (Elemental Focus)', 'Elemental Focus', 'Elemental Focus'), '1', t('Шанс, что следующее заклинание будет бесплатным', 'A chance for your next damage spell to be free', 'Шанс, що наступне заклинання буде безкоштовним')],
                [t('Око шторма (Eye of the Storm)', 'Eye of the Storm', 'Eye of the Storm'), '3', t('Молния и Выброс лавы реже сбиваются уроном', 'Damage pushes back Lightning Bolt and Lava Burst less often', 'Lightning Bolt і Lava Burst рідше збиваються шкодою')],
                [t('Выброс лавы (Lava Burst)', 'Lava Burst', 'Lava Burst'), '1', t('Сильнее по цели с Огненным шоком', 'Hits harder on a target with Flame Shock', 'Сильніший по цілі з Flame Shock')],
                [t('Конвекция (Convection)', 'Convection', 'Convection'), '3', t('Шоки, Молния и Выброс лавы дешевле', 'Cheaper shocks, Lightning Bolt and Lava Burst', 'Дешевші шоки, Lightning Bolt і Lava Burst')],
            ]}),
            ('text', [
                t('Это общее у Icy Veins и вкладки «Deep Elemental» в гайде Wowhead; Конвекцию Wowhead берёт 4. Расходятся последние очки: Icy Veins — Trial by Fire 2 (Кольцо огня чаще, Тотем магмы дольше), Wowhead — Earthbound. С очками Legacy оба добирают [[Электрическую перегрузку|Lightning Overload]] 3 и одно очко [[Неистовства стихий|Elemental Fury]]. Для прокачки Wowhead советует другой путь: 10 очков в Совершенствование и 11 в Исцеление ради Mindfulness и Водного щита — так меньше проблем с маной.',
                  'This is what Icy Veins and the “Deep Elemental” tab of the Wowhead guide share; Wowhead takes Convection to 4. The last points differ: Icy Veins takes Trial by Fire 2 (Fire Nova more often, a longer Magma Totem), Wowhead takes Earthbound. With Legacy points both add Lightning Overload 3 and one point in Elemental Fury. For leveling, Wowhead suggests another path: 10 points in Enhancement and 11 in Restoration for Mindfulness and Water Shield, which eases mana problems.',
                  'Це спільне в Icy Veins і вкладки «Deep Elemental» у гайді Wowhead; Convection Wowhead бере 4. Розходяться останні очки: Icy Veins — Trial by Fire 2 (Fire Nova частіше, Magma Totem довше), Wowhead — Earthbound. З очками Legacy обидва добирають Lightning Overload 3 і одне очко Elemental Fury. Для прокачування Wowhead радить інший шлях: 10 очок у Вдосконалення й 11 у Зцілення заради Mindfulness і Water Shield — так менше проблем із маною.'),
            ]),
            ('steps', [
                {'t': t('Перед боем', 'Before the pull', 'Перед боєм'),
                 'd': t('Тотемы через Зов Стихий, Опаляющий тотем последним; против группы — Тотем магмы.', 'Totems with Call of the Elements, Searing Totem last; Magma Totem against a group.', 'Тотеми через Call of the Elements, Searing Totem останнім; проти групи — Magma Totem.')},
                {'t': t('Молния', 'Lightning Bolt', 'Lightning Bolt'),
                 'd': t('Начать бой издалека.', 'To open from range.', 'Почати бій здалеку.')},
                {'t': t('Кольцо огня', 'Fire Nova', 'Fire Nova'),
                 'd': t('По откату против трёх врагов и больше.', 'On cooldown against three or more enemies.', 'По відкату проти трьох ворогів і більше.')},
                {'t': t('Огненный шок', 'Flame Shock', 'Flame Shock'),
                 'd': t('Сразу после; на долгой цели обновлять.', 'Right after; refresh it on a long-lived target.', 'Одразу після; на довгій цілі оновлювати.')},
                {'t': t('Выброс лавы', 'Lava Burst', 'Lava Burst'),
                 'd': t('По откату.', 'On cooldown.', 'По відкату.')},
                {'t': t('Молния', 'Lightning Bolt', 'Lightning Bolt'),
                 'd': t('Всё остальное время.', 'The rest of the time.', 'Увесь інший час.')},
            ]),
            ('tip', t('Держите тотемы-усиления вроде Тотема силы земли: в группе они дают больше, чем ещё одна Молния (Icy Veins). Характеристики по Icy Veins: сила заклинаний, крит, меткость, интеллект.',
                      'Keep buff totems such as Strength of Earth Totem down: in a group they are worth more than one more Lightning Bolt (Icy Veins). Stats according to Icy Veins: spell power, crit, hit, Intellect.',
                      'Тримайте тотеми-посилення на кшталт Strength of Earth Totem: у групі вони дають більше, ніж ще одна Lightning Bolt (Icy Veins). Характеристики за Icy Veins: сила заклинань, крит, влучність, інтелект.')),
        ]},
        {'id': 'enhancement', 'title': t('Совершенствование: урон', 'Enhancement: damage', 'Вдосконалення: шкода'), 'blocks': [
            ('text', [
                t('Совершенствование — основной спек шамана для прокачки: базовый урон заклинаний снижен, а урон держится на автоатаках и Оружии Камнедробителя (Wowhead). К 30 уровню есть Удар бури и Оружие неистовства ветра, но маны на них мало. Призрачный волк с талантом вызывается быстрее и работает в помещениях.',
                  'Enhancement is the Shaman’s main leveling spec: base spell damage is lower, and your damage rests on auto attacks and Rockbiter Weapon (Wowhead). By level 30 you have Stormstrike and Windfury Weapon, but little mana for them. With the talent, Ghost Wolf is faster to cast and works indoors.',
                  'Вдосконалення — основна спеціалізація шамана для прокачування: базова шкода заклинань знижена, а шкода тримається на автоатаках і Rockbiter Weapon (Wowhead). До 30 рівня є Stormstrike і Windfury Weapon, але мани на них мало. Ghost Wolf із талантом викликається швидше й працює в приміщеннях.'),
            ]),
            ('table', {'head': H_TAL, 'rows': [
                [t('Грохочущие удары (Thundering Strikes)', 'Thundering Strikes', 'Thundering Strikes'), '5', t('Шанс крита заклинаний и атак', 'Crit chance with spells and attacks', 'Шанс криту заклинань і атак')],
                [t('Гибкость разума (Mental Dexterity)', 'Mental Dexterity', 'Mental Dexterity'), '3', t('Сила атаки от интеллекта', 'Attack power from Intellect', 'Сила атаки від інтелекту')],
                [t('Улучшенный призрачный волк (Improved Ghost Wolf)', 'Improved Ghost Wolf', 'Improved Ghost Wolf'), '2', t('Призрачный волк быстрее и в помещениях', 'A faster Ghost Wolf that works indoors', 'Ghost Wolf швидше й у приміщеннях')],
                [t('Оружие стихий (Elemental Weapons)', 'Elemental Weapons', 'Elemental Weapons'), '3', t('Сильнее зачарования оружия', 'Stronger weapon imbues', 'Сильніші зачарування зброї')],
                ['Shamanistic Focus', '1', t('Шоки и Щит молний дешевле на 45%', 'Shocks and Lightning Shield cost 45% less', 'Шоки й Lightning Shield дешевші на 45%')],
                [t('Шквал (Flurry)', 'Flurry', 'Flurry'), '4', t('Скорость атак после крита', 'Attack speed after a crit', 'Швидкість атак після криту')],
                [t('Удар бури (Stormstrike)', 'Stormstrike', 'Stormstrike'), '1', t('Удар и +20% к урону следующей Молнии или Земного шока', 'A strike and +20% damage on your next Lightning Bolt or Earth Shock', 'Удар і +20% до шкоди наступної Lightning Bolt або Earth Shock')],
                ['Improved Stormstrike', '1', t('Шанс восполнять ману во время чтения и сброс отката Удара бури', 'A chance for mana regeneration while casting and Stormstrike resets', 'Шанс відновлювати ману під час читання й скидання відкату Stormstrike')],
            ]}),
            ('text', [
                t('Icy Veins и Wowhead совпадают в 20 очках из 21. Последнее проходное: Icy Veins кладёт его в Знания предков (Ancestral Knowledge), Wowhead — в Предчувствие (Anticipation). С очками Legacy оба доводят Improved Stormstrike до 2 и берут Оружие духов (Spirit Weapons) и [[Ментальную скорость|Mental Quickness]]. Оружие Водоворота (Maelstrom Weapon) Wowhead советует не брать, пока нельзя вложить все 5 очков.',
                  'Icy Veins and Wowhead match in 20 of 21 points. The last one is a filler: Icy Veins puts it into Ancestral Knowledge, Wowhead into Anticipation. With Legacy points both take Improved Stormstrike to 2 and add Spirit Weapons and Mental Quickness. Wowhead advises against Maelstrom Weapon until you can put all 5 points into it.',
                  'Icy Veins і Wowhead збігаються у 20 очках із 21. Останнє прохідне: Icy Veins кладе його в Ancestral Knowledge, Wowhead — в Anticipation. З очками Legacy обидва доводять Improved Stormstrike до 2 і беруть Spirit Weapons та Mental Quickness. Maelstrom Weapon Wowhead радить не брати, поки не можна вкласти всі 5 очок.'),
            ]),
            ('steps', [
                {'t': t('Перед боем', 'Before the pull', 'Перед боєм'),
                 'd': t('Оружие неистовства ветра, тотемы через Зов Стихий, Щит молний.', 'Windfury Weapon, totems with Call of the Elements, Lightning Shield.', 'Windfury Weapon, тотеми через Call of the Elements, Lightning Shield.')},
                {'t': t('Начало', 'Opening', 'Початок'),
                 'd': t('Молния 1-го ранга, чтобы притянуть врага.', 'A rank 1 Lightning Bolt to pull.', 'Lightning Bolt 1-го рангу, щоб притягнути ворога.')},
                {'t': t('Удар бури', 'Stormstrike', 'Stormstrike'),
                 'd': t('По откату; ловите сбросы отката.', 'On cooldown; watch for resets.', 'По відкату; ловіть скидання відкату.')},
                {'t': t('Земной шок', 'Earth Shock', 'Earth Shock'),
                 'd': t('По откату: он тратит усиление от Удара бури. В группе чередуйте с Огненным шоком.', 'On cooldown: it consumes the Stormstrike bonus. In a group, alternate it with Flame Shock.', 'По відкату: він витрачає посилення від Stormstrike. У групі чергуйте з Flame Shock.')},
                {'t': t('Много угрозы', 'Too much threat', 'Забагато загрози'),
                 'd': t('Ледяной шок вместо Земного.', 'Frost Shock instead of Earth Shock.', 'Frost Shock замість Earth Shock.')},
                {'t': t('Группа', 'Group of enemies', 'Група'),
                 'd': t('Кольцо огня с тотемом огня, если хватает маны.', 'Fire Nova with a Fire Totem down, if you have the mana.', 'Fire Nova з тотемом вогню, якщо вистачає мани.')},
            ]),
            ('tip', t('Маны на всю ротацию не хватает: всё, кроме Удара бури, — по необходимости (Icy Veins). Характеристики по Icy Veins: урон оружия, меткость и мастерство, крит, сила, интеллект.',
                      'You do not have the mana for the full rotation: use everything except Stormstrike only when needed (Icy Veins). Stats according to Icy Veins: weapon damage, hit and Expertise, crit, Strength, Intellect.',
                      'Мани на всю ротацію не вистачає: усе, крім Stormstrike, — за потреби (Icy Veins). Характеристики за Icy Veins: шкода зброї, влучність і майстерність, крит, сила, інтелект.')),
        ]},
        {'id': 'restoration', 'title': t('Исцеление: лекарь', 'Restoration: healer', 'Зцілення: цілитель'), 'blocks': [
            ('text', [
                t('Исцеление — лучший лекарь беты вместе с Послушанием жреца. Соло спек слаб, поэтому качаются Совершенствованием, а Исцеление берут для групп (Wowhead). На 30 уровне в ветке открываются Тотем прилива маны и Природная стремительность.',
                  'Restoration shares the top healer spot of the beta with Discipline Priest. It is weak solo, so you level as Enhancement and take Restoration for groups (Wowhead). At level 30 the tree opens up Mana Tide Totem and Nature’s Swiftness.',
                  'Зцілення — найкращий цілитель бети разом із Послухом жерця. Наодинці спеціалізація слабка, тож качаються Вдосконаленням, а Зцілення беруть для груп (Wowhead). На 30 рівні в гілці відкриваються Mana Tide Totem і Nature’s Swiftness.'),
            ]),
            ('table', {'head': H_TAL, 'rows': [
                [t('Улучшенная волна исцеления (Improved Healing Wave)', 'Improved Healing Wave', 'Improved Healing Wave'), '5', t('Волна исцеления читается быстрее', 'Faster Healing Wave', 'Healing Wave читається швидше')],
                ['Mindfulness', '3', t('Часть восполнения маны идёт во время чтения', 'Part of your mana regeneration continues while casting', 'Частина відновлення мани триває під час читання')],
                ['Natural Grace', '2', t('Меньше угрозы от заклинаний', 'Less threat from your spells', 'Менше загрози від заклинань')],
                [t('Исцеление предков (Ancestral Healing)', 'Ancestral Healing', 'Ancestral Healing'), '3', t('Броня цели растёт после крита лечения', 'The target gains armor after a critical heal', 'Броня цілі росте після криту лікування')],
                [t('Средоточие исцеления (Healing Focus)', 'Healing Focus', 'Healing Focus'), '1', t('Лечение реже сбивается уроном', 'Damage interrupts your heals less often', 'Лікування рідше збивається шкодою')],
                [t('Водный щит (Water Shield)', 'Water Shield', 'Water Shield'), '1', t('Мана при ударах по вам и при критах', 'Mana when you are hit and on crits', 'Мана при ударах по вас і при критах')],
                [t('Мастерство владения приливами (Tidal Mastery)', 'Tidal Mastery', 'Tidal Mastery'), '4', t('Крит лечения', 'Healing crit', 'Крит лікування')],
                [t('Тотем прилива маны (Mana Tide Totem)', 'Mana Tide Totem', 'Mana Tide Totem'), '1', t('Мана всей группе на 12 секунд', 'Mana for the whole group for 12 seconds', 'Мана всій групі на 12 секунд')],
                [t('Природная стремительность (Nature’s Swiftness)', 'Nature’s Swiftness', 'Nature’s Swiftness'), '1', t('Следующее заклинание природы — мгновенное', 'Your next Nature spell is instant', 'Наступне заклинання природи — миттєве')],
            ]}),
            ('text', [
                t('Icy Veins и Wowhead (его билд для групп) совпадают во всех 21 очке, и с очками Legacy тоже: Мастерство владения приливами до 5, Путь исцеления (Healing Way) 3 — Волна исцеления лечит сильнее — и одно очко [[Чистоты|Purification]]. Для соло Wowhead даёт другой билд: 11 очков в Исцеление и 10 в Стихии.',
                  'Icy Veins and Wowhead (its group build) match in all 21 points, and with the Legacy points too: Tidal Mastery to 5, Healing Way 3 for a stronger Healing Wave, and one point in Purification. For solo play Wowhead gives another build: 11 points in Restoration and 10 in Elemental.',
                  'Icy Veins і Wowhead (його білд для груп) збігаються в усіх 21 очку, і з очками Legacy теж: Tidal Mastery до 5, Healing Way 3 — Healing Wave лікує сильніше — і одне очко Purification. Для гри наодинці Wowhead дає інший білд: 11 очок у Зцілення й 10 у Стихії.'),
            ]),
            ('steps', [
                {'t': t('Перед боем', 'Before the pull', 'Перед боєм'),
                 'd': t('Тотемы через Зов Стихий; Тотем силы земли, если в группе бойцы ближнего боя.', 'Totems with Call of the Elements; Strength of Earth Totem if the group has melee.', 'Тотеми через Call of the Elements; Strength of Earth Totem, якщо в групі бійці ближнього бою.')},
                {'t': t('Волна исцеления', 'Healing Wave', 'Healing Wave'),
                 'd': t('Основное лечение; при небольшом уроне — низкий ранг.', 'Your main heal; a lower rank when damage is light.', 'Основне лікування; за невеликої шкоди — низький ранг.')},
                {'t': t('Природная стремительность', 'Nature’s Swiftness', 'Nature’s Swiftness'),
                 'd': t('В опасный момент: мгновенная Волна исцеления.', 'In a dangerous moment: an instant Healing Wave.', 'У небезпечний момент: миттєва Healing Wave.')},
                {'t': t('Тотем прилива маны', 'Mana Tide Totem', 'Mana Tide Totem'),
                 'd': t('Когда мана кончается в долгом бою.', 'When mana runs low in a long fight.', 'Коли мана закінчується в довгому бою.')},
                {'t': t('Спокойная минута', 'A quiet moment', 'Спокійна хвилина'),
                 'd': t('Опаляющий тотем и Кольцо огня против группы, иначе Молния.', 'Searing Totem and Fire Nova against a group, otherwise Lightning Bolt.', 'Searing Totem і Fire Nova проти групи, інакше Lightning Bolt.')},
            ]),
            ('tip', t('Характеристики по Icy Veins: сила лечения, крит, интеллект, дух, мана раз в 5 секунд. Водный щит и Исцеление предков работают от критов лечения, поэтому Мастерство владения приливами ценнее, чем кажется (Wowhead).',
                      'Stats according to Icy Veins: healing power, crit, Intellect, Spirit, mana per 5 seconds. Water Shield and Ancestral Healing run on critical heals, so Tidal Mastery is worth more than it looks (Wowhead).',
                      'Характеристики за Icy Veins: сила лікування, крит, інтелект, дух, мана раз на 5 секунд. Water Shield і Ancestral Healing працюють від критів лікування, тож Tidal Mastery цінніше, ніж здається (Wowhead).')),
        ]},
        {'id': 'faq', 'title': FAQ_T, 'blocks': [
            ('faq', [
                {'id': 'q1', 'q': t('Какой спек шамана лучший?', 'Which Shaman spec is best?', 'Яка спеціалізація шамана найкраща?'),
                 'a': [t('Для группы — Исцеление: в тир-листе беты оно в S. Для урона — Совершенствование (A*), Стихии — B*.', 'For groups, Restoration: it is in tier S on the beta tier list. For damage, Enhancement (A*); Elemental is B*.', 'Для групи — Зцілення: у тір-листі бети воно в S. Для шкоди — Вдосконалення (A*), Стихії — B*.')]},
                {'id': 'q2', 'q': t('Чем качаться шаману?', 'Which spec should a Shaman level as?', 'Чим качатися шаману?'),
                 'a': [t('Оба источника советуют Совершенствование: автоатаки не тратят ману. Стихии слабы до 40 уровня (Wowhead).', 'Both sources recommend Enhancement: auto attacks cost no mana. Elemental is weak before level 40 (Wowhead).', 'Обидва джерела радять Вдосконалення: автоатаки не витрачають ману. Стихії слабкі до 40 рівня (Wowhead).')]},
                {'id': 'q3', 'q': t('Есть ли шаман у Альянса?', 'Can the Alliance play a Shaman?', 'Чи є шаман в Альянсу?'),
                 'a': [t('Да: в Forever шаманом Альянса может быть дворф (Icy Veins).', 'Yes: in Forever, Dwarves can be Alliance Shamans (Icy Veins).', 'Так: у Forever шаманом Альянсу може бути дворф (Icy Veins).')]},
                {'id': 'q4', 'q': WHEN_Q, 'a': [WHEN_A]},
            ]),
        ]},
        {'id': 'related', 'title': t('Смотрите также', 'See also', 'Дивіться також'), 'blocks': [
            ('tiles', _related('shaman', [t('Шаман', 'Shaman', 'Шаман'), t('Прокачка Шамана', 'Shaman leveling', 'Прокачування Шамана')])),
        ]},
    ],
})

# ---------- warlock ----------

SPEC_BUILDS.append({
    'slug': 'builds-warlock', 'art': 'warlock', 'hero': 'hero_leveling', 'hub': False,
    'title': t('Билды Чернокнижника', 'Warlock Builds', 'Білди Чорнокнижника'),
    'lead': t('Таланты, приоритет и характеристики Колдовства, Демонологии и Разрушения. Здесь только то, в чём сходятся Icy Veins и Wowhead.',
              'Talents, priorities and stats for Affliction, Demonology and Destruction. This page shows only what Icy Veins and Wowhead agree on.',
              'Таланти, пріоритет і характеристики Прокляття, Демонології та Руйнування. Тут лише те, у чому сходяться Icy Veins і Wowhead.'),
    'tile': t('Колдовство, Демонология, Разрушение: таланты и приоритет', 'Affliction, Demonology, Destruction: talents and priorities', 'Прокляття, Демонологія, Руйнування: таланти й пріоритет'),
    'pills': [BETA, SPECS3, LATER],
    'sources': [
        ('Icy Veins: Affliction Warlock Guide', 'https://www.icy-veins.com/wow-forever/affliction-warlock-ranged-dps-pve-guide'),
        ('Icy Veins: Demonology Warlock Guide', 'https://www.icy-veins.com/wow-forever/demonology-warlock-ranged-dps-pve-guide'),
        ('Icy Veins: Destruction Warlock Guide', 'https://www.icy-veins.com/wow-forever/destruction-warlock-ranged-dps-pve-guide'),
        ('Icy Veins: Warlock Talent Calculator', 'https://www.icy-veins.com/wow-forever/warlock-talent-calculator'),
        ('Wowhead: Level 30 Affliction Warlock', 'https://www.wowhead.com/forever/guide/classes/warlock/affliction/level-30-dps-overview'),
        ('Wowhead: Level 30 Demonology Warlock', 'https://www.wowhead.com/forever/guide/classes/warlock/demonology/level-30-dps-overview'),
        ('Wowhead: Level 30 Destruction Warlock', 'https://www.wowhead.com/forever/guide/classes/warlock/destruction/level-30-dps-overview'),
        ('Wowhead: Warlock Talent Calculator', 'https://www.wowhead.com/forever/talent-calc/warlock'),
    ],
    'sections': [
        {'id': 'roles', 'title': t('Спеки и роли', 'Specs and roles', 'Спеціалізації та ролі'), 'blocks': [
            ('table', {'head': H_ROLES, 'rows': [
                [t('Колдовство', 'Affliction', 'Прокляття'), DPS, 'A',
                 t('Периодический урон, сильнее всех соло', 'Damage over time, the strongest solo', 'Періодична шкода, найсильніший наодинці')],
                [t('Демонология', 'Demonology', 'Демонологія'), DPS, 'A',
                 t('Суккуб наносит урон и держит врага', 'The Succubus deals damage and holds the enemy', 'Сукуб завдає шкоди й тримає ворога')],
                [t('Разрушение', 'Destruction', 'Руйнування'), DPS, 'A',
                 t('Прямой урон, Ожог Тьмы и Поджигание', 'Direct damage, Shadowburn and Conflagrate', 'Пряма шкода, Shadowburn і Conflagrate')],
            ]}),
            ('text', [ROLES_NOTE, t('Тир Разрушения — только по RankedBoost.', 'The Destruction tier comes from RankedBoost only.', 'Тір Руйнування — лише за RankedBoost.')]),
        ]},
        {'id': 'affliction', 'title': t('Колдовство: урон', 'Affliction: damage', 'Прокляття: шкода'), 'blocks': [
            ('text', [
                t('В Forever Проклятие агонии называется Bane of Agony, а Жизнеотвод растёт от духа (Wowhead). Icy Veins и Wowhead собирают Колдовство по-разному. У Icy Veins — периодический урон и мгновенные Стрелы Тьмы от Сумерек. У Wowhead — «танкование Похищением жизни»: суккуб бьёт, враг бьёт вас, а Похищение жизни возвращает здоровье.',
                  'In Forever, Curse of Agony is called Bane of Agony, and Life Tap scales with Spirit (Wowhead). Icy Veins and Wowhead build Affliction differently. Icy Veins goes for damage over time and instant Shadow Bolts from Nightfall. Wowhead goes for drain tanking: the Succubus hits, the enemy hits you, and Drain Life gives the health back.',
                  'У Forever Curse of Agony називається Bane of Agony, а Life Tap росте від духу (Wowhead). Icy Veins і Wowhead збирають Прокляття по-різному. В Icy Veins — періодична шкода й миттєві Shadow Bolt від Nightfall. У Wowhead — «танкування Drain Life»: сукуб б’є, ворог б’є вас, а Drain Life повертає здоров’я.'),
            ]),
            ('table', {'head': H_TAL, 'rows': [
                [t('Улучшенная порча (Improved Corruption)', 'Improved Corruption', 'Improved Corruption'), '5', t('Порча мгновенная и сильнее', 'An instant, stronger Corruption', 'Corruption миттєва й сильніша')],
                [t('Подавление (Suppression)', 'Suppression', 'Suppression'), '4', t('Меткость и меньше угрозы', 'Hit and less threat', 'Влучність і менше загрози')],
                [t('Улучшенный жизнеотвод (Improved Life Tap)', 'Improved Life Tap', 'Improved Life Tap'), '2', t('Больше маны от Жизнеотвода', 'More mana from Life Tap', 'Більше мани від Life Tap')],
            ]}),
            ('text', [
                t('Только это общее у Icy Veins и Wowhead. Icy Veins добирает Предел мрака (Grim Reach) 2, Improved Bane of Agony 2, [[Пандемию|Pandemic]] 3, Сумерки (Nightfall) 2 и Вытягивание жизни (Siphon Life). Wowhead — Improved Drains 3, Malediction, Усиление проклятия (Amplify Curse) и Вытягивание души (Soul Siphon): Похищение жизни сильнее за каждый ваш эффект Колдовства на цели. С очками Legacy Wowhead доводит Вытягивание души до 3.',
                  'That is all Icy Veins and Wowhead share. Icy Veins adds Grim Reach 2, Improved Bane of Agony 2, Pandemic 3, Nightfall 2 and Siphon Life. Wowhead adds Improved Drains 3, Malediction, Amplify Curse and Soul Siphon: Drain Life gets stronger for each of your Affliction effects on the target. With Legacy points Wowhead takes Soul Siphon to 3.',
                  'Лише це спільне в Icy Veins і Wowhead. Icy Veins добирає Grim Reach 2, Improved Bane of Agony 2, Pandemic 3, Nightfall 2 і Siphon Life. Wowhead — Improved Drains 3, Malediction, Amplify Curse і Soul Siphon: Drain Life сильніше за кожен ваш ефект Прокляття на цілі. З очками Legacy Wowhead доводить Soul Siphon до 3.'),
            ]),
            ('steps', [
                {'t': t('Демон', 'Demon', 'Демон'),
                 'd': t('Отправить первым.', 'Send it in first.', 'Відправити першим.')},
                {'t': t('Проклятие', 'Curse', 'Прокляття'),
                 'd': t('На боссах и элитах — Проклятие стихий или Проклятие безрассудства, по составу группы (Icy Veins).', 'On bosses and elites, Curse of the Elements or Curse of Recklessness, depending on your group (Icy Veins).', 'На босах і елітах — Curse of the Elements або Curse of Recklessness, залежно від складу групи (Icy Veins).')},
                {'t': 'Bane of Agony',
                 'd': t('Если цель проживёт долго.', 'If the target will live long enough.', 'Якщо ціль проживе довго.')},
                {'t': t('Порча', 'Corruption', 'Corruption'),
                 'd': t('Мгновенная, на каждую цель.', 'Instant, on every target.', 'Миттєва, на кожну ціль.')},
                {'t': t('Похищение жизни', 'Drain Life', 'Drain Life'),
                 'd': t('Когда нужно здоровье; у Wowhead — основное заклинание между проклятиями.', 'When you need health; Wowhead uses it as the main filler between DoTs.', 'Коли потрібне здоров’я; у Wowhead — основне заклинання між прокляттями.')},
                {'t': t('Нет маны', 'Out of mana', 'Немає мани'),
                 'd': t('Жизнеотвод; здоровье вернёт Похищение жизни. Цель почти мертва — жезл.', 'Life Tap; Drain Life gives the health back. Target nearly dead: wand.', 'Life Tap; здоров’я поверне Drain Life. Ціль майже мертва — жезл.')},
            ]),
            ('tip', t('Характеристики по Icy Veins: сила заклинаний, меткость, крит, интеллект, дух. Дух важнее, чем в Classic: от него растёт Жизнеотвод (Wowhead).',
                      'Stats according to Icy Veins: spell power, hit, crit, Intellect, Spirit. Spirit matters more than in Classic: Life Tap scales with it (Wowhead).',
                      'Характеристики за Icy Veins: сила заклинань, влучність, крит, інтелект, дух. Дух важливіший, ніж у Classic: від нього росте Life Tap (Wowhead).')),
        ]},
        {'id': 'demonology', 'title': t('Демонология: урон', 'Demonology: damage', 'Демонологія: шкода'), 'blocks': [
            ('text', [
                t('Демонология держится на суккубе: она бьёт примерно в 1,5 раза сильнее демона Бездны, а с Demonic Brand держит врага на себе (Wowhead). Жгучая боль клеймит цель, и следующие атаки демона наносят дополнительный урон. Питомцы в Forever растут от ваших характеристик (Icy Veins).',
                  'Demonology runs on the Succubus: she hits about 1.5 times as hard as the Voidwalker, and with Demonic Brand she keeps the enemy on herself (Wowhead). Searing Pain brands the target, so the demon’s next attacks deal extra damage. In Forever pets scale with your stats (Icy Veins).',
                  'Демонологія тримається на сукубі: вона б’є приблизно в 1,5 раза сильніше за Voidwalker, а з Demonic Brand тримає ворога на собі (Wowhead). Searing Pain таврує ціль, і наступні атаки демона завдають додаткової шкоди. Улюбленці у Forever ростуть від ваших характеристик (Icy Veins).'),
            ]),
            ('table', {'head': H_TAL, 'rows': [
                [t('Нечестивая сила (Unholy Power)', 'Unholy Power', 'Unholy Power'), '5', t('Урон демона', 'Demon damage', 'Шкода демона')],
                ['Demonic Energies', '2', t('Ваш урон заклинаниями лечит демона, Жизнеотвод даёт ему ману', 'Your spell damage heals the demon; Life Tap gives it mana', 'Ваша шкода заклинаннями лікує демона, Life Tap дає йому ману')],
                [t('Улучшенный сайаад (Improved Sayaad)', 'Improved Sayaad', 'Improved Sayaad'), '3', t('Сильнее заклинания суккуба', 'Stronger Succubus spells', 'Сильніші заклинання сукуба')],
                [t('Мастер призыва (Master Summoner)', 'Master Summoner', 'Master Summoner'), '2', t('Призыв демона быстрее и дешевле', 'Faster, cheaper demon summons', 'Виклик демона швидший і дешевший')],
                ['Demonic Brand', '3', t('Клеймо от Жгучей боли: демон бьёт сильнее', 'A brand from Searing Pain: the demon hits harder', 'Тавро від Searing Pain: демон б’є сильніше')],
            ]}),
            ('text', [
                t('Это общее у Icy Veins и Wowhead. Расходятся: Icy Veins уже на 30 уровне берёт [[Связку души|Soul Link]] — 30% урона по вам переходит на демона — и к ней [[Энергию Скверны|Fel Vitality]], Демоническое жертвоприношение (Demonic Sacrifice) и Господство Скверны (Fel Domination). Wowhead берёт Демоническое облачение (Demonic Embrace) 3 и 3 очка в Колдовство, а Связку души — только с очками Legacy, вместе с [[Демоническим знанием|Demonic Knowledge]] 3.',
                  'This is what Icy Veins and Wowhead share. They differ: Icy Veins takes Soul Link at level 30 already, so 30% of the damage you take goes to the demon, along with Fel Vitality, Demonic Sacrifice and Fel Domination. Wowhead takes Demonic Embrace 3 and 3 points in Affliction, and Soul Link only with Legacy points, together with Demonic Knowledge 3.',
                  'Це спільне в Icy Veins і Wowhead. Розходяться: Icy Veins уже на 30 рівні бере Soul Link — 30% шкоди по вас переходить на демона — і до нього Fel Vitality, Demonic Sacrifice та Fel Domination. Wowhead бере Demonic Embrace 3 і 3 очки в Прокляття, а Soul Link — лише з очками Legacy, разом із Demonic Knowledge 3.'),
            ]),
            ('steps', [
                {'t': t('Перед боем', 'Before the pull', 'Перед боєм'),
                 'd': t('Связка души, если взяли; демон атакует первым.', 'Soul Link if you have it; the demon attacks first.', 'Soul Link, якщо взяли; демон атакує першим.')},
                {'t': t('Порча', 'Corruption', 'Corruption'),
                 'd': t('И Bane of Agony, если у цели много здоровья.', 'Plus Bane of Agony if the target has a lot of health.', 'І Bane of Agony, якщо в цілі багато здоров’я.')},
                {'t': t('Жгучая боль', 'Searing Pain', 'Searing Pain'),
                 'd': t('Клеймо; обновлять, когда спадает, примерно раз в 6 секунд (Wowhead).', 'The brand; recast it when it drops, roughly every 6 seconds (Wowhead).', 'Тавро; оновлювати, коли спадає, приблизно раз на 6 секунд (Wowhead).')},
                {'t': t('Похищение жизни', 'Drain Life', 'Drain Life'),
                 'd': t('Основное заклинание: лечит и вас, и демона.', 'Your main filler: it heals both you and the demon.', 'Основне заклинання: лікує і вас, і демона.')},
                {'t': t('Нет маны', 'Out of mana', 'Немає мани'),
                 'd': t('Жизнеотвод. Цель почти мертва — жезл.', 'Life Tap. Target nearly dead: wand.', 'Life Tap. Ціль майже мертва — жезл.')},
            ]),
            ('tip', t('Характеристики по Icy Veins: сила заклинаний, меткость, интеллект, крит, дух. Охотник Скверны на 30 уровне даётся за задание класса, но для прокачки оба источника советуют суккуба.',
                      'Stats according to Icy Veins: spell power, hit, Intellect, crit, Spirit. The Felhunter comes from a class quest at level 30, but both sources recommend the Succubus for leveling.',
                      'Характеристики за Icy Veins: сила заклинань, влучність, інтелект, крит, дух. Felhunter на 30 рівні дають за завдання класу, але для прокачування обидва джерела радять сукуба.')),
        ]},
        {'id': 'destruction', 'title': t('Разрушение: урон', 'Destruction: damage', 'Руйнування: шкода'), 'blocks': [
            ('text', [
                t('Разрушение бьёт прямыми заклинаниями: быстрее чтение, сильнее криты и два мгновенных удара — Поджигание и Ожог Тьмы. Ожог Тьмы стоит осколок души, но возвращает его, если цель умрёт за 8 секунд, поэтому им добивают. Новый талант Bane of Havoc переносит 15% урона по другим целям на проклятую цель (Icy Veins).',
                  'Destruction hits with direct spells: faster casts, harder crits and two instant hits, Conflagrate and Shadowburn. Shadowburn costs a Soul Shard but gives it back if the target dies within 8 seconds, so you use it to finish enemies. The new Bane of Havoc talent copies 15% of your damage on other targets to the cursed one (Icy Veins).',
                  'Руйнування б’є прямими заклинаннями: швидше читання, сильніші крити й два миттєві удари — Conflagrate і Shadowburn. Shadowburn коштує уламок душі, але повертає його, якщо ціль загине за 8 секунд, тож ним добивають. Новий талант Bane of Havoc переносить 15% шкоди по інших цілях на прокляту ціль (Icy Veins).'),
            ]),
            ('table', {'head': H_TAL, 'rows': [
                [t('Погибель (Bane)', 'Bane', 'Bane'), '5', t('Стрела Тьмы и Жертвенный огонь на 0,5 секунды быстрее', 'Shadow Bolt and Immolate cast 0.5 seconds faster', 'Shadow Bolt та Immolate на 0,5 секунди швидші')],
                [t('Разгром (Ruin)', 'Ruin', 'Ruin'), '5', t('Урон критов заклинаний Разрушения', 'Destruction spell crit damage', 'Шкода критів заклинань Руйнування')],
                [t('Ожог Тьмы (Shadowburn)', 'Shadowburn', 'Shadowburn'), '1', t('Мгновенный удар, чтобы добить', 'An instant hit to finish a target', 'Миттєвий удар, щоб добити')],
                ['Agonizing Flames', '3', t('Урон заклинаний Разрушения и крит Жгучей боли', 'Destruction spell damage and Searing Pain crit', 'Шкода заклинань Руйнування й крит Searing Pain')],
                [t('Поджигание (Conflagrate)', 'Conflagrate', 'Conflagrate'), '1', t('Мгновенный урон, тратит Жертвенный огонь', 'Instant damage that consumes Immolate', 'Миттєва шкода, витрачає Immolate')],
            ]}),
            ('text', [
                t('Это общее у Icy Veins и Wowhead. Расходятся: Icy Veins берёт Предел разрушения (Destructive Reach) 2, Катаклизм (Cataclysm) 3 — заклинания дешевле — и Bane of Havoc. Wowhead — Последствия (Aftermath) 5 ради урона Жертвенного огня и одно очко Улучшенной порчи, а Bane of Havoc — только с очками Legacy. Разгром, по Wowhead, пока даёт мало: на 30 уровне мало крита.',
                  'This is what Icy Veins and Wowhead share. They differ: Icy Veins takes Destructive Reach 2, Cataclysm 3 for cheaper spells, and Bane of Havoc. Wowhead takes Aftermath 5 for Immolate damage and one point in Improved Corruption, and Bane of Havoc only with Legacy points. According to Wowhead, Ruin does little for now: there is not much crit at level 30.',
                  'Це спільне в Icy Veins і Wowhead. Розходяться: Icy Veins бере Destructive Reach 2, Cataclysm 3 — заклинання дешевші — і Bane of Havoc. Wowhead — Aftermath 5 заради шкоди Immolate і одне очко Improved Corruption, а Bane of Havoc — лише з очками Legacy. Ruin, за Wowhead, поки дає мало: на 30 рівні мало криту.'),
            ]),
            ('steps', [
                {'t': t('Демон', 'Demon', 'Демон'),
                 'd': t('Отправить первым. Для Разрушения Wowhead советует демона Бездны: он держит угрозу.', 'Send it in first. For Destruction, Wowhead recommends the Voidwalker: it holds threat.', 'Відправити першим. Для Руйнування Wowhead радить Voidwalker: він тримає загрозу.')},
                {'t': t('Начало', 'Opening', 'Початок'),
                 'd': t('Стрела Тьмы и сразу Жертвенный огонь: оба попадут почти одновременно (Icy Veins).', 'Shadow Bolt and Immolate right after it: both land at almost the same time (Icy Veins).', 'Shadow Bolt і одразу Immolate: обидва влучать майже одночасно (Icy Veins).')},
                {'t': t('Между ударами', 'Filler', 'Між ударами'),
                 'd': t('Стрела Тьмы при лишней мане, иначе жезл.', 'Shadow Bolt with spare mana, otherwise your wand.', 'Shadow Bolt за зайвої мани, інакше жезл.')},
                {'t': t('Поджигание', 'Conflagrate', 'Conflagrate'),
                 'd': t('Перед концом Жертвенного огня.', 'Just before Immolate runs out.', 'Перед кінцем Immolate.')},
                {'t': t('Ожог Тьмы', 'Shadowburn', 'Shadowburn'),
                 'd': t('Добить цель и вернуть осколок души.', 'Finish the target and get the Soul Shard back.', 'Добити ціль і повернути уламок душі.')},
                {'t': t('Нужны осколки', 'Need shards', 'Потрібні уламки'),
                 'd': t('Похищение души вместо Ожога Тьмы.', 'Drain Soul instead of Shadowburn.', 'Drain Soul замість Shadowburn.')},
            ]),
            ('tip', t('Характеристики по Icy Veins: сила заклинаний, меткость, скорость, крит. Жгучая боль с Agonizing Flames критует чаще, но даёт много угрозы.',
                      'Stats according to Icy Veins: spell power, hit, haste, crit. With Agonizing Flames, Searing Pain crits more often, but it generates a lot of threat.',
                      'Характеристики за Icy Veins: сила заклинань, влучність, швидкість, крит. Searing Pain з Agonizing Flames критує частіше, але дає багато загрози.')),
        ]},
        {'id': 'faq', 'title': FAQ_T, 'blocks': [
            ('faq', [
                {'id': 'q1', 'q': t('Какой спек чернокнижника лучший?', 'Which Warlock spec is best?', 'Яка спеціалізація чорнокнижника найкраща?'),
                 'a': [t('В тир-листе беты все три — A. Демонология лучшая для подземелий по Noobtoboss, Колдовство сильнее всех соло, у Разрушения меньше всего данных.', 'All three are A on the beta tier list. Demonology is the best dungeon spec according to Noobtoboss, Affliction is the strongest solo, and Destruction has the least data.', 'У тір-листі бети всі три — A. Демонологія найкраща для підземель за Noobtoboss, Прокляття найсильніше наодинці, у Руйнування найменше даних.')]},
                {'id': 'q2', 'q': t('Что такое Bane of Agony?', 'What is Bane of Agony?', 'Що таке Bane of Agony?'),
                 'a': [t('Так в Forever называется Проклятие агонии из Classic: периодический урон, который набирает силу к концу. Улучшающий его талант тоже переименован — Improved Bane of Agony.', 'It is the Forever name of Classic’s Curse of Agony: damage over time that ramps up towards the end. The talent that improves it was renamed too: Improved Bane of Agony.', 'Так у Forever називається Curse of Agony з Classic: періодична шкода, що набирає силу до кінця. Талант, що його покращує, теж перейменовано — Improved Bane of Agony.')]},
                {'id': 'q3', 'q': t('Какого демона брать?', 'Which demon should I use?', 'Якого демона брати?'),
                 'a': [t('Для Колдовства и Демонологии — суккуба: она бьёт сильнее. Для Разрушения Wowhead советует демона Бездны: он лучше держит угрозу.', 'For Affliction and Demonology, the Succubus: she hits harder. For Destruction, Wowhead recommends the Voidwalker: it holds threat better.', 'Для Прокляття й Демонології — сукуба: вона б’є сильніше. Для Руйнування Wowhead радить Voidwalker: він краще тримає загрозу.')]},
                {'id': 'q4', 'q': WHEN_Q, 'a': [WHEN_A]},
            ]),
        ]},
        {'id': 'related', 'title': t('Смотрите также', 'See also', 'Дивіться також'), 'blocks': [
            ('tiles', _related('warlock', [t('Чернокнижник', 'Warlock', 'Чорнокнижник'), t('Прокачка Чернокнижника', 'Warlock leveling', 'Прокачування Чорнокнижника')])),
        ]},
    ],
})

# ---------- druid ----------

SPEC_BUILDS.append({
    'slug': 'builds-druid', 'art': 'druid', 'hero': 'hero_leveling', 'hub': False,
    'title': t('Билды Друида', 'Druid Builds', 'Білди Друїда'),
    'lead': t('Таланты, приоритет и характеристики Баланса, Силы зверя и Исцеления. Здесь только то, в чём сходятся Icy Veins и Wowhead.',
              'Talents, priorities and stats for Balance, Feral and Restoration. This page shows only what Icy Veins and Wowhead agree on.',
              'Таланти, пріоритет і характеристики Балансу, Сили звіра та Зцілення. Тут лише те, у чому сходяться Icy Veins і Wowhead.'),
    'tile': t('Баланс, Сила зверя, Исцеление: таланты и приоритет', 'Balance, Feral, Restoration: talents and priorities', 'Баланс, Сила звіра, Зцілення: таланти й пріоритет'),
    'pills': [BETA, SPECS3, LATER],
    'sources': [
        ('Icy Veins: Balance Druid Guide', 'https://www.icy-veins.com/wow-forever/balance-druid-ranged-dps-pve-guide'),
        ('Icy Veins: Feral Druid Guide', 'https://www.icy-veins.com/wow-forever/feral-druid-melee-dps-and-tank-pve-guide'),
        ('Icy Veins: Restoration Druid Guide', 'https://www.icy-veins.com/wow-forever/restoration-druid-healer-pve-guide'),
        ('Icy Veins: Druid Talent Calculator', 'https://www.icy-veins.com/wow-forever/druid-talent-calculator'),
        ('Wowhead: Level 30 Balance Druid', 'https://www.wowhead.com/forever/guide/classes/druid/balance/level-30-dps-overview'),
        ('Wowhead: Level 30 Feral Druid DPS', 'https://www.wowhead.com/forever/guide/classes/druid/feral/level-30-dps-overview'),
        ('Wowhead: Level 30 Restoration Druid', 'https://www.wowhead.com/forever/guide/classes/druid/restoration/level-30-healer-overview'),
        ('Wowhead: Druid Talent Calculator', 'https://www.wowhead.com/forever/talent-calc/druid'),
    ],
    'sections': [
        {'id': 'roles', 'title': t('Спеки и роли', 'Specs and roles', 'Спеціалізації та ролі'), 'blocks': [
            ('table', {'head': H_ROLES, 'rows': [
                [t('Баланс', 'Balance', 'Баланс'), DPS, 'C',
                 t('Лунный огонь и Рой насекомых; Затмение пока слабо', 'Moonfire and Insect Swarm; Eclipse is weak for now', 'Moonfire та Insect Swarm; Eclipse поки слабке')],
                [t('Сила зверя (кошка)', 'Feral (cat)', 'Сила звіра (кіт)'), DPS, 'B',
                 t('Переходящая сила: мана в энергию', 'Shifting Power turns mana into Energy', 'Shifting Power: мана в енергію')],
                [t('Сила зверя (медведь)', 'Feral (bear)', 'Сила звіра (ведмідь)'), TANK, 'B',
                 t('Танкует, но уступает Паладину и Воину', 'Tanks, but trails Paladin and Warrior', 'Танкує, але поступається Паладину й Воїну')],
                [t('Исцеление', 'Restoration', 'Зцілення'), HEALER, 'A',
                 t('Омоложение и Быстрое восстановление', 'Rejuvenation and Swiftmend', 'Rejuvenation і Swiftmend')],
            ]}),
            ('text', [ROLES_NOTE, t('Многое у друида открывается после 30 уровня, поэтому данных о нём меньше, чем о других классах. У Исцеления gamer-guides ставит S.', 'Much of the Druid unlocks after level 30, so there is less data on it than on other classes. gamer-guides puts Restoration in S.', 'Багато в друїда відкривається після 30 рівня, тож даних про нього менше, ніж про інші класи. Зцілення gamer-guides ставить у S.')]),
        ]},
        {'id': 'balance', 'title': t('Баланс: урон', 'Balance: damage', 'Баланс: шкода'), 'blocks': [
            ('text', [
                t('Баланс на 30 уровне — заклинатель с периодическим уроном: Лунный огонь и Рой насекомых, затем Гнев. Ураган откроется только на 40 уровне (Icy Veins). Wowhead даёт три билда: на периодический урон, на чтение Гнева и Звездного огня через Затмение и «медведя-заклинателя» для быстрой прокачки.',
                  'At level 30 Balance is a damage-over-time caster: Moonfire and Insect Swarm, then Wrath. Hurricane only unlocks at level 40 (Icy Veins). Wowhead gives three builds: damage over time, hard-casting Wrath and Starfire through Eclipse, and a “Spellbear” for fast leveling.',
                  'Баланс на 30 рівні — заклинач із періодичною шкодою: Moonfire та Insect Swarm, потім Wrath. Hurricane відкриється лише на 40 рівні (Icy Veins). Wowhead дає три білди: на періодичну шкоду, на читання Wrath і Starfire через Eclipse та «ведмедя-заклинача» для швидкого прокачування.'),
            ]),
            ('table', {'head': H_TAL, 'rows': [
                [t('Лунное сияние (Moonglow)', 'Moonglow', 'Moonglow'), '3', t('Заклинания урона дешевле', 'Cheaper damage spells', 'Дешевші заклинання шкоди')],
                ['Nature’s Majesty', '2', t('Шанс крита заклинаний и атак', 'Crit chance with spells and attacks', 'Шанс криту заклинань і атак')],
                [t('Предел сил Природы (Nature’s Reach)', 'Nature’s Reach', 'Nature’s Reach'), '2', t('Дальность и меткость заклинаний Баланса', 'Range and hit for Balance spells', 'Дальність і влучність заклинань Балансу')],
                ['Nature’s Splendor', '1', t('Дольше Лунный огонь, Рой насекомых, Омоложение и Восстановление', 'Longer Moonfire, Insect Swarm, Rejuvenation and Regrowth', 'Довші Moonfire, Insect Swarm, Rejuvenation і Regrowth')],
                [t('Рой насекомых (Insect Swarm)', 'Insect Swarm', 'Insect Swarm'), '1', t('Периодический урон; можно читать, не глядя на цель', 'Damage over time; castable without facing the target', 'Періодична шкода; можна читати, не дивлячись на ціль')],
                [t('Улучшенный лунный огонь (Improved Moonfire)', 'Improved Moonfire', 'Improved Moonfire'), '2', t('Урон и крит Лунного огня', 'Moonfire damage and crit', 'Шкода й крит Moonfire')],
            ]}),
            ('text', [
                t('Это общее у Icy Veins и билда Wowhead на периодический урон. Улучшенный гнев (Improved Wrath) 5 берут Icy Veins и билд Wowhead на чтение. Остальное расходится: Icy Veins кладёт 5 очков в Средоточие Природы (Nature’s Focus) из ветки Исцеления — заклинания реже сбиваются уроном, Wowhead — Genesis 5 и Отмщение (Vengeance) 4. Таланты от крита вроде Отмщения Icy Veins считает слабыми, пока крита мало.',
                  'This is what Icy Veins and Wowhead’s damage-over-time build share. Improved Wrath 5 is in both the Icy Veins build and Wowhead’s hard-casting build. The rest differs: Icy Veins puts 5 points into Nature’s Focus from the Restoration tree so damage pushes back your casts less, Wowhead takes Genesis 5 and Vengeance 4. Icy Veins considers crit talents such as Vengeance weak while you have little crit.',
                  'Це спільне в Icy Veins і білда Wowhead на періодичну шкоду. Improved Wrath 5 беруть Icy Veins і білд Wowhead на читання. Решта розходиться: Icy Veins кладе 5 очок у Nature’s Focus з гілки Зцілення — заклинання рідше збиваються шкодою, Wowhead — Genesis 5 і Vengeance 4. Таланти від криту на кшталт Vengeance Icy Veins вважає слабкими, поки криту мало.'),
            ]),
            ('steps', [
                {'t': t('Лунный огонь', 'Moonfire', 'Moonfire'),
                 'd': t('На каждой цели в бою.', 'On every target in combat.', 'На кожній цілі в бою.')},
                {'t': t('Рой насекомых', 'Insect Swarm', 'Insect Swarm'),
                 'd': t('После Лунного огня.', 'After Moonfire.', 'Після Moonfire.')},
                {'t': t('Гнев', 'Wrath', 'Wrath'),
                 'd': t('Основное заклинание.', 'Your main spell.', 'Основне заклинання.')},
                {'t': t('Враг добежал', 'An enemy reaches you', 'Ворог добіг'),
                 'd': t('Гнев деревьев, чтобы держать его на расстоянии (Wowhead).', 'Entangling Roots to keep it at range (Wowhead).', 'Entangling Roots, щоб тримати його на відстані (Wowhead).')},
            ]),
            ('tip', t('Характеристики по Icy Veins (для беты): интеллект, сила заклинаний, дух, мана раз в 5 секунд, крит. Затмение без очков Legacy, по Wowhead, работает вполсилы; в тир-листе беты Баланс — C.',
                      'Stats according to Icy Veins (for the beta): Intellect, spell power, Spirit, mana per 5 seconds, crit. According to Wowhead, Eclipse is muted without Legacy points; Balance is C on the beta tier list.',
                      'Характеристики за Icy Veins (для бети): інтелект, сила заклинань, дух, мана раз на 5 секунд, крит. Eclipse без очок Legacy, за Wowhead, працює вполовину; у тір-листі бети Баланс — C.')),
        ]},
        {'id': 'feral', 'title': t('Сила зверя: урон и танк', 'Feral: damage and tank', 'Сила звіра: шкода й танк'), 'blocks': [
            ('text', [
                bt(t('Сила зверя — одна ветка на две роли: кошка бьёт, медведь танкует. Новый талант Переходящая сила превращает ману в энергию в облике кошки. Облик медведя даётся за задание класса на 10 уровне, облик кошки — на 20 (Icy Veins). Урона по площади у кошки на 30 уровне почти нет (Wowhead).',
                  'Feral is one tree for two roles: the cat deals damage, the bear tanks. The new Shifting Power talent turns mana into Energy in Cat Form. Bear Form comes from a class quest at level 10, Cat Form at 20 (Icy Veins). At level 30 the cat has almost no area damage (Wowhead).',
                  'Сила звіра — одна гілка на дві ролі: кіт б’є, ведмідь танкує. Новий талант Shifting Power перетворює ману на енергію в Cat Form. Bear Form дають за завдання класу на 10 рівні, Cat Form — на 20 (Icy Veins). Шкоди по площі в кота на 30 рівні майже немає (Wowhead).'), 3),
            ]),
            ('table', {'head': H_TAL, 'rows': [
                [t('Свирепость (Ferocity)', 'Ferocity', 'Ferocity'), '5', t('Трепка, Primal Bite, Размах, Когти и Глубокая рана дешевле', 'Cheaper Maul, Primal Bite, Swipe, Claw and Rake', 'Дешевші Maul, Primal Bite, Swipe, Claw і Rake')],
                [t('Животный инстинкт (Feral Instinct)', 'Feral Instinct', 'Feral Instinct'), '3', t('Урон Размаха, Крадущийся зверь незаметнее', 'Swipe damage and a stealthier Prowl', 'Шкода Swipe, Prowl непомітніший')],
                [t('Звериная скорость (Feral Swiftness)', 'Feral Swiftness', 'Feral Swiftness'), '2', t('Скорость в облике кошки и уклонение', 'Cat Form speed and dodge', 'Швидкість у Cat Form і ухилення')],
                [t('Растерзать противника (Shredding Attacks)', 'Shredding Attacks', 'Shredding Attacks'), '3', t('Полоснуть дешевле', 'Cheaper Shred', 'Дешевший Shred')],
                [t('Бешеное неистовство (Savage Fury)', 'Savage Fury', 'Savage Fury'), '2', t('Урон Когтей, Глубокой раны, Полоснуть, Трепки и Размаха', 'Claw, Rake, Shred, Maul and Swipe damage', 'Шкода Claw, Rake, Shred, Maul і Swipe')],
                [t('Острые когти (Sharpened Claws)', 'Sharpened Claws', 'Sharpened Claws'), '2', t('Крит в облике медведя и кошки', 'Crit in Bear and Cat Form', 'Крит у Bear Form і Cat Form')],
                [t('Переходящая сила (Shifting Power)', 'Shifting Power', 'Shifting Power'), '1', t('Мана в энергию в облике кошки', 'Mana into Energy in Cat Form', 'Мана в енергію в Cat Form')],
                ['Primal Bite', '1', t('Главный удар медведя, много угрозы', 'The bear’s main attack, high threat', 'Головний удар ведмедя, багато загрози')],
                [t('Вожак стаи (Leader of the Pack)', 'Leader of the Pack', 'Leader of the Pack'), '1', t('+3% к шансу крита всей группы', '+3% crit chance for the whole group', '+3% до шансу криту всієї групи')],
            ]}),
            ('text', [
                t('Icy Veins и Wowhead (его билд для прокачки и обеих ролей) совпадают в 20 очках из 21. Последнее: у Icy Veins — Blood Frenzy, у Wowhead — Звериная атака (Feral Charge); Icy Veins называет её заменой. С очками Legacy оба берут Improved Shifting Power 2: Переходящая сила чаще. Для чистого урона у Wowhead есть отдельный билд: Сердце дикой природы (Heart of the Wild) 5 вместо Животного инстинкта, Звериной скорости, Звериной атаки и Primal Bite.',
                  'Icy Veins and Wowhead (its build for leveling and both roles) match in 20 of 21 points. The last one: Icy Veins takes Blood Frenzy, Wowhead takes Feral Charge, which Icy Veins names as the alternative. With Legacy points both take Improved Shifting Power 2 for a more frequent Shifting Power. For pure damage Wowhead has a separate build: Heart of the Wild 5 instead of Feral Instinct, Feral Swiftness, Feral Charge and Primal Bite.',
                  'Icy Veins і Wowhead (його білд для прокачування й обох ролей) збігаються у 20 очках із 21. Останнє: в Icy Veins — Blood Frenzy, у Wowhead — Feral Charge; Icy Veins називає його заміною. З очками Legacy обидва беруть Improved Shifting Power 2: Shifting Power частіше. Для чистої шкоди у Wowhead є окремий білд: Heart of the Wild 5 замість Feral Instinct, Feral Swiftness, Feral Charge і Primal Bite.'),
            ]),
            ('steps', [
                {'t': t('Переходящая сила', 'Shifting Power', 'Shifting Power'),
                 'd': t('По откату, когда энергии мало, чтобы прибавка не сгорела.', 'On cooldown, while Energy is low enough that none of the gain is wasted.', 'По відкату, коли енергії мало, щоб прибавка не згоріла.')},
                {'t': t('Разорвать', 'Rip', 'Rip'),
                 'd': t('На 4–5 приёмах серии, если цель проживёт ещё 6 секунд (Wowhead).', 'At 4–5 combo points if the target will live another 6 seconds (Wowhead).', 'На 4–5 прийомах серії, якщо ціль проживе ще 6 секунд (Wowhead).')},
                {'t': t('Глубокая рана', 'Rake', 'Rake'),
                 'd': t('Если цель проживёт 6 секунд.', 'If the target will live 6 seconds.', 'Якщо ціль проживе 6 секунд.')},
                {'t': t('Полоснуть', 'Shred', 'Shred'),
                 'd': t('Основной удар из-за спины цели; если не зайти сзади — Когти.', 'Your main strike from behind the target; Claw if you cannot get behind.', 'Основний удар з-за спини цілі; якщо не зайти ззаду — Claw.')},
                {'t': t('Медведь', 'Bear', 'Ведмідь'),
                 'd': t('Primal Bite — главный расход Ярости, Размах — против группы, Трепка — лишняя Ярость; Исступление даёт Ярость в начале боя (Icy Veins).', 'Primal Bite is your main Rage spender, Swipe against a group, Maul for spare Rage; Enrage gives Rage at the start of a fight (Icy Veins).', 'Primal Bite — головна витрата Люті, Swipe — проти групи, Maul — зайва Лють; Enrage дає Лють на початку бою (Icy Veins).')},
            ]),
            ('tip', t('Характеристики по Icy Veins: урон оружия, меткость и мастерство, крит, сила, ловкость. Primal Bite, Переходящая сила и Blood Frenzy — новые таланты Forever. В тир-листе беты медведь — B: танкует, но уступает Паладину и Воину.',
                      'Stats according to Icy Veins: weapon damage, hit and Expertise, crit, Strength, Agility. Primal Bite, Shifting Power and Blood Frenzy are new Forever talents. On the beta tier list the bear is B: it tanks, but trails Paladin and Warrior.',
                      'Характеристики за Icy Veins: шкода зброї, влучність і майстерність, крит, сила, спритність. Primal Bite, Shifting Power і Blood Frenzy — нові таланти Forever. У тір-листі бети ведмідь — B: танкує, але поступається Паладину й Воїну.')),
        ]},
        {'id': 'restoration', 'title': t('Исцеление: лекарь', 'Restoration: healer', 'Зцілення: цілитель'), 'blocks': [
            ('text', [
                t('Исцеление на 30 уровне получает Быстрое восстановление и Природную стремительность, а Омоложение и Восстановление теперь могут давать критическое лечение (Wowhead). У тренера на 30 уровне — Спокойствие, сильное лечение всей группы.',
                  'At level 30 Restoration gets Swiftmend and Nature’s Swiftness, and Rejuvenation and Regrowth can now crit (Wowhead). The trainer teaches Tranquility at level 30, a strong heal for the whole group.',
                  'Зцілення на 30 рівні отримує Swiftmend і Nature’s Swiftness, а Rejuvenation і Regrowth тепер можуть давати критичне лікування (Wowhead). У тренера на 30 рівні — Tranquility, сильне лікування всієї групи.'),
            ]),
            ('table', {'head': H_TAL, 'rows': [
                ['Gift of the Earthmother', '1', t('Короче общий откат после Омоложения и Быстрого восстановления', 'A shorter global cooldown on Rejuvenation and Swiftmend', 'Коротший глобальний відкат після Rejuvenation і Swiftmend')],
                [t('Быстрое восстановление (Swiftmend)', 'Swiftmend', 'Swiftmend'), '1', t('Мгновенное лечение за счёт Омоложения или Восстановления', 'An instant heal that uses up Rejuvenation or Regrowth', 'Миттєве лікування за рахунок Rejuvenation або Regrowth')],
            ]}),
            ('text', [
                t('Встроенные билды гайда Icy Veins открываются неверно, поэтому сверяли по его тексту. Для лечения в группе оба источника берут Gift of the Earthmother и Быстрое восстановление и оба упоминают Средоточие Природы (Nature’s Focus); Wowhead кладёт в него 5 очков. Дальше у Wowhead вся ветка Исцеления: Дар природы (Gift of Nature) 5, Отражение (Reflection) 3, Naturalist 5 и Природная стремительность. Для мира Icy Veins советует другой путь: сначала Улучшенный гнев (Improved Wrath) и Рой насекомых из Баланса, потом Исцеление. С очками Legacy Wowhead берёт Улучшенное спокойствие (Improved Tranquility): лечение группы без угрозы с откатом 2 минуты.',
                  'The embedded builds in the Icy Veins guide do not load correctly, so they were checked against its text. For group healing both sources take Gift of the Earthmother and Swiftmend, and both mention Nature’s Focus; Wowhead puts 5 points into it. After that Wowhead goes all the way down Restoration: Gift of Nature 5, Reflection 3, Naturalist 5 and Nature’s Swiftness. For the open world Icy Veins suggests another path: Improved Wrath and Insect Swarm from Balance first, then Restoration. With Legacy points Wowhead takes Improved Tranquility: a threat-free group heal on a 2-minute cooldown.',
                  'Вбудовані білди гайда Icy Veins відкриваються неправильно, тож звіряли за його текстом. Для лікування в групі обидва джерела беруть Gift of the Earthmother і Swiftmend і обидва згадують Nature’s Focus; Wowhead кладе в нього 5 очок. Далі у Wowhead уся гілка Зцілення: Gift of Nature 5, Reflection 3, Naturalist 5 і Nature’s Swiftness. Для світу Icy Veins радить інший шлях: спершу Improved Wrath і Insect Swarm з Балансу, потім Зцілення. З очками Legacy Wowhead бере Improved Tranquility: лікування групи без загрози з відкатом 2 хвилини.'),
            ]),
            ('steps', [
                {'t': t('Перед боем', 'Before the pull', 'Перед боєм'),
                 'd': t('Шипы на танка.', 'Thorns on the tank.', 'Thorns на танка.')},
                {'t': t('Омоложение', 'Rejuvenation', 'Rejuvenation'),
                 'd': t('Держать на танке и на всех, кто получает урон.', 'Keep it on the tank and on anyone taking damage.', 'Тримати на танку й на всіх, хто отримує шкоду.')},
                {'t': t('Восстановление', 'Regrowth', 'Regrowth'),
                 'd': t('Первое прямое лечение, затем низкие ранги Целительного прикосновения (Wowhead).', 'Your first direct heal, then low ranks of Healing Touch (Wowhead).', 'Перше пряме лікування, потім низькі ранги Healing Touch (Wowhead).')},
                {'t': t('Опасность', 'Danger', 'Небезпека'),
                 'd': t('Омоложение и через секунду Быстрое восстановление.', 'Rejuvenation, then Swiftmend a second later.', 'Rejuvenation і за секунду Swiftmend.')},
                {'t': t('Быстрое восстановление на откате', 'Swiftmend on cooldown', 'Swiftmend на відкаті'),
                 'd': t('Природная стремительность и Целительное прикосновение высшего ранга.', 'Nature’s Swiftness and a max-rank Healing Touch.', 'Nature’s Swiftness і Healing Touch найвищого рангу.')},
                {'t': t('Беда со всей группой', 'The whole group in trouble', 'Біда з усією групою'),
                 'd': t('Спокойствие.', 'Tranquility.', 'Tranquility.')},
            ]),
            ('tip', t('Характеристики по Icy Veins (для беты): интеллект, сила лечения, дух, мана раз в 5 секунд, крит. Свободную ману тратьте на урон: Гнев и Лунный огонь (Icy Veins).',
                      'Stats according to Icy Veins (for the beta): Intellect, healing power, Spirit, mana per 5 seconds, crit. Spend spare mana on damage: Wrath and Moonfire (Icy Veins).',
                      'Характеристики за Icy Veins (для бети): інтелект, сила лікування, дух, мана раз на 5 секунд, крит. Вільну ману витрачайте на шкоду: Wrath і Moonfire (Icy Veins).')),
        ]},
        {'id': 'faq', 'title': FAQ_T, 'blocks': [
            ('faq', [
                {'id': 'q1', 'q': t('Какой спек друида лучший?', 'Which Druid spec is best?', 'Яка спеціалізація друїда найкраща?'),
                 'a': [t('Для группы — Исцеление: в тир-листе беты A (у gamer-guides S). Кошка и медведь — B, Баланс — C.', 'For groups, Restoration: A on the beta tier list (S at gamer-guides). Cat and bear are B, Balance is C.', 'Для групи — Зцілення: у тір-листі бети A (у gamer-guides S). Кіт і ведмідь — B, Баланс — C.')]},
                {'id': 'q2', 'q': t('Может ли друид танковать в WoW Forever?', 'Can a Druid tank in WoW Forever?', 'Чи може друїд танкувати у WoW Forever?'),
                 'a': [t('Да, в облике медведя: Primal Bite, Размах и Исступление. В тир-листе беты медведь уступает Паладину и Воину.', 'Yes, in Bear Form: Primal Bite, Swipe and Enrage. On the beta tier list the bear trails Paladin and Warrior.', 'Так, у Bear Form: Primal Bite, Swipe і Enrage. У тір-листі бети ведмідь поступається Паладину й Воїну.')]},
                {'id': 'q3', 'q': t('Почему о друиде так мало данных?', 'Why is there so little Druid data?', 'Чому про друїда так мало даних?'),
                 'a': [t('Многое открывается после 30 уровня: Ураган — на 40, урона по площади у кошки пока нет. Билды к 60 появятся после старта.', 'Much of it unlocks after level 30: Hurricane comes at 40, and the cat has no area damage yet. Level 60 builds will follow after launch.', 'Багато відкривається після 30 рівня: Hurricane — на 40, шкоди по площі в кота поки немає. Білди до 60 з’являться після старту.')]},
                {'id': 'q4', 'q': WHEN_Q, 'a': [WHEN_A]},
            ]),
        ]},
        {'id': 'related', 'title': t('Смотрите также', 'See also', 'Дивіться також'), 'blocks': [
            ('tiles', _related('druid', [t('Друид', 'Druid', 'Друїд'), t('Прокачка Друида', 'Druid leveling', 'Прокачування Друїда')])),
        ]},
    ],
})

# anchor of each spec section, for links from the tier list (ru spec name in the tier table -> slug#id)
SPEC_LINKS = {'Паладин · Защита': 'builds-paladin/#protection', 'Паладин · Свет': 'builds-paladin/#holy',
              'Паладин · Воздаяние': 'builds-paladin/#retribution', 'Воин · Защита': 'builds-warrior/#protection',
              'Воин · Неистовство': 'builds-warrior/#fury', 'Воин · Оружие': 'builds-warrior/#arms',
              'Маг · Тайная магия': 'builds-mage/#arcane', 'Маг · Огонь': 'builds-mage/#fire', 'Маг · Лёд': 'builds-mage/#frost',
              'Охотник · Повелитель зверей': 'builds-hunter/#beast-mastery', 'Охотник · Стрельба': 'builds-hunter/#marksmanship',
              'Охотник · Выживание': 'builds-hunter/#survival', 'Разбойник · Ликвидация': 'builds-rogue/#assassination',
              'Разбойник · Бой': 'builds-rogue/#combat', 'Разбойник · Скрытность': 'builds-rogue/#subtlety',
              'Жрец · Послушание': 'builds-priest/#discipline', 'Жрец · Свет': 'builds-priest/#holy', 'Жрец · Темная магия': 'builds-priest/#shadow',
              'Шаман · Стихии': 'builds-shaman/#elemental', 'Шаман · Совершенствование': 'builds-shaman/#enhancement',
              'Шаман · Исцеление': 'builds-shaman/#restoration', 'Чернокнижник · Колдовство': 'builds-warlock/#affliction',
              'Чернокнижник · Демонология': 'builds-warlock/#demonology', 'Чернокнижник · Разрушение': 'builds-warlock/#destruction',
              'Друид · Баланс': 'builds-druid/#balance', 'Друид · Сила зверя (кошка)': 'builds-druid/#feral',
              'Друид · Сила зверя (медведь)': 'builds-druid/#feral', 'Друид · Исцеление': 'builds-druid/#restoration'}


def _link_specs(blocks):
    """Tier list «PvE по ролям»: the spec cell of a class with a builds page becomes a link to its section."""
    for kind, data in blocks:
        if kind == 'tabs':
            for tab in data:
                _link_specs(tab['blocks'])
        elif kind == 'table':
            for row in data['rows']:
                c = row[1]
                if isinstance(c, dict) and c.get('ru') in SPEC_LINKS:
                    row[1] = (c, f'guides/{SPEC_LINKS[c["ru"]]}')


def attach(guides, hubs, order):
    """Connect the build pages: tile texts of the related links, GUIDES, the «Билды по классам» section and the spec links of the tier list."""
    by = {g['slug']: g for g in guides}
    desc = {'classes/': {h['slug']: h for h in hubs}['classes']['tile'], 'guides/best-race/': by['best-race']['tile'],
            'guides/tier-list/': by['tier-list']['tile']}
    tiles = []
    for g in SPEC_BUILDS:
        cid = g['slug'].removeprefix('builds-')
        g['js'] = 'buildshare'                              # «Поделиться» under every spec heading (build_guides.JS)
        g['tile_art'] = cid                                  # «Другие гайды»: the class art (build_guides keeps one picture once)
        sec = g['sections'][-1]
        assert sec['id'] == 'related'
        for x in sec['blocks'][0][1]:
            h = x['href'].split('#')[0]
            x['d'] = desc['classes/'] if h.startswith('classes/') else by[h.removeprefix('guides/').strip('/')]['tile'] if h.startswith('guides/leveling-') else desc[h]
        tiles.append({'t': g['title'], 'd': g['tile'], 'href': f'guides/{g["slug"]}/', 'art': cid})
        titles = {s['id']: s['title'] for s in g['sections']}       # «Защита: танк» -> the tree «Защита» (talents.py cuts at the colon)
        for s in g['sections']:                                   # the talent tree opens the table of the spec (talents.py: nothing without data)
            if any(kind == 'tree' for kind, _ in s['blocks']):        # attach() may run twice (build.py and build_guides import it)
                continue
            for i, (kind, data) in enumerate(s['blocks']):
                if kind == 'table' and data['head'] is H_TAL:
                    s['blocks'].insert(i, ('tree', {'cls': cid, 'spec': s['id'], 'rows': data['rows'], 'titles': titles}))
                    break
    guides.extend(SPEC_BUILDS)
    tl = by['tier-list']['sections']
    pve = next(s for s in tl if s['id'] == 'pve')
    _link_specs(pve['blocks'])
    tl.insert(tl.index(pve) + 1, {'id': 'builds', 'title': BUILDS_TITLE, 'blocks': [('text', [BUILDS_LEAD]), ('tiles', tiles)]})
    guides.sort(key=lambda g: order.index(g['slug']))
