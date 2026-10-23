"""Radio of the guide: tracks of Kevin MacLeod (incompetech.com, CC BY 4.0) -> <MEDIA>/<slug>.m4a
(AAC 64 kbit/s, loudness -16 LUFS so stations play at one level) and assets/radio/stations.json
(stations, the "On air" day plan, titles, authors, durations, credits) that assets/radio/radio.js reads when the panel opens.
Source mp3: https://incompetech.com/music/royalty-free/mp3-royaltyfree/<file>.mp3 (file names: incompetech.com/music/royalty-free/pieces.json),
saved into a folder as <Title>.mp3.
Run: python tools/make_radio.py <folder with the mp3>  (needs ffmpeg and ffprobe in PATH)"""
import glob, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'assets', 'radio')

# Where the tracks are served from: '' = assets/radio/ of the site itself. To move them to other storage
# (e.g. a Cloudflare R2 bucket on media.gabella.site), upload the .m4a files there and put its address here, then rerun.
MEDIA = ''

KM = 'Kevin MacLeod'
# art: picture of the station tile, from assets/art (without .webp); pos: its object-position (portraits: the face).
# tracks: titles, or (title, author) when the author is not Kevin MacLeod.
STATIONS = [
    {'id': 'morning', 'art': 'hero_dawn-960', 'name': {'ru': 'Утро в долине', 'en': 'Morning in the Vale', 'uk': 'Ранок у долині'},
     'mood': {'ru': 'Арфа и флейта на рассвете', 'en': 'Harp and flute at dawn', 'uk': 'Арфа й флейта на світанку'},
     'tracks': ['Morning', 'Ascending the Vale', 'Enchanted Journey', 'Canon in D for Two Renaissance Harps', 'Evening', 'Royal Coupling',
                'Dreamy Flashback', 'Frozen Star', 'Decline', 'The Parting', 'Windswept', 'On the Shore', 'Cello Suite #1 in G - Prelude',
                'Adventures in Adventureland']},
    {'id': 'road', 'art': 'hunter-600', 'pos': '50% 20%', 'name': {'ru': 'Дорога', 'en': 'The Road', 'uk': 'Дорога'},
     'mood': {'ru': 'Волынка и скрипка в пути', 'en': 'Pipes and fiddle on the way', 'uk': 'Волинка й скрипка в дорозі'},
     'tracks': ['Achaidh Cheide', 'Skye Cuillin', 'Lord of the Land', 'Teller of the Tales', 'Celtic Impulse', 'Angevin', 'Tabuk',
                'The Other Side of the Door', 'Americana', 'Long Road Ahead', 'Temple of the Manes', 'Moorland', 'Heavy Heart', 'Hidden Past']},
    {'id': 'forest', 'art': 'night-elf-600', 'pos': '50% 20%', 'name': {'ru': 'Древний лес', 'en': 'Ancient Forest', 'uk': 'Прадавній ліс'},
     'mood': {'ru': 'Тайны под кронами', 'en': 'Secrets under the canopy', 'uk': 'Таємниці під кронами'},
     'tracks': ['Willow and the Light', 'Night of the Owl', 'The Snow Queen', 'The Path of the Goblin King', 'Enchanted Valley', 'Magic Forest',
                'Heart of Nowhere', 'Myst', 'River Fire', 'Vulcan', 'Not As It Seems', 'Angevin B', 'Tempting Secrets']},
    {'id': 'steppe', 'art': 'tauren-600', 'pos': '50% 20%', 'name': {'ru': 'Степи и барабаны', 'en': 'Drums of the Plains', 'uk': 'Степи й барабани'},
     'mood': {'ru': 'Ритм кочевых племён', 'en': 'Rhythm of the tribes', 'uk': 'Ритм кочових племен'},
     'tracks': ['Dentaneosuchus Hunt', 'Sauropod Spotting', 'Cretaceous Dawn', 'Truth in the Stones', 'Firesong', 'Silver Flame',
                'Trouble with Tribals', 'Arcane', 'Firebrand', 'Lotus', 'Crossing the Chasm']},
    {'id': 'tavern', 'art': 'dwarf-600', 'pos': '50% 20%', 'name': {'ru': 'Таверна', 'en': 'Tavern', 'uk': 'Таверна'},
     'mood': {'ru': 'Лютня и эль у очага', 'en': 'Lute and ale by the hearth', 'uk': 'Лютня й ель біля вогнища'},
     'tracks': ['Master of the Feast', 'Minstrel Guild', 'Folk Round', 'Pippin the Hunchback', 'Village Consort', 'Thatched Villagers',
                'Fiddles McGinty', 'Galway', 'Club Seamus', 'Crunk Knight', 'Industrious Ferret', 'Mischief Maker', 'Errigal',
                'Suonatore di Liuto', 'The Britons']},
    {'id': 'dungeon', 'art': 'warlock-600', 'pos': '50% 18%', 'name': {'ru': 'Подземелье', 'en': 'Dungeon', 'uk': 'Підземелля'},
     'mood': {'ru': 'Факелы и тени', 'en': 'Torches and shadows', 'uk': 'Смолоскипи й тіні'},
     'tracks': ['Dark Times', 'Unseen Horrors', 'Ancient Rite', 'Drums of the Deep', 'Lost Time', 'Lost Frontier', 'Intrepid', 'Vanishing',
                'Return of the Mummy', 'Oppressive Gloom', 'This House', 'Mary Celeste', 'The Chamber', 'Serpentine Trek']},
    {'id': 'battle', 'art': 'warrior-600', 'pos': '50% 20%', 'name': {'ru': 'Битва', 'en': 'Battle', 'uk': 'Битва'},
     'mood': {'ru': 'За Альянс! За Орду!', 'en': 'For the Alliance! For the Horde!', 'uk': 'За Альянс! За Орду!'},
     'tracks': ['Heroic Age', 'Five Armies', 'Crusade', 'Prelude and Action', 'Black Vortex', 'Death and Axes', 'Darkling', 'Rynos Theme',
                'Hero Down', 'Death of Kings', 'Majestic Hills', 'Colossus', 'Stoneworld Battle', 'The Descent', 'Clash Defiant']},
    {'id': 'night', 'art': 'hero_campfire-960', 'name': {'ru': 'Ночной привал', 'en': 'Night Camp', 'uk': 'Нічний привал'},
     'mood': {'ru': 'Тихо, пока все спят', 'en': 'Quiet while the camp sleeps', 'uk': 'Тихо, поки всі сплять'},
     'tracks': ['Midnight Tale', 'Anguish', 'Gymnopedie No. 1', 'Gymnopedie No. 2', 'Water Lily', 'Reawakening', 'At Rest', 'Disquiet',
                'Danse Morialta', 'Brittle Rille', 'Avec Soin', 'Facile', 'Calmant', 'Prelude in C (BWV 846)', 'Canon in D Major']},
]
# "On air": the station plan by the listener's local hour (from..to, to may pass midnight); tracks of the part's stations are mixed.
AIR = [
    {'id': 'morning', 'from': 6, 'to': 11, 'name': {'ru': 'Утро', 'en': 'Morning', 'uk': 'Ранок'}, 'stations': ['morning', 'road']},
    {'id': 'day', 'from': 11, 'to': 17, 'name': {'ru': 'День', 'en': 'Day', 'uk': 'День'}, 'stations': ['road', 'forest', 'steppe']},
    {'id': 'evening', 'from': 17, 'to': 23, 'name': {'ru': 'Вечер', 'en': 'Evening', 'uk': 'Вечір'}, 'stations': ['tavern', 'battle', 'dungeon']},
    {'id': 'night', 'from': 23, 'to': 6, 'name': {'ru': 'Ночь', 'en': 'Night', 'uk': 'Ніч'}, 'stations': ['night', 'forest']},
]
LICENSE = ('CC BY 4.0', 'https://creativecommons.org/licenses/by/4.0/')
SOURCES = {KM: 'incompetech.com'}


def slug(title):
    return re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')


def duration(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path],
                         capture_output=True, text=True, check=True).stdout
    return round(float(out))


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else sys.exit(__doc__)
    os.makedirs(OUT, exist_ok=True)
    data = {'media': MEDIA, 'license': LICENSE[0], 'license_url': LICENSE[1], 'sources': SOURCES, 'air': AIR, 'stations': []}
    used, total = set(), 0
    for st in STATIONS:
        tracks = []
        for item in st['tracks']:
            title, author = (item, KM) if isinstance(item, str) else item
            f = slug(title) + '.m4a'
            dst = os.path.join(OUT, f)
            assert f not in used, f'{title}: track is on two stations'
            used.add(f)
            if not os.path.exists(dst):
                subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(src, title + '.mp3'), '-vn', '-map_metadata', '-1',
                                '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11', '-ar', '44100', '-c:a', 'aac', '-b:a', '64k',
                                '-movflags', '+faststart', dst], check=True)
            d = duration(dst)
            total += d
            tracks.append({'t': title, 'a': author, 'f': f, 'd': d} if author != KM else {'t': title, 'f': f, 'd': d})
            print(f'{st["id"]:8} {title:38} {os.path.getsize(dst) // 1024:6} KB')
        data['stations'].append({k: st[k] for k in ('id', 'art', 'pos', 'name', 'mood') if k in st} | {'author': KM, 'tracks': tracks})
    for old in glob.glob(os.path.join(OUT, '*.m4a')):   # tracks no station plays any more
        if os.path.basename(old) not in used:
            os.remove(old)
            print('removed', os.path.basename(old))
    with open(os.path.join(OUT, 'stations.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
    size = sum(os.path.getsize(os.path.join(OUT, f)) for f in used)
    print(f'{len(used)} tracks, {total // 3600} h {total % 3600 // 60} min, {size / 2**20:.0f} MB')


if __name__ == '__main__':
    main()
