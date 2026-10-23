"""Web images for the guide: source art (gabella-bot/assets/wow_art) -> assets/art/*.avif|webp in several widths,
plus class and race page extras: blurred hero backdrop assets/art/<id>-bg.webp and share preview assets/og/<id>.jpg.
Race portraits live in wow_art/races/<race id>.jpg and are saved under the race page slug.
Run: python tools/make_images.py [path-to-wow_art] [--classes-only | --races-only | --faces-only | --hero-mobile]"""
import os, sys
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

ARGS = [a for a in sys.argv[1:] if not a.startswith('--')]
SRC = ARGS[0] if ARGS else os.path.join(os.path.expanduser('~'), 'gabella-bot', 'assets', 'wow_art')
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', 'art')
CLASSES = ['warrior', 'paladin', 'hunter', 'rogue', 'priest', 'shaman', 'mage', 'warlock', 'druid']
RACES = {'human': 'human', 'dwarf': 'dwarf', 'nightelf': 'night-elf', 'gnome': 'gnome', 'skyA': 'skyborne-alliance',
         'orc': 'orc', 'undead': 'undead', 'tauren': 'tauren', 'troll': 'troll', 'skyH': 'skyborne-horde'}
SCENE_Q = 66  # wide scene art fills the screen: AVIF at 52 smears grass and fur there
JOBS = [('hero_dawn', [960, 1440, 1920, 2560, 3840])] + [('hero_campfire', [960, 1600, 2560]), ('hero_road', [960, 1600, 2560])] + [(c, [360, 600, 896]) for c in CLASSES]


def save(im, name, w, aq=52):
    if im.width != w:
        up = w > im.width
        h = round(im.height * w / im.width)
        im = im.resize((w, h), Image.LANCZOS)
        if up:  # upscaled: restore a little edge contrast
            im = im.filter(ImageFilter.UnsharpMask(radius=1.6, percent=60, threshold=2))
    im.save(os.path.join(OUT, f'{name}-{w}.avif'), quality=aq, speed=4)
    im.save(os.path.join(OUT, f'{name}-{w}.webp'), quality=80, method=6)


def source(name):
    """Source art; <name>@4x.jpg (the same picture upscaled 4x) wins when present, so wide screens get real detail."""
    big = os.path.join(SRC, name + '@4x.jpg')
    return Image.open(big if os.path.exists(big) else os.path.join(SRC, name + '.jpg')).convert('RGB')


def cover(im, w, h):
    """Scale and center-crop to w x h."""
    k = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def backdrop(im, w, h):
    """Blurred, darkened wide copy of a portrait that fills the space around it."""
    bg = cover(im, w, h).filter(ImageFilter.GaussianBlur(max(w, h) / 40))
    return ImageEnhance.Brightness(bg).enhance(.55)


def page_extras(cid, src=None):
    im = Image.open(src or os.path.join(SRC, cid + '.jpg')).convert('RGB')
    backdrop(im, 480, 270).save(os.path.join(OUT, f'{cid}-bg.webp'), quality=70, method=6)
    # share preview 1200x630: backdrop + centered portrait with soft side edges
    og = backdrop(im, 1200, 630)
    por = im.resize((round(im.width * 630 / im.height), 630), Image.LANCZOS)
    mask = Image.new('L', por.size, 255)
    d = ImageDraw.Draw(mask)
    fade = por.width // 4
    for x in range(fade):
        a = round(255 * x / fade)
        d.line([(x, 0), (x, 630)], fill=a)
        d.line([(por.width - 1 - x, 0), (por.width - 1 - x, 630)], fill=a)
    og.paste(por, ((1200 - por.width) // 2, 0), mask)
    os.makedirs(os.path.join(os.path.dirname(OUT), 'og'), exist_ok=True)
    og.save(os.path.join(os.path.dirname(OUT), 'og', f'{cid}.jpg'), quality=84, optimize=True, progressive=True)


# face centre as a share of portrait height, where it differs from the default
FACE_Y = {'gnome': .33, 'dwarf': .27, 'skyborne-horde': .24}


def face(src, name):
    """Square head-and-shoulders crop for round avatars: <name>-face.avif|webp, 160 px."""
    im = Image.open(src).convert('RGB')
    w, h = im.size
    side, cy = int(w * .44), int(h * FACE_Y.get(name, .25))
    im = im.crop((w // 2 - side // 2, cy - side // 2, w // 2 + side // 2, cy + side // 2)).resize((160, 160), Image.LANCZOS)
    im.save(os.path.join(OUT, f'{name}-face.avif'), quality=55, speed=4)
    im.save(os.path.join(OUT, f'{name}-face.webp'), quality=82, method=6)


def hero_mobile():
    """Portrait cut of the home hero for phones: hero_dawn-m-600|1000. Cut at x = .6 * (width - 600), so the
    phone view (object-position 60%) shows exactly the same part of the picture as with the full-width file:
    the banner, the paladin and the elf, with no face under the title."""
    im = source('hero_dawn')
    w = round(600 * im.height / 768)
    x = round(.6 * (im.width - w))
    im = im.crop((x, 0, x + w, im.height))
    for width in (600, 1000):
        save(im, 'hero_dawn-m', width, SCENE_Q)
    print('hero_dawn-m ok')


def main():
    os.makedirs(OUT, exist_ok=True)
    if '--hero-mobile' in sys.argv:
        hero_mobile()
        return
    if '--faces-only' in sys.argv:
        for cid in CLASSES:
            face(os.path.join(SRC, cid + '.jpg'), cid)
        for rid, slug in RACES.items():
            face(os.path.join(SRC, 'races', rid + '.jpg'), slug)
        print('faces ok')
        return
    if '--races-only' in sys.argv:
        for rid, slug in RACES.items():
            src = os.path.join(SRC, 'races', rid + '.jpg')
            page_extras(slug, src)
            im = Image.open(src).convert('RGB')
            for w in (360, 600, 896):
                save(im, slug, w)
            face(src, slug)
            print(slug, 'ok')
        return
    for cid in CLASSES:
        page_extras(cid)
        face(os.path.join(SRC, cid + '.jpg'), cid)
    print('class extras ok')
    if '--classes-only' in sys.argv:
        return
    for name, widths in JOBS:
        im = source(name)
        for w in widths:
            save(im, name, w, SCENE_Q if name.startswith('hero_') else 52)
        print(name, 'ok')
    hero_mobile()


if __name__ == '__main__':
    main()
