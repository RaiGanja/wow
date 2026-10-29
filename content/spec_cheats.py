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
GEAR_T = n9('Экипировка, чары, камни, расходники', 'Gear, enchants, gems, consumables', 'Спорядження, чари, камені, витратні',
            'Ausrüstung, Verzauberungen, Edelsteine, Verbrauchsgüter', 'Équipement, enchantements, gemmes, consommables',
            'Equipo, encantamientos, gemas, consumibles', 'Equipamento, encantamentos, gemas, consumíveis',
            'Equipaggiamento, incantamenti, gemme, consumabili', 'Ekwipunek, zaklęcia, kamienie, materiały eksploatacyjne')
WAIT = n9('Ждёт данных: на бете был только 30 уровень, список Forever добавим после старта 5 ноября.',
          'Waiting for data: the beta stopped at level 30, the Forever list comes after the Nov 5 launch.',
          'Чекає на дані: у беті був лише 30 рівень, список Forever додамо після старту 5 листопада.',
          'Wartet auf Daten: Die Beta ging nur bis Stufe 30, die Forever-Liste folgt nach dem Start am 5. November.',
          'En attente de données : la bêta s’arrêtait au niveau 30, la liste Forever arrivera après le lancement du 5 novembre.',
          'A la espera de datos: la beta llegó solo al nivel 30, la lista de Forever llegará tras el lanzamiento del 5 de noviembre.',
          'Aguardando dados: a beta foi só até o nível 30, a lista do Forever vem após o lançamento de 5 de novembro.',
          'In attesa di dati: la beta arrivava solo al livello 30, la lista di Forever arriverà dopo il lancio del 5 novembre.',
          'Czeka na dane: beta sięgała tylko 30 levelu, listę Forever dodamy po starcie 5 listopada.')
NEXT_PFX = n9('Дальше', 'Next', 'Далі', 'Weiter', 'Suite', 'Siguiente', 'Próximo', 'Avanti', 'Dalej')


def _name(x, lang):
    return x if isinstance(x, str) else (x.get(lang) or x['en'])


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
            bar[lang] = (f'<div id="cheat" data-cls="{cid}" data-spec="{spec}" data-from="{escape(FROM_LINK[lang])}">'
                         f'<p class="small" id="cheatRace" hidden></p>'
                         f'<p id="cheatBest" data-l="{escape(BEST[lang])}"></p>'
                         f'<dl class="cxrows">'
                         f'<div><dt>{escape(GOAL[lang])}</dt><dd><a href="#leveling">{escape(GOAL_LV[lang])}</a> · '
                         f'<a href="#group">{escape(GOAL_DG[lang])}: {escape(role)}</a></dd></div>'
                         f'<div><dt>{escape(KEYT[lang])}</dt><dd>{keys}. <a href="#talents">{escape(ORDER_L[lang])}</a></dd></div>'
                         f'<div><dt>{escape(GEAR_T[lang])}</dt><dd>{escape(WAIT[lang])}</dd></div>'
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
