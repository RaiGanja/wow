"""Детектор официальных постов Blizzard про WoW Forever -> задача (issue) с меткой blue в RaiGanja/wow.
Источник: синие посты форумов Blizzard (US и EU), лента blizzard-tracker. Туда же попадают статьи news.blizzard.com /
worldofwarcraft.blizzard.com (их публикуют на форуме тем же постом), патчноуты и хотфиксы.
Признак Forever: раздел форума WoW: Forever (US 346–349, EU 359–362) или слово «Forever» в заголовке темы.
Повтор не создаётся: ключ поста (us-<тема>, ответ — us-<тема>-<номер поста>) уже есть в задачах с меткой blue
(открытых и закрытых) или ссылка на него уже в NEWS. Ответ с номером нужен: заметки разработчиков и патчноуты беты
Blizzard дописывает новыми ответами в одну и ту же тему (us 2360696, eu 631316), иначе ловилось бы только первое обновление.
Запуск: python tools/blue_watch.py           — показать новые посты (ничего не создаёт)
        python tools/blue_watch.py --issues  — создать задачи (GitHub Actions: .github/workflows/blue.yml, нужен GITHUB_TOKEN)
Сеть упала -> пишем в stderr и выходим с кодом 0: следующий запуск через 15 минут.

Запись в content/guides.py NEWS по задаче — TEMPLATE ниже, он же уходит в текст задачи."""
import html, json, os, re, sys, urllib.request
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = 'RaiGanja/wow'
LABEL = 'blue'
MAX_AGE_H = 24                      # older posts are not news any more (and the first run does not flood)
UA = {'User-Agent': 'gabella-wow-guide (+https://gabella.site/wow/)'}
FORUMS = {
    'us': ('https://us.forums.blizzard.com/en/wow', {346, 347, 348, 349}),
    'eu': ('https://eu.forums.blizzard.com/en/wow', {359, 360, 361, 362}),
}
TEMPLATE = """Запись в content/guides.py, список NEWS (новые сверху), факты только из первоисточника:
{'date': 'ГГГГ-ММ-ДД',                       # дата поста Blizzard
 'url': 'https://…',                          # первоисточник: пост форума Blizzard или статья worldofwarcraft.blizzard.com
 'title': t(ru, en, uk),                      # до ~60 знаков, суть, без «Blizzard объявила»
 'text': t(ru, en, uk),                       # 3–5 строк сути: даты, время с UTC, цифры, кого касается
 'so': t(ru, en, uk),                         # одна строка «что это значит для игрока»
 'cls': 'all' | 'mage priest'}                # только если пост меняет классы: «касается вашего класса»
Переводы de, fr, es, pt, it, pl — в i18n/<lang>.json по английской строке (python build.py --missing <lang>).
Источник — в 'sources' гайда news. Выкатка: build.py -> tests/run_all.py -> коммит -> pull --rebase -> push -> md5 живой = собранной."""


def get(url):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30))


def clean(s, limit=500):
    s = html.unescape(re.sub(r'<[^>]+>', ' ', s or ''))
    s = re.sub(r'\s+', ' ', s).strip()
    return s if len(s) <= limit else s[:limit].rsplit(' ', 1)[0] + '…'


def pick(posts, region, now):
    """Forever posts of one region's blue tracker, not older than MAX_AGE_H: {key, region, topic, title, url, at, reply, excerpt}."""
    base, cats = FORUMS[region]
    out = []
    for p in posts:
        title = html.unescape(p.get('topic_title') or '')
        if p.get('category_id') not in cats and 'forever' not in title.lower():
            continue
        at = datetime.fromisoformat(p['created_at'].replace('Z', '+00:00'))
        if (now - at).total_seconds() > MAX_AGE_H * 3600:
            continue
        n = p.get('post_number', 1)
        # a reply is keyed by its post number: Blizzard adds each new Development Notes / patch notes update as a reply
        # to the same long-lived topic (us 2360696), so a topic-only key would swallow every update after the first
        out.append({'key': f'{region}-{p["topic_id"]}' + (f'-{n}' if n > 1 else ''), 'region': region, 'topic': p['topic_id'], 'title': title,
                    'url': f'{base}/t/{p["topic_id"]}/{p["post_number"]}', 'at': at, 'reply': p.get('post_number', 1) > 1,
                    'excerpt': clean(p.get('excerpt'))})
    return out


def merge(found):
    """One item per story: a topic once per run (its first blue post), the same post in US and EU once (US link first):
    a new topic by its title, a reply by its title and post number (Development Notes updates go out in both regions)."""
    seen_topic, seen_title, out = set(), set(), []
    for x in sorted(found, key=lambda x: (x['at'], x['region'] != 'us')):
        norm = re.sub(r'\W+', ' ', x['title'].lower()).strip()
        # US and EU titles of one topic differ in the date («Updated October 26» / «Updated 26 October»): a reply matches
        # by the first five words of the title and its post number
        story = (' '.join(norm.split()[:5]), x['url'].rsplit('/', 1)[1]) if x['reply'] else (norm, '')
        topic = f"{x['region']}-{x['topic']}"
        if topic in seen_topic or story in seen_title:
            continue
        seen_topic.add(topic)
        seen_title.add(story)
        out.append(x)
    return out


def known_urls():
    """Topic keys already in NEWS (content/guides.py): a post written up by hand is not a new task."""
    src = open(os.path.join(ROOT, 'content', 'guides.py'), encoding='utf-8').read()
    rx = r'https://(us|eu)\.forums\.blizzard\.com/en/wow/t/(?:[a-z0-9-]*[a-z-][a-z0-9-]*/)?(\d+)(?:/(\d+))?'   # slug has a letter
    return {f'{r}-{n}' + (f'-{p}' if p and p != '1' else '') for r, n, p in re.findall(rx, src)}


def gh(method, path, token, body=None):
    req = urllib.request.Request(f'https://api.github.com{path}', method=method,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={'Authorization': f'Bearer {token}', 'Accept': 'application/vnd.github+json', **UA})
    return json.load(urllib.request.urlopen(req, timeout=30))


def issue_keys(token):
    issues = gh('GET', f'/repos/{REPO}/issues?labels={LABEL}&state=all&per_page=100', token)
    return {k for i in issues for k in re.findall(r'\[((?:us|eu)-\d+(?:-\d+)?)\]', i['title'])}


def body(x):
    kind = 'ответ разработчика в теме' if x['reply'] else 'новый пост'
    return (f"Blizzard, {kind}: {x['url']}\n"
            f"Пост: {x['at']:%Y-%m-%d %H:%M} UTC. На сайте до {x['at'] + timedelta(hours=3):%Y-%m-%d %H:%M} UTC (3 часа).\n\n"
            f"> {x['excerpt']}\n\n```\n{TEMPLATE}\n```\n")


def main(argv):
    now = datetime.now(timezone.utc)
    found = []
    for region, (base, _) in FORUMS.items():
        try:
            found += pick(get(f'{base}/groups/blizzard-tracker/posts.json')['posts'], region, now)
        except Exception as e:
            print(f'skip {region}: {e}', file=sys.stderr)
    items = [x for x in merge(found) if x['key'] not in known_urls()]
    token = os.environ.get('GITHUB_TOKEN')
    if '--issues' not in argv or not token:
        for x in items:
            print(f"{x['at']:%Y-%m-%d %H:%M} [{x['key']}] {'↳ ' if x['reply'] else ''}{x['title']} {x['url']}")
        print(f'{len(items)} new' + ('' if '--issues' not in argv else ' (no GITHUB_TOKEN: nothing created)'))
        return
    try:
        have = issue_keys(token)
    except Exception as e:
        print(f'skip: issues: {e}', file=sys.stderr)
        return
    for x in items:
        if x['key'] in have:
            continue
        title = f"[{x['key']}] {'Ответ: ' if x['reply'] else ''}{x['title']}"[:200]
        gh('POST', f'/repos/{REPO}/issues', token, {'title': title, 'body': body(x), 'labels': [LABEL]})
        print('issue:', title)


if __name__ == '__main__':
    main(sys.argv[1:])
