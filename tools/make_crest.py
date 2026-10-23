"""Спрайт знаков герба: assets/me/crest/src/<id>.svg (game-icons.net) -> assets/me/crest/charges.svg.
Фон-квадрат game-icons (path M0 0h512v512H0z) и все fill убираются: цвет знака задаёт <use fill>."""
import os, re, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'content'))
import guilds  # noqa: E402

SRC = os.path.join(HERE, 'assets', 'me', 'crest', 'src')
OUT = os.path.join(HERE, 'assets', 'me', 'crest', 'charges.svg')


def paths(svg):
    ds = re.findall(r'<path[^>]*\sd="([^"]+)"', svg)
    return [d for d in ds if not re.fullmatch(r'M0 0h512v512H0z', d.strip())]


def main():
    out = ['<svg xmlns="http://www.w3.org/2000/svg" style="display:none">']
    for cid, _, _ in guilds.CHARGES:
        svg = open(os.path.join(SRC, cid + '.svg'), encoding='utf-8').read()
        ds = paths(svg)
        assert ds, cid
        out.append(f'<symbol id="c-{cid}" viewBox="0 0 512 512"><path d="{" ".join(ds)}"/></symbol>')
    out.append('</svg>')
    open(OUT, 'w', encoding='utf-8', newline='\n').write(''.join(out))
    print(OUT, os.path.getsize(OUT))


if __name__ == '__main__':
    main()
