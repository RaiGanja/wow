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
P7 = open(os.path.join(FX, 'us-2360696-7.cooked'), encoding='utf-8').read()
P6 = open(os.path.join(FX, 'us-2360696-6-part.cooked'), encoding='utf-8').read()


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
INTRO = '<p>As we approach the launch, we have been reflecting on feedback about racial traits.</p>'
edited = INTRO + P7.replace('by 1% (was 2%)', 'by 1.5% (was 2%)')
upd = (NOW - timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%S.000Z')
ev = nw.run(json.loads(json.dumps(CFG)), ledger, 48, Fake(site_pages(edited, created, eu=False, updated=upd)))
assert [e['event'] for e in ev] == ['edit'] and len(ev[0]['res']['new_lines']) == 1 and len(ev[0]['res']['gone_lines']) == 1, ev
assert ev[0]['res']['check'][0]['ability'] == 'Ruthless'                         # only the changed line is checked again
with tempfile.TemporaryDirectory() as d:
    files = nw.save(d, ledger, ev, test=True)
    entry_text = open(files[0], encoding='utf-8').read()
    ledger_text = open(os.path.join(d, 'ledger.json'), encoding='utf-8').read()
    assert 'reflecting on feedback' not in entry_text + ledger_text          # the prose of the post is never kept
    assert 'Ruthless now increases' not in ledger_text                       # the ledger keeps hashes only
    assert 'Ruthless now increases critical chance by 1.5% (was 2%).' in entry_text   # the change line travels with the event
    log = [json.loads(x) for x in open(os.path.join(d, 'log.jsonl'), encoding='utf-8')]
    assert log[0]['event'] == 'edit' and log[0]['test'] is True
    body = nw.issue_body(ev[0])
    assert 'правка поста' in body and 'https://us.example/en/wow/t/dev-notes/10/1' in body
    facts = nw.facts_from_issue(body)            # the editor reads the facts from the issue, not from the forum
    assert facts['key'] == 'us-10-1' and len(facts['facts']) == 1 and facts['facts'][0]['pairs'][0] == {'new': 1.5, 'old': 2, 'unit': '%', 'old_unit': '%'}
    assert facts['facts'][0]['nums'] == [1.5, 2] and facts['entry'].startswith('news-data:entries/')
    assert 'reflecting on feedback' not in body
    entries_saved = [json.load(open(p, encoding='utf-8')) for p in files]

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

# ---------- level 1: the short note in 9 languages (tools/news_publish.py) ----------
import news_publish as pb      # noqa: E402
import news_gate as ng         # noqa: E402
import news_notify as nn       # noqa: E402
ev = nw.run(json.loads(json.dumps(CFG)), {}, 48, Fake(site_pages(P7, '2026-10-26T20:35:27.223Z')))
ents = [nw.entry(e) for e in ev]
led = {}
notes, changed = pb.apply(ents, [], led)
assert len(notes) == 1 and changed[0][0] == 'us-10-1', changed                      # the EU copy is not a second note
t = notes[0]['t']
assert set(t) == set(pb.LANGS)
assert t['ru']['h'] == 'Заметки разработчиков от 26.10 (бета)' and t['en']['h'] == 'Developer notes of Oct 26 (beta)'
assert t['de']['h'] == 'Entwicklerhinweise vom 26.10 (Beta)' and t['pl']['h'] == 'Notatki deweloperów z 26.10 (beta)'
assert notes[0]['url'].startswith('https://us.example/') and notes[0]['title_en'].startswith('WoW Forever Beta Development Notes')
assert pb.apply(ents, notes, led)[1] == []                                          # the same post again: nothing
assert pb.apply(ents, [], led)[1] == []                                             # reverted note: does not come back
e2 = dict(ents[0], event='edit', sha='f' * 64, detected_at='2026-10-26T21:10:00Z')
n2, ch2 = pb.apply([e2], notes, led)
assert ch2 and n2[0]['t']['ru']['upd'] == 'обновлено 26.10' and n2[0]['t']['en']['upd'] == 'updated Oct 26'
tech = dict(ents[0], key='us-11-1', title='Beta Realm Restart Today At 2:00 p.m. PDT')
assert not pb.publishable(tech)                                                     # technical posts are not news
reply = dict(ents[0], key='us-12-5', post=5, short_news=dict(ents[0]['short_news'], kind='post'))
assert not pb.publishable(reply)                                                    # a reply inside a topic: issue only
assert pb.texts('hotfixes', False, '2026-11-06T18:00:00Z')['fr']['h'] == 'Correctifs du 06.11'
art = pb.texts('article', False, '2026-10-26T17:00:00Z', title='Watch the WoW: Forever Short Story')
assert art['ru'] == {'h': 'Watch the WoW: Forever Short Story', 'en': 1, 'src': 'Blizzard, на английском'}   # an article keeps its English title

# ---------- level 2: number gate on a real git commit (tools/news_gate.py) ----------
import subprocess                                                                   # noqa: E402
fx = {'key': 'us-10-1', 'sha': 'ab' * 32, 'facts': [c for c in ents[0]['changes'] if c['abilities'] and c['abilities'][0] in ('Ruthless', 'Human Spirit')]}
with tempfile.TemporaryDirectory() as d:
    g = lambda *a: subprocess.run(['git', '-C', d, *a], check=True, capture_output=True)   # noqa: E731
    g('init', '-q', '-b', 'main')
    os.makedirs(os.path.join(d, 'content'))
    os.makedirs(os.path.join(d, 'i18n'))
    os.makedirs(os.path.join(d, 'tools'))
    open(os.path.join(d, 'content', 'races.py'), 'w', encoding='utf-8').write("R = t('Ruthless: +2% к шансу крита', 'Ruthless: +2% crit chance', 'Ruthless: +2% криту')\nH = 'The Human Spirit: +5% spirit, since 15.10.2026'\n")
    open(os.path.join(d, 'i18n', 'de.json'), 'w', encoding='utf-8').write('{\n "Ruthless: +2% crit chance": "Ruthless: +2 % Krit"\n}\n')
    g('add', '-A'); g('-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-qm', 'base'); g('branch', 'base')
    ng.ROOT = d

    def commit(races, de, extra=None):
        g('checkout', '-q', '-B', 'work', 'base')
        open(os.path.join(d, 'content', 'races.py'), 'w', encoding='utf-8').write(races)
        open(os.path.join(d, 'i18n', 'de.json'), 'w', encoding='utf-8').write(de)
        if extra:
            open(os.path.join(d, extra), 'w', encoding='utf-8').write('x = 1\n')
        g('add', '-A'); g('-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-qm', 'edit')
        return ng.gate(fx, 'base', 'work')
    good = ("R = t('Ruthless: +1% к шансу крита', 'Ruthless: +1% crit chance', 'Ruthless: +1% криту')\n"
            "H = 'The Human Spirit: +10% spirit, since 26.10.2026'\n")
    res = commit(good, '{\n "Ruthless: +1% crit chance": "Ruthless: +1 % Krit"\n}\n')
    assert res['ok'], res                                                           # numbers of the post, dates do not count
    res = commit(good.replace('+10% spirit', '+12% spirit'), '{\n "Ruthless: +1% crit chance": "Ruthless: +1 % Krit"\n}\n')
    assert not res['ok'] and any('12' in x for x in res['fails']), res              # 12 is not in the post
    res = commit(good, '{\n "Ruthless: +1% crit chance": "Ruthless: mehr Krit"\n}\n')
    assert not res['ok'] and any('old 2 is gone' in x for x in res['fails']), res   # de lost the new value
    res = commit(good, '{\n "Ruthless: +1% crit chance": "Ruthless: +1 % Krit"\n}\n', extra='tools/x.py')
    assert not res['ok'] and any('not a text edit' in x for x in res['fails'])      # code is never auto-merged
    g('checkout', '-q', '-B', 'two', 'base')
    for i in (1, 2):
        open(os.path.join(d, 'content', 'races.py'), 'a', encoding='utf-8').write(f'# {i}\n')
        g('-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-qam', f'c{i}')
    assert any('exactly 1' in x for x in ng.gate(fx, 'base', 'two')['fails'])     # one commit = one revert
    ng.ROOT = ROOT

# ---------- notice: Discord first, Resend second, secrets never printed ----------
sent = []
nn.post = lambda url, body, headers=None: (sent.append((url, body, headers)), 204 if 'discord' in url else 200)[1]
import io, contextlib                                                               # noqa: E402
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    assert nn.notify('t', 'x', env={'SITE_WEBHOOK_NOTES': 'https://discord.example/api/webhooks/SECRET1'}) == 'discord'
    assert nn.notify('t', 'x', env={'RESEND_API_KEY': 'SECRET2', 'NOTIFY_TO': 'a@b.c'}) == 'resend'
    assert nn.notify('t', 'x', env={}) is None
assert 'SECRET' not in buf.getvalue() and sent[0][1]['allowed_mentions'] == {'parse': []}

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
