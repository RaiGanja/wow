"""Шпоры спеков: guides/spec-<класс>-<спек>/, вкладки Билд · Таланты · Прокачка 1→60 · С кем играть · БиС · Ротация.
Страница не пишет новых фактов о игре: вкладки собираются из готовых разделов builds-<класс> и leveling-<класс>.
«БиС» и «Ротация» до старта 05.11 пустые и говорят это честно (бета была открыта до 30 уровня).
Ссылка на билд b/<раса>-<класс>-<спек>/ у этих спеков ведёт сюда (build_cards.py), «Поделиться» на странице делится той же ссылкой.
Заготовка attach() кладёт страницы в GUIDES до langs.fill, finish() добавляет названия на всех языках (нужен hero_core из build_guides)."""
from html import escape

# (класс, спек): самые частые по данным сайта — оба прокачиваемых «быстрых» спека (Охотник S и Маг S в тир-листе прокачки),
# лучший танк беты и лекарь (Послушание, S в PvE и PvP); роли: 2 урона, танк, лекарь. Выбор Вячеслава 28.10
CHEATS = [('hunter', 'beast-mastery'), ('mage', 'frost'), ('paladin', 'protection'), ('priest', 'discipline')]
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
    'bis': n9('БиС · после старта', 'BiS · after launch', 'БіС · після старту', 'BiS · nach dem Start', 'BiS · après le lancement',
              'BiS · tras el lanzamiento', 'BiS · após o lançamento', 'BiS · dopo il lancio', 'BiS · po starcie'),
    'rotation': n9('Ротация · после старта', 'Rotation · after launch', 'Ротація · після старту', 'Rotation · nach dem Start',
                   'Rotation · après le lancement', 'Rotación · tras el lanzamiento', 'Rotação · após o lançamento',
                   'Rotazione · dopo il lancio', 'Rotacja · po starcie'),
}
PICK = n9('Подобрать свою расу', 'Pick your race', 'Підібрати свою расу', 'Eigene Rasse wählen', 'Choisir ma race', 'Elegir mi raza',
          'Escolher minha raça', 'Scegli la tua razza', 'Wybierz swoją rasę')
FROM_LINK = n9('Раса из ссылки', 'Race from the link', 'Раса з посилання', 'Rasse aus dem Link', 'Race du lien', 'Raza del enlace',
               'Raça do link', 'Razza dal link', 'Rasa z linku')
BIS_NOTE = n9(
    'Лучшее снаряжение 60 уровня появится после старта 5 ноября. На бете был открыт только 30 уровень, предметы 60 уровня Forever пока неизвестны. Список добавим по данным игры.',
    'The best level 60 gear will appear after the Nov 5 launch. The beta only went up to level 30, and Forever’s level 60 items are not known yet. We will add the list from the game’s data.',
    'Найкраще спорядження 60 рівня з’явиться після старту 5 листопада. У беті був відкритий лише 30 рівень, предмети 60 рівня Forever поки невідомі. Додамо список за даними гри.',
    'Die beste Ausrüstung für Stufe 60 folgt nach dem Start am 5. November. Die Beta ging nur bis Stufe 30, die Gegenstände für Stufe 60 in Forever sind noch unbekannt. Wir ergänzen die Liste anhand der Spieldaten.',
    'Le meilleur équipement du niveau 60 arrivera après le lancement du 5 novembre. La bêta n’allait que jusqu’au niveau 30, les objets du niveau 60 de Forever sont encore inconnus. Nous ajouterons la liste d’après les données du jeu.',
    'El mejor equipo de nivel 60 llegará tras el lanzamiento del 5 de noviembre. La beta solo llegó al nivel 30 y los objetos de nivel 60 de Forever aún no se conocen. Añadiremos la lista con los datos del juego.',
    'O melhor equipamento do nível 60 virá após o lançamento de 5 de novembro. A beta foi aberta só até o nível 30 e os itens do nível 60 do Forever ainda são desconhecidos. Vamos adicionar a lista com os dados do jogo.',
    'Il miglior equipaggiamento di livello 60 arriverà dopo il lancio del 5 novembre. La beta arrivava solo al livello 30 e gli oggetti di livello 60 di Forever non sono ancora noti. Aggiungeremo la lista dai dati del gioco.',
    'Najlepszy sprzęt na 60 level pojawi się po starcie 5 listopada. Beta sięgała tylko 30 levelu, a przedmioty 60 levelu w Forever nie są jeszcze znane. Dodamy listę na podstawie danych z gry.')
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
        row = next(r for r in roles['rows'] if sec['title']['ru'].startswith(r[0]['ru']))
        blocks = sec['blocks']
        texts = [d for k, d in blocks if k == 'text']
        tree = next(((k, d) for k, d in blocks if k == 'tree'), None)
        table = next((k, d) for k, d in blocks if k == 'table')
        steps = next((k, d) for k, d in blocks if k == 'steps')
        tip = next((k, d) for k, d in blocks if k == 'tip')
        lvl = lambda i: _section(lv, i)  # noqa: E731
        party = next(x for x in next(d for k, d in lvl('play')['blocks'] if k == 'tabs') if x['id'] == 'party')
        answer_table = ('table', {'head': [roles['head'][1], roles['head'][2], roles['head'][3]], 'rows': [row[1:]]})
        tab_build = [('text', texts[0]), tip]
        tab_talents = ([tree] if tree else []) + [table] + [('text', x) for x in texts[1:]]
        tab_level = [('h3', lvl('spec')['title'])] + lvl('spec')['blocks'] + [('h3', lvl('talents')['title'])] + lvl('talents')['blocks']
        tab_group = party['blocks'] + [('text', [GROUP_NOTE])]
        guide = {
            'slug': slug, 'art': cid, 'hero': 'hero_leveling', 'hub': False, 'more': False, 'js': 'cheat', 'cheat': (cid, spec, row, roles['head'][2]),
            'title': bg['title'], 'lead': bg['lead'], 'tile': sec['title'], 'pills': list(bg['pills'][:1]),
            'sources': [s for s in bg['sources'] if spec.split('-')[0].title() in s[0] or 'Calculator' in s[0]] or bg['sources'],
            'sections': [
                {'id': 'answer', 'title': ANSWER, 'blocks': [('raw', {}), answer_table]},
                {'id': 'build', 'title': TAB['build'], 'blocks': tab_build},
                {'id': 'talents', 'title': TAB['talents'], 'blocks': tab_talents},
                {'id': 'leveling', 'title': TAB['leveling'], 'blocks': tab_level},
                {'id': 'group', 'title': TAB['group'], 'blocks': tab_group},
                {'id': 'bis', 'title': TAB['bis'], 'blocks': [('text', [BIS_NOTE])]},
                {'id': 'rotation', 'title': TAB['rotation'], 'blocks': [('text', [ROT_NOTE]), steps]},
                {'id': 'related', 'title': SEE_ALSO, 'blocks': [('tiles', [
                    {'t': FULL_BUILDS, 'd': bg['tile'], 'href': f'guides/builds-{cid}/#{spec}', 'art': cid},
                    {'t': FULL_LEVELING, 'd': lv['tile'], 'href': f'guides/leveling-{cid}/', 'art': 'hero_dawn'},
                    {'t': GROUP_TILE, 'd': GROUP_NOTE, 'href': 'tools/#raid', 'art': 'hero_tierlist'}])]},
            ],
        }
        guides.append(guide)
    guides.sort(key=lambda g: order.index(g['slug']))


def finish(guides, hero_core, langs_mod):
    """Titles, leads and the bar with the buttons in every language, then langs.fill for what is still short."""
    for g in guides:
        if g['slug'] not in SLUGS:
            continue
        cid, spec, row, tierh = g.pop('cheat')
        title, lead, bar = {}, {}, {}
        for lang in LANGS9:
            if lang not in langs_mod.LANGS:
                continue
            n = hero_core(lang)
            sn = n['sn'][cid][n['sid'][cid].index(spec)]
            title[lang] = f'{n["cn"][cid]} · {sn}'
            lead[lang] = f'{row[1][lang]} · {tierh[lang]}: {row[2]}. {row[3][lang]}. {LEAD_TAIL[lang]}'
            bar[lang] = (f'<div id="cheat" data-cls="{cid}" data-spec="{spec}" data-from="{escape(FROM_LINK[lang])}">'
                         f'<p class="small" id="cheatRace" hidden></p>'
                         f'<p id="cheatBest" data-l="{escape(BEST[lang])}"></p>'
                         f'<p class="gbtns"><a class="btn" id="cheatPick" href="../../tools/#pick={cid}">{escape(PICK[lang])}</a> '
                         f'<button type="button" class="btn ghost" id="cheatShare">{escape(n["tx"]["share"])}</button> '
                         f'<span class="small" role="status" id="cheatMsg"></span></p></div>')
        g['title'], g['lead'], g['crumb'] = title, lead, title
        SEO[f'guides/{g["slug"]}/'] = ({l: f'{title[l]}: {SEO_TAIL[l]}' for l in title}, dict(lead))
        g['sections'][0]['blocks'][0] = ('raw', bar)
        for sec in g['sections']:                                  # the headings of the borrowed sections: raw html, built after fill
            sec['blocks'] = [('raw', _h(d)) if k == 'h3' else (k, d) for k, d in sec['blocks']]
        g['tile'] = title
    langs_mod.fill([g for g in guides if g['slug'] in SLUGS])
