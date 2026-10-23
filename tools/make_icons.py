"""App icons for the installable site (PWA) from the gold G logo: assets/icons/icon-192.png, icon-512.png,
icon-maskable-512.png (letter inside the 80% safe circle) and apple-touch-icon.png (180, no transparency).
Run: python tools/make_icons.py"""
import os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'assets', 'icons')
BG = (10, 11, 13)


def fit(logo, size, scale):
    """Logo scaled to `scale` of the canvas, centred on the site background."""
    im = Image.new('RGB', (size, size), BG)
    s = round(size * scale)
    im.paste(logo.resize((s, s), Image.LANCZOS), ((size - s) // 2, (size - s) // 2))
    return im


def main():
    os.makedirs(OUT, exist_ok=True)
    logo = Image.open(os.path.join(ROOT, 'assets', 'logo.png')).convert('RGB')
    for name, size, scale in (('icon-192', 192, 1), ('icon-512', 512, 1), ('icon-maskable-512', 512, .8), ('apple-touch-icon', 180, .9)):
        fit(logo, size, scale).quantize(96, Image.Quantize.FASTOCTREE).save(os.path.join(OUT, name + '.png'), optimize=True)  # engraved art: 96 colours keep it sharp at a fraction of the size
        print(name, 'ok')


if __name__ == '__main__':
    main()
