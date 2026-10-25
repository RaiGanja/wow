"""Variants of the home hero (day, dusk, night) made by editing hero_dawn drift a few pixels; the living
layer's mask (assets/living/hero_dawn-fx.png) must fit all of them. Aligns a variant to hero_dawn by its edges
(lighting differs, outlines do not), then checks the residual shift inside every mask zone.
Run: python tools/align_tod.py <wow_art> <day|dusk|night> [--allow=G] [raw files...]   (default raw: hero_<tod>.raw*.jpg;
--allow lists zones whose shift a person accepted after looking at the overlay)
Writes hero_<tod>.jpg (best aligned try, at the size of hero_dawn.jpg) and hero_<tod>-overlay.png; exit code 1 when no try passes."""
import glob, os, sys
import cv2, numpy as np

W, H = 1376, 768
LIMIT = 2.0   # px: the most a mask zone may still be off
WIN = 64      # px: side of the square windows the residual shift is measured in
MARGIN = 8    # px: border of a window left out of the correlation (the shift-back leaves junk there)
MATCH = 0.7   # min Pearson correlation of a window's edges after undoing the found shift; below it the window is not
              # counted (no common outlines, e.g. a repainted sky: the found shift is a random peak)
MIN_SHARE = .25   # a zone with fewer counted windows (share of its windows) is reported as not measured
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MASK = os.path.join(ROOT, 'assets', 'living', 'hero_dawn-fx.png')


def edges(im):
    g = cv2.GaussianBlur(cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(np.float32), (0, 0), 1.2)
    m = cv2.magnitude(cv2.Sobel(g, cv2.CV_32F, 1, 0), cv2.Sobel(g, cv2.CV_32F, 0, 1))
    m = cv2.GaussianBlur(m, (0, 0), 2)
    return m / (m.max() + 1e-6)


def fit(ref, img):
    """Transform (3x3, W x H grid, maps ref pixels to img pixels) that lays img onto ref by edges: affine, then
    homography if that fits better. ref must be W x H; img any size. Returns (T, ECC score)."""
    a, b = edges(ref), edges(cv2.resize(img, (W, H), interpolation=cv2.INTER_AREA))
    best = (np.eye(3, dtype=np.float64), -1.)
    crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-6)
    for mode, eye in ((cv2.MOTION_AFFINE, np.eye(2, 3, dtype=np.float32)), (cv2.MOTION_HOMOGRAPHY, np.eye(3, dtype=np.float32))):
        try:
            cc, M = cv2.findTransformECC(a, b, eye, mode, crit, None, 5)
        except cv2.error:
            continue
        if cc > best[1]:
            best = (np.vstack([M, [0, 0, 1]]) if mode == cv2.MOTION_AFFINE else M.astype(np.float64), cc)
    return best


def warp(img, T, size):
    """Apply grid transform T to img of any size, writing an image of size (w, h): the grid is scaled to both ends,
    so a 4K source is resampled once, at full size."""
    w, h = size
    to_grid = np.diag([W / w, H / h, 1.])                         # output pixel -> grid
    to_img = np.diag([img.shape[1] / W, img.shape[0] / H, 1.])    # grid -> source pixel
    M = to_img @ T @ to_grid
    return cv2.warpPerspective(img, M, (w, h), flags=cv2.INTER_LANCZOS4 + cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REFLECT)


def align(ref, img):
    """Warp img onto ref (W x H). Returns (aligned BGR W x H, ECC score)."""
    T, cc = fit(ref, img)
    return warp(img, T, (W, H)), cc


def align_full(ref, img):
    """Same as align, but ref is the master at full size and the result has its size (shift measured in the grid)."""
    T, cc = fit(cv2.resize(ref, (W, H), interpolation=cv2.INTER_AREA), img)
    return warp(img, T, (ref.shape[1], ref.shape[0])), cc


def _matches(wa, wb, dx, dy):
    """True when the edges of window wb, moved back by the found shift (dx, dy), correlate with wa (centre only)."""
    back = cv2.warpAffine(wb, np.float32([[1, 0, -dx], [0, 1, -dy]]), (WIN, WIN), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    c = slice(MARGIN, WIN - MARGIN)
    u, v = wa[c, c].ravel(), back[c, c].ravel()
    u, v = u - u.mean(), v - v.mean()
    d = float(np.sqrt((u * u).sum() * (v * v).sum()))
    return d > 1e-9 and float((u * v).sum()) / d >= MATCH


def check(ref, aligned, mask):
    """Per mask zone: {'shift': largest leftover shift (px) over counted windows, 'n': counted windows,
    'total': windows in the zone, 'measured': enough of them were counted}. Phase correlation of edge maps in WIN px windows."""
    a, b = edges(ref), edges(aligned)
    # the mask file may be stored at half size; bring it to the W x H grid of the images (nearest keeps zones crisp)
    if mask.shape[:2] != (H, W):
        mask = cv2.resize(mask, (W, H), interpolation=cv2.INTER_NEAREST)
    zones = {'R': mask[:, :, 2], 'G': mask[:, :, 1], 'B': mask[:, :, 0], 'A': mask[:, :, 3]}
    win = cv2.createHanningWindow((WIN, WIN), cv2.CV_32F)
    out = {}
    for name, z in zones.items():
        z = cv2.dilate((z > 40).astype(np.uint8), np.ones((13, 13), np.uint8))
        worst, n, total = 0., 0, 0
        for y in range(0, H - WIN, WIN // 2):
            for x in range(0, W - WIN, WIN // 2):
                wa, wb = a[y:y + WIN, x:x + WIN], b[y:y + WIN, x:x + WIN]
                if z[y:y + WIN, x:x + WIN].mean() < .25 or wa.std() < .02:
                    continue
                total += 1
                (dx, dy), resp = cv2.phaseCorrelate(wa.copy(), wb.copy(), win)  # copies: phaseCorrelate windows its inputs in place
                if resp > .15 and _matches(wa, wb, dx, dy):
                    n += 1
                    worst = max(worst, float(np.hypot(dx, dy)))
        out[name] = {'shift': round(worst, 2), 'n': n, 'total': total, 'measured': total > 0 and n >= MIN_SHARE * total}
    return out


def problems(res, allow=''):
    """Reasons a check() result fails the variant (empty list = passes). A sky zone (B) that was not measured is left
    to a human looking at the overlay; R, G and A must have counted windows. Zones in `allow` may be shifted: a person
    looked at the overlay and accepted it (e.g. folds inside the banner repainted, its outline in place)."""
    out = [f'{k}: сдвиг {v["shift"]} px > {LIMIT}' for k, v in res.items() if v['shift'] > LIMIT and k not in allow]
    out += [f'{k}: нет учтённых окон' for k, v in res.items() if k in 'RGA' and v['n'] == 0 and v['total']]   # an empty zone (no river on the home) has nothing to measure
    return out


def show(res):
    return {k: (f'{v["shift"]} ({v["n"]}/{v["total"]})' if v['measured'] else f'не измерена ({v["n"]}/{v["total"]})') for k, v in res.items()}


def overlay(ref, aligned):
    e = (edges(ref) > .18).astype(np.uint8)
    out = aligned.copy()
    out[e > 0] = (74, 165, 201)   # gold #c9a54a in BGR: outlines of hero_dawn over the variant
    return out


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    art, tod = sys.argv[1], sys.argv[2]
    allow = ''.join(a.split('=', 1)[1] for a in sys.argv[3:] if a.startswith('--allow='))
    raws = [a for a in sys.argv[3:] if not a.startswith('--')] or sorted(glob.glob(os.path.join(art, f'hero_{tod}.raw*.jpg')))
    master = cv2.imread(os.path.join(art, 'hero_dawn.jpg'))
    ref = cv2.resize(master, (W, H), interpolation=cv2.INTER_AREA)
    mask = cv2.imread(MASK, cv2.IMREAD_UNCHANGED)
    best = None
    for p in raws:
        img = cv2.imread(p)
        T, cc = fit(ref, img)
        aligned = warp(img, T, (W, H))
        res = check(ref, aligned, mask)
        bad = problems(res, allow)
        ok = cc > .5 and not bad
        print(os.path.basename(p), ('ok' if ok else 'брак') + (f' (принято: {allow})' if ok and allow else ''), f'ecc={cc:.3f}', show(res), *bad)
        worst = max(v['shift'] for v in res.values())
        if ok and (best is None or worst < best[0]):
            best = (worst, aligned, img, T)
    if best is None:
        sys.exit(1)
    full = warp(best[2], best[3], (master.shape[1], master.shape[0]))   # the master's size: a 4K source stays 4K
    cv2.imwrite(os.path.join(art, f'hero_{tod}.jpg'), full, [cv2.IMWRITE_JPEG_QUALITY, 95])
    cv2.imwrite(os.path.join(art, f'hero_{tod}-overlay.png'), overlay(ref, best[1]))
    print(f'hero_{tod}.jpg ok, shift {best[0]} px')


if __name__ == '__main__':
    main()
