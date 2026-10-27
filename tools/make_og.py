"""Share previews 1200x630 with the page title on the art: home (og-<lang>.jpg), guides, the classes/ and races/ sections
and tools (og/<slug>-<lang>.jpg). Rendered from HTML with the site fonts by headless Chrome, so the type matches the site.
Class and race pages keep their language-neutral art previews from make_images.py.
Run: python tools/make_og.py [slug ...] [--langs=de,fr]   (no args = all cards in every built language)"""
import json, os, re, subprocess, sys, tempfile
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path[:0] = [os.path.join(ROOT, 'content'), ROOT]
from guides import HUB, GUIDES, HUBS  # noqa: E402

sys.path.insert(0, ROOT)
import langs  # noqa: E402

CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
LANGS = langs.LANGS
BRAND = 'Gabella'
START = {'ru': 'Старт 5 ноября 2026', 'en': 'Launch November 4–5, 2026', 'uk': 'Старт 5 листопада 2026',
         'de': 'Start am 5. November 2026', 'fr': 'Lancement le 5 novembre 2026', 'es': 'Lanzamiento: 4–5 de noviembre de 2026',
         'pt': 'Lançamento em 4 de novembro de 2026', 'it': 'Uscita il 5 novembre 2026', 'pl': 'Start 5 listopada 2026'}
EXACT = {'launch-day': {'ru': '04.11, 23:00 UTC · Киев 05.11, 01:00', 'en': 'Nov 4, 3:00 PM PST · 23:00 UTC',
                        'uk': 'Старт 04.11, 23:00 UTC · 15:00 PST', 'de': '5. November, 00:00 MEZ',
                        'fr': '5 novembre, minuit à Paris', 'es': '4 nov., 23:00 UTC · Madrid 00:00',
                        'pt': '4 de novembro, 20:00 em Brasília', 'it': '5 novembre, ore 00:00 in Italia',
                        'pl': 'Start 04.11, 23:00 UTC · 15:00 PST'}}   # the launch card names the moment (uk, pl: the lead already gives local time)
HOME = {'t': {l: 'WoW Forever' for l in langs.ALL},
        'd': {'ru': 'Legacy, тир-лист, конструктор группы, новости',
              'en': 'Legacy, tier list, group builder, news',
              'uk': 'Legacy, тір-лист, конструктор групи, новини',
              'de': 'Legacy, Tierliste, Gruppenplaner, News',
              'fr': 'Legacy, tier list, créateur de groupe, actus',
              'es': 'Legacy, tier list, creador de grupos, noticias',
              'pt': 'Legacy, tier list, montador de grupo, notícias',
              'it': 'Legacy, tier list, creatore di gruppi, notizie',
              'pl': 'Legacy, tier lista, kreator grupy, newsy'}}
TOOLS = {'t': langs.derive({'ru': 'Инструменты', 'en': 'Tools', 'uk': 'Інструменти'}),
         'd': {'ru': 'Рамки группы, рейдовая сетка, сравнение классов и рас, поиск по гиду',
               'en': 'Party frames, raid grid, class and race comparison, guide search',
               'uk': 'Рамки групи, рейдова сітка, порівняння класів і рас, пошук по гіду',
               'de': 'Gruppenrahmen, Schlachtzugsraster, Klassen- und Volksvergleich, Suche',
               'fr': 'Cadres de groupe, grille de raid, comparaison des classes et races, recherche',
               'es': 'Marcos de grupo, cuadrícula de banda, comparación de clases y razas, búsqueda',
               'pt': 'Quadros de grupo, grade de raide, comparação de classes e raças, busca',
               'it': 'Riquadri del gruppo, griglia d’incursione, confronto classi e razze, ricerca',
               'pl': 'Ramki grupy, siatka raidu, porównanie klas i ras, wyszukiwarka'}}
langs.fill([HUB, GUIDES, HUBS])
FOCUS = {'hero_dawn': '70%', 'hero_campfire': '88%'}   # horizontal crop of a landscape scene; the default is the right edge
NODATE = {'tier-list'}   # the beta snapshot is refreshed after launch: no launch date under the title
SKIP = set()            # a card that waits for its new scene; named on the command line it is rendered anyway


def cards():
    """(file name without -lang, art, title by lang, line under the title by lang)"""
    yield 'og', 'hero_dawn', HOME['t'], HOME['d']
    yield 'og/guides', HUB['hero'], HUB['title'], HUB['lead']
    for g in GUIDES + HUBS:
        yield 'og/' + g['slug'], g.get('hero') or g['art'], g['title'], g['lead']      # the scene of the page itself
    yield 'og/tools', 'hero_tools', TOOLS['t'], TOOLS['d']


def url(path):
    return 'file:///' + os.path.join(ROOT, path).replace('\\', '/')


def html(art, title, lead, lang, slug=''):
    wide = art.startswith('hero_')
    pic = (f'<img class="wide" src="{url(f"assets/art/{art}-1600.webp" if art == "hero_campfire" else f"assets/art/{art}-1440.webp")}">'
           if wide else
           f'<img class="blur" src="{url(f"assets/art/{art}-bg.webp")}"><img class="por" src="{url(f"assets/art/{art}-896.webp")}">')
    fonts = ''.join(
        f'@font-face{{font-family:"{fam}";font-weight:400 700;src:url({url("assets/fonts/" + f)}) format("woff2");unicode-range:{rng}}}'
        for fam, base in (('Spectral SC', 'spectral-sc'), ('Golos Text', 'golos-text'))
        for f, rng in ((base + '-cyrillic.woff2', 'U+0400-045F,U+0490-0491,U+04B0-04B1,U+2116'), (base + '-latin-ext.woff2', 'U+0100-02BA,U+1E00-1E9F'),
                       (base + '-latin.woff2', 'U+0000-00FF,U+2000-206F')))
    return f'''<!doctype html><meta charset="utf-8"><style>{fonts}
*{{margin:0;box-sizing:border-box}}
body{{width:1200px;height:630px;overflow:hidden;background:#050505;position:relative;font-family:"Golos Text";color:#efe9da;font-variant-numeric:lining-nums}}
img{{position:absolute;display:block}}
.wide{{inset:0;width:100%;height:100%;object-fit:cover;object-position:{FOCUS.get(art, '50%')} 50%}}
.blur{{inset:0;width:100%;height:100%;object-fit:cover;filter:brightness(.8)}}
.por{{right:40px;top:0;height:630px;-webkit-mask-image:linear-gradient(90deg,transparent,#000 22%,#000 78%,transparent)}}
.shade{{position:absolute;inset:0;background:linear-gradient(90deg,#050505 0%,rgba(5,5,5,.92) 34%,rgba(5,5,5,.35) 62%,rgba(5,5,5,0) 80%),
  linear-gradient(0deg,rgba(5,5,5,.85) 0%,rgba(5,5,5,0) 36%)}}
.txt{{position:absolute;left:72px;top:0;bottom:0;width:640px;display:flex;flex-direction:column;justify-content:center;gap:24px}}
.brand{{position:absolute;left:72px;top:56px;display:flex;align-items:center;gap:16px;font:600 30px/1 "Spectral SC";color:#efe9da;letter-spacing:.04em;font-variant-numeric:lining-nums}}
.brand img{{position:static;width:56px;height:56px;border-radius:10px;box-shadow:0 0 0 1px rgba(201,165,74,.45)}}
h1{{font:600 {'92' if len(title) <= 14 else '74'}px/1.02 "Spectral SC";letter-spacing:.02em;text-wrap:balance;font-variant-numeric:lining-nums}}
p{{font-size:30px;line-height:1.35;color:#c9c2b0;text-wrap:pretty;max-width:{"520" if wide else "600"}px}}
.start{{position:absolute;left:72px;bottom:56px;font:600 28px/1 "Spectral SC";letter-spacing:.03em;color:#c9a54a;font-variant-numeric:lining-nums}}
</style><body>{pic}<div class="shade"></div>
<div class="brand"><img src="{url('assets/logo.png')}" alt="">{BRAND}</div>
<div class="txt"><h1>{title}</h1><p>{lead}</p></div>
<div class="start">{'' if slug in NODATE else EXACT.get(slug, START)[lang]}</div>
<div id="res" hidden></div>
<script>/* lay the text block out between the logo and the launch line: width first (Spectral is wide), then height */
document.fonts.ready.then(()=>{{   /* measure in Spectral, not in the fallback that is there before the font arrives */
const R=e=>e.getBoundingClientRect(),$=s=>document.querySelector(s),h=$('h1'),p=$('p'),br=$('.brand'),st=$('.start');
const px=()=>parseFloat(getComputedStyle(h).fontSize),LH=40.5,GAP=24;
const fits=()=>R(h).top>=R(br).bottom+GAP&&R(p).bottom<=R(st).top-GAP;
while(h.scrollWidth>h.clientWidth&&px()>40)h.style.fontSize=(px()-2)+'px';
while(!fits()&&px()>48)h.style.fontSize=(px()-2)+'px';
if(!fits()){{const sen=p.textContent.split(/(?<=[.!?])\\s+/);while(!fits()&&sen.length>1){{sen.pop();p.textContent=sen.join(' ')}}
 const w=p.textContent.split(' ');while(!fits()&&w.length>3){{w.pop();p.textContent=w.join(' ').replace(/[,;:\u2013-]$/,'')+'\u2026'}}}}
const box=e=>{{const r=R(e);return [r.left,r.top,r.right,r.bottom]}},bx={{brand:box(br),title:box(h),lead:box(p),start:box(st)}};
$('#res').textContent=JSON.stringify({{boxes:bx,font:px(),wide:h.scrollWidth>h.clientWidth,lines:Math.round(R(p).height/LH),block:R(p).bottom-R(h).top}})}})</script></body>'''


def chrome(src, *args):
    return subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files',
                           '--force-device-scale-factor=1', '--window-size=1200,630', '--virtual-time-budget=3000', *args,
                           'file:///' + src.replace('\\', '/')], check=True, capture_output=True)


def check(res, out):
    """The laid-out boxes must stay inside the 48 px margins and keep 24 px between neighbours; otherwise stop and name the file."""
    bx, names = res['boxes'], ['brand', 'title', 'lead', 'start']
    bad = [f'{n} leaves the 48 px margin' for n in names if bx[n][0] < 48 or bx[n][1] < 48 or bx[n][2] > 1152 or bx[n][3] > 582]
    bad += [f'{a} and {b} are closer than 24 px' for i, a in enumerate(names) for b in names[i + 1:]
            if bx[a][0] < bx[b][2] and bx[b][0] < bx[a][2] and bx[a][1] < bx[b][3] + 24 and bx[b][1] < bx[a][3] + 24]
    if res['wide']:
        bad.append('the longest word of the title does not fit the column')
    if bad:
        raise SystemExit(f'{out}: ' + '; '.join(bad))


METRICS = {}


def shoot(page, out):
    with tempfile.TemporaryDirectory() as tmp:
        src, png = os.path.join(tmp, 'c.html'), os.path.join(tmp, 'c.png')
        with open(src, 'w', encoding='utf-8') as f:
            f.write(page)
        dom = chrome(src, '--dump-dom').stdout.decode('utf-8')          # the page lays itself out; read what it decided
        res = json.loads(re.search(r'<div id="res"[^>]*>(.*?)</div>', dom, re.S).group(1))
        check(res, out)
        METRICS[os.path.relpath(out, ROOT).replace('\\', '/')] = res
        chrome(src, f'--screenshot={png}')
        Image.open(png).convert('RGB').save(out, quality=82, optimize=True, progressive=True)


def main():
    only = {a for a in sys.argv[1:] if not a.startswith('--')}
    pick = next((a[8:].split(',') for a in sys.argv[1:] if a.startswith('--langs=')), LANGS)   # --langs=de,fr: only these
    for name, art, title, lead in cards():
        slug = name.split('/')[-1]
        if (only and slug not in only) or (not only and slug in SKIP):
            continue
        for lang in (l for l in pick if l in title):        # a one-language guide has one card
            out = os.path.join(ROOT, 'assets', f'{name}-{lang}.jpg')
            shoot(html(art, title[lang], lead[lang], lang, slug), out)
        print(name, 'ok')
    if os.environ.get('OG_REPORT'):
        with open(os.environ['OG_REPORT'], 'w') as f:
            json.dump(METRICS, f)


if __name__ == '__main__':
    main()
