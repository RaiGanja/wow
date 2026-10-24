"""RSS Wowhead -> assets/news.json (только записи про Forever, 30 последних, новые сверху).
Источник и признак Forever — как в news.py бота gabella-bot: слово «forever» в заголовке, описании или категориях.
Сеть упала или RSS сломан -> ничего не пишем, выходим с кодом 0 (старый файл остаётся).
Запуск: python tools/fetch_news.py  (в GitHub Actions — .github/workflows/news.yml)"""
import json, os, sys, urllib.request
from email.utils import parsedate_to_datetime
from xml.etree import ElementTree as ET

FEED = 'https://www.wowhead.com/news/rss/all'
WOWHEAD = 'https://www.wowhead.com/'
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', 'news.json')


def parse(xml):
    out = []
    for it in ET.fromstring(xml).iter('item'):
        title = (it.findtext('title') or '').strip()
        cats = ' '.join(c.text or '' for c in it.findall('category'))
        if 'forever' not in ' '.join((title, it.findtext('description') or '', cats)).lower():
            continue
        url = (it.findtext('link') or '').strip()
        if not url.startswith(WOWHEAD):   # only links to Wowhead itself: a javascript: or foreign link in the feed is dropped
            continue
        when = parsedate_to_datetime(it.findtext('pubDate'))
        out.append((when.timestamp(), {'date': when.strftime('%Y-%m-%d'), 'title': title, 'url': url}))
    return [x for _, x in sorted(out, key=lambda p: p[0], reverse=True)][:30]


def merge(new, old):
    """The feed only holds the latest posts: keep older Forever news from the file, newest first, 30 at most."""
    seen = {x['url'] for x in new}
    return sorted(new + [x for x in old if x['url'] not in seen and x['url'].startswith(WOWHEAD)], key=lambda x: x['date'], reverse=True)[:30]


def main():
    try:
        req = urllib.request.Request(FEED, headers={'User-Agent': 'gabella-wow-guide'})
        items = parse(urllib.request.urlopen(req, timeout=30).read().decode('utf-8'))
    except Exception as e:
        print(f'skip: {e}', file=sys.stderr)
        return
    old = json.load(open(OUT, encoding='utf-8')) if os.path.exists(OUT) else None
    items = merge(items, old or [])
    if items and items != old:
        with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
            json.dump(items, f, ensure_ascii=False, indent=1)
            f.write('\n')
        print(f'written {len(items)}')
    else:
        print('no change')


if __name__ == '__main__':
    main()
