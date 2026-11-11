"""Generate monster skin textures (pure Python + PIL).
T_MonsterCrack.png   tileable: R = crack depth (1 = deep crack), G = per-plate variation, B = fine crack
T_MonsterCrack_N.png tileable tangent-space normal map from the cracks
T_MonsterFaceMask.png head UV: R = eye sockets, G = mouth/lips, B = tear streaks under eyes
"""
import math, random, sys
from PIL import Image, ImageFilter

OUT = sys.argv[1]
S = 1024
random.seed(7)

def tile_warp(u, v, seed, amp):
    # tileable warp from integer-frequency sines
    r = random.Random(seed)
    terms = [(r.randint(1, 4), r.randint(1, 4), r.random() * 6.28, r.random() * 6.28) for _ in range(5)]
    dx = dy = 0.0
    for fx, fy, p1, p2 in terms:
        dx += math.sin(2 * math.pi * (fx * u + fy * v) + p1) / fx
        dy += math.sin(2 * math.pi * (fy * u - fx * v) + p2) / fy
    return dx * amp, dy * amp

def make_points(n, seed):
    r = random.Random(seed)
    return [[(r.random(), r.random(), r.random()) for _ in range(n)] for _ in range(n)]

def voronoi(u, v, pts, n):
    x, y = u * n, v * n
    cx, cy = int(x), int(y)
    f1 = f2 = 9.0
    id1 = 0.0
    for oy in (-1, 0, 1):
        for ox in (-1, 0, 1):
            gx, gy = cx + ox, cy + oy
            px, py, val = pts[gy % n][gx % n]
            dx = gx + px - x
            dy = gy + py - y
            d = math.sqrt(dx * dx + dy * dy)
            if d < f1:
                f2, f1, id1 = f1, d, val
            elif d < f2:
                f2 = d
    return f1, f2, id1

N1, N2 = 9, 23
P1, P2 = make_points(N1, 11), make_points(N2, 23)
crack = Image.new('RGB', (S, S))
H = [[0.0] * S for _ in range(S)]
px = crack.load()
for j in range(S):
    v = (j + 0.5) / S
    for i in range(S):
        u = (i + 0.5) / S
        wx, wy = tile_warp(u, v, 3, 0.022)
        f1, f2, cid = voronoi(u + wx, v + wy, P1, N1)
        e1 = (f2 - f1) * N1 / S * 1.0  # not used directly
        big = max(0.0, 1.0 - (f2 - f1) / 0.11)
        wx2, wy2 = tile_warp(u, v, 5, 0.012)
        g1, g2, _ = voronoi(u + wx2, v + wy2, P2, N2)
        fine = max(0.0, 1.0 - (g2 - g1) / 0.13)
        big = big ** 1.6
        fine = fine ** 2.2
        depth = max(big, fine * 0.6)
        H[j][i] = depth
        px[i, j] = (int(depth * 255), int(cid * 255), int(fine * 255))
crack.save(OUT + '/T_MonsterCrack.png')

# normal map from height (tileable Sobel)
nm = Image.new('RGB', (S, S))
npx = nm.load()
k = 3.0
for j in range(S):
    for i in range(S):
        hl = H[j][(i - 1) % S]; hr = H[j][(i + 1) % S]
        hu = H[(j - 1) % S][i]; hd = H[(j + 1) % S][i]
        dx = (hr - hl) * k
        dy = (hd - hu) * k
        nx, ny, nz = dx, dy, 1.0   # crack is a depression: height = -depth
        l = math.sqrt(nx * nx + ny * ny + nz * nz)
        npx[i, j] = (int((nx / l * 0.5 + 0.5) * 255), int((ny / l * 0.5 + 0.5) * 255), int((nz / l * 0.5 + 0.5) * 255))
nm.save(OUT + '/T_MonsterCrack_N.png')

# face mask in head UV space
M = 1024
mask = Image.new('RGB', (M, M))
mp = mask.load()
noise = Image.effect_noise((M, M), 60).filter(ImageFilter.GaussianBlur(10))
nz = noise.load()
eyes = [(0.378, 0.372), (0.622, 0.372)]
mouth = (0.5, 0.583)
def smooth(e0, e1, x):
    t = min(1.0, max(0.0, (x - e0) / (e1 - e0)))
    return t * t * (3 - 2 * t)
for j in range(M):
    v = (j + 0.5) / M
    for i in range(M):
        u = (i + 0.5) / M
        n = (nz[i, j] - 128) / 128.0
        er = 0.0
        tear = 0.0
        for ex, ey in eyes:
            dx = (u - ex) / 0.083
            dy = (v - ey) / (0.062 if v < ey else 0.085)
            d = math.sqrt(dx * dx + dy * dy) + n * 0.25
            er = max(er, 1.0 - smooth(0.55, 1.05, d))
            # tear streak running down from the lower lid
            sx = (u - ex - 0.01) / 0.012
            if v > ey:
                sy = (v - ey) / 0.16
                tear = max(tear, (1.0 - smooth(0.4, 1.0, abs(sx) + n * 0.3)) * (1.0 - smooth(0.2, 1.0, sy)))
        mx = (u - mouth[0]) / 0.105
        my = (v - mouth[1]) / 0.045
        dm = math.sqrt(mx * mx + my * my) + n * 0.2
        mr = 1.0 - smooth(0.6, 1.1, dm)
        mp[i, j] = (int(er * 255), int(mr * 255), int(tear * 255))
mask.save(OUT + '/T_MonsterFaceMask.png')
print('ok')
