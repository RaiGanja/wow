"""Урезанные шрифты (tools/subset_fonts.py): в каждом файле есть все символы сайта, которые были в оригинале,
иначе браузер нарисует их системным шрифтом; адреса шрифтов в страницах и sw.js с ?v= текущего файла.
Запуск после python build.py: python tests/test_fonts.py"""
import hashlib, json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import subset_fonts as S  # noqa: E402

FONTS = os.path.join(ROOT, 'assets', 'fonts')
COVER = json.load(open(S.COVER, encoding='utf-8'))
RERUN = 'run python tools/subset_fonts.py, then python build.py'


def sha(name, n=10):
    return hashlib.sha1(open(os.path.join(FONTS, name), 'rb').read()).hexdigest()[:n]


def test_files_are_the_recorded_cuts():
    faces = S.faces()
    assert faces and set(faces) == set(COVER), (sorted(faces), sorted(COVER))
    for name in faces:
        assert os.path.isfile(os.path.join(S.SRC, name)), f'original missing: tools/fonts-src/{name}'
        assert sha(name) == COVER[name]['sha'], f'{name} is not the cut subset.json describes: {RERUN}'
        assert os.path.getsize(os.path.join(FONTS, name)) < os.path.getsize(os.path.join(S.SRC, name)), name


def test_every_site_character_is_kept():
    chars = S.site_chars()
    for name, rng in S.faces().items():
        lost = (chars & rng & S.unranges(COVER[name]['orig'])) - S.unranges(COVER[name]['kept'])
        assert not lost, f'{name} lacks {"".join(sorted(map(chr, lost)))!r}: {RERUN}'


def test_font_addresses_carry_the_file_version():
    rx = re.compile(r'assets/fonts/([\w-]+\.woff2)(\?v=\w+)?')
    files = [os.path.join(ROOT, 'sw.js')]
    for d, dirs, fs in os.walk(ROOT):
        dirs[:] = [x for x in dirs if not x.startswith('.') and x not in ('assets', 'content', 'i18n', 'tests', 'node_modules')]
        files += [os.path.join(d, f) for f in fs if f.endswith('.html') and not f.endswith('.src.html')]
    seen = 0
    for p in files:
        for name, v in rx.findall(open(p, encoding='utf-8').read()):
            if name in COVER:
                assert v == f'?v={sha(name, 8)}', (os.path.relpath(p, ROOT), name, v)
                seen += 1
    assert seen > 1000, seen


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_'):
            fn()
    print('OK')
