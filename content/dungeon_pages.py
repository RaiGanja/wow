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
# needs: (need, from, how) · bosses: name, abil, tank, heal, dps, split (optional), opt (event boss), last (final boss)
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
        mark = OPT if b.get('opt') else LAST if b.get('last') else None
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
    langs.fill([DUNGEON_PAGES, SEC, FACT, GROUP5, ROLES, SPLIT, OPT, LAST, SRC_LINE, XP_LINE, LOOT_WAIT, LOOT_GO, LOOT_LEAD, LOOT_HEAD,
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
        SEO[f'guides/{slug}/'] = ({l: f'{name_seo[l]} WoW Forever: {SEO_TAIL[l]}' for l in langs.LANGS}, p['desc'])
    for g, p in made:                                              # «Next step»: the list, another dungeon page, the group builder
        other = next(((og, op) for og, op in made if op is not p), None)
        g['next'] = [('guides/dungeons/', ALL_LINK)] + ([(f'guides/{other[0]["slug"]}/', other[0]['title'])] if other else []) + [('tools/#raid', GROUP_NEXT)]
    dg = next(x for x in guides if x['slug'] == 'dungeons')
    lst = next(s for s in dg['sections'] if s['id'] == 'list')
    links = _per_lang(lambda l: f'<p class="small">{_x(PAGES_LABEL, l)} '
                                + ' · '.join(f'<a href="{p["slug"]}/">{escape(langs.name(p["name"], l))}</a>' for p in DUNGEON_PAGES) + '</p>')
    lst['blocks'].insert(next(i for i, (k, _) in enumerate(lst['blocks']) if k == 'raw') + 1, ('raw', links))
