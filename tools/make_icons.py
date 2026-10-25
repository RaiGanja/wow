"""App icons for the installable site (PWA) from the gold G logo: assets/icons/icon-192.png, icon-512.png,
icon-maskable-512.png (letter inside the 80% safe circle) and apple-touch-icon.png (180, no transparency).
Run: python tools/make_icons.py"""
import os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'assets', 'icons')
BG = (5, 5, 5)


def fit(logo, size, scale):
    """Logo scaled to `scale` of the canvas, centred on the site background."""
    im = Image.new('RGB', (size, size), BG)
    s = round(size * scale)
    im.paste(logo.resize((s, s), Image.LANCZOS), ((size - s) // 2, (size - s) // 2))
    return im


def quant(im):
    """96-colour palette with the background colour exact (the quantizer lands one step off on near-black)."""
    q = im.quantize(96, Image.Quantize.FASTOCTREE)
    pal = q.getpalette()
    i = min(range(len(pal) // 3), key=lambda k: sum(abs(pal[3 * k + c] - BG[c]) for c in range(3)))
    pal[3 * i:3 * i + 3] = list(BG)
    q.putpalette(pal)
    return q


def main():
    os.makedirs(OUT, exist_ok=True)
    logo = Image.open(os.path.join(ROOT, 'assets', 'logo.png')).convert('RGB')
    for name, size, scale in (('icon-192', 192, 1), ('icon-512', 512, 1), ('icon-maskable-512', 512, .8), ('apple-touch-icon', 180, .9)):
        quant(fit(logo, size, scale)).save(os.path.join(OUT, name + '.png'), optimize=True)  # engraved art: 96 colours keep it sharp at a fraction of the size
        print(name, 'ok')


if __name__ == '__main__':
    main()
