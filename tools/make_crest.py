"""Спрайт знаков герба: assets/me/crest/src/<id>.svg (game-icons.net) -> assets/me/crest/charges.svg.
Фон-квадрат game-icons (path M0 0h512v512H0z) и все fill убираются: цвет знака задаёт <use fill>.
viewBox каждого знака — квадрат 512 с центром в центре рисунка: в гербе знак стоит ровно по середине формы."""
import os, re, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'content'))
sys.path.insert(0, os.path.join(HERE, 'tools'))
import guilds  # noqa: E402
from svgpath import bbox, paths  # noqa: E402

SRC = os.path.join(HERE, 'assets', 'me', 'crest', 'src')
OUT = os.path.join(HERE, 'assets', 'me', 'crest', 'charges.svg')
def main():
    out = ['<svg xmlns="http://www.w3.org/2000/svg" style="display:none">']
    for cid, _, _ in guilds.CHARGES:
        svg = open(os.path.join(SRC, cid + '.svg'), encoding='utf-8').read()
        ds = paths(svg)
        assert ds, cid
        x0, y0, x1, y1 = [min(b[i] for b in map(bbox, ds)) if i < 2 else max(b[i] for b in map(bbox, ds)) for i in range(4)]
        vx, vy = round((x0 + x1) / 2 - 256, 1) + 0, round((y0 + y1) / 2 - 256, 1) + 0   # + 0: no "-0"
        out.append(f'<symbol id="c-{cid}" viewBox="{vx:g} {vy:g} 512 512"><path d="{" ".join(ds)}"/></symbol>')
    out.append('</svg>')
    open(OUT, 'w', encoding='utf-8', newline='\n').write(''.join(out))
    print(OUT, os.path.getsize(OUT))


if __name__ == '__main__':
    main()
