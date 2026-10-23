"""Радио: stations.json сходится с файлами и сеткой «Эфира». Запуск: python tests/test_radio.py"""
import glob, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RADIO = os.path.join(ROOT, 'assets', 'radio')
data = json.load(open(os.path.join(RADIO, 'stations.json'), encoding='utf-8'))
ids = [s['id'] for s in data['stations']]
files = [t['f'] for s in data['stations'] for t in s['tracks']]

assert len(ids) == len(set(ids)) == 8, ids
assert len(files) == len(set(files)), 'трек на двух станциях'
on_disk = {os.path.basename(f) for f in glob.glob(os.path.join(RADIO, '*.m4a'))}
if not data['media']:   # треки на самом сайте: каждый есть, лишних нет
    assert set(files) == on_disk, (set(files) ^ on_disk)
else:                   # треки в R2 (media.gabella.site): в репо их нет — лимит GitHub Pages 1 ГБ
    assert data['media'].startswith('https://') and data['media'].endswith('/'), data['media']
    assert not on_disk, sorted(on_disk)[:5]
assert data['license'] in data['licenses'] and all(u.startswith('https://creativecommons.org/') for _, u in data['licenses'].values())
assert all(t.get('l', data['license']) in data['licenses'] for s in data['stations'] for t in s['tracks'])
for s in data['stations']:
    assert os.path.exists(os.path.join(ROOT, 'assets', 'art', s['art'] + '.webp')), s['art']
    assert all(s['name'][l] and s['mood'][l] for l in ('ru', 'en', 'uk')), s['id']
    minutes = sum(t['d'] for t in s['tracks']) / 60
    assert len(s['tracks']) >= 10 and minutes >= 35, (s['id'], len(s['tracks']), minutes)
    assert all(t['d'] > 30 for t in s['tracks']), s['id']
    assert all((t.get('a') or s['author']) in data['sources'] for t in s['tracks']), s['id']

# «Эфир»: у каждого часа суток ровно одна часть, у части есть станции, и каждая станция где-то звучит
def part(h):
    return [p['id'] for p in data['air'] if (p['from'] <= h < p['to'] if p['from'] < p['to'] else h >= p['from'] or h < p['to'])]
assert all(len(part(h)) == 1 for h in range(24)), {h: part(h) for h in range(24)}
assert all(p['stations'] and set(p['stations']) <= set(ids) for p in data['air'])
assert set(ids) == {s for p in data['air'] for s in p['stations']}, set(ids) - {s for p in data['air'] for s in p['stations']}
print('OK', len(files), 'tracks,', round(sum(t['d'] for s in data['stations'] for t in s['tracks']) / 3600, 1), 'h')
