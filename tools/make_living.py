"""Masks for the living art (assets/living/living.js): which parts of a picture move and how.
One RGBA PNG per picture, half the source size, in source coordinates (1376 x 768 grid):
  hero_dawn      R falling water, G banner cloth (0 at the pole -> 1 at the tip), B open sky, A river
  hero_campfire  R flames, G (unused), B open sky, A river
  hero_road      R (unused), G (unused), B open sky, A river
  hero_roster    R hearth fire and candle flames, G banners (0 at the beam -> 1 at the tip), B night windows, A (unused)
  hero_tools     R (unused), G banner (0 at the pole -> 1 at the tip), B open sky, A lake
  hero_guides    R (unused), G pennant (0 at the spear -> 1 at the tip), B open sky, A river
  hero_dungeons  R brazier, campfire and torch flames, G (unused), B night sky, A stream
  hero_professions R forge fire, G hanging herbs (0 at the beam -> 1 at the tips), B open sky, A stream
  hero_faq       R candle flames, G banners (0 at the rod -> 1 at the tip), B sunbeam from the window, A (unused)
Run: python tools/make_living.py [path-to-wow_art]"""
import os, sys
from PIL import Image, ImageDraw, ImageFilter, ImageChops

SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.expanduser('~'), 'projects', 'gabella', 'bot', 'assets', 'wow_art')
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


def shape(polys, ramp=None):
    """Grey mask of hand-drawn polygons (cloth, a lake); ramp(x, y) scales the value inside."""
    m = Image.new('L', (W, H), 0)
    d = ImageDraw.Draw(m)
    for p in polys:
        d.polygon(p, fill=255)
    if ramp:
        mp = m.load()
        for y in range(H):
            for x in range(W):
                if mp[x, y]:
                    mp[x, y] = round(255 * ramp(x, y))
    return m


def save(name, r, g, b, a):
    os.makedirs(OUT, exist_ok=True)
    half = [c.resize((W // 2, H // 2), Image.LANCZOS) for c in (r, g, b, a)]  # one by one: RGBA resize premultiplies alpha
    im = Image.merge('RGBA', half)
    im.save(os.path.join(OUT, f'{name}-fx.png'), optimize=True)
    print(name, 'ok', os.path.getsize(os.path.join(OUT, f'{name}-fx.png')) // 1024, 'KB')


def dawn():
    im = load('hero_dawn')
    grey = im.convert('L')
    hp = ImageChops.subtract(grey, grey.filter(ImageFilter.GaussianBlur(6)), 1, 0).load()  # falls are streaks brighter than what is behind
    falls = [(680, 190, 698, 335), (714, 228, 728, 330)]  # thin falls under the floating islands
    water = pick(im, falls, lambda r, g, b, x, y: lum(r, g, b) > .55 and sat(r, g, b) < .25 and hp[x, y] > 2, lambda x, y: fade(y, 190, 212))
    big = pick(im, [(586, 440, 646, 566), (676, 455, 694, 525)], lambda r, g, b, x, y: lum(r, g, b) > .5 and sat(r, g, b) < .25 and hp[x, y] > 1,  # the valley fall
               lambda x, y: fade(y, 440, 454) * (1 - fade(y, 545, 566)))
    water = ImageChops.lighter(water, big)
    cloth = pick(im, [(778, 36, 1250, 170)], lambda r, g, b, x, y: sat(r, g, b) > .3 and (b > r + 10 or r > b + 30) and not (x > 1050 and y > 148),  # cloth and gold trim; not the sky, topknot or mohawk
                 lambda x, y: min(1, (x - 778) / 470))  # banner: 0 at the pole -> 1 at the tail
    open_sky = sky([(190, 95, 478, 372), (598, 150, 772, 340), (748, 0, 1262, 180), (752, 0, 800, H), (850, 0, W, H)],
                   (200, 330))  # castle, islands, banner, pole, mountains and heroes
    river = ImageChops.lighter(pick(im, [(520, 405, 680, 448)], lambda r, g, b, x, y: lum(r, g, b) > .78 and sat(r, g, b) < .15),  # upper bends
                               pick(im, [(345, 585, 610, 705)], lambda r, g, b, x, y: lum(r, g, b) > .45 and sat(r, g, b) < .18))  # lower reach in shade
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
    open_sky = sky([(700, 100, 905, 270), (868, 40, W, 340), (1110, 115, 1315, 390), (212, 82, 282, 138)], (190, 245))  # castle, cliffs, signpost, moon
    river = pick(im, [(340, 350, 520, 445), (556, 452, 724, 508)], lambda r, g, b, x, y: lum(r, g, b) > .4 and b >= r)
    zero = Image.new('L', (W, H), 0)
    save('hero_road', zero, zero, open_sky, soft(river, 1, 2))


def roster():
    im = load('hero_roster')
    flame = lambda r, g, b, x, y: r > 200 and g > 110 and r - b > 110   # noqa: E731
    fire = pick(im, [(95, 395, 225, 510), (443, 386, 456, 406), (701, 394, 712, 414), (716, 402, 725, 416)], flame)
    banners = shape([[(380, 22), (450, 22), (448, 232), (412, 264), (382, 232)], [(634, 0), (728, 0), (726, 212), (683, 245), (638, 212)]],
                    lambda x, y: fade(y, 40, 250))   # hang from the beams: still at the top, the tips swing
    windows = pick(im, [(912, 118, 1075, 300), (1290, 88, W, 330)], lambda r, g, b, x, y: b > r + 30)
    zero = Image.new('L', (W, H), 0)
    save('hero_roster', soft(fire, 2, 2), soft(banners, 0, 2), soft(windows, 0, 1.5), zero)


def tools():
    im = load('hero_tools')
    banner = shape([[(808, 160), (872, 160), (872, 286), (840, 302), (808, 286)]], lambda x, y: fade(y, 160, 300))
    open_sky = ImageChops.multiply(pick(im, [(90, 55, 700, 320)], lambda r, g, b, x, y: lum(r, g, b) > .5),
                                   sky([(600, 170, 720, H)], (225, 300)))   # right cliff; peaks stay sharp
    lake = shape([[(300, 398), (470, 398), (430, 440), (560, 462), (560, 520), (470, 545), (380, 565), (260, 615), (150, 660),
                   (103, 663), (117, 550), (217, 510), (283, 490), (210, 417)]])
    zero = Image.new('L', (W, H), 0)
    save('hero_tools', zero, soft(banner, 0, 1.5), soft(open_sky, 1, 2), soft(lake, 0, 3))


def guides():
    im = load('hero_guides')
    pennant = pick(im, [(592, 405, 712, 528)], lambda r, g, b, x, y: lum(r, g, b) < .3 or (r > 150 and g > 110 and b < 90),
                   lambda x, y: fade(x, 708, 610))   # black-and-gold cloth; the spear on the right stays put
    open_sky = sky([(530, 170, 820, H), (75, 280, 305, 365), (765, 140, 925, H), (855, 160, W, H), (1140, 0, W, H), (0, 250, 560, H)],
                   (215, 290))   # peak, castle, signpost, heroes, cliff, hills
    river = pick(im, [(240, 330, 560, 452)], lambda r, g, b, x, y: lum(r, g, b) > .62 and sat(r, g, b) < .3 and b > g - 25)
    zero = Image.new('L', (W, H), 0)
    save('hero_guides', zero, soft(pennant, 1, 1.5), open_sky, soft(river, 1, 2))


def dungeons():
    im = load('hero_dungeons')
    flame = lambda r, g, b, x, y: r > 200 and g > 110 and r - b > 110   # noqa: E731
    fire = pick(im, [(215, 418, 285, 482), (600, 420, 662, 480), (1000, 555, 1105, 655), (1238, 285, 1278, 348)], flame)
    night = pick(im, [(560, 0, 840, 250)], lambda r, g, b, x, y: b > 85 and b > r + 40)   # the cliffs are darker than the sky
    stream = pick(im, [(270, 585, 480, 705)], lambda r, g, b, x, y: lum(r, g, b) > .3 and b > r + 15)
    zero = Image.new('L', (W, H), 0)
    save('hero_dungeons', soft(fire, 2, 2), zero, soft(night, 0, 2), soft(stream, 1, 2))


def professions():
    im = load('hero_professions')
    flame = lambda r, g, b, x, y: r > 200 and g > 110 and r - b > 110   # noqa: E731
    fire = pick(im, [(112, 385, 238, 478)], flame)
    herbs = shape([[(845, 95), (900, 95), (902, 205), (870, 215), (845, 200)], [(898, 105), (935, 105), (935, 200), (900, 200)],
                   [(925, 120), (1010, 120), (1010, 235), (925, 235)]], lambda x, y: fade(y, 100, 225))
    open_sky = ImageChops.multiply(pick(im, [(300, 0, 760, 250)], lambda r, g, b, x, y: lum(r, g, b) > .6 and sat(r, g, b) < .35),
                                   sky([(0, 0, 330, 210), (600, 150, 820, H), (580, 0, 800, 120), (0, 210, W, H)], (190, 250)))   # roof, house, trees
    stream = pick(im, [(440, 365, 600, 498)], lambda r, g, b, x, y: lum(r, g, b) > .55 and sat(r, g, b) < .35 and b >= g - 15)
    zero = Image.new('L', (W, H), 0)
    save('hero_professions', soft(fire, 2, 2), soft(herbs, 0, 2), soft(open_sky, 1, 2), soft(stream, 1, 2))


def faq():
    im = load('hero_faq')
    flame = lambda r, g, b, x, y: lum(r, g, b) > .75 and r > b + 50   # noqa: E731
    candles = pick(im, [(30, 405, 82, 440), (148, 420, 168, 442)], flame)
    banners = shape([[(152, 0), (244, 0), (240, 300), (198, 355), (155, 300)], [(546, 30), (612, 30), (612, 290), (580, 330), (548, 290)]],
                    lambda x, y: fade(y, 30, 330))
    beam = shape([[(230, 60), (385, 60), (660, 560), (610, 700), (320, 700), (205, 445)]]).filter(ImageFilter.GaussianBlur(30))
    zero = Image.new('L', (W, H), 0)
    save('hero_faq', soft(candles, 2, 2), soft(banners, 0, 2), beam, zero)


if __name__ == '__main__':
    dawn()
    campfire()
    road()
    roster()
    tools()
    guides()
    dungeons()
    professions()
    faq()
