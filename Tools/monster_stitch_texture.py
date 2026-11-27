"""Bookbinding stitch strip for the monster seams (spine, sternum, wrists) (Pillow).

Usage: python Tools/monster_stitch_texture.py <out_folder>

T_MonsterStitch.png  256x128, tiles along U (one stitch per tile), V = across the seam (0..1, seam at V 0.5).
  R = thread (waxed linen cross stitch), G = puncture holes + the cut line,
  B = pucker shading (paper pulled toward each puncture).
Mapped in M_MonsterPaperSkin by the "Custom" node StitchCoords (pre-skinned local position, not UV).
"""
import math, os, random, sys
from PIL import Image, ImageDraw, ImageFilter

OUT = sys.argv[1]
W, H = 256, 128
rnd = random.Random(11)
S = 4  # supersample
thread = Image.new('L', (W * S, H * S), 0)
holes = Image.new('L', (W * S, H * S), 0)
dt, dh = ImageDraw.Draw(thread), ImageDraw.Draw(holes)
cy = H * S / 2
# the cut the seam closes: a thin wavering line along U
pts = [(x, cy + math.sin(x / (W * S) * 2 * math.pi) * 2 * S) for x in range(0, W * S + 1, 8)]
dh.line(pts, fill=170, width=int(2.5 * S))
# one cross stitch per tile, with its four puncture holes
for ox in (-W * S, 0, W * S):  # draw neighbours so the tile wraps
    a, b = ox + 0.22 * W * S, ox + 0.78 * W * S
    top, bot = 0.16 * H * S, 0.84 * H * S
    for (x0, y0, x1, y1) in ((a, top, b, bot), (a, bot, b, top)):
        dt.line([x0, y0, x1, y1], fill=255, width=int(12 * S))
        dt.line([x0, y0, x1, y1], fill=205, width=int(5 * S))
    for (x, y) in ((a, top), (b, top), (a, bot), (b, bot)):
        r = 7 * S
        dh.ellipse([x - r, y - r, x + r, y + r], fill=255)
thread = thread.filter(ImageFilter.GaussianBlur(S * 0.8)).resize((W, H), Image.LANCZOS)
holes = holes.filter(ImageFilter.GaussianBlur(S * 0.8)).resize((W, H), Image.LANCZOS)
# pucker: soft dark halo around holes and along the cut
pucker = holes.filter(ImageFilter.GaussianBlur(7))
pucker = Image.eval(pucker, lambda v: min(255, int(v * 2.2)))
Image.merge('RGB', (thread, holes, pucker)).save(os.path.join(OUT, 'T_MonsterStitch.png'))
print('ok')
