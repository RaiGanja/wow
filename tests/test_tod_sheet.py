"""Лист «утро / день / вечер / ночь»: четыре сцены 2×2 и крупные планы героев в 100% исходника.
Запуск: python tests/test_tod_sheet.py"""
import os, sys, unittest
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import tod_sheet


class Sheet(unittest.TestCase):
    def setUp(self):
        self.ims = [Image.new('RGB', (2752, 1536), c) for c in ((200, 0, 0), (0, 200, 0), (0, 0, 200), (90, 90, 90))]

    def test_scenes_two_by_two(self):
        out = tod_sheet.scenes(self.ims, width=400)
        self.assertEqual(out.width, 2 * 400 + 8)
        self.assertEqual(out.getpixel((10, 60)), (200, 0, 0))        # dawn top left
        self.assertEqual(out.getpixel((420, 60)), (0, 200, 0))       # day top right

    def test_heroes_at_full_size(self):
        out = tod_sheet.heroes(self.ims)
        x0, y0, x1, y1 = tod_sheet.HEROES['paladin']
        cw = max(b[2] - b[0] for b in tod_sheet.HEROES.values()) * 2   # 2752 = 2 x grid: crops are not scaled
        self.assertEqual(out.width, 4 * cw + 3 * 6)
        self.assertEqual(out.getpixel((5, 40)), (200, 0, 0))
        self.assertEqual(out.getpixel((3 * (cw + 6) + 5, 40)), (90, 90, 90))   # night column


if __name__ == '__main__':
    unittest.main()
