"""Masks for the living art (assets/living/living.js): which parts of a picture move and how.
One RGBA PNG per picture, half the source size, in source coordinates (1376 x 768 grid):
  hero_dawn      R falling water, G banner cloth (0 at the pole -> 1 at the tip), B open sky, A river
  hero_campfire  R flames, G (unused), B open sky, A river
  hero_road      R (unused), G (unused), B open sky, A river
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
    grey = im.convert('L')
    hp = ImageChops.subtract(grey, grey.filter(ImageFilter.GaussianBlur(6)), 1, 0).load()  # falls are streaks brighter than the clouds behind
    falls = [(464, 196, 494, 345), (510, 150, 556, 372), (596, 146, 640, 350), (698, 190, 734, 335), (742, 160, 772, 305)]  # under the floating island
    water = pick(im, falls, lambda r, g, b, x, y: lum(r, g, b) > .7 and sat(r, g, b) < .2 and hp[x, y] > 4, lambda x, y: fade(y, 146, 176))
    cloth = pick(im, [(676, 30, 1350, 172)], lambda r, g, b, x, y: lum(r, g, b) < .5 and b > r + 12 and not (1050 < x < 1135 and y > 116 or x > 1030 and y > 140),
                 lambda x, y: min(1, (x - 676) / 640))  # banner: 0 at the pole -> 1 at the tail
    open_sky = sky([(452, 80, 802, 345), (656, 0, 1376, 182), (660, 0, 692, H), (736, 120, W, H)], (150, 330))  # island, banner, pole, heroes
    river = ImageChops.lighter(pick(im, [(220, 470, 580, 555)], lambda r, g, b, x, y: lum(r, g, b) > .8),  # sunlit bends
                               pick(im, [(210, 555, 480, 606)], lambda r, g, b, x, y: lum(r, g, b) > .55 and sat(r, g, b) < .15))  # silver reach in shade
    save('hero_dawn', soft(water, 1, 1.5), soft(cloth, 3, 1.2), open_sky, soft(river, 1, 2))


def campfire():
    im = load('hero_campfire')
    flames = pick(im, [(855, 500, 1015, 655)], lambda r, g, b, x, y: r > 200 and g > 110 and r - b > 110)
    open_sky = sky([(1090, 0, W, 430), (700, 180, 925, 430), (920, 160, 1100, 430), (585, 295, 725, 430)],  # rock+orc, troll, paladin, elf
                   (300, 390))  # heads stay sharp
    river = ImageChops.lighter(pick(im, [(180, 470, 430, 530)], lambda r, g, b, x, y: lum(r, g, b) > .5 and b >= r),  # moonlit bends
                               pick(im, [(170, 525, 515, 602)], lambda r, g, b, x, y: lum(r, g, b) > .3 and b > r + 40))  # wide reach below
    zero = Image.new('L', (W, H), 0)
    save('hero_campfire', soft(flames, 2, 2.5), zero, open_sky, soft(river, 1, 2))


def road():
    im = load('hero_road')
    open_sky = sky([(200, 160, 365, 300), (690, 115, 905, H), (860, 135, 1185, H), (1095, 0, W, H), (800, 0, W, 225)],
                   (130, 235))  # castle, horse, paladin, signpost, cliffs
    river = pick(im, [(260, 360, 560, 520)], lambda r, g, b, x, y: lum(r, g, b) > .45 and b >= r)
    zero = Image.new('L', (W, H), 0)
    save('hero_road', zero, zero, open_sky, soft(river, 1, 2))


if __name__ == '__main__':
    dawn()
    campfire()
    road()
