"""Лента обновлений сайта для Discord (updates.json). Запуск: python tests/test_updates.py"""
import json, os, re
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load():
    with open(os.path.join(HERE, 'updates.json'), encoding='utf-8') as f:
        return json.load(f)['updates']


def test_entries_valid():
    ids = set()
    for e in load():
        assert e['id'] not in ids, e['id']
        ids.add(e['id'])
        assert re.fullmatch(r'\d{4}-\d{2}-\d{2}', e['date']), e['id']
        assert e['title'].get('en'), e['id']
        assert set(e['title']) <= {'en', 'uk', 'ru'} and set(e.get('text', {})) <= {'en', 'uk', 'ru'}, e['id']
        urls = [e['url']] if isinstance(e['url'], str) else list(e['url'].values())
        assert all(u.startswith('https://gabella.site/') for u in urls), e['id']


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_'):
            fn()
    print('OK')
