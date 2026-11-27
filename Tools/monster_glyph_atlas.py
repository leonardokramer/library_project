"""Typewriter glyph atlas for writing on the monster skin at runtime (Pillow).

Usage: python Tools/monster_glyph_atlas.py <out_folder>

T_MonsterGlyphs.png  512x512, 16 x 8 cells of 32 x 64 px, white glyph on black (R = ink).
Cell index i = position of the character in CHARSET below (col = i % 16, row = i // 16).
BP_ScareManager.SkinCharset must hold EXACTLY the same string (same order).
The glyph is centered horizontally; the baseline is at y = 46 in every cell.
Font: Tools/fonts/CourierPrime/CourierPrime-Regular.ttf (OFL).
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

CHARSET = (" ABCDEFGHIJKLMNOPQRSTUVWXYZ"
           "abcdefghijklmnopqrstuvwxyz"
           "0123456789"
           ".,:;-/()_#*'"
           "ÁÀÂÃÉÊÍÓÔÕÚÇ"
           "áàâãéêíóôõúçüº"
           "·!?\"")

if __name__ == '__main__':
    OUT = sys.argv[1]
    HERE = os.path.dirname(os.path.abspath(__file__))
    FONT = os.path.join(HERE, 'fonts', 'CourierPrime', 'CourierPrime-Regular.ttf')
    assert len(CHARSET) <= 128, len(CHARSET)
    CW, CH, BASE = 32, 64, 46
    f = ImageFont.truetype(FONT, 42)
    img = Image.new('L', (512, 512), 0)
    d = ImageDraw.Draw(img)
    for i, ch in enumerate(CHARSET):
        cx, cy = (i % 16) * CW, (i // 16) * CH
        w = d.textlength(ch, font=f)
        d.text((cx + (CW - w) / 2, cy + BASE), ch, fill=255, font=f, anchor='ls')
    Image.merge('RGB', (img, img, img)).save(os.path.join(OUT, 'T_MonsterGlyphs.png'))
    print(len(CHARSET), 'glyphs')
    print(CHARSET)
