"""Radio of the guide: tracks of Kevin MacLeod (incompetech.com) and other authors under CC BY / CC0 (opengameart.org)
-> <tracks folder>/<slug>.m4a (AAC <BITRATE>, loudness -16 LUFS so stations play at one level) and assets/radio/stations.json
(stations, the "On air" day plan, titles, authors, licenses, durations) that assets/radio/radio.js reads when the panel opens.
Track lists: tools/radio_tracks.py. Sources are saved into one folder as <Title>.<mp3|ogg|wav|flac> (":" in a title -> "_");
Kevin MacLeod: https://incompetech.com/music/royalty-free/mp3-royaltyfree/<file>.mp3 (file names: incompetech.com/music/royalty-free/pieces.json).
The .m4a files are served from MEDIA (Cloudflare R2), not from the site: upload the tracks folder there after a run
(npx wrangler r2 object put gabella-media/radio/<file> --file <tracks folder>/<file> --remote).
Run: python tools/make_radio.py <folder with the sources> <tracks folder>  (needs ffmpeg and ffprobe in PATH)"""
import glob, json, os, re, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from radio_tracks import KM, LICENSES, SOURCES, TRACKS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'assets', 'radio')

# Where the tracks are served from: the radio/ folder of the Cloudflare R2 bucket gabella-media (domain media.gabella.site).
# '' = assets/radio/ of the site itself (the site on GitHub Pages is limited to 1 GB, so the library lives on R2).
MEDIA = 'https://media.gabella.site/radio/'
# Sound quality of the tracks: 256k AAC, near-transparent to the 320k mp3 / wav sources (never lower than 128k). To change it, delete the .m4a in the tracks folder, rerun and upload again.
BITRATE = '256k'

# art: picture of the station tile, from assets/art (without .webp); pos: its object-position (portraits: the face).
# Tracks of each station: TRACKS[id] in tools/radio_tracks.py.
STATIONS = [
    {'id': 'morning', 'art': 'hero_dawn-960', 'name': {'ru': 'Утро в долине', 'en': 'Morning in the Vale', 'uk': 'Ранок у долині'},
     'mood': {'ru': 'Арфа и флейта на рассвете', 'en': 'Harp and flute at dawn', 'uk': 'Арфа й флейта на світанку'}},
    {'id': 'road', 'art': 'hunter-600', 'pos': '50% 20%', 'name': {'ru': 'Дорога', 'en': 'The Road', 'uk': 'Дорога'},
     'mood': {'ru': 'Волынка и скрипка в пути', 'en': 'Pipes and fiddle on the way', 'uk': 'Волинка й скрипка в дорозі'}},
    {'id': 'forest', 'art': 'night-elf-600', 'pos': '50% 20%', 'name': {'ru': 'Древний лес', 'en': 'Ancient Forest', 'uk': 'Прадавній ліс'},
     'mood': {'ru': 'Тайны под кронами', 'en': 'Secrets under the canopy', 'uk': 'Таємниці під кронами'}},
    {'id': 'steppe', 'art': 'tauren-600', 'pos': '50% 20%', 'name': {'ru': 'Степи и барабаны', 'en': 'Drums of the Plains', 'uk': 'Степи й барабани'},
     'mood': {'ru': 'Ритм кочевых племён', 'en': 'Rhythm of the tribes', 'uk': 'Ритм кочових племен'}},
    {'id': 'tavern', 'art': 'dwarf-600', 'pos': '50% 20%', 'name': {'ru': 'Таверна', 'en': 'Tavern', 'uk': 'Таверна'},
     'mood': {'ru': 'Лютня и эль у очага', 'en': 'Lute and ale by the hearth', 'uk': 'Лютня й ель біля вогнища'}},
    {'id': 'dungeon', 'art': 'warlock-600', 'pos': '50% 18%', 'name': {'ru': 'Подземелье', 'en': 'Dungeon', 'uk': 'Підземелля'},
     'mood': {'ru': 'Факелы и тени', 'en': 'Torches and shadows', 'uk': 'Смолоскипи й тіні'}},
    {'id': 'battle', 'art': 'warrior-600', 'pos': '50% 20%', 'name': {'ru': 'Битва', 'en': 'Battle', 'uk': 'Битва'},
     'mood': {'ru': 'За Альянс! За Орду!', 'en': 'For the Alliance! For the Horde!', 'uk': 'За Альянс! За Орду!'}},
    {'id': 'night', 'art': 'hero_campfire-960', 'name': {'ru': 'Ночной привал', 'en': 'Night Camp', 'uk': 'Нічний привал'},
     'mood': {'ru': 'Тихо, пока все спят', 'en': 'Quiet while the camp sleeps', 'uk': 'Тихо, поки всі сплять'}},
]
# "On air": the station plan by the listener's local hour (from..to, to may pass midnight); tracks of the part's stations are mixed.
AIR = [
    {'id': 'morning', 'from': 6, 'to': 11, 'name': {'ru': 'Утро', 'en': 'Morning', 'uk': 'Ранок'}, 'stations': ['morning', 'road']},
    {'id': 'day', 'from': 11, 'to': 17, 'name': {'ru': 'День', 'en': 'Day', 'uk': 'День'}, 'stations': ['road', 'forest', 'steppe']},
    {'id': 'evening', 'from': 17, 'to': 23, 'name': {'ru': 'Вечер', 'en': 'Evening', 'uk': 'Вечір'}, 'stations': ['tavern', 'battle', 'dungeon']},
    {'id': 'night', 'from': 23, 'to': 6, 'name': {'ru': 'Ночь', 'en': 'Night', 'uk': 'Ніч'}, 'stations': ['night', 'forest']},
]
# Station and day-part texts in the guide's other languages, by the English text: de, fr, es, pt (pt-BR), it, pl
TX = {
    'Morning in the Vale': ('Morgen im Tal', 'Matin dans la vallée', 'Mañana en el valle', 'Manhã no vale', 'Mattino nella valle', 'Poranek w dolinie'),
    'Harp and flute at dawn': ('Harfe und Flöte im Morgengrauen', 'Harpe et flûte à l’aube', 'Arpa y flauta al amanecer', 'Harpa e flauta ao amanhecer',
                               'Arpa e flauto all’alba', 'Harfa i flet o świcie'),
    'The Road': ('Unterwegs', 'La route', 'El camino', 'A estrada', 'La strada', 'Droga'),
    'Pipes and fiddle on the way': ('Dudelsack und Fiedel auf dem Weg', 'Cornemuse et violon en chemin', 'Gaita y violín por el camino',
                                    'Gaita e rabeca pelo caminho', 'Cornamusa e violino in cammino', 'Dudy i skrzypce w drodze'),
    'Ancient Forest': ('Uralter Wald', 'Forêt ancienne', 'Bosque ancestral', 'Floresta ancestral', 'Foresta antica', 'Prastary las'),
    'Secrets under the canopy': ('Geheimnisse unter dem Blätterdach', 'Secrets sous la canopée', 'Secretos bajo las copas', 'Segredos sob as copas',
                                 'Segreti sotto le fronde', 'Tajemnice pod koronami drzew'),
    'Drums of the Plains': ('Trommeln der Steppe', 'Tambours des plaines', 'Tambores de las llanuras', 'Tambores das planícies', 'Tamburi delle pianure', 'Bębny równin'),
    'Rhythm of the tribes': ('Rhythmus der Stämme', 'Rythme des tribus', 'Ritmo de las tribus', 'Ritmo das tribos', 'Ritmo delle tribù', 'Rytm plemion'),
    'Tavern': ('Taverne', 'Taverne', 'Taberna', 'Taverna', 'Taverna', 'Karczma'),
    'Lute and ale by the hearth': ('Laute und Ale am Kamin', 'Luth et bière au coin du feu', 'Laúd y cerveza junto al hogar', 'Alaúde e cerveja junto à lareira',
                                   'Liuto e birra accanto al focolare', 'Lutnia i piwo przy kominku'),
    'Dungeon': ('Dungeon', 'Donjon', 'Mazmorra', 'Masmorra', 'Spedizione', 'Dungeon'),
    'Torches and shadows': ('Fackeln und Schatten', 'Torches et ombres', 'Antorchas y sombras', 'Tochas e sombras', 'Torce e ombre', 'Pochodnie i cienie'),
    'Battle': ('Schlacht', 'Bataille', 'Batalla', 'Batalha', 'Battaglia', 'Bitwa'),
    'For the Alliance! For the Horde!': ('Für die Allianz! Für die Horde!', 'Pour l’Alliance ! Pour la Horde !', '¡Por la Alianza! ¡Por la Horda!',
                                         'Pela Aliança! Pela Horda!', 'Per l’Alleanza! Per l’Orda!', 'For the Alliance! For the Horde!'),
    'Night Camp': ('Nachtlager', 'Bivouac nocturne', 'Campamento nocturno', 'Acampamento noturno', 'Bivacco notturno', 'Nocny obóz'),
    'Quiet while the camp sleeps': ('Still, während das Lager schläft', 'Silence, le camp dort', 'Silencio mientras el campamento duerme',
                                    'Silêncio enquanto o acampamento dorme', 'Silenzio mentre il campo dorme', 'Cicho, gdy obóz śpi'),
    'Morning': ('Morgen', 'Matin', 'Mañana', 'Manhã', 'Mattina', 'Rano'),
    'Day': ('Tag', 'Journée', 'Día', 'Dia', 'Giorno', 'Dzień'),
    'Evening': ('Abend', 'Soir', 'Tarde', 'Tarde', 'Sera', 'Wieczór'),
    'Night': ('Nacht', 'Nuit', 'Noche', 'Noite', 'Notte', 'Noc'),
}
NEW_LANGS = ('de', 'fr', 'es', 'pt', 'it', 'pl')


def add_langs(items):
    """name/mood dicts of stations and day parts: add the new languages from TX by the English text."""
    for it in items:
        for k in ('name', 'mood'):
            if k in it:
                it[k].update(zip(NEW_LANGS, TX[it[k]['en']]))
    return items


add_langs(STATIONS)
add_langs(AIR)


def slug(title):
    return re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')


def source(folder, title):
    """The source file of a track: <Title>.<ext> (":" is not allowed in Windows file names)."""
    name = title.replace(':', '_')
    for ext in ('flac', 'wav', 'ogg', 'mp3'):
        path = os.path.join(folder, f'{name}.{ext}')
        if os.path.exists(path):
            return path
    sys.exit(f'{title}: no source in {folder}')


def duration(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path],
                         capture_output=True, text=True, check=True).stdout
    return round(float(out))


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    src, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    data = {'media': MEDIA, 'license': 'by4', 'licenses': {k: list(v) for k, v in LICENSES.items()}, 'sources': SOURCES,
            'air': AIR, 'stations': []}
    used, total = set(), 0
    for st in STATIONS:
        tracks = []
        for item in TRACKS[st['id']]:
            title, author, lic = (item, KM, 'by4') if isinstance(item, str) else item
            assert author in SOURCES and lic in LICENSES, title
            f = slug(title) + '.m4a'
            dst = os.path.join(out, f)
            assert f not in used, f'{title}: track is on two stations'
            used.add(f)
            if not os.path.exists(dst):
                subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', source(src, title), '-vn', '-map_metadata', '-1',
                                '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11', '-ar', '44100', '-ac', '2', '-c:a', 'aac', '-b:a', BITRATE,
                                '-movflags', '+faststart', dst], check=True)
            d = duration(dst)
            total += d
            tracks.append({'t': title, 'f': f, 'd': d} | ({'a': author} if author != KM else {}) | ({'l': lic} if lic != 'by4' else {}))
            print(f'{st["id"]:8} {title:38} {os.path.getsize(dst) // 1024:6} KB')
        data['stations'].append({k: st[k] for k in ('id', 'art', 'pos', 'name', 'mood') if k in st} | {'author': KM, 'tracks': tracks})
    for old in glob.glob(os.path.join(out, '*.m4a')):   # tracks no station plays any more
        if os.path.basename(old) not in used:
            os.remove(old)
            print('removed', os.path.basename(old))
    with open(os.path.join(OUT, 'stations.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
    size = sum(os.path.getsize(os.path.join(out, f)) for f in used)
    print(f'{len(used)} tracks, {total // 3600} h {total % 3600 // 60} min, {size / 2**20:.0f} MB')


if __name__ == '__main__':
    main()
