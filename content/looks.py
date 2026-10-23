"""Облик персонажа: пол и фон портрета. Спек: gabella-docs/wow/specs/2026-10-23-portraits-design.md.
tools/export_game.py кладёт это в assets/game.json (его читает API: проверка и умолчания)."""

V = '2'   # бамп при замене картинок в assets/me/look/ — Cloudflare держит /wow/assets/ 30 дней

SEXES = ['m', 'f']

# пол по умолчанию — как на прежнем лице расы, чтобы старые профили выглядели знакомо
SEX_DEFAULT = {'human': 'm', 'dwarf': 'f', 'gnome': 'm', 'nightelf': 'f', 'skyA': 'm',
               'orc': 'm', 'undead': 'm', 'tauren': 'm', 'troll': 'm', 'skyH': 'f'}

# новые пустые сцены Gemini: id → русское название (фон карточки и фон портрета)
SCENES = [('scene-tavern', 'Таверна'), ('scene-pass', 'Перевал'), ('scene-swamp', 'Топи'), ('scene-desert', 'Пустыня'),
          ('scene-nightwood', 'Ночной лес'), ('scene-harbor', 'Гавань'), ('scene-ruins', 'Руины'), ('scene-peak', 'Вершина')]

# запертые фоны: id → id награды (к 04.11 пусто; сезон и достижения добавят)
LOCK = {}
