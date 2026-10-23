"""Variants of the home hero (day, dusk, night) made by editing hero_dawn in Gemini drift a few pixels; the living
layer's mask (assets/living/hero_dawn-fx.png) must fit all of them. Aligns a variant to hero_dawn by its edges
(lighting differs, outlines do not), then checks the residual shift inside every mask zone.
Run: python tools/align_tod.py <wow_art> <day|dusk|night> [raw files...]   (default raw: hero_<tod>.raw*.jpg)
Writes hero_<tod>.jpg (best aligned try) and hero_<tod>-overlay.png; exit code 1 when no try passes."""
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


def align(ref, img):
    """Warp img onto ref (affine, then homography if that fits better). Returns (aligned BGR W x H, ECC score)."""
    img = cv2.resize(img, (W, H), interpolation=cv2.INTER_AREA)
    a, b = edges(ref), edges(img)
    best = (img, -1.)
    crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-6)
    for mode, eye in ((cv2.MOTION_AFFINE, np.eye(2, 3, dtype=np.float32)), (cv2.MOTION_HOMOGRAPHY, np.eye(3, dtype=np.float32))):
        try:
            cc, M = cv2.findTransformECC(a, b, eye, mode, crit, None, 5)
        except cv2.error:
            continue
        flags = cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP
        out = (cv2.warpAffine(img, M, (W, H), flags=flags, borderMode=cv2.BORDER_REFLECT) if mode == cv2.MOTION_AFFINE
               else cv2.warpPerspective(img, M, (W, H), flags=flags, borderMode=cv2.BORDER_REFLECT))
        if cc > best[1]:
            best = (out, cc)
    return best


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


def problems(res):
    """Reasons a check() result fails the variant (empty list = passes). A sky zone (B) that was not measured is left
    to a human looking at the overlay; R, G and A must have counted windows."""
    out = [f'{k}: сдвиг {v["shift"]} px > {LIMIT}' for k, v in res.items() if v['shift'] > LIMIT]
    out += [f'{k}: нет учтённых окон' for k, v in res.items() if k in 'RGA' and v['n'] == 0]
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
    raws = sys.argv[3:] or sorted(glob.glob(os.path.join(art, f'hero_{tod}.raw*.jpg')))
    ref = cv2.resize(cv2.imread(os.path.join(art, 'hero_dawn.jpg')), (W, H), interpolation=cv2.INTER_AREA)
    mask = cv2.imread(MASK, cv2.IMREAD_UNCHANGED)
    best = None
    for p in raws:
        aligned, cc = align(ref, cv2.imread(p))
        res = check(ref, aligned, mask)
        bad = problems(res)
        ok = cc > .5 and not bad
        print(os.path.basename(p), 'ok' if ok else 'брак', f'ecc={cc:.3f}', show(res), *bad)
        worst = max(v['shift'] for v in res.values())
        if ok and (best is None or worst < best[0]):
            best = (worst, aligned)
    if best is None:
        sys.exit(1)
    cv2.imwrite(os.path.join(art, f'hero_{tod}.jpg'), best[1], [cv2.IMWRITE_JPEG_QUALITY, 95])
    cv2.imwrite(os.path.join(art, f'hero_{tod}-overlay.png'), overlay(ref, best[1]))
    print(f'hero_{tod}.jpg ok, shift {best[0]} px')


if __name__ == '__main__':
    main()
