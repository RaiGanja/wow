"""Watcher of official news (tools/news_watch.py, news_parse.py, news_check.py). Run: python tests/test_news_auto.py
Data: tests/fixtures/news (lists of changes of real Blizzard posts of 16.10 and 26.10); the full topics, if present,
in projects/gabella/docs/wow/news-auto/samples (outside the repo) are parsed too."""
import json, os, sys, tempfile
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import news_parse as np      # noqa: E402
import news_check as nc      # noqa: E402
import news_watch as nw      # noqa: E402

FX = os.path.join(HERE, 'fixtures', 'news')
P7 = open(os.path.join(FX, 'us-2360696-7.html'), encoding='utf-8').read()
P6 = open(os.path.join(FX, 'us-2360696-6-part.html'), encoding='utf-8').read()


def by_name(items, name, kind=None):
    return [c for c in items if c['abilities'] and c['abilities'][0] == name and (kind is None or c['kind'] == kind)]


# ---------- parse: Racial Ability Tuning Pass, 26.10 ----------
it = np.changes(P7)
assert len(it) == 14, [c['text'][:40] for c in it]
r = by_name(it, 'Ruthless')[0]
assert r['subject'] == {'type': 'race', 'id': 'human'} and r['kind'] == 'changed'
assert r['pairs'] == [{'new': 1, 'old': 2, 'unit': '%', 'old_unit': '%'}], r['pairs']
assert by_name(it, 'Human Spirit')[0]['pairs'][0]['new'] == 10
pr = by_name(it, 'Plainsrunning', 'changed')[0]
assert [(p['old'], p['new']) for p in pr['pairs']] == [(1, 2), (30, 60)] and pr['subject']['id'] == 'tauren'
assert by_name(it, 'Plainsrunning', 'no_longer') and by_name(it, 'Endurance', 'no_longer')
assert by_name(it, 'Earth Fury', 'removed')[0]['subject']['id'] == 'dwarf'
assert by_name(it, 'Savage', 'removed') and by_name(it, 'Command', 'added')
assert np.norm(by_name(it, 'Artisan’s Precision', 'added')[0]['abilities'][0]) == "artisan's precision"
assert by_name(it, 'Wind-Blessed Haste')[0]['pairs'][0] == {'new': 2, 'old': 3, 'unit': '%', 'old_unit': '%'}
assert by_name(it, 'Read Leyline')[0]['pairs'][0]['old'] == 100
assert {c['subject']['id'] for c in it} == {'human', 'dwarf', 'tauren', 'orc', 'skyborne'}
assert len({c['h'] for c in it}) == 14                      # every line has its own hash

# ---------- parse: units, specs, notes (16.10) ----------
it6 = np.changes(P6)
assert by_name(it6, 'War Stomp')[0]['pairs'] == [{'new': 90, 'old': 2, 'unit': 's', 'old_unit': 'min'}]
assert by_name(it6, 'Cultivation')[0]['pairs'][0] == {'new': 15, 'old': 60, 'unit': 'min', 'old_unit': 'min'}
assert by_name(it6, 'Leader of the Pack')[0]['subject'] == {'type': 'class', 'id': 'druid', 'spec': 'feral'}
assert all(c['kind'] == 'note' for c in it6 if c['text'].startswith('Developers’ notes'))
assert np.pairs('Cooldown reduced from 2 minutes to 90 seconds.') == [{'new': 90, 'old': 2, 'unit': 's', 'old_unit': 'min'}]
assert np.pairs('Now has 1 Trap (was 1 Trap among all).') == []      # same number is not a change

# ---------- hash: markup-only edits are the same version, a changed number is a new one ----------
assert np.digest(P7) == np.digest(P7.replace('class="anchor"', 'class="anchor x"'))
assert np.digest(P7) != np.digest(P7.replace('by 1% (was 2%)', 'by 1.5% (was 2%)'))

# ---------- check against the site (a small fixed site, not the build) ----------
site = {'races/human/': ['Ruthless +2% crit chance', 'The Human Spirit +5% spirit'],
        'races/tauren/': ['Endurance +5% health and +2% crit damage'],
        'guides/builds-rogue/': ['Endurance: Sprint and Evasion cooldown −15%'],          # the rogue talent, not the racial
        'races/orc/': ['Savage: +1% crit chance'],
        'guides/best-race/': ['Human: Ruthless gives +1% crit with any weapon, Night Elf: Elune’s Light +10% crit.'],
        'guides/builds-druid/': ['Savage Fury 2/2'],                                        # not the orc racial Savage
        'guides/news/': ['Ruthless +2% crit (15.10)']}                                      # history page: skipped
rep = nc.check(it, site)
st = {(x['ability'], f['page']): f['status'] for x in rep for f in x['findings']}
assert st[('Ruthless', 'races/human/')] == 'outdated' and st[('Ruthless', 'guides/best-race/')] == 'ok', st
assert st[('Human Spirit', 'races/human/')] == 'outdated'
assert st[('Savage', 'races/orc/')] == 'outdated' and ('Savage', 'guides/builds-druid/') not in st
assert st[('Endurance', 'races/tauren/')] == 'check' and ('Endurance', 'guides/builds-rogue/') not in st
assert not any(p == 'guides/news/' for _, p in st)
assert st[('Artisan’s Precision', None)] == 'missing'
out, chk = nc.outdated_pages(rep)
assert set(out) == {'races/human/', 'races/orc/'} and 'races/tauren/' in chk
md = nc.render(rep)
assert 'https://gabella.site/wow/en/races/human/' in md and 'Artisan’s Precision' in md

# ---------- number gate for automatic edits (stage 4) ----------
orig = np.plain(P7)
ruth = by_name(it, 'Ruthless')[0]['pairs']
assert nc.verify_edit(orig, 'Ruthless: +2% crit chance', 'Ruthless: +1% crit chance', ruth)['ok']
assert nc.verify_edit(orig, 'Безжалостность: +2 % крит', 'Безжалостность: +1 % крит', ruth)['ok']          # any language
bad = nc.verify_edit(orig, 'Ruthless: +2% crit chance', 'Ruthless: +1% crit chance, +7% haste', ruth)
assert not bad['ok'] and bad['extra'] == [7]                                                          # a number not in the post
miss = nc.verify_edit(orig, 'Ruthless: +2% crit chance', 'Ruthless: more crit', ruth)
assert not miss['ok'] and miss['missing'] == [1]                                                      # the new value is lost

# ---------- watcher: baseline, new, edit, twins, no text in the stored entries ----------
NOW = datetime.now(timezone.utc)
CFG = {'forums': {'us': {'base': 'https://us.example/en/wow', 'categories': ['wow-forever/346']},
                  'eu': {'base': 'https://eu.example/en/wow', 'categories': ['wow-forever/359']}},
       'watch_topics': {'us': [10], 'eu': []}, 'beta_categories': {'us': [349], 'eu': [362]}, 'tracker': {'enabled': False}}


def topic(tid, cooked, created, cat=349, title='WoW Forever Beta Development Notes - Updated October 26', updated=None):
    return {'id': tid, 'slug': 'dev-notes', 'title': title, 'category_id': cat,
            'post_stream': {'stream': [tid * 10 + 1], 'posts': [{'id': tid * 10 + 1, 'post_number': 1, 'staff': True, 'cooked': cooked,
                                                                 'username': 'Kaivax', 'user_title': 'Community Manager', 'created_at': created,
                                                                 'updated_at': updated or created, 'version': 1}]}}


class Fake:
    def __init__(self, pages):
        self.pages, self.count, self.urls = pages, 0, []

    def get(self, name, url, as_json=True):
        self.count += 1
        self.urls.append(url)
        return self.pages.get(url)


def site_pages(cooked, created, eu=True, updated=None):
    at = created
    p = {'https://us.example/en/wow/c/wow-forever/346.json': {'topic_list': {'topics': [
            {'id': 10, 'last_posted_at': updated or at, 'highest_post_number': 1, 'posters': [{'primary_group_id': 62}]},
            {'id': 11, 'last_posted_at': at, 'highest_post_number': 4, 'posters': [{'primary_group_id': None}]}]}},
         'https://us.example/en/wow/t/10.json': topic(10, cooked, created, updated=updated),
         'https://eu.example/en/wow/c/wow-forever/359.json': {'topic_list': {'topics': [
            {'id': 20, 'last_posted_at': at, 'highest_post_number': 1, 'posters': [{'primary_group_id': 7}]}]}}}
    if eu:
        p['https://eu.example/en/wow/t/20.json'] = topic(20, cooked, created, cat=362, title='WoW Forever Beta Development Notes - Updated 26 October')
    return p


created = (NOW - timedelta(hours=2)).strftime('%Y-%m-%dT%H:%M:%S.000Z')
ledger = {}
ev = nw.run(json.loads(json.dumps(CFG)), ledger, None, Fake(site_pages(P7, created)))
assert [e['event'] for e in ev] == ['baseline', 'baseline']                       # first run: only marks as seen
fake = Fake(site_pages(P7, created))
assert nw.run(json.loads(json.dumps(CFG)), ledger, None, fake) == []              # nothing new
assert 'https://us.example/en/wow/t/11.json' not in fake.urls                      # a players' topic is not read
ledger = {}
ev = nw.run(json.loads(json.dumps(CFG)), ledger, 48, Fake(site_pages(P7, created)))
assert [e['event'] for e in ev] == ['new', 'new'] and ev[1]['twin_of'] == 'us-10-1' and ev[0]['also'], ev   # EU copy = one story
assert ev[0]['rec']['beta'] and nw.short_news(ev[0]['rec'])['kind'] == 'dev-notes'
assert len(ev[0]['res']['outdated']) >= 0 and len(ev[0]['res']['changes']) == 14
edited = P7.replace('by 1% (was 2%)', 'by 1.5% (was 2%)')
upd = (NOW - timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%S.000Z')
ev = nw.run(json.loads(json.dumps(CFG)), ledger, 48, Fake(site_pages(edited, created, eu=False, updated=upd)))
assert [e['event'] for e in ev] == ['edit'] and len(ev[0]['res']['new_lines']) == 1 and len(ev[0]['res']['gone_lines']) == 1, ev
assert ev[0]['res']['check'][0]['ability'] == 'Ruthless'                         # only the changed line is checked again
with tempfile.TemporaryDirectory() as d:
    files = nw.save(d, ledger, ev, test=True)
    text = open(files[0], encoding='utf-8').read() + open(os.path.join(d, 'ledger.json'), encoding='utf-8').read()
    assert 'Ruthless now increases' not in text and 'critical chance by' not in text     # sentences of the post are not stored
    log = [json.loads(x) for x in open(os.path.join(d, 'log.jsonl'), encoding='utf-8')]
    assert log[0]['event'] == 'edit' and log[0]['test'] is True
    body = nw.issue_body(ev[0])
    assert 'правка поста' in body and 'https://us.example/en/wow/t/dev-notes/10/1' in body

# a network failure is counted, not fatal
led = {}
f = nw.Fetcher(led, pause=0)
assert f.get('x', 'http://127.0.0.1:9/none.json') is None and led['sources']['x']['fails'] == 1

# articles list of worldofwarcraft.blizzard.com
art = ('<article class="NewsBlog"><div class="NewsBlog-date LocalizedDateMount" data-props="{&quot;iso8601&quot;:&quot;2026-10-26T17:00:00.000Z&quot;}">'
       '</div><div class="NewsBlog-title">Watch the WoW: Forever Short Story</div><a class="Link NewsBlog-link" href="/news/24313105/watch-the-wow-forever"></a></article>'
       '<article class="NewsBlog"><div class="NewsBlog-title">Hotfixes: October 26, 2026</div><a href="/news/24307310/hotfixes-october-26-2026"></a></article>')
lst = nw.article_list(art, 'https://worldofwarcraft.blizzard.com', 'forever')
assert lst == [{'id': '24313105', 'title': 'Watch the WoW: Forever Short Story', 'created_at': '2026-10-26T17:00:00.000Z',
                'url': 'https://worldofwarcraft.blizzard.com/en-us/news/24313105/watch-the-wow-forever'}], lst

# the tracker hint is off: no request to /groups/ (robots.txt of the forums disallows /en/wow/g)
fake = Fake({})
nw.run(json.loads(json.dumps(CFG)), {}, None, fake)
assert not any('/groups/' in u for u in fake.urls)
src = json.load(open(os.path.join(ROOT, 'tools', 'news_sources.json'), encoding='utf-8'))
assert src['tracker']['enabled'] is False

# ---------- full real topics, if the samples are on this computer ----------
for base in (os.path.join(ROOT, '..', '..', '..', '..', 'docs', 'wow', 'news-auto', 'samples'),
             os.path.join(ROOT, '..', 'docs', 'wow', 'news-auto', 'samples')):
    s = os.path.join(base, 'us-2360696-topic-2026-10-27.json')
    if os.path.exists(s):
        c7, _ = np.load(s, 7)
        assert len(np.changes(c7)) == 14
        c6, _ = np.load(s, 6)
        big = np.changes(c6)
        assert len(big) > 120 and by_name(big, 'Blood Fury')[0]['pairs'][0] == {'new': 3, 'old': 2, 'unit': 'min', 'old_unit': 'min'}
        print('samples: parsed', len(big) + 14, 'changes of 2 real posts')
        break
print('OK')
