"""Logo files from the griffin-G monogram (gold on black): assets/brand/griffin-g-src.png.
Makes assets/logo.png (512, on the site background; PWA icons, OG and the Discord bot read it),
assets/brand/mark.webp (header mark) and assets/icons/favicon-64.png — both on the dark tile,
because on the light theme the black engraving lines would vanish into the paper.
Run: python tools/make_logo.py, then python tools/make_icons.py and python tools/make_og.py."""
import os
import numpy as np
from PIL import Image, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'assets', 'brand', 'griffin-g-src.png')
BG = (5, 5, 5)
GOLD = (201, 165, 74)


def transparent(im):
    """Black background → alpha; gold kept by un-premultiplying against black."""
    a = np.asarray(im).astype(np.float32)
    alpha = np.clip((a.max(axis=2) - 34) / (160 - 34), 0, 1)
    rgb = np.where(alpha[..., None] > 0, a / np.maximum(alpha[..., None], 1e-3), 0).clip(0, 255)
    return Image.fromarray(np.dstack([rgb, alpha * 255]).astype(np.uint8), 'RGBA')


def square(im, pad):
    """Crop to the drawing and centre it on a square with `pad` share of margin."""
    box = im.getchannel('A').point(lambda v: 255 if v > 40 else 0).getbbox()
    im = im.crop(box)
    side = round(max(im.size) * (1 + 2 * pad))
    out = Image.new('RGBA', (side, side), (0, 0, 0, 0))
    out.paste(im, ((side - im.width) // 2, (side - im.height) // 2), im)
    return out


def quant(im):
    """96-colour palette with the background colour exact (the quantizer lands one step off on near-black)."""
    q = im.quantize(96, Image.Quantize.FASTOCTREE)
    pal = q.getpalette()
    i = min(range(len(pal) // 3), key=lambda k: sum(abs(pal[3 * k + c] - BG[c]) for c in range(3)))
    pal[3 * i:3 * i + 3] = list(BG)
    q.putpalette(pal)
    return q


def main():
    mark = transparent(Image.open(SRC).convert('RGB'))
    logo = Image.new('RGBA', (512, 512), BG + (255,))
    inner = square(mark, .12).resize((512, 512), Image.LANCZOS)
    logo.alpha_composite(inner)
    quant(logo.convert('RGB')).save(os.path.join(ROOT, 'assets', 'logo.png'), optimize=True)
    logo = logo.convert('RGB')
    tight = square(mark, .02).resize((512, 512), Image.LANCZOS)

    def frame(grow):
        """Tight crop on the site background, flat gold, lines thickened by `grow` px: hatching merges into solid shapes."""
        flat = Image.new('RGBA', tight.size, GOLD + (0,))
        flat.putalpha(tight.getchannel('A').filter(ImageFilter.MaxFilter(grow)))
        out = Image.new('RGBA', tight.size, BG + (255,))
        out.alpha_composite(flat)
        return out.convert('RGB')
    small = frame(3).resize((96, 96), Image.LANCZOS)   # header mark, shown at 40 px
    small.save(os.path.join(ROOT, 'assets', 'brand', 'mark.webp'), quality=90)
    icons = os.path.join(ROOT, 'assets', 'icons')
    # Favicon frame: the same mark, tighter (ring fills the tile) with the engraving lines lifted, so the head and the G read at 16-32 px
    fav = frame(5)
    quant(fav.resize((64, 64), Image.LANCZOS)).save(os.path.join(icons, 'favicon-64.png'), optimize=True)
    # Google search shows a favicon only in sizes that are multiples of 48; favicon.ico goes to the hub root too
    for size in (48, 96):
        fav.resize((size, size), Image.LANCZOS).save(os.path.join(icons, f'favicon-{size}.png'), optimize=True)
    fav.save(os.path.join(icons, 'favicon.ico'), sizes=[(16, 16), (32, 32), (48, 48)])
    print('logo ok')


if __name__ == '__main__':
    main()
