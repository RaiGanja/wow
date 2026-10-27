"""Official Blizzard post (forum cooked HTML or a worldofwarcraft.blizzard.com article) -> structured list of changes.

Each change is one leaf bullet with its path of headings: ['Racial Abilities and Traits', 'Tauren'] or ['Classes', 'Druid', 'Feral'].
For every change: subject (race / class / spec), ability names, numbers with their old values, the kind of change.
Only stdlib; the text itself is not stored by the watcher (copyright): it keeps the structured fields and a hash of each line.

    python tools/news_parse.py <post.html | topic.json [post_number]>   - print the changes of one post"""
import hashlib, html, json, os, re, sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RACES = {'human': 'human', 'humans': 'human', 'dwarf': 'dwarf', 'dwarves': 'dwarf', 'night elf': 'nightelf', 'night elves': 'nightelf',
         'gnome': 'gnome', 'gnomes': 'gnome', 'skyborne': 'skyborne', 'orc': 'orc', 'orcs': 'orc', 'undead': 'undead',
         'forsaken': 'undead', 'tauren': 'tauren', 'troll': 'troll', 'trolls': 'troll'}
CLASSES = ['warrior', 'paladin', 'hunter', 'rogue', 'priest', 'shaman', 'mage', 'warlock', 'druid']
SPECS = {'warrior': ['arms', 'fury', 'protection'], 'paladin': ['holy', 'protection', 'retribution'],
         'hunter': ['beast mastery', 'marksmanship', 'survival'], 'rogue': ['assassination', 'combat', 'subtlety'],
         'priest': ['discipline', 'holy', 'shadow'], 'shaman': ['elemental', 'enhancement', 'restoration'],
         'mage': ['arcane', 'fire', 'frost'], 'warlock': ['affliction', 'demonology', 'destruction'],
         'druid': ['balance', 'feral', 'restoration']}
BLOCK = {'p', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'div', 'blockquote', 'table', 'tr', 'td', 'th'}
UNITS = [(r'%', '%'), (r'percent', '%'), (r'seconds?|secs?|s\b', 's'), (r'minutes?|mins?', 'min'), (r'hours?|hrs?', 'h'),
         (r'yards?|yds?', 'yd'), (r'stacks?', 'stack'), (r'charges?', 'charge'), (r'ranks?', 'rank'), (r'points?', 'pt')]
NUM = re.compile(r'(?<![\w.])(\d+(?:[.,]\d+)?)(?:\s*(%|percent\b|seconds?\b|secs?\b|s\b|minutes?\b|mins?\b|hours?\b|hrs?\b|yards?\b|yds?\b|stacks?\b|charges?\b|ranks?\b|points?\b))?', re.I)
WAS = re.compile(r'\((?:was|previously|from)\s+([^)]*)\)', re.I)
FROM_TO = re.compile(r'\bfrom\s+(\d+(?:\.\d+)?)\s*([%a-z]*)\s+to\s+(\d+(?:\.\d+)?)\s*([%a-z]*)', re.I)


class Node:
    def __init__(self, tag, parent=None):
        self.tag, self.parent, self.kids = tag, parent, []

    def text(self, deep=True):
        out = []
        for k in self.kids:
            if isinstance(k, str):
                out.append(k)
            elif deep or k.tag not in ('ul', 'ol'):
                out.append(k.text(deep) + (' ' if k.tag in BLOCK else ''))
        return re.sub(r'\s+', ' ', ''.join(out)).strip()

    def own_text(self):
        """Text of a list item without its nested lists: the heading of a group like <li><strong>Tauren</strong><ul>…"""
        return self.text(deep=False)

    def blocks(self, tags):
        return [k for k in self.kids if not isinstance(k, str) and k.tag in tags]


class _Tree(HTMLParser):
    VOID = {'br', 'img', 'hr', 'meta', 'link', 'input', 'source', 'wbr'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = self.cur = Node('root')
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.skip += 1
            return
        if tag in self.VOID:
            if tag == 'br':
                self.cur.kids.append(' ')
            return
        if tag == 'a' and dict(attrs).get('class') == 'anchor':    # Discourse heading anchors: empty, keep out of the text
            n = Node('a-anchor', self.cur)
        else:
            n = Node(tag, self.cur)
        self.cur.kids.append(n)
        self.cur = n

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.skip = max(0, self.skip - 1)
            return
        n = self.cur
        while n is not self.root and n.tag != tag and not (tag == 'a' and n.tag == 'a-anchor'):
            n = n.parent
        if n is not self.root:
            self.cur = n.parent

    def handle_data(self, data):
        if not self.skip:
            self.cur.kids.append(data)


def tree(src):
    p = _Tree()
    p.feed(src or '')
    p.close()
    return p.root


def plain(src):
    """Visible text of an HTML fragment, one block per line: used for the hash and for the number check."""
    lines = []

    def walk(n):
        buf = []
        for k in n.kids:
            if isinstance(k, str):
                buf.append(k)
            elif k.tag in BLOCK:
                if ''.join(buf).strip():
                    lines.append(re.sub(r'\s+', ' ', ''.join(buf)).strip())
                buf = []
                walk(k)
            else:
                buf.append(k.text())
        if ''.join(buf).strip():
            lines.append(re.sub(r'\s+', ' ', ''.join(buf)).strip())
    walk(tree(src))
    return '\n'.join(lines)


def digest(src):
    """sha256 of the normalized visible text: markup-only edits (anchors, classes) do not count as a new version."""
    return hashlib.sha256(plain(src).encode('utf-8')).hexdigest()


def norm(s):
    s = html.unescape(s or '').replace('’', "'").replace('‘', "'").replace('–', '-').replace('—', '-').lower()
    s = re.sub(r'[-_/]', ' ', s)
    s = re.sub(r"[^\w' !]+", ' ', s)
    s = re.sub(r'^the\s+', '', s.strip())
    return re.sub(r'\s+', ' ', s).strip()


def unit(u):
    u = (u or '').strip().lower()
    for pat, name in UNITS:
        if u and re.fullmatch(pat, u):
            return name
    return ''


def numbers(text):
    """[(value, unit)] of every number in the text; 4 minutes and 240 seconds stay as written (no conversion)."""
    out = []
    for m in NUM.finditer(text or ''):
        v = float(m.group(1).replace(',', '.'))
        out.append((int(v) if v.is_integer() else v, unit(m.group(2))))
    return out


def pairs(text):
    """Old -> new values: 'to 1% (was 2%)', 'by 10% (was 5%)', 'from 2 minutes to 90 seconds'. Unit of the old value falls back to the new one."""
    out = []
    for m in WAS.finditer(text):
        before = text[:m.start()]
        new = numbers(before[-80:])
        old = numbers(m.group(1))
        if new and old:
            nv, nu = new[-1]
            ov, ou = old[0]
            if nv == ov and (nu or ou) == (ou or nu):
                continue
            out.append({'new': nv, 'old': ov, 'unit': nu or ou, 'old_unit': ou or nu})
    for m in FROM_TO.finditer(text):
        ov, ou = numbers(m.group(1) + m.group(2))[0]
        nv, nu = numbers(m.group(3) + m.group(4))[0]
        out.append({'new': nv, 'old': ov, 'unit': nu or ou, 'old_unit': ou or nu})
    return out


def kind(text):
    t = text.lower()
    if re.match(r'\s*(added|new)\b', t) or re.search(r'\bre-?added\b', t):
        return 'added'
    if re.search(r'\bremoved\b', t) and not re.search(r'\bno longer removed\b', t):
        return 'removed'
    if re.search(r'\breplaced with\b', t):
        return 'replaced'
    if re.search(r'\bno longer\b', t):
        return 'no_longer'
    if pairs(text) or re.search(r'\b(increased|reduced|decreased|lowered|raised|now)\b', t):
        return 'changed'
    if re.search(r'\b(fixed|resolved|bug)\b', t):
        return 'fix'
    return 'note'


def subject(path):
    """Race / class / spec from the headings above a bullet (nearest wins for race; class + spec when both are there)."""
    race = cls = spec = None
    for comp in path:
        c = norm(comp)
        if c in RACES:
            race = RACES[c]
        elif c in CLASSES:
            cls = c
        elif cls and c in SPECS.get(cls, []):
            spec = c
    if race and not cls:
        return {'type': 'race', 'id': race}
    if cls:
        return {'type': 'class', 'id': cls, **({'spec': spec} if spec else {})}
    return {'type': 'general'}


_NAMES = None


def known_names():
    """English names the site knows: i18n/names.json keys, talents of content/talents/*.json, extra names from tools/news_sources.json."""
    global _NAMES
    if _NAMES is None:
        names = set(json.load(open(os.path.join(ROOT, 'i18n', 'names.json'), encoding='utf-8')))
        tdir = os.path.join(ROOT, 'content', 'talents')
        for f in os.listdir(tdir) if os.path.isdir(tdir) else []:
            if f.endswith('.json'):
                for tr in json.load(open(os.path.join(tdir, f), encoding='utf-8')).get('trees', []):
                    names |= {t['n']['en'] for t in tr.get('talents', []) if t.get('n', {}).get('en')}
        src = os.path.join(ROOT, 'tools', 'news_sources.json')
        if os.path.exists(src):
            names |= set(json.load(open(src, encoding='utf-8')).get('names', []))
        _NAMES = sorted((n for n in names if len(n) > 3), key=len, reverse=True)
    return _NAMES


SKIP = {'fixed', 'resolved', 'the', 'a', 'an', 'horde', 'alliance', "developers' notes", "developer's notes", 'developers notes', 'pets', 'wands',
        'creatures', 'players', 'arrows', 'healing reduction', 'using', 'while', 'when', 'it', 'this', 'these', 'all', 'multiple instances',
        'cooldown', 'duration', 'range', 'mana cost', 'cast time', 'damage', 'healing', 'threat',
        'warriors', 'paladins', 'hunters', 'rogues', 'priests', 'shamans', 'mages', 'warlocks', 'druids', 'casters'}
LEAD = re.compile(r"^(?:[Aa]dded:\s*)?([A-Z][\w'’!]*(?:[ -](?:of|the|to|on|[A-Z][\w'’!]*))*)\s*(?::|-\s|\(|\s(?i:now|no longer|bonus|removed|re-added|is|cooldown|has|will|can|also|duration|damage|replaced|increased|reduced|chance)\b)")


def abilities(text, path=()):
    """Ability names in a bullet: the lead name ('Plainsrunning now…', 'Endurance: …', 'Added: Artisan’s Precision - …')
    plus any name the site knows (longest first, no overlaps). Race and class words are not abilities."""
    found, taken = [], []
    lead = LEAD.match(text.strip())
    skip = set(RACES) | set(CLASSES) | {n for s in SPECS.values() for n in s} | SKIP
    if lead and norm(lead.group(1)) not in skip and not norm(lead.group(1)).startswith(('fixed', 'resolved', 'using', 'while', 'when', 'it ')):
        found.append(lead.group(1).strip())
        taken.append((0, len(lead.group(1))))
    for n in known_names():     # case-sensitive: 'Regeneration' (troll racial) is a name, 'regeneration' is a word
        for m in re.finditer(r'(?<![\w])' + re.escape(n) + r'(?![\w])', text):
            if any(a < m.end() and m.start() < b for a, b in taken):
                continue
            if norm(n) in skip:
                continue
            found.append(text[m.start():m.end()])
            taken.append((m.start(), m.end()))
    seen, out = set(), []
    for f in found:
        if norm(f) not in seen:
            seen.add(norm(f))
            out.append(f)
    return out


def changes(src):
    """Leaf bullets (and plain paragraphs under a heading) of a post, with their heading path."""
    root = tree(src)
    out = []
    heads = []          # (level, text) of h1..h6 and bold-only paragraphs, the latter count as level 7

    def add(text, path):
        text = re.sub(r'\s+', ' ', text).strip()
        if not text or len(text) < 8:
            return
        names = abilities(text, path)
        if not names:   # 'Duration reduced to 6 seconds' under <li>Scatter Shot<ul>: the ability is the nearest group below the subject
            subj_words = set(RACES) | set(CLASSES) | {n for s in SPECS.values() for n in s}
            tail = []
            for comp in reversed(path):
                if norm(comp) in subj_words:
                    break
                tail.append(comp)
            if tail and len(tail) < len(path):
                names = [tail[0]]
        out.append({'path': list(path), 'text': text, 'subject': subject(path), 'abilities': names,
                    'kind': kind(text), 'pairs': pairs(text), 'numbers': numbers(text),
                    'h': hashlib.sha1(norm(text).encode('utf-8')).hexdigest()[:12]})

    def walk_list(lst, path):
        for li in lst.blocks(('li',)):
            sub = li.blocks(('ul', 'ol'))
            inner = [k for k in li.kids if not isinstance(k, str) and k.tag == 'p']
            own = li.own_text()
            if sub:
                label = own.rstrip(':').strip()
                is_label = len(label) <= 60 and not re.search(r'[.!]\s*$', label) and not pairs(label)
                if is_label:
                    for s in sub:
                        walk_list(s, path + [label])
                else:           # a real change with sub-notes (developers' notes): one item, the notes stay out
                    add(own, path)
                    for s in sub:
                        walk_list(s, path + [own[:60]])
            elif inner and not own.strip():
                add(li.text(), path)
            else:
                add(own, path)

    def walk(n):
        for k in n.kids:
            if isinstance(k, str):
                continue
            if re.fullmatch(r'h[1-6]', k.tag):
                lvl = int(k.tag[1])
                while heads and heads[-1][0] >= lvl:
                    heads.pop()
                heads.append((lvl, k.text()))
            elif k.tag == 'p':
                t = k.text()
                strong = [c for c in k.kids if not isinstance(c, str) and c.tag in ('strong', 'b')]
                if strong and norm(''.join(c.text() for c in strong)) == norm(t) and len(t) <= 80:
                    while heads and heads[-1][0] >= 7:
                        heads.pop()
                    heads.append((7, t.rstrip(':')))
                elif heads and not re.search(r"developers?['’] notes", t, re.I):
                    add(t, [h for _, h in heads])
            elif k.tag in ('ul', 'ol'):
                walk_list(k, [h for _, h in heads])
            elif k.tag in ('div', 'section', 'article', 'blockquote', 'details'):
                walk(k)
    walk(root)
    # developers' notes and pure fixes without numbers are context, not changes to facts: keep them, the checker skips them
    for c in out:
        if re.match(r"developers?['’] notes", c['text'], re.I):
            c['kind'] = 'note'
    return out


def structured(items):
    """What the watcher stores: the facts of each change line (the bullet itself, its numbers, old -> new) and the line hash.
    Only the list of changes is kept, never the prose around it: the cloud editor cannot open the Blizzard forum
    (403 from its proxy), so the facts travel with the event; the site itself never shows these lines."""
    return [{'path': c['path'], 'subject': c['subject'], 'abilities': c['abilities'], 'kind': c['kind'], 'pairs': c['pairs'],
             'nums': sorted({v for v, _ in c['numbers']}, key=float), 'text': c['text'], 'h': c['h']}
            for c in items if c['kind'] != 'note' or c['abilities']]


def load(path, post=None):
    """HTML file, a Discourse topic .json (post number, default the last staff post) or a post .json -> (cooked html, meta)."""
    raw = open(path, encoding='utf-8').read()
    if not path.endswith('.json'):
        return raw, {}
    d = json.loads(raw)
    posts = d.get('post_stream', {}).get('posts') or [d]
    if post:
        p = next(p for p in posts if p.get('post_number') == int(post))
    else:
        p = [p for p in posts if p.get('staff') and p.get('cooked')][-1]
    return p['cooked'], {'topic': p.get('topic_id'), 'post': p.get('post_number'), 'created_at': p.get('created_at'), 'updated_at': p.get('updated_at')}


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    cooked, meta = load(argv[0], argv[1] if len(argv) > 1 else None)
    print(json.dumps(meta, ensure_ascii=False))
    for c in changes(cooked):
        subj = c['subject'].get('id', '-') + ('/' + c['subject']['spec'] if c['subject'].get('spec') else '')
        pr = ' '.join(f"{p['old']}{p['old_unit']}->{p['new']}{p['unit']}" for p in c['pairs'])
        print(f"{c['kind']:9} {subj:16} {', '.join(c['abilities'])[:40]:40} {pr:24} | {c['text'][:90]}")
    return 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main(sys.argv[1:]))
