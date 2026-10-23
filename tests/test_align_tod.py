"""Совмещение вариантов шапки с рассветом: известный сдвиг находится, локальная порча бракуется.
Запуск: python tests/test_align_tod.py"""
import os, sys, unittest
import cv2, numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import align_tod

ART = os.path.join(os.path.expanduser('~'), 'gabella-bot', 'assets', 'wow_art', 'hero_dawn.jpg')
MASK = os.path.join(ROOT, 'assets', 'living', 'hero_dawn-fx.png')


class Align(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ref = cv2.resize(cv2.imread(ART), (1376, 768))
        cls.mask = cv2.imread(MASK, cv2.IMREAD_UNCHANGED)

    def relit(self, im):
        """Другое «время суток»: темнее и синее — цвет другой, контуры те же."""
        out = im.astype(np.float32) * np.array([1.15, .75, .55]) * .6
        return np.clip(out, 0, 255).astype(np.uint8)

    def test_shift_and_scale_recovered(self):
        M = np.float32([[1.012, 0, -7], [0, 1.012, 4]])
        moved = cv2.warpAffine(self.relit(self.ref), M, (1376, 768), borderMode=cv2.BORDER_REFLECT)
        aligned, cc = align_tod.align(self.ref, moved)
        res = align_tod.check(self.ref, aligned, self.mask)
        self.assertGreater(cc, .6)
        self.assertTrue(all(v <= 2 for v in res.values()), res)

    def test_moved_waterfall_rejected(self):
        bad = self.relit(self.ref).copy()
        x, y, w, h = 458, 532, 106, 122         # нижний водопад (зона R маски) уехал на 12 px
        bad[y:y + h, x + 12:x + w + 12] = bad[y:y + h, x:x + w]
        aligned, _ = align_tod.align(self.ref, bad)
        res = align_tod.check(self.ref, aligned, self.mask)
        self.assertGreater(max(res.values()), 2, res)


if __name__ == '__main__':
    unittest.main()
