"""Страницы подземелий guides/dungeons/<slug>/: шапка (уровни, вход, сторона, группа), «Что нужно группе», боссы по порядку
с тактикой по ролям, добыча по боссам (из data/gear30.json, нет данных — нет раздела), задания, ссылка на таблицу подземелий.

Новое подземелье = одна запись в DUNGEON_PAGES (тексты ru/en/uk через t(); de/fr/es/pt/it/pl — i18n/<lang>.json по английской
строке, сборка падает на непереведённом). Уровни, зона и сторона берутся из DUNGEONS (index.src.html) по полю 'name': там же
расхождения уровней с другими сайтами. Имена боссов, заданий и NPC — английские (lang="en"), пока нет клиента ruRU/ukUA.
Факты: где сайты расходятся, это пишется в 'split' босса или в тексте, а не прячется.
attach() кладёт страницы в GUIDES до langs.fill в build_guides; таблица guides/dungeons/ получает ссылки через table_links()."""
import ast
import json
import os
from html import escape

import build
import langs

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEAR30_PATH = os.environ.get('GABELLA_GEAR30') or os.path.join(HERE, 'data', 'gear30.json')   # the same file the spec sheets read


def t(ru, en, uk):
    return {'ru': ru, 'en': en, 'uk': uk}


def en(name):
    """A game name without a client translation: English on every page, marked so the ru name pass leaves it alone."""
    return f'<span lang="en">{escape(name)}</span>'


# ---------- labels ----------

SEC = {'about': t('Коротко', 'At a glance', 'Коротко'),
       'group': t('Что нужно группе', 'What the group needs', 'Що потрібно групі'),
       'bosses': t('Боссы по порядку', 'Bosses in order', 'Боси по черзі'),
       'loot': t('Добыча по боссам', 'Loot by boss', 'Здобич за босами'),
       'quests': t('Задания', 'Quests', 'Завдання')}
FACT = {'lv': t('Уровни', 'Levels', 'Рівні'), 'ent': t('Вход', 'Entrance', 'Вхід'), 'side': t('Сторона', 'Side', 'Сторона'),
        'group': t('Группа', 'Group', 'Група'), 'bosses': t('Боссы', 'Bosses', 'Боси'), 'loot': t('Добыча', 'Loot', 'Здобич')}
GROUP5 = t('5 игроков: танк, лекарь и трое в урон.', '5 players: a tank, a healer and three damage dealers.',
           '5 гравців: танк, цілитель і троє в шкоду.')
ROLES = (t('Танк', 'Tank', 'Танк'), t('Лекарь', 'Healer', 'Цілитель'), t('Урон', 'Damage', 'Шкода'))
SPLIT = t('По источникам расходится', 'Sources disagree', 'Джерела розходяться')
OPT = t('по событию, можно пропустить', 'event boss, optional', 'за подією, можна пропустити')
LAST = t('последний', 'final', 'останній')
RARE = t('редкий, появляется не всегда', 'rare, not always there', 'рідкісний, з’являється не завжди')
SKIP = t('можно пропустить', 'optional', 'можна пропустити')
SRC_LINE = t('Источник: официальные материалы Blizzard и данные беты. Где сайты расходятся, это подписано.',
             'Source: official Blizzard materials and beta data. Where sites disagree, it is noted.',
             'Джерело: офіційні матеріали Blizzard і дані бети. Де сайти розходяться, це підписано.')
XP_LINE = t('Опыт по данным беты: дополнительный опыт за задания подземелий Blizzard урезала вдвое (01.10), опыт за врагов в подземельях подняла примерно на 20% (08.10).',
            'Experience per beta data: Blizzard halved the extra experience from dungeon quests (Oct 1) and raised experience from dungeon enemies by about 20% (Oct 8).',
            'Досвід за даними бети: додатковий досвід за завдання підземель Blizzard урізала вдвічі (01.10), досвід за ворогів у підземеллях підняла приблизно на 20% (08.10).')
LOOT_WAIT = t('Ждёт данных: наш список предметов беты по спекам ещё не собран. Раздел появится вместе с ним.',
              'Waiting for data: our list of beta items by spec is not compiled yet. The section appears with it.',
              'Чекає на дані: наш список предметів бети за спеками ще не зібраний. Розділ з’явиться разом із ним.')
LOOT_GO = t('По боссам, с отметкой спеков', 'By boss, with the specs marked', 'За босами, з позначкою спеків')
LOOT_LEAD = t('Предметы, которые наш список экипировки 13–30 советует спекам, с этих боссов. Это не полный список добычи.',
              'Items from these bosses that our 13–30 gear list recommends to specs. This is not the full loot table.',
              'Предмети з цих босів, які наш список екіпірування 13–30 радить спекам. Це не повний список здобичі.')
LOOT_HEAD = (t('Предмет', 'Item', 'Предмет'), t('Ур.', 'Lvl', 'Рів.'), t('Для спеков', 'For specs', 'Для спеків'))
NEED_HEAD = (t('Что нужно', 'Need', 'Що потрібно'), t('Откуда', 'From', 'Звідки'), t('Как справиться', 'How to handle it', 'Як упоратися'))
QUEST_HEAD = (t('Задание', 'Quest', 'Завдання'), t('Где взять', 'Where to get it', 'Де взяти'), t('Для кого', 'For', 'Для кого'))
SIDE = {'alliance': t('Альянс', 'Alliance', 'Альянс'), 'horde': t('Орда', 'Horde', 'Орда'),
        'both': t('Обе фракции', 'Both factions', 'Обидві фракції')}
ALL_LINK = t('Все подземелья по уровням', 'All dungeons by level', 'Усі підземелля за рівнями')
PAGES_LABEL = t('Отдельные страницы: боссы по ролям, что нужно группе, задания.', 'Pages of their own: bosses by role, what the group needs, quests.',
                'Окремі сторінки: боси за ролями, що потрібно групі, завдання.')
GROUP_NEXT = t('Собрать группу и текст для поиска', 'Build a group and an LFG line', 'Зібрати групу й текст для пошуку')
TILE = t('Боссы по ролям, что нужно группе, задания', 'Bosses by role, what the group needs, quests', 'Боси за ролями, що потрібно групі, завдання')
SEO_TAIL = t('боссы, тактика, задания', 'Bosses, Tactics, Quests', 'боси, тактика, завдання')

BLIZZ_NOTES = 'https://eu.forums.blizzard.com/en/wow/t/wow-forever-beta-development-notes-%E2%80%93-updated-26-october/631316'

# ---------- the dungeons: one record each ----------
# name: the English name as in DUNGEONS · slug: guides/dungeons/<slug>/ · lv_note: where the level range comes from
# needs: (need, from, how) · bosses: name, abil, tank, heal, dps, split (optional), opt (event boss), rare (rare spawn),
#   skip (optional boss), last (final boss)
# quests: (name, where, side) with side 'alliance' | 'horde' | 'both'

DUNGEON_PAGES = [
    {'name': 'Hall of Thanes', 'slug': 'hall-of-thanes',
     'seo_ru': 'Hall of Thanes', 'pill': t('4 босса', '4 bosses', '4 боси'),
     'desc': t('Hall of Thanes (13–18) в WoW Forever: вход под Стальгорном, четыре босса с тактикой для танка, лекаря и урона, что снимать группе, пять заданий.',
               'Hall of Thanes (13–18) in WoW Forever: the entrance beneath Ironforge, four bosses with tank, healer and damage tactics, what to dispel, five quests.',
               'Hall of Thanes (13–18) у WoW Forever: вхід під Ironforge, чотири боси з тактикою для танка, цілителя й шкоди, що знімати групі, п’ять завдань.'),
     'lead': t('Новое подземелье Forever под [[Стальгорном|Ironforge]]: четыре босса, тактика для танка, лекаря и урона, что снимать группе, пять заданий.',
               'A new Forever dungeon beneath Ironforge: four bosses, tactics for the tank, healer and damage dealers, what the group must dispel, five quests.',
               'Нове підземелля Forever під Ironforge: чотири боси, тактика для танка, цілителя й шкоди, що знімати групі, п’ять завдань.'),
     'lv_note': t('По Warcraft Tavern и Icy Veins; Method даёт 13–20. Blizzard диапазон не публиковала.',
                  'Per Warcraft Tavern and Icy Veins; Method gives 13–20. Blizzard has not published a range.',
                  'За Warcraft Tavern та Icy Veins; Method дає 13–20. Blizzard діапазон не публікувала.'),
     'entrance': t('[[Стальгорн|Ironforge]], Old Ironforge под тронным залом. От Великой кузни идите в зал короля Магни, там налево в коридор с паутиной и вниз до входа. По пути лава, падение в неё смертельно.',
                   'Ironforge, Old Ironforge beneath the throne room. From the Great Forge walk into King Magni’s hall, take the cobwebbed passage on the left and go down to the entrance. There is lava on the way, and a fall into it is lethal.',
                   'Ironforge, Old Ironforge під тронною залою. Від Великої кузні йдіть до зали короля Магні, там ліворуч у коридор із павутиною й униз до входу. Дорогою лава, падіння в неї смертельне.'),
     'side': t('Альянс. Орда войти может, но идёт долго через земли Альянса. Из пяти заданий Орде доступны два по Icy Veins и Method; Warcraft Tavern пишет, что ни одного.',
               'Alliance. The Horde can enter but faces a long trip through Alliance lands. Two of the five quests are open to the Horde per Icy Veins and Method; Warcraft Tavern says none.',
               'Альянс. Орда може ввійти, але йде довго через землі Альянсу. З п’яти завдань Орді доступні два за Icy Veins і Method; Warcraft Tavern пише, що жодного.'),
     'boss_fact': t('4, порядок у трёх сайтов один.', '4, three sites give the same order.', '4, порядок у трьох сайтів однаковий.'),
     'boss_note': t('Kami-Labs первым боссом называет Infurnus, Warcraft Tavern, Icy Veins и Method — Faldrim Anvilmar. Здесь порядок трёх сайтов.',
                    'Kami-Labs names Infurnus as the first boss; Warcraft Tavern, Icy Veins and Method name Faldrim Anvilmar. The order here is that of the three sites.',
                    'Kami-Labs першим босом називає Infurnus, Warcraft Tavern, Icy Veins і Method — Faldrim Anvilmar. Тут порядок трьох сайтів.'),
     'needs': [
         (t('Снять проклятие', 'Remove a curse', 'Зняти прокляття'),
          t('Faldrim Anvilmar: Anvilmar’s Curse на танке, −20% к скорости атаки и заклинаний на 10 минут.',
            'Faldrim Anvilmar: Anvilmar’s Curse on the tank, −20% attack and casting speed for 10 minutes.',
            'Faldrim Anvilmar: Anvilmar’s Curse на танку, −20% до швидкості атаки й заклинань на 10 хвилин.'),
          t('Снимите, если в группе есть кому. Нет — танк живёт с ним, бой это не ломает.',
            'Remove it if someone in the group can. If not, the tank lives with it; the fight still works.',
            'Зніміть, якщо в групі є кому. Немає — танк живе з ним, бій це не ламає.')),
         (t('Снять болезнь', 'Cure a disease', 'Зняти хворобу'),
          t('Bloodhound Runt после первого босса: Infected Wounds, больше физического урона по цели на 5 минут.',
            'Bloodhound Runts after the first boss: Infected Wounds, more physical damage taken for 5 minutes.',
            'Bloodhound Runt після першого боса: Infected Wounds, більше фізичної шкоди по цілі на 5 хвилин.'),
          t('Снятие болезни, Simple Poultice из Первой помощи или Stoneform дворфа.',
            'A disease cure, a Simple Poultice from First Aid or the dwarf’s Stoneform.',
            'Зняття хвороби, Simple Poultice з Першої допомоги або Stoneform дворфа.')),
         (t('Сбить заклинание', 'Interrupt a cast', 'Збити заклинання'),
          t('Faldrim Anvilmar: Mind Blast. Dark Iron Summoner: Fireball и призыв огненного элементаля.',
            'Faldrim Anvilmar: Mind Blast. Dark Iron Summoner: Fireball and the summoning of a fire elemental.',
            'Faldrim Anvilmar: Mind Blast. Dark Iron Summoner: Fireball і виклик вогняного елементаля.'),
          t('Первым сбивайте призыв. Mind Blast можно и пропустить.', 'Interrupt the summoning first. Mind Blast can be let through.',
            'Першим збивайте виклик. Mind Blast можна й пропустити.')),
         (t('Защита от страха', 'Fear protection', 'Захист від страху'),
          t('Durgen Dirgehammer: страх на всю группу, 8 секунд.', 'Durgen Dirgehammer: a group-wide fear for 8 seconds.',
            'Durgen Dirgehammer: страх на всю групу, 8 секунд.'),
          t('Tremor Totem шамана. До боя зачистите зал, чтобы испуганные не притащили соседей.',
            'A shaman’s Tremor Totem. Clear the room before the pull so feared players do not drag in more enemies.',
            'Tremor Totem шамана. До бою зачистіть залу, щоб налякані не притягли сусідів.')),
         (t('Уйти из-под бомб', 'Step out of bombs', 'Відійти з-під бомб'),
          t('Dark Iron Engineer: динамит по цели угрозы, урон по площади.', 'Dark Iron Engineers: dynamite at their threat target, area damage.',
            'Dark Iron Engineer: динаміт по цілі загрози, шкода по площі.'),
          t('Бомба летит в точку с начала каста: отойдите, пока не упала.', 'The bomb is aimed at a spot when the cast starts: move before it lands.',
            'Бомба летить у точку з початку касту: відійдіть, доки не впала.')),
     ],
     'group_tip': t('Бочонки Seaforium Blasting Powder у групп Черного Железа взрываются от выстрела: дальний бой стреляет по ним до боя, и пак приходит уже раненым.',
                    'Kegs of Seaforium Blasting Powder next to the Dark Iron packs explode when shot: ranged players hit them before the pull, and the pack arrives already hurt.',
                    'Бочки Seaforium Blasting Powder біля груп Dark Iron вибухають від пострілу: далекий бій стріляє по них до бою, і пак приходить уже пораненим.'),
     'bosses': [
         {'name': 'Faldrim Anvilmar',
          'abil': t('Неупокоенный дворф, ходит вокруг своей гробницы в Anvilmar’s Rest. Mind Blast (прерывается) и Anvilmar’s Curse на танка.',
                    'An undead dwarf circling his tomb in Anvilmar’s Rest. Mind Blast (interruptible) and Anvilmar’s Curse on the tank.',
                    'Неупокоєний дворф, ходить довкола своєї гробниці в Anvilmar’s Rest. Mind Blast (переривається) і Anvilmar’s Curse на танка.'),
          'tank': t('Сначала зачистите призраков у гробницы, потом берите босса: соседей он сам не зовёт.',
                    'Clear the ghosts around the tomb first, then pull the boss: he does not call his neighbours.',
                    'Спершу зачистіть привидів біля гробниці, потім беріть боса: сусідів він сам не кличе.'),
          'heal': t('Урон небольшой. Проклятие висит 10 минут: снимите его хотя бы после боя.',
                    'Damage is low. The curse lasts 10 minutes: remove it at least after the fight.',
                    'Шкода невелика. Прокляття висить 10 хвилин: зніміть його хоча б після бою.'),
          'dps': t('Прерывайте Mind Blast, когда прерывание свободно.', 'Interrupt Mind Blast whenever your interrupt is free.',
                   'Переривайте Mind Blast, коли переривання вільне.')},
         {'name': 'Magmatus',
          'abil': t('Огненный элементаль, стоит вместе с Dark Iron Summoner. Пульсирующий огонь вокруг себя (Fire Nova), Combustion на случайного игрока.',
                    'A fire elemental standing with a Dark Iron Summoner. Pulsing fire around itself (Fire Nova), Combustion on a random player.',
                    'Вогняний елементаль, стоїть разом із Dark Iron Summoner. Пульсуючий вогонь довкола себе (Fire Nova), Combustion на випадкового гравця.'),
          'tank': t('Отведите Magmatus от группы и держите там, пока группа убивает призывателя.',
                    'Drag Magmatus away from the group and hold him there while the group kills the summoner.',
                    'Відведіть Magmatus від групи й тримайте там, поки група вбиває викликача.'),
          'heal': t('Лечите всех в ближнем бою, не только танка, и того, на ком Combustion.',
                    'Heal everyone in melee range, not just the tank, and whoever has Combustion.',
                    'Лікуйте всіх у ближньому бою, не лише танка, і того, на кому Combustion.'),
          'dps': t('Первым убейте Dark Iron Summoner. Дальний бой стоит подальше от босса, ближний следит за здоровьем.',
                   'Kill the Dark Iron Summoner first. Ranged players keep away from the boss, melee watch their health.',
                   'Першим убийте Dark Iron Summoner. Далекий бій стоїть подалі від боса, ближній стежить за здоров’ям.')},
         {'name': 'Plunder',
          'abil': t('Каменный голем, ходит по залу перед последним боссом. Одно умение: отбрасывание.',
                    'A stone golem patrolling the hall before the final boss. One ability: a knockback.',
                    'Кам’яний голем, ходить залою перед останнім босом. Одне вміння: відкидання.'),
          'tank': t('Встаньте спиной к стене или в угол, подальше от других групп, иначе отбросит прямо в них.',
                    'Stand with your back to a wall or in a corner, away from other packs, or the knockback throws you into them.',
                    'Станьте спиною до стіни або в кут, подалі від інших груп, інакше відкине просто в них.'),
          'heal': t('Бой простой. Стойте там, куда отброшенный танк не притянет новых врагов.',
                    'A simple fight. Stand where a knocked-back tank will not pull in more enemies.',
                    'Бій простий. Стійте там, куди відкинутий танк не притягне нових ворогів.'),
          'dps': t('Не стойте перед боссом. Ближние группы врагов зачистите заранее.', 'Do not stand in front of the boss. Clear nearby packs beforehand.',
                   'Не стійте перед босом. Ближні групи ворогів зачистіть заздалегідь.')},
         {'name': 'Durgen Dirgehammer', 'last': True,
          'abil': t('Вожак дворфов Черного Железа в Reliquary of Kings, с ним два Lesser Stone Golem. Страх на всю группу на 8 секунд, Rend на танке.',
                    'The Dark Iron leader in the Reliquary of Kings, with two Lesser Stone Golems. A group-wide fear for 8 seconds, Rend on the tank.',
                    'Ватажок дворфів Dark Iron у Reliquary of Kings, із ним два Lesser Stone Golem. Страх на всю групу на 8 секунд, Rend на танку.'),
          'tank': t('До боя зачистите весь зал: под страхом игроки разбегаются и тянут оставшихся врагов.',
                    'Clear the whole room before the pull: feared players run off and drag in the enemies left.',
                    'До бою зачистіть усю залу: під страхом гравці розбігаються й тягнуть ворогів, що лишилися.'),
          'heal': t('Rend даёт постоянный урон по танку. После страха первым поднимайте танка.',
                    'Rend is steady damage on the tank. After a fear, top up the tank first.',
                    'Rend дає постійну шкоду по танку. Після страху першим піднімайте танка.'),
          'dps': t('Големы бьют сильно и быстро, от них не убежать.', 'The golems hit hard and fast, and you cannot outrun them.',
                   'Големи б’ють сильно й швидко, від них не втекти.'),
          'split': t('кого бить первым. Warcraft Tavern и Icy Veins — сначала големов, Method — сначала Durgen.',
                     'who to kill first. Warcraft Tavern and Icy Veins: the golems first; Method: Durgen first.',
                     'кого бити першим. Warcraft Tavern і Icy Veins — спершу големів, Method — спершу Durgen.')},
     ],
     'boss_tip': t('В одном из склепов зала Durgen лежит табличка Treaty of Understanding: она даёт задание для короля Магни. На выходе сдайте An Ancient Grudge призраку у входа.',
                   'One of the vaults in Durgen’s room holds the Treaty of Understanding tablet: it starts a quest for King Magni. On the way out, turn in An Ancient Grudge to the ghost near the entrance.',
                   'В одному зі склепів зали Durgen лежить табличка Treaty of Understanding: вона дає завдання для короля Магні. На виході здайте An Ancient Grudge привиду біля входу.'),
     'quests': [
         ('Important Heirlooms', t('Thom Filch у входа в подземелье', 'Thom Filch just outside the dungeon', 'Thom Filch біля входу в підземелля'), 'alliance'),
         ('The Restless Dead', t('Afadra Dunwall, вверх по лестнице от входа', 'Afadra Dunwall, up the stairs from the entrance',
                                 'Afadra Dunwall, угору сходами від входу'), 'both'),
         ('Old Ironforge Incursion', t('Dark Iron Map с Dark Iron Spy в [[Дун Мороге|Dun Morogh]]', 'A Dark Iron Map from a Dark Iron Spy in Dun Morogh',
                                       'Dark Iron Map з Dark Iron Spy у Dun Morogh'), 'alliance'),
         ('An Ancient Grudge', t('Ghostly Attendant внутри подземелья', 'The Ghostly Attendant inside the dungeon', 'Ghostly Attendant усередині підземелля'), 'both'),
         ('The Treaty of Understanding', t('Табличка в склепе зала последнего босса', 'A tablet in a vault of the final boss room',
                                           'Табличка в склепі зали останнього боса'), 'alliance'),
     ],
     'quest_note': t('Для кого — по Icy Veins и Method; Warcraft Tavern пишет, что у Орды здесь заданий нет. Уровень заданий 14 (Method).',
                     'The “For” column follows Icy Veins and Method; Warcraft Tavern says the Horde has no quests here. Quest level 14 (Method).',
                     'Для кого — за Icy Veins і Method; Warcraft Tavern пише, що в Орди тут завдань немає. Рівень завдань 14 (Method).'),
     'sources': [
         ('Warcraft Tavern: Hall of Thanes', 'https://www.warcrafttavern.com/forever/guides/hall-of-thanes/'),
         (t('Warcraft Tavern: задания Hall of Thanes', 'Warcraft Tavern: Hall of Thanes quests', 'Warcraft Tavern: завдання Hall of Thanes'),
          'https://www.warcrafttavern.com/forever/guides/hall-of-thanes-quests/'),
         (t('Icy Veins: Hall of Thanes (19.10)', 'Icy Veins: Hall of Thanes (Oct 19)', 'Icy Veins: Hall of Thanes (19.10)'), 'https://www.icy-veins.com/wow-forever/hall-of-thanes-guide'),
         (t('Method: Hall of Thanes (15.10)', 'Method: Hall of Thanes (Oct 15)', 'Method: Hall of Thanes (15.10)'), 'https://www.method.gg/wow-forever/dungeons/hall-of-thanes'),
     ]},

    {'name': 'Ruins of Lordaeron', 'slug': 'ruins-of-lordaeron',
     'seo_ru': 'Руины Лордерона', 'pill': t('6 боссов', '6 bosses', '6 босів'),
     'desc': t('Руины Лордерона (Ruins of Lordaeron, 15–20) в WoW Forever: вход над Подгородом, шесть боссов с тактикой по ролям, что снимать группе, задания Орды и Альянса.',
               'Ruins of Lordaeron (15–20) in WoW Forever: the entrance above the Undercity, six bosses with tactics by role, what to dispel, Horde and Alliance quests.',
               'Ruins of Lordaeron (15–20) у WoW Forever: вхід над Undercity, шість босів із тактикою за ролями, що знімати групі, завдання Орди й Альянсу.'),
     'lead': t('Новое подземелье Forever над [[Подгородом|Undercity]]: шесть боссов, из них два по событию, тактика по ролям, что снимать группе, задания обеих фракций.',
               'A new Forever dungeon above the Undercity: six bosses, two of them event bosses, tactics by role, what the group must dispel, quests for both factions.',
               'Нове підземелля Forever над Undercity: шість босів, із них два за подією, тактика за ролями, що знімати групі, завдання обох фракцій.'),
     'lv_note': t('По Warcraft Tavern и Icy Veins; Method даёт 15–22. Blizzard диапазон не публиковала.',
                  'Per Warcraft Tavern and Icy Veins; Method gives 15–22. Blizzard has not published a range.',
                  'За Warcraft Tavern та Icy Veins; Method дає 15–22. Blizzard діапазон не публікувала.'),
     'entrance': t('Tirisfal Glades, над [[Подгородом|Undercity]]. Пройдите главные ворота руин и, не доходя до замка, поверните налево: вход наверху лестницы.',
                   'Tirisfal Glades, above the Undercity. Go through the main gate of the ruins and turn left before the keep: the entrance is up the stairs.',
                   'Tirisfal Glades, над Undercity. Пройдіть головну браму руїн і, не доходячи до замку, поверніть ліворуч: вхід угорі сходів.'),
     'side': t('Орда. Альянс тоже может войти, у него четыре своих задания, все внутри. Путь Альянса долгий: кораблём до Southshore в [[Предгорьях Хилсбрада|Hillsbrad Foothills]], дальше на север через [[Серебряный бор|Silverpine Forest]].',
               'Horde. The Alliance can enter too and has four quests of its own, all inside. The Alliance trip is long: by ship to Southshore in the Hillsbrad Foothills, then north through Silverpine Forest.',
               'Орда. Альянс теж може ввійти, у нього чотири свої завдання, усі всередині. Шлях Альянсу довгий: кораблем до Southshore у Hillsbrad Foothills, далі на північ через Silverpine Forest.'),
     'boss_fact': t('6: четыре по пути и два по событию. Ещё есть редкий Lordaeron Captain.',
                    '6: four on the way and two event bosses. There is also the rare Lordaeron Captain.',
                    '6: чотири по дорозі й два за подією. Ще є рідкісний Lordaeron Captain.'),
     'boss_note': t('Порядок прохода у Warcraft Tavern, Icy Veins и Method один. Редкий Lordaeron Captain иногда появляется на западе: Альянсу он дружелюбен, убить его может только Орда. По Icy Veins, он приходит после всех остальных боссов.',
                    'Warcraft Tavern, Icy Veins and Method give the same route. The rare Lordaeron Captain sometimes spawns in the west: he is friendly to the Alliance, only the Horde can kill him. Per Icy Veins, he comes after all the other bosses.',
                    'Порядок проходу у Warcraft Tavern, Icy Veins і Method однаковий. Рідкісний Lordaeron Captain іноді з’являється на заході: Альянсу він дружній, убити його може лише Орда. За Icy Veins, він приходить після всіх інших босів.'),
     'needs': [
         (t('Снять болезнь', 'Cure a disease', 'Зняти хворобу'),
          t('Нежить Плети: Ghoul Plague на 30 минут, медленнее бег и ниже урон.', 'Scourge undead: Ghoul Plague for 30 minutes, slower movement and lower damage.',
            'Нежить Scourge: Ghoul Plague на 30 хвилин, повільніший біг і нижча шкода.'),
          t('Снимайте сразу: полчаса с ней не пройти.', 'Cure it at once: you cannot play half an hour with it.', 'Знімайте одразу: пів години з нею не пройти.')),
         (t('Снять яд', 'Cure a poison', 'Зняти отруту'),
          t('Witherfang и Viktor the Vile: яд на танке. Пауки у входа.', 'Witherfang and Viktor the Vile: a poison on the tank. The spiders near the entrance.',
            'Witherfang і Viktor the Vile: отрута на танку. Павуки біля входу.'),
          t('Снимите, если есть чем. Без этого бой тоже проходится.', 'Cure it if you can. The fight works without it too.', 'Зніміть, якщо є чим. Без цього бій теж проходиться.')),
         (t('Снять проклятие', 'Remove a curse', 'Зняти прокляття'),
          t('Wailing Banshee: проклятие, ниже меткость.', 'Wailing Banshees: a curse that lowers hit chance.', 'Wailing Banshee: прокляття, нижча влучність.'),
          t('Снимите с танка и тех, кто бьёт оружием.', 'Remove it from the tank and weapon users.', 'Зніміть із танка й тих, хто б’є зброєю.')),
         (t('Развеять магию', 'Dispel magic', 'Розвіяти магію'),
          t('Skeletal Mage: Frost Armor на себе.', 'Skeletal Mages: Frost Armor on themselves.', 'Skeletal Mage: Frost Armor на собі.'),
          t('Развейте, и маги падают быстрее.', 'Dispel it and the mages go down faster.', 'Розвійте, і маги падають швидше.')),
         (t('Сбить заклинание', 'Interrupt a cast', 'Збити заклинання'),
          t('The Abandoned: Drain Life по танку. Rath’mael: Flamestrike.', 'The Abandoned: Drain Life on the tank. Rath’mael: Flamestrike.',
            'The Abandoned: Drain Life по танку. Rath’mael: Flamestrike.'),
          t('Прерывание или оглушение.', 'An interrupt or a stun.', 'Переривання або оглушення.')),
         (t('Запас маны', 'Mana to spare', 'Запас мани'),
          t('Viktor the Vile и The Abandoned приходят после волн врагов.', 'Viktor the Vile and The Abandoned come after waves of enemies.',
            'Viktor the Vile і The Abandoned приходять після хвиль ворогів.'),
          t('Начинайте событие с полной маной, держите зелья и бинты.', 'Start the event at full mana, with potions and bandages at hand.',
            'Починайте подію з повною маною, тримайте зілля й бинти.')),
         (t('Урон магией', 'Magic damage', 'Шкода магією'),
          t('Stone Watcher, горгульи на верхних ярусах: Stone Slumber, неуязвимы к физическому урону и лечатся.',
            'Stone Watchers, the gargoyles on the upper floors: Stone Slumber, immune to physical damage and healing.',
            'Stone Watcher, горгулі на верхніх ярусах: Stone Slumber, невразливі до фізичної шкоди й лікуються.'),
          t('В каменной фазе бейте заклинаниями.', 'Use spells during the stone phase.', 'У кам’яній фазі бийте заклинаннями.')),
     ],
     'group_tip': t('Умерли внутри — дух появится во дворе, а не у далёкого кладбища. Альянсу поэтому важнее всего дойти до входа живым.',
                    'If you die inside, your ghost appears in the courtyard, not at a distant graveyard. For the Alliance the hard part is reaching the entrance alive.',
                    'Загинули всередині — дух з’явиться в дворі, а не біля далекого цвинтаря. Альянсу тому найважливіше дійти до входу живим.'),
     'bosses': [
         {'name': 'Witherfang',
          'abil': t('Паучиха, ходит по King’s Alley у входа вместе с паучатами (Broodling). Яд на танке.',
                    'A spider patrolling King’s Alley near the entrance with her Broodlings. A poison on the tank.',
                    'Павучиха, ходить King’s Alley біля входу разом із павученятами (Broodling). Отрута на танку.'),
          'tank': t('По Warcraft Tavern, свой патруль она с собой не зовёт: выманите её одну издалека.',
                    'Per Warcraft Tavern, she does not bring her patrol along: pull her alone from range.',
                    'За Warcraft Tavern, свій патруль вона з собою не кличе: виманіть її саму здалеку.'),
          'heal': t('Яд на танке можно снять, но бой спокойно проходится и без этого.', 'The poison on the tank can be cured, but the fight is fine without it.',
                    'Отруту на танку можна зняти, але бій спокійно проходиться й без цього.'),
          'dps': t('Пришли паучата: Warcraft Tavern бьёт сначала их, Method — сначала босса.',
                   'If the Broodlings came along: Warcraft Tavern kills them first, Method the boss first.',
                   'Прийшли павученята: Warcraft Tavern б’є спершу їх, Method — спершу боса.')},
         {'name': 'The Baron',
          'abil': t('Охраняет пролом в стене. Сильный удар с отбрасыванием, урон по всем в ближнем бою. С него падают Abominable Head (задание Орды) и Head of the Baron (задание Альянса).',
                    'Guards a breach in the wall. A heavy blow with a knockback, damage to everyone in melee range. He drops the Abominable Head (Horde quest) and the Head of the Baron (Alliance quest).',
                    'Охороняє пролом у стіні. Сильний удар із відкиданням, шкода по всіх у ближньому бою. З нього падають Abominable Head (завдання Орди) і Head of the Baron (завдання Альянсу).'),
          'tank': t('Спиной к стене. После отбрасывания сразу возвращайте босса на себя.', 'Back to a wall. After a knockback, take the boss back at once.',
                    'Спиною до стіни. Після відкидання одразу повертайте боса на себе.'),
          'heal': t('Держите танка почти полным: по Method удар снимает около половины здоровья. Пока танк оглушён, босс бьёт следующего.',
                    'Keep the tank near full: per Method the blow takes about half of their health. While the tank is stunned, the boss hits the next player.',
                    'Тримайте танка майже повним: за Method удар знімає близько половини здоров’я. Поки танк оглушений, бос б’є наступного.'),
          'dps': t('Ближний бой — за спиной босса. Дальний стоит подальше и друг от друга, чтобы удар по площади не задел всех.',
                   'Melee stay behind the boss. Ranged keep their distance from him and from each other, so the area hit does not catch everyone.',
                   'Ближній бій — за спиною боса. Далекий стоїть подалі й одне від одного, щоб удар по площі не зачепив усіх.'),
          'split': t('что делает удар. Warcraft Tavern и Method — оглушение танка, Icy Veins — сброс угрозы.',
                     'what the blow does. Warcraft Tavern and Method: a stun on the tank; Icy Veins: a threat drop.',
                     'що робить удар. Warcraft Tavern і Method — оглушення танка, Icy Veins — скидання загрози.')},
         {'name': 'Viktor the Vile', 'opt': True,
          'abil': t('Событие: камин в сгоревшем доме на юго-западе. Пять волн нежити, потом Viktor. Сам бой простой, тот же яд, что у Witherfang.',
                    'Event: the fireplace in a burned-down house in the south-west. Five waves of undead, then Viktor. The fight itself is simple, with the same poison as Witherfang.',
                    'Подія: камін у згорілому будинку на південному заході. П’ять хвиль нежиті, потім Viktor. Сам бій простий, та сама отрута, що в Witherfang.'),
          'tank': t('Собирайте каждую волну на себя: передышки между ними почти нет.', 'Gather every wave on yourself: there is almost no break between them.',
                    'Збирайте кожну хвилю на себе: перепочинку між ними майже немає.'),
          'heal': t('Начинайте с полной маной: волны выпивают её ещё до Viktor.', 'Start at full mana: the waves drain it before Viktor shows up.',
                    'Починайте з повною маною: хвилі випивають її ще до Viktor.'),
          'dps': t('Бейте волны по площади и лечитесь сами. Слабой группе босса можно пропустить.', 'Hit the waves with area damage and heal yourselves. A weak group can skip this boss.',
                   'Бийте хвилі по площі й лікуйтеся самі. Слабкій групі боса можна пропустити.')},
         {'name': 'The Abandoned', 'opt': True,
          'abil': t('Событие: статуя с горящими глазами на площади. Три волны, потом босс. Frost Armor замедляет тех, кто бьёт его, Frost Nova держит на месте, Drain Life тянет здоровье танка.',
                    'Event: the statue with glowing eyes in the square. Three waves, then the boss. Frost Armor slows those who hit him, Frost Nova roots, Drain Life drains the tank.',
                    'Подія: статуя з палаючими очима на площі. Три хвилі, потім бос. Frost Armor сповільнює тих, хто його б’є, Frost Nova тримає на місці, Drain Life тягне здоров’я танка.'),
          'tank': t('Волны идут из коридоров с двух сторон. Кто застрял в коридоре, приведите сами, иначе событие встанет.',
                    'The waves come from corridors on both sides. Fetch anyone stuck in a corridor yourself, or the event stalls.',
                    'Хвилі йдуть із коридорів з двох боків. Хто застряг у коридорі, приведіть самі, інакше подія стане.'),
          'heal': t('Снова полная мана перед стартом. Drain Life бьёт по танку, пока его не прервут.', 'Full mana again before you start. Drain Life hits the tank until someone interrupts it.',
                    'Знову повна мана перед стартом. Drain Life б’є по танку, доки його не перервуть.'),
          'dps': t('Прерывание или оглушение берегите для [[Похищения жизни|Drain Life]]. Ближнему бою Frost Armor режет скорость.',
                   'Save an interrupt or a stun for Drain Life. Frost Armor slows the melee.',
                   'Переривання або оглушення бережіть для Drain Life. Ближньому бою Frost Armor ріже швидкість.')},
         {'name': 'Bjork',
          'abil': t('Ходит в северо-западной части. Anti-Magic Shield: короткий зелёный щит, под ним он неуязвим к заклинаниям.',
                    'Patrols the north-west part. Anti-Magic Shield: a short green bubble that makes him immune to spells.',
                    'Ходить у північно-західній частині. Anti-Magic Shield: короткий зелений щит, під ним він невразливий до заклинань.'),
          'tank': t('Сначала зачистите всё вокруг: вурдалаки рядом бьют больно.', 'Clear everything around first: the ghouls nearby hit hard.',
                    'Спершу зачистіть усе довкола: вурдалаки поруч б’ють боляче.'),
          'heal': t('Простой бой на танке.', 'A simple fight on the tank.', 'Простий бій на танку.'),
          'dps': t('Под щитом заклинатели ждут, оружие бьёт дальше. Щит держится около 3 секунд (Method).',
                   'Casters wait while the shield is up, weapons keep hitting. The shield lasts about 3 seconds (Method).',
                   'Під щитом заклиначі чекають, зброя б’є далі. Щит тримається близько 3 секунд (Method).'),
          'split': t('умение. Warcraft Tavern и Method — Anti-Magic Shield, Icy Veins — отбрасывание.',
                     'the ability. Warcraft Tavern and Method: Anti-Magic Shield; Icy Veins: a knockback.',
                     'уміння. Warcraft Tavern і Method — Anti-Magic Shield, Icy Veins — відкидання.')},
         {'name': 'Rath’mael', 'last': True,
          'abil': t('Скелет-маг в огороженной части кладбища. Flamestrike.', 'A skeleton mage in the fenced part of the graveyard. Flamestrike.',
                    'Скелет-маг в огородженій частині цвинтаря. Flamestrike.'),
          'tank': t('После каста [[Огненного столба|Flamestrike]] уводите босса из огня.', 'After a Flamestrike cast, move the boss out of the fire.',
                    'Після касту Flamestrike виводьте боса з вогню.'),
          'heal': t('Огонь бьёт ближний бой: лечите всех рядом с боссом.', 'The fire hits the melee: heal everyone near the boss.',
                    'Вогонь б’є ближній бій: лікуйте всіх поруч із босом.'),
          'dps': t('Не стойте рядом с танком на касте. Прервите или оглушите Flamestrike, если можете.',
                   'Do not stand next to the tank during the cast. Interrupt or stun Flamestrike if you can.',
                   'Не стійте поруч із танком на касті. Перервіть або оглушіть Flamestrike, якщо можете.'),
          'split': t('Flamestrike. Warcraft Tavern — огонь под танком, выйти; Icy Veins — прерывать или оглушать, плюс аура по ближнему бою; Method — выйти или оглушить.',
                     'Flamestrike. Warcraft Tavern: fire under the tank, step out; Icy Veins: interrupt or stun, plus an aura hitting the melee; Method: step out or stun.',
                     'Flamestrike. Warcraft Tavern — вогонь під танком, вийти; Icy Veins — переривати або оглушати, плюс аура по ближньому бою; Method — вийти або оглушити.')},
     ],
     'boss_tip': t('На кладбище после Rath’mael найдите тело Edward: оно нужно для заданий обеих фракций. Альянсу — выйти пешком, без камня возвращения, и сдать Head of the Baron капитану Truman у входа.',
                   'After Rath’mael, find Edward’s body in the graveyard: both factions need it for quests. Alliance players walk out instead of using the Hearthstone and hand the Head of the Baron to Captain Truman by the entrance.',
                   'На цвинтарі після Rath’mael знайдіть тіло Edward: воно потрібне для завдань обох фракцій. Альянсу — вийти пішки, без каменя повернення, і здати Head of the Baron капітану Truman біля входу.'),
     'quests': [
         ('Light’s Justice', t('Morbin Lightbane в [[Подгороде|Undercity]]', 'Morbin Lightbane in the Undercity', 'Morbin Lightbane в Undercity'), 'horde'),
         ('The New Plague', t('Theodore Griffs в [[Подгороде|Undercity]]', 'Theodore Griffs in the Undercity', 'Theodore Griffs в Undercity'), 'horde'),
         ('The Wrath of Rath’mael', t('Deathguard Kristof в [[Тирисфальских лесах|Tirisfal Glades]]', 'Deathguard Kristof in Tirisfal Glades',
                                      'Deathguard Kristof у Tirisfal Glades'), 'horde'),
         ('A Frightened Request', t('Tabetha Heartweaver в [[Серебряном бору|Silverpine Forest]]', 'Tabetha Heartweaver in Silverpine Forest',
                                    'Tabetha Heartweaver у Silverpine Forest'), 'horde'),
         ('Unending Torment', t('Abominable Head с The Baron', 'The Abominable Head from The Baron', 'Abominable Head із The Baron'), 'horde'),
         ('Abominable Creatures', t('Captain Truman внутри, у входа', 'Captain Truman inside, by the entrance', 'Captain Truman усередині, біля входу'), 'alliance'),
         ('Bloodied Insignia', t('Bloodied Insignia с нежити внутри', 'A Bloodied Insignia from the undead inside', 'Bloodied Insignia з нежиті всередині'), 'alliance'),
         ('Remember That I Love You', t('Crumpled Paper на кладбище у Rath’mael', 'A Crumpled Paper in the graveyard with Rath’mael',
                                        'Crumpled Paper на цвинтарі біля Rath’mael'), 'alliance'),
         ('Crest of Lordaeron', t('Сам герб, место случайное: за дверью у The Baron, в комнате на пути Bjork или на крышах с горгульями',
                                  'The crest itself, in a random spot: behind a door near The Baron, in a room on Bjork’s path or on the rooftops with the gargoyles',
                                  'Сам герб, місце випадкове: за дверима біля The Baron, у кімнаті на шляху Bjork або на дахах із горгулями'), 'both'),
     ],
     'quest_note': t('Названия — по Warcraft Tavern и Method; у задания из [[Серебряного бора|Silverpine Forest]] Method пишет другое имя (The Wrath of Rath’mael). A Frightened Request и Bloodied Insignia упомянуты в заметках беты Blizzard (01.10).',
                     'Names per Warcraft Tavern and Method; for the Silverpine Forest quest Method gives another name (The Wrath of Rath’mael). A Frightened Request and Bloodied Insignia appear in Blizzard’s beta notes (Oct 1).',
                     'Назви — за Warcraft Tavern і Method; для завдання із Silverpine Forest Method пише іншу назву (The Wrath of Rath’mael). A Frightened Request і Bloodied Insignia згадано в нотатках бети Blizzard (01.10).'),
     'sources': [
         ('Warcraft Tavern: The Ruins of Lordaeron', 'https://www.warcrafttavern.com/forever/guides/the-ruins-of-lordaeron/'),
         (t('Warcraft Tavern: задания Ruins of Lordaeron', 'Warcraft Tavern: Ruins of Lordaeron quests', 'Warcraft Tavern: завдання Ruins of Lordaeron'),
          'https://www.warcrafttavern.com/forever/guides/the-ruins-of-lordaeron-quests/'),
         (t('Icy Veins: Ruins of Lordaeron (19.10)', 'Icy Veins: Ruins of Lordaeron (Oct 19)', 'Icy Veins: Ruins of Lordaeron (19.10)'), 'https://www.icy-veins.com/wow-forever/ruins-of-lordaeron-guide'),
         (t('Method: Ruins of Lordaeron (15.10)', 'Method: Ruins of Lordaeron (Oct 15)', 'Method: Ruins of Lordaeron (15.10)'), 'https://www.method.gg/wow-forever/dungeons/ruins-of-lordaeron'),
     ]},
    {'name': 'Ragefire Chasm', 'slug': 'ragefire-chasm',
     'seo_ru': 'Огненная пропасть', 'pill': t('4 босса', '4 bosses', '4 боси'),
     'desc': t('Огненная пропасть (Ragefire Chasm, 13–18) в WoW Forever: вход в Оргриммаре, четыре босса с тактикой по ролям, что снимать, задания Орды.',
               'Ragefire Chasm (13–18) in WoW Forever: entrance in Orgrimmar, four bosses with tactics by role, what to dispel, Horde quests.',
               'Ragefire Chasm (13–18) у WoW Forever: вхід в Orgrimmar, чотири боси з тактикою за ролями, що знімати, завдання Орди.'),
     'lead': t('Первое подземелье Орды, прямо в [[Оргриммаре|Orgrimmar]]: четыре босса, тактика для танка, лекаря и урона, что снимать и сбивать, пять заданий.',
               'The Horde’s first dungeon, right inside Orgrimmar: four bosses, tactics for the tank, healer and damage dealers, what to dispel and interrupt, five quests.',
               'Перше підземелля Орди, просто в Orgrimmar: чотири боси, тактика для танка, цілителя й шкоди, що знімати й збивати, п’ять завдань.'),
     'lv_note': t('Warcraft Tavern и Method дают одно и то же. Blizzard диапазон не публиковала.',
                  'Warcraft Tavern and Method agree. Blizzard has not published a range.',
                  'Warcraft Tavern і Method збігаються. Blizzard діапазон не публікувала.'),
     'entrance': t('Orgrimmar, Cleft of Shadow в центре города, координаты 52.8, 49.6 (Warcraft Tavern). Внутри извилистая пещера с лавой и парой боковых проходов.',
                   'Orgrimmar, the Cleft of Shadow in the middle of the city, coordinates 52.8, 49.6 (Warcraft Tavern). Inside is a winding lava cave with a couple of side passages.',
                   'Orgrimmar, Cleft of Shadow у центрі міста, координати 52.8, 49.6 (Warcraft Tavern). Усередині звивиста печера з лавою й кількома бічними проходами.'),
     'side': t('Орда. Все задания ордынские. Warcraft Tavern пишет, что Альянс войти может, но на этих уровнях почти не доберётся; Method называет подземелье только ордынским. У Альянса на тех же уровнях Hall of Thanes.',
               'Horde. All quests are Horde quests. Warcraft Tavern says the Alliance can enter but can hardly get here at these levels; Method calls the dungeon Horde-only. The Alliance has Hall of Thanes at the same levels.',
               'Орда. Усі завдання ординські. Warcraft Tavern пише, що Альянс увійти може, але на цих рівнях майже не дістанеться; Method називає підземелля лише ординським. В Альянсу на тих самих рівнях Hall of Thanes.'),
     'boss_fact': t('4, порядок у Warcraft Tavern и Method один.', '4, Warcraft Tavern and Method give the same order.', '4, порядок у Warcraft Tavern і Method однаковий.'),
     'boss_note': t('Порядок прохода у обоих сайтов один. Расходятся они в том, кого бить первым у Jergosh the Invoker и Bazzalan.',
                    'Both sites give the same route. They disagree on who to kill first at Jergosh the Invoker and Bazzalan.',
                    'Порядок проходу в обох сайтів однаковий. Розходяться вони в тому, кого бити першим у Jergosh the Invoker і Bazzalan.'),
     'needs': [
         (t('Сбить заклинание', 'Interrupt a cast', 'Збити заклинання'),
          t('Ragefire Shaman: Healing Wave. Jergosh the Invoker: Immolate.', 'Ragefire Shamans: Healing Wave. Jergosh the Invoker: Immolate.',
            'Ragefire Shaman: Healing Wave. Jergosh the Invoker: Immolate.'),
          t('Шаманов прерывайте или оглушайте, иначе пак лечится. Immolate сбивайте, чтобы не горел танк.',
            'Interrupt or stun the shamans, or the pack heals up. Interrupt Immolate so the tank does not burn.',
            'Шаманів переривайте або оглушайте, інакше пак лікується. Immolate збивайте, щоб не горів танк.')),
         (t('Снять яд', 'Cure a poison', 'Зняти отруту'),
          t('Bazzalan: яд на цели угрозы.', 'Bazzalan: a poison on his threat target.', 'Bazzalan: отрута на цілі загрози.'),
          t('Снимайте с танка, если есть чем.', 'Cure it on the tank if you can.', 'Знімайте з танка, якщо є чим.')),
         (t('Снять проклятие', 'Remove a curse', 'Зняти прокляття'),
          t('Jergosh the Invoker: Curse of Weakness. Searing Blade Cultist: Curse of Agony на танке (Method).',
            'Jergosh the Invoker: Curse of Weakness. Searing Blade Cultists: Curse of Agony on the tank (Method).',
            'Jergosh the Invoker: Curse of Weakness. Searing Blade Cultist: Curse of Agony на танку (Method).'),
          t('Снимите, если в группе есть кому. Нет — лекарь просто лечит больше.', 'Remove it if someone in the group can. If not, the healer simply heals more.',
            'Зніміть, якщо в групі є кому. Немає — цілитель просто лікує більше.')),
         (t('Не упасть в лаву', 'Stay out of the lava', 'Не впасти в лаву'),
          t('Taragaman the Hungerer: Uppercut подбрасывает танка и отбрасывает назад.', 'Taragaman the Hungerer: Uppercut throws the tank up and back.',
            'Taragaman the Hungerer: Uppercut підкидає танка й відкидає назад.'),
          t('Танк держит босса в середине площадки, спиной не к лаве.', 'The tank holds the boss in the middle of the platform, back away from the lava.',
            'Танк тримає боса посередині майданчика, спиною не до лави.')),
         (t('Брать по одному паку', 'One pack at a time', 'Брати по одному паку'),
          t('Searing Blade Enforcer: Shield Slam оглушает танка на 2 секунды (Method).', 'Searing Blade Enforcers: Shield Slam stuns the tank for 2 seconds (Method).',
            'Searing Blade Enforcer: Shield Slam оглушує танка на 2 секунди (Method).'),
          t('Несколько сразу — и оглушения идут цепочкой. Паки здесь плотные.', 'Several at once and the stuns chain. The packs here are tight.',
            'Кілька одразу — і оглушення йдуть ланцюжком. Паки тут щільні.')),
     ],
     'group_tip': t('Шаманы и Searing Blade Warlock бьют издалека. Тяните их из-за угла: они подойдут сами и не поднимут соседей.',
                    'The shamans and Searing Blade Warlocks attack from range. Pull them around a corner: they come to you and do not wake their neighbours.',
                    'Шамани й Searing Blade Warlock б’ють здалеку. Тягніть їх з-за рогу: вони підійдуть самі й не піднімуть сусідів.'),
     'bosses': [
         {'name': 'Oggleflint',
          'abil': t('Вожак троггов, с ним два помощника. Cleave по тем, кто стоит перед ним (Method).',
                    'The trogg chieftain with two adds. Cleave on whoever stands in front of him (Method).',
                    'Ватажок троґів, із ним два помічники. Cleave по тих, хто стоїть перед ним (Method).'),
          'tank': t('Отверните босса от группы. Помощников держите на себе, пока их убивают.',
                    'Turn the boss away from the group. Hold the adds on yourself while they die.',
                    'Відверніть боса від групи. Помічників тримайте на собі, поки їх убивають.'),
          'heal': t('Лечите танка. Пока он собирает помощников, не перетяните их лечением.',
                    'Heal the tank. While he gathers the adds, do not pull them with your healing.',
                    'Лікуйте танка. Поки він збирає помічників, не перетягніть їх лікуванням.'),
          'dps': t('Сначала два помощника, потом босс. Перед боссом не стойте.', 'The two adds first, then the boss. Do not stand in front of him.',
                   'Спершу два помічники, потім бос. Перед босом не стійте.')},
         {'name': 'Taragaman the Hungerer',
          'abil': t('Демон на средней площадке, без помощников. Fire Nova по всем в ближнем бою, Uppercut подбрасывает танка (Method).',
                    'A demon on the middle platform, no adds. Fire Nova hits everyone in melee range, Uppercut throws the tank (Method).',
                    'Демон на середньому майданчику, без помічників. Fire Nova по всіх у ближньому бою, Uppercut підкидає танка (Method).'),
          'tank': t('Держите его в середине площадки, чтобы Uppercut не скинул в лаву. Патрули возьмите до босса.',
                    'Keep him in the middle of the platform so Uppercut does not throw you into the lava. Take the patrols before the boss.',
                    'Тримайте його посередині майданчика, щоб Uppercut не скинув у лаву. Патрулі візьміть до боса.'),
          'heal': t('Лечите танка и ближний бой после каждого [[Кольца огня|Fire Nova]].', 'Heal the tank, and the melee after each Fire Nova.',
                    'Лікуйте танка й ближній бій після Fire Nova.'),
          'dps': t('Простой бой: бейте босса и следите за угрозой. С него падает сердце для Slaying the Beast.',
                   'A simple fight: hit the boss and watch your threat. He drops the heart for Slaying the Beast.',
                   'Простий бій: бийте боса й стежте за загрозою. З нього падає серце для Slaying the Beast.')},
         {'name': 'Jergosh the Invoker',
          'abil': t('Чернокнижник Searing Blade, с ним два помощника. Immolate и Curse of Weakness.',
                    'A Searing Blade warlock with two adds. Immolate and Curse of Weakness.',
                    'Чорнокнижник Searing Blade, із ним два помічники. Immolate і Curse of Weakness.'),
          'tank': t('Сначала зачистите охрану на подходе, потом берите босса и обоих помощников.',
                    'Clear the guards on the way first, then pull the boss and both adds.',
                    'Спершу зачистіть охорону на підході, потім беріть боса й обох помічників.'),
          'heal': t('Урон по группе заметный: берегите ману.', 'The damage to the group adds up: save your mana.',
                    'Шкода по групі помітна: бережіть ману.'),
          'dps': t('Прерывайте Immolate, если класс умеет.', 'Interrupt Immolate if your class can.', 'Переривайте Immolate, якщо клас уміє.'),
          'split': t('кого бить первым. Warcraft Tavern — сначала помощников, Method — сначала Jergosh, он сильнее их.',
                     'who to kill first. Warcraft Tavern: the adds first; Method: Jergosh first, he is the strongest of the three.',
                     'кого бити першим. Warcraft Tavern — спершу помічників, Method — спершу Jergosh, він сильніший за них.')},
         {'name': 'Bazzalan', 'last': True,
          'abil': t('Сатир в верхней части пещеры, в самом конце, с двумя помощниками. Яд на цели угрозы и Sinister Strike.',
                    'A satyr in the upper part of the cave, at the very end, with two adds. A poison on his threat target and Sinister Strike.',
                    'Сатир у верхній частині печери, у самому кінці, із двома помічниками. Отрута на цілі загрози й Sinister Strike.'),
          'tank': t('Бьёт больно: начинайте бой, когда у лекаря полная мана.', 'He hits hard: start when the healer has full mana.',
                    'Б’є боляче: починайте бій, коли в цілителя повна мана.'),
          'heal': t('Снимайте яд с танка.', 'Cure the poison on the tank.', 'Знімайте отруту з танка.'),
          'dps': t('Бейте одну цель вместе, по метке танка.', 'Hit one target together, the one the tank marks.',
                   'Бийте одну ціль разом, за міткою танка.'),
          'split': t('кого бить первым. Warcraft Tavern — сначала помощников, Method — сначала Bazzalan, потом помощников.',
                     'who to kill first. Warcraft Tavern: the adds first; Method: Bazzalan first, then the adds.',
                     'кого бити першим. Warcraft Tavern — спершу помічників, Method — спершу Bazzalan, потім помічників.')},
     ],
     'boss_tip': t('Тело Maur Grimtotem для Searching for the Lost Satchel лежит в боковом проходе: на первой развилке направо, к Oggleflint. Jergosh и Bazzalan нужны для последней части Hidden Enemies.',
                   'Maur Grimtotem’s body for Searching for the Lost Satchel lies in a side passage: take the first right, towards Oggleflint. Jergosh and Bazzalan are needed for the last part of Hidden Enemies.',
                   'Тіло Maur Grimtotem для Searching for the Lost Satchel лежить у бічному проході: на першому розгалуженні праворуч, до Oggleflint. Jergosh і Bazzalan потрібні для останньої частини Hidden Enemies.'),
     'quests': [
         ('Testing an Enemy’s Strength', t('Rahauro в [[Громовом Утесе|Thunder Bluff]]', 'Rahauro in Thunder Bluff', 'Rahauro у Thunder Bluff'), 'horde'),
         ('Searching for the Lost Satchel', t('Rahauro в [[Громовом Утесе|Thunder Bluff]]', 'Rahauro in Thunder Bluff', 'Rahauro у Thunder Bluff'), 'horde'),
         ('Slaying the Beast', t('Neeru Fireblade, Cleft of Shadow в [[Оргриммаре|Orgrimmar]]', 'Neeru Fireblade, the Cleft of Shadow in Orgrimmar',
                                 'Neeru Fireblade, Cleft of Shadow в Orgrimmar'), 'horde'),
         ('The Power to Destroy…', t('Varimathras в [[Подгороде|Undercity]]', 'Varimathras in the Undercity', 'Varimathras в Undercity'), 'horde'),
         ('Hidden Enemies', t('Thrall в [[Оргриммаре|Orgrimmar]], цепочка', 'Thrall in Orgrimmar, a chain', 'Thrall в Orgrimmar, ланцюжок'), 'horde'),
     ],
     'quest_note': t('Уровень заданий 9 (Warcraft Tavern, Method). Hidden Enemies — цепочка от Thrall: знак Lieutenant’s Insignia с Burning Blade в Skull Rock, разговор с Neeru Fireblade, потом Jergosh и Bazzalan. Тело Maur Grimtotem даёт продолжение, Returning the Lost Satchel. По Warcraft Tavern, задания с классики почти не менялись.',
                     'Quest level 9 (Warcraft Tavern, Method). Hidden Enemies is a chain from Thrall: a Lieutenant’s Insignia from the Burning Blade in Skull Rock, a talk with Neeru Fireblade, then Jergosh and Bazzalan. Maur Grimtotem’s body gives the follow-up, Returning the Lost Satchel. Per Warcraft Tavern, the quests are much as they were in Classic.',
                     'Рівень завдань 9 (Warcraft Tavern, Method). Hidden Enemies — ланцюжок від Thrall: знак Lieutenant’s Insignia з Burning Blade у Skull Rock, розмова з Neeru Fireblade, потім Jergosh і Bazzalan. Тіло Maur Grimtotem дає продовження, Returning the Lost Satchel. За Warcraft Tavern, завдання з класики майже не змінилися.'),
     'sources': [
         ('Warcraft Tavern: Ragefire Chasm', 'https://www.warcrafttavern.com/forever/guides/ragefire-chasm/'),
         (t('Warcraft Tavern: задания [[Огненной пропасти|Ragefire Chasm]]', 'Warcraft Tavern: Ragefire Chasm quests', 'Warcraft Tavern: завдання Ragefire Chasm'),
          'https://www.warcrafttavern.com/forever/guides/ragefire-chasm-quests/'),
         (t('Method: Ragefire Chasm (12.10)', 'Method: Ragefire Chasm (Oct 12)', 'Method: Ragefire Chasm (12.10)'), 'https://www.method.gg/wow-forever/dungeons/ragefire-chasm'),
     ]},
    {'name': 'The Deadmines', 'slug': 'the-deadmines',
     'seo_ru': 'Мертвые копи', 'pill': t('8 боссов', '8 bosses', '8 босів'),
     'desc': t('Мертвые копи (The Deadmines, 15–22) в WoW Forever: вход в Moonbrook, восемь боссов с тактикой для танка, лекаря и урона, кого бить первым, семь заданий Альянса.',
               'The Deadmines (15–22) in WoW Forever: entrance in Moonbrook, eight bosses with tactics by role, who to kill first, Alliance quests.',
               'The Deadmines (15–22) у WoW Forever: вхід у Moonbrook, вісім босів із тактикою для танка, цілителя й шкоди, кого бити першим, сім завдань Альянсу.'),
     'lead': t('Шахты братства Defias под [[Западным Краем|Westfall]]: восемь боссов до корабля VanCleef, тактика по ролям, кого бить первым, семь заданий Альянса.',
               'The Defias Brotherhood’s mines beneath Westfall: eight bosses up to VanCleef’s ship, tactics by role, who to kill first, seven Alliance quests.',
               'Шахти братства Defias під Westfall: вісім босів до корабля VanCleef, тактика за ролями, кого бити першим, сім завдань Альянсу.'),
     'lv_note': t('По Warcraft Tavern; Method и Icy Veins дают 17–26. Blizzard диапазон не публиковала.',
                  'Per Warcraft Tavern; Method and Icy Veins give 17–26. Blizzard has not published a range.',
                  'За Warcraft Tavern; Method та Icy Veins дають 17–26. Blizzard діапазон не публікувала.'),
     'entrance': t('Westfall, Moonbrook: большое здание Defias в юго-западном углу деревни, около 42, 72 (Warcraft Tavern). Внутри лабиринт пещер, портал в самом низу.',
                   'Westfall, Moonbrook: the large Defias building in the south-west corner of the village, around 42, 72 (Warcraft Tavern). Inside is a maze of caves with the portal at the bottom.',
                   'Westfall, Moonbrook: велика будівля Defias у південно-західному куті села, близько 42, 72 (Warcraft Tavern). Усередині лабіринт печер, портал у самому низу.'),
     'side': t('Альянс. Орда войти может, но заданий у неё здесь нет, а дорога долгая: дирижаблем из [[Дуротара|Durotar]] в Grom’gol, оттуда вплавь на север, в обход врагов [[Тернистой долины|Stranglethorn Vale]] (Method).',
               'Alliance. The Horde can enter but has no quests here, and the trip is long: by zeppelin from Durotar to Grom’gol, then swim north past the enemies of Stranglethorn Vale (Method).',
               'Альянс. Орда може ввійти, але завдань у неї тут немає, а дорога довга: дирижаблем із Durotar до Grom’gol, звідти вплав на північ, в обхід ворогів Stranglethorn Vale (Method).'),
     'boss_fact': t('8, из них редкий Miner Johnson и необязательный Cookie.', '8, including the rare Miner Johnson and the optional Cookie.',
                    '8, із них рідкісний Miner Johnson і необов’язковий Cookie.'),
     'boss_note': t('Порядок у Warcraft Tavern и Method один, кроме Cookie: Method ставит его перед Captain Greenskin, Warcraft Tavern — после VanCleef, на выходе. Captain Greenskin убейте раньше VanCleef: вместе они почти наверняка кладут группу (Warcraft Tavern).',
                    'Warcraft Tavern and Method give the same order except for Cookie: Method puts him before Captain Greenskin, Warcraft Tavern after VanCleef, on the way out. Kill Captain Greenskin before VanCleef: the two together almost always wipe the group (Warcraft Tavern).',
                    'Порядок у Warcraft Tavern і Method однаковий, крім Cookie: Method ставить його перед Captain Greenskin, Warcraft Tavern — після VanCleef, на виході. Captain Greenskin убийте раніше за VanCleef: разом вони майже напевно кладуть групу (Warcraft Tavern).'),
     'needs': [
         (t('Быстро убить охрану', 'Kill the guards fast', 'Швидко вбити охорону'),
          t('Mr. Smite и Edwin VanCleef: рядом по два Defias Blackguard в незаметности. Smite Stomp оглушает всех рядом.',
            'Mr. Smite and Edwin VanCleef: two stealthed Defias Blackguards beside each. Smite Stomp stuns everyone nearby.',
            'Mr. Smite і Edwin VanCleef: поруч по два Defias Blackguard у непомітності. Smite Stomp оглушує всіх поруч.'),
          t('Охрану бейте первой: оглушение при живой охране быстро убивает (Method).', 'Kill the guards first: a stun with the guards alive kills fast (Method).',
            'Охорону бийте першою: оглушення при живій охороні швидко вбиває (Method).')),
         (t('Сбить заклинание', 'Interrupt a cast', 'Збити заклинання'),
          t('Cookie: Cookie’s Cooking лечит его. Defias Evoker: Flamestrike по месту, где стоит танк.',
            'Cookie: Cookie’s Cooking heals him. Defias Evokers: Flamestrike on the spot where the tank stands.',
            'Cookie: Cookie’s Cooking лікує його. Defias Evoker: Flamestrike по місцю, де стоїть танк.'),
          t('Cookie’s Cooking сбивайте всегда. Flamestrike прерывайте, не успели — выходите из огня.', 'Always interrupt the Cooking. Interrupt Flamestrike; if you miss it, step out of the fire.',
            'Cooking збивайте завжди. Flamestrike переривайте, не встигли — виходьте з вогню.')),
         (t('Снять замедление', 'Remove a slow', 'Зняти сповільнення'),
          t('Gilnid: Molten Metal на танке.', 'Gilnid: Molten Metal on the tank.', 'Gilnid: Molten Metal на танку.'),
          t('По Method это урон и −50% к скорости бега, снимает Blessing of Freedom паладина. Warcraft Tavern пишет, что Molten Metal режет угрозу танка.',
            'Per Method it is damage and −50% movement speed, removed by a paladin’s Blessing of Freedom. Warcraft Tavern says Molten Metal cuts the tank’s threat.',
            'За Method це шкода й −50% до швидкості бігу, знімає Blessing of Freedom паладина. Warcraft Tavern пише, що Molten Metal ріже загрозу танка.')),
         (t('Снять яд', 'Cure a poison', 'Зняти отруту'),
          t('Captain Greenskin: Poisoned Harpoon на танке (Method).', 'Captain Greenskin: Poisoned Harpoon on the tank (Method).',
            'Captain Greenskin: Poisoned Harpoon на танку (Method).'),
          t('Снимите, если есть чем.', 'Cure it if you can.', 'Зніміть, якщо є чим.')),
         (t('Страх', 'Fear', 'Страх'),
          t('Sneed’s Shredder: Terrify (Method).', 'Sneed’s Shredder: Terrify (Method).', 'Sneed’s Shredder: Terrify (Method).'),
          t('Зачистите комнату с Goblin Woodcarver до боя, чтобы испуганные не притащили новых.',
            'Clear the Goblin Woodcarvers from the room before the pull so feared players do not bring more.',
            'Зачистіть кімнату з Goblin Woodcarver до бою, щоб налякані не притягли нових.')),
     ],
     'group_tip': t('Паки здесь плотные (Method). Контроль вроде [[Превращения|Polymorph]] на одного из охраны облегчает почти каждый бой, начиная с Defias Watchman у Rhahk’zor.',
                    'The packs here are tight (Method). Crowd control such as Polymorph on one of the guards eases almost every fight, starting with the Defias Watchmen at Rhahk’zor.',
                    'Паки тут щільні (Method). Контроль на кшталт Polymorph на одного з охорони полегшує майже кожен бій, починаючи з Defias Watchman біля Rhahk’zor.'),
     'bosses': [
         {'name': 'Rhahk’zor',
          'abil': t('Огр у первой двери, с ним два Defias Watchman, бьют издалека (Warcraft Tavern). Rhahk’Zor Slam оглушает на 3 секунды (Method).',
                    'An ogre at the first door with two Defias Watchmen who attack from range (Warcraft Tavern). Rhahk’Zor Slam stuns for 3 seconds (Method).',
                    'Огр біля перших дверей, із ним два Defias Watchman, б’ють здалеку (Warcraft Tavern). Rhahk’Zor Slam оглушує на 3 секунди (Method).'),
          'tank': t('По Method его можно вытянуть без охраны. Взяли охрану — отметьте её и держите на себе.',
                    'Per Method he can be pulled without the guards. If they come, mark them and hold them on yourself.',
                    'За Method його можна витягти без охорони. Узяли охорону — позначте її й тримайте на собі.'),
          'heal': t('Бой на танке. Пока он собирает охрану, не перетяните её лечением.', 'A fight on the tank. While he gathers the guards, do not pull them with your healing.',
                    'Бій на танку. Поки він збирає охорону, не перетягніть її лікуванням.'),
          'dps': t('Сначала Defias Watchman, потом босс. На одного можно Polymorph.', 'The Defias Watchmen first, then the boss. One can be polymorphed.',
                   'Спершу Defias Watchman, потім бос. На одного можна Polymorph.')},
         {'name': 'Miner Johnson', 'rare': True,
          'abil': t('Может не появиться. Стоит слева на развилке за дверью Rhahk’zor, вокруг Defias Miner. Pierce Armor на танке (Method).',
                    'May not spawn. Stands on the left at the junction past Rhahk’zor’s door, with Defias Miners around. Pierce Armor on the tank (Method).',
                    'Може не з’явитися. Стоїть ліворуч на розгалуженні за дверима Rhahk’zor, довкола Defias Miner. Pierce Armor на танку (Method).'),
          'tank': t('Бой на танке. Шахтёров рядом возьмите до него.', 'A fight on the tank. Take the miners nearby before him.',
                    'Бій на танку. Шахтарів поруч візьміть до нього.'),
          'heal': t('Pierce Armor снижает броню танка: лечите плотнее.', 'Pierce Armor lowers the tank’s armor: heal more closely.',
                    'Pierce Armor знижує броню танка: лікуйте щільніше.'),
          'dps': t('Бейте босса. Шахтёры, если пришли, по Method — после него.', 'Hit the boss. Miners who joined go after him, per Method.',
                   'Бийте боса. Шахтарі, якщо прийшли, за Method — після нього.')},
         {'name': 'Sneed’s Shredder',
          'abil': t('Гоблин Sneed в машине-лесорубе. Terrify (страх) и Distracting Pain. Машина ломается — выходит Sneed и бьёт Disarm по цели угрозы.',
                    'The goblin Sneed in a shredder. Terrify (a fear) and Distracting Pain. When the shredder breaks, Sneed climbs out and casts Disarm on his threat target.',
                    'Гоблін Sneed у машині-лісорубі. Terrify (страх) і Distracting Pain. Машина ламається — виходить Sneed і б’є Disarm по цілі загрози.'),
          'tank': t('Держите угрозу: по Warcraft Tavern, Distracting Pain переходит на других, если танк её теряет. Вышел Sneed — у него новая угроза, сразу провоцируйте.',
                    'Hold threat: per Warcraft Tavern, Distracting Pain spreads to others if the tank loses it. Once Sneed is out, his threat is fresh: taunt him at once.',
                    'Тримайте загрозу: за Warcraft Tavern, Distracting Pain переходить на інших, якщо танк її втрачає. Вийшов Sneed — у нього нова загроза, одразу провокуйте.'),
          'heal': t('Бой на танке. Под Disarm танк держит угрозу хуже.', 'A fight on the tank. Under Disarm the tank holds threat worse.',
                    'Бій на танку. Під Disarm танк тримає загрозу гірше.'),
          'dps': t('Сломали машину — сразу на Sneed, но после первого удара танка.', 'Once the shredder breaks, switch to Sneed, after the tank’s first hit.',
                   'Зламали машину — одразу на Sneed, але після першого удару танка.')},
         {'name': 'Gilnid',
          'abil': t('Гоблин в литейной, с ним Goblin Craftsman и Goblin Engineer. Molten Metal на танке.',
                    'A goblin in the foundry with a Goblin Craftsman and a Goblin Engineer. Molten Metal on the tank.',
                    'Гоблін у ливарні, із ним Goblin Craftsman і Goblin Engineer. Molten Metal на танку.'),
          'tank': t('До боя зачистите хотя бы одну сторону комнаты (Warcraft Tavern).', 'Clear at least one side of the room before the pull (Warcraft Tavern).',
                    'До бою зачистіть хоча б один бік кімнати (Warcraft Tavern).'),
          'heal': t('Лечите танка и не перетяните помощников лечением.', 'Heal the tank and do not pull the adds with your healing.',
                    'Лікуйте танка й не перетягніть помічників лікуванням.'),
          'dps': t('Не тяните лишнего: в комнате тесно.', 'Do not pull extra: the room is crowded.', 'Не тягніть зайвого: у кімнаті тісно.'),
          'split': t('что делает Molten Metal и кого бить первым. Warcraft Tavern — режет угрозу танка, сначала помощников; Method — урон и замедление на 50%, сначала Gilnid.',
                     'what Molten Metal does and who to kill first. Warcraft Tavern: it cuts the tank’s threat, adds first; Method: damage and a 50% slow, Gilnid first.',
                     'що робить Molten Metal і кого бити першим. Warcraft Tavern — ріже загрозу танка, спершу помічників; Method — шкода й сповільнення на 50%, спершу Gilnid.')},
         {'name': 'Mr. Smite',
          'abil': t('Таурен-пират у корабля, рядом два Defias Blackguard в незаметности. Три фазы, на переходах Smite Stomp оглушает всех рядом; во второй фазе он с двумя оружиями и бьёт заметно сильнее (Warcraft Tavern).',
                    'A tauren pirate by the ship with two stealthed Defias Blackguards. Three phases; at each change Smite Stomp stuns everyone nearby; in the second phase he dual-wields and hits much harder (Warcraft Tavern).',
                    'Таурен-пірат біля корабля, поруч два Defias Blackguard у непомітності. Три фази, на переходах Smite Stomp оглушує всіх поруч; у другій фазі він із двома зброями й б’є помітно сильніше (Warcraft Tavern).'),
          'tank': t('Отметьте охрану. Защитные способности берегите на вторую фазу.', 'Mark the guards. Save your defensive cooldowns for the second phase.',
                    'Позначте охорону. Захисні вміння бережіть на другу фазу.'),
          'heal': t('Пока убивают охрану, берегите ману: во второй фазе урон по танку резко растёт.', 'Save mana while the guards die: in the second phase the damage on the tank jumps.',
                    'Поки вбивають охорону, бережіть ману: у другій фазі шкода по танку різко зростає.'),
          'dps': t('Обоих Defias Blackguard — до босса.', 'Both Defias Blackguards before the boss.', 'Обох Defias Blackguard — до боса.')},
         {'name': 'Cookie', 'skip': True,
          'abil': t('Повар на корабле, ходит по левой стороне после Mr. Smite. Acid Splash по цели угрозы, Cookie’s Cooking лечит его. С него падает Cookie’s Stirring Rod, жезл для заклинателей.',
                    'The ship’s cook, walking the left side after Mr. Smite. Acid Splash on his threat target, Cookie’s Cooking heals him. He drops Cookie’s Stirring Rod, a wand for casters.',
                    'Кухар на кораблі, ходить лівим боком після Mr. Smite. Acid Splash по цілі загрози, Cookie’s Cooking лікує його. З нього падає Cookie’s Stirring Rod, жезл для заклиначів.'),
          'tank': t('Не тяните его вместе с пиратами. Прерывайте Cookie’s Cooking, если можете.', 'Do not pull him together with the pirates. Interrupt the Cooking if you can.',
                    'Не тягніть його разом із піратами. Переривайте Cooking, якщо можете.'),
          'heal': t('Бой на танке.', 'A fight on the tank.', 'Бій на танку.'),
          'dps': t('Прерывайте Cookie’s Cooking, иначе бой затянется.', 'Interrupt Cookie’s Cooking, or the fight drags on.',
                   'Переривайте Cookie’s Cooking, інакше бій затягнеться.')},
         {'name': 'Captain Greenskin',
          'abil': t('Гоблин-капитан на палубе, с ним Defias Squallshaper, Defias Pirate и Defias Companion. Cleave и Poisoned Harpoon на танке (Method). Его легко зацепить случайно (Warcraft Tavern).',
                    'The goblin captain on deck with a Defias Squallshaper, a Defias Pirate and a Defias Companion. Cleave and Poisoned Harpoon on the tank (Method). He is easy to pull by accident (Warcraft Tavern).',
                    'Гоблін-капітан на палубі, із ним Defias Squallshaper, Defias Pirate і Defias Companion. Cleave і Poisoned Harpoon на танку (Method). Його легко зачепити випадково (Warcraft Tavern).'),
          'tank': t('Подходите осторожно и отметьте помощников. Cleave отверните от группы.', 'Approach carefully and mark the adds. Turn the Cleave away from the group.',
                    'Підходьте обережно й позначте помічників. Cleave відверніть від групи.'),
          'heal': t('Пока убивают помощников, берегите ману. Яд с танка снимайте.', 'Save mana while the adds die. Cure the poison on the tank.',
                    'Поки вбивають помічників, бережіть ману. Отруту з танка знімайте.'),
          'dps': t('Бейте по меткам танка.', 'Follow the tank’s marks.', 'Бийте за мітками танка.'),
          'split': t('кого бить первым. Warcraft Tavern — двух помощников, потом капитана; Method — сначала Defias Companion, потом капитана, потом остальных.',
                     'who to kill first. Warcraft Tavern: two adds, then the captain; Method: the Defias Companion first, then the captain, then the rest.',
                     'кого бити першим. Warcraft Tavern — двох помічників, потім капітана; Method — спершу Defias Companion, потім капітана, потім решту.')},
         {'name': 'Edwin VanCleef', 'last': True,
          'abil': t('Вожак Defias на верхней палубе, рядом два Defias Blackguard в незаметности. Thrash; на половине здоровья зовёт ещё двоих (VanCleef’s Allies). С него падает An Unsent Letter.',
                    'The Defias leader on the top deck with two stealthed Defias Blackguards. Thrash; at half health he calls two more (VanCleef’s Allies). He drops An Unsent Letter.',
                    'Ватажок Defias на верхній палубі, поруч два Defias Blackguard у непомітності. Thrash; на половині здоров’я кличе ще двох (VanCleef’s Allies). З нього падає An Unsent Letter.'),
          'tank': t('Сначала Captain Greenskin. Первых двух охранников держите на себе, пока их убивают.', 'Captain Greenskin first. Hold the first two guards on yourself while they die.',
                    'Спершу Captain Greenskin. Перших двох охоронців тримайте на собі, поки їх убивають.'),
          'heal': t('Бой долгий, урон по танку высокий: следите за маной.', 'A long fight with heavy damage on the tank: watch your mana.',
                    'Бій довгий, шкода по танку висока: стежте за маною.'),
          'dps': t('Первую пару охраны убейте быстро. Вторую — под контроль или оставьте и добивайте VanCleef (Warcraft Tavern). По Method, оглушение в момент половины здоровья срывает призыв.',
                   'Kill the first pair of guards fast. Control the second pair or leave it and finish VanCleef (Warcraft Tavern). Per Method, a stun right at half health stops the summon.',
                   'Першу пару охорони вбийте швидко. Другу — під контроль або залиште й добивайте VanCleef (Warcraft Tavern). За Method, оглушення в момент половини здоров’я зриває виклик.')},
     ],
     'boss_tip': t('С VanCleef падают An Unsent Letter (начало The Unsent Letter) и его голова для The Defias Brotherhood. Cookie удобно убить на выходе: после VanCleef спуститесь на нижнюю палубу к трапу.',
                   'VanCleef drops An Unsent Letter (it starts The Unsent Letter) and his head for The Defias Brotherhood. Cookie is easy to kill on the way out: after VanCleef, drop to the lower deck towards the gangplank.',
                   'З VanCleef падають An Unsent Letter (початок The Unsent Letter) і його голова для The Defias Brotherhood. Cookie зручно вбити на виході: після VanCleef спустіться на нижню палубу до трапа.'),
     'quests': [
         ('Collecting Memories', t('Wilder Thistlenettle, Dwarven District в [[Штормграде|Stormwind City]]', 'Wilder Thistlenettle, the Dwarven District in Stormwind',
                                   'Wilder Thistlenettle, Dwarven District у Stormwind'), 'alliance'),
         ('Oh Brother…', t('Wilder Thistlenettle, Dwarven District в [[Штормграде|Stormwind City]]', 'Wilder Thistlenettle, the Dwarven District in Stormwind',
                           'Wilder Thistlenettle, Dwarven District у Stormwind'), 'alliance'),
         ('Underground Assault', t('Shoni the Shilent, Dwarven District в [[Штормграде|Stormwind City]]', 'Shoni the Shilent, the Dwarven District in Stormwind',
                                   'Shoni the Shilent, Dwarven District у Stormwind'), 'alliance'),
         ('Red Silk Bandanas', t('Scout Riell, Sentinel Hill в [[Западном Крае|Westfall]]', 'Scout Riell, Sentinel Hill in Westfall', 'Scout Riell, Sentinel Hill у Westfall'), 'alliance'),
         ('The Defias Brotherhood', t('Gryan Stoutmantle, Sentinel Hill', 'Gryan Stoutmantle, Sentinel Hill', 'Gryan Stoutmantle, Sentinel Hill'), 'alliance'),
         ('Destruction in Deadmines', t('Alba Fairmoon, Sentinel Hill', 'Alba Fairmoon, Sentinel Hill', 'Alba Fairmoon, Sentinel Hill'), 'alliance'),
         ('The Unsent Letter', t('An Unsent Letter с Edwin VanCleef', 'An Unsent Letter from Edwin VanCleef', 'An Unsent Letter з Edwin VanCleef'), 'alliance'),
     ],
     'quest_note': t('Все задания для Альянса (Warcraft Tavern, Method). Collecting Memories и Oh Brother… делаются у входа, снаружи подземелья. Red Silk Bandanas и The Defias Brotherhood открываются цепочкой Defias в Sentinel Hill, Destruction in Deadmines — цепочкой Testing the Wells. Warcraft Tavern пишет, что Forever добавила одну новую цепочку, но не называет её; Destruction in Deadmines в классике не было. Классовые задания паладинов сюда не внесены.',
                     'All quests are for the Alliance (Warcraft Tavern, Method). Collecting Memories and Oh Brother… are done near the entrance, outside the dungeon. Red Silk Bandanas and The Defias Brotherhood open with the Defias chain at Sentinel Hill, Destruction in Deadmines with the Testing the Wells chain. Warcraft Tavern says Forever added one new chain but does not name it; Destruction in Deadmines was not in Classic. Paladin class quests are not listed here.',
                     'Усі завдання для Альянсу (Warcraft Tavern, Method). Collecting Memories і Oh Brother… робляться біля входу, ззовні підземелля. Red Silk Bandanas і The Defias Brotherhood відкриваються ланцюжком Defias у Sentinel Hill, Destruction in Deadmines — ланцюжком Testing the Wells. Warcraft Tavern пише, що Forever додала один новий ланцюжок, але не називає його; Destruction in Deadmines у класиці не було. Класові завдання паладинів сюди не внесено.'),
     'sources': [
         ('Warcraft Tavern: The Deadmines', 'https://www.warcrafttavern.com/forever/guides/the-deadmines/'),
         (t('Warcraft Tavern: задания [[Мертвых копей|The Deadmines]]', 'Warcraft Tavern: The Deadmines quests', 'Warcraft Tavern: завдання The Deadmines'),
          'https://www.warcrafttavern.com/forever/guides/the-deadmines-quests/'),
         (t('Method: The Deadmines (21.10)', 'Method: The Deadmines (Oct 21)', 'Method: The Deadmines (21.10)'), 'https://www.method.gg/wow-forever/dungeons/the-deadmines'),
     ]},
    {'name': 'Wailing Caverns', 'slug': 'wailing-caverns',
     'seo_ru': 'Пещеры Стенаний', 'pill': t('9 боссов', '9 bosses', '9 босів'),
     'desc': t('Пещеры Стенаний (Wailing Caverns, 17–24) в WoW Forever: вход в Степях, девять боссов с тактикой по ролям, событие Naralex, задания.',
               'Wailing Caverns (17–24) in WoW Forever: entrance in The Barrens, nine bosses with tactics by role, the Naralex event, quests.',
               'Wailing Caverns (17–24) у WoW Forever: вхід у The Barrens, дев’ять босів із тактикою за ролями, подія Naralex, завдання.'),
     'lead': t('Пещеры друидов Клыка в [[Степях|The Barrens]]: девять боссов, тактика по ролям, событие с учеником Naralex, что сбивать и снимать, семь заданий.',
               'The Druids of the Fang’s caves in The Barrens: nine bosses, tactics by role, the Disciple of Naralex event, what to interrupt and cure, seven quests.',
               'Печери друїдів Ікла в The Barrens: дев’ять босів, тактика за ролями, подія з учнем Naralex, що збивати й знімати, сім завдань.'),
     'lv_note': t('По Warcraft Tavern; Method и Icy Veins дают 15–24. Blizzard диапазон не публиковала.',
                  'Per Warcraft Tavern; Method and Icy Veins give 15–24. Blizzard has not published a range.',
                  'За Warcraft Tavern; Method та Icy Veins дають 15–24. Blizzard діапазон не публікувала.'),
     'entrance': t('The Barrens, пещера в оазисе Lushwater Oasis, около 46.0, 36.3 (Warcraft Tavern; Method называет место Forgotten Pools). Через внешнюю пещеру с патрулями элиты вниз к озеру, там портал.',
                   'The Barrens, a cave at Lushwater Oasis, around 46.0, 36.3 (Warcraft Tavern; Method calls the spot the Forgotten Pools). Through the outer cave with elite patrols down to the pool, where the portal is.',
                   'The Barrens, печера в оазі Lushwater Oasis, близько 46.0, 36.3 (Warcraft Tavern; Method називає місце Forgotten Pools). Через зовнішню печеру з патрулями еліти вниз до озера, там портал.'),
     'side': t('Орда: два задания только для неё, пять для обеих фракций. Альянс войти может, но путь долгий: кораблём из Menethil Harbor в Theramore и дальше к Ratchet или из Booty Bay кораблём в Ratchet (Method).',
               'Horde: two quests are Horde-only, five are for both factions. The Alliance can enter, but the trip is long: by ship from Menethil Harbor to Theramore and on to Ratchet, or from Booty Bay by ship to Ratchet (Method).',
               'Орда: два завдання лише для неї, п’ять для обох фракцій. Альянс може ввійти, але шлях довгий: кораблем із Menethil Harbor до Theramore й далі до Ratchet або з Booty Bay кораблем до Ratchet (Method).'),
     'boss_fact': t('9, из них редкий Deviate Faerie Dragon. Последний, Mutanus, приходит по событию.', '9, including the rare Deviate Faerie Dragon. The last one, Mutanus, comes with an event.',
                    '9, із них рідкісний Deviate Faerie Dragon. Останній, Mutanus, приходить за подією.'),
     'boss_note': t('Пещеры не линейные. Порядок здесь по Method; Warcraft Tavern первым ставит Kresh, он плавает по ручью и встречается когда угодно. Mutanus появляется, только когда убиты четыре друида: Anacondra, Cobrahn, Pythas и Serpentis.',
                    'The caves are not linear. The order here is Method’s; Warcraft Tavern puts Kresh first, he swims along the stream and can turn up at any time. Mutanus appears only once the four druids are dead: Anacondra, Cobrahn, Pythas and Serpentis.',
                    'Печери не лінійні. Порядок тут за Method; Warcraft Tavern першим ставить Kresh, він плаває струмком і трапляється будь-коли. Mutanus з’являється, лише коли вбито чотирьох друїдів: Anacondra, Cobrahn, Pythas і Serpentis.'),
     'needs': [
         (t('Сбить сон', 'Interrupt the sleep', 'Збити сон'),
          t('Друиды Клыка и четыре босса-друида: Druid’s Slumber, сон на 8 секунд, бьёт и по лекарю. Ещё Lightning Bolt и Healing Touch.',
            'The Druids of the Fang and the four druid bosses: Druid’s Slumber, an 8-second sleep that can hit the healer. Also Lightning Bolt and Healing Touch.',
            'Друїди Ікла й чотири боси-друїди: Druid’s Slumber, сон на 8 секунд, б’є й по цілителю. Ще Lightning Bolt і Healing Touch.'),
          t('Сначала сон, потом лечение, потом молнию (Method). Распределите прерывания до боя.', 'The sleep first, then the heal, then the bolt (Method). Assign interrupts before the pull.',
            'Спершу сон, потім лікування, потім блискавку (Method). Розподіліть переривання до бою.')),
         (t('Снять яд', 'Cure a poison', 'Зняти отруту'),
          t('Deviate Viper: Localized Toxin на цели угрозы. Lord Cobrahn в облике змеи (Warcraft Tavern).', 'Deviate Vipers: Localized Toxin on their threat target. Lord Cobrahn in serpent form (Warcraft Tavern).',
            'Deviate Viper: Localized Toxin на цілі загрози. Lord Cobrahn у подобі змії (Warcraft Tavern).'),
          t('Снимайте с танка, если есть чем: яда здесь много.', 'Cure it on the tank if you can: there is a lot of poison here.', 'Знімайте з танка, якщо є чим: отрути тут багато.')),
         (t('Страх', 'Fear', 'Страх'),
          t('Deviate Dreadfang и Mutanus the Devourer: Terrify.', 'Deviate Dreadfangs and Mutanus the Devourer: Terrify.', 'Deviate Dreadfang і Mutanus the Devourer: Terrify.'),
          t('На Mutanus лекарь стоит подальше, чтобы страх и оглушение доставали реже.', 'At Mutanus the healer stays far back, so the fear and stun reach them less often.',
            'На Mutanus цілитель стоїть подалі, щоб страх і оглушення діставали рідше.')),
         (t('Стоять врозь и вдали', 'Spread out and keep away', 'Стояти нарізно й далеко'),
          t('Skum: Chained Bolt. Verdan the Everliving: Grasping Vines держит на месте всех в 10 метрах (Warcraft Tavern).',
            'Skum: Chained Bolt. Verdan the Everliving: Grasping Vines roots everyone within 10 yards (Warcraft Tavern).',
            'Skum: Chained Bolt. Verdan the Everliving: Grasping Vines тримає на місці всіх у 10 метрах (Warcraft Tavern).'),
          t('На Skum разойдитесь. На Verdan дальний бой и лекарь стоят дальше 10 метров.', 'Spread out at Skum. At Verdan the ranged and the healer stay beyond 10 yards.',
            'На Skum розійдіться. На Verdan далекий бій і цілитель стоять далі 10 метрів.')),
         (t('Урон магией', 'Magic damage', 'Шкода магією'),
          t('Kresh: высокая броня. Skum: неуязвим к урону природой (Warcraft Tavern).', 'Kresh: high armor. Skum: immune to Nature damage (Warcraft Tavern).',
            'Kresh: висока броня. Skum: невразливий до шкоди природою (Warcraft Tavern).'),
          t('Заклинатели бьют Kresh лучше оружия. На Skum урон природой не работает.', 'Casters hurt Kresh more than weapons do. Nature damage does nothing to Skum.',
            'Заклиначі б’ють Kresh краще за зброю. На Skum шкода природою не працює.')),
     ],
     'group_tip': t('Пещеры путаные, местами надо прыгать через провалы. Ученик Naralex (Disciple of Naralex) ждёт у входа: событие лучше начинать после полной зачистки (Method), путь к нему тогда свободен.',
                    'The caves are a maze, with gaps to jump in places. The Disciple of Naralex waits at the entrance: start the event after a full clear (Method), so the way is free.',
                    'Печери заплутані, подекуди треба стрибати через провалля. Учень Naralex (Disciple of Naralex) чекає біля входу: подію краще починати після повної зачистки (Method), шлях тоді вільний.'),
     'bosses': [
         {'name': 'Lady Anacondra',
          'abil': t('Друид Клыка, обычно первая: ходит в начальных пещерах. Lightning Bolt, Healing Touch, Sleep и Thorns Aura, которая возвращает урон бьющим вплотную.',
                    'A Druid of the Fang, usually the first: she patrols the opening caves. Lightning Bolt, Healing Touch, Sleep and Thorns Aura, which returns damage to melee attackers.',
                    'Друїдка Ікла, зазвичай перша: ходить у початкових печерах. Lightning Bolt, Healing Touch, Sleep і Thorns Aura, що повертає шкоду тим, хто б’є впритул.'),
          'tank': t('Отведите её от других групп. Сон на танка не действует (Warcraft Tavern).', 'Pull her away from other packs. Sleep is not cast on the tank (Warcraft Tavern).',
                    'Відведіть її від інших груп. Сон на танка не діє (Warcraft Tavern).'),
          'heal': t('Лечите группу, прежде всего танка. Thorns Aura не снимается.', 'Heal the group, the tank first. Thorns Aura cannot be purged.',
                    'Лікуйте групу, передусім танка. Thorns Aura не знімається.'),
          'dps': t('Прерывайте Sleep, Healing Touch и [[Молнию|Lightning Bolt]]. Ближний бой получает урон от шипов.', 'Interrupt Sleep, Healing Touch and Lightning Bolt. Melee take damage from the thorns.',
                   'Переривайте Sleep, Healing Touch і Lightning Bolt. Ближній бій отримує шкоду від шипів.')},
         {'name': 'Kresh',
          'abil': t('Черепаха, плавает по ручью. Сильные физические удары и Bite, высокая броня.', 'A turtle swimming along the stream. Heavy physical hits and Bite, high armor.',
                    'Черепаха, плаває струмком. Сильні фізичні удари й Bite, висока броня.'),
          'tank': t('Отверните его от группы, защитные способности держите под рукой.', 'Turn him away from the group and keep your defensive cooldowns ready.',
                    'Відверніть його від групи, захисні вміння тримайте напоготові.'),
          'heal': t('Держите танка полным.', 'Keep the tank topped up.', 'Тримайте танка повним.'),
          'dps': t('Простой бой. Заклинатели бьют его лучше, чем оружие.', 'A simple fight. Casters hurt him more than weapons do.',
                   'Простий бій. Заклиначі б’ють його краще, ніж зброя.')},
         {'name': 'Lord Cobrahn',
          'abil': t('Друид Клыка в Pit of Fangs, с ним Deviate Python. Lightning Bolt, Healing Touch, Druid’s Slumber; ближе к смерти принимает облик змеи и бьёт ядом.',
                    'A Druid of the Fang in the Pit of Fangs with Deviate Pythons. Lightning Bolt, Healing Touch, Druid’s Slumber; near death he takes serpent form and uses poison.',
                    'Друїд Ікла в Pit of Fangs, із ним Deviate Python. Lightning Bolt, Healing Touch, Druid’s Slumber; ближче до смерті набуває подоби змії й б’є отрутою.'),
          'tank': t('Держите угрозу. Уснул лекарь — продержитесь на защитных способностях.', 'Hold threat. If the healer is asleep, survive on your defensive cooldowns.',
                    'Тримайте загрозу. Заснув цілитель — протримайтеся на захисних уміннях.'),
          'heal': t('Сон держит 8 секунд: заранее повесьте на танка лечение со временем.', 'The sleep lasts 8 seconds: keep heals over time on the tank in advance.',
                    'Сон тримає 8 секунд: заздалегідь повісьте на танка лікування з часом.'),
          'dps': t('Питонов добейте по площади, потом босса. Druid’s Slumber сбивайте раньше [[Целительного прикосновения|Healing Touch]] (Method).',
                   'Finish the pythons with area damage, then the boss. Interrupt Druid’s Slumber before Healing Touch (Method).',
                   'Пітонів добийте по площі, потім боса. Druid’s Slumber збивайте раніше за Healing Touch (Method).')},
         {'name': 'Deviate Faerie Dragon', 'rare': True,
          'abil': t('Появляется изредка в разных местах пещер. Своих умений почти нет; по Method, рядом пара друидов Клыка со сном.',
                    'Spawns now and then in different parts of the caves. Hardly any abilities of its own; per Method, a couple of Druids of the Fang with the sleep stand nearby.',
                    'З’являється зрідка в різних місцях печер. Своїх умінь майже немає; за Method, поруч пара друїдів Ікла зі сном.'),
          'tank': t('Держите угрозу на драконе и на друидах.', 'Hold threat on the dragon and the druids.', 'Тримайте загрозу на драконі й на друїдах.'),
          'heal': t('Лечите танка, следите за сном.', 'Heal the tank and watch for the sleep.', 'Лікуйте танка, стежте за сном.'),
          'dps': t('Сначала друиды, потом дракон (Method).', 'The druids first, then the dragon (Method).', 'Спершу друїди, потім дракон (Method).')},
         {'name': 'Lord Pythas',
          'abil': t('Друид Клыка, с ним Druid of the Fang и Deviate Shambler (Method). Lightning Bolt, Healing Touch, Druid’s Slumber и Thunderclap, который замедляет бег и атаку.',
                    'A Druid of the Fang with a Druid of the Fang and a Deviate Shambler (Method). Lightning Bolt, Healing Touch, Druid’s Slumber and Thunderclap, which slows movement and attacks.',
                    'Друїд Ікла, із ним Druid of the Fang і Deviate Shambler (Method). Lightning Bolt, Healing Touch, Druid’s Slumber і Thunderclap, що сповільнює біг і атаку.'),
          'tank': t('Возьмите угрозу на боссе и помощниках, чтобы урон шёл по одному.', 'Get threat on the boss and the adds so the damage dealers can take them one by one.',
                    'Візьміть загрозу на босі й помічниках, щоб шкода йшла по одному.'),
          'heal': t('Танка бьют двое-трое сразу: лечите его плотно.', 'Two or three hit the tank at once: heal him closely.', 'Танка б’ють двоє-троє одразу: лікуйте його щільно.'),
          'dps': t('Прерывайте Slumber, Healing Touch и [[Молнию|Lightning Bolt]]. Помощников оглушайте.', 'Interrupt Slumber, Healing Touch and Lightning Bolt. Stun the adds.',
                   'Переривайте Slumber, Healing Touch і Lightning Bolt. Помічників оглушайте.'),
          'split': t('кого бить первым. Method — помощников; Warcraft Tavern порядок не задаёт.', 'who to kill first. Method: the adds; Warcraft Tavern sets no order.',
                     'кого бити першим. Method — помічників; Warcraft Tavern порядку не задає.')},
         {'name': 'Skum',
          'abil': t('Громовой ящер в Winding Chasm. Одно умение: Chained Bolt, молния по нескольким игрокам.', 'A thunder lizard in the Winding Chasm. One ability: Chained Bolt, lightning that hits several players.',
                    'Громовий ящір у Winding Chasm. Одне вміння: Chained Bolt, блискавка по кількох гравцях.'),
          'tank': t('Отверните его от группы.', 'Turn him away from the group.', 'Відверніть його від групи.'),
          'heal': t('Стойте подальше от остальных, чтобы молния не перескакивала.', 'Stand apart from the others so the lightning does not jump.',
                    'Стійте подалі від інших, щоб блискавка не перескакувала.'),
          'dps': t('Разойдитесь. Урон природой не используйте.', 'Spread out. Do not use Nature damage.', 'Розійдіться. Шкоду природою не використовуйте.'),
          'split': t('Chained Bolt. Warcraft Tavern — прерывается; Method — просто разойтись.', 'Chained Bolt. Warcraft Tavern: interruptible; Method: just spread out.',
                     'Chained Bolt. Warcraft Tavern — переривається; Method — просто розійтися.')},
         {'name': 'Lord Serpentis',
          'abil': t('Глава друидов Клыка. Те же Lightning Bolt, Healing Touch и Druid’s Slumber.', 'The leader of the Druids of the Fang. The same Lightning Bolt, Healing Touch and Druid’s Slumber.',
                    'Голова друїдів Ікла. Ті самі Lightning Bolt, Healing Touch і Druid’s Slumber.'),
          'tank': t('Держите угрозу и сбивайте Healing Touch или сон, когда можете.', 'Hold threat and interrupt Healing Touch or the sleep when you can.',
                    'Тримайте загрозу й збивайте Healing Touch або сон, коли можете.'),
          'heal': t('Лечите танка и следите за остальными.', 'Heal the tank and keep an eye on the rest.', 'Лікуйте танка й стежте за рештою.'),
          'dps': t('Прерывайте сон, лечение и молнию.', 'Interrupt the sleep, the heal and the bolt.', 'Переривайте сон, лікування й блискавку.'),
          'split': t('помощники. Warcraft Tavern — без помощников; Method — два друида Клыка, их бить первыми.', 'adds. Warcraft Tavern: no adds; Method: two Druids of the Fang, kill them first.',
                     'помічники. Warcraft Tavern — без помічників; Method — два друїди Ікла, їх бити першими.')},
         {'name': 'Verdan the Everliving',
          'abil': t('Элементаль у водопада после Serpentis, бьёт очень сильно. Grasping Vines: урон и корни на всех в 10 метрах, короткое оглушение; не прерывается.',
                    'An elemental by the waterfall after Serpentis who hits very hard. Grasping Vines: damage and roots on everyone within 10 yards, a short stun; it cannot be interrupted.',
                    'Елементаль біля водоспаду після Serpentis, б’є дуже сильно. Grasping Vines: шкода й коріння на всіх у 10 метрах, коротке оглушення; не переривається.'),
          'tank': t('Бой на танке; от корней не уйти.', 'A fight on the tank; the vines cannot be avoided.', 'Бій на танку; від коріння не втекти.'),
          'heal': t('Стойте дальше 10 метров. Пока танк в корнях, держите на нём щиты и лечение со временем.',
                    'Stand beyond 10 yards. While the tank is rooted, keep shields and heals over time on him.',
                    'Стійте далі 10 метрів. Поки танк у корінні, тримайте на ньому щити й лікування з часом.'),
          'dps': t('Дальний бой — дальше 10 метров. Ближний бой терпит корни.', 'Ranged stay beyond 10 yards. Melee put up with the vines.',
                   'Далекий бій — далі 10 метрів. Ближній бій терпить коріння.')},
         {'name': 'Mutanus the Devourer', 'last': True,
          'abil': t('Событие: проведите Disciple of Naralex до камня ритуала. На месте две волны врагов, потом Mutanus из воды. Thundercrack оглушает всех рядом, Terrify пугает, Naralex’s Nightmare усыпляет или берёт игрока под контроль.',
                    'Event: escort the Disciple of Naralex to the ritual stone. There come two waves of enemies, then Mutanus from the water. Thundercrack stuns everyone nearby, Terrify fears, Naralex’s Nightmare puts a player to sleep or takes control of them.',
                    'Подія: проведіть Disciple of Naralex до каменя ритуалу. На місці дві хвилі ворогів, потім Mutanus із води. Thundercrack оглушує всіх поруч, Terrify лякає, Naralex’s Nightmare присипляє або бере гравця під контроль.'),
          'tank': t('Уведите босса от ученика: если тот погибнет, событие сорвётся. Защитные способности — под Thundercrack.', 'Drag the boss away from the Disciple: if he dies, the event fails. Use defensive cooldowns around Thundercrack.',
                    'Відведіть боса від учня: якщо той загине, подія зірветься. Захисні вміння — під Thundercrack.'),
          'heal': t('Стойте на предельной дистанции. После Thundercrack лечите ближний бой.', 'Stand at maximum range. After Thundercrack, heal the melee.',
                    'Стійте на граничній дистанції. Після Thundercrack лікуйте ближній бій.'),
          'dps': t('Сначала волны (по Warcraft Tavern, семь слизней и три змеи), потом босс. Naralex’s Nightmare прерывайте.',
                   'The waves first (per Warcraft Tavern, seven oozes and three snakes), then the boss. Interrupt Naralex’s Nightmare.',
                   'Спершу хвилі (за Warcraft Tavern, сім слизнів і три змії), потім бос. Naralex’s Nightmare переривайте.')},
     ],
     'boss_tip': t('Каждый из четырёх друидов даёт камень для Leaders of the Fang. С Mutanus падает The Glowing Shard, начало одноимённого задания: по Warcraft Tavern, сначала к Sputtervalve в Ratchet, потом к Falla Sagewind на горе над пещерами.',
                   'Each of the four druids drops a gem for Leaders of the Fang. Mutanus drops The Glowing Shard, which starts the quest of the same name: per Warcraft Tavern, first to Sputtervalve in Ratchet, then to Falla Sagewind on the hill above the caves.',
                   'Кожен із чотирьох друїдів дає камінь для Leaders of the Fang. З Mutanus падає The Glowing Shard, початок однойменного завдання: за Warcraft Tavern, спершу до Sputtervalve у Ratchet, потім до Falla Sagewind на горі над печерами.'),
     'quests': [
         ('Serpentbloom', t('Apothecary Zamah, Spirit Rise в [[Громовом Утесе|Thunder Bluff]]', 'Apothecary Zamah, Spirit Rise in Thunder Bluff', 'Apothecary Zamah, Spirit Rise у Thunder Bluff'), 'horde'),
         ('Leaders of the Fang', t('Nara Wildmane, Elder Rise в [[Громовом Утесе|Thunder Bluff]], после цепочки', 'Nara Wildmane, Elder Rise in Thunder Bluff, after a chain',
                                   'Nara Wildmane, Elder Rise у Thunder Bluff, після ланцюжка'), 'horde'),
         ('Deviate Eradication', t('Ebru, пещера над входом', 'Ebru, the cave above the entrance', 'Ebru, печера над входом'), 'both'),
         ('Deviate Hides', t('Nalpak, пещера над входом', 'Nalpak, the cave above the entrance', 'Nalpak, печера над входом'), 'both'),
         ('Trouble at the Docks', t('Crane Operator Bigglefuzz в Ratchet', 'Crane Operator Bigglefuzz in Ratchet', 'Crane Operator Bigglefuzz у Ratchet'), 'both'),
         ('Smart Drinks', t('Mebok Mizzyrix в Ratchet, после Raptor Horns', 'Mebok Mizzyrix in Ratchet, after Raptor Horns', 'Mebok Mizzyrix у Ratchet, після Raptor Horns'), 'both'),
         ('The Glowing Shard', t('The Glowing Shard с Mutanus the Devourer', 'The Glowing Shard from Mutanus the Devourer', 'The Glowing Shard із Mutanus the Devourer'), 'both'),
     ],
     'quest_note': t('По Warcraft Tavern, задания перенесены с классики, изменились только награды. Leaders of the Fang открывает цепочка Tonga Runetotem в Crossroads. Trouble at the Docks делается во внешней пещере: Mad Magglish ходит в незаметности. Deviate Hides и Smart Drinks редко закрываются за один проход (Method). Где сдавать The Glowing Shard, Warcraft Tavern пишет по-разному.',
                     'Per Warcraft Tavern, the quests carried over from Classic with only the rewards changed. Leaders of the Fang opens with Tonga Runetotem’s chain at the Crossroads. Trouble at the Docks is done in the outer cave: Mad Magglish moves in stealth. Deviate Hides and Smart Drinks rarely finish in one run (Method). Warcraft Tavern gives two different turn-ins for The Glowing Shard.',
                     'За Warcraft Tavern, завдання перенесено з класики, змінилися лише нагороди. Leaders of the Fang відкриває ланцюжок Tonga Runetotem у Crossroads. Trouble at the Docks робиться в зовнішній печері: Mad Magglish ходить у непомітності. Deviate Hides і Smart Drinks рідко закриваються за один прохід (Method). Де здавати The Glowing Shard, Warcraft Tavern пише по-різному.'),
     'sources': [
         ('Warcraft Tavern: Wailing Caverns', 'https://www.warcrafttavern.com/forever/guides/wailing-caverns/'),
         (t('Warcraft Tavern: задания [[Пещер Стенаний|Wailing Caverns]]', 'Warcraft Tavern: Wailing Caverns quests', 'Warcraft Tavern: завдання Wailing Caverns'),
          'https://www.warcrafttavern.com/forever/guides/wailing-caverns-quests/'),
         (t('Method: Wailing Caverns (20.10)', 'Method: Wailing Caverns (Oct 20)', 'Method: Wailing Caverns (20.10)'), 'https://www.method.gg/wow-forever/dungeons/wailing-caverns'),
     ]},
    {'name': 'Shadowfang Keep', 'slug': 'shadowfang-keep',
     'seo_ru': 'Крепость Темного Клыка', 'pill': t('9 боссов', '9 bosses', '9 босів'),
     'desc': t('Крепость Темного Клыка (Shadowfang Keep, 20–26) в WoW Forever: вход в Серебряном бору, девять боссов с тактикой по ролям, что снимать, задания Орды.',
               'Shadowfang Keep (20–26) in WoW Forever: entrance in Silverpine Forest, nine bosses with tactics by role, what to dispel, Horde quests.',
               'Shadowfang Keep (20–26) у WoW Forever: вхід у Silverpine Forest, дев’ять босів із тактикою за ролями, що знімати, завдання Орди.'),
     'lead': t('Замок Arugal и его воргенов в [[Серебряном бору|Silverpine Forest]]: девять боссов, тактика по ролям, что снимать и сбивать, три задания Орды.',
               'The keep of Arugal and his worgen in Silverpine Forest: nine bosses, tactics by role, what to dispel and interrupt, three Horde quests.',
               'Замок Arugal і його воргенів у Silverpine Forest: дев’ять босів, тактика за ролями, що знімати й збивати, три завдання Орди.'),
     'lv_note': t('По Warcraft Tavern; Method и Icy Veins дают 20–30. Blizzard диапазон не публиковала.',
                  'Per Warcraft Tavern; Method and Icy Veins give 20–30. Blizzard has not published a range.',
                  'За Warcraft Tavern; Method та Icy Veins дають 20–30. Blizzard діапазон не публікувала.'),
     'entrance': t('Silverpine Forest, в горах к северу от Pyrewood Village, около 44.5, 68.0 (Warcraft Tavern). Ближайшая точка полёта Орды — The Sepulcher.',
                   'Silverpine Forest, in the hills north of Pyrewood Village, around 44.5, 68.0 (Warcraft Tavern). The nearest Horde flight point is The Sepulcher.',
                   'Silverpine Forest, у горах на північ від Pyrewood Village, близько 44.5, 68.0 (Warcraft Tavern). Найближча точка польоту Орди — The Sepulcher.'),
     'side': t('Орда: обычные задания здесь только у неё. Альянс войти может, но добираться долго (Warcraft Tavern): через [[Болотину|Wetlands]] и Southshore в [[Предгорьях Хилсбрада|Hillsbrad Foothills]] (Method).',
               'Horde: the regular quests here are Horde-only. The Alliance can enter, but the trip is long (Warcraft Tavern): through the Wetlands and Southshore in the Hillsbrad Foothills (Method).',
               'Орда: звичайні завдання тут лише в неї. Альянс може ввійти, але добиратися довго (Warcraft Tavern): через Wetlands і Southshore у Hillsbrad Foothills (Method).'),
     'boss_fact': t('9, из них редкий Deathsworn Captain.', '9, including the rare Deathsworn Captain.', '9, із них рідкісний Deathsworn Captain.'),
     'boss_note': t('Порядок у Warcraft Tavern и Method один. После Rethilgore открывается дверь во двор (Warcraft Tavern), дальше коридоры замка вверх к Arugal.',
                    'Warcraft Tavern and Method give the same order. Killing Rethilgore opens the door to the courtyard (Warcraft Tavern); from there the keep’s corridors lead up to Arugal.',
                    'Порядок у Warcraft Tavern і Method однаковий. Після Rethilgore відчиняються двері у двір (Warcraft Tavern), далі коридори замку вгору до Arugal.'),
     'needs': [
         (t('Снять проклятие', 'Remove a curse', 'Зняти прокляття'),
          t('Baron Silverlaine: Veil of Shadow на танке, −75% к получаемому лечению на 15 секунд.', 'Baron Silverlaine: Veil of Shadow on the tank, −75% healing taken for 15 seconds.',
            'Baron Silverlaine: Veil of Shadow на танку, −75% до отримуваного лікування на 15 секунд.'),
          t('Снимайте сразу или прерывайте каст (Warcraft Tavern). Нечем — танк живёт на защитных способностях.', 'Remove it at once or interrupt the cast (Warcraft Tavern). If you cannot, the tank survives on defensive cooldowns.',
            'Знімайте одразу або переривайте каст (Warcraft Tavern). Нічим — танк живе на захисних уміннях.')),
         (t('Снять яд', 'Cure a poison', 'Зняти отруту'),
          t('Fenrus the Devourer: Toxic Saliva, урон со временем (Method).', 'Fenrus the Devourer: Toxic Saliva, damage over time (Method).',
            'Fenrus the Devourer: Toxic Saliva, шкода з часом (Method).'),
          t('Снимайте с танка, если есть чем.', 'Cure it on the tank if you can.', 'Знімайте з танка, якщо є чим.')),
         (t('Сбить заклинание', 'Interrupt a cast', 'Збити заклинання'),
          t('Commander Springvale: Holy Light, в том числе под [[Божественным щитом|Divine Shield]].', 'Commander Springvale: Holy Light, including under Divine Shield.',
            'Commander Springvale: Holy Light, зокрема під Divine Shield.'),
          t('Прерывание держите под его лечение: щит не мешает сбить каст (Warcraft Tavern).', 'Keep an interrupt for his heal: the shield does not stop you interrupting it (Warcraft Tavern).',
            'Переривання тримайте під його лікування: щит не заважає збити каст (Warcraft Tavern).')),
         (t('Убить первым', 'Kill first', 'Убити першим'),
          t('Wailing Guardsman: Screams of the Past, немота на всех рядом на 5 секунд, повторяется (Method).', 'Wailing Guardsmen: Screams of the Past, a 5-second silence on everyone nearby, repeated (Method).',
            'Wailing Guardsman: Screams of the Past, німота на всіх поруч на 5 секунд, повторюється (Method).'),
          t('Убивайте их раньше остальных, особенно у Springvale.', 'Kill them before anything else, especially at Springvale.', 'Убивайте їх раніше за інших, особливо в Springvale.')),
         (t('Урон оружием', 'Weapon damage', 'Шкода зброєю'),
          t('Shadowfang Moonwalker: Anti-Magic Shield, неуязвим к магии 10 секунд (Method).', 'Shadowfang Moonwalkers: Anti-Magic Shield, immune to magic for 10 seconds (Method).',
            'Shadowfang Moonwalker: Anti-Magic Shield, невразливий до магії 10 секунд (Method).'),
          t('Под щитом его бьют оружием, заклинатели переключаются.', 'While the shield is up, weapons hit him and casters switch targets.',
            'Під щитом його б’ють зброєю, заклиначі перемикаються.')),
         (t('Контроль на своего', 'Crowd control on an ally', 'Контроль на свого'),
          t('Archmage Arugal: Arugal’s Curse отдаёт игрока под контроль на 10 секунд (Method), не снимается (Warcraft Tavern).',
            'Archmage Arugal: Arugal’s Curse turns a player against the group for 10 seconds (Method) and cannot be removed (Warcraft Tavern).',
            'Archmage Arugal: Arugal’s Curse віддає гравця під контроль на 10 секунд (Method), не знімається (Warcraft Tavern).'),
          t('Своего не бейте: контроль или провокация, пока не отпустит.', 'Do not hit your ally: crowd control or a taunt until it wears off.',
            'Свого не бийте: контроль або провокація, доки не відпустить.')),
     ],
     'group_tip': t('Залы Silverlaine и Springvale забиты врагами: тяните по одной группе, весь зал сразу — почти верная смерть.',
                    'The rooms of Silverlaine and Springvale are packed with enemies: pull one pack at a time, the whole room at once is almost certain death.',
                    'Зали Silverlaine і Springvale забиті ворогами: тягніть по одній групі, уся зала одразу — майже певна смерть.'),
     'bosses': [
         {'name': 'Rethilgore',
          'abil': t('Ворген у камер, с ним Bleak Worg и Shadowfang Whitescalp (Warcraft Tavern). Soul Drain: оглушение и урон со временем (Method).',
                    'A worgen by the cells with Bleak Worgs and a Shadowfang Whitescalp (Warcraft Tavern). Soul Drain: a stun plus damage over time (Method).',
                    'Ворген біля камер, із ним Bleak Worg і Shadowfang Whitescalp (Warcraft Tavern). Soul Drain: оглушення й шкода з часом (Method).'),
          'tank': t('Держите на себе помощников, пока их убивают.', 'Hold the adds on yourself while they die.', 'Тримайте на собі помічників, поки їх убивають.'),
          'heal': t('Босс бьёт танка сильно: берегите ману.', 'The boss hits the tank hard: save your mana.', 'Бос б’є танка сильно: бережіть ману.'),
          'dps': t('Сначала помощники, потом босс. Оглушайте, когда можно.', 'The adds first, then the boss. Stun when you can.', 'Спершу помічники, потім бос. Оглушайте, коли можна.')},
         {'name': 'Razorclaw the Butcher',
          'abil': t('Мясник с помощниками. Butcher Drain по танку снова и снова.', 'The butcher with adds. Butcher Drain on the tank again and again.',
                    'М’ясник із помічниками. Butcher Drain по танку знову й знову.'),
          'tank': t('Отметьте помощников и снимайте их по одному.', 'Mark the adds and take them one at a time.', 'Позначте помічників і знімайте їх по одному.'),
          'heal': t('Лечите танка, Butcher Drain идёт без перерыва.', 'Heal the tank: Butcher Drain keeps coming.', 'Лікуйте танка, Butcher Drain іде без перерви.'),
          'dps': t('Сначала помощники, потом босс.', 'The adds first, then the boss.', 'Спершу помічники, потім бос.')},
         {'name': 'Baron Silverlaine',
          'abil': t('Призрак хозяина замка. Veil of Shadow на танке: −75% к получаемому лечению на 15 секунд.', 'The ghost of the keep’s lord. Veil of Shadow on the tank: −75% healing taken for 15 seconds.',
                    'Привид господаря замку. Veil of Shadow на танку: −75% до отримуваного лікування на 15 секунд.'),
          'tank': t('До боя зачистите зал. Под Veil of Shadow включайте защитные способности.', 'Clear the room before the pull. Use defensive cooldowns under Veil of Shadow.',
                    'До бою зачистіть залу. Під Veil of Shadow вмикайте захисні вміння.'),
          'heal': t('Снимайте проклятие сразу; пока оно висит, лечение по танку почти не проходит.', 'Remove the curse at once; while it is up, healing on the tank barely lands.',
                    'Знімайте прокляття одразу; поки воно висить, лікування по танку майже не проходить.'),
          'dps': t('Прерывайте Veil of Shadow, оглушайте босса.', 'Interrupt Veil of Shadow and stun the boss.', 'Переривайте Veil of Shadow, оглушайте боса.')},
         {'name': 'Commander Springvale',
          'abil': t('Нежить-паладин, с ним Haunted Servitor и Wailing Guardsman (Method). Hammer of Justice, Holy Light, Divine Shield на 10 секунд; по Warcraft Tavern, щит при 30% здоровья.',
                    'An undead paladin with a Haunted Servitor and a Wailing Guardsman (Method). Hammer of Justice, Holy Light, a 10-second Divine Shield; per Warcraft Tavern, the shield comes at 30% health.',
                    'Нежить-паладин, із ним Haunted Servitor і Wailing Guardsman (Method). Hammer of Justice, Holy Light, Divine Shield на 10 секунд; за Warcraft Tavern, щит при 30% здоров’я.'),
          'tank': t('Тяните зал мелкими группами. Босса держите, пока бьют охрану.', 'Pull the room in small packs. Hold the boss while the guards die.',
                    'Тягніть залу дрібними групами. Боса тримайте, поки б’ють охорону.'),
          'heal': t('Берегите ману: бой затягивается из-за щита и лечения.', 'Save mana: the shield and the heals drag the fight out.', 'Бережіть ману: бій затягується через щит і лікування.'),
          'dps': t('Первым Wailing Guardsman. Holy Light сбивайте и под щитом.', 'The Wailing Guardsman first. Interrupt Holy Light even under the shield.',
                   'Першим Wailing Guardsman. Holy Light збивайте й під щитом.')},
         {'name': 'Odo the Blindwatcher',
          'abil': t('Ворген с летучими мышами Vile Bat. Howling Rage: чем дольше бой и меньше у него здоровья, тем сильнее он бьёт.',
                    'A worgen with Vile Bats. Howling Rage: the longer the fight and the lower his health, the harder he hits.',
                    'Ворген із кажанами Vile Bat. Howling Rage: що довший бій і менше в нього здоров’я, то сильніше він б’є.'),
          'tank': t('Уведите мышей от группы: они бьют по площади и обезоруживают (Method).', 'Pull the bats away from the group: they cleave and disarm (Method).',
                    'Відведіть кажанів від групи: вони б’ють по площі й обеззброюють (Method).'),
          'heal': t('Начинайте спокойно: урон растёт к концу боя.', 'Start calmly: the damage ramps up towards the end.', 'Починайте спокійно: шкода зростає під кінець бою.'),
          'dps': t('Сначала мыши. Сильные способности берегите на вторую половину здоровья босса (Warcraft Tavern).', 'The bats first. Save your big cooldowns for the boss’s second half of health (Warcraft Tavern).',
                   'Спершу кажани. Сильні вміння бережіть на другу половину здоров’я боса (Warcraft Tavern).')},
         {'name': 'Deathsworn Captain', 'rare': True,
          'abil': t('Появляется не всегда, в зоне после Odo. Cleave и Hamstring.', 'Not always there; appears in the area after Odo. Cleave and Hamstring.',
                    'З’являється не завжди, у зоні після Odo. Cleave і Hamstring.'),
          'tank': t('Отведите его от группы и не тяните вместе с другими врагами.', 'Pull him away from the group and not together with other enemies.',
                    'Відведіть його від групи й не тягніть разом з іншими ворогами.'),
          'heal': t('Бой на танке.', 'A fight on the tank.', 'Бій на танку.'),
          'dps': t('Стойте за спиной, не перебивайте угрозу танка.', 'Stand behind him and do not pull threat off the tank.', 'Стійте за спиною, не перебивайте загрозу танка.')},
         {'name': 'Fenrus the Devourer',
          'abil': t('Волк у входа в покои Arugal, без помощников. Toxic Saliva: яд с уроном со временем (Method).', 'A wolf guarding the way to Arugal’s chambers, no adds. Toxic Saliva: a poison with damage over time (Method).',
                    'Вовк біля входу до покоїв Arugal, без помічників. Toxic Saliva: отрута зі шкодою з часом (Method).'),
          'tank': t('Держите защитные способности наготове.', 'Keep your defensive cooldowns ready.', 'Тримайте захисні вміння напоготові.'),
          'heal': t('Снимайте яд с танка и берегите ману.', 'Cure the poison on the tank and save mana.', 'Знімайте отруту з танка й бережіть ману.'),
          'dps': t('Проверка урона: бейте быстро.', 'A damage check: hit fast.', 'Перевірка шкоди: бийте швидко.'),
          'split': t('насколько он опасен. Warcraft Tavern — бьёт сильно; Method — слабый бой.', 'how dangerous he is. Warcraft Tavern: he hits hard; Method: a weak fight.',
                     'наскільки він небезпечний. Warcraft Tavern — б’є сильно; Method — слабкий бій.')},
         {'name': 'Wolf Master Nandos',
          'abil': t('Охраняет дверь к Arugal, с ним четыре волка. Зовёт новых: Bleak Worg или Lupine Horror.', 'Guards the door to Arugal with four wolves. Calls more: Bleak Worgs or Lupine Horrors.',
                    'Охороняє двері до Arugal, із ним чотири вовки. Кличе нових: Bleak Worg або Lupine Horror.'),
          'tank': t('Быстро забирайте призванных волков на себя.', 'Pick up the summoned wolves fast.', 'Швидко забирайте викликаних вовків на себе.'),
          'heal': t('Лечите танка, когда на нём собирается стая.', 'Heal the tank while the pack gathers on him.', 'Лікуйте танка, коли на ньому збирається зграя.'),
          'dps': t('Призванных бейте по площади, не перебивая угрозу танка; потом босса.', 'Hit the summons with area damage without pulling threat; then the boss.',
                   'Викликаних бийте по площі, не перебиваючи загрозу танка; потім боса.'),
          'split': t('когда он зовёт стаю. Warcraft Tavern — на 80% здоровья; Method — убьёте его волков, и он вступает в бой сам.',
                     'when he calls the pack. Warcraft Tavern: at 80% health; Method: kill his wolves and he joins the fight himself.',
                     'коли він кличе зграю. Warcraft Tavern — на 80% здоров’я; Method — уб’єте його вовків, і він вступає в бій сам.')},
         {'name': 'Archmage Arugal', 'last': True,
          'abil': t('Хозяин воргенов, в зале с тремя воргенами. Void Bolt сильно бьёт тенью и не прерывается, Arugal’s Curse отдаёт игрока под контроль, Shadow Port переносит его по залу, Thundershock бьёт по площади.',
                    'The master of the worgen, in a hall with three worgen. Void Bolt hits hard with shadow and cannot be interrupted, Arugal’s Curse turns a player, Shadow Port moves him around the hall, Thundershock hits an area.',
                    'Господар воргенів, у залі з трьома воргенами. Void Bolt сильно б’є тінню й не переривається, Arugal’s Curse віддає гравця під контроль, Shadow Port переносить його залою, Thundershock б’є по площі.'),
          'tank': t('Сначала три воргена. Сопротивление тёмной магии сильно помогает (Warcraft Tavern).', 'The three worgen first. Shadow resistance helps a lot (Warcraft Tavern).',
                    'Спершу три воргени. Опір темній магії дуже допомагає (Warcraft Tavern).'),
          'heal': t('Void Bolt бьёт по танку больно. От него можно уйти за угол (Method).', 'Void Bolt hits the tank hard. It can be dodged by breaking line of sight (Method).',
                    'Void Bolt б’є по танку боляче. Від нього можна сховатися за ріг (Method).'),
          'dps': t('Не бейте игрока под проклятием: контроль или провокация. Когда Arugal прыгает по залу, догоняйте его.', 'Do not hit a cursed player: crowd control or a taunt. When Arugal jumps around the hall, follow him.',
                   'Не бийте гравця під прокляттям: контроль або провокація. Коли Arugal стрибає залою, наздоганяйте його.')},
     ],
     'boss_tip': t('Тело Deathstalker Vincent для Deathstalkers in Shadowfang лежит сразу после Rethilgore, справа от лестницы во двор. Book of Ur стоит на полке в комнате Fenrus, её легко пропустить. Голова Arugal нужна для Arugal Must Die.',
                   'Deathstalker Vincent’s body for Deathstalkers in Shadowfang lies just past Rethilgore, to the right of the stairs into the courtyard. The Book of Ur sits on a shelf in Fenrus’s room and is easy to miss. Arugal’s head is needed for Arugal Must Die.',
                   'Тіло Deathstalker Vincent для Deathstalkers in Shadowfang лежить одразу після Rethilgore, праворуч від сходів у двір. Book of Ur стоїть на полиці в кімнаті Fenrus, її легко пропустити. Голова Arugal потрібна для Arugal Must Die.'),
     'quests': [
         ('Deathstalkers in Shadowfang', t('High Executor Hadrec, The Sepulcher в [[Серебряном бору|Silverpine Forest]]', 'High Executor Hadrec, The Sepulcher in Silverpine Forest',
                                           'High Executor Hadrec, The Sepulcher у Silverpine Forest'), 'horde'),
         ('The Book of Ur', t('Keeper Bel’dugur, The Apothecarium в [[Подгороде|Undercity]]', 'Keeper Bel’dugur, The Apothecarium in the Undercity',
                              'Keeper Bel’dugur, The Apothecarium в Undercity'), 'horde'),
         ('Arugal Must Die', t('Dalar Dawnweaver, The Sepulcher в [[Серебряном бору|Silverpine Forest]]', 'Dalar Dawnweaver, The Sepulcher in Silverpine Forest',
                               'Dalar Dawnweaver, The Sepulcher у Silverpine Forest'), 'horde'),
     ],
     'quest_note': t('Уровни заданий 16–18 (Method). Классовые задания сюда не внесены: паладинам The Test of Righteousness (Альянс) и A Moon-Kissed Blade (Орда, Method), чернокнижникам The Orb of Soran’ruk, разбойникам The Horn of Xelthos (Warcraft Tavern).',
                     'Quest levels 16–18 (Method). Class quests are not listed here: The Test of Righteousness (Alliance) and A Moon-Kissed Blade (Horde, Method) for paladins, The Orb of Soran’ruk for warlocks, The Horn of Xelthos for rogues (Warcraft Tavern).',
                     'Рівні завдань 16–18 (Method). Класові завдання сюди не внесено: паладинам The Test of Righteousness (Альянс) і A Moon-Kissed Blade (Орда, Method), чорнокнижникам The Orb of Soran’ruk, розбійникам The Horn of Xelthos (Warcraft Tavern).'),
     'sources': [
         ('Warcraft Tavern: Shadowfang Keep', 'https://www.warcrafttavern.com/forever/guides/shadowfang-keep/'),
         (t('Warcraft Tavern: задания [[Крепости Темного Клыка|Shadowfang Keep]]', 'Warcraft Tavern: Shadowfang Keep quests', 'Warcraft Tavern: завдання Shadowfang Keep'),
          'https://www.warcrafttavern.com/forever/guides/shadowfang-keep-quests/'),
         (t('Method: Shadowfang Keep (20.10)', 'Method: Shadowfang Keep (Oct 20)', 'Method: Shadowfang Keep (20.10)'), 'https://www.method.gg/wow-forever/dungeons/shadowfang-keep'),
     ]},
]
BY_NAME = {d['name']: d for d in DUNGEON_PAGES}
SEO = {}   # guides/dungeons/<slug>/ -> (title, description) by language: seo.py adds it to META


# ---------- data from elsewhere ----------

def registry():
    """DUNGEONS of index.src.html: {name: (min, max, zone, new, other sites, side, both)} and the names in table order."""
    src = open(os.path.join(HERE, 'index.src.html'), encoding='utf-8').read()
    i = src.index('const DUNGEONS = [')
    rows = [ast.literal_eval(x.strip().rstrip(',')) for x in src[i:src.index('\n];', i)].split('\n')[1:] if x.strip().startswith('[')]
    return {r[0]: tuple(r[1:]) + (None,) * (7 - len(r[1:])) for r in rows}, [r[0] for r in rows]


def table_links():
    """{row index in DUNGEONS: 'slug/'}: the table on guides/dungeons/ links the dungeons that have a page."""
    _, order = registry()
    return {i: f'{BY_NAME[n]["slug"]}/' for i, n in enumerate(order) if n in BY_NAME}


def load_gear30(path=None):
    try:
        with open(path or GEAR30_PATH, encoding='utf-8') as f:
            return json.load(f)
    except (OSError, ValueError):
        return {'items': {}, 'specs': {}}


def loot_index(name, data=None):
    """Reverse index of the gear list (data/gear30.json): {boss: [(item id, item, sorted spec keys)]} for one dungeon."""
    data = data if data is not None else load_gear30()
    got = {}
    for spec, picks in (data.get('specs') or {}).items():
        for e in picks:
            for s in e.get('src') or []:
                if s.get('kind') == 'drop' and (s.get('dungeon') or {}).get('en') == name and (s.get('boss') or {}).get('en'):
                    got.setdefault(s['boss']['en'], {}).setdefault(str(e['id']), set()).add(spec)
    items = data.get('items') or {}
    return {b: sorted(((i, items[i], sorted(sp)) for i, sp in ids.items() if i in items), key=lambda x: (-(x[1].get('lvl') or 0), x[1]['names']['en']))
            for b, ids in got.items()}


# ---------- rendering (all languages, after langs.fill) ----------

def _x(d, lang):
    return escape(d[lang]) if isinstance(d, dict) else escape(d)


def _facts(p, reg, lang, has_loot):
    lo, hi, zone, new, alt, side, both = reg
    lv = f'{lo}–{hi}' if lo != hi else str(lo)
    loot = (f'<a href="#loot">{_x(LOOT_GO, lang)}</a>' if has_loot else _x(LOOT_WAIT, lang))
    rows = [(FACT['lv'], f'{lv}<br><span class="small">{_x(p["lv_note"], lang)}</span>'), (FACT['ent'], _x(p['entrance'], lang)),
            (FACT['side'], _x(p['side'], lang)), (FACT['group'], _x(GROUP5, lang)), (FACT['bosses'], _x(p['boss_fact'], lang)),
            (FACT['loot'], loot)]
    return ('<dl class="cxrows">' + ''.join(f'<div><dt>{_x(k, lang)}</dt><dd>{v}</dd></div>' for k, v in rows) + '</dl>'
            f'<p class="small">{_x(SRC_LINE, lang)} {_x(XP_LINE, lang)}</p>'
            f'<p><a class="more-l" href="../">{_x(ALL_LINK, lang)}</a></p>')


def _table(head, rows, lang):
    """A .gtable like the guide tables: rows are lists of ready HTML; on a phone the first cell heads the card."""
    hs = [_x(h, lang) for h in head]
    th = ''.join(f'<th scope="col">{h}</th>' for h in hs)
    body = ''.join('<tr>' + ''.join(f'<td data-l="{h}"' + (' class="k"' if i == 0 else '') + f'>{c}</td>' for i, (h, c) in enumerate(zip(hs, r))) + '</tr>'
                   for r in rows)
    return f'<table class="gtable"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table>'


def _bosses(p, lang):
    out = []
    for n, b in enumerate(p['bosses'], 1):
        mark = OPT if b.get('opt') else RARE if b.get('rare') else SKIP if b.get('skip') else LAST if b.get('last') else None
        roles = ''.join(f'<div><dt>{_x(r, lang)}</dt><dd>{_x(b[k], lang)}</dd></div>' for r, k in zip(ROLES, ('tank', 'heal', 'dps')))
        split = f'<p class="small">{_x(SPLIT, lang)}: {_x(b["split"], lang)}</p>' if b.get('split') else ''
        out.append(f'<li><h3>{n}. {en(b["name"])}' + (f' <span class="dgm">· {_x(mark, lang)}</span>' if mark else '') + '</h3>'
                   f'<p>{_x(b["abil"], lang)}</p><dl class="cxrows">{roles}</dl>{split}</li>')
    return f'<p>{_x(p["boss_note"], lang)}</p><ol class="dgboss">{"".join(out)}</ol>'


def _spec_name(key, lang):
    cid, spec = key.split('-', 1)
    c = next((c for c in build.CLASSES if c['id'] == cid), None)
    if not c:
        return key
    s = next((s for s in c['specs'] if s['en'].lower().replace(' ', '-') == spec), None)
    return f'{build.tr(c["n"], lang)} · {build.tr(s["n"], lang) if s else spec}'


def _loot(p, idx, lang):
    out = [f'<p>{_x(LOOT_LEAD, lang)}</p>']
    for b in p['bosses']:
        rows = [[escape(it['names'].get(lang) or it['names']['en']), str(it.get('lvl') or '—'), escape(', '.join(_spec_name(k, lang) for k in sp))]
                for _, it, sp in idx.get(b['name'], [])]
        if rows:
            out.append(f'<h3>{en(b["name"])}</h3>' + _table(LOOT_HEAD, rows, lang))
    return ''.join(out)


def _per_lang(fn):
    return {lang: fn(lang) for lang in langs.LANGS}


def attach(guides, order, gear=None):
    """The dungeon pages after 'dungeons' in ORDER, and their links on the dungeon list. gear: test data instead of data/gear30.json."""
    langs.fill([DUNGEON_PAGES, SEC, FACT, GROUP5, ROLES, SPLIT, OPT, LAST, RARE, SKIP, SRC_LINE, XP_LINE, LOOT_WAIT, LOOT_GO, LOOT_LEAD, LOOT_HEAD,
                NEED_HEAD, QUEST_HEAD, SIDE, ALL_LINK, PAGES_LABEL, GROUP_NEXT, TILE, SEO_TAIL])
    reg, _ = registry()
    data = gear if gear is not None else load_gear30()
    at = order.index('dungeons') + 1
    made = []
    for p in DUNGEON_PAGES:
        assert p['name'] in reg, f'{p["name"]}: not in DUNGEONS (index.src.html)'
        idx = loot_index(p['name'], data)
        title = {l: f'{langs.name(p["name"], l)}' for l in langs.LANGS}
        sections = [
            {'id': 'about', 'title': SEC['about'], 'blocks': [('raw', _per_lang(lambda l: _facts(p, reg[p['name']], l, bool(idx))))]},
            {'id': 'group', 'title': SEC['group'], 'blocks': [
                ('raw', _per_lang(lambda l: _table(NEED_HEAD, [[_x(a, l), _x(b, l), _x(c, l)] for a, b, c in p['needs']], l))),
                ('tip', p['group_tip'])]},
            {'id': 'bosses', 'title': SEC['bosses'], 'blocks': [('raw', _per_lang(lambda l: _bosses(p, l))), ('tip', p['boss_tip'])]},
        ]
        if idx:                                                    # no gear data: no section (an empty one is worse than none)
            sections.append({'id': 'loot', 'title': SEC['loot'], 'blocks': [('raw', _per_lang(lambda l: _loot(p, idx, l)))]})
        sections.append({'id': 'quests', 'title': SEC['quests'], 'blocks': [
            ('raw', _per_lang(lambda l: _table(QUEST_HEAD, [[en(q), _x(w, l), _x(SIDE[s], l)] for q, w, s in p['quests']], l))),
            ('text', [p['quest_note']])]})
        slug = f'dungeons/{p["slug"]}'
        g = {'slug': slug, 'art': 'warlock', 'hero': 'hero_dungeons', 'og': 'dungeons', 'hub': False, 'others': False,
             'title': title, 'crumb': title, 'lead': p['lead'],   # the h1 is the name alone: the search title (SEO) says the rest
             'tile': TILE, 'pills': [], 'sections': sections,
             'sources': [(t('Blizzard: заметки беты Forever', 'Blizzard: Forever beta development notes', 'Blizzard: нотатки бети Forever'), BLIZZ_NOTES)]
                        + [(s, u) for s, u in p['sources']]}
        lo, hi = reg[p['name']][:2]
        g['pills'] = [f'{lo}–{hi}', SIDE[reg[p['name']][5]], p['pill']]
        guides.append(g)
        made.append((g, p))
        order.insert(at, slug)
        at += 1
        name_seo = {l: (p['seo_ru'] if l == 'ru' else langs.name(p['name'], l)) for l in langs.LANGS}
        full = {l: f'{name_seo[l]} WoW Forever: {SEO_TAIL[l]}' for l in langs.LANGS}   # a long local name: the name alone (60 chars max)
        SEO[f'guides/{slug}/'] = ({l: v if len(v) <= 60 else f'{name_seo[l]} WoW Forever' for l, v in full.items()}, p['desc'])
    _, names = registry()
    made.sort(key=lambda gp: names.index(gp[1]['name']))           # table (level) order
    for i, (g, p) in enumerate(made):                              # «Next step»: the list, the next dungeon page by level, the group builder
        other = made[i + 1] if i + 1 < len(made) else made[i - 1] if i else None
        g['next'] = [('guides/dungeons/', ALL_LINK)] + ([(f'guides/{other[0]["slug"]}/', other[0]['title'])] if other else []) + [('tools/#raid', GROUP_NEXT)]
    dg = next(x for x in guides if x['slug'] == 'dungeons')
    lst = next(s for s in dg['sections'] if s['id'] == 'list')
    links = _per_lang(lambda l: f'<p class="small">{_x(PAGES_LABEL, l)} '
                                + ' · '.join(f'<a href="{p["slug"]}/">{escape(langs.name(p["name"], l))}</a>' for p in sorted(DUNGEON_PAGES, key=lambda p: names.index(p['name']))) + '</p>')
    lst['blocks'].insert(next(i for i, (k, _) in enumerate(lst['blocks']) if k == 'raw') + 1, ('raw', links))
