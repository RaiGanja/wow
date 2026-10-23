"""Review sheets for the home hero by time of day, for a yes/no before the variants go live.
Run: python tools/tod_sheet.py <out_dir> <dawn.jpg> <day.jpg> <dusk.jpg> <night.jpg>   (aligned variants, same size)
Writes <out_dir>/tod-sheet.jpg (the four scenes 2 x 2, captioned) and <out_dir>/tod-heroes.jpg (every hero cropped at
100% of the source, one row per hero, dawn / day / dusk / night side by side)."""
import os, sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1376, 768   # grid the hero boxes are given in (the mask's grid); scaled to the source size
TODS = ('dawn', 'day', 'dusk', 'night')
NAMES = {'dawn': 'Утро', 'day': 'День', 'dusk': 'Вечер', 'night': 'Ночь'}
HEROES = {   # x0, y0, x1, y1 in the W x H grid: head and shoulders
    'paladin': (720, 236, 912, 428), 'elf': (884, 262, 1012, 420), 'orc': (980, 120, 1190, 340),
    'troll': (1130, 140, 1376, 370), 'dwarf': (1100, 390, 1300, 610), 'lantern': (960, 500, 1080, 730)}
GOLD, BG = (201, 165, 74), (10, 11, 13)


def font(size):
    for f in ('C:/Windows/Fonts/segoeui.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'):
        if os.path.exists(f):
            return ImageFont.truetype(f, size)
    return ImageFont.load_default()


def scenes(ims, width=1376):
    """2 x 2 sheet of whole scenes, each `width` px wide, captioned."""
    h = round(width * ims[0].height / ims[0].width)
    gap, cap = 8, 40
    out = Image.new('RGB', (2 * width + gap, 2 * (h + cap) + gap), BG)
    d, f = ImageDraw.Draw(out), font(26)
    for i, (tod, im) in enumerate(zip(TODS, ims)):
        x, y = (i % 2) * (width + gap), (i // 2) * (h + cap + gap)
        d.text((x + 4, y + 6), NAMES[tod], fill=GOLD, font=f)
        out.paste(im.resize((width, h), Image.LANCZOS), (x, y + cap))
    return out


def heroes(ims):
    """Rows of hero crops at 100% of the source, one column per time of day."""
    sx, sy = ims[0].width / W, ims[0].height / H
    boxes = {k: tuple(round(v * s) for v, s in zip(b, (sx, sy, sx, sy))) for k, b in HEROES.items()}
    gap, cap = 6, 34
    cw = max(b[2] - b[0] for b in boxes.values())
    out = Image.new('RGB', (4 * cw + 3 * gap, cap + sum(b[3] - b[1] + gap for b in boxes.values())), BG)
    d, f = ImageDraw.Draw(out), font(22)
    for i, tod in enumerate(TODS):
        d.text((i * (cw + gap) + 4, 4), NAMES[tod], fill=GOLD, font=f)
    y = cap
    for b in boxes.values():
        for i, im in enumerate(ims):
            out.paste(im.crop(b), (i * (cw + gap), y))
        y += b[3] - b[1] + gap
    return out


def main():
    if len(sys.argv) != 6:
        sys.exit(__doc__)
    out = sys.argv[1]
    ims = [Image.open(p).convert('RGB') for p in sys.argv[2:]]
    if len({im.size for im in ims}) != 1:
        sys.exit('variants differ in size: align them first (tools/align_tod.py)')
    os.makedirs(out, exist_ok=True)
    scenes(ims).save(os.path.join(out, 'tod-sheet.jpg'), quality=90)
    heroes(ims).save(os.path.join(out, 'tod-heroes.jpg'), quality=92)
    print(os.path.join(out, 'tod-sheet.jpg'), os.path.join(out, 'tod-heroes.jpg'))


if __name__ == '__main__':
    main()
