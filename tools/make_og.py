"""Share previews 1200x630 with the page title on the art: home (og-<lang>.jpg), guides, the classes/ and races/ sections
and tools (og/<slug>-<lang>.jpg). Rendered from HTML with the site fonts by headless Chrome, so the type matches the site.
Class and race pages keep their language-neutral art previews from make_images.py.
Run: python tools/make_og.py [slug ...]   (no args = all cards)"""
import os, subprocess, sys, tempfile
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'content'))
from guides import HUB, GUIDES, HUBS  # noqa: E402

CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
LANGS = ('ru', 'en', 'uk')
BRAND = 'Gabella Team'
START = {'ru': 'Старт 4 ноября 2026', 'en': 'Launch November 4, 2026', 'uk': 'Старт 4 листопада 2026'}
HOME = {'t': {'ru': 'WoW Forever', 'en': 'WoW Forever', 'uk': 'WoW Forever'},
        'd': {'ru': 'Открытый гид: классы, расы, подземелья, прокачка и сборка группы',
              'en': 'An open guide: classes, races, dungeons, leveling and party building',
              'uk': 'Відкритий гід: класи, раси, підземелля, прокачування та збір групи'}}
TOOLS = {'t': {'ru': 'Инструменты', 'en': 'Tools', 'uk': 'Інструменти'},
         'd': {'ru': 'Рамки группы, рейдовая сетка, сравнение классов и рас, поиск по гиду',
               'en': 'Party frames, raid grid, class and race comparison, guide search',
               'uk': 'Рамки групи, рейдова сітка, порівняння класів і рас, пошук по гіду'}}
WIDE = ('hero_dawn', 'hero_campfire')    # landscape art fills the card; portraits stand on the right


def cards():
    """(file name without -lang, art, title by lang, line under the title by lang)"""
    yield 'og', 'hero_dawn', HOME['t'], HOME['d']
    yield 'og/guides', HUB['art'], HUB['title'], HUB['lead']
    for g in GUIDES + HUBS:
        yield 'og/' + g['slug'], g['art'], g['title'], g['lead']
    yield 'og/tools', 'rogue', TOOLS['t'], TOOLS['d']


def url(path):
    return 'file:///' + os.path.join(ROOT, path).replace('\\', '/')


def html(art, title, lead, lang):
    wide = art in WIDE
    pic = (f'<img class="wide" src="{url(f"assets/art/{art}-1440.webp" if art == "hero_dawn" else f"assets/art/{art}-1600.webp")}">'
           if wide else
           f'<img class="blur" src="{url(f"assets/art/{art}-bg.webp")}"><img class="por" src="{url(f"assets/art/{art}-896.webp")}">')
    fonts = ''.join(
        f'@font-face{{font-family:"{fam}";font-weight:400 700;src:url({url("assets/fonts/" + f)}) format("woff2");unicode-range:{rng}}}'
        for fam, base in (('Bona Nova SC', 'bona-nova-sc'), ('Golos Text', 'golos-text'))
        for f, rng in ((base + '-cyrillic.woff2', 'U+0400-045F,U+0490-0491,U+04B0-04B1,U+2116'), (base + '-latin.woff2', 'U+0000-00FF,U+2000-206F')))
    return f'''<!doctype html><meta charset="utf-8"><style>{fonts}
*{{margin:0;box-sizing:border-box}}
body{{width:1200px;height:630px;overflow:hidden;background:#07080a;position:relative;font-family:"Golos Text";color:#efe9da}}
img{{position:absolute;display:block}}
.wide{{inset:0;width:100%;height:100%;object-fit:cover;object-position:{'70%' if art == 'hero_dawn' else '88%'} 50%}}
.blur{{inset:0;width:100%;height:100%;object-fit:cover;filter:brightness(.8)}}
.por{{right:40px;top:0;height:630px;-webkit-mask-image:linear-gradient(90deg,transparent,#000 22%,#000 78%,transparent)}}
.shade{{position:absolute;inset:0;background:linear-gradient(90deg,#07080a 0%,rgba(7,8,10,.92) 34%,rgba(7,8,10,.35) 62%,rgba(7,8,10,0) 80%),
  linear-gradient(0deg,rgba(7,8,10,.85) 0%,rgba(7,8,10,0) 36%)}}
.txt{{position:absolute;left:72px;top:0;bottom:0;width:640px;display:flex;flex-direction:column;justify-content:center;gap:22px}}
.brand{{position:absolute;left:72px;top:56px;display:flex;align-items:center;gap:14px;font-size:24px;color:#cfc8b6;letter-spacing:.01em}}
.brand img{{position:static;width:56px;height:56px;border-radius:10px;box-shadow:0 0 0 1px rgba(201,165,74,.45)}}
h1{{font:700 {'92' if len(title) <= 14 else '74'}px/1.02 "Bona Nova SC";letter-spacing:.02em;text-wrap:balance}}
p{{font-size:30px;line-height:1.35;color:#c9c2b0;text-wrap:pretty;max-width:{"520" if wide else "600"}px}}
.start{{position:absolute;left:72px;bottom:56px;font:700 28px/1 "Bona Nova SC";letter-spacing:.03em;color:#c9a54a}}
</style><body>{pic}<div class="shade"></div>
<div class="brand"><img src="{url('assets/logo.png')}" alt="">{BRAND}</div>
<div class="txt"><h1>{title}</h1><p>{lead}</p></div>
<div class="start">{START[lang]}</div></body>'''


def shoot(page, out):
    with tempfile.TemporaryDirectory() as tmp:
        src, png = os.path.join(tmp, 'c.html'), os.path.join(tmp, 'c.png')
        with open(src, 'w', encoding='utf-8') as f:
            f.write(page)
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files',
                        '--force-device-scale-factor=1', '--window-size=1200,630', '--virtual-time-budget=3000',
                        f'--screenshot={png}', 'file:///' + src.replace('\\', '/')],
                       check=True, capture_output=True)
        Image.open(png).convert('RGB').save(out, quality=82, optimize=True, progressive=True)


def main():
    only = set(sys.argv[1:])
    for name, art, title, lead in cards():
        if only and name.split('/')[-1] not in only:
            continue
        for lang in LANGS:
            out = os.path.join(ROOT, 'assets', f'{name}-{lang}.jpg')
            shoot(html(art, title[lang], lead[lang], lang), out)
        print(name, 'ok')


if __name__ == '__main__':
    main()
