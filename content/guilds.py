"""Гильдии: лимиты правил, части герба, порядок открытий за знамёна (числа; тексты — i18n/me.*.txt).
Читают сайт и API (tools/export_game.py -> assets/game.json). Знаки — силуэты game-icons.net (CC BY 3.0)."""
import os

LIMITS = {
    'members': 1000, 'officers': 5, 'request_days': 14, 'requests_user': 3, 'requests_guild': 50,
    'kick_days': 7, 'rename_days': 30, 'create_glory': 5, 'top': 10, 'rated_min': 5,
    'count_glory': 5, 'count_days': 7, 'banner_every': 4, 'banner_min': 3,
    'name_min': 2, 'name_max': 24, 'motto_max': 80, 'crest_max': 200, 'contrast_min': 2.0,
}
SHAPES = ['heater', 'round', 'kite', 'banner']
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
    ('bear', 'delapouite/bear-head', False), ('boar', 'caro-asercion/boar', False), ('stag', 'delapouite/deer-head', False),
    ('raven', 'lorc/raven', False), ('serpent', 'lorc/snake', False), ('flame', 'lorc/flame', False),
    ('tower', 'delapouite/castle', False), ('hammer', 'lorc/warhammer', False), ('sun', 'lorc/sun', False),
    ('star', 'lorc/star-swirl', False), ('rose', 'lorc/rose', False), ('horse', 'delapouite/horse-head', False),
    ('fist', 'lorc/fist', False),
]
BANNER_UNLOCKS = []          # волна 1б: 'charge:<id>' в порядке открытия
DEFAULT_CREST = {'s': 'heater', 'f': 'plain', 'c': ['black', 'black'], 'i': 'griffin', 'ic': 'gold', 'b': 'gold'}
TEXTURE = os.path.join(os.path.dirname(__file__), '..', 'assets', 'me', 'crest', 'metal.webp')


def export():
    return {
        'limits': LIMITS, 'shapes': SHAPES, 'fields': FIELDS, 'palette': PALETTE, 'borders': BORDERS,
        'charges': [{'id': i, 'lock': lock} for i, _, lock in CHARGES],
        'banner_unlocks': BANNER_UNLOCKS, 'default_crest': DEFAULT_CREST, 'texture': os.path.exists(TEXTURE),
    }
