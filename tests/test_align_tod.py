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

    @staticmethod
    def worst(res):
        return max(v['shift'] for v in res.values())

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
        self.assertTrue(all(v['shift'] <= 2 for v in res.values()), res)

    def test_moved_waterfall_rejected(self):
        bad = self.relit(self.ref).copy()
        x, y, w, h = 458, 532, 106, 122         # нижний водопад (зона R маски) уехал на 12 px
        bad[y:y + h, x + 12:x + w + 12] = bad[y:y + h, x:x + w]
        aligned, _ = align_tod.align(self.ref, bad)
        res = align_tod.check(self.ref, aligned, self.mask)
        self.assertGreater(self.worst(res), 2, res)

    def shifted(self, box, dx):
        bad = self.relit(self.ref).copy()
        x, y, w, h = box
        bad[y:y + h, x + dx:x + w + dx] = bad[y:y + h, x:x + w]
        return bad

    def test_near_threshold_shifts_rejected(self):
        cases = {'lower waterfall R': (458, 532, 106, 122), 'upper waterfall R': (916, 110, 56, 200),
                 'banner G': (1286, 298, 90, 74, -4), 'banner G 2': (948, 328, 124, 64)}
        for name, box in cases.items():
            dx = box[4] if len(box) > 4 else 4     # the banner touches the right edge: shift it left
            aligned, _ = align_tod.align(self.ref, self.shifted(box[:4], dx))
            res = align_tod.check(self.ref, aligned, self.mask)
            self.assertGreater(self.worst(res), 2, (name, res))

    def test_small_noise_passes(self):
        ok, buf = cv2.imencode('.jpg', self.relit(self.ref), [cv2.IMWRITE_JPEG_QUALITY, 80])
        aligned, _ = align_tod.align(self.ref, cv2.imdecode(buf, cv2.IMREAD_COLOR))
        res = align_tod.check(self.ref, aligned, self.mask)
        self.assertTrue(all(v['shift'] <= 2 for v in res.values()), res)
        bad = self.shifted((458, 532, 106, 122), 1)
        aligned, _ = align_tod.align(self.ref, bad)
        res = align_tod.check(self.ref, aligned, self.mask)
        self.assertTrue(all(v['shift'] <= 2 for v in res.values()), res)

    def test_check_is_idempotent(self):
        aligned, _ = align_tod.align(self.ref, self.shifted((458, 532, 106, 122), 12))
        r1 = align_tod.check(self.ref, aligned, self.mask)
        r2 = align_tod.check(self.ref, aligned, self.mask)
        self.assertEqual(r1, r2)

    @staticmethod
    def clouds(seed):
        """Сглаженный шум — «облака»; у разных seed контуры независимы."""
        n = np.random.RandomState(seed).rand(768, 1376).astype(np.float32)
        n = cv2.GaussianBlur(n, (0, 0), 6)
        n = (n - n.min()) / (n.max() - n.min())
        return cv2.cvtColor((n * 255).astype(np.uint8), cv2.COLOR_GRAY2BGR)

    @staticmethod
    def zone_mask(x, y, w, h):
        m = np.zeros((768, 1376, 4), np.uint8)
        m[y:y + h, x:x + w, 0] = 255     # зона B
        return m

    def test_real_shift_of_one_structure_caught(self):
        base = np.zeros((768, 1376, 3), np.uint8)
        cv2.circle(base, (400, 300), 40, (255, 255, 255), -1)
        cv2.rectangle(base, (380, 330), (430, 380), (200, 200, 200), -1)
        moved = np.roll(base, 5, axis=1)
        res = align_tod.check(base, moved, self.zone_mask(320, 240, 200, 200))
        self.assertGreater(res['B']['shift'], align_tod.LIMIT, res)

    def test_redrawn_clouds_do_not_count(self):
        for seed in range(5):
            res = align_tod.check(self.clouds(seed), self.clouds(seed + 100), self.zone_mask(100, 100, 600, 400))
            self.assertLessEqual(res['B']['shift'], align_tod.LIMIT, (seed, res))

    def test_shift_caught_despite_lighting_noise_and_redrawn_patch(self):
        rng = np.random.RandomState(7)
        moved = np.roll(self.ref, 5, axis=1).astype(np.float32) * .6 + 51      # other light, 5 px shift
        moved += rng.normal(0, 4, moved.shape)                                   # mild independent noise
        moved[200:330, 560:700] = rng.rand(130, 140, 1) * 255                    # a patch redrawn from scratch
        moved = cv2.GaussianBlur(np.clip(moved, 0, 255).astype(np.uint8), (0, 0), .8)
        res = align_tod.check(self.ref, moved, self.mask)
        self.assertGreater(self.worst(res), align_tod.LIMIT, res)

    def test_skipped_zone_is_not_measured_not_zero(self):
        res = align_tod.check(self.clouds(1), self.clouds(2), self.zone_mask(100, 100, 600, 400))
        self.assertFalse(res['B']['measured'], res)
        self.assertIn('не измерена', align_tod.show(res)['B'])

    def test_zone_without_counted_windows_fails_variant(self):
        for zone in 'RGA':
            res = {k: {'shift': 0., 'n': 5, 'total': 5, 'measured': True} for k in 'RGAB'}
            res[zone] = {'shift': 0., 'n': 0, 'total': 5, 'measured': False}
            self.assertTrue(align_tod.problems(res), zone)
        res = {k: {'shift': 0., 'n': 5, 'total': 5, 'measured': True} for k in 'RGAB'}
        res['B'] = {'shift': 0., 'n': 0, 'total': 5, 'measured': False}
        self.assertEqual(align_tod.problems(res), [])      # unmeasured sky alone does not fail


if __name__ == '__main__':
    unittest.main()
