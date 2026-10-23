"""Radio of the guide: tracks of Kevin MacLeod (incompetech.com, CC BY 4.0) -> assets/radio/<slug>.m4a
(AAC 80 kbit/s, loudness -16 LUFS so stations play at one level) and assets/radio/stations.json
(stations, titles, durations, credits) that assets/radio/radio.js reads when the panel opens.
Source mp3: https://incompetech.com/music/royalty-free/mp3-royaltyfree/<Title>.mp3, downloaded by hand into a folder.
Run: python tools/make_radio.py <folder with the mp3>  (needs ffmpeg and ffprobe in PATH)"""
import json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'assets', 'radio')

# art: picture of the station tile, from assets/art (without .webp); pos: its object-position (portraits: the face)
STATIONS = [
    {'id': 'tavern', 'art': 'hero_campfire-960', 'name': {'ru': 'Таверна', 'en': 'Tavern', 'uk': 'Таверна'},
     'mood': {'ru': 'Лютня у очага', 'en': 'Lute by the hearth', 'uk': 'Лютня біля вогнища'},
     'tracks': ['Master of the Feast', 'Minstrel Guild', 'Folk Round', 'Pippin the Hunchback']},
    {'id': 'road', 'art': 'hero_dawn-960', 'name': {'ru': 'Дорога', 'en': 'The Road', 'uk': 'Дорога'},
     'mood': {'ru': 'Рассвет над холмами', 'en': 'Dawn over the hills', 'uk': 'Світанок над пагорбами'},
     'tracks': ['Achaidh Cheide', 'Skye Cuillin', 'Teller of the Tales', 'Lord of the Land']},
    {'id': 'dungeon', 'art': 'warlock-600', 'pos': '50% 18%', 'name': {'ru': 'Подземелье', 'en': 'Dungeon', 'uk': 'Підземелля'},
     'mood': {'ru': 'Факелы и тени', 'en': 'Torches and shadows', 'uk': 'Смолоскипи й тіні'},
     'tracks': ['Dark Times', 'Black Vortex', 'Unseen Horrors', 'Ancient Rite']},
    {'id': 'battle', 'art': 'warrior-600', 'pos': '50% 20%', 'name': {'ru': 'Битва', 'en': 'Battle', 'uk': 'Битва'},
     'mood': {'ru': 'За Альянс! За Орду!', 'en': 'For the Alliance! For the Horde!', 'uk': 'За Альянс! За Орду!'},
     'tracks': ['Heroic Age', 'Five Armies', 'Crusade', 'Prelude and Action']},
]
AUTHOR = 'Kevin MacLeod (incompetech.com)'
LICENSE = ('CC BY 4.0', 'https://creativecommons.org/licenses/by/4.0/')


def slug(title):
    return re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')


def duration(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path],
                         capture_output=True, text=True, check=True).stdout
    return round(float(out))


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else sys.exit(__doc__)
    os.makedirs(OUT, exist_ok=True)
    data = {'author': AUTHOR, 'license': LICENSE[0], 'license_url': LICENSE[1], 'stations': []}
    for st in STATIONS:
        tracks = []
        for title in st['tracks']:
            dst = os.path.join(OUT, slug(title) + '.m4a')
            if not os.path.exists(dst):
                subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(src, title + '.mp3'), '-vn', '-map_metadata', '-1',
                                '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11', '-ar', '44100', '-c:a', 'aac', '-b:a', '80k',
                                '-movflags', '+faststart', dst], check=True)
            tracks.append({'t': title, 'f': slug(title) + '.m4a', 'd': duration(dst)})
            print(f'{st["id"]:8} {title:24} {os.path.getsize(dst) // 1024:6} KB')
        data['stations'].append({k: st[k] for k in ('id', 'art', 'pos', 'name', 'mood') if k in st} | {'tracks': tracks})
    with open(os.path.join(OUT, 'stations.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))


if __name__ == '__main__':
    main()
