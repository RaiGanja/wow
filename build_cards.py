"""Share pages of built characters: b/<race>-<class>-<spec>/ in every language (168 x 9 = 1512 light pages).
A chat shows the link as a card: the picture is assets/og/b/<slug>.jpg (tools/make_build_cards.py, one card per build and language),
the words are the page's og:title / og:description in the reader's language. A visitor is sent on to tools/#pick=<race>.<class>.<spec>.
The pages are noindex (1512 thin pages stay out of the search index and out of sitemap.xml). Run after build_guides, before seo/og_version."""
import functools, json, os, sys
from html import escape

import build
from build import LANGS, SITE, page_dir
import langs
from content.spec_cheats import HAS_CHEAT

HERE = build.HERE
sys.path.insert(0, os.path.join(HERE, 'tools'))
import make_build_cards as MC  # noqa: E402

MC.names = functools.cache(MC.names)   # the language data is read once per language, not once per page

LOCALE = {'ru': 'ru_RU', 'uk': 'uk_UA', 'en': 'en_US', 'de': 'de_DE', 'fr': 'fr_FR', 'es': 'es_ES', 'it': 'it_IT', 'pt': 'pt_BR', 'pl': 'pl_PL'}
OPEN = {'ru': 'Открыть в подборщике', 'uk': 'Відкрити в підбірнику', 'en': 'Open in the picker', 'de': 'Im Auswahltool öffnen',
        'fr': 'Ouvrir dans le sélecteur', 'es': 'Abrir en el selector', 'it': 'Apri nel selettore', 'pt': 'Abrir no seletor', 'pl': 'Otwórz w selektorze'}
OPEN_SHEET = {'ru': 'Открыть шпору спека', 'uk': 'Відкрити шпору спека', 'en': 'Open the spec cheat sheet', 'de': 'Spickzettel der Skillung öffnen',
              'fr': 'Ouvrir la fiche de la spécialisation', 'es': 'Abrir la guía rápida de la espec.', 'it': 'Apri la scheda della specializzazione',
              'pt': 'Abrir o resumo da especialização', 'pl': 'Otwórz ściągę specjalizacji'}
IMG_ALT = {'ru': 'Карточка: {t}', 'uk': 'Картка: {t}', 'en': 'Card: {t}', 'de': 'Karte: {t}', 'fr': 'Carte : {t}', 'es': 'Tarjeta: {t}',
           'it': 'Scheda: {t}', 'pt': 'Cartão: {t}', 'pl': 'Karta: {t}'}

PAGE = '''<!doctype html>
<html lang="@@HL@@">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex,follow">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>@@TITLE@@ · Gabella</title>
<meta name="description" content="@@DESC@@">
<meta name="theme-color" content="#050505">
@@ALT@@
<link rel="canonical" href="@@URL@@">
<link rel="icon" type="image/png" sizes="48x48" href="@@ROOT@@assets/icons/favicon-48.png">
<link rel="manifest" href="@@ROOT@@manifest-@@LANG@@.webmanifest">
<meta property="og:type" content="website">
<meta property="og:locale" content="@@LOCALE@@">
<meta property="og:site_name" content="Gabella">
<meta property="og:title" content="@@TITLE@@">
<meta property="og:description" content="@@DESC@@">
<meta property="og:url" content="@@URL@@">
<meta property="og:image" content="@@IMG@@">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="@@ALTT@@">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="@@TITLE@@">
<meta name="twitter:description" content="@@DESC@@">
<meta name="twitter:image" content="@@IMG@@">
<script type="application/ld+json">@@LD@@</script>
<style>
:root { color-scheme: dark light; --bg: #050505; --fg: #ece6d8; --muted: #a8a294; --gold: #c9a54a; --line: #2a2820; }
@media (prefers-color-scheme: light) { :root { --bg: #f6f1e6; --fg: #1d1a14; --muted: #5f594b; --gold: #7a5a14; --line: #d8cfba; } }
* { box-sizing: border-box; }
body { margin: 0; min-height: 100vh; display: grid; place-items: center; padding: 24px 16px; background: var(--bg); color: var(--fg); font: 1rem/1.5 Georgia, "Times New Roman", serif; }
main { width: 100%; max-width: 520px; }
.brand { display: flex; align-items: center; gap: 10px; margin: 0 0 20px; font-size: .85rem; letter-spacing: .14em; text-transform: uppercase; color: var(--gold); }
.brand img { width: 32px; height: 32px; }
section { padding: 14px 0; border-top: 1px solid var(--line); }
h1 { margin: 0 0 4px; font-size: 1.5rem; font-weight: 600; line-height: 1.2; }
p { margin: 0 0 6px; }
.m { color: var(--muted); }
a { color: var(--gold); text-underline-offset: 3px; }
</style>
</head>
<body>
<main>
<p class="brand"><img src="@@ROOT@@assets/brand/mark.webp" width="32" height="32" alt="">Gabella · WoW Forever</p>
<section>
<h1>@@NAME@@</h1>
<p>@@SPEC@@</p>
<p class="m">@@ROLE@@ · @@FAC@@</p>
<p><a id="go" href="@@PICK@@">@@OPEN@@</a></p>
</section>
</main>
<script>location.replace(document.getElementById('go').href);</script>
<script>if ('serviceWorker' in navigator) addEventListener('load', () => navigator.serviceWorker.register('@@ROOT@@sw.js').catch(() => {}));</script>
</body>
</html>
'''


def render(race, cls, spec, lang):
    sub = f'b/{MC.slug(race, cls, spec)}/'
    here = page_dir(lang, sub)
    root = build.rel(here, '')
    n = MC.names(lang)
    i = n['sid'][cls].index(spec)
    name, spec_n, fac = MC.title(lang, race, cls, n), n['sn'][cls][i], n['fn'][MC.GAME['races'][race]['f']]
    title, desc = MC.og_text(race, cls, spec, lang)
    url = SITE + here
    alt = build.alternates(sub)
    ld = json.dumps({'@context': 'https://schema.org', '@type': 'WebPage', 'name': title, 'url': url, 'inLanguage': langs.HREFLANG[lang],
                     'isPartOf': {'@type': 'WebSite', 'name': 'Gabella', 'url': SITE}}, ensure_ascii=False)
    rep = {'HL': langs.HREFLANG[lang], 'LANG': lang, 'TITLE': escape(title), 'DESC': escape(desc), 'ALT': alt, 'URL': url, 'ROOT': root,
           'LOCALE': LOCALE[lang], 'IMG': f'{SITE}assets/og/b/{MC.slug(race, cls, spec)}-{lang}.jpg', 'ALTT': escape(IMG_ALT[lang].format(t=title)),
           'LD': ld.replace('</', '<\\/'), 'NAME': escape(name), 'SPEC': escape(spec_n), 'FAC': escape(fac), 'ROLE': escape(MC.role_line(cls, spec, lang)), 'OPEN': OPEN[lang],
           'PICK': f'{build.rel(here, page_dir(lang))}tools/#pick={race}.{cls}.{spec}'}
    if f'{cls}-{spec}' in HAS_CHEAT:   # the four specs with a cheat sheet: the card leads there, the picker is one button away
        rep['PICK'] = f'{build.rel(here, page_dir(lang))}guides/spec-{cls}-{spec}/#race={race}'
        rep['OPEN'] = OPEN_SHEET[lang]
    html = PAGE
    for k, v in rep.items():
        html = html.replace(f'@@{k}@@', v)
    assert '@@' not in html, (sub, lang)
    return here + 'index.html', html


def main():
    if '--list' in sys.argv:
        return
    todo = list(MC.combos())
    for lang in LANGS:
        for race, cls, spec in todo:
            assert os.path.isfile(os.path.join(HERE, 'assets', 'og', 'b', f'{MC.slug(race, cls, spec)}-{lang}.jpg')), (race, cls, spec, lang, f'no card: python tools/make_build_cards.py --variant=A --langs={lang}')
    n = 0
    for lang in LANGS:
        for race, cls, spec in todo:
            path, html = render(race, cls, spec, lang)
            full = os.path.join(HERE, path)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            with open(full, 'w', encoding='utf-8', newline='\n') as f:
                f.write(html)
            n += 1
    print(f'build cards: {n} pages', file=sys.stderr)
