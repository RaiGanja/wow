"""Каналы аудитории: Telegram в подвале и sameAs, блок «Новости» и карточка в профиле на 9 языках, /privacy/.
Запуск: python tests/test_news.py (после python build.py)"""
import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from langs import LANGS

TG = 'https://t.me/gabella_wow'


def page(rel):
    return open(os.path.join(ROOT, rel, 'index.html'), encoding='utf-8').read()


def pre(lang, sub=''):
    return ('' if lang == 'ru' else lang + '/') + sub


def test_telegram_constant():
    import build
    assert build.TELEGRAM == TG


def test_footer_and_same_as():
    for lang in LANGS:
        html = page(pre(lang))
        assert f'<a href="{TG}" target="_blank" rel="noopener">Telegram</a>' in html, lang
        ld = ''.join(re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S))
        assert TG in ld, lang


def test_profile_gets_the_channel():
    for lang in LANGS:
        html = page(pre(lang, 'profile/'))
        gd = json.loads(re.search(r'const GD = (\{.*?\});\n', html).group(1))
        assert gd['tg'] == TG and gd['invite'].startswith('https://discord.gg/'), lang


def test_profile_news_block():
    for lang in LANGS:
        html = page(pre(lang, 'profile/'))
        for key in ('function newsBox()', 'id="newsF"', 'data-act="newsMail"', 'data-act="newsOff"', "'/news/email'", '${newsBox()}${waysBox()}'):
            assert key in html, (lang, key)


def test_profile_news_card_and_confirm():
    for lang in LANGS:
        html = page(pre(lang, 'profile/'))
        for key in ('function newsAsk()', 'data-act="newsGo"', 'data-act="newsNo"', "'/news/confirm'", "h.startsWith('news=')",
                    "'news-on'", '${levelAsk()}${newsAsk()}${nextHtml()}', "NEWS_LS = 'gabella-news-asked'"):
            assert key in html, (lang, key)


def test_privacy_mentions_letters():
    assert 'храним адрес (зашифрованным)' in page('privacy/')
    assert 'we keep the address (encrypted)' in page('en/privacy/')
    assert 'speichern wir die Adresse (verschlüsselt)' in page('de/privacy/')


def test_privacy_turnstile_mentions_subscribing():
    assert 'подписке на письма сайт загружает проверку' in page('privacy/')
    assert 'subscribe to emails, the site loads' in page('en/privacy/')


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_'):
            fn()
    print('OK')
