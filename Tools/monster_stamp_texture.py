"""Rubber stamp "VENCIDO" for the monster's forehead (Pillow).

Usage: python Tools/monster_stamp_texture.py <out_folder>

T_MonsterStamp.png  512x256, R = stamp ink (white = ink, uneven pressure, worn holes).
                    The bottom strip inside the frame (y 168..228) is left empty: the date is
                    drawn there at runtime (BP_ScareManager.WriteSkin into RT_MonsterStamp).
Font: Tools/fonts/CourierPrime (OFL).
"""
import os, random, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
BOLD = os.path.join(HERE, 'fonts', 'CourierPrime', 'CourierPrime-Bold.ttf')
W, H = 512, 256
rnd = random.Random(7)

img = Image.new('L', (W, H), 0)
d = ImageDraw.Draw(img)
# double frame
d.rectangle([10, 10, W - 11, H - 11], outline=255, width=9)
d.rectangle([24, 24, W - 25, H - 25], outline=255, width=3)
# word
f = ImageFont.truetype(BOLD, 92)
bb = d.textbbox((0, 0), 'VENCIDO', font=f)
tw, th = bb[2] - bb[0], bb[3] - bb[1]
d.text(((W - tw) / 2 - bb[0], (24 + 160 - th) / 2 - bb[1]), 'VENCIDO', fill=255, font=f)
# thin rule above the date strip
d.line([40, 160, W - 41, 160], fill=255, width=3)

px = img.load()
# uneven pressure: stronger on the left/top, fading to the lower right
for y in range(H):
    for x in range(W):
        if px[x, y]:
            p = 1.0 - 0.45 * (x / W) * 0.7 - 0.3 * (y / H)
            p *= rnd.uniform(0.82, 1.0)
            px[x, y] = int(px[x, y] * max(0.0, min(1.0, p)))
# worn holes (rubber missing ink)
holes = Image.new('L', (W, H), 255)
hd = ImageDraw.Draw(holes)
for _ in range(260):
    x, y = rnd.uniform(0, W), rnd.uniform(0, H)
    r = rnd.uniform(1.0, 4.5)
    hd.ellipse([x - r, y - r, x + r, y + r], fill=0)
for _ in range(6):  # a few long scratches
    x, y = rnd.uniform(0, W), rnd.uniform(0, H)
    hd.line([x, y, x + rnd.uniform(-90, 90), y + rnd.uniform(-12, 12)], fill=0, width=2)
holes = holes.filter(ImageFilter.GaussianBlur(0.8))
img = Image.composite(img, Image.new('L', (W, H), 0), holes)
img = img.filter(ImageFilter.GaussianBlur(0.7))
Image.merge('RGB', (img, img, img)).save(os.path.join(OUT, 'T_MonsterStamp.png'))
print('stamp ok')
