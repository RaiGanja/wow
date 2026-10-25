"""Logo files from the griffin-G monogram (gold on black): assets/brand/griffin-g-src.jpg.
Makes assets/logo.png (512, on the site background; PWA icons, OG and the Discord bot read it),
assets/brand/mark.webp (header mark) and assets/icons/favicon-64.png — both on the dark tile,
because on the light theme the black engraving lines would vanish into the paper.
Run: python tools/make_logo.py, then python tools/make_icons.py and python tools/make_og.py."""
import os
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'assets', 'brand', 'griffin-g-src.jpg')
BG = (5, 5, 5)


def transparent(im):
    """Black background → alpha; gold kept by un-premultiplying against black."""
    a = np.asarray(im).astype(np.float32)
    alpha = np.clip((a.max(axis=2) - 22) / (150 - 22), 0, 1)
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
    small = logo.resize((96, 96), Image.LANCZOS)
    small.save(os.path.join(ROOT, 'assets', 'brand', 'mark.webp'), quality=90)
    icons = os.path.join(ROOT, 'assets', 'icons')
    quant(logo.resize((64, 64), Image.LANCZOS)).save(os.path.join(icons, 'favicon-64.png'), optimize=True)
    # Google search shows a favicon only in sizes that are multiples of 48; favicon.ico goes to the hub root too
    for size in (48, 96):
        logo.resize((size, size), Image.LANCZOS).save(os.path.join(icons, f'favicon-{size}.png'), optimize=True)
    logo.save(os.path.join(icons, 'favicon.ico'), sizes=[(16, 16), (32, 32), (48, 48)])
    print('logo ok')


if __name__ == '__main__':
    main()
