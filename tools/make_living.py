"""Masks for the living art (assets/living/living.js): which parts of a picture move and how.
One RGBA PNG per picture, half the source size, in source coordinates (1376 x 768 grid):
  hero_dawn      R falling water, G banner cloth (0 at the pole -> 1 at the tip), B open sky, A river
  hero_campfire  R flames, G (unused), B open sky, A river
  hero_road      R lantern flames, G (unused), B open sky, A river
  hero_roster, hero_tools, hero_guides, hero_dungeons, hero_professions, hero_faq, hero_news,
  hero_leveling, hero_classes, hero_races, hero_ukrainian, hero_requirements (one shader, living.js GEN):
                 R flames, G plants and hanging cloth in the wind (0 where tied -> 1 at the tips), B open sky, A river or lake
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
    water = pick(im, [(450, 516, 508, 632)], lambda r, g, b, x, y: lum(r, g, b) > .45 and sat(r, g, b) < .25 and hp[x, y] > 1,  # the valley fall
                 lambda x, y: fade(y, 516, 530) * (1 - fade(y, 608, 632)))
    cloth = pick(im, [(884, 126, 1114, 204)], lambda r, g, b, x, y: sat(r, g, b) > .22 and (b > r + 10 or r > b + 30),  # cloth and gold trim, not the sky
                 lambda x, y: min(1, (x - 884) / 226))  # banner: 0 at the pole -> 1 at the tail
    open_sky = ImageChops.multiply(pick(im, [(0, 0, W, 340)], lambda r, g, b, x, y: lum(r, g, b) > .55),   # the floating rocks stay put
                                   open_area([(0, 0), (W, 0), (W, 40), (1240, 98), (1122, 132), (900, 126), (898, 66), (854, 66), (854, 330),
                                              (836, 330), (826, 250), (800, 196), (770, 150), (722, 150), (694, 200), (670, 246),
                                              (640, 290), (620, 340), (0, 340)], (240, 312)))   # castle, banner, pole, heroes
    river = ImageChops.lighter(pick(im, [(368, 458, 600, 514)], lambda r, g, b, x, y: lum(r, g, b) > .7 and sat(r, g, b) < .2),  # bends above the fall
                               pick(im, [(420, 630, 560, 705)], lambda r, g, b, x, y: lum(r, g, b) > .38 and sat(r, g, b) < .2))  # below it, in shade
    save('hero_dawn', soft(water, 1, 1.5), soft(cloth, 3, 1.2), soft(open_sky, 1, 2), soft(river, 1, 2))


def campfire():
    im = load('hero_campfire')
    fire = flames(im, [(985, 480, 1095, 575)], 190)
    open_sky = ImageChops.multiply(open_area([(0, 0), (1165, 0), (1148, 150), (1000, 160), (860, 236), (760, 246), (692, 236),
                                              (650, 330), (0, 330)], (270, 335)), moon(365, 110, 48))   # heroes, the rock and the moon stay put
    river = pick(im, [(320, 400, 520, 570)], lambda r, g, b, x, y: lum(r, g, b) > .42 and b > r + 20)
    zero = Image.new('L', (W, H), 0)
    save('hero_campfire', soft(fire, 2, 2.5), zero, soft(open_sky, 1, 2), soft(river, 1, 2))


def road():
    im = load('hero_road')
    lamps = flames(im, [(822, 312, 860, 362), (862, 462, 905, 522)], 190)
    open_sky = ImageChops.multiply(open_area([(0, 0), (1040, 0), (1030, 130), (950, 176), (892, 140), (872, 92), (728, 92), (705, 282),
                                              (600, 300), (300, 290), (272, 228), (150, 222), (100, 268), (0, 268)], (232, 300)),
                                   moon(252, 115, 40))   # signpost, tree, heroes, castle and the moon stay put
    river = pick(im, [(355, 380, 645, 600), (110, 540, 470, 620)], lambda r, g, b, x, y: lum(r, g, b) > .32 and b > r + 25)
    zero = Image.new('L', (W, H), 0)
    save('hero_road', soft(lamps, 2, 2), zero, soft(open_sky, 1, 2), soft(river, 1, 2))


def roster():
    im = load('hero_roster')
    fire = flames(im, [(90, 355, 255, 545), (565, 370, 595, 410), (1015, 445, 1045, 485), (1050, 435, 1080, 475)], 190)
    banners = shape([[(132, 0), (262, 0), (262, 205), (198, 240), (134, 205)], [(376, 96), (472, 96), (470, 312), (424, 352), (378, 312)]],
                    lambda x, y: fade(y, 20, 245) if x < 300 else fade(y, 110, 350))   # still at the rods, the tips swing
    zero = Image.new('L', (W, H), 0)
    save('hero_roster', soft(fire, 2, 2), soft(banners, 0, 2), zero, zero)


def tools():
    im = load('hero_tools')
    lamp = flames(im, [(775, 170, 825, 230)], 190)
    banner = shape([[(578, 198), (690, 198), (688, 360), (634, 400), (580, 360)]], lambda x, y: fade(y, 200, 400))
    opening = shape([[(205, 172), (440, 165), (458, 335), (150, 345), (175, 250)]]).filter(ImageFilter.GaussianBlur(10))
    open_sky = ImageChops.multiply(opening, pick(im, [(140, 160, 470, 350)], lambda r, g, b, x, y: lum(r, g, b) > .55))
    lake = pick(im, [(125, 380, 470, 505)], lambda r, g, b, x, y: lum(r, g, b) > .5 and sat(r, g, b) < .35)
    save('hero_tools', soft(lamp, 2, 2), soft(banner, 0, 1.5), soft(open_sky, 1, 2), soft(lake, 1, 2))


def guides():
    im = load('hero_guides')
    open_sky = open_area([(0, 0), (W, 0), (W, 165), (1252, 168), (1140, 158), (1080, 128), (958, 138), (936, 96),
                          (920, 60), (818, 60), (758, 108), (742, 226), (712, 228), (700, 300), (0, 300)], (228, 292))   # signpost, heroes, castle
    zero = Image.new('L', (W, H), 0)
    save('hero_guides', zero, zero, soft(open_sky, 1, 2), zero)


def dungeons():
    im = load('hero_dungeons')
    fire = flames(im, [(390, 430, 450, 495), (630, 435, 682, 495), (925, 540, 1060, 650), (1108, 450, 1162, 525)], 190)
    night = ImageChops.multiply(open_area([(250, 0), (690, 0), (660, 100), (560, 150), (420, 140), (330, 120), (260, 60)], (90, 150)),
                                moon(462, 52, 34))   # between the cliffs; the moon stays put
    stream = pick(im, [(450, 355, 570, 625)], lambda r, g, b, x, y: lum(r, g, b) > .38 and b > r + 25)
    zero = Image.new('L', (W, H), 0)
    save('hero_dungeons', soft(fire, 2, 2), zero, soft(night, 1, 2), soft(stream, 1, 2))


def professions():
    im = load('hero_professions')
    fire = ImageChops.lighter(flames(im, [(40, 370, 150, 465)], 190), flames(im, [(715, 535, 840, 590), (975, 405, 1000, 435)], 210))
    herbs = shape([[(858, 140), (900, 140), (905, 245), (870, 260), (855, 240)], [(905, 150), (940, 150), (945, 255), (905, 250)],
                   [(940, 150), (982, 150), (985, 262), (945, 262)], [(1225, 80), (1290, 80), (1295, 200), (1228, 200)]],
                  lambda x, y: fade(y, 145, 255) if x < 1100 else fade(y, 85, 200))   # tied at the beam, the bundles swing
    open_sky = ImageChops.multiply(pick(im, [(110, 20, 700, 280)], lambda r, g, b, x, y: lum(r, g, b) > .62 and sat(r, g, b) < .45),
                                   open_area([(112, 30), (150, 26), (700, 108), (700, 210), (560, 232), (330, 262), (112, 262)], (200, 262)))
    stream = pick(im, [(330, 330, 570, 405)], lambda r, g, b, x, y: lum(r, g, b) > .6 and sat(r, g, b) < .4)
    save('hero_professions', soft(fire, 2, 2), soft(herbs, 0, 2), soft(open_sky, 1, 2), soft(stream, 1, 2))


def faq():
    im = load('hero_faq')
    candles = flames(im, [(530, 368, 598, 412)], 180)
    banners = shape([[(102, 40), (200, 40), (198, 300), (152, 322), (104, 300)], [(522, 165), (574, 165), (574, 318), (548, 336), (522, 318)]],
                    lambda x, y: fade(y, 45, 320) if x < 300 else fade(y, 170, 335))
    zero = Image.new('L', (W, H), 0)
    save('hero_faq', soft(candles, 2, 2), soft(banners, 0, 2), zero, zero)


def news():
    im = load('hero_news')
    lamp = flames(im, [(915, 145, 985, 235)], 190)
    open_sky = open_area([(240, 0), (1100, 0), (1098, 62), (1050, 98), (1040, 48), (925, 38), (912, 112), (862, 150), (780, 150),
                          (690, 172), (620, 205), (560, 220), (470, 118), (330, 108), (300, 58)], (110, 215))   # roofs, raven, lantern, board
    zero = Image.new('L', (W, H), 0)
    save('hero_news', soft(lamp, 2, 2), zero, soft(open_sky, 1, 2), zero)


def moon(x, y, r):
    """255 everywhere but a soft hole around the moon, so the clouds do not drag it along."""
    m = Image.new('L', (W, H), 255)
    ImageDraw.Draw(m).ellipse((x - r, y - r, x + r, y + r), fill=0)
    return m.filter(ImageFilter.GaussianBlur(r / 3))


def flames(im, boxes, hot=200):
    return pick(im, boxes, lambda r, g, b, x, y: r > hot and g > 110 and r - b > 110 and lum(r, g, b) > hot / 340)


def open_area(poly, top_fade):
    """Open sky inside a hand-drawn outline (the skyline, heads), soft edges, fading out towards the horizon."""
    return ImageChops.multiply(shape([poly]).filter(ImageFilter.GaussianBlur(18)), sky([], top_fade))


def leveling():
    im = load('hero_leveling')
    open_sky = ImageChops.multiply(pick(im, [(110, 20, 580, 270)], lambda r, g, b, x, y: lum(r, g, b) > .62 and sat(r, g, b) < .42),
                                   sky([(0, 0, 110, H), (560, 0, W, H)], (215, 270)))   # between the trees, above the far hills
    river = pick(im, [(290, 330, 510, 570)], lambda r, g, b, x, y: lum(r, g, b) > .62 and sat(r, g, b) < .3)
    zero = Image.new('L', (W, H), 0)
    save('hero_leveling', zero, zero, soft(open_sky, 1, 2), soft(river, 1, 2))


def classes():
    im = load('hero_classes')
    open_sky = ImageChops.multiply(pick(im, [(0, 0, 575, 230)], lambda r, g, b, x, y: lum(r, g, b) > .66),
                                   sky([(570, 0, W, H), (0, 200, 340, H)], (150, 215)))   # tower, walls; the peaks stay put
    zero = Image.new('L', (W, H), 0)
    save('hero_classes', zero, zero, soft(open_sky, 1, 2), zero)


def races():
    im = load('hero_races')
    lamps = flames(im, [(218, 440, 242, 470), (388, 450, 412, 480), (446, 392, 466, 420), (728, 512, 752, 542), (242, 608, 270, 645),
                        (618, 618, 642, 650), (140, 480, 160, 510)])
    open_sky = ImageChops.multiply(pick(im, [(0, 0, W, 300)], lambda r, g, b, x, y: lum(r, g, b) > .62),
                                   open_area([(0, 0), (1150, 0), (1150, 60), (1000, 110), (900, 150), (800, 200), (760, 300), (0, 300)],
                                             (230, 300)))   # along the mountain ridge, above the heroes
    zero = Image.new('L', (W, H), 0)
    save('hero_races', soft(lamps, 2, 2), zero, soft(open_sky, 1, 2), zero)


def ukrainian():
    im = load('hero_ukrainian')
    sunflowers = pick(im, [(0, 362, 440, 500)], lambda r, g, b, x, y: r > 165 and g > 115 and b < 90 and r > b + 90 and sat(r, g, b) > .6,
                      lambda x, y: fade(y, 500, 380))   # heads sway, the stems stay rooted; not the sunlit field behind them
    open_sky = open_area([(0, 0), (W, 0), (W, 110), (1350, 110), (1290, 128), (1262, 134), (1180, 134), (1120, 128), (1050, 128),
                          (1000, 206), (962, 222), (900, 214), (860, 216), (830, 250), (790, 250), (740, 236), (690, 254),
                          (650, 270), (560, 320), (240, 320), (230, 225), (140, 225), (125, 270), (0, 270)], (250, 320))   # windmill, roofs, heads
    zero = Image.new('L', (W, H), 0)
    save('hero_ukrainian', zero, soft(sunflowers, 1, 1.5), soft(open_sky, 1, 2), zero)


def requirements():
    im = load('hero_requirements')
    fire = flames(im, [(470, 30, 530, 120), (990, 20, 1050, 110), (505, 330, 540, 375), (995, 340, 1065, 400)], 235)
    zero = Image.new('L', (W, H), 0)
    save('hero_requirements', soft(fire, 2, 2), zero, zero, zero)


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
    news()
    leveling()
    classes()
    races()
    ukrainian()
    requirements()
