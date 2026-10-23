"""Masks for the living art (assets/living/living.js): which parts of a picture move and how.
One RGBA PNG per picture, half the source size, in source coordinates (1376 x 768 grid):
  hero_dawn      R falling water, G banner cloth (0 at the pole -> 1 at the tip), B open sky, A river
  hero_campfire  R flames, G (unused), B open sky, A river
Run: python tools/make_living.py [path-to-wow_art]"""
import os, sys
from PIL import Image, ImageFilter, ImageChops

SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.expanduser('~'), 'gabella-bot', 'assets', 'wow_art')
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', 'living')
W, H = 1376, 768


def load(name):
    im = Image.open(os.path.join(SRC, name + '.jpg')).convert('RGB')
    return im.resize((W, H), Image.LANCZOS) if im.size != (W, H) else im


def pick(im, boxes, test, ramp=None):
    """Grey mask: 255 where test(r, g, b, x, y) holds inside one of the boxes; ramp(x, y) scales the value."""
    m = Image.new('L', (W, H), 0)
    px, mp = im.load(), m.load()
    for x0, y0, x1, y1 in boxes:
        for y in range(y0, y1):
            for x in range(x0, x1):
                r, g, b = px[x, y]
                if test(r, g, b, x, y):
                    mp[x, y] = round(255 * (ramp(x, y) if ramp else 1))
    return m


def soft(m, grow=1, blur=1.5):
    if grow:
        m = m.filter(ImageFilter.MaxFilter(grow * 2 + 1))
    return m.filter(ImageFilter.GaussianBlur(blur))


def lum(r, g, b):
    return (.2126 * r + .7152 * g + .0722 * b) / 255


def sat(r, g, b):
    hi, lo = max(r, g, b), min(r, g, b)
    return (hi - lo) / hi if hi else 0


def fade(v, a, b):
    """0 at a, 1 at b (either direction), clamped."""
    t = max(0, min(1, (v - a) / (b - a)))
    return t * t * (3 - 2 * t)


def sky(boxes_out, top_fade):
    """Open sky: 1 above top_fade[0], fading to 0 at top_fade[1], minus the boxes (islands, peaks, castle)."""
    m = Image.new('L', (W, H), 0)
    mp = m.load()
    for y in range(H):
        v = round(255 * (1 - fade(y, *top_fade)))
        if v:
            for x in range(W):
                mp[x, y] = v
    cut = Image.new('L', (W, H), 255)
    for b in boxes_out:
        cut.paste(0, b)
    cut = cut.filter(ImageFilter.GaussianBlur(14))
    return ImageChops.multiply(m, cut)


def save(name, r, g, b, a):
    os.makedirs(OUT, exist_ok=True)
    half = [c.resize((W // 2, H // 2), Image.LANCZOS) for c in (r, g, b, a)]  # one by one: RGBA resize premultiplies alpha
    im = Image.merge('RGBA', half)
    im.save(os.path.join(OUT, f'{name}-fx.png'), optimize=True)
    print(name, 'ok', os.path.getsize(os.path.join(OUT, f'{name}-fx.png')) // 1024, 'KB')


def dawn():
    im = load('hero_dawn')
    falls = [(860, 112, 884, 305), (916, 98, 972, 310), (1055, 102, 1080, 270), (1104, 112, 1125, 220)]
    water = pick(im, falls, lambda r, g, b, x, y: lum(r, g, b) > .5 and sat(r, g, b) < .3, lambda x, y: fade(y, 98, 122))
    low = pick(im, [(458, 526, 564, 664)], lambda r, g, b, x, y: lum(r, g, b) > .33 and b >= r,  # the lower fall sits in shade
               lambda x, y: fade(y, 526, 540) * (1 - fade(y, 640, 664)))
    water = ImageChops.lighter(water, low)
    blue = pick(im, [(838, 298, 1072, 394)], lambda r, g, b, x, y: lum(r, g, b) < .5 or sat(r, g, b) > .38,
                lambda x, y: min(1, (x - 832) / 236))
    red = pick(im, [(1213, 300, 1374, 378)], lambda r, g, b, x, y: r > g + 28 or lum(r, g, b) < .4,
               lambda x, y: min(1, (x - 1209) / 160))
    cloth = ImageChops.lighter(blue, red)
    open_sky = sky([(806, 40, 1198, 318), (1250, 196, W, 330), (280, 262, 372, 300)], (190, 285))
    river = pick(im, [(376, 462, 566, 548)], lambda r, g, b, x, y: lum(r, g, b) > .58 and b >= r)
    save('hero_dawn', soft(water, 1, 1.5), soft(cloth, 3, 1.2), open_sky, soft(river, 1, 2))


def campfire():
    im = load('hero_campfire')
    flames = pick(im, [(918, 505, 1010, 590)], lambda r, g, b, x, y: r > 200 and g > 110 and r - b > 110)
    open_sky = sky([(1090, 0, W, 330), (392, 196, 478, 286), (160, 250, 300, 330),  # rock, island, ruins
                    (895, 182, 978, 300), (712, 252, 792, 330), (596, 276, 644, 330)], (215, 300))  # staff, axe, bow
    river = pick(im, [(300, 330, 560, 480)], lambda r, g, b, x, y: lum(r, g, b) > .55 and b >= r)
    zero = Image.new('L', (W, H), 0)
    save('hero_campfire', soft(flames, 2, 2.5), zero, open_sky, soft(river, 1, 2))


if __name__ == '__main__':
    dawn()
    campfire()
