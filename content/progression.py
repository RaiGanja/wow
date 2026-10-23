"""Прокачка профиля: Слава, отдых, недельные задания, сезоны, цвета имени (русский исходник чисел; тексты — i18n/me.*.txt).
Читают сайт и API (tools/export_game.py -> assets/game.json). Числа подгоняет тест темпа gabella-api/test/pace.test.ts."""

GLORY = {'max': 60, 'a': 60, 'b': 14, 'p': 1.15}            # шаг n->n+1 = round(a + b * n ** p)
# источник: (опыт, потолок в день по МСК, удваивается отдыхом)
SOURCES = {'visit': (30, 30, True), 'radio': (5, 120, True), 'page': (10, 100, True), 'tool': (20, 60, True)}
ACH_XP = 20                                                 # за очко достижения
WEEKLY_XP, WEEKLY_ALL_XP = 400, 600
RESTED = {'period_h': 8, 'per_period': 0.05, 'cap': 1.5}    # доли стоимости текущего шага
WEEK_ANCHOR = '2026-10-28T04:00:00Z'                        # среда 07:00 МСК, неделя 0
WEEKLY_CATS = ['radio', 'guide', 'tools', 'rhythm']
STATIONS_KEY, GUIDE_KEY = 'station', 'guide'


def weekly(sets):
    """Пул заданий. key — ключ /progress (или visit, radio_min, lfg); item — конкретный элемент набора; goal — сколько раз;
    distinct — считать разные элементы."""
    t = [
        dict(id='radio_hour', cat='radio', key='radio_min', goal=12),           # 12 пульсов по 5 мин
        dict(id='radio_3h', cat='radio', key='radio_min', goal=36),
        dict(id='stations3', cat='radio', key='station', goal=3, distinct=True),
        dict(id='guides3', cat='guide', key='guide', goal=3, distinct=True),
        dict(id='classes3', cat='guide', key='class', goal=3, distinct=True),
        dict(id='races3', cat='guide', key='race', goal=3, distinct=True),
        dict(id='party5', cat='tools', key='party5', goal=1),
        dict(id='raid40', cat='tools', key='raid40', goal=1),
        dict(id='compare3', cat='tools', key='compare3', goal=1),
        dict(id='share_team', cat='tools', key='share_team', goal=1),
        dict(id='search5', cat='tools', key='search', goal=5),
        dict(id='days3', cat='rhythm', key='visit', goal=3),
        dict(id='days5', cat='rhythm', key='visit', goal=5),
        dict(id='lfg', cat='rhythm', key='lfg', goal=1),
        dict(id='show_card', cat='rhythm', key='show_card', goal=1),
        dict(id='play_page', cat='rhythm', key='play_page', goal=1),
    ]
    t += [dict(id='st_' + s, cat='radio', key='station', item=s, goal=1) for s in sets['station']]
    t += [dict(id='g_' + g, cat='guide', key='guide', item=g, goal=1) for g in sets['guide']]
    t += [dict(id='c_' + c, cat='guide', key='class', item=c, goal=1) for c in sets['class']]
    return t


SEASONS = [{'id': 's1', 'starts': '2026-11-03T21:00:00Z', 'min_weeks': 8}]
STAR_XP, WEEK_STARS = 2000, 3
# 30 ступеней: порог звёзд round(1.2 * k); награды — косметика навсегда, остальные ступени — сундук опыта
_REW = {5: 'badge:s1', 10: 'bg:s1-1', 15: 'title:pioneer', 20: 'bg:s1-2', 30: 'frame:s1'}
TRACK = {'s1': [{'step': k, 'stars': round(1.2 * k), 'reward': _REW.get(k), 'xp': 0 if k in _REW else 300} for k in range(1, 31)]}
NAME_COLORS = [('poor', 1), ('common', 1), ('uncommon', 15), ('rare', 30), ('epic', 45), ('legendary', 60)]
MOTTO_GLORY, REPORT_GLORY, REPORTS_HIDE = 5, 10, 3
