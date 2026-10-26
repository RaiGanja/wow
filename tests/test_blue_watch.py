"""Детектор синих постов Forever (tools/blue_watch.py). Запуск: python tests/test_blue_watch.py"""
import os, sys
from datetime import datetime, timezone
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'tools'))
import blue_watch as bw

NOW = datetime(2026, 10, 23, 23, 0, tzinfo=timezone.utc)


def post(topic, title, cat, at, n=1, excerpt='Text <b>here</b> &amp; more'):
    return {'topic_id': topic, 'topic_title': title, 'category_id': cat, 'created_at': at, 'post_number': n, 'excerpt': excerpt}


US = [post(1, 'Thank You For Testing the WoW Forever Beta', 347, '2026-10-23T17:01:12.659Z'),
      post(2, 'Class Tuning Incoming - October 27', 171, '2026-10-23T22:52:00.000Z'),            # retail: skipped
      post(3, 'Dive Into WoW: Forever, the Gods of Zul&rsquo;Aman', 171, '2026-10-23T17:06:00.000Z'),  # general section, Forever in title
      post(4, 'Fix Warrior in PVP', 346, '2026-10-23T20:00:00.000Z', n=12),                   # a developer reply in a Forever thread
      post(5, 'Forever Beta Will Return Shortly', 349, '2026-10-21T01:46:00.000Z')]           # older than MAX_AGE_H
EU = [post(91, 'Thank You For Testing the WoW Forever Beta', 360, '2026-10-23T17:01:40.000Z')]   # same story in EU

found = bw.pick(US, 'us', NOW) + bw.pick(EU, 'eu', NOW)
assert {x['key'] for x in found} == {'us-1', 'us-3', 'us-4', 'eu-91'}, found
items = bw.merge(found)
assert [x['key'] for x in items] == ['us-1', 'us-3', 'us-4'], items          # EU copy of the same title dropped
assert items[0]['url'] == 'https://us.forums.blizzard.com/en/wow/t/1/1' and items[0]['excerpt'] == 'Text here & more'
assert items[1]['title'] == 'Dive Into WoW: Forever, the Gods of Zul’Aman' and items[2]['reply']
body = bw.body(items[0])
assert '2026-10-23 17:01 UTC' in body and '2026-10-23 20:01 UTC' in body and "'so': t(ru, en, uk)" in body
assert bw.clean('a ' * 400).endswith('…') and len(bw.clean('a ' * 400)) <= 501
# entries already written by hand are not new tasks
assert 'eu-637228' in bw.known_urls()
print('OK')
