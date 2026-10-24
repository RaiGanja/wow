"""Запуск: python tests/test_fetch_news.py"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'tools'))
import fetch_news as fn

XML = '''<?xml version="1.0"?><rss><channel>
<item><title>WoW Forever beta patch notes</title><link>https://www.wowhead.com/news/1</link>
<pubDate>Thu, 23 Oct 2026 10:00:00 GMT</pubDate><category>Forever</category></item>
<item><title>Retail hotfixes</title><link>https://www.wowhead.com/news/2</link>
<pubDate>Wed, 22 Oct 2026 10:00:00 GMT</pubDate><category>Retail</category></item>
<item><title>Class tuning</title><link>https://www.wowhead.com/news/3</link><description>Changes coming to WoW Forever next week</description>
<pubDate>Wed, 22 Oct 2026 09:00:00 GMT</pubDate></item>
<item><title>WoW Forever trap</title><link>javascript:alert(1)</link>
<pubDate>Wed, 22 Oct 2026 08:00:00 GMT</pubDate></item>
<item><title>WoW Forever elsewhere</title><link>https://evil.example/forever</link>
<pubDate>Wed, 22 Oct 2026 07:00:00 GMT</pubDate></item>
</channel></rss>'''

items = fn.parse(XML)
assert items == [{'date': '2026-10-23', 'title': 'WoW Forever beta patch notes', 'url': 'https://www.wowhead.com/news/1'},
                 {'date': '2026-10-22', 'title': 'Class tuning', 'url': 'https://www.wowhead.com/news/3'}], items
# only Wowhead links survive, also among the old ones already in the file
old = [{'date': '2026-10-01', 'title': 'Old', 'url': 'https://www.wowhead.com/news/0'}, {'date': '2026-10-02', 'title': 'Bad', 'url': 'javascript:alert(1)'}, items[0]]
merged = fn.merge(items, old)
assert [x['url'] for x in merged] == ['https://www.wowhead.com/news/1', 'https://www.wowhead.com/news/3', 'https://www.wowhead.com/news/0'], merged
assert len(fn.merge(items * 0 + [{'date': f'2026-09-{d:02d}', 'title': 't', 'url': str(d)} for d in range(1, 31)], items)) == 30
print('OK')
