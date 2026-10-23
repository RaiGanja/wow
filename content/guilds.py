"""Гильдии: лимиты правил, части герба, порядок открытий за знамёна (числа; тексты — i18n/me.*.txt).
Читают сайт и API (tools/export_game.py -> assets/game.json). Знаки — силуэты game-icons.net (CC BY 3.0)."""
import math, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tools'))
from svgpath import bbox, paths, points  # noqa: E402

LIMITS = {
    'members': 1000, 'officers': 5, 'request_days': 14, 'requests_user': 3, 'requests_guild': 50,
    'kick_days': 7, 'rename_days': 30, 'create_glory': 5, 'top': 10, 'rated_min': 5,
    'count_glory': 5, 'count_days': 7, 'banner_every': 4, 'banner_min': 3,
    'name_min': 2, 'name_max': 24, 'motto_max': 80, 'crest_max': 200, 'contrast_min': 2.0,
    # знак на гербе: масштаб в %, сдвиг в единицах viewBox 100; рамка знака целиком внутри формы с отступом pad (обводка)
    'scale_min': 60, 'scale_max': 140, 'shift_max': 40, 'crest_pad': 3, 'charge_size': 52,
}
SHAPES = ['heater', 'round', 'kite', 'banner']
# контуры форм во viewBox 100x100; центр знака и делений поля — центр масс формы (у щита он выше середины)
SHAPE_PATHS = {
    'heater': 'M8 6h84v38c0 26-18 42-42 50C26 86 8 70 8 44z',
    'round': 'M50 4a46 46 0 1 1 0 92a46 46 0 1 1 0-92z',
    'kite': 'M12 6h76v32c0 28-18 48-38 58C30 86 12 66 12 38z',
    'banner': 'M14 4h72v90L50 78L14 94z',
}
FIELDS = ['plain', 'pale', 'fess', 'quarterly', 'chevron', 'bend']
PALETTE = {
    'black': '#16171a', 'night': '#262b45', 'crimson': '#8f1f2e', 'ember': '#a3401c',
    'azure': '#2a5a8c', 'teal': '#1f5b5e', 'emerald': '#1f5a3a', 'purple': '#4b2466',
    'bronze': '#8a5a2b', 'gold': '#c9a54a', 'silver': '#b9bec6', 'bone': '#d9cfb8',
}
BORDERS = ['gold', 'silver', 'bronze', 'none']
# (id, путь на game-icons.net «автор/имя», замок). Путь заполняется в задаче 9 по поиску на сайте;
# lock=True — открывается знамёнами (волна 1б, порядок — BANNER_UNLOCKS).
CHARGES = [
    ('lion', 'lorc/lion', False), ('wolf', 'lorc/wolf-head', False), ('dragon', 'lorc/dragon-head', False),
    ('skull', 'lorc/skull-crossed-bones', False), ('griffin', 'delapouite/griffin-symbol', False),
    ('axe', 'lorc/battle-axe', False), ('sword', 'lorc/broadsword', False), ('crown', 'lorc/crown', False),
    ('moon', 'lorc/moon', False), ('tree', 'lorc/oak', False), ('eagle', 'lorc/eagle-emblem', False),
    ('bear', 'delapouite/bear-head', False), ('boar', 'caro-asercion/boar', False), ('stag', 'lorc/stag-head', False),
    ('raven', 'lorc/raven', False), ('serpent', 'lorc/snake', False), ('flame', 'carl-olsen/flame', False),
    ('tower', 'delapouite/castle', False), ('hammer', 'delapouite/warhammer', False), ('sun', 'lorc/sun', False),
    ('star', 'lorc/star-swirl', False), ('rose', 'lorc/rose', False), ('horse', 'delapouite/horse-head', False),
    ('fist', 'lorc/fist', False),
]
BANNER_UNLOCKS = []          # волна 1б: 'charge:<id>' в порядке открытия
DEFAULT_CREST = {'s': 'heater', 'f': 'plain', 'c': ['black', 'black'], 'i': 'griffin', 'ic': 'gold', 'b': 'gold'}
TEXTURE = os.path.join(os.path.dirname(__file__), '..', 'assets', 'me', 'crest', 'metal.webp')

def centroid(pts):
    a = cx = cy = 0.0
    for (x1, y1), (x2, y2) in zip(pts[-1:] + pts[:-1], pts):
        f = x1 * y2 - x2 * y1
        a, cx, cy = a + f, cx + (x1 + x2) * f, cy + (y1 + y2) * f
    return cx / (3 * a), cy / (3 * a)


def geometry():
    """Per shape: outline, centre (rounded to .5) and the outline as a polygon (for the 'charge inside the shape' check on the site and in the API)."""
    out = {}
    for k in SHAPES:
        pts = points(SHAPE_PATHS[k], 16)
        cx, cy = centroid(pts)
        poly = [[round(x, 1) + 0, round(y, 1) + 0] for x, y in pts]
        out[k] = {'d': SHAPE_PATHS[k], 'c': [round(cx * 2) / 2, round(cy * 2) / 2], 'poly': [p for i, p in enumerate(poly) if p != poly[i - 1]]}
    return out


def charge_box(cid):
    """Width and height of the glyph in its 512 box (the sprite centres it; tools/make_crest.py)."""
    src = os.path.join(os.path.dirname(__file__), '..', 'assets', 'me', 'crest', 'src', cid + '.svg')
    bs = [bbox(d) for d in paths(open(src, encoding='utf-8').read())]
    return [math.ceil(max(b[2] for b in bs) - min(b[0] for b in bs)), math.ceil(max(b[3] for b in bs) - min(b[1] for b in bs))]


def authors():
    """Unique game-icons.net authors of the charges (first path segment), in catalog order: for the license line on /privacy/."""
    return list(dict.fromkeys(path.split('/')[0] for _, path, _ in CHARGES))


def export():
    return {
        'limits': LIMITS, 'shapes': SHAPES, 'geo': geometry(), 'fields': FIELDS, 'palette': PALETTE, 'borders': BORDERS,
        'charges': [{'id': i, 'lock': lock, 'box': charge_box(i)} for i, _, lock in CHARGES],
        'banner_unlocks': BANNER_UNLOCKS, 'default_crest': DEFAULT_CREST, 'texture': os.path.exists(TEXTURE),
    }
