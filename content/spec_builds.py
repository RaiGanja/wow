"""Гайды «Билды <класса>»: страницы guides/builds-<класс>/, у каждого спека свой раздел с якорем (#protection, #fury…).
Строка = t(ru, en, uk); de, es, fr, it, pl, pt берутся из i18n/<lang>.json по английской строке (как в class_guides.py).
Названия: ru — как в клиенте ruRU (i18n/names.json, Wowhead ruRU), новые таланты Forever без ruRU — английские
(список: docs/wow/specs/texts-2026-10-25-spec-builds/names-todo.md); en/uk/pl — английские.
Правило текста: бета закрыта на 30 уровне, поэтому в таблицах только таланты и очки, в которых сходятся
Icy Veins и Wowhead (их билды 30 уровня, сверены по калькуляторам 25.10). Где они расходятся — это сказано словами,
без очков. Раскладку на 51 очко к 60 дадим после старта 04.11.
Источник текстов: docs/wow/specs/texts-2026-10-25-spec-builds (не в репо). attach() подключает страницы к GUIDES,
раздел «Билды по классам» в тир-листе, ссылки из тир-листа на разделы спеков и плитку хаба."""
from content.class_guides import t, tx

SPEC_BUILDS = []

BETA = tx('По бете', 'Beta data', 'За бетою', de='Betadaten', fr='Données de la bêta', pt='Dados da beta')
SPECS3 = t('3 спека', '3 specs', '3 спеціалізації')
LATER = t('Обновим после 04.11', 'Updated after Nov 4', 'Оновимо після 4 листопада')
H_TAL = [t('Талант', 'Talent', 'Талант'), t('Очки', 'Points', 'Очки'),
         tx('Зачем', 'Why', 'Навіщо', de='Wozu', es='Para qué', it='A cosa serve', pl='Po co', pt='Para quê')]
H_ROLES = [tx('Спек', 'Spec', 'Спек', de='Skillung', es='Espec.', fr='Spé', it='Spec.', pl='Spec', pt='Espec.'),
           t('Роль', 'Role', 'Роль'), t('Тир PvE', 'PvE tier', 'Тір PvE'), t('Главное', 'Key point', 'Головне')]
TANK, HEALER, DPS = t('Танк', 'Tank', 'Танк'), t('Лекарь', 'Healer', 'Цілитель'), t('Урон', 'Damage', 'Шкода')
FAQ_T = t('Вопросы', 'Questions', 'Питання')
WHEN_Q = t('Когда будет полный билд на 60?', 'When will the full level 60 build be out?', 'Коли буде повний білд на 60?')
WHEN_A = t('После старта 4 ноября: на бете был открыт только 30 уровень, рейды откроются 09.12. Тогда добавим раскладку на все 51 очко.',
           'After the Nov 4 launch: the beta only went up to level 30, and raids open on Dec 9. Then we will add the layout for all 51 points.',
           'Після старту 4 листопада: у беті був відкритий лише 30 рівень, рейди відкриються 9 грудня. Тоді додамо розкладку на всі 51 очко.')
ROLES_NOTE = t('Тиры — из тир-листа беты. В таблицах талантов только то, в чём сходятся Icy Veins и Wowhead; у каждого спека сказано, где они расходятся.',
               'Tiers come from the beta tier list. The talent tables show only what Icy Veins and Wowhead agree on; each spec says where they differ.',
               'Тіри — з тір-листа бети. У таблицях талантів лише те, у чому сходяться Icy Veins і Wowhead; для кожної спеціалізації сказано, де вони розходяться.')

BUILDS_TITLE = tx('Билды по классам', 'Builds by class', 'Білди за класами',
                  de='Builds nach Klasse', es='Builds por clase', fr='Builds par classe',
                  it='Build per classe', pl='Buildy według klas', pt='Builds por classe')
BUILDS_LEAD = tx('Таланты, приоритет и характеристики спеков к 60 уровню. Пока три класса; остальные шесть добавим после старта, по живым данным.',
                 'Talents, priorities and stats for each spec at level 60. Three classes for now; the other six will follow after launch, based on live data.',
                 'Таланти, пріоритет і характеристики спеціалізацій до 60 рівня. Поки три класи; решту шість додамо після старту, за живими даними.',
                 de='Talente, Prioritäten und Werte jeder Skillung für Stufe 60. Vorerst drei Klassen; die anderen sechs folgen nach dem Start mit Live-Daten.',
                 es='Talentos, prioridades y atributos de cada especialización a nivel 60. De momento, tres clases; las otras seis llegarán tras el lanzamiento, con datos reales.',
                 fr='Talents, priorités et caractéristiques de chaque spécialisation au niveau 60. Trois classes pour l’instant ; les six autres suivront après la sortie, d’après les données réelles.',
                 it='Talenti, priorità e statistiche di ogni specializzazione al livello 60. Per ora tre classi; le altre sei arriveranno dopo l’uscita, con dati reali.',
                 pl='Talenty, priorytety i statystyki każdej specjalizacji na 60 levelu. Na razie trzy klasy; pozostałe sześć dodamy po starcie, na podstawie danych z gry.',
                 pt='Talentos, prioridades e atributos de cada especialização no nível 60. Por enquanto, três classes; as outras seis virão após o lançamento, com dados reais.')
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
    'lead': t('Таланты, приоритет и характеристики Защиты, Света и Воздаяния. Бета была открыта до 30 уровня, поэтому здесь только то, в чём сходятся Icy Veins и Wowhead.',
              'Talents, priorities and stats for Protection, Holy and Retribution. The beta only went up to level 30, so this page shows only what Icy Veins and Wowhead agree on.',
              'Таланти, пріоритет і характеристики Захисту, Світла й Відплати. Бета була відкрита до 30 рівня, тож тут лише те, у чому сходяться Icy Veins і Wowhead.'),
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
                t('Здесь Icy Veins и Wowhead совпадают почти полностью. С пятью очками перка Legacy Talented оба берут Отмщение (Vengeance), Специализацию на двуручном оружии и одно очко Воитель Света (Champion of the Light): часть интеллекта идёт в силу заклинаний. Завершающий талант ветки — Изгиб Света (Twist of Light): после смены печати следующий удар ещё раз применяет старую.',
                  'Here Icy Veins and Wowhead match almost fully. With the five points of the Legacy Talented perk, both take Vengeance, Two-Handed Weapon Specialization and one point in Champion of the Light: part of your Intellect becomes spell power. The last talent of the tree is Twist of Light: after you switch seals, your next hit applies the old one once more.',
                  'Тут Icy Veins і Wowhead збігаються майже повністю. З п’ятьма очками перка Legacy Talented обидва беруть Vengeance, Two-Handed Weapon Specialization і одне очко Champion of the Light: частина інтелекту йде в силу заклинань. Останній талант гілки — Twist of Light: після зміни печатки наступний удар ще раз застосовує стару.'),
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
    'lead': t('Таланты, приоритет и характеристики Защиты, Неистовства и Оружия. Бета была открыта до 30 уровня, поэтому здесь только то, в чём сходятся Icy Veins и Wowhead.',
              'Talents, priorities and stats for Protection, Fury and Arms. The beta only went up to level 30, so this page shows only what Icy Veins and Wowhead agree on.',
              'Таланти, пріоритет і характеристики Захисту, Люті та Зброї. Бета була відкрита до 30 рівня, тож тут лише те, у чому сходяться Icy Veins і Wowhead.'),
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
                [t('Улучшенное кровопускание (Improved Rend)', 'Improved Rend', 'Improved Rend'), '3', t('Урон Кровопускания', 'Rend damage', 'Шкода Rend')],
                [t('Неукротимость (Defiance)', 'Defiance', 'Defiance'), '3', t('Больше угрозы в оборонительной стойке со щитом', 'More threat in Defensive Stance with a shield', 'Більше загрози в оборонній стійці зі щитом')],
            ]}),
            ('text', [
                t('Сходятся Icy Veins и Wowhead; Неукротимость Icy Veins советует для подземелий. Расходятся: Icy Veins добирает Improved Bloodrage и Безжалостность (Cruelty), Wowhead — Ни шагу назад (Last Stand). Для подземелий на капе оба советуют Сосредоточенную ярость (Focused Rage): удары дешевле.',
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
                t('Сходятся Icy Veins и Wowhead. Расходятся: Icy Veins берёт Отражение (Deflection), Wowhead — Improved Heroic Strike и Impale. Пять очков перка Legacy Talented оба отдают в Кровавый азарт (Bloodthrill): удары по цели с Кровопусканием иногда открывают Превосходство.',
                  'Icy Veins and Wowhead agree. They differ: Icy Veins takes Deflection, Wowhead takes Improved Heroic Strike and Impale. Both put the five Legacy Talented points into Bloodthrill: hits on a target with Rend sometimes enable Overpower.',
                  'Сходяться Icy Veins і Wowhead. Розходяться: Icy Veins бере Deflection, Wowhead — Improved Heroic Strike та Impale. П’ять очок перка Legacy Talented обидва віддають у Bloodthrill: удари по цілі з Rend іноді відкривають Overpower.'),
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
    'lead': t('Таланты, приоритет и характеристики Тайной магии, Огня и Льда. Бета была открыта до 30 уровня, поэтому здесь только то, в чём сходятся Icy Veins и Wowhead.',
              'Talents, priorities and stats for Arcane, Fire and Frost. The beta only went up to level 30, so this page shows only what Icy Veins and Wowhead agree on.',
              'Таланти, пріоритет і характеристики Тайної магії, Вогню та Льоду. Бета була відкрита до 30 рівня, тож тут лише те, у чому сходяться Icy Veins і Wowhead.'),
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
                t('Остальное Icy Veins и Wowhead собирают по-разному, а встроенный билд в гайде Wowhead не открывается. Общее правило у обоих: Средоточие чар (Arcane Focus) нужно против врагов выше вашего уровня — в подземельях и на боссах; если бьёте только врагов своего уровня, вместо него Improved Channeling. Icy Veins ещё берёт Чародейскую сосредоточенность (Arcane Concentration) 5 и Присутствие разума (Presence of Mind).',
                  'Icy Veins and Wowhead build the rest differently, and the embedded build in the Wowhead guide does not open. The rule both share: Arcane Focus is for enemies above your level, in dungeons and on bosses; if you only fight enemies of your level, take Improved Channeling instead. Icy Veins also takes Arcane Concentration 5 and Presence of Mind.',
                  'Решту Icy Veins і Wowhead збирають по-різному, а вбудований білд у гайді Wowhead не відкривається. Спільне правило в обох: Arcane Focus потрібне проти ворогів вище за ваш рівень — у підземеллях і на босах; якщо б’єте лише ворогів свого рівня, замість нього Improved Channeling. Icy Veins ще бере Arcane Concentration 5 і Presence of Mind.'),
            ]),
            ('steps', [
                {'t': t('Чародейская вспышка', 'Arcane Blast', 'Arcane Blast'),
                 'd': t('2–3 раза подряд. Дольше копить заряды — только на боссе.', '2–3 times in a row. Stack it longer only on a boss.', '2–3 рази поспіль. Довше накопичувати заряди — лише на босі.')},
                {'t': t('Заградительные стрелы', 'Missile Barrage', 'Missile Barrage'),
                 'd': t('Сработали — Чародейские снаряды.', 'When it procs, Arcane Missiles.', 'Спрацювало — Arcane Missiles.')},
                {'t': t('Нет срабатывания', 'No proc', 'Немає спрацювання'),
                 'd': t('После 2–3 вспышек — Огненный взрыв: заряды спадут, и мана перестанет утекать.', 'After 2–3 Blasts, Fire Blast: the stacks drop and the mana drain stops.', 'Після 2–3 Blast — Fire Blast: заряди спадуть, і мана перестане витікати.')},
                {'t': t('Группа под танком', 'A group on the tank', 'Група під танком'),
                 'd': t('Чародейский взрыв; Огненный столб заранее, если хватает маны.', 'Arcane Explosion; Flamestrike first if you have the mana.', 'Arcane Explosion; Flamestrike заздалегідь, якщо вистачає мани.')},
            ]),
            ('tip', t('Чародейская вспышка, Заградительные стрелы и Arcane Wrath — новые для Classic таланты. Icy Veins пишет, что на 60 меткость станет заметно важнее из-за рейдовых боссов.',
                      'Arcane Blast, Missile Barrage and Arcane Wrath are talents new to Classic. Icy Veins says hit will matter much more at 60 because of raid bosses.',
                      'Arcane Blast, Missile Barrage і Arcane Wrath — нові для Classic таланти. Icy Veins пише, що на 60 влучність стане помітно важливішою через рейдових босів.')),
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
                t('Сходятся Icy Veins и Wowhead. Воспламенение (Ignite) берут оба, но с разным числом очков. Улучшенный ожог (Improved Scorch) Wowhead берёт уже на 30, Icy Veins называет его почти обязательным к 60 для PvE. Расходятся: Icy Veins берёт Master of Elements, Wowhead — Critical Mass и Точность стихии (Elemental Precision).',
                  'Icy Veins and Wowhead agree. Both take Ignite, but with a different number of points. Wowhead takes Improved Scorch at 30 already, and Icy Veins calls it close to mandatory for PvE at 60. They differ: Icy Veins takes Master of Elements, Wowhead takes Critical Mass and Elemental Precision.',
                  'Сходяться Icy Veins і Wowhead. Ignite беруть обидва, але з різною кількістю очок. Improved Scorch Wowhead бере вже на 30, Icy Veins називає його майже обов’язковим до 60 для PvE. Розходяться: Icy Veins бере Master of Elements, Wowhead — Critical Mass і Elemental Precision.'),
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
                {'t': t('Группа под танком', 'A group on the tank', 'Група під танком'),
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
                t('Сходятся Icy Veins и Wowhead. Точность стихии (Elemental Precision) берут оба, но с разным числом очков. Icy Veins ещё берёт Обморожение (Frostbite), Ледяные осколки (Ice Shards), Обледенение (Shatter) и Направленную силу льда (Frost Channeling); Wowhead в тексте гайда советует Ледяную глыбу (Ice Block) и Холодную хватку (Cold Snap), а его встроенный билд не открывается.',
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

# anchor of each spec section, for links from the tier list (ru spec name in the tier table -> slug#id)
SPEC_LINKS = {'Паладин · Защита': 'builds-paladin/#protection', 'Паладин · Свет': 'builds-paladin/#holy',
              'Паладин · Воздаяние': 'builds-paladin/#retribution', 'Воин · Защита': 'builds-warrior/#protection',
              'Воин · Неистовство': 'builds-warrior/#fury', 'Воин · Оружие': 'builds-warrior/#arms',
              'Маг · Тайная магия': 'builds-mage/#arcane', 'Маг · Огонь': 'builds-mage/#fire', 'Маг · Лёд': 'builds-mage/#frost'}


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
        g['tile_art'] = cid                                  # «Другие гайды»: the class art (build_guides keeps one picture once)
        sec = g['sections'][-1]
        assert sec['id'] == 'related'
        for x in sec['blocks'][0][1]:
            h = x['href'].split('#')[0]
            x['d'] = desc['classes/'] if h.startswith('classes/') else by[h.removeprefix('guides/').strip('/')]['tile'] if h.startswith('guides/leveling-') else desc[h]
        tiles.append({'t': g['title'], 'd': g['tile'], 'href': f'guides/{g["slug"]}/', 'art': cid})
    guides.extend(SPEC_BUILDS)
    tl = by['tier-list']['sections']
    pve = next(s for s in tl if s['id'] == 'pve')
    _link_specs(pve['blocks'])
    tl.insert(tl.index(pve) + 1, {'id': 'builds', 'title': BUILDS_TITLE, 'blocks': [('text', [BUILDS_LEAD]), ('tiles', tiles)]})
    guides.sort(key=lambda g: order.index(g['slug']))
