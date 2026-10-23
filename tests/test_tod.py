"""Время суток в шапке: файлы вариантов, бюджет размера, часы как у радио, разметка без лишней загрузки.
Запуск: python tests/test_tod.py"""
import json, os, re, subprocess, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ART = os.path.join(ROOT, 'assets', 'art')
TODS = ['dawn', 'day', 'dusk', 'night']
WIDE = (960, 1440, 1920, 2560, 3840)
MOBILE = (600, 1000)
import sys
sys.path.insert(0, ROOT)


def size(name):
    return os.path.getsize(os.path.join(ART, name))


class Files(unittest.TestCase):
    def test_every_variant_and_width_exists_within_budget(self):
        for tod in TODS:
            for ext in ('avif', 'webp'):
                for w in WIDE:
                    self.assertLessEqual(size(f'hero_{tod}-{w}.{ext}'), size(f'hero_dawn-{w}.{ext}') * 1.15, (tod, w, ext))
                for w in MOBILE:
                    self.assertLessEqual(size(f'hero_{tod}-m-{w}.{ext}'), size(f'hero_dawn-m-{w}.{ext}') * 1.15, (tod, 'm', w, ext))


class Hours(unittest.TestCase):
    def test_bounds_follow_radio(self):
        import tod
        air = json.load(open(os.path.join(ROOT, 'assets', 'radio', 'stations.json'), encoding='utf-8'))['air']
        self.assertEqual(tod.bounds(), [next(p['from'] for p in air if tod.RADIO[p['id']] == t) for t in tod.PARTS])

    def test_part_in_browser_matches_radio_every_hour(self):
        import tod
        air = json.load(open(os.path.join(ROOT, 'assets', 'radio', 'stations.json'), encoding='utf-8'))['air']
        def radio(h):
            p = next(p for p in air if (p['from'] <= h < p['to'] if p['from'] < p['to'] else h >= p['from'] or h < p['to']))
            return tod.RADIO[p['id']]
        js = 'var B=' + json.dumps(tod.bounds()) + ';' + tod.PART_JS + ';console.log(JSON.stringify([...Array(24).keys()].map(part)))'
        got = json.loads(subprocess.run(['node', '-e', js], capture_output=True, text=True, check=True).stdout)
        self.assertEqual(got, [radio(h) for h in range(24)])

    def test_texts_in_every_language(self):
        import tod, langs
        for lang in langs.ALL:
            self.assertEqual(set(tod.names(lang)), set(tod.PARTS), lang)
            self.assertTrue(all(tod.TEXT[lang].get(k) for k in ('auto', 'reset', 'label')), lang)


class Markup(unittest.TestCase):
    def test_hero_has_no_real_srcset_and_falls_back_to_dawn(self):
        import tod
        h = tod.hero()
        pic = h.split('</picture>')[0]
        self.assertNotIn(' srcset="', pic)
        self.assertNotIn(' src="', pic)
        self.assertIn('data-srcset="@@ROOT@@assets/art/hero_{tod}-960.avif 960w', pic)
        self.assertIn('<noscript>', h)
        self.assertIn('hero_dawn-1920.webp', h.split('<noscript>')[1])

    def test_built_home_pages(self):
        for page in ('index.html', 'en/index.html', 'de/index.html'):
            html = open(os.path.join(ROOT, page), encoding='utf-8').read()
            head = html.split('</head>')[0]
            self.assertIn('window.GabellaTod', head, page)
            self.assertIn('data-tod-sw', html, page)
            self.assertNotIn('hero_dawn-1920.avif 1920w', html.split('<noscript>')[0].split('</head>')[1], page)

    def test_leveling_guide_follows_time_of_day(self):
        html = open(os.path.join(ROOT, 'guides', 'leveling', 'index.html'), encoding='utf-8').read()
        self.assertIn('window.GabellaTod', html.split('</head>')[0])
        self.assertIn('hero_{tod}-1440', html)
        self.assertRegex(html, r'assets/tod/tod\.js\?v=\w{10}')
        self.assertIn('data-tod-sw', html)
        other = open(os.path.join(ROOT, 'guides', 'professions', 'index.html'), encoding='utf-8').read()
        self.assertNotIn('GabellaTod', other)
        self.assertNotIn('data-tod-sw', other)


class Wiring(unittest.TestCase):
    def test_living_sun_measured_for_every_variant(self):
        js = open(os.path.join(ROOT, 'assets', 'living', 'living.js'), encoding='utf-8').read()
        sun = re.search(r'const SUN = \{([^}]+)\}', js).group(1)
        for tod in TODS:
            x, y = map(int, re.search(rf'{tod}: \[(\d+), (\d+)\]', sun).groups())
            self.assertTrue(0 < x < 1376 and 0 < y < 768, (tod, x, y))

    def test_home_loads_tod_script_with_version(self):
        html = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
        self.assertRegex(html, r'assets/tod/tod\.js\?v=\w{10}')
        self.assertRegex(html, r'assets/tod/tod\.css\?v=\w{10}')


if __name__ == '__main__':
    unittest.main()
