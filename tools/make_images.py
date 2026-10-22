"""Web images for the guide: source art (gabella-bot/assets/wow_art) -> assets/art/*.avif|webp in several widths,
plus class page extras: blurred hero backdrop assets/art/<class>-bg.webp and share preview assets/og/<class>.jpg.
Run: python tools/make_images.py [path-to-wow_art] [--classes-only]"""
import os, sys
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

ARGS = [a for a in sys.argv[1:] if not a.startswith('--')]
SRC = ARGS[0] if ARGS else os.path.join(os.path.expanduser('~'), 'gabella-bot', 'assets', 'wow_art')
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', 'art')
CLASSES = ['warrior', 'paladin', 'hunter', 'rogue', 'priest', 'shaman', 'mage', 'warlock', 'druid']
JOBS = [('hero_dawn', [960, 1440, 1920, 2560])] + [('hero_campfire', [960, 1600])] + [(c, [360, 600, 896]) for c in CLASSES]


def save(im, name, w):
    if im.width != w:
        h = round(im.height * w / im.width)
        im = im.resize((w, h), Image.LANCZOS)
        if w > 1376:  # upscaled: restore a little edge contrast
            im = im.filter(ImageFilter.UnsharpMask(radius=1.6, percent=60, threshold=2))
    im.save(os.path.join(OUT, f'{name}-{w}.avif'), quality=52, speed=4)
    im.save(os.path.join(OUT, f'{name}-{w}.webp'), quality=80, method=6)


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


def class_extras(cid):
    im = Image.open(os.path.join(SRC, cid + '.jpg')).convert('RGB')
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


def main():
    os.makedirs(OUT, exist_ok=True)
    for cid in CLASSES:
        class_extras(cid)
    print('class extras ok')
    if '--classes-only' in sys.argv:
        return
    for name, widths in JOBS:
        im = Image.open(os.path.join(SRC, name + '.jpg')).convert('RGB')
        for w in widths:
            save(im, name, w)
        print(name, 'ok')


if __name__ == '__main__':
    main()
