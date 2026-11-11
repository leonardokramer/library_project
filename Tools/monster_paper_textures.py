"""Generate the "old paper" monster skin textures (pure Python + Pillow).

Usage: python Tools/monster_paper_textures.py <out_folder>

T_MonsterPaper.png    tileable RGBA: R = crease (fold lines + crumple facet edges), G = foxing/stains,
                      B = ink veins, A = crumple facet shade (0..1, 0.5 = flat)
T_MonsterPaper_N.png  tileable tangent-space normal map (crumpled facets + folds)
T_MonsterText.png     tileable: R = typewriter ink (faded, uneven)
"""
import math, random, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = sys.argv[1]
S = 1024
rnd = random.Random(42)


def tile_noise(u, v, seed, octaves=5, maxf=6):
    """Tileable smooth noise from integer-frequency sines, roughly in [-1, 1]."""
    r = random.Random(seed)
    s = 0.0
    tot = 0.0
    for _ in range(octaves):
        fx, fy = r.randint(1, maxf), r.randint(-maxf, maxf)
        p = r.random() * 6.283
        a = 1.0 / math.sqrt(fx * fx + fy * fy)
        s += a * math.sin(2 * math.pi * (fx * u + fy * v) + p)
        tot += a
    return s / tot


def make_points(n, seed):
    r = random.Random(seed)
    return [[(r.random(), r.random(), r.random(), r.uniform(-1, 1), r.uniform(-1, 1)) for _ in range(n)] for _ in range(n)]


def voronoi(u, v, pts, n):
    x, y = u * n, v * n
    cx, cy = int(math.floor(x)), int(math.floor(y))
    f1 = f2 = 9.0
    best = None
    for oy in (-1, 0, 1):
        for ox in (-1, 0, 1):
            gx, gy = cx + ox, cy + oy
            px, py, val, gx2, gy2 = pts[gy % n][gx % n]
            dx = gx + px - x
            dy = gy + py - y
            d = math.sqrt(dx * dx + dy * dy)
            if d < f1:
                f2, f1 = f1, d
                best = (val, gx2, gy2, dx, dy)
            elif d < f2:
                f2 = d
    return f1, f2, best


# ---------- crumple facets, folds, ink veins, foxing ----------
NC = 7                      # crumple cells across the tile
PC = make_points(NC, 3)
NV = 4                      # ink vein network (coarse)
PV = make_points(NV, 9)
# long folds: tileable lines a*u + b*v = const (integer a, b)
FOLDS = [(1, 0, 0.31), (0, 1, 0.62), (1, 1, 0.17), (1, -2, 0.44), (2, 1, 0.83)]
# foxing spots
SPOTS = [(rnd.random(), rnd.random(), rnd.uniform(0.006, 0.025), rnd.uniform(0.4, 1.0)) for _ in range(70)]

H = [[0.0] * S for _ in range(S)]
img = Image.new('RGBA', (S, S))
px = img.load()
for j in range(S):
    v = (j + 0.5) / S
    for i in range(S):
        u = (i + 0.5) / S
        wx = tile_noise(u, v, 1, 4, 3) * 0.02
        wy = tile_noise(u, v, 2, 4, 3) * 0.02
        f1, f2, (val, ga, gb, dx, dy) = voronoi(u + wx, v + wy, PC, NC)
        # facet = tilted plane per cell
        facet = (ga * dx + gb * dy) * 0.6 + (val - 0.5) * 0.3
        edge = max(0.0, 1.0 - (f2 - f1) / 0.06) ** 2      # crumple crease
        fold = 0.0
        for a, b, c in FOLDS:
            t = (a * u + b * v - c) % 1.0
            d = min(t, 1.0 - t) * S / math.sqrt(a * a + b * b)  # px distance to the fold line
            fold = max(fold, max(0.0, 1.0 - d / 2.5))
            facet += 0.12 * (1.0 - min(1.0, d / 60.0))          # soft ridge along the fold
        crease = max(edge * 0.2, fold)
        # ink veins: thin edges of a warped coarse voronoi, broken up by a noise mask
        vx = tile_noise(u, v, 5, 5, 4) * 0.05
        vy = tile_noise(u, v, 6, 5, 4) * 0.05
        g1, g2, _ = voronoi(u + vx, v + vy, PV, NV)
        vein = max(0.0, 1.0 - (g2 - g1) / 0.035) ** 1.5
        brk = tile_noise(u, v, 7, 5, 5)
        vein *= max(0.0, min(1.0, (brk + 0.1) * 2.5))
        # foxing: soft blotches + spots
        fox = max(0.0, tile_noise(u, v, 8, 6, 4) * 1.3 - 0.35)
        for sx, sy, sr, sa in SPOTS:
            ddx = (u - sx + 0.5) % 1.0 - 0.5
            ddy = (v - sy + 0.5) % 1.0 - 0.5
            dd = math.sqrt(ddx * ddx + ddy * ddy)
            if dd < sr * 1.6:
                fox = max(fox, sa * max(0.0, 1.0 - dd / sr) ** 0.7)
        fox = min(1.0, fox)
        H[j][i] = facet * 0.6 - fold * 0.25 - edge * 0.05
        px[i, j] = (int(crease * 255), int(fox * 255), int(min(1.0, vein) * 255),
                    int(max(0.0, min(1.0, 0.5 + facet * 0.8)) * 255))
img.save(OUT + '/T_MonsterPaper.png')

# ---------- normal map ----------
nm = Image.new('RGB', (S, S))
npx = nm.load()
k = 6.0
for j in range(S):
    for i in range(S):
        dx = (H[j][(i + 1) % S] - H[j][(i - 1) % S]) * k
        dy = (H[(j + 1) % S][i] - H[(j - 1) % S][i]) * k
        dx = max(-1.5, min(1.5, dx)); dy = max(-1.5, min(1.5, dy))
        l = math.sqrt(dx * dx + dy * dy + 1.0)
        npx[i, j] = (int((-dx / l * 0.5 + 0.5) * 255), int((-dy / l * 0.5 + 0.5) * 255), int((1.0 / l * 0.5 + 0.5) * 255))
nm.save(OUT + '/T_MonsterPaper_N.png')

# ---------- typewriter text (tileable) ----------
LINES = [
    "RETURNED  15/07/1996  overdue  three days  no fine collected",
    "the reader did not come back for the second volume",
    "LOAN No. 0413   shelf 19   condition: water damaged",
    "pages missing between 112 and 140   reported by staff",
    "do not lend after closing   do not lend after closing",
    "borrowed by: ________   returned by: ________",
    "the card was signed twice in the same hand",
    "WITHDRAWN FROM CIRCULATION   see note on back cover",
    "he asked for the book that is not in the catalogue",
    "RESERVED   RESERVED   RESERVED   RESERVED",
]
T = Image.new('L', (S, S), 0)
d = ImageDraw.Draw(T)
font = ImageFont.truetype('C:/Windows/Fonts/cour.ttf', 22)
y = 6
li = 0
cw = font.getbbox('M')[2]
ncols = S // cw
step = S / ncols                       # exact wrap: ncols characters per tile width
while y < S:
    line = LINES[li % len(LINES)] + "    "
    li += 1
    off = rnd.randrange(len(line))
    fade = rnd.uniform(0.6, 1.0)
    for c in range(ncols):
        ch = line[(c + off) % len(line)]
        a = int(255 * fade * rnd.uniform(0.75, 1.0))
        jy = y + rnd.choice((0, 0, 0, 1, -1))
        x = c * step
        for ox in (0, -S):          # wrap horizontally
            d.text((x + ox, jy), ch, fill=a, font=font)
    y += 31
T = T.filter(ImageFilter.GaussianBlur(0.6))
tp = T.load()
# uneven ribbon: modulate by tileable noise
for j in range(S):
    for i in range(S):
        n = tile_noise(i / S, j / S, 11, 5, 5)
        tp[i, j] = int(tp[i, j] * max(0.0, min(1.0, 0.85 + n * 0.4)))
Image.merge('RGB', (T, T, T)).save(OUT + '/T_MonsterText.png')
print('ok')

# ---------- face mask for the paper look (head UV) ----------
# T_MonsterFaceMaskInk.png: R = eye sockets, G = mouth, B = ink drips running down from eyes and mouth corners,
# A = text emphasis (forehead)
M = 1024
fm = Image.new('RGBA', (M, M), (0, 0, 0, 0))
fr = Image.new('L', (M, M), 0); fg = Image.new('L', (M, M), 0); fb = Image.new('L', (M, M), 0); fa = Image.new('L', (M, M), 0)
dr, dg, db, da = (ImageDraw.Draw(x) for x in (fr, fg, fb, fa))
rr = random.Random(77)
eyes = [(0.378, 0.372), (0.622, 0.372)]
for ex, ey in eyes:
    # irregular dark socket: many overlapping blobs
    for _ in range(60):
        a = rr.random() * 6.283
        rad = rr.uniform(0.0, 1.0) ** 0.5
        cx = ex + math.cos(a) * 0.055 * rad
        cy = ey + math.sin(a) * 0.04 * rad + 0.004
        r = rr.uniform(0.012, 0.03)
        dr.ellipse([(cx - r) * M, (cy - r) * M, (cx + r) * M, (cy + r) * M], fill=255)
mx, my = 0.5, 0.583
dg.ellipse([(mx - 0.1) * M, (my - 0.042) * M, (mx + 0.1) * M, (my + 0.042) * M], fill=255)


def drip(x0, y0, length, width):
    """A wavy ink run going down (+V), tapering, with a drop at the end."""
    x, y = x0, y0
    steps = int(length * M)
    w = width
    for s in range(steps):
        t = s / steps
        x += rr.uniform(-0.6, 0.6) / M + math.sin(t * 9 + x0 * 50) * 0.25 / M
        y += 1.0 / M
        ww = w * (1.0 - 0.55 * t)
        db.ellipse([(x - ww) * M, (y - ww * 0.6) * M, (x + ww) * M, (y + ww * 0.6) * M], fill=int(255 * (1 - 0.25 * t)))
    r = w * 1.3
    db.ellipse([(x - r) * M, (y - r) * M, (x + r) * M, (y + r * 1.4) * M], fill=200)


for ex, ey in eyes:
    for k in range(rr.randint(3, 4)):
        drip(ex + rr.uniform(-0.035, 0.035), ey + 0.03, rr.uniform(0.08, 0.26), rr.uniform(0.008, 0.015))
for side in (-1, 1):
    for k in range(2):
        drip(mx + side * rr.uniform(0.085, 0.1), my + 0.01, rr.uniform(0.1, 0.25), rr.uniform(0.007, 0.012))
# text emphasis on the forehead
da.ellipse([0.3 * M, 0.08 * M, 0.7 * M, 0.27 * M], fill=255)
fr = fr.filter(ImageFilter.GaussianBlur(6))
fg = fg.filter(ImageFilter.GaussianBlur(5))
fb = fb.filter(ImageFilter.GaussianBlur(2.0))
fa = fa.filter(ImageFilter.GaussianBlur(25))
Image.merge('RGBA', (fr, fg, fb, fa)).save(OUT + '/T_MonsterFaceMaskInk.png')
print('facemask ok')
