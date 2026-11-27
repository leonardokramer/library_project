"""Mask of the MetaHuman underwear painted on the monster body texture (body UV).

Usage: python Tools/monster_underwear_mask.py <body_bc_thumbnail.png> <out_folder>

Input: 256x256 thumbnail of T_Body_BC_VT (EditorAppToolset.CaptureAssetImage). The underwear is the only
low-saturation (gray) area of the baked body color. The left half is mirrored onto the right half because the
thumbnail carries a "VT" badge in the lower right corner (the body UV is symmetric).
Output: T_MonsterUnderwearMask.png 1024x1024, white = underwear (dilated and softened so the edge seam vanishes).
"""
import colorsys, os, sys
from PIL import Image, ImageFilter

src, out = sys.argv[1], sys.argv[2]
im = Image.open(src).convert('RGB')
W, H = im.size
p = im.load()
m = Image.new('L', (W, H))
q = m.load()
for y in range(H):
    for x in range(W // 2):
        r, g, b = [c / 255 for c in p[x, y]]
        s = colorsys.rgb_to_hsv(r, g, b)[1]
        v = 255 if s < 0.12 else 0
        q[x, y] = v
        q[W - 1 - x, y] = v
# back waistband: a thin dark line across the middle of the UV (not gray, so add it by hand; thumbnail px)
from PIL import ImageDraw
ImageDraw.Draw(m).rectangle([104, 99, 151, 107], fill=255)
m = m.filter(ImageFilter.MaxFilter(5))          # dilate ~2 px of the thumbnail (~64 texels)
m = m.resize((1024, 1024), Image.BILINEAR).filter(ImageFilter.GaussianBlur(6))
Image.merge('RGB', (m, m, m)).save(os.path.join(out, 'T_MonsterUnderwearMask.png'))
print('ok')
