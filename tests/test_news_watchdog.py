"""Logic of tools/news_watchdog.py on substituted data. Run: python tests/test_news_watchdog.py"""
import os, sys
from datetime import datetime, timedelta, timezone
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'tools'))
import news_watchdog as w  # noqa: E402

now = datetime(2026, 10, 31, 12, 0, tzinfo=timezone.utc)
ago = lambda m: now - timedelta(minutes=m)
assert w.decide(now, ago(10), False) == ('none', 10)
assert w.decide(now, ago(25), False) == ('none', 25)          # exactly 25: still fine
assert w.decide(now, ago(26), False) == ('open', 26)
assert w.decide(now, ago(213), False) == ('open', 213)
assert w.decide(now, ago(213), True) == ('none', 213)         # no duplicate
assert w.decide(now, ago(5), True) == ('close', 5)
assert w.decide(now, None, False)[0] == 'open'
assert w.parse('2026-10-31T10:00:00Z') == datetime(2026, 10, 31, 10, 0, tzinfo=timezone.utc)
print('ok news_watchdog')
