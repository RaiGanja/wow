"""Поисковая обвязка собранных страниц: заголовки под запросы и их длина, метки подтверждения кабинетов,
IndexNow (ключ, отбор изменённых страниц). Запуск после python build.py: python tests/test_seo.py"""
import html as H, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.argv = sys.argv[:1] + ['--list']          # seo/build: collect texts, write nothing
import seo  # noqa: E402
from langs import LANGS  # noqa: E402
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import indexnow  # noqa: E402


def built(path, lang):
    d = seo.page_dir(lang, path)
    return open(os.path.join(ROOT, d, 'index.html'), encoding='utf-8').read()


def test_titles_fit_the_results_page():
    for path, by_lang in seo.page_meta().items():
        if path in seo.NOINDEX:
            continue
        for lang, (title, desc) in by_lang.items():
            assert len(title) <= 60, (path, lang, len(title), title)
            assert 'WoW Forever' in title, (path, lang, title)
            assert len(desc) <= 160, (path, lang, len(desc), desc)


def test_titles_follow_real_queries():
    m = seo.page_meta()
    assert m['classes/hunter/']['en'][0].startswith('WoW Forever Hunter Guide'), m['classes/hunter/']['en']
    assert 'Racials' in m['races/human/']['en'][0]
    assert 'Instanzen' in m['guides/dungeons/']['de'][0]
    assert 'mensalidade' in m['guides/faq/']['pt'][0]
    assert 'cuándo sale' in m['guides/faq/']['es'][0]


def test_built_title_matches_meta():
    m = seo.page_meta()
    for path in ('', 'classes/mage/', 'guides/faq/'):
        for lang in LANGS:
            assert f'<title>{H.escape(m[path][lang][0], quote=True)}</title>' in built(path, lang), (path, lang)


def test_structured_data():
    import json
    def blocks(path, lang):
        return [json.loads(b.replace('<\\/', '</')) for b in
                re.findall(r'<script type="application/ld\+json">(.*?)</script>', built(path, lang), re.S)]
    home = {b['@type'] for b in blocks('', 'en')}
    assert {'WebSite', 'Organization'} <= home, home
    art = next(b for b in blocks('guides/leveling/', 'de') if b['@type'] == 'Article')
    assert re.fullmatch(r'\d{4}-\d\d-\d\d', art['dateModified']) and art['inLanguage'] == 'de'
    assert art['image'].startswith('https://gabella.site/wow/assets/og/')
    assert not any(b['@type'] == 'Article' for b in blocks('guides/news/', 'en'))      # the feed has no fixed date
    assert any(b['@type'] == 'FAQPage' for b in blocks('guides/faq/', 'en'))


def test_verify_meta_only_when_set():
    html = built('', 'en')
    for name, value in seo.VERIFY.items():
        assert (f'<meta name="{name}"' in html) == bool(value), name
    saved = dict(seo.VERIFY)
    try:
        seo.VERIFY['msvalidate.01'] = 'abc"1'
        m = seo.page_meta()['']['en']
        out = seo.apply(seo.apply(html, '', 'en', *m), '', 'en', *m)          # rebuild over a built page: one tag, not two
        assert out.count('<meta name="msvalidate.01" content="abc&quot;1">') == 1
    finally:
        seo.VERIFY.clear(); seo.VERIFY.update(saved)


def test_indexnow_key_and_filter():
    assert re.fullmatch(r'[0-9a-f]{32}', indexnow.KEY)
    assert indexnow.norm('<script src="a.js?v=1a2b"></script>') == indexnow.norm('<script src="a.js?v=ffee"></script>')
    os.chdir(ROOT)
    urls = indexnow.sitemap_urls()
    assert 'https://gabella.site/wow/' in urls and 'https://gabella.site/wow/en/classes/mage/' in urls
    assert not any('/profile/' in u or '/u/' in u for u in urls)


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_'):
            fn()
    print('OK')
