"""SVG path sampling for the crest: glyph bounding boxes (tools/make_crest.py) and shape outlines (content/guilds.py)."""
import math, re

ARGS = {'M': 2, 'L': 2, 'H': 1, 'V': 1, 'C': 6, 'S': 4, 'Q': 4, 'T': 2, 'A': 7, 'Z': 0}


def paths(svg):
    ds = re.findall(r'<path[^>]*\sd="([^"]+)"', svg)
    return [d for d in ds if not re.fullmatch(r'M0 0h512v512H0z', d.strip())]


def tokens(d):
    """Commands and numbers; arc flags may be glued to the next number (a5 5 0 011 1)."""
    out = re.findall(r'[A-Za-z]|[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?', d)
    res, k, cmd = [], 0, ''
    while k < len(out):
        t = out[k]
        if t.isalpha():
            cmd, k = t, k + 1
            if cmd in 'zZ':
                res.append((cmd, []))
            continue
        n = ARGS[cmd.upper()]
        if cmd in 'aA':
            vals, j = [], k
            while len(vals) < 7:
                s = out[j]
                if len(vals) in (3, 4) and len(s) > 1 and s[0] in '01':
                    vals.append(float(s[0]))
                    out[j] = s[1:]
                    continue
                vals.append(float(s))
                j += 1
            k = j
        else:
            vals, k = [float(x) for x in out[k:k + n]], k + n
        res.append((cmd, vals))
        if cmd == 'm':
            cmd = 'l'
        elif cmd == 'M':
            cmd = 'L'
    return res


def points(d, n=24):
    """The outline as points: lines as their ends, curves and arcs at n points each."""
    pts, x, y, sx, sy, cx, cy = [], 0.0, 0.0, 0.0, 0.0, None, None
    for cmd, v in tokens(d):
        rel, C = cmd.islower(), cmd.upper()
        ox, oy = (x, y) if rel else (0.0, 0.0)
        if C == 'Z':
            x, y, cx = sx, sy, None
            continue
        if C == 'M':
            x, y = ox + v[0], oy + v[1]
            sx, sy, cx = x, y, None
            pts.append((x, y))
        elif C == 'L':
            x, y, cx = ox + v[0], oy + v[1], None
            pts.append((x, y))
        elif C == 'H':
            x, cx = (x + v[0]) if rel else v[0], None
            pts.append((x, y))
        elif C == 'V':
            y, cx = (y + v[0]) if rel else v[0], None
            pts.append((x, y))
        elif C in 'CS':
            if C == 'C':
                x1, y1, x2, y2, ex, ey = ox + v[0], oy + v[1], ox + v[2], oy + v[3], ox + v[4], oy + v[5]
            else:
                x1, y1 = (2 * x - cx, 2 * y - cy) if cx is not None else (x, y)
                x2, y2, ex, ey = ox + v[0], oy + v[1], ox + v[2], oy + v[3]
            for i in range(1, n + 1):
                t = i / n
                a, b, c, e = (1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t * t, t ** 3
                pts.append((a * x + b * x1 + c * x2 + e * ex, a * y + b * y1 + c * y2 + e * ey))
            x, y, cx, cy = ex, ey, x2, y2
        elif C in 'QT':
            raise ValueError('quadratic curves are not used by the charges')
        elif C == 'A':
            rx, ry, phi, fa, fs, ex, ey = abs(v[0]), abs(v[1]), math.radians(v[2]), v[3], v[4], ox + v[5], oy + v[6]
            pts += arc(x, y, rx, ry, phi, fa, fs, ex, ey, n)
            x, y, cx = ex, ey, None
    return pts


def bbox(d):
    """Bounding box of the sampled outline: accurate to well under a unit of 512."""
    pts = points(d)
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


def arc(x1, y1, rx, ry, phi, fa, fs, x2, y2, n):
    """SVG endpoint arc -> sampled points (the W3C center parameterization)."""
    if not rx or not ry:
        return [(x2, y2)]
    c, s = math.cos(phi), math.sin(phi)
    dx, dy = (x1 - x2) / 2, (y1 - y2) / 2
    xp, yp = c * dx + s * dy, -s * dx + c * dy
    lam = xp * xp / (rx * rx) + yp * yp / (ry * ry)
    if lam > 1:
        rx, ry = rx * math.sqrt(lam), ry * math.sqrt(lam)
    num = rx * rx * ry * ry - rx * rx * yp * yp - ry * ry * xp * xp
    k = math.sqrt(max(0, num / (rx * rx * yp * yp + ry * ry * xp * xp)))
    if fa == fs:
        k = -k
    cxp, cyp = k * rx * yp / ry, -k * ry * xp / rx
    ccx, ccy = c * cxp - s * cyp + (x1 + x2) / 2, s * cxp + c * cyp + (y1 + y2) / 2
    ang = lambda ux, uy, vx, vy: math.atan2(ux * vy - uy * vx, ux * vx + uy * vy)
    t1 = ang(1, 0, (xp - cxp) / rx, (yp - cyp) / ry)
    dt = ang((xp - cxp) / rx, (yp - cyp) / ry, (-xp - cxp) / rx, (-yp - cyp) / ry)
    if not fs and dt > 0:
        dt -= 2 * math.pi
    elif fs and dt < 0:
        dt += 2 * math.pi
    out = []
    for i in range(1, n + 1):
        t = t1 + dt * i / n
        out.append((ccx + rx * math.cos(t) * c - ry * math.sin(t) * s, ccy + rx * math.cos(t) * s + ry * math.sin(t) * c))
    return out


