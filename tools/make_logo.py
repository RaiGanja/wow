"""Logo files from the approved mark (griffin in the G, gold on #050505, no outer rings): assets/brand/gabella-icon-1024.png.
Makes assets/logo.png (512; PWA icons, OG and the Discord bot read it), assets/brand/mark.webp (header mark, 96)
and assets/icons/favicon-48/64/96.png + favicon.ico. The 16/32/48 px favicon frames are hand-tuned (engraving merged
into a blob so the G reads): assets/brand/favicon-<size>-src.png, copied as they are.
To swap the mark: replace gabella-icon-1024.png (and the favicon-*-src.png frames), then
python tools/make_logo.py && python tools/make_icons.py && python tools/make_og.py && python build.py"""
import os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRAND = os.path.join(ROOT, 'assets', 'brand')
ICONS = os.path.join(ROOT, 'assets', 'icons')
BG = (5, 5, 5)


def quant(im):
    """96-colour palette with the background colour exact (the quantizer lands one step off on near-black)."""
    q = im.quantize(96, Image.Quantize.FASTOCTREE)
    pal = q.getpalette()
    i = min(range(len(pal) // 3), key=lambda k: sum(abs(pal[3 * k + c] - BG[c]) for c in range(3)))
    pal[3 * i:3 * i + 3] = list(BG)
    q.putpalette(pal)
    return q


def main():
    src = Image.open(os.path.join(BRAND, 'gabella-icon-1024.png')).convert('RGB')
    logo = src.resize((512, 512), Image.LANCZOS)
    quant(logo).save(os.path.join(ROOT, 'assets', 'logo.png'), optimize=True)
    src.resize((96, 96), Image.LANCZOS).save(os.path.join(BRAND, 'mark.webp'), quality=90)
    fav = {s: Image.open(os.path.join(BRAND, f'favicon-{s}-src.png')).convert('RGB') for s in (16, 32, 48)}
    quant(src.resize((64, 64), Image.LANCZOS)).save(os.path.join(ICONS, 'favicon-64.png'), optimize=True)
    # Google search shows a favicon only in sizes that are multiples of 48; favicon.ico goes to the hub root too
    fav[48].save(os.path.join(ICONS, 'favicon-48.png'), optimize=True)
    src.resize((96, 96), Image.LANCZOS).save(os.path.join(ICONS, 'favicon-96.png'), optimize=True)
    fav[48].save(os.path.join(ICONS, 'favicon.ico'), sizes=[(16, 16), (32, 32), (48, 48)], append_images=[fav[16], fav[32]])
    print('logo ok')


if __name__ == '__main__':
    main()
