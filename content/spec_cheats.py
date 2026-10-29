"""Шпоры спеков: guides/spec-<класс>-<спек>/, вкладки Билд · Таланты · Прокачка 1→60 · С кем играть · БиС · Ротация.
Страница не пишет новых фактов о игре: вкладки собираются из готовых разделов builds-<класс> и leveling-<класс>.
Вкладки БиС нет: пустая вкладка хуже отсутствия; строка «Экипировка» в ответе за 5 секунд говорит «ждёт данных», пока нет списка Forever.
Ссылка на билд b/<раса>-<класс>-<спек>/ у этих спеков ведёт сюда (build_cards.py), «Поделиться» на странице делится той же ссылкой.
Заготовка attach() кладёт страницы в GUIDES до langs.fill, finish() добавляет названия на всех языках (нужен hero_core из build_guides)."""
from html import escape

# (класс, спек): самые частые по данным сайта — оба прокачиваемых «быстрых» спека (Охотник S и Маг S в тир-листе прокачки),
# лучший танк беты и лекарь (Послушание, S в PvE и PvP); роли: 2 урона, танк, лекарь. Выбор Вячеслава 28.10
CHEATS = [('hunter', 'beast-mastery'), ('mage', 'frost'), ('paladin', 'protection'), ('priest', 'discipline'), ('rogue', 'combat'),
          ('warrior', 'protection'), ('warrior', 'fury'), ('warrior', 'arms'), ('paladin', 'holy'), ('paladin', 'retribution'),
          ('hunter', 'marksmanship'), ('hunter', 'survival'), ('rogue', 'assassination'), ('rogue', 'subtlety'),
          ('priest', 'holy'), ('priest', 'shadow'), ('shaman', 'elemental'), ('shaman', 'enhancement'), ('shaman', 'restoration'),
          ('mage', 'arcane'), ('mage', 'fire'), ('warlock', 'affliction'), ('warlock', 'demonology'), ('warlock', 'destruction'),
          ('druid', 'balance'), ('druid', 'feral'), ('druid', 'restoration')]   # all 27 specs since 29.10; the first five came first
SLUGS = [f'spec-{c}-{s}' for c, s in CHEATS]
HAS_CHEAT = {f'{c}-{s}' for c, s in CHEATS}

LANGS9 = ('ru', 'en', 'uk', 'de', 'fr', 'es', 'pt', 'it', 'pl')


def n9(ru, en, uk, de, fr, es, pt, it, pl):
    return dict(zip(LANGS9, (ru, en, uk, de, fr, es, pt, it, pl)))


ANSWER = n9('Ответ за 5 секунд', 'The answer in 5 seconds', 'Відповідь за 5 секунд', 'Die Antwort in 5 Sekunden', 'La réponse en 5 secondes',
            'La respuesta en 5 segundos', 'A resposta em 5 segundos', 'La risposta in 5 secondi', 'Odpowiedź w 5 sekund')
BEST = n9('Лучшая раса', 'Best race', 'Найкраща раса', 'Beste Rasse', 'Meilleure race', 'Mejor raza', 'Melhor raça', 'Migliore razza', 'Najlepsza rasa')
SHEET = n9('Шпора', 'Cheat sheet', 'Шпора', 'Spickzettel', 'Fiche rapide', 'Guía rápida', 'Resumo', 'Scheda rapida', 'Ściąga')
TAB = {
    'build': n9('Билд', 'Build', 'Білд', 'Build', 'Build', 'Build', 'Build', 'Build', 'Build'),
    'talents': n9('Таланты', 'Talents', 'Таланти', 'Talente', 'Talents', 'Talentos', 'Talentos', 'Talenti', 'Talenty'),
    'leveling': n9('Прокачка 1→60', 'Leveling 1→60', 'Прокачування 1→60', 'Leveln 1→60', 'Progression 1→60', 'Subida 1→60',
                   'Evolução 1→60', 'Salita 1→60', 'Levelowanie 1→60'),
    'group': n9('С кем играть', 'Who to group with', 'З ким грати', 'Mit wem spielen', 'Avec qui jouer', 'Con quién jugar',
                'Com quem jogar', 'Con chi giocare', 'Z kim grać'),
    'rotation': n9('Ротация', 'Rotation', 'Ротація', 'Rotation', 'Rotation', 'Rotación', 'Rotação', 'Rotazione', 'Rotacja'),
}
PICK = n9('Подобрать свою расу', 'Pick your race', 'Підібрати свою расу', 'Eigene Rasse wählen', 'Choisir ma race', 'Elegir mi raza',
          'Escolher minha raça', 'Scegli la tua razza', 'Wybierz swoją rasę')
FROM_LINK = n9('Раса из ссылки', 'Race from the link', 'Раса з посилання', 'Rasse aus dem Link', 'Race du lien', 'Raza del enlace',
               'Raça do link', 'Razza dal link', 'Rasa z linku')
ROT_NOTE = n9(
    'Ротация на 60 уровне будет после старта 5 ноября. Пока здесь порядок действий на 30 уровне по бете, как у Icy Veins и Wowhead.',
    'The level 60 rotation will come after the Nov 5 launch. For now this is the level 30 order of actions from the beta, as given by Icy Veins and Wowhead.',
    'Ротація на 60 рівні буде після старту 5 листопада. Поки що тут порядок дій на 30 рівні за бетою, як в Icy Veins і Wowhead.',
    'Die Rotation für Stufe 60 folgt nach dem Start am 5. November. Bis dahin steht hier die Reihenfolge für Stufe 30 aus der Beta, wie bei Icy Veins und Wowhead.',
    'La rotation du niveau 60 viendra après le lancement du 5 novembre. En attendant, voici l’ordre des actions au niveau 30 d’après la bêta, comme chez Icy Veins et Wowhead.',
    'La rotación de nivel 60 llegará tras el lanzamiento del 5 de noviembre. De momento, aquí está el orden de acciones del nivel 30 según la beta, como en Icy Veins y Wowhead.',
    'A rotação do nível 60 virá após o lançamento de 5 de novembro. Por enquanto, aqui está a ordem das ações no nível 30 segundo a beta, como no Icy Veins e no Wowhead.',
    'La rotazione di livello 60 arriverà dopo il lancio del 5 novembre. Per ora qui c’è l’ordine delle azioni al livello 30 secondo la beta, come su Icy Veins e Wowhead.',
    'Rotacja na 60 level pojawi się po starcie 5 listopada. Na razie jest tu kolejność działań na 30 levelu z bety, jak u Icy Veins i Wowhead.')
GROUP_NOTE = n9(
    'Состав группы собирается в конструкторе: до 5, 10, 20 или 40 игроков, ссылка и текст для поиска группы.',
    'Build the group in the group builder: up to 5, 10, 20 or 40 players, with a link and a text for looking for a group.',
    'Склад групи збирається в конструкторі: до 5, 10, 20 або 40 гравців, посилання й текст для пошуку групи.',
    'Die Gruppe stellst du im Gruppenbauer zusammen: bis zu 5, 10, 20 oder 40 Spieler, mit Link und Text für die Gruppensuche.',
    'La composition du groupe se prépare dans le constructeur : jusqu’à 5, 10, 20 ou 40 joueurs, avec un lien et un texte pour chercher un groupe.',
    'El grupo se arma en el constructor: hasta 5, 10, 20 o 40 jugadores, con enlace y texto para buscar grupo.',
    'O grupo é montado no construtor: até 5, 10, 20 ou 40 jogadores, com link e texto para procurar grupo.',
    'Il gruppo si compone nel costruttore: fino a 5, 10, 20 o 40 giocatori, con link e testo per cercare un gruppo.',
    'Skład grupy ustawiasz w konstruktorze: do 5, 10, 20 lub 40 graczy, z linkiem i tekstem do szukania grupy.')
GROUP_TILE = n9('Сборщик группы', 'Group builder', 'Конструктор групи', 'Gruppenbauer', 'Constructeur de groupe', 'Constructor de grupo',
                'Construtor de grupo', 'Costruttore di gruppo', 'Konstruktor grupy')
FULL_LEVELING = n9('Полный гайд прокачки класса', 'Full class leveling guide', 'Повний гайд прокачування класу', 'Vollständiger Level-Guide der Klasse',
                   'Guide complet de progression de la classe', 'Guía completa de subida de la clase', 'Guia completo de evolução da classe',
                   'Guida completa alla salita della classe', 'Pełny poradnik levelowania klasy')
FULL_BUILDS = n9('Все спеки класса', 'All specs of the class', 'Усі спеки класу', 'Alle Skillungen der Klasse', 'Toutes les spécialisations de la classe',
                 'Todas las especializaciones de la clase', 'Todas as especializações da classe', 'Tutte le specializzazioni della classe',
                 'Wszystkie specjalizacje klasy')
SEE_ALSO = n9('Смотрите также', 'See also', 'Дивіться також', 'Siehe auch', 'À voir aussi', 'Véase también', 'Veja também', 'Vedi anche', 'Zobacz też')
SEO_TAIL = n9('шпора WoW Forever', 'WoW Forever cheat sheet', 'шпора WoW Forever', 'Spickzettel WoW Forever', 'fiche WoW Forever',
              'guía rápida WoW Forever', 'resumo WoW Forever', 'scheda WoW Forever', 'ściąga WoW Forever')
SEO = {}   # guides/<slug>/ -> (title, description) by language, for seo.META (build.py adds it before seo.main)
LEAD_TAIL = n9('Билд, таланты, прокачка и группа на одной странице.', 'Build, talents, leveling and group on one page.',
               'Білд, таланти, прокачування й група на одній сторінці.', 'Build, Talente, Leveln und Gruppe auf einer Seite.',
               'Build, talents, progression et groupe sur une seule page.', 'Build, talentos, subida y grupo en una sola página.',
               'Build, talentos, evolução e grupo em uma só página.', 'Build, talenti, salita e gruppo in una sola pagina.',
               'Build, talenty, levelowanie i grupa na jednej stronie.')

GOAL = n9('Цель', 'Goal', 'Мета', 'Ziel', 'Objectif', 'Objetivo', 'Objetivo', 'Obiettivo', 'Cel')
GOAL_LV = n9('Прокачка', 'Leveling', 'Прокачування', 'Leveln', 'Progression', 'Subida', 'Evolução', 'Salita', 'Levelowanie')
GOAL_DG = n9('Подземелья', 'Dungeons', 'Підземелля', 'Dungeons', 'Donjons', 'Mazmorras', 'Masmorras', 'Spedizioni', 'Lochy')
KEYT = n9('Ключевые таланты', 'Key talents', 'Ключові таланти', 'Wichtige Talente', 'Talents clés', 'Talentos clave', 'Talentos-chave',
          'Talenti chiave', 'Kluczowe talenty')
ORDER_L = n9('Порядок взятия по уровням', 'Order of points by level', 'Порядок вибору за рівнями', 'Reihenfolge nach Stufe', 'Ordre par niveau',
             'Orden por nivel', 'Ordem por nível', 'Ordine per livello', 'Kolejność wg poziomu')
GEAR_ROWS = [
    n9('Чары', 'Enchants', 'Чари', 'Verzauberungen', 'Enchantements', 'Encantamientos', 'Encantamentos', 'Incantamenti', 'Zaklęcia'),
    n9('Расходники', 'Consumables', 'Витратні', 'Verbrauchsgüter', 'Consommables', 'Consumibles', 'Consumíveis', 'Consumabili',
       'Materiały eksploatacyjne'),
    n9('Камни и материалы', 'Gems and materials', 'Камені й матеріали', 'Edelsteine und Materialien', 'Gemmes et matériaux',
       'Gemas y materiales', 'Gemas e materiais', 'Gemme e materiali', 'Kamienie i materiały')]
# Waiting lines per row: the reason is what the sources really lack, not "after launch"
WAIT = [
    n9('Ждёт данных: у Icy Veins и Wowhead по этому спеку чар нет.', 'Waiting for data: Icy Veins and Wowhead list no enchants for this spec.',
       'Чекає на дані: в Icy Veins і Wowhead для цього спеку чарів немає.', 'Wartet auf Daten: Icy Veins und Wowhead nennen für diese Skillung keine Verzauberungen.',
       'En attente de données : Icy Veins et Wowhead ne listent aucun enchantement pour cette spécialisation.',
       'A la espera de datos: Icy Veins y Wowhead no listan encantamientos para esta especialización.',
       'Aguardando dados: Icy Veins e Wowhead não listam encantamentos para esta especialização.',
       'In attesa di dati: Icy Veins e Wowhead non elencano incantamenti per questa specializzazione.',
       'Czeka na dane: Icy Veins i Wowhead nie podają zaklęć dla tej specjalizacji.'),
    n9('Ждёт данных: у Icy Veins и Wowhead по этому спеку расходников нет.', 'Waiting for data: Icy Veins and Wowhead list no consumables for this spec.',
       'Чекає на дані: в Icy Veins і Wowhead для цього спеку витратних немає.', 'Wartet auf Daten: Icy Veins und Wowhead nennen für diese Skillung keine Verbrauchsgüter.',
       'En attente de données : Icy Veins et Wowhead ne listent aucun consommable pour cette spécialisation.',
       'A la espera de datos: Icy Veins y Wowhead no listan consumibles para esta especialización.',
       'Aguardando dados: Icy Veins e Wowhead não listam consumíveis para esta especialização.',
       'In attesa di dati: Icy Veins e Wowhead non elencano consumabili per questa specializzazione.',
       'Czeka na dane: Icy Veins i Wowhead nie podają materiałów eksploatacyjnych dla tej specjalizacji.'),
    n9('Ждёт данных: у Icy Veins и Wowhead по этому спеку камней и материалов нет.', 'Waiting for data: Icy Veins and Wowhead list no gems or materials for this spec.',
       'Чекає на дані: в Icy Veins і Wowhead для цього спеку каменів і матеріалів немає.', 'Wartet auf Daten: Icy Veins und Wowhead nennen für diese Skillung keine Edelsteine oder Materialien.',
       'En attente de données : Icy Veins et Wowhead ne listent ni gemmes ni matériaux pour cette spécialisation.',
       'A la espera de datos: Icy Veins y Wowhead no listan gemas ni materiales para esta especialización.',
       'Aguardando dados: Icy Veins e Wowhead não listam gemas nem materiais para esta especialização.',
       'In attesa di dati: Icy Veins e Wowhead non elencano gemme né materiali per questa specializzazione.',
       'Czeka na dane: Icy Veins i Wowhead nie podają kamieni ani materiałów dla tej specjalizacji.')]


def _it(en, ru=None, de=None, fr=None, es=None, pt=None, it=None):
    """Item name: the client name where Wowhead Forever has one; uk, pl and the rest fall back to English."""
    return {'en': en, 'ru': ru or en, 'de': de or en, 'fr': fr or en, 'es': es or en, 'pt': pt or en, 'it': it or en}


I_POISON = _it('Instant Poison', 'Быстродействующий яд', 'Sofort wirkendes Gift', 'Poison instantané', 'Veneno instantáneo', 'Veneno Instantâneo')
I_STONE = _it('Rough Sharpening Stone', 'Грубое точило', 'Rauer Wetzstein', 'Pierre à aiguiser brute', 'Piedra de afilar férrea', 'Pedra de Afiar Rústica')
I_AGI = _it('Elixir of Agility', 'Эликсир Ловкости', 'Elixier der Beweglichkeit', 'Elixir d’Agilité', 'Elixir de agilidad', 'Elixir de Agilidade')
I_GHP = _it('Greater Healing Potion', 'Сильное лечебное зелье', 'Großer Heiltrank', 'Potion de soins supérieure', 'Poción de curación superior', 'Poção Maior de Cura')
E_POISON = n9('на оба оружия, лишний урон с каждым ударом', 'on both weapons, extra damage with each hit',
              'на обидві зброї, додаткова шкода з кожним ударом', 'auf beiden Waffen, zusätzlicher Schaden bei jedem Treffer',
              'sur les deux armes, dégâts supplémentaires à chaque coup', 'en ambas armas, daño adicional con cada golpe',
              'nas duas armas, dano extra a cada golpe', 'su entrambe le armi, danno extra a ogni colpo',
              'na obu broniach, dodatkowe obrażenia przy każdym trafieniu')
E_STONE = n9('ставится вместе с ядом: в Forever можно держать оба', 'goes on together with a poison: in Forever you can have both',
             'ставиться разом з отрутою: у Forever можна тримати обидва', 'zusammen mit einem Gift: in Forever sind beide gleichzeitig möglich',
             'avec un poison : dans Forever, les deux peuvent être actifs', 'junto con un veneno: en Forever puedes tener los dos',
             'junto com um veneno: no Forever dá para ter os dois', 'insieme a un veleno: in Forever si possono avere entrambi',
             'razem z trucizną: w Forever można mieć oba naraz')
E_AGI = n9('+15 ловкости на 1 час', '+15 Agility for 1 hour', '+15 спритності на 1 годину', '+15 Beweglichkeit für 1 Stunde',
           '+15 d’agilité pendant 1 heure', '+15 de agilidad durante 1 hora', '+15 de Agilidade por 1 hora', '+15 Agilità per 1 ora',
           '+15 zręczności na 1 godzinę')
E_GHP = n9('лечение в бою: разбойник сам не лечится', 'healing in combat: a Rogue has no self-heal', 'зцілення в бою: розбійник сам себе не лікує',
           'Heilung im Kampf: der Schurke kann sich nicht selbst heilen', 'soins en combat : le voleur ne peut pas se soigner seul',
           'curación en combate: el pícaro no se cura solo', 'cura em combate: o ladino não se cura sozinho',
           'cura in combattimento: il ladro non si cura da solo', 'leczenie w walce: łotrzyk sam się nie leczy')
# (class-spec) -> row index (0 enchants, 1 consumables, 2 gems and materials) -> ([(item, effect)], source). No entry: the WAIT line of the row
GEAR = {
    'rogue-combat': {1: ([(I_POISON, E_POISON), (I_STONE, E_STONE), (I_AGI, E_AGI), (I_GHP, E_GHP)], 'Icy Veins, Wowhead')},
}
STATS_T = n9('Приоритет статов', 'Stat priority', 'Пріоритет характеристик', 'Wertepriorität', 'Priorité des caractéristiques',
             'Prioridad de estadísticas', 'Prioridade de atributos', 'Priorità delle statistiche', 'Priorytet statystyk')
STAT = {
    'wd': n9('Урон оружия', 'Weapon damage', 'Шкода зброї', 'Waffenschaden', 'Dégâts de l’arme', 'Daño de arma', 'Dano da arma',
             'Danni dell’arma', 'Obrażenia broni'),
    'hit': n9('Меткость', 'Hit', 'Влучність', 'Trefferwertung', 'Toucher', 'Golpe', 'Acerto', 'Colpire', 'Trafienie'),
    'exp': n9('Мастерство', 'Expertise', 'Майстерність', 'Waffenkunde', 'Expertise', 'Pericia', 'Perícia', 'Maestria', 'Biegłość'),
    'agi': n9('Ловкость', 'Agility', 'Спритність', 'Beweglichkeit', 'Agilité', 'Agilidad', 'Agilidade', 'Agilità', 'Zręczność'),
    'crit': n9('Крит', 'Crit', 'Крит', 'Krit', 'Critique', 'Crítico', 'Crítico', 'Critico', 'Kryt'),
    'str': n9('Сила', 'Strength', 'Сила', 'Stärke', 'Force', 'Fuerza', 'Força', 'Forza', 'Siła'),
    'sp': n9('Сила заклинаний', 'Spell power', 'Сила заклинань', 'Zaubermacht', 'Puissance des sorts', 'Poder con hechizos', 'Poder mágico',
             'Potere magico', 'Moc zaklęć'),
    'hp': n9('Сила лечения', 'Healing power', 'Сила зцілення', 'Heilkraft', 'Puissance de soins', 'Poder de sanación', 'Poder de cura',
             'Potere di cura', 'Moc leczenia'),
    'int': n9('Интеллект', 'Intellect', 'Інтелект', 'Intelligenz', 'Intelligence', 'Intelecto', 'Intelecto', 'Intelletto', 'Intelekt'),
    'spi': n9('Дух', 'Spirit', 'Дух', 'Willenskraft', 'Esprit', 'Espíritu', 'Espírito', 'Spirito', 'Duch'),
    'mp5': n9('Мана раз в 5 с', 'Mana per 5 s', 'Мана раз на 5 с', 'Mana alle 5 Sek.', 'Mana toutes les 5 s', 'Maná cada 5 s',
              'Mana a cada 5 s', 'Mana ogni 5 s', 'Mana co 5 s'),
    'haste': n9('Скорость', 'Haste', 'Швидкість', 'Tempo', 'Hâte', 'Celeridad', 'Aceleração', 'Celerità', 'Szybkość'),
}
# The order from the spec's tip in spec_builds.py (Icy Veins for the beta; Fury also Warcraft Tavern). No key: the sources give no order;
# 'split': they disagree (Frost: Icy Veins hit first, Warcraft Tavern spell power).
IV, IVT = 'Icy Veins', 'Icy Veins, Warcraft Tavern'
STATS = {
    'paladin-holy': ('hp int spi', IV), 'paladin-retribution': ('wd hit crit', IV), 'warrior-fury': ('hit crit str', IVT),
    'hunter-beast-mastery': ('wd hit agi crit', IV), 'hunter-marksmanship': ('wd hit agi crit', IV),
    'hunter-survival': ('wd hit agi crit str', IV), 'rogue-assassination': ('wd hit exp agi crit', IV),
    'rogue-combat': ('wd hit exp agi crit', IV), 'rogue-subtlety': ('wd hit exp agi crit', IV),
    'priest-discipline': ('hp mp5 spi int crit', IV), 'priest-holy': ('hp mp5 spi int crit', IV), 'priest-shadow': ('sp crit hit int', IV),
    'shaman-elemental': ('sp crit hit int', IV), 'shaman-enhancement': ('wd hit exp crit str int', IV),
    'shaman-restoration': ('hp crit int spi mp5', IV), 'warlock-affliction': ('sp hit crit int spi', IV),
    'warlock-demonology': ('sp hit int crit spi', IV), 'warlock-destruction': ('sp hit haste crit', IV),
    'druid-balance': ('int sp spi mp5 crit', IV), 'druid-feral': ('wd hit exp crit str agi', IV),
    'druid-restoration': ('int hp spi mp5 crit', IV), 'mage-frost': 'split',
}
STATS_NONE = n9('Ждёт данных: в гайдах Icy Veins и Wowhead по бете порядка статов нет.',
                'Waiting for data: the Icy Veins and Wowhead beta guides give no stat order.',
                'Чекає на дані: у гайдах Icy Veins і Wowhead за бетою порядку характеристик немає.',
                'Wartet auf Daten: Die Beta-Guides von Icy Veins und Wowhead nennen keine Reihenfolge.',
                'En attente de données : les guides bêta d’Icy Veins et de Wowhead ne donnent pas d’ordre.',
                'A la espera de datos: las guías de la beta de Icy Veins y Wowhead no dan un orden.',
                'Aguardando dados: os guias da beta do Icy Veins e do Wowhead não dão uma ordem.',
                'In attesa di dati: le guide della beta di Icy Veins e Wowhead non danno un ordine.',
                'Czeka na dane: poradniki bety Icy Veins i Wowhead nie podają kolejności.')
STATS_SPLIT = n9('Ждёт данных: источники расходятся. Icy Veins ставит первой меткость, Warcraft Tavern — силу заклинаний.',
                 'Waiting for data: the sources disagree. Icy Veins puts hit first, Warcraft Tavern puts spell power first.',
                 'Чекає на дані: джерела розходяться. Icy Veins ставить першою влучність, Warcraft Tavern — силу заклинань.',
                 'Wartet auf Daten: Die Quellen sind uneins. Icy Veins setzt Trefferwertung zuerst, Warcraft Tavern Zaubermacht.',
                 'En attente de données : les sources divergent. Icy Veins place le toucher en premier, Warcraft Tavern la puissance des sorts.',
                 'A la espera de datos: las fuentes no coinciden. Icy Veins pone primero el golpe, Warcraft Tavern el poder con hechizos.',
                 'Aguardando dados: as fontes divergem. Icy Veins põe acerto primeiro, Warcraft Tavern põe poder mágico.',
                 'In attesa di dati: le fonti non concordano. Icy Veins mette prima colpire, Warcraft Tavern il potere magico.',
                 'Czeka na dane: źródła się różnią. Icy Veins stawia najpierw trafienie, Warcraft Tavern moc zaklęć.')
FAQ_T = n9('Вопросы', 'Questions', 'Питання', 'Fragen', 'Questions', 'Preguntas', 'Perguntas', 'Domande', 'Pytania')
# Button and tab names as talents.py shows them (ed, share, b_general, b_leveling)
FAQ = [
    {'id': 'copy-build',
     'q': n9('Как скопировать билд?', 'How do I copy the build?', 'Як скопіювати білд?', 'Wie kopiere ich den Build?', 'Comment copier le build ?',
             '¿Cómo copio la build?', 'Como copio a build?', 'Come copio la build?', 'Jak skopiować build?'),
     'a': [n9('В разделе «Таланты» нажмите «Собрать свой билд», расставьте очки и нажмите «Копировать билд»: очки сохранятся в ссылке. Кнопка наверху страницы делится ссылкой на эту шпору.',
              'In the Talents section, press “Make your own build”, place the points and press “Copy build”: the points are kept in the link. The button at the top of the page shares a link to this cheat sheet.',
              'У розділі «Таланти» натисніть «Зібрати свій білд», розставте очки й натисніть «Копіювати білд»: очки збережуться в посиланні. Кнопка вгорі сторінки ділиться посиланням на цю шпору.',
              'Im Abschnitt Talente auf „Eigenen Build erstellen“ tippen, Punkte setzen und „Build kopieren“ drücken: Die Punkte stehen im Link. Der Knopf oben teilt einen Link zu diesem Spickzettel.',
              'Dans la section Talents, appuyez sur « Créer votre build », placez les points puis sur « Copier le build » : les points restent dans le lien. Le bouton en haut de la page partage un lien vers cette fiche.',
              'En la sección Talentos, pulsa «Crear tu build», coloca los puntos y pulsa «Copiar build»: los puntos quedan en el enlace. El botón de arriba comparte un enlace a esta guía rápida.',
              'Na seção Talentos, toque em “Montar sua build”, distribua os pontos e toque em “Copiar build”: os pontos ficam no link. O botão no topo compartilha um link para este resumo.',
              'Nella sezione Talenti premi «Crea la tua build», assegna i punti e premi «Copia build»: i punti restano nel link. Il pulsante in alto condivide un link a questa scheda.',
              'W sekcji Talenty naciśnij „Złóż własny build”, rozdaj punkty i naciśnij „Kopiuj build”: punkty zostają w linku. Przycisk na górze strony udostępnia link do tej ściągi.')]},
    {'id': 'leveling-tab',
     'q': n9('Зачем вкладка «Прокачка» у талантов?', 'What is the “Leveling” tab in the talents for?', 'Навіщо вкладка «Прокачка» в талантах?',
             'Wozu dient der Reiter „Leveln“ bei den Talenten?', 'À quoi sert l’onglet « Progression » des talents ?',
             '¿Para qué sirve la pestaña «Subida de nivel» de los talentos?', 'Para que serve a aba “Evolução” dos talentos?',
             'A cosa serve la scheda «Livellamento» dei talenti?', 'Po co jest zakładka „Levelowanie” w talentach?'),
     'a': [n9('«Общая» — раскладка очков на 30 уровне по бете. «Прокачка» — порядок очков с 10 по 60 уровень; 31–60 взяты из гайда прокачки класса, после старта сверим их с игрой.',
              '“General” is the level 30 point layout from the beta. “Leveling” is the order of points from level 10 to 60; levels 31–60 come from the class leveling guide, and we will check them against the game after launch.',
              '«Загальна» — розкладка очок на 30 рівні за бетою. «Прокачка» — порядок очок з 10 по 60 рівень; 31–60 узяті з гайду прокачування класу, після старту звіримо їх із грою.',
              '„Allgemein“ ist die Punkteverteilung auf Stufe 30 aus der Beta. „Leveln“ ist die Reihenfolge der Punkte von Stufe 10 bis 60; 31–60 stammen aus dem Level-Guide der Klasse, nach dem Start gleichen wir sie mit dem Spiel ab.',
              '« Général » est la répartition des points au niveau 30 d’après la bêta. « Progression » est l’ordre des points du niveau 10 au 60 ; les niveaux 31–60 viennent du guide de progression de la classe, nous les vérifierons dans le jeu après le lancement.',
              '«General» es el reparto de puntos del nivel 30 según la beta. «Subida de nivel» es el orden de los puntos del nivel 10 al 60; del 31 al 60 sale de la guía de subida de la clase y lo comprobaremos en el juego tras el lanzamiento.',
              '“Geral” é a distribuição de pontos do nível 30 segundo a beta. “Evolução” é a ordem dos pontos do nível 10 ao 60; do 31 ao 60 vem do guia de evolução da classe e vamos conferir no jogo após o lançamento.',
              '«Generale» è la distribuzione dei punti al livello 30 secondo la beta. «Livellamento» è l’ordine dei punti dal livello 10 al 60; i livelli 31–60 vengono dalla guida al livellamento della classe e li verificheremo nel gioco dopo il lancio.',
              '„Ogólna” to rozkład punktów na 30 levelu z bety. „Levelowanie” to kolejność punktów od 10 do 60 levelu; poziomy 31–60 pochodzą z poradnika levelowania klasy, po starcie sprawdzimy je w grze.')]},
    {'id': 'legacy-points',
     'q': n9('Что с очками Legacy?', 'What about the Legacy points?', 'Що з очками Legacy?', 'Was ist mit den Legacy-Punkten?',
             'Et les points Legacy ?', '¿Qué pasa con los puntos de Legacy?', 'E os pontos de Legacy?', 'E i punti Legacy?', 'Co z punktami Legacy?'),
     'a': [n9('Перк Legacy Talented (до 5 рангов) открывает очки талантов раньше нормы, до 5 уровней. Куда их тратить, сказано в разделе «Таланты», если источники это называют. Все перки — в гайде Legacy.',
              'The Legacy perk Talented (up to 5 ranks) unlocks talent points earlier than normal, by up to 5 levels. Where to spend them is in the Talents section when the sources name it. All perks are in the Legacy guide.',
              'Перк Legacy Talented (до 5 рангів) відкриває очки талантів раніше за норму, до 5 рівнів. Куди їх витрачати, сказано в розділі «Таланти», якщо джерела це називають. Усі перки — в гайді Legacy.',
              'Der Legacy-Vorteil Talented (bis zu 5 Ränge) schaltet Talentpunkte früher frei, um bis zu 5 Stufen. Wohin damit, steht im Abschnitt Talente, wenn die Quellen es nennen. Alle Vorteile stehen im Legacy-Guide.',
              'L’avantage Legacy Talented (jusqu’à 5 rangs) débloque les points de talent plus tôt, jusqu’à 5 niveaux. Où les dépenser est indiqué dans la section Talents quand les sources le précisent. Tous les avantages sont dans le guide Legacy.',
              'La ventaja de Legacy Talented (hasta 5 rangos) desbloquea los puntos de talento antes, hasta 5 niveles. Dónde gastarlos se indica en la sección Talentos cuando las fuentes lo dicen. Todas las ventajas están en la guía de Legacy.',
              'O benefício de Legacy Talented (até 5 níveis) libera pontos de talento mais cedo, em até 5 níveis. Onde gastá-los está na seção Talentos quando as fontes dizem. Todos os benefícios estão no guia de Legacy.',
              'Il vantaggio Legacy Talented (fino a 5 gradi) sblocca i punti talento prima, fino a 5 livelli. Dove spenderli è indicato nella sezione Talenti quando le fonti lo dicono. Tutti i vantaggi sono nella guida Legacy.',
              'Atut Legacy Talented (do 5 rang) odblokowuje punkty talentów wcześniej, nawet o 5 leveli. Gdzie je wydać, podano w sekcji Talenty, jeśli źródła to mówią. Wszystkie atuty są w poradniku Legacy.')],
     'link': (n9('Гайд Legacy', 'Legacy guide', 'Гайд Legacy', 'Legacy-Guide', 'Guide Legacy', 'Guía de Legacy', 'Guia de Legacy', 'Guida Legacy',
                 'Poradnik Legacy'), '../legacy/')},
]
NEXT_PFX = n9('Дальше', 'Next', 'Далі', 'Weiter', 'Suite', 'Siguiente', 'Próximo', 'Avanti', 'Dalej')


def _name(x, lang):
    return x if isinstance(x, str) else (x.get(lang) or x['en'])


def _gear(key, i, lang):
    got = GEAR.get(key, {}).get(i)
    if not got:
        return escape(WAIT[i][lang])
    items, src = got
    return '<br>'.join(f'{escape(_name(n, lang))} — {escape(e[lang])}' for n, e in items) + f'<br><span class="small">{escape(src)}</span>'


def _h(text):
    return {l: f'<h3>{escape(text[l])}</h3>' for l in text if l in LANGS9}


def _section(guide, sid):
    return next(s for s in guide['sections'] if s['id'] == sid)


def attach(guides, hubs, order):
    """The four pages with their texts; the titles come in finish() (they need the names of all languages)."""
    by = {g['slug']: g for g in guides}
    for (cid, spec), slug in zip(CHEATS, SLUGS):
        bg, lv = by[f'builds-{cid}'], by[f'leveling-{cid}']
        sec = next(s for s in bg['sections'] if s['id'] == spec)
        roles = next(s for s in bg['sections'] if s['id'] == 'roles')['blocks'][0][1]
        rows = [r for r in roles['rows'] if sec['title']['ru'].startswith(r[0]['ru'].split(' (')[0])]   # Feral: cat and bear rows
        blocks = sec['blocks']
        texts = [d for k, d in blocks if k == 'text']
        tree = next(((k, d) for k, d in blocks if k == 'tree'), None)
        table = next((k, d) for k, d in blocks if k == 'table')
        steps = next((k, d) for k, d in blocks if k == 'steps')
        tip = next((k, d) for k, d in blocks if k == 'tip')
        lvl = lambda i: _section(lv, i)  # noqa: E731
        party = next(x for x in next(d for k, d in lvl('play')['blocks'] if k == 'tabs') if x['id'] == 'party')
        answer_table = (('table', {'head': roles['head'][1:4], 'rows': [rows[0][1:]]}) if len(rows) == 1 else
                        ('table', {'head': roles['head'], 'rows': rows}))
        tab_build = [('text', texts[0]), tip]
        tab_talents = ([tree] if tree else []) + [table] + [('text', x) for x in texts[1:]]
        tab_level = [('h3', lvl('spec')['title'])] + lvl('spec')['blocks'] + [('h3', lvl('talents')['title'])] + lvl('talents')['blocks']
        tab_group = party['blocks'] + [('text', [GROUP_NOTE])]
        guide = {
            'slug': slug, 'art': cid, 'hero': 'hero_leveling', 'hub': False, 'more': False, 'js': 'cheat', 'cheat': (cid, spec, rows, roles['head'][2], table[1]['rows']),
            'title': bg['title'], 'lead': bg['lead'], 'tile': sec['title'], 'pills': list(bg['pills'][:1]),
            'sources': [s for s in bg['sources'] if spec.split('-')[0].title() in s[0] or 'Calculator' in s[0]] or bg['sources'],
            'sections': [
                {'id': 'answer', 'title': ANSWER, 'blocks': [('raw', {}), answer_table]},
                {'id': 'build', 'title': TAB['build'], 'blocks': tab_build},
                {'id': 'talents', 'title': TAB['talents'], 'blocks': tab_talents},
                {'id': 'leveling', 'title': TAB['leveling'], 'blocks': tab_level},
                {'id': 'group', 'title': TAB['group'], 'blocks': tab_group},
                {'id': 'rotation', 'title': TAB['rotation'], 'blocks': [('text', [ROT_NOTE]), steps]},
                {'id': 'faq', 'title': FAQ_T, 'blocks': [('faq', FAQ)]},
                {'id': 'related', 'title': SEE_ALSO, 'blocks': [('tiles', [
                    {'t': FULL_BUILDS, 'd': bg['tile'], 'href': f'guides/builds-{cid}/#{spec}', 'art': cid},
                    {'t': FULL_LEVELING, 'd': lv['tile'], 'href': f'guides/leveling-{cid}/', 'art': 'hero_dawn'},
                    {'t': GROUP_TILE, 'd': GROUP_NOTE, 'href': 'tools/#raid', 'art': 'hero_tierlist'}])]},
            ],
        }
        guides.append(guide)
    for slug in SLUGS:
        if slug not in order:
            order.append(slug)
    guides.sort(key=lambda g: order.index(g['slug']))


def finish(guides, hero_core, langs_mod):
    """Titles, leads and the bar with the buttons in every language, then langs.fill for what is still short."""
    for g in guides:
        if g['slug'] not in SLUGS:
            continue
        cid, spec, rows, tierh, trows = g.pop('cheat')
        title, lead, bar = {}, {}, {}
        for lang in LANGS9:
            if lang not in langs_mod.LANGS:
                continue
            n = hero_core(lang)
            sn = n['sn'][cid][n['sid'][cid].index(spec)]
            title[lang] = f'{n["cn"][cid]} · {sn}'   # the dot stays with the class on a wrapped heading
            role = ' / '.join(r[1][lang] for r in rows)
            lead[lang] = f'{role} · {tierh[lang]}: {" / ".join(dict.fromkeys(r[2] for r in rows))}. {rows[0][3][lang]}. {LEAD_TAIL[lang]}'
            top = [trows[-1]] + sorted(trows[:-1], key=lambda r: -int(r[1]))[:4]   # the last row is the spec's main talent, then the most points
            keys = ' · '.join(f'{escape(_name(r[0], lang))} ×{r[1]}' for r in top)
            leveling_href = f'../leveling-{cid}/'
            st = STATS.get(f'{cid}-{spec}')
            stats = (escape(STATS_SPLIT[lang]) if st == 'split' else escape(STATS_NONE[lang]) if st is None else
                     ' › '.join(escape(STAT[k][lang]) for k in st[0].split()) + f' <span class="small">({st[1]})</span>')
            bar[lang] = (f'<div id="cheat" data-cls="{cid}" data-spec="{spec}" data-from="{escape(FROM_LINK[lang])}">'
                         f'<p class="small" id="cheatRace" hidden></p>'
                         f'<p id="cheatBest" data-l="{escape(BEST[lang])}"></p>'
                         f'<dl class="cxrows">'
                         f'<div><dt>{escape(GOAL[lang])}</dt><dd><a href="#leveling">{escape(GOAL_LV[lang])}</a> · '
                         f'<a href="#group">{escape(GOAL_DG[lang])}: {escape(role)}</a></dd></div>'
                         f'<div><dt>{escape(KEYT[lang])}</dt><dd>{keys}. <a href="#talents">{escape(ORDER_L[lang])}</a></dd></div>'
                         f'<div><dt>{escape(STATS_T[lang])}</dt><dd>{stats}</dd></div>'
                         + ''.join(f'<div><dt>{escape(r[lang])}</dt><dd>{_gear(f"{cid}-{spec}", i, lang)}</dd></div>' for i, r in enumerate(GEAR_ROWS)) +
                         f'</dl>'
                         f'<p class="gbtns"><a class="btn cxnext" href="{leveling_href}">{escape(NEXT_PFX[lang])}: {escape(TAB["leveling"][lang])} →</a> '
                         f'<a class="btn ghost" id="cheatPick" href="../../tools/#pick={cid}">{escape(PICK[lang])}</a> '
                         f'<button type="button" class="btn ghost" id="cheatShare">{escape(n["tx"]["share"])}</button> '
                         f'<span class="small" role="status" id="cheatMsg"></span></p></div>')
        g['title'], g['lead'], g['crumb'] = title, lead, title
        SEO[f'guides/{g["slug"]}/'] = ({l: f'{title[l]}: {SEO_TAIL[l]}' for l in title}, dict(lead))
        g['sections'][0]['blocks'][0] = ('raw', bar)
        for sec in g['sections']:                                  # the headings of the borrowed sections: raw html, built after fill
            sec['blocks'] = [('raw', _h(d)) if k == 'h3' else (k, d) for k, d in sec['blocks']]
        g['tile'] = title
    langs_mod.fill([g for g in guides if g['slug'] in SLUGS])
