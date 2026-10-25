"""Masks for the living art (assets/living/living.js): which parts of a picture move and how.
One RGBA PNG per picture, half the source size, in source coordinates (1376 x 768 grid):
  hero_dawn      R falling water, G banner cloth (0 at the pole -> 1 at the tip), B open sky, A (none: only the fall moves)
  hero_campfire  R flames, G (unused), B open sky, A (none)
  hero_road      R lights (see below), G (unused), B open sky, A (none)
  hero_roster, hero_tools, hero_guides, hero_dungeons, hero_professions, hero_faq, hero_news,
  hero_leveling, hero_classes, hero_races, hero_ukrainian, hero_requirements, hero_bestrace, hero_tierlist
  (one shader, living.js GEN):
                 R lights, G plants and hanging cloth in the wind (0 where tied -> 1 at the tips), B open sky, A river or lake
No water on the home page but the fall, none on leveling and tools; no fire on roster, no candle flames (faq).
Lights (R, living.js lights()): 1 open fire that flows up (hearth, forge, braziers), .75 a candle flame that sways in place,
  .5 lantern glass that glows, under .43 the soft halo around lanterns and candles.
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
    open_sky = ImageChops.multiply(open_sky, moon(642, 340, 44))   # the night variant's moon by the castle stays put
    zero = Image.new('L', (W, H), 0)   # the river stays still: the painted water looks better than the moving one
    save('hero_dawn', soft(water, 1, 1.5), soft(cloth, 3, 1.2), soft(open_sky, 1, 2), zero)


def campfire():
    im = load('hero_campfire')
    fire = flames(im, [(985, 480, 1095, 575)], 190)
    open_sky = ImageChops.multiply(open_area([(0, 0), (1165, 0), (1148, 132), (990, 132), (900, 200), (770, 200), (700, 222),
                                              (600, 222), (540, 236), (505, 250), (495, 330), (0, 330)], (270, 335)),
                                   moon(365, 110, 48))   # the Horde party (troll's totem, mohawk, orc's top-knot, horns), the rock and the moon stay put
    zero = Image.new('L', (W, H), 0)
    save('hero_campfire', soft(fire, 2, 2.5), zero, soft(open_sky, 1, 2), zero)


def road():
    im = load('hero_road')
    lamps = lights(lamps=glass(im, [(813, 321, 842, 356), (494, 488, 536, 560)]), spots=[(828, 338, 110), (515, 525, 120)])   # signpost, dwarf's hand
    open_sky = ImageChops.multiply(open_area([(0, 0), (1010, 0), (1000, 110), (885, 110), (800, 82), (760, 82), (690, 122), (690, 300),
                                              (300, 300), (272, 200), (100, 200), (90, 268), (0, 268)], (232, 300)),
                                   moon(245, 112, 36))   # signpost, tree, heroes, castle and the moon stay put
    zero = Image.new('L', (W, H), 0)
    save('hero_road', lamps, zero, soft(open_sky, 1, 2), zero)


def roster():
    banners = shape([[(132, 0), (262, 0), (262, 205), (198, 240), (134, 205)], [(376, 96), (472, 96), (470, 312), (424, 352), (378, 312)]],
                    lambda x, y: fade(y, 20, 245) if x < 300 else fade(y, 110, 350))   # still at the rods, the tips swing
    zero = Image.new('L', (W, H), 0)
    save('hero_roster', zero, soft(banners, 0, 2), zero, zero)   # no fire: the hearth and the candles stay as painted


def tools():
    im = load('hero_tools')
    lamp = lights(lamps=glass(im, [(758, 154, 812, 219)]), spots=[(785, 188, 130)])
    banner = shape([[(578, 198), (690, 198), (688, 360), (634, 400), (580, 360)]], lambda x, y: fade(y, 200, 400))
    opening = shape([[(205, 172), (440, 165), (458, 335), (150, 345), (175, 250)]]).filter(ImageFilter.GaussianBlur(10))
    open_sky = ImageChops.multiply(opening, pick(im, [(140, 160, 470, 350)], lambda r, g, b, x, y: lum(r, g, b) > .55))
    zero = Image.new('L', (W, H), 0)   # the lake stays still
    save('hero_tools', lamp, soft(banner, 0, 1.5), soft(open_sky, 1, 2), zero)


def guides():
    im = load('hero_guides')
    open_sky = open_area([(0, 0), (W, 0), (W, 230), (1340, 230), (1340, 105), (1240, 105), (1235, 135), (1150, 128), (1100, 118),
                          (975, 148), (925, 92), (845, 56), (805, 56), (745, 92), (742, 198), (698, 198), (692, 300), (0, 300)],
                         (228, 292))   # signpost, the druid's staff and pack, heroes, the stronghold
    zero = Image.new('L', (W, H), 0)
    save('hero_guides', zero, zero, soft(open_sky, 1, 2), zero)


def dungeons():
    im = load('hero_dungeons')
    fire = lights(soft(flames(im, [(390, 430, 450, 495), (630, 435, 682, 495), (925, 540, 1060, 650)], 190), 2, 2),   # braziers, campfire
                  lamps=glass(im, [(1076, 462, 1120, 524)]), spots=[(1098, 492, 100)])   # the dwarf's lantern
    night = ImageChops.multiply(open_area([(250, 0), (690, 0), (660, 100), (560, 150), (420, 140), (330, 120), (260, 60)], (90, 150)),
                                moon(462, 52, 34))   # between the cliffs; the moon stays put
    stream = pick(im, [(450, 355, 570, 625)], lambda r, g, b, x, y: lum(r, g, b) > .38 and b > r + 25)
    zero = Image.new('L', (W, H), 0)
    save('hero_dungeons', fire, zero, soft(night, 1, 2), soft(stream, 1, 2))


def professions():
    im = load('hero_professions')
    fire = lights(soft(ImageChops.lighter(flames(im, [(35, 325, 165, 460)], 190), flames(im, [(715, 535, 840, 590)], 210)), 2, 2),   # forge, hot iron
                  flame(im, [(979.5, 410, 424, 4.5)]), spots=[(980, 418, 30)])   # the burner under the flask
    herbs = shape([[(858, 140), (900, 140), (905, 245), (870, 260), (855, 240)], [(905, 150), (940, 150), (942, 198), (906, 198)],   # the bundle in the elf's hand: only above her fingers
                   [(940, 150), (982, 150), (985, 262), (945, 262)], [(1225, 80), (1290, 80), (1295, 200), (1228, 200)]],
                  lambda x, y: fade(y, 145, 255) if x < 1100 else fade(y, 85, 200))   # tied at the beam, the bundles swing
    open_sky = ImageChops.multiply(pick(im, [(110, 20, 700, 280)], lambda r, g, b, x, y: lum(r, g, b) > .62 and sat(r, g, b) < .45),
                                   open_area([(112, 30), (150, 26), (700, 108), (700, 210), (560, 232), (330, 262), (112, 262)], (200, 262)))
    stream = pick(im, [(330, 330, 570, 405)], lambda r, g, b, x, y: lum(r, g, b) > .6 and sat(r, g, b) < .4)
    save('hero_professions', fire, soft(herbs, 0, 2), soft(open_sky, 1, 2), soft(stream, 1, 2))


def faq():
    banners = shape([[(100, 44), (198, 44), (196, 300), (150, 318), (102, 300)], [(515, 165), (574, 165), (574, 320), (545, 338), (517, 320)]],
                    lambda x, y: fade(y, 45, 320) if x < 300 else fade(y, 170, 335))
    zero = Image.new('L', (W, H), 0)
    save('hero_faq', zero, soft(banners, 0, 2), zero, zero)   # the candles stay as painted


def news():
    im = load('hero_news')
    lamp = lights(lamps=glass(im, [(918, 163, 967, 217)]), spots=[(942, 190, 130)])   # the glass glows, not the post beside it
    open_sky = open_area([(240, 0), (1100, 0), (1098, 62), (1050, 98), (1040, 48), (925, 38), (912, 112), (862, 150), (780, 150),
                          (690, 172), (620, 205), (560, 220), (470, 118), (330, 108), (300, 58)], (110, 215))   # roofs, raven, lantern, board
    zero = Image.new('L', (W, H), 0)
    save('hero_news', lamp, zero, soft(open_sky, 1, 2), zero)


def moon(x, y, r):
    """255 everywhere but a soft hole around the moon, so the clouds do not drag it along."""
    m = Image.new('L', (W, H), 255)
    ImageDraw.Draw(m).ellipse((x - r, y - r, x + r, y + r), fill=0)
    return m.filter(ImageFilter.GaussianBlur(r / 3))


def flames(im, boxes, hot=200):
    return pick(im, boxes, lambda r, g, b, x, y: r > hot and g > 110 and r - b > 110 and lum(r, g, b) > hot / 340)


def candle(x, tip, wick, hw):
    """Outline of a candle flame: a teardrop from its tip down to the wick, hw its half width (art px)."""
    h = wick - tip
    return [(x, tip), (x + hw * .55, tip + h * .3), (x + hw, tip + h * .68), (x + hw * .7, wick), (x - hw * .7, wick),
            (x - hw, tip + h * .68), (x - hw * .55, tip + h * .3)]


def flame(im, cs):
    """Candle flames: inside the teardrops, only where the flame is bright."""
    boxes = [(int(x - hw - 1), int(tip - 1), int(x + hw + 2), int(wick + 2)) for x, tip, wick, hw in cs]
    return soft(ImageChops.multiply(shape([candle(*c) for c in cs]), pick(im, boxes, lambda r, g, b, x, y: lum(r, g, b) > .5)), 1, .8)


def glass(im, boxes):
    """Lit lantern glass inside the boxes; the dark frame between the panes stays out."""
    return soft(pick(im, boxes, lambda r, g, b, x, y: lum(r, g, b) > .42 and r > b + 50), 0, 1)


def halo(spots):
    """Warm light around lanterns and candles: 1 at (x, y), fading out at radius r."""
    m = Image.new('L', (W, H), 0)
    mp = m.load()
    for cx, cy, r in spots:
        for y in range(max(0, cy - r), min(H, cy + r)):
            for x in range(max(0, cx - r), min(W, cx + r)):
                d = ((x - cx) ** 2 + (y - cy) ** 2) ** .5 / r
                if d < 1:
                    mp[x, y] = max(mp[x, y], round(255 * (1 - d) ** 1.5))
    return m


def lights(fire=None, flames=None, lamps=None, spots=()):
    """Mask R for living.js lights(): fire 1, candle flames .75, lantern glass .5, the halo under .43."""
    r = halo(spots).point(lambda v: round(v * .43))
    for m, k in ((lamps, .5), (flames, .75), (fire, 1)):
        if m is not None:
            r = ImageChops.lighter(r, m.point(lambda v, k=k: round(v * k)))
    return r


def open_area(poly, top_fade):
    """Open sky inside a hand-drawn outline (the skyline, heads), soft edges, fading out towards the horizon."""
    return ImageChops.multiply(shape([poly]).filter(ImageFilter.GaussianBlur(18)), sky([], top_fade))


def leveling():
    im = load('hero_leveling')
    open_sky = ImageChops.multiply(pick(im, [(110, 20, 540, 270)], lambda r, g, b, x, y: lum(r, g, b) > .62 and sat(r, g, b) < .42),
                                   sky([(0, 0, 110, H), (525, 0, W, H)], (215, 270)))   # between the trees, above the far hills; clear of the tauren's antlers
    zero = Image.new('L', (W, H), 0)   # the river stays still
    save('hero_leveling', zero, zero, soft(open_sky, 1, 2), zero)


def classes():
    im = load('hero_classes')
    open_sky = ImageChops.multiply(pick(im, [(0, 0, 575, 230)], lambda r, g, b, x, y: lum(r, g, b) > .66),
                                   sky([(570, 0, W, H), (0, 200, 340, H)], (95, 150)))   # tower, walls; the peaks stay put
    zero = Image.new('L', (W, H), 0)
    save('hero_classes', zero, zero, soft(open_sky, 1, 2), zero)


def races():
    im = load('hero_races')
    lamps = lights(lamps=glass(im, [(221, 447, 239, 469), (141, 486, 159, 508), (451, 391, 469, 413), (388, 426, 406, 448), (731, 519, 749, 541), (247, 617, 265, 639), (619, 624, 637, 646)]),
                   spots=[(230, 458, 26), (150, 497, 26), (460, 402, 26), (397, 437, 26), (740, 530, 26), (256, 628, 34), (628, 635, 34)])   # the market lanterns
    open_sky = ImageChops.multiply(pick(im, [(0, 0, W, 300)], lambda r, g, b, x, y: lum(r, g, b) > .62),
                                   open_area([(0, 0), (1150, 0), (1150, 60), (1000, 110), (900, 150), (800, 200), (760, 300), (0, 300)],
                                             (230, 300)))   # along the mountain ridge, above the heroes
    zero = Image.new('L', (W, H), 0)
    save('hero_races', lamps, zero, soft(open_sky, 1, 2), zero)


def ukrainian():
    im = load('hero_ukrainian')
    sunflowers = pick(im, [(0, 362, 440, 500)], lambda r, g, b, x, y: r > 165 and g > 115 and b < 90 and r > b + 90 and sat(r, g, b) > .6,
                      lambda x, y: fade(y, 500, 380))   # heads sway, the stems stay rooted; not the sunlit field behind them
    open_sky = open_area([(0, 0), (W, 0), (W, 215), (1262, 215), (1262, 86), (1160, 86), (1100, 94), (900, 124), (900, 196),
                          (780, 196), (765, 148), (712, 148), (690, 196), (600, 214), (560, 222), (430, 222), (420, 320), (245, 320),
                          (240, 212), (132, 212), (118, 270), (0, 270)], (250, 320))   # windmill, roofs, heads
    zero = Image.new('L', (W, H), 0)
    save('hero_ukrainian', zero, soft(sunflowers, 1, 1.5), soft(open_sky, 1, 2), zero)


def requirements():
    im = load('hero_requirements')
    fire = lights(soft(flames(im, [(1008, 330, 1062, 392)], 235), 2, 2),   # the furnace (not the dwarf's shoulder beside it)
                  lamps=glass(im, [(474, 36, 538, 118), (990, 36, 1044, 108)]),
                  spots=[(505, 78, 100), (1017, 72, 90)])   # the two hanging lanterns
    zero = Image.new('L', (W, H), 0)
    save('hero_requirements', fire, zero, zero, zero)


def bestrace():
    im = load('hero_bestrace')
    open_sky = ImageChops.multiply(pick(im, [(30, 0, 860, 260)], lambda r, g, b, x, y: lum(r, g, b) > .6),
                                   open_area([(40, 0), (845, 0), (800, 70), (765, 150), (700, 140), (670, 100), (590, 96), (575, 138),
                                              (510, 130), (500, 190), (400, 200), (365, 250), (262, 250), (242, 160), (228, 104),
                                              (120, 104), (100, 170), (55, 150), (40, 100)], (190, 250)))   # cliffs and statue heads stay put
    river = ImageChops.multiply(shape([[(398, 395), (428, 395), (432, 428), (470, 468), (505, 495), (530, 525), (550, 560), (560, 595), (550, 625),
                                        (525, 645), (500, 660), (300, 672), (150, 685), (120, 640), (150, 590), (250, 555), (330, 518), (362, 478), (385, 428)]]),
                                pick(im, [(110, 390, 650, 720)], lambda r, g, b, x, y: lum(r, g, b) > .26 and sat(r, g, b) < .32))
    zero = Image.new('L', (W, H), 0)   # no fire: daylight in the canyon
    save('hero_bestrace', zero, zero, soft(open_sky, 1, 2), soft(river, 1, 2))   # the water ends at the rock under the heroes


def tierlist():
    im = load('hero_tierlist')
    lamps = lights(lamps=glass(im, [(165, 178, 208, 248), (527, 278, 552, 312), (1228, 100, 1284, 178)]),
                   spots=[(186, 212, 70), (540, 295, 40), (1256, 140, 80)])   # the glass glows, no flame
    banners = shape([[(30, 48), (98, 48), (95, 250), (64, 285), (34, 250)], [(212, 102), (265, 102), (262, 285), (238, 300), (214, 285)],
                     [(336, 132), (382, 132), (380, 295), (358, 312), (338, 295)], [(420, 158), (462, 158), (460, 300), (440, 318), (422, 300)]],
                    lambda x, y: fade(y, 50, 285) if x < 150 else fade(y, 105, 300) if x < 300 else fade(y, 135, 312) if x < 400 else fade(y, 160, 318))
    poles = Image.new('L', (W, H), 0)
    for b in [(52, 0, 74, 60), (230, 55, 250, 110), (348, 100, 368, 140), (430, 145, 450, 165), (112, 130, 212, 260), (494, 248, 556, 320),
              (895, 30, 1000, 205), (845, 110, 910, 205), (1222, 30, 1376, 300)]:
        poles.paste(255, b)   # spear tips, lantern posts and the lamps, the paladin's raised hammer
    poles = ImageChops.invert(ImageChops.lighter(poles, banners.point(lambda v: 255 if v else 0)).filter(ImageFilter.MaxFilter(13)))
    open_sky = ImageChops.multiply(open_area([(0, 0), (1222, 0), (1222, 190), (1120, 232), (1060, 160), (1000, 118), (995, 28), (895, 28),
                                              (845, 150), (845, 200), (700, 200), (600, 188), (588, 245), (560, 262),
                                              (0, 280)], (230, 290)), poles.filter(ImageFilter.GaussianBlur(6)))   # the banners swing, the sky drifts behind them
    save('hero_tierlist', lamps, soft(banners, 0, 2), soft(open_sky, 1, 2), Image.new('L', (W, H), 0))


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
    bestrace()
    tierlist()
