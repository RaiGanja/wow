"""Web images for the guide: source art (gabella-bot/assets/wow_art) -> assets/art/*.avif|webp in several widths.
Run: python tools/make_images.py [path-to-wow_art]"""
import os, sys
from PIL import Image, ImageFilter

SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.expanduser('~'), 'gabella-bot', 'assets', 'wow_art')
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


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, widths in JOBS:
        im = Image.open(os.path.join(SRC, name + '.jpg')).convert('RGB')
        for w in widths:
            save(im, name, w)
        print(name, 'ok')


if __name__ == '__main__':
    main()
