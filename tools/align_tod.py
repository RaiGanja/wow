"""Variants of the home hero (day, dusk, night) made by editing hero_dawn in Gemini drift a few pixels; the living
layer's mask (assets/living/hero_dawn-fx.png) must fit all of them. Aligns a variant to hero_dawn by its edges
(lighting differs, outlines do not), then checks the residual shift inside every mask zone.
Run: python tools/align_tod.py <wow_art> <day|dusk|night> [raw files...]   (default raw: hero_<tod>.raw*.jpg)
Writes hero_<tod>.jpg (best aligned try) and hero_<tod>-overlay.png; exit code 1 when no try passes."""
import glob, os, sys
import cv2, numpy as np

W, H = 1376, 768
LIMIT = 2.0   # px: the most a mask zone may still be off
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


def check(ref, aligned, mask):
    """Largest leftover shift (px) inside each mask zone, by phase correlation of edge maps in 64 px windows."""
    a, b = edges(ref), edges(aligned)
    # the mask file may be stored at half size; bring it to the W x H grid of the images (nearest keeps zones crisp)
    if mask.shape[:2] != (H, W):
        mask = cv2.resize(mask, (W, H), interpolation=cv2.INTER_NEAREST)
    zones = {'R': mask[:, :, 2], 'G': mask[:, :, 1], 'B': mask[:, :, 0], 'A': mask[:, :, 3]}
    win = cv2.createHanningWindow((64, 64), cv2.CV_32F)
    out = {}
    for name, z in zones.items():
        z = cv2.dilate((z > 40).astype(np.uint8), np.ones((13, 13), np.uint8))
        worst = 0.
        for y in range(0, H - 64, 32):
            for x in range(0, W - 64, 32):
                if z[y:y + 64, x:x + 64].mean() < .25 or a[y:y + 64, x:x + 64].std() < .02:
                    continue
                (dx, dy), resp = cv2.phaseCorrelate(a[y:y + 64, x:x + 64], b[y:y + 64, x:x + 64], win)
                if resp > .15:
                    worst = max(worst, float(np.hypot(dx, dy)))
        out[name] = round(worst, 2)
    return out


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
        ok = cc > .5 and max(res.values()) <= LIMIT
        print(os.path.basename(p), 'ok' if ok else 'брак', f'ecc={cc:.3f}', res)
        if ok and (best is None or max(res.values()) < best[0]):
            best = (max(res.values()), aligned)
    if best is None:
        sys.exit(1)
    cv2.imwrite(os.path.join(art, f'hero_{tod}.jpg'), best[1], [cv2.IMWRITE_JPEG_QUALITY, 95])
    cv2.imwrite(os.path.join(art, f'hero_{tod}-overlay.png'), overlay(ref, best[1]))
    print(f'hero_{tod}.jpg ok, shift {best[0]} px')


if __name__ == '__main__':
    main()
