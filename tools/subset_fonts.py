"""Site fonts cut down to the characters the built site uses: assets/fonts/<name>.woff2 from tools/fonts-src/<name>.woff2.
Same families, weights, wght axis, hinting and OpenType features (kern, lnum, tnum, frac ...) as the originals;
only glyphs no character of the site reaches are dropped. The @font-face unicode-range groups in index.src.html stay.
Kept per file: (characters of the built pages, scripts and data + their upper/lower case + MARGIN) inside its unicode-range.
tools/fonts-src/subset.json records what each file kept; tests/test_fonts.py checks every site character against it.
Russian and Ukrainian pages take <family>-ru-uk.woff2 instead of -cyrillic: Cyrillic + build.CYR_FONT_CORE in one file
(build.cyr_fonts). The originals in tools/fonts-src are made once by
python tools/subset_fonts.py --ru-uk-sources <GolosText[wght].ttf from github.com/google/fonts, ofl/golostext> (Golos -ru-uk)
python tools/subset_fonts.py --display-sources <SpectralSC-SemiBold.ttf from github.com/google/fonts, ofl/spectralsc>.
Run after python build.py when the test asks for it, then build again (new ?v= on the fonts): python tools/subset_fonts.py
(needs: pip install fonttools brotli)"""
import hashlib, html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'tools', 'fonts-src')
OUT = os.path.join(ROOT, 'assets', 'fonts')
COVER = os.path.join(SRC, 'subset.json')
TEXT = ('.html', '.js', '.json', '.webmanifest', '.css', '.svg', '.txt', '.vtt', '.md', '.xml')
SKIP = {'node_modules', 'tests', 'content', 'i18n', 'fonts-src'}


def _span(a, b):
    return set(range(a, b + 1))


# headroom for text that is not in the build yet: news feed, player and guild names, new translations
MARGIN = (_span(0x20, 0x7E) | _span(0xA0, 0xFF)                                    # ASCII, Latin-1
          | _span(0x100, 0x17F) | {0x192, 0x218, 0x219, 0x21A, 0x21B, 0x2BC}          # Latin Extended-A, Romanian
          | _span(0x410, 0x44F) | {0x401, 0x451, 0x404, 0x454, 0x406, 0x456, 0x407, 0x457, 0x490, 0x491, 0x40E, 0x45E, 0x301}
          | _span(0x2010, 0x2027) | {0x2030, 0x2032, 0x2033, 0x2039, 0x203A, 0x20AC, 0x20BD, 0x2116, 0x2122, 0x2191, 0x2193, 0x2212, 0x2215})


def site_chars(root=ROOT):
    """Every character of the built site: pages, scripts, their texts (JSON and JS escapes decoded) and data,
    with upper and lower case for text-transform."""
    seen = set()
    for d, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if not x.startswith('.') and x not in SKIP]
        for f in files:
            if not f.endswith(TEXT) or '.src.' in f:
                continue
            s = open(os.path.join(d, f), encoding='utf-8', errors='replace').read()
            s = re.sub(r'\\u\{([0-9a-fA-F]{1,6})\}', lambda m: chr(int(m[1], 16)), s)
            s = re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m[1], 16)), s)
            seen |= set(html.unescape(s))
    for ch in list(seen):
        seen |= set(ch.upper()) | set(ch.lower())
    return {ord(c) for c in seen}


def parse_range(rng):
    cps = set()
    for part in rng.split(','):
        a, _, b = part.strip()[2:].partition('-')
        cps |= _span(int(a, 16), int(b or a, 16))
    return cps


def faces(root=ROOT):
    """{file name: set of code points of its unicode-range} from the @font-face rules of index.src.html."""
    css = open(os.path.join(root, 'index.src.html'), encoding='utf-8').read()
    out = {name: parse_range(rng) for name, rng in
           re.findall(r'assets/fonts/([\w-]+\.woff2)\)[^;]*;\s*unicode-range:\s*([^;]+);', css)}
    sys.path.insert(0, root)
    from build import CYR_FONT_CORE
    for name, rng in list(out.items()):
        if name.endswith('-cyrillic.woff2'):
            out[name.replace('-cyrillic', '-ru-uk')] = rng | parse_range(CYR_FONT_CORE)
    return out


def ranges(cps):
    """[[a, b], ...] runs of consecutive code points, for subset.json."""
    out = []
    for c in sorted(cps):
        if out and out[-1][1] == c - 1:
            out[-1][1] = c
        else:
            out.append([c, c])
    return out


def unranges(rs):
    return {c for a, b in rs for c in range(a, b + 1)}


def narrow_axis(font):
    """A variable font (Golos Text, wght 400-900) only for the weights its @font-face rules ask for (font-weight: 400 600
    in index.src.html; a heavier request is clamped to 600 by the browser anyway): the deltas beyond 600 and the vertical
    tables (no vertical text on the site) go, -35% per file; outlines at 400-600 differ from the original by 1 unit of 1000 at most."""
    from fontTools.varLib import instancer
    css = open(os.path.join(ROOT, 'index.src.html'), encoding='utf-8').read()
    lo, hi = map(int, re.search(r'font-family: "Golos Text"; font-style: normal; font-weight: (\d+) (\d+)', css).groups())
    flavor = font.flavor
    font = instancer.instantiateVariableFont(font, {'wght': (lo, hi)}, inplace=False)
    for tag in ('VVAR', 'vhea', 'vmtx'):
        if tag in font:
            del font[tag]
    font.flavor = flavor
    return font


def cut(src, dst, keep):
    from fontTools import subset
    opts = subset.Options()
    opts.flavor = 'woff2'
    opts.layout_features = ['*']                # kern, mark, lnum, tnum, frac, locl ... as in the original
    opts.layout_scripts = ['*']
    opts.name_IDs = ['*']
    opts.name_languages = ['*']
    opts.notdef_outline = True
    opts.hinting = True                         # the display face carries TrueType hinting: Windows draws it with it
    opts.drop_tables = []
    font = subset.load_font(src, opts)
    sub = subset.Subsetter(opts)
    sub.populate(unicodes=sorted(keep))
    sub.subset(font)
    if 'fvar' in font:
        font = narrow_axis(font)
    subset.save_font(font, dst, opts)
    data = open(dst, 'rb').read()
    print(f'{os.path.basename(dst)}: {os.path.getsize(src)} -> {len(data)} bytes, {len(keep)} characters', file=sys.stderr)
    return hashlib.sha1(data).hexdigest()[:10]


# the display face (Spectral SC SemiBold, static) is cut from the upstream TTF into the same files Google Fonts serves:
# one per unicode-range of its @font-face rules, plus -ru-uk. Only titles and big figures use it (22 px and up), so it goes
# without TrueType hinting (no visible change at those sizes, -10 KB) and keeps the features the pages ask for:
# kerning, marks, local forms and lining figures (its default figures are old-style)
DISPLAY = 'spectral-sc'
DISPLAY_FEATURES = ['kern', 'mark', 'mkmk', 'ccmp', 'locl', 'lnum', 'tnum']


def display_sources(ttf):
    """tools/fonts-src/spectral-sc-{cyrillic,latin-ext,latin,ru-uk}.woff2 from SpectralSC-SemiBold.ttf
    (github.com/google/fonts, ofl/spectralsc)."""
    from fontTools import subset
    rngs = {name[len(DISPLAY) + 1:-6]: rng for name, rng in faces().items() if name.startswith(DISPLAY + '-')}
    for part, rng in rngs.items():
        opts = subset.Options()
        opts.flavor = 'woff2'
        opts.layout_features = DISPLAY_FEATURES
        opts.layout_scripts = ['*']
        opts.name_IDs = ['*']
        opts.name_languages = ['*']
        opts.notdef_outline = True
        opts.hinting = False
        opts.drop_tables = ['meta']
        font = subset.load_font(ttf, opts)
        sub = subset.Subsetter(opts)
        sub.populate(unicodes=sorted(rng))
        sub.subset(font)
        subset.save_font(font, os.path.join(SRC, f'{DISPLAY}-{part}.woff2'), opts)


def ru_uk_sources(golos):
    """tools/fonts-src/golos-text-ru-uk.woff2: the -cyrillic and -latin originals as one font. Golos Text is variable,
    which fontTools cannot merge, so it is cut from the upstream font the Google Fonts files are subsets of
    (same outlines), to their characters and features."""
    from fontTools import subset
    from fontTools.ttLib import TTFont
    keep, feats = set(), set()
    for part in ('cyrillic', 'latin'):
        t = TTFont(os.path.join(SRC, f'golos-text-{part}.woff2'))
        keep |= set(t.getBestCmap())
        feats |= {r.FeatureTag for tag in ('GSUB', 'GPOS') for r in t[tag].table.FeatureList.FeatureRecord}
    opts = subset.Options()
    opts.flavor = 'woff2'
    opts.layout_features = sorted(feats)
    opts.layout_scripts = ['*']
    opts.name_IDs = ['*']
    opts.name_languages = ['*']
    opts.notdef_outline = True
    opts.drop_tables = []
    font = subset.load_font(golos, opts)
    sub = subset.Subsetter(opts)
    sub.populate(unicodes=sorted(keep))
    sub.subset(font)
    subset.save_font(font, os.path.join(SRC, 'golos-text-ru-uk.woff2'), opts)


def main():
    from fontTools.ttLib import TTFont
    want = site_chars() | MARGIN
    cover = {}
    for name, rng in sorted(faces().items()):
        src = os.path.join(SRC, name)
        orig = set(TTFont(src).getBestCmap()) & rng
        keep = orig & want
        cover[name] = {'sha': cut(src, os.path.join(OUT, name), keep), 'orig': ranges(orig), 'kept': ranges(keep)}
    with open(COVER, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(cover, f, indent=1)
        f.write('\n')


if __name__ == '__main__':
    if sys.argv[1:2] == ['--ru-uk-sources']:
        ru_uk_sources(sys.argv[2])
    elif sys.argv[1:2] == ['--display-sources']:
        display_sources(sys.argv[2])
    else:
        main()
