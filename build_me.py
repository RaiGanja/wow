"""Профили: тексты для assets/me/me.js -> assets/me/i18n-<lang>.json (названия и описания достижений, подсказки секретов,
ранги, рамки, категории, очки, подписи тоста и шапки) и страницы «Состав» (roster/), «Мой профиль» (profile/), игрок (u/).
Страницы: оболочка me.src.html + общие me-pages.src.css/js + фрагмент roster|profile|player.src.html (style, body, script).
Русский исходник — content/achievements.py, UI ниже и русский текст страниц; en/uk — i18n/me.{ru,en,uk}.txt (строка в строку),
новые языки — i18n/<lang>.json по английской строке (как весь сайт). Тексты прокачки — GROWTH ниже.
Запуск: python build_me.py [--list]  (build.py запускает его сам; --list печатает русские фрагменты страниц без перевода)"""
import json, os, re, sys

import build
import langs
from langs import LANGS

HERE = build.HERE
sys.path.insert(0, os.path.join(HERE, 'content'))
import achievements as A  # noqa: E402
import looks as LK  # noqa: E402
import guides as G  # noqa: E402
langs.fill(G.GUIDES)

_ru, _en, _uk = (build.load(f'me.{l}.txt') for l in langs.OLD)
assert len(_ru) == len(_en) == len(_uk), (len(_ru), len(_en), len(_uk))
build.T.update({r: (e, u) for r, e, u in zip(_ru, _en, _uk)})

UI = {'got': 'Достижение получено', 'rankUp': 'Новый ранг', 'profile': 'Мой профиль', 'login': 'Войти', 'pts': 'очков', 'ptsN': 'Очки: {n}',
      'lvlAsk': 'На странице «В игре» у вас {n} уровень. Обновить персонажа {name}?', 'update': 'Обновить', 'notNow': 'Не сейчас',
      'menu': 'Меню профиля', 'myPage': 'Моя страница ↗', 'chars': 'Персонажи', 'look': 'Внешний вид', 'account': 'Аккаунт',
      'newChar': 'Создать персонажа', 'noChar': 'Персонажа пока нет', 'logout': 'Выйти'}

# Прокачка: тексты Славы, недельных заданий, сезона, витрины, хроники, жалоб. Ключ -> русская строка; сайт читает их из i18n-<lang>.json (раздел g).
# Переводы: en/uk — в конце i18n/me.*.txt (строка в строку), остальные — i18n/<lang>.json по английской строке. Шаблоны: {n} {d} {p} {x} {a} {r} {name}.
GROWTH = {
    'glory': 'Слава',
    'glory_n': 'Слава {n}',
    'glory_rested': 'Вы отдохнули в таверне — опыт ×2',
    'week': 'Задания недели',
    'week_ends': 'До сброса {d}',
    'week_swap': 'Заменить',
    'week_swap_used': 'Замена на этой неделе уже была',
    'week_streak': 'Недель подряд: {n}',
    'week_all': 'Все три — +600 опыта и 3 звезды сезона',
    'season': 'Сезон 1',
    'season_stars': 'Звёзды: {n}',
    'season_step': 'Ступень {n} из 30',
    'season_toast': 'Ступень сезона {n}',
    'season_keep': 'Всё полученное остаётся навсегда',
    'showcase': 'Витрина',
    'showcase_hint': 'До пяти наград. Порядок — ваш',
    'rarity': 'есть у {p}% игроков',
    'name_color': 'Цвет имени',
    'color_poor': 'Серый',
    'color_common': 'Белый',
    'color_uncommon': 'Зелёный',
    'color_rare': 'Синий',
    'color_epic': 'Фиолетовый',
    'color_legendary': 'Оранжевый',
    'color_locked': 'Со Славы {n}',
    'chronicle': 'Хроника',
    'chronicle_hide': 'Скрыть хронику от других',
    'chronicle_more': 'Показать ещё',
    'ch_join': 'Новый игрок Gabella',
    'ch_step': 'Ступень {n} сезона',
    'ch_badge': 'Значок «Сезон 1»',
    'ch_lvl60': '{name} — 60 уровень',
    'ch_ach': 'Получено «{a}»',
    'ch_rank': 'Ранг: {r}',
    'motto_later': 'Будет виден другим со Славы 5',
    'report': 'Пожаловаться',
    'report_name': 'Имя',
    'report_motto': 'Девиз',
    'report_other': 'Другое',
    'report_sent': 'Жалоба отправлена',
    'report_limit': 'Вы уже жаловались сегодня',
    'tab_all': 'Все игроки',
    'verified': 'Подтверждено',
    'teaser': 'Профиль копит ваш путь: Слава, рамки, сезоны',
    'err_bad_word': 'Так нельзя: выберите другие слова',
    'err_no_links': 'Без ссылок и упоминаний',
    'err_members_only': 'Вход временно только для участников Gabella Team',
    'task_radio_hour': 'Час радио',
    'task_radio_3h': 'Три часа радио',
    'task_stations3': 'Три разные станции',
    'task_guides3': 'Три гайда',
    'task_classes3': 'Три класса',
    'task_races3': 'Три расы',
    'task_party5': 'Собрать группу на пятерых',
    'task_raid40': 'Собрать рейд на сорок',
    'task_compare3': 'Сравнить три класса или расы',
    'task_share_team': 'Поделиться составом группы',
    'task_search5': 'Пять поисков по сайту',
    'task_days3': 'Зайти в три разных дня',
    'task_days5': 'Зайти в пять разных дней',
    'task_lfg': 'Включить «Ищу группу»',
    'task_show_card': 'Поделиться своей страницей',
    'task_play_page': 'Открыть «В игре»',
    'task_st': 'Станция «{x}»',
    'task_g': 'Гайд «{x}»',
    'task_c': 'Класс: {x}',
    'title_pioneer': 'Первопроходец',
    'bg_s1-1': 'Сезон 1: рассвет',
    'bg_s1-2': 'Сезон 1: ночь',
    'task_done': 'Выполнено',
    'act_radio': 'Включить радио',
    'act_guides': 'Открыть гайды',
    'act_classes': 'Открыть классы',
    'act_races': 'Открыть расы',
    'act_party': 'Собрать группу',
    'act_raid': 'Собрать рейд',
    'act_compare': 'Сравнить',
    'act_search': 'Искать',
    'act_lfg': 'Ищу группу',
    'act_copy': 'Скопировать ссылку',
    'act_play': 'Открыть «В игре»',
    'showcase_up': 'Выше',
    'showcase_down': 'Ниже',
    'showcase_del': 'Убрать из витрины',
    'showcase_add': 'Добавить',
    'showcase_empty': 'Пусто',
    'chronicle_empty': 'Пока пусто',
    'tab_reports': 'Жалобы',
    'reports_n': 'Жалоб: {n}',
    'reports_empty': 'Открытых жалоб нет',
    'rep_keep': 'Оставить',
    'rep_hide': 'Скрыть',
    'rep_ban': 'Бан',
    'rep_ban_ask': 'Забанить игрока? Его сессии закончатся.',
    'rep_now': 'Сейчас: {x}',
    'err_task_done': 'Это задание уже выполнено',
    'err_bad_showcase': 'Витрина: до пяти наград из полученных',
    'err_swap_used': 'Замена на этой неделе уже была',
    'tab_team': 'Gabella Team',   # без перевода
    'tab_team_hint': 'Участники сервера Gabella',
    'xp_first': 'Слава растёт — смотрите профиль',
    'report_field': 'Что не так',
    'report_reason': 'Причина (необязательно)',
    'report_send': 'Отправить',
    'report_cancel': 'Отмена',
    'err_report': 'Не получилось отправить',
    'verify_level': 'Подтвердить уровень',
    'verify_ask': 'Уровень персонажа {name} (1–60)',
    'verify_done': 'Уровень подтверждён',
    'verify_bad': 'Нужно число от 1 до 60',
    'team_empty': 'В Gabella Team пока никого',
    'menu': 'Действия',
    'close': 'Закрыть',
    'tabs_label': 'Состав',
}
GROWTH['glory_toast'] = GROWTH['ch_glory'] = GROWTH['glory_n']

# Guilds: UI texts of the guild pages and the crest (keys -> Russian source). Placeholders: %n %d %c %g %r.
GUILD = {
    'tab': 'Гильдии', 'tab_hint': 'Гильдии WoW Forever на Gabella',
    'power': 'Сила', 'power_hint': 'Средняя Слава 10 лучших участников', 'banners': 'Знамёна', 'streak': 'Серия',
    'sort_power': 'Сила', 'sort_banners': 'Знамёна', 'sort_new': 'Новые', 'search': 'Название гильдии',
    'size_n': '%n персонажей', 'size_few': '%n персонажа', 'size_1': '%n персонаж', 'unrated': 'Меньше 5 участников — без места в рейтинге', 'created': 'Создана %d',
    'hidden': 'Гильдия #%n', 'former': 'Бывший участник', 'empty': 'Гильдий пока нет',
    'leader': 'Глава', 'officer': 'Офицер', 'member': 'Участник',
    'members': 'Состав', 'chronicle': 'Хроника', 'more': 'Показать ещё', 'all_classes': 'Все классы', 'all_ranks': 'Все роли',
    'create': 'Создать гильдию', 'create_low': 'Со Славы 5', 'settings': 'Настроить', 'save': 'Сохранить', 'cancel': 'Отмена',
    'name': 'Название', 'motto': 'Девиз', 'crest': 'Герб', 'shape': 'Форма', 'field': 'Поле', 'charge': 'Знак', 'border': 'Кайма',
    'random': 'Случайный', 'border_none': 'Без каймы', 'pick_char': 'Персонаж',
    'link': 'Ссылка для приглашения', 'copy': 'Копировать', 'copied': 'Скопировано', 'reset': 'Сбросить ссылку',
    'reset_q': 'Старая ссылка перестанет работать.', 'requests': 'Заявки', 'accept': 'Принять', 'decline': 'Отклонить',
    'no_requests': 'Заявок нет', 'apply': 'Подать заявку', 'applied': 'Заявка отправлена', 'withdraw': 'Отозвать',
    'login_to_join': 'Войти, чтобы вступить', 'no_char': 'Нет персонажа этой фракции без гильдии',
    'leave': 'Выйти из гильдии', 'leave_q': 'Выйти из гильдии %g?', 'kick': 'Исключить', 'make_officer': 'Сделать офицером',
    'make_member': 'Снять с офицеров', 'make_leader': 'Сделать главой', 'leader_q': 'Сделать %c главой? Вы станете офицером.',
    'disband': 'Распустить гильдию', 'disband_q': 'Гильдия %g исчезнет вместе с хроникой.', 'my_guild': 'Моя гильдия',
    'char_guild': 'Гильдия: %g · %r', 'joined_toast': 'Вас приняли в %g',
    'ev_create': 'Гильдия создана', 'ev_join': '%c вступает в гильдию', 'ev_leave': '%c покидает гильдию', 'ev_kick': '%c исключают из гильдии',
    'ev_leader': '%c — новый глава', 'ev_rename': 'Новое название: %r',
    'report_name': 'Название гильдии', 'report_motto': 'Девиз гильдии', 'report_crest': 'Герб гильдии',
    'e_bad_name': 'Только буквы, пробел, апостроф и дефис, 2–24 знака', 'e_bad_word': 'Такое название не подойдёт',
    'e_no_links': 'Без ссылок', 'e_name_taken': 'Название уже занято', 'e_bad_crest': 'Герб не сохранился — выберите другое сочетание',
    'e_bad_motto': 'Девиз — до 80 знаков, без ссылок',
    'e_glory_low': 'Создать гильдию можно со Славы 5', 'e_one_leader': 'Вы уже глава гильдии', 'e_wrong_faction': 'Персонаж другой фракции',
    'e_already_in_guild': 'Персонаж уже в гильдии', 'e_in_guild': 'Сначала выйдите из гильдии', 'e_bad_code': 'Ссылка устарела — попросите новую',
    'e_too_many_requests': 'Не больше 3 заявок одновременно', 'e_guild_requests_full': 'У гильдии слишком много заявок — попробуйте позже',
    'e_guild_full': 'В гильдии нет мест', 'e_kicked_recently': 'Повторная заявка — через 7 дней после исключения',
    'e_rename_cooldown': 'Переименовать можно раз в 30 дней', 'e_officers_full': 'Не больше 5 офицеров',
    'e_leader_leaves': 'Сначала передайте главенство', 'e_rate': 'Одна новая гильдия в сутки',
    'e_generic': 'Не получилось. Обновите страницу и попробуйте ещё раз.', 'e_forbidden': 'Нет прав на это действие.', 'e_not_found': 'Уже неактуально — обновите страницу.',
    'not_found': 'Гильдия не найдена.',
    'color': 'Цвет', 'unlock_at': 'Знамя %n', 'bad_contrast': 'Не читается на этом поле',
    'pos': 'Положение знака', 'scale': 'Размер', 'shift_x': 'Влево и вправо', 'shift_y': 'Вверх и вниз', 'pos_reset': 'Сбросить',
    'pos_hint': 'Знак можно перетащить на гербе',
    'sh_heater': 'Классический', 'sh_round': 'Круглый', 'sh_kite': 'Удлинённый', 'sh_banner': 'Вымпел',
    'fl_plain': 'Сплошное', 'fl_pale': 'Вертикальное', 'fl_fess': 'Горизонтальное', 'fl_quarterly': 'Четверти', 'fl_chevron': 'Шеврон', 'fl_bend': 'Перевязь',
    'cg_lion': 'Лев', 'cg_wolf': 'Волк', 'cg_dragon': 'Дракон', 'cg_skull': 'Череп', 'cg_griffin': 'Грифон', 'cg_axe': 'Топор', 'cg_sword': 'Меч', 'cg_crown': 'Корона', 'cg_moon': 'Луна', 'cg_tree': 'Дерево', 'cg_eagle': 'Орёл', 'cg_bear': 'Медведь', 'cg_boar': 'Кабан', 'cg_stag': 'Олень', 'cg_raven': 'Ворон', 'cg_serpent': 'Змея', 'cg_flame': 'Пламя', 'cg_tower': 'Башня', 'cg_hammer': 'Молот', 'cg_sun': 'Солнце', 'cg_star': 'Звезда', 'cg_rose': 'Роза', 'cg_horse': 'Конь', 'cg_fist': 'Кулак',
    'col_black': 'Чёрный', 'col_night': 'Ночной', 'col_crimson': 'Багровый', 'col_ember': 'Ржавый', 'col_azure': 'Лазурный', 'col_teal': 'Бирюзовый', 'col_emerald': 'Изумрудный', 'col_purple': 'Пурпурный', 'col_bronze': 'Бронзовый', 'col_gold': 'Золотой', 'col_silver': 'Серебряный', 'col_bone': 'Костяной',
}


def strings():
    """Every Russian string me.js and the profile pages show, in a stable order (the line files follow it)."""
    out = list(UI.values()) + list(GROWTH.values()) + list(GUILD.values()) + [c[1] for c in A.CATS] + [r[2] for r in A.RANKS] + [f[2] for f in A.FRAMES]
    out += [n for _, n in LK.SCENES]
    for a in A.ACH:
        out += [a[5], a[6]] + ([a[7]] if len(a) > 7 else [])
    return [s for s in dict.fromkeys(out) if any('А' <= ch <= 'я' or ch in 'Ёё' for ch in s)]


def week_keys():
    """Weekly task id -> the progress key its events carry (radio_min, station, guide, ...)."""
    sys.path.insert(0, os.path.join(HERE, 'tools'))
    import export_game
    return {w['id']: w['key'] for w in export_game.game()['progression']['weekly']}


def texts(lang):
    missing = [s for s in strings() if s not in build.T]
    t = lambda s: build.tr(s, lang)   # noqa: E731
    ach = {}
    for a in A.ACH:
        ach[a[0]] = [t(a[5]), t(a[6])] + ([t(a[7])] if len(a) > 7 else [])
    return {
        'ui': {k: t(v) for k, v in UI.items()},
        'cats': {c[0]: t(c[1]) for c in A.CATS},
        'ranks': {r[0]: t(r[2]) for r in A.RANKS},
        'frames': {f[0]: t(f[2]) for f in A.FRAMES},
        'ach': ach,
        'pts': {a[0]: a[2] for a in A.ACH},
        'secret': [a[0] for a in A.ACH if len(a) > 7],
        'g': {k: t(v) for k, v in GROWTH.items()},
        'gl': {k: t(v) for k, v in GUILD.items()},
        'wk': week_keys(),                                                               # weekly task id -> progress key (me.js sends repeats of these)
        'titles': {x: t(GROWTH['title_' + x]) for x in A.TITLES if x not in ach},     # a title that is not an achievement (pioneer)
        'bg': {k[3:]: t(v) for k, v in GROWTH.items() if k.startswith('bg_')},       # season backgrounds by id (s1-1, s1-2)
    }, missing


PAGES = [('roster/', 'roster.src.html'), ('profile/', 'profile.src.html'), ('u/', 'player.src.html'), ('g/', 'guild.src.html')]
NOINDEX = {'profile/', 'u/', 'g/'}
INVITE = build.DISCORD   # кнопка «Вступить в Gabella Team» на экране «не участник»


def page_data(lang):
    """Game data the pages draw with: races and classes with names and colours, professions, achievement rules, ranks."""
    sys.path.insert(0, os.path.join(HERE, 'tools'))
    import export_game
    g = export_game.game()
    src = open(os.path.join(HERE, 'index.src.html'), encoding='utf-8').read()
    rn = {r['id']: r['n'] for r in build.parse_races(src)}
    block = src[src.index('const PROFS = ['):]
    pn = dict(re.findall(r"\['(\w+)', '([^']+)', 1,", block[:block.index('\n];')]))
    t = lambda s: build.tr(s, lang)   # noqa: E731
    return {
        'races': {rid: {'f': r['f'], 'cls': r['cls'], 'slug': r['slug'], 'n': t(rn[rid])} for rid, r in g['races'].items()},
        'classes': {c['id']: {'roles': g['classes'][c['id']]['roles'], 'n': t(c['n']), 'color': build.COLOR[c['id']]} for c in build.CLASSES},
        'profs': {p: t(pn[p]) for p in g['profs']},
        'sets': g['sets'], 'cats': g['cats'], 'ach': g['achievements'], 'ranks': g['ranks'], 'frames': g['frames'],
        'prog': {'glory_max': g['progression']['glory']['max'], 'colors': g['progression']['name_colors'],
                 'track': {sid: [[x['step'], x['stars'], x['reward']] for x in st] for sid, st in g['progression']['track'].items()},
                 'season': g['progression']['seasons'][0]['id'], 'motto_glory': g['progression']['motto_glory'],
                 'weekly': {w['id']: {k: w[k] for k in ('key', 'item') if k in w} for w in g['progression']['weekly']}},
        'guilds': g['guilds'], 'titles': g['titles'], 'backgrounds': g['backgrounds'], 'looks': g['looks'],
        'scenes': {s: t(n) for s, n in LK.SCENES}, 'deadline': g['deadline_founder'], 'invite': INVITE,
        'items': {'station': {x['id']: x['name'][lang] for x in json.load(open(os.path.join(HERE, 'assets', 'radio', 'stations.json'), encoding='utf-8'))['stations']},
                  'guide': {x['slug']: x['title'][lang] for x in G.GUIDES if 'only' not in x}},
    }


def part(src, rx, name):
    m = re.search(rx, src, re.S)
    assert m, name
    return m.group(1).strip('\n')


def build_page(lang, sub, frag, shell, base_css, sprite, me_css, me_js):
    here = build.page_dir(lang, sub)
    root, home = build.rel(here, ''), build.rel(here, build.page_dir(lang))
    html = shell.replace('@@BASE_CSS@@', base_css).replace('@@SPRITE@@', sprite).replace('@@ME_CSS@@', me_css)
    html = html.replace('@@TABBAR@@', build.tabbar('profile/' if sub == 'profile/' else None))
    html = html.replace('@@P_CSS@@', part(frag, r'<style>(.*?)</style>', 'style'))
    html = html.replace('@@P_BODY@@', part(frag, r'<!--body-->(.*?)<!--/body-->', 'body'))
    html = html.replace('@@ME_JS@@', me_js).replace('@@P_JS@@', part(frag, r'<script>(.*?)</script>', 'script'))
    name = part(frag, r'<h1[^>]*>(.*?)</h1>', 'h1')
    html = html.replace('@@P_NAME@@', re.sub('<[^>]+>', '', name))
    html = html.replace('@@P_ROBOTS@@', '<meta name="robots" content="noindex">\n' if sub in NOINDEX else '')
    html = html.replace('@@NAV_ROSTER@@', ' aria-current="true"' if sub == 'roster/' else '')
    html = html.replace('@@NAV_PROFILE@@', ' aria-current="true"' if sub == 'profile/' else '')
    html, missing = build.translate(html, lang)
    html = html.replace('@@GD@@', json.dumps(page_data(lang), ensure_ascii=False, separators=(',', ':')))
    html = html.replace('@@LANG@@', lang).replace('@@HOME@@', home).replace('@@CANON@@', build.SITE + here)
    html = html.replace('@@ALTERNATES@@', build.alternates(sub))
    if 'data-fx=' in html:                                         # living art over the hero (roster)
        html = html.replace('</body>', '<script src="@@ROOT@@assets/living/living.js" defer></script>\n</body>', 1)
    html = build.localize(html, lang, here).replace('assets/og.png', f'assets/og-{lang}.jpg')   # the site card (tools/make_og.py)
    return here + 'index.html', html, missing


def build_pages():
    src = open(os.path.join(HERE, 'index.src.html'), encoding='utf-8').read()
    base_css = src[src.index('<style>') + 7:src.index('</style>')].strip('\n')
    s0 = src.index('<svg width="0" height="0"')
    sprite = src[s0:src.index('</svg>', s0) + 6]
    read = lambda n: open(os.path.join(HERE, n), encoding='utf-8').read()   # noqa: E731
    shell, me_css, me_js = read('me.src.html'), read('me-pages.src.css'), read('me-pages.src.js')
    out, missing = [], []
    for lang in LANGS:
        for sub, name in PAGES:
            path, html, miss = build_page(lang, sub, read(name), shell, base_css, sprite, me_css, me_js)
            assert '@@' not in html, (path, re.findall(r'@@\w+@@', html)[:5])
            out.append((path, html))
            missing += miss
    return out, missing


def main():
    os.makedirs(os.path.join(HERE, 'assets', 'me'), exist_ok=True)
    allmissing = []
    for lang in LANGS:
        data, missing = texts(lang)
        allmissing += missing
        with open(os.path.join(HERE, 'assets', 'me', f'i18n-{lang}.json'), 'w', encoding='utf-8', newline='\n') as f:
            json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
            f.write('\n')
    uniq = list(dict.fromkeys(allmissing))
    if uniq:
        print('build_me: no en/uk line for:\n' + '\n'.join(uniq), file=sys.stderr)
        sys.exit(1)
    pages, missing = build_pages()
    uniq = list(dict.fromkeys(missing))
    if '--list' in sys.argv:          # build.py --list / --missing: report, write nothing
        if '--missing' not in sys.argv:
            print('\n'.join(uniq))
        return
    for path, html in pages:
        full = os.path.join(HERE, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        open(full, 'w', encoding='utf-8', newline='\n').write(html)
    print(f'build_me: pages {len(pages)}, missing {len(uniq)}', file=sys.stderr)
    if uniq:
        sys.exit(1)


if __name__ == '__main__':
    main()
