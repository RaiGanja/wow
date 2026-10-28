"""Share cards of a built character (race + class + spec, faction from the race): 1200x630, one per combination.
The art is the class x faction portrait (assets/art/<class>-<race>-896.webp, 18 files); the type is the site's
(Spectral SC + Golos Text), rendered by headless Chrome as in make_og.py.

Three looks wait for the choice:
  A  text column on the left, portrait on the right (like the guide cards)
  B  portrait in the middle, text centred under it (safe for the square crop of WhatsApp and Reddit)
  C  no words on the art: the mark, the portrait, the spec slot; the name goes to og:title (one file serves 9 languages)
The talent split (17/34/0) is drawn only when it is given (--pts); without it the line is not drawn at all.
The spec slot holds the first letter of the spec until the spec icons exist (ICON below), then an <img> takes its place.

Run:
  python tools/make_build_cards.py --variants OUT_DIR        three looks on three samples, with and without points
  python tools/make_build_cards.py --variant=A --langs=en [--skip]   one English card per build: assets/og/b/<slug>.jpg (168 files)
  python tools/make_build_cards.py --variant=A [--langs=ru,en] [--only=human-warrior-arms]   the cards into assets/og/b/
                                                             (all 168 x languages; nothing is drawn without --variant)"""
import json, os, re, subprocess, sys, tempfile
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path[:0] = [os.path.join(ROOT, 'content'), ROOT]
import build_guides as BG  # noqa: E402
import build  # noqa: E402
import langs  # noqa: E402
from classes import CLASSES  # noqa: E402
import make_og  # noqa: E402

CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
GAME = json.load(open(os.path.join(ROOT, 'assets', 'game.json'), encoding='utf-8'))
COLOR = build.COLOR
POR = {('warrior', 'alliance'): 'human', ('warrior', 'horde'): 'orc', ('paladin', 'alliance'): 'human', ('paladin', 'horde'): 'undead',
       ('hunter', 'alliance'): 'nightelf', ('hunter', 'horde'): 'orc', ('rogue', 'alliance'): 'nightelf', ('rogue', 'horde'): 'orc',
       ('priest', 'alliance'): 'gnome', ('priest', 'horde'): 'undead', ('shaman', 'alliance'): 'dwarf', ('shaman', 'horde'): 'orc',
       ('mage', 'alliance'): 'gnome', ('mage', 'horde'): 'orc', ('warlock', 'alliance'): 'gnome', ('warlock', 'horde'): 'orc',
       ('druid', 'alliance'): 'nightelf', ('druid', 'horde'): 'tauren'}   # the 18 class x faction portraits
ICON = {}   # spec id -> assets path of its icon, filled after 05.11; empty = the letter
SLUG = {'nightelf': 'nightelf', 'skyA': 'skyborne-a', 'skyH': 'skyborne-h'}   # url part of the race
# the line under the name: what the combination was checked against (game.json, 27.10) / where the points come from
CHECKED = {'ru': 'Сочетание сверено с WoW Forever · 27.10.2026', 'uk': 'Поєднання звірене з WoW Forever · 27.10.2026',
           'en': 'Checked against WoW Forever · 27 Oct 2026', 'de': 'Mit WoW Forever abgeglichen · 27.10.2026',
           'fr': 'Vérifié sur WoW Forever · 27/10/2026', 'es': 'Comprobado en WoW Forever · 27/10/2026',
           'it': 'Verificato su WoW Forever · 27/10/2026', 'pt': 'Conferido no WoW Forever · 27/10/2026',
           'pl': 'Sprawdzone w WoW Forever · 27.10.2026'}
PTS_SRC = {'ru': 'Таланты из ссылки игрока', 'uk': 'Таланти з посилання гравця', 'en': 'Talents from the player link',
           'de': 'Talente aus dem Link', 'fr': 'Talents du lien', 'es': 'Talentos del enlace', 'it': 'Talenti dal link',
           'pt': 'Talentos do link', 'pl': 'Talenty z linku'}


def spec_roles(cls, spec):
    """roles of a spec from the class pages (a '?' role is a guess and stays off the card)"""
    c = next(x for x in CLASSES if x['id'] == cls)
    sp = next(x for x in c['specs'] if re.sub(r'\W+', '-', x['en'].lower()) == spec)
    return [r for r in sp['roles'] if not r.endswith('?')]


# og:description: what the player gets from the link (role, side, what is inside); no date
DESC = {'ru': '{spec} · {role}. {fac}. Сочетание проверено по WoW Forever; таланты, прокачка и расы класса в подборщике Gabella.',
        'uk': '{spec} · {role}. {fac}. Поєднання перевірено за WoW Forever; таланти, прокачування й раси класу в підбірнику Gabella.',
        'en': '{spec} · {role}. {fac}. The combination is checked against WoW Forever; talents, leveling and the class races in the Gabella picker.',
        'de': '{spec} · {role}. {fac}. Kombination mit WoW Forever abgeglichen; Talente, Leveln und Klassenvölker im Gabella-Auswahltool.',
        'fr': '{spec} · {role}. {fac}. Combinaison vérifiée sur WoW Forever ; talents, leveling et races de la classe dans le sélecteur Gabella.',
        'es': '{spec} · {role}. {fac}. Combinación comprobada en WoW Forever; talentos, nivelación y razas de la clase en el selector de Gabella.',
        'it': '{spec} · {role}. {fac}. Combinazione verificata su WoW Forever; talenti, livellamento e razze della classe nel selettore Gabella.',
        'pt': '{spec} · {role}. {fac}. Combinação conferida no WoW Forever; talentos, evolução e raças da classe no seletor da Gabella.',
        'pl': '{spec} · {role}. {fac}. Zestaw sprawdzony w WoW Forever; talenty, levelowanie i rasy klasy w selektorze Gabella.'}


def role_line(cls, spec, lang):
    return make_og.JOIN.join(make_og.ROLES[lang][r] for r in spec_roles(cls, spec))


def names(lang):
    h = BG.hero_core(lang)
    return h


def title(lang, race, cls, N):
    """Race + class the way the language says it: «Человек-воин», «Human Warrior», «Mensch · Krieger»."""
    r, c = N['rn'][race], N['cn'][cls]
    if lang in ('ru', 'uk'):
        return f'{r}-{c[0].lower() + c[1:]}'
    if lang == 'en':
        return f'{r} {c}'
    return f'{r} · {c}'


def combos():
    """(race, class, spec) for every combination Forever has (game.json): 56 x 3 = 168."""
    sid = BG.HERO.SPEC_IDS
    for race, r in GAME['races'].items():
        for cls in r['cls']:
            for spec in sid[cls]:
                yield race, cls, spec


def slug(race, cls, spec):
    return f'{SLUG.get(race, race)}-{cls}-{spec}'


def url(path):
    return 'file:///' + os.path.join(ROOT, path).replace('\\', '/')


FONTS = ''.join(
    f'@font-face{{font-family:"{fam}";font-weight:400 700;src:url({url("assets/fonts/" + f)}) format("woff2");unicode-range:{rng}}}'
    for fam, base in (('Spectral SC', 'spectral-sc'), ('Golos Text', 'golos-text'))
    for f, rng in ((base + '-cyrillic.woff2', 'U+0400-045F,U+0490-0491,U+04B0-04B1,U+2116'), (base + '-latin-ext.woff2', 'U+0100-02BA,U+1E00-1E9F'),
                   (base + '-latin.woff2', 'U+0000-00FF,U+2000-206F')))

BASE = f'''{FONTS}
*{{margin:0;box-sizing:border-box}}
body{{width:1200px;height:630px;overflow:hidden;background:#050505;position:relative;font-family:"Golos Text";color:#efe9da;font-variant-numeric:lining-nums}}
img{{display:block}}
.slot{{width:64px;height:64px;border-radius:50%;border:2px solid var(--cc);display:grid;place-items:center;flex:none;
  font:600 34px/1 "Spectral SC";color:var(--cc);background:#0b0b0b;overflow:hidden}}
.slot img{{width:100%;height:100%;object-fit:cover}}
.pts{{font:600 44px/1 "Golos Text";color:var(--cc);letter-spacing:.02em;font-variant-numeric:lining-nums tabular-nums}}
.pts i{{font-style:normal;color:#6f6858;padding:0 .18em}}
.foot{{position:absolute;bottom:44px;font-size:26px;color:#8f877a;display:flex;gap:18px;align-items:center}}
.foot b{{font:600 24px/1 "Spectral SC";color:#c9a54a;letter-spacing:.04em}}
'''


def slot(spec, sn, cc):
    ico = ICON.get(spec)
    inner = f'<img src="{url(ico)}" alt="">' if ico else sn[0]
    return f'<div class="slot" style="--cc:{cc}">{inner}</div>'


def pts_html(pts):
    return '<i>/</i>'.join(str(p) for p in pts)


def page_a(d):
    """A: text column left, portrait right."""
    pts = f'<div class="pts">{pts_html(d["pts"])}</div>' if d['pts'] else ''
    src = PTS_SRC[d['lang']] if d['pts'] else ''
    return f'''<!doctype html><meta charset="utf-8"><style>{BASE}
.por{{position:absolute;right:0;top:0;height:630px;width:720px;object-fit:cover;object-position:50% 18%;
  -webkit-mask-image:linear-gradient(90deg,transparent 0%,#000 50%)}}
.shade{{position:absolute;inset:0;background:linear-gradient(0deg,rgba(5,5,5,.9) 0%,rgba(5,5,5,0) 30%)}}
.brand{{position:absolute;left:72px;top:52px;display:flex;align-items:center;gap:20px;font:600 44px/1 "Spectral SC";letter-spacing:.05em}}
.brand img{{width:88px;height:88px;border-radius:50%}}
.txt{{position:absolute;left:72px;top:190px;width:640px;display:flex;flex-direction:column;gap:22px}}
h1{{font:600 76px/1.02 "Spectral SC";letter-spacing:.01em;text-wrap:balance}}
.spec{{display:flex;align-items:center;gap:18px;font:600 40px/1 "Spectral SC";color:#c9a54a}}
.fac{{font-size:28px;color:#a59d8c;letter-spacing:.02em}}
.rule{{width:84px;height:3px;background:var(--cc)}}
.foot{{left:72px}}
</style><body style="--cc:{d['cc']}"><img class="por" src="{url(d['por'])}"><div class="shade"></div>
<div class="brand"><img src="{url('assets/logo.png')}" alt="">Gabella</div>
<div class="txt"><div class="rule"></div><h1>{d['title']}</h1>
<div class="spec">{slot(d['spec'], d['sn'], d['cc']) if ICON.get(d['spec']) else ''}{d['sn']}</div>{pts}<div class="fac">{d['role']} · {d['fac']}</div></div>
<div class="foot"><b>gabella.site</b><span>{src}</span></div></body>'''


def page_b(d):
    """B: portrait in the middle third (survives a square crop), name centred under the face."""
    pts = f'<div class="pts">{pts_html(d["pts"])}</div>' if d['pts'] else ''
    src = PTS_SRC[d['lang']] if d['pts'] else CHECKED[d['lang']]
    return f'''<!doctype html><meta charset="utf-8"><style>{BASE}
.bg{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:brightness(.35) blur(2px)}}
.por{{position:absolute;left:300px;top:-40px;width:600px;height:800px;object-fit:cover;object-position:50% 0;
  -webkit-mask-image:linear-gradient(90deg,transparent,#000 24%,#000 76%,transparent)}}
.shade{{position:absolute;inset:0;background:linear-gradient(0deg,#050505 0%,rgba(5,5,5,.94) 30%,rgba(5,5,5,0) 62%),
  linear-gradient(90deg,#050505 0%,rgba(5,5,5,.2) 30%,rgba(5,5,5,.2) 70%,#050505 100%)}}
.brand{{position:absolute;left:56px;top:48px;width:48px;height:48px}}
.txt{{position:absolute;left:0;right:0;bottom:96px;display:flex;flex-direction:column;align-items:center;gap:16px;text-align:center}}
h1{{font:600 68px/1.02 "Spectral SC";letter-spacing:.01em;max-width:1000px}}
.spec{{display:flex;align-items:center;gap:16px;font:600 34px/1 "Spectral SC";color:#c9a54a}}
.spec .slot{{width:52px;height:52px;font-size:28px}}
.spec span{{color:#a59d8c;font:400 24px/1 "Golos Text"}}
.foot{{left:0;right:0;justify-content:center;bottom:36px;font-size:24px}}
.side{{position:absolute;top:0;bottom:0;width:4px;background:var(--cc);opacity:.9}}
</style><body style="--cc:{d['cc']}"><img class="bg" src="{url(d['bg'])}"><img class="por" src="{url(d['por'])}"><div class="shade"></div>
<img class="brand" src="{url('assets/logo.png')}" alt=""><div class="side" style="left:0"></div>
<div class="txt"><h1>{d['title']}</h1><div class="spec">{slot(d['spec'], d['sn'], d['cc'])}{d['sn']}<span>· {d['fac']}</span></div>{pts}</div>
<div class="foot"><b>gabella.site</b><span>{src}</span></div></body>'''


def page_c(d):
    """C: no words: the mark, the portrait, the spec slot, a class-colour rule; digits only when points are given."""
    pts = f'<div class="pts">{pts_html(d["pts"])}</div>' if d['pts'] else ''
    return f'''<!doctype html><meta charset="utf-8"><style>{BASE}
.por{{position:absolute;right:0;top:0;height:630px;width:760px;object-fit:cover;object-position:50% 15%;
  -webkit-mask-image:linear-gradient(90deg,transparent 0%,#000 34%)}}
.shade{{position:absolute;inset:0;background:radial-gradient(ellipse at 72% 40%,rgba(5,5,5,0) 30%,rgba(5,5,5,.55) 80%)}}
.mark{{position:absolute;left:96px;top:155px;width:260px;height:260px}}
.col{{position:absolute;left:96px;top:450px;display:flex;align-items:center;gap:32px}}
.rule{{position:absolute;left:96px;top:118px;width:260px;height:3px;background:var(--cc)}}
.site{{position:absolute;left:96px;bottom:44px;font:600 24px/1 "Spectral SC";color:#c9a54a;letter-spacing:.05em}}
</style><body style="--cc:{d['cc']}"><img class="por" src="{url(d['por'])}"><div class="shade"></div>
<div class="rule"></div><img class="mark" src="{url('assets/logo.png')}" alt="">
<div class="col">{slot(d['spec'], d['sn'], d['cc'])}{pts}</div><div class="site">gabella.site</div></body>'''


PAGES = {'A': page_a, 'B': page_b, 'C': page_c}


def portrait_for(race, cls):
    """(portrait, backdrop) of a card: the race the caption names, never another one (a dwarf hunter drew a night elf, 28.10).
    Only a painting named <class>-<race> with the same race may stand for the class; otherwise the portrait of the race itself.
    A race without a portrait of its own stops the run. The best race of a side (build.portraits) is not used here."""
    rs = GAME['races'][race]['slug']
    both = f'assets/art/{cls}-{race}-896.webp'
    por, bg = (both, both.replace('-896', '-bg')) if os.path.isfile(os.path.join(ROOT, both)) else (f'assets/art/{rs}-896.webp', f'assets/art/{rs}-bg.webp')
    assert os.path.isfile(os.path.join(ROOT, por)) and os.path.isfile(os.path.join(ROOT, bg)), f'{race}: no portrait of its own ({por})'
    return por, bg


def portrait_race(path):
    """The race a portrait file shows, from its name: 'dwarf-896.webp' -> 'dwarf', 'hunter-nightelf-896.webp' -> 'nightelf', a class alone -> None."""
    n = os.path.basename(path).rsplit('-', 1)[0]
    ids = {r['slug']: rid for rid, r in GAME['races'].items()}
    if n in ids:
        return ids[n]
    r = n.partition('-')[2]
    return r if r in GAME['races'] else None


def data(race, cls, spec, lang, pts=None):
    N = names(lang)
    fac = GAME['races'][race]['f']
    i = N['sid'][cls].index(spec)
    por, bg = portrait_for(race, cls)
    return {'lang': lang, 'race': race, 'cls': cls, 'spec': spec, 'title': title(lang, race, cls, N), 'sn': N['sn'][cls][i],
            'fac': N['fn'][fac], 'cc': COLOR[cls], 'pts': pts, 'role': role_line(cls, spec, lang), 'por': por, 'bg': bg}


def og_text(race, cls, spec, lang):
    """og:title / og:description of the page (the words that C leaves off the art)."""
    N = names(lang)
    i = N['sid'][cls].index(spec)
    fac = N['fn'][GAME['races'][race]['f']]
    return (f'{title(lang, race, cls, N)} · {N["sn"][cls][i]}',
            DESC[lang].format(spec=N['sn'][cls][i], role=role_line(cls, spec, lang), fac=fac))


def chrome(src, *args):
    return subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files',
                           '--force-device-scale-factor=1', '--window-size=1200,630', '--virtual-time-budget=3000', *args,
                           'file:///' + src.replace('\\', '/')], check=True, capture_output=True)


def shoot(page, out, png=False, size=(1200, 630)):
    with tempfile.TemporaryDirectory() as tmp:
        src, shot = os.path.join(tmp, 'c.html'), os.path.join(tmp, 'c.png')
        with open(src, 'w', encoding='utf-8') as f:
            f.write(page)
        args = [] if size == (1200, 630) else [f'--window-size={size[0]},{size[1]}']
        chrome(src, f'--screenshot={shot}', *args)
        im = Image.open(shot).convert('RGB')
        if png:
            im.save(out)
        else:
            im.save(out, quality=70, optimize=True, progressive=True)   # 70: ~50 KB a card, 168 cards of C ~8 MB


SAMPLES = [('human', 'warrior', 'arms', (31, 20, 0)), ('orc', 'shaman', 'enhancement', (0, 31, 20)), ('nightelf', 'druid', 'feral', (14, 32, 5))]


def variants(out):
    os.makedirs(out, exist_ok=True)
    made = {}
    for v, fn in PAGES.items():
        for race, cls, spec, pts in SAMPLES:
            for state, p in (('', None), ('-pts', pts)):
                name = f'{v}-{slug(race, cls, spec)}{state}'
                d = data(race, cls, spec, 'ru', p)
                shoot(fn(d), os.path.join(out, name + '.png'), png=True)
                shoot(fn(d), os.path.join(out, name + '.jpg'))   # the weight the site would carry
                made[name] = (os.path.getsize(os.path.join(out, name + '.jpg')), og_text(race, cls, spec, 'ru'))
                print(name, made[name][0])
    sheet(out, made)
    return made


def sheet(out, made):
    """variants.png: per look three cards (state before 05.11), one card with points (mock-up), and how one card reads
    in Discord, Telegram, X, WhatsApp and Reddit at their real preview sizes (imitations of the chat apps)."""
    u = lambda n: 'file:///' + os.path.join(out, n + '.png').replace('\\', '/')
    rows = ''
    label = {'A': 'A · колонка слева, портрет справа', 'B': 'B · портрет в центре, имя под ним',
             'C': 'C · без слов: знак, портрет, слот спека (имя только в заголовке ссылки)'}
    for v in PAGES:
        s0 = f'{v}-{slug(*SAMPLES[0][:3])}'
        t, dsc = made[s0][1]
        cards = ''.join(f'<figure><img src="{u(f"{v}-{slug(*s[:3])}")}"><figcaption>{slug(*s[:3])} · без очков · {made[f"{v}-{slug(*s[:3])}"][0] // 1024} КБ</figcaption></figure>' for s in SAMPLES)
        cards += f'<figure class="mock"><img src="{u(s0 + "-pts")}"><figcaption>МАКЕТ: с очками (после 05.11, только если очки есть в ссылке)</figcaption></figure>'
        prev = f'''<div class="dc"><div class="dcs">gabella.site</div><div class="dct">{t}</div><div class="dcd">{dsc}</div><img src="{u(s0)}"></div>
<div class="tg"><div class="tgs">Gabella</div><div class="tgt">{t}</div><div class="tgd">{dsc}</div><img src="{u(s0)}"></div>
<div class="x"><img src="{u(s0)}"><span>gabella.site</span></div>
<div class="wa"><div class="wai" style="background-image:url({u(s0)})"></div><div><b>{t}</b><br>{dsc}<br><span>gabella.site</span></div></div>
<div class="rd"><div class="rdi" style="background-image:url({u(s0)})"></div><span>Reddit, миниатюра 140</span></div>'''
        rows += f'<section><h2>{label[v]}</h2><div class="cards">{cards}</div><div class="prev">{prev}</div></section>'
    html = f'''<!doctype html><meta charset="utf-8"><style>{FONTS}
*{{margin:0;box-sizing:border-box}}body{{width:2400px;background:#111;color:#ddd;font:20px/1.35 "Golos Text";padding:40px}}
h1{{font:600 40px "Spectral SC";color:#c9a54a;margin-bottom:8px}}.note{{color:#999;margin-bottom:30px}}
section{{border-top:1px solid #333;padding:28px 0}}h2{{font:600 34px "Spectral SC";color:#efe9da;margin-bottom:18px}}
.cards{{display:flex;gap:20px}}figure{{width:570px}}figure img{{width:570px;display:block;border:1px solid #333}}
figcaption{{font-size:17px;color:#999;margin-top:6px}}.mock img{{outline:4px dashed #c9a54a;outline-offset:-4px}}.mock figcaption{{color:#c9a54a;font-weight:600}}
.prev{{display:flex;gap:28px;margin-top:22px;align-items:flex-start}}
.dc{{width:432px;background:#2b2d31;border-left:4px solid #c9a54a;border-radius:4px;padding:12px 16px 16px;font:15px/1.3 sans-serif}}
.dcs{{font-size:12px;color:#b5bac1}}.dct{{color:#00a8fc;font-weight:700;margin:4px 0}}.dcd{{color:#dbdee1;font-size:14px;margin-bottom:10px}}
.dc img{{width:400px;border-radius:4px;display:block}}
.tg{{width:380px;background:#182533;border-radius:10px;padding:8px 10px 10px;border-left:3px solid #6ab3f3;font:14px/1.3 sans-serif}}
.tgs{{color:#6ab3f3;font-weight:700}}.tgt{{color:#fff;font-weight:700}}.tgd{{color:#ccc;margin-bottom:6px}}.tg img{{width:356px;border-radius:6px;display:block}}
.x{{width:506px;position:relative}}.x img{{width:506px;border-radius:16px;border:1px solid #333;display:block}}
.x span{{position:absolute;left:12px;bottom:12px;background:rgba(0,0,0,.77);color:#fff;font:13px sans-serif;padding:2px 6px;border-radius:4px}}
.wa{{width:330px;display:flex;gap:8px;background:#1d2c33;border-radius:8px;padding:6px;font:13px/1.3 sans-serif;color:#e9edef}}
.wai{{width:84px;height:84px;flex:none;border-radius:6px;background-size:cover;background-position:center}}
.wa span{{color:#8696a0}}.rd{{font:13px sans-serif;color:#999}}
.rdi{{width:140px;height:140px;border-radius:8px;background-size:cover;background-position:center;margin-bottom:6px}}
</style><body><h1>Карточка собранного персонажа · варианты A / B / C</h1>
<div class="note">1200×630. Пример: ru. Под каждым вариантом: Discord (400 px), Telegram (356 px), X (506 px), WhatsApp (84 px, обрезка в квадрат), Reddit (140 px, квадрат) — имитация вида чатов. Очки 31/20/0 и т. п. — только МАКЕТ: до 05.11 строка не рисуется.</div>
{rows}</body>'''
    with tempfile.TemporaryDirectory() as tmp:
        src, shot = os.path.join(tmp, 's.html'), os.path.join(tmp, 's.png')
        with open(src, 'w', encoding='utf-8') as f:
            f.write(html)
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files',
                        '--force-device-scale-factor=1', '--window-size=2400,2620', '--virtual-time-budget=4000',
                        f'--screenshot={shot}', 'file:///' + src.replace('\\', '/')], check=True, capture_output=True)
        Image.open(shot).convert('RGB').save(os.path.join(out, 'variants.png'))


def main():
    args = sys.argv[1:]
    if '--variants' in args:
        variants(args[args.index('--variants') + 1])
        return
    v = next((a[10:] for a in args if a.startswith('--variant=')), None)
    if v not in PAGES:
        raise SystemExit('name the look: --variant=A|B|C (or --variants OUT_DIR for the samples)')
    pick = next((a[8:].split(',') for a in args if a.startswith('--langs=')), langs.LANGS)
    only = next((set(a[7:].split(',')) for a in args if a.startswith('--only=')), None)
    os.makedirs(os.path.join(ROOT, 'assets', 'og', 'b'), exist_ok=True)
    total = 0
    for race, cls, spec in combos():
        s = slug(race, cls, spec)
        if only and s not in only:
            continue
        for lang in (['xx'] if v == 'C' else pick):      # C has no words: one file for all languages
            out = os.path.join(ROOT, 'assets', 'og', 'b', f'{s}.jpg' if v == 'C' else f'{s}-{lang}.jpg')   # A: one card per language
            if '--skip' in args and os.path.exists(out):
                total += os.path.getsize(out)
                continue
            shoot(PAGES[v](data(race, cls, spec, 'en' if lang == 'xx' else lang)), out)
            total += os.path.getsize(out)
    print(f'{total / 1048576:.1f} MB')


if __name__ == '__main__':
    main()
