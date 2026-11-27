"""Main Street: predios comerciais de tijolo (casca), placas, toldos, escadas de incendio, hotel,
cinema e caixa-d'agua. Exporta um FBX por peca.
Uso: blender -b -P main_street.py -- <pasta_saida> [nome1 nome2 ...]
Metros. Fachada em X=0 (+X = rua), centro da largura em Y=0, chao Z=0, fundo em X=-D.
Blender +Y = UE -Y (texto corre para +Y para ler certo da rua).
Slots de material (o UE troca pelo nome): Brick, Trim, Stone, Glass, WinLit, Board, Frame, Interior,
SignBand, Roof, Metal, Letters, Neon, Awning, Bulb, Tank.
Referencias e regras: docs/TOWN_ART_PASS.md ("Main Street").
"""
import bpy, bmesh, sys, os, math, random

argv = sys.argv[sys.argv.index('--') + 1:]
OUT = argv[0]
ONLY = set(argv[1:])
os.makedirs(OUT, exist_ok=True)
FONT_SERIF = r'C:\Windows\Fonts\georgiab.ttf'
FONT_SANS = r'C:\Windows\Fonts\arialbd.ttf'

GF = 4.3      # altura do terreo
UF = 3.5      # altura dos andares de cima
WALL = 0.32   # espessura das paredes

# ---------------------------------------------------------------- utilidades
class Mesh:
    def __init__(self):
        self.parts = {}   # slot -> bmesh

    def bm(self, slot):
        if slot not in self.parts:
            self.parts[slot] = bmesh.new()
        return self.parts[slot]

    def box(self, slot, x0, x1, y0, y1, z0, z1):
        if x0 > x1: x0, x1 = x1, x0
        if y0 > y1: y0, y1 = y1, y0
        if z0 > z1: z0, z1 = z1, z0
        if x1 - x0 < 1e-4 or y1 - y0 < 1e-4 or z1 - z0 < 1e-4:
            return
        bm = self.bm(slot)
        vs = [bm.verts.new(v) for v in [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
                                        (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]]
        for f in [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]:
            bm.faces.new([vs[i] for i in f])

    def cyl(self, slot, cx, cy, z0, z1, r, seg=16, cap=True, r1=None):
        r1 = r if r1 is None else r1
        bm = self.bm(slot)
        bot = [bm.verts.new((cx + r * math.cos(2 * math.pi * i / seg), cy + r * math.sin(2 * math.pi * i / seg), z0)) for i in range(seg)]
        top = [bm.verts.new((cx + r1 * math.cos(2 * math.pi * i / seg), cy + r1 * math.sin(2 * math.pi * i / seg), z1)) for i in range(seg)]
        for i in range(seg):
            j = (i + 1) % seg
            bm.faces.new([bot[i], bot[j], top[j], top[i]])
        if cap:
            bm.faces.new(list(reversed(bot)))
            if r1 > 1e-3:
                bm.faces.new(top)

    def cone(self, slot, cx, cy, z0, z1, r, seg=16):
        bm = self.bm(slot)
        bot = [bm.verts.new((cx + r * math.cos(2 * math.pi * i / seg), cy + r * math.sin(2 * math.pi * i / seg), z0)) for i in range(seg)]
        tip = bm.verts.new((cx, cy, z1))
        for i in range(seg):
            bm.faces.new([bot[i], bot[(i + 1) % seg], tip])
        bm.faces.new(list(reversed(bot)))

    def add_object(self, slot, obj):
        """junta um objeto (ex.: texto convertido) no slot"""
        bm = self.bm(slot)
        me = obj.data
        tmp = bmesh.new(); tmp.from_mesh(me)
        tmp.transform(obj.matrix_world)
        m = bpy.data.meshes.new('tmp'); tmp.to_mesh(m); tmp.free()
        bm.from_mesh(m)
        bpy.data.meshes.remove(m)
        bpy.data.objects.remove(obj)

    def export(self, name):
        if ONLY and name not in ONLY:
            return
        objs = []
        for slot, bm in self.parts.items():
            bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
            me = bpy.data.meshes.new(name + '_' + slot)
            bm.to_mesh(me); bm.free()
            o = bpy.data.objects.new(name + '_' + slot, me)
            bpy.context.collection.objects.link(o)
            m = bpy.data.materials.get(slot) or bpy.data.materials.new(slot)
            o.data.materials.append(m)
            objs.append(o)
        bpy.ops.object.select_all(action='DESELECT')
        for o in objs:
            bpy.context.view_layer.objects.active = o
            o.select_set(True)
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.uv.cube_project(cube_size=2.0)
            bpy.ops.object.mode_set(mode='OBJECT')
            o.select_set(False)
        for o in objs:
            o.select_set(True)
        bpy.context.view_layer.objects.active = objs[0]
        bpy.ops.object.join()
        bpy.ops.export_scene.fbx(filepath=os.path.join(OUT, name + '.fbx'), use_selection=True,
                                 apply_scale_options='FBX_SCALE_UNITS', mesh_smooth_type='FACE')
        bpy.ops.object.delete()
        print('exported', name)

def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def text_obj(body, size, font, extrude=0.02, bevel=0.0):
    cu = bpy.data.curves.new('t', 'FONT')
    cu.body = body
    cu.font = bpy.data.fonts.load(font, check_existing=True)
    cu.size = size
    cu.extrude = extrude
    cu.bevel_depth = bevel
    cu.align_x = 'CENTER'; cu.align_y = 'CENTER'
    o = bpy.data.objects.new('t', cu)
    bpy.context.collection.objects.link(o)
    bpy.context.view_layer.objects.active = o
    o.select_set(True)
    bpy.ops.object.convert(target='MESH')
    o = bpy.context.view_layer.objects.active
    o.select_set(False)
    return o

def wall_with_holes(m, slot, x0, x1, y0, y1, z0, z1, holes, axis='x'):
    """parede plana (axis x: plano em x, cobre y0..y1 x z0..z1) com furos [(a0,a1,z0,z1)]
    (a = y para axis x; a = x para axis y)"""
    a0, a1 = (y0, y1)
    cuts = sorted(set([a0, a1] + [h[0] for h in holes] + [h[1] for h in holes]))
    cuts = [c for c in cuts if a0 <= c <= a1]
    for i in range(len(cuts) - 1):
        c0, c1 = cuts[i], cuts[i + 1]
        mid = (c0 + c1) / 2
        zs = sorted([(h[2], h[3]) for h in holes if h[0] <= mid <= h[1]])
        z = z0
        for (hz0, hz1) in zs:
            if hz0 > z:
                seg = (z, hz0)
                if axis == 'x': m.box(slot, x0, x1, c0, c1, *seg)
                else: m.box(slot, c0, c1, x0, x1, *seg)
            z = max(z, hz1)
        if z < z1:
            if axis == 'x': m.box(slot, x0, x1, c0, c1, z, z1)
            else: m.box(slot, c0, c1, x0, x1, z, z1)

# ---------------------------------------------------------------- predio comercial
def window(m, xf, ya, yb, za, zb, state, rec=0.12, side=None):
    """janela na fachada (plano x=xf, normal +X). state: G vidro escuro, L acesa, B tabuas, D escura aberta, S persiana"""
    gx = xf - rec
    if state == 'L':
        m.box('WinLit', gx - 0.02, gx, ya, yb, za, zb)
    elif state == 'B':
        m.box('Board', gx + 0.02, gx + 0.06, ya - 0.02, yb + 0.02, za - 0.02, zb + 0.02)
        m.box('Glass', gx - 0.02, gx, ya, yb, za, zb)
    elif state == 'D':
        m.box('Interior', gx - 0.6, gx - 0.58, ya, yb, za, zb)
    elif state == 'S':
        m.box('Glass', gx - 0.02, gx, ya, yb, za, zb)
        m.box('Trim', gx - 0.06, gx - 0.04, ya, yb, za + (zb - za) * 0.45, zb)   # persiana meio baixada
    else:
        m.box('Glass', gx - 0.02, gx, ya, yb, za, zb)
    if state in ('G', 'L', 'S'):
        # caixilho: travessa e montante
        zm = za + (zb - za) * 0.52
        m.box('Frame', gx, gx + 0.04, ya, yb, zm - 0.03, zm + 0.03)
        m.box('Frame', gx, gx + 0.04, (ya + yb) / 2 - 0.025, (ya + yb) / 2 + 0.025, za, zb)
    # revestimento interno do vao (sem frestas)
    m.box('Trim', gx - 0.02, xf, ya - 0.02, ya, za, zb)
    m.box('Trim', gx - 0.02, xf, yb, yb + 0.02, za, zb)
    # peitoril e verga
    m.box('Trim', xf - 0.05, xf + 0.09, ya - 0.08, yb + 0.08, za - 0.12, za)
    m.box('Trim', xf - 0.02, xf + 0.05, ya - 0.12, yb + 0.12, zb, zb + 0.22)

def commercial(name, W, floors, seed, D=12.0, cornice='bracket', shop='display', entry='center',
               side_windows=None, roof_items=True, parapet=1.3, upper=None, lit_shop=False):
    """side_windows: None, '+y', '-y' ou 'both' (predio de esquina)"""
    reset()
    rnd = random.Random(seed)
    m = Mesh()
    hw = W / 2
    H = GF + UF * (floors - 1)
    top = H + parapet
    bays = max(2, round(W / 3.8))
    # ---- fachada (x = 0 .. -WALL)
    holes = []
    pil = 0.45
    holes.append((-hw + pil, hw - pil, 0.0, 3.65))                    # vitrine do terreo
    win_w, win_h = 1.15, 2.15
    upper = upper or ''
    states = []
    for f in range(1, floors):
        zf = GF + UF * (f - 1)
        for b in range(bays):
            yc = -hw + W * (b + 0.5) / bays
            holes.append((yc - win_w / 2, yc + win_w / 2, zf + 0.85, zf + 0.85 + win_h))
            if upper:
                st = upper[(len(states)) % len(upper)]
            else:
                st = rnd.choices('GLBDS', weights=[46, 12, 20, 10, 12])[0]
            states.append((yc, zf, st))
    wall_with_holes(m, 'Brick', -WALL, 0.0, -hw, hw, -0.05, top, holes)
    for (yc, zf, st) in states:
        window(m, 0.0, yc - win_w / 2, yc + win_w / 2, zf + 0.85, zf + 0.85 + win_h, st)
    # ---- laterais, fundo, telhado (paredes cheias; se esquina, com janelas)
    def side(ysgn):
        yw = ysgn * hw
        hs = []
        if side_windows in (('+y' if ysgn > 0 else '-y'), 'both'):
            sb = max(2, int((D - 2) / 3.2))
            for f in range(floors):
                zf = 0 if f == 0 else GF + UF * (f - 1)
                for b in range(sb):
                    xc = -1.2 - (D - 2.4) * (b + 0.5) / sb
                    z0 = zf + (0.9 if f else 0.7); z1 = z0 + (win_h if f else 2.6)
                    hs.append((xc - win_w / 2, xc + win_w / 2, z0, z1))
        y0, y1 = (yw - WALL, yw) if ysgn > 0 else (yw, yw + WALL)
        # parede lateral (plano em y)
        wall_with_holes(m, 'Brick', y0, y1, -D, -WALL + 0.01, -0.05, top, hs, axis='y')
        for (a0, a1, z0, z1) in hs:
            st = rnd.choices('GLBDS', weights=[50, 10, 22, 8, 10])[0]
            gy = (y1 - 0.12) if ysgn > 0 else (y0 + 0.12)
            sl = 'WinLit' if st == 'L' else ('Interior' if st == 'D' else 'Glass')
            m.box(sl, a0, a1, gy - 0.01, gy + 0.01, z0, z1)
            if st == 'B':
                ob = (y1 + 0.03) if ysgn > 0 else (y0 - 0.03)
                m.box('Board', a0 - 0.02, a1 + 0.02, ob - 0.02, ob + 0.02, z0 - 0.02, z1 + 0.02)
            out = y1 if ysgn > 0 else y0
            m.box('Trim', a0 - 0.08, a1 + 0.08, out - 0.05 * ysgn, out + 0.09 * ysgn, z0 - 0.12, z0)
            m.box('Trim', a0 - 0.12, a1 + 0.12, out - 0.02 * ysgn, out + 0.05 * ysgn, z1, z1 + 0.22)
    side(+1); side(-1)
    m.box('Brick', -D - 0.01, -D + WALL, -hw, hw, -0.05, top)          # fundo
    m.box('Roof', -D, -WALL, -hw + WALL, hw - WALL, H - 0.25, H)       # laje
    m.box('Trim', -D - 0.02, 0.02, -hw - 0.02, hw + 0.02, top, top + 0.12)   # rufo do parapeito
    # ---- cornija
    if cornice == 'bracket':
        m.box('Trim', 0.0, 0.55, -hw - 0.15, hw + 0.15, top - 0.55, top - 0.25)
        m.box('Trim', 0.0, 0.35, -hw - 0.1, hw + 0.1, top - 0.75, top - 0.55)
        n = int(W / 0.9)
        for i in range(n + 1):
            yy = -hw + W * i / n
            m.box('Trim', 0.0, 0.42, yy - 0.08, yy + 0.08, top - 1.05, top - 0.55)
    elif cornice == 'stepped':
        m.box('Brick', 0.0, 0.12, -hw, hw, top - 0.9, top - 0.75)
        m.box('Brick', 0.0, 0.22, -hw, hw, top - 0.75, top - 0.6)
        m.box('Trim', 0.0, 0.3, -hw - 0.05, hw + 0.05, top - 0.25, top)
        for i in range(int(W / 0.6) + 1):
            yy = -hw + 0.3 + i * 0.6
            if yy < hw - 0.2:
                m.box('Brick', 0.0, 0.1, yy - 0.12, yy + 0.12, top - 1.1, top - 0.9)
    else:   # simples
        m.box('Trim', 0.0, 0.3, -hw - 0.05, hw + 0.05, top - 0.35, top)
    # cinta entre o terreo e o primeiro andar
    m.box('Trim', 0.0, 0.1, -hw, hw, GF - 0.05, GF + 0.12)
    # pilastras do terreo
    m.box('Brick', 0.0, 0.12, -hw, -hw + pil, 0, GF - 0.05)
    m.box('Brick', 0.0, 0.12, hw - pil, hw, 0, GF - 0.05)
    m.box('Stone', -0.05, 0.16, -hw, -hw + pil + 0.02, 0, 0.5)
    m.box('Stone', -0.05, 0.16, hw - pil - 0.02, hw, 0, 0.5)
    # ---- vitrine
    sw0, sw1 = -hw + pil, hw - pil
    m.box('SignBand', -0.05, 0.08, sw0, sw1, 3.65, GF - 0.05)         # faixa do letreiro
    m.box('Trim', 0.0, 0.12, sw0, sw1, 3.55, 3.65)
    rec = 0.35
    ew = 1.25; ed = 1.1
    if entry == 'center':
        e0 = -ew / 2
    elif entry == 'left':
        e0 = sw0 + 0.25            # Blender -Y = direita de quem olha da rua... so muda o lado
    else:
        e0 = sw1 - 0.25 - ew
    e1 = e0 + ew
    gx = -rec
    glass_slot = 'WinLit' if lit_shop else 'Glass'
    m.box('Interior', -3.2, -3.0, sw0, sw1, 0, 3.55)                   # fundo escuro da loja
    m.box('Interior', -3.2, gx, sw0, sw1, 3.5, 3.55)                   # forro
    m.box('Interior', -3.2, gx, sw0, sw1, 0.0, 0.02)
    for (a, b) in ((sw0, e0), (e1, sw1)):
        if b - a < 0.2:
            continue
        if shop == 'boarded':
            m.box('Board', gx, gx + 0.05, a, b, 0.0, 3.5)
        else:
            m.box('Frame', gx - 0.05, gx + 0.05, a, b, 0.0, 0.6)           # rodape (kickplate)
            m.box(glass_slot, gx - 0.02, gx, a, b, 0.6, 2.95)
            m.box('Frame', gx - 0.04, gx + 0.04, a, b, 2.95, 3.05)
            m.box(glass_slot, gx - 0.02, gx, a, b, 3.05, 3.5)                # bandeira (transom)
            nm = max(1, int((b - a) / 1.6))
            for i in range(1, nm):
                yy = a + (b - a) * i / nm
                m.box('Frame', gx - 0.03, gx + 0.03, yy - 0.025, yy + 0.025, 0.6, 3.5)
            m.box('Frame', gx - 0.04, gx + 0.04, a, a + 0.06, 0.0, 3.5)
            m.box('Frame', gx - 0.04, gx + 0.04, b - 0.06, b, 0.0, 3.5)
    # entrada recuada
    m.box('Frame', gx - ed, gx, e0 - 0.04, e0, 0.0, 3.5)
    m.box('Frame', gx - ed, gx, e1, e1 + 0.04, 0.0, 3.5)
    if shop == 'boarded':
        m.box('Board', gx - ed, gx - ed + 0.05, e0, e1, 0, 3.5)
    else:
        m.box('Frame', gx - ed - 0.06, gx - ed, e0, e1, 0, 3.5)
        m.box(glass_slot, gx - ed, gx - ed + 0.02, e0 + 0.12, e1 - 0.12, 0.9, 2.3)
        m.box('Glass', gx - ed + 0.02, gx - ed + 0.03, e0, e1, 2.45, 3.4)
    m.box('Stone', gx - ed, 0.12, e0, e1, -0.02, 0.03)                  # soleira
    m.box('Interior', gx - ed, gx, e0, e1, 3.45, 3.5)
    # ---- telhado: caixas, chamine, antena
    if roof_items:
        for i in range(rnd.randint(1, 3)):
            k = rnd.random()
            x = -rnd.uniform(2.5, D - 2.0); y = rnd.uniform(-hw + 1.2, hw - 1.2)
            if k < 0.45:
                m.box('Metal', x - 0.8, x + 0.8, y - 0.6, y + 0.6, H, H + rnd.uniform(0.8, 1.3))
            elif k < 0.75:
                m.box('Brick', x - 0.35, x + 0.35, y - 0.35, y + 0.35, H, top + rnd.uniform(0.8, 2.0))
            else:
                m.cyl('Metal', x, y, H, H + rnd.uniform(3.0, 5.0), 0.03, seg=6)
                m.box('Metal', x - 0.02, x + 0.02, y - 0.6, y + 0.6, H + 2.8, H + 2.84)
    m.export(name)

# ---------------------------------------------------------------- pecas avulsas
def sign_band_text(name, text, width, font=FONT_SERIF, h=0.42, slot='Letters'):
    """letras sobre a faixa (centro em y=0, z=0; o UE posiciona em z 3,97 m, x +0,08)"""
    reset()
    m = Mesh()
    t = text_obj(text, h, font, extrude=0.025)
    t.rotation_euler = (math.radians(90), 0, math.radians(90))
    bpy.context.view_layer.update()
    d = t.dimensions
    if d.x > width:
        s = width / d.x
        t.scale = (s, s, s)
        bpy.context.view_layer.update()
    t.location = (0.03, 0, 0)
    bpy.context.view_layer.update()
    m.add_object(slot, t)
    m.export(name)

def neon_sign(name, text, h=0.6, font=FONT_SANS, box_pad=0.25):
    """letreiro de neon com caixa de metal atras (centro y=0, base z=0)"""
    reset()
    m = Mesh()
    t = text_obj(text, h, font, extrude=0.03, bevel=0.012)
    t.rotation_euler = (math.radians(90), 0, math.radians(90))
    bpy.context.view_layer.update()
    w = t.dimensions.y
    t.location = (0.14, 0, h / 2 + box_pad)
    bpy.context.view_layer.update()
    m.add_object('Neon', t)
    m.box('Metal', 0.0, 0.08, -w / 2 - box_pad, w / 2 + box_pad, 0, h + 2 * box_pad)
    m.box('Metal', 0.0, 0.11, -w / 2 - box_pad, w / 2 + box_pad, 0, 0.05)
    m.export(name)

def blade_sign(name, text, letter_h=0.62, font=FONT_SANS, neon=True, arm=0.5):
    """placa vertical saindo da fachada (base em z=0, encosta em x=0, sai para +X)"""
    reset()
    m = Mesh()
    n = len(text)
    Hs = n * letter_h * 1.25 + 0.6
    Wb = letter_h * 1.6
    x0, x1 = arm, arm + Wb
    m.box('Metal', x0, x1, -0.14, 0.14, 0, Hs)
    m.box('Frame', x0 - 0.05, x1 + 0.05, -0.16, 0.16, Hs, Hs + 0.08)
    m.box('Frame', x0 - 0.05, x1 + 0.05, -0.16, 0.16, -0.08, 0)
    m.box('Metal', 0.0, arm, -0.05, 0.05, 0.4, 0.5)
    m.box('Metal', 0.0, arm, -0.05, 0.05, Hs - 0.5, Hs - 0.4)
    for face in (+1, -1):
        for i, ch in enumerate(text):
            if ch == ' ':
                continue
            t = text_obj(ch, letter_h, font, extrude=0.03, bevel=0.01 if neon else 0.0)
            # face +Y (le de quem vem do sul no UE? as duas faces tem letras)
            t.rotation_euler = (math.radians(90), 0, math.radians(180) if face > 0 else 0)
            bpy.context.view_layer.update()
            t.location = ((x0 + x1) / 2, face * 0.17, Hs - 0.3 - letter_h * 1.25 * (i + 0.5))
            bpy.context.view_layer.update()
            m.add_object('Neon' if neon else 'Letters', t)
    m.export(name)

def awning(name, W, depth=1.3, drop=0.35):
    """toldo inclinado (x=0 na fachada, topo z=0; o UE coloca em z ~3,55)"""
    reset()
    m = Mesh()
    bm = m.bm('Awning')
    hw = W / 2
    p = [(0, -hw, 0), (0, hw, 0), (depth, hw, -0.75), (depth, -hw, -0.75)]
    v = [bm.verts.new(q) for q in p]
    bm.faces.new(v); bm.faces.new(list(reversed([bm.verts.new(q) for q in p])))
    # aba
    q = [(depth, -hw, -0.75), (depth, hw, -0.75), (depth, hw, -0.75 - drop), (depth, -hw, -0.75 - drop)]
    v = [bm.verts.new(a) for a in q]
    bm.faces.new(v); bm.faces.new(list(reversed([bm.verts.new(a) for a in q])))
    for s in (-1, 1):
        r = [(0, s * hw, 0), (depth, s * hw, -0.75), (depth, s * hw, -0.75 - drop)]
        v = [bm.verts.new(a) for a in r]
        bm.faces.new(v); bm.faces.new(list(reversed([bm.verts.new(a) for a in r])))
    m.box('Metal', 0, depth, -hw, -hw + 0.03, -0.78, -0.75)
    m.box('Metal', 0, depth, hw - 0.03, hw, -0.78, -0.75)
    m.export(name)

def fire_escape(name, floors, L=3.2):
    """escada de incendio na lateral (encosta em y=0, sai para +y; x de -L-1 a -1; 1o patamar no 2o andar)"""
    reset()
    m = Mesh()
    xa, xb = -1.0 - L, -1.0
    for f in range(1, floors):
        z = GF + UF * (f - 1) + 0.05
        m.box('Metal', xa, xb, 0.0, 1.1, z - 0.05, z)
        for (y0, y1) in ((1.05, 1.1),):
            m.box('Metal', xa, xb, y0, y1, z + 0.95, z + 1.0)
            m.box('Metal', xa, xb, y0, y1, z + 0.45, z + 0.48)
        for i in range(int(L / 0.6) + 1):
            xx = xa + i * (L / int(L / 0.6))
            m.box('Metal', xx - 0.015, xx + 0.015, 1.06, 1.1, z, z + 1.0)
        m.box('Metal', xa - 0.015, xa + 0.015, 0.0, 1.1, z + 0.95, z + 1.0)
        m.box('Metal', xb - 0.015, xb + 0.015, 0.0, 1.1, z + 0.95, z + 1.0)
        # lance para o patamar de cima (diagonal em degraus)
        if f < floors - 1:
            n = 12
            for i in range(n):
                xx = xa + 0.3 + (L - 0.9) * i / n
                zz = z + UF * i / n
                m.box('Metal', xx, xx + 0.25, 0.15, 0.85, zz, zz + 0.04)
            m.box('Metal', xa + 0.3, xb - 0.6, 0.12, 0.15, z, z + UF)
        # suportes
        m.box('Metal', xa, xa + 0.05, 0.0, 1.0, z - 0.6, z - 0.05)
        m.box('Metal', xb - 0.05, xb, 0.0, 1.0, z - 0.6, z - 0.05)
    # escada de mao recolhida sob o 1o patamar
    z = GF + 0.05
    m.box('Metal', xb - 0.6, xb - 0.56, 0.3, 0.33, z - 2.4, z)
    m.box('Metal', xb - 0.6, xb - 0.56, 0.7, 0.73, z - 2.4, z)
    for i in range(7):
        m.box('Metal', xb - 0.6, xb - 0.56, 0.3, 0.73, z - 2.3 + i * 0.32, z - 2.28 + i * 0.32)
    m.export(name)

def hotel(name, W=28.0, floors=5, D=16.0, seed=5):
    """hotel antigo de 5 andares (fecha a ponta norte da rua)"""
    commercial(name, W, floors, seed, D=D, cornice='bracket', shop='display', entry='center',
               side_windows='both', parapet=1.8, lit_shop=True,
               upper='GGBGLGDGGSGBGGGLGGBGGDGGGSGBGG')

def theater(name, W=20.0, D=24.0):
    """cinema velho: fachada alta lisa, marquise com lampadas e letreiro de letras soltas"""
    reset()
    m = Mesh()
    hw = W / 2
    top = 13.0
    holes = [(-hw + 1.0, hw - 1.0, 0, 3.4), (-1.2, 1.2, 6.0, 10.5)]
    wall_with_holes(m, 'Brick', -WALL, 0, -hw, hw, -0.05, top, holes)
    window(m, 0.0, -1.2, 1.2, 6.0, 10.5, 'G')
    m.box('Brick', -24, -24 + WALL, -hw, hw, -0.05, top)
    m.box('Brick', -24, -WALL, -hw, -hw + WALL, -0.05, top)
    m.box('Brick', -24, -WALL, hw - WALL, hw, -0.05, top)
    m.box('Roof', -24, -WALL, -hw, hw, top - 1.5, top - 1.2)
    m.box('Stone', 0, 0.35, -hw - 0.2, hw + 0.2, top - 0.6, top)
    m.box('Stone', 0, 0.2, -hw - 0.1, hw + 0.1, top - 1.0, top - 0.6)
    for yy in (-hw + 0.4, hw - 0.4, -4.0, 4.0):
        m.box('Stone', 0, 0.25, yy - 0.4, yy + 0.4, 3.4, top - 1.0)
    # bilheteria e portas (fundo escuro)
    m.box('Interior', -3.0, -2.9, -hw + 1, hw - 1, 0, 3.4)
    m.box('Frame', -0.6, -0.4, -hw + 1, hw - 1, 0, 0.5)
    for yy in (-6, -3, 3, 6):
        m.box('Glass', -0.42, -0.4, yy - 1.2, yy + 1.2, 0.5, 3.0)
    m.box('Frame', -1.6, 0.2, -1.0, 1.0, 0, 2.6)                          # bilheteria
    m.box('Glass', 0.2, 0.22, -0.8, 0.8, 1.0, 2.2)
    # marquise
    mz0, mz1 = 3.6, 5.2
    m.box('Frame', 0, 3.2, -hw + 0.5, hw - 0.5, mz0, mz0 + 0.25)
    m.box('SignBand', 2.9, 3.2, -hw + 0.8, hw - 0.8, mz0 + 0.25, mz1)       # quadro de letras (branco)
    m.box('Frame', 2.85, 3.25, -hw + 0.5, hw - 0.5, mz1, mz1 + 0.2)
    m.box('Frame', 2.85, 3.25, -hw + 0.5, hw - 0.5, mz0 + 0.2, mz0 + 0.3)
    for yy in (-hw + 0.5, hw - 0.5):
        m.box('Frame', 0, 3.25, yy - 0.15, yy + 0.15, mz0, mz1 + 0.2)
    m.box('Metal', 0, 3.0, -hw + 0.8, hw - 0.8, mz1 + 0.2, mz1 + 0.25)
    rnd = random.Random(7)
    for i in range(int((W - 2) / 0.45)):
        yy = -hw + 1.0 + i * 0.45
        for zz in (mz0 + 0.05,):
            slot = 'Bulb' if rnd.random() < 0.55 else 'Frame'
            m.box(slot, 3.1, 3.3, yy - 0.06, yy + 0.06, zz - 0.12, zz)
    for i, word in enumerate(('CLOSED', 'FOR SEASON')):
        t = text_obj(word, 0.42, FONT_SANS, extrude=0.02)
        t.rotation_euler = (math.radians(90), 0, math.radians(90))
        bpy.context.view_layer.update()
        t.location = (3.22, 0, mz1 - 0.42 - i * 0.6)
        bpy.context.view_layer.update()
        m.add_object('Letters', t)
    m.export(name)

def water_tower(name):
    reset()
    m = Mesh()
    R = 4.2; zt = 22.0
    for (x, y) in ((3, 3), (-3, 3), (3, -3), (-3, -3)):
        m.cyl('Metal', x, y, 0, zt, 0.22, seg=8)
    for z in (5.5, 11, 16.5):
        for (a, b) in (((3, 3), (-3, 3)), ((-3, 3), (-3, -3)), ((-3, -3), (3, -3)), ((3, -3), (3, 3))):
            x0, y0 = a; x1, y1 = b
            m.box('Metal', min(x0, x1) - 0.06, max(x0, x1) + 0.06, min(y0, y1) - 0.06, max(y0, y1) + 0.06, z, z + 0.12)
    # diagonais finas
    for (a, b) in (((3, 3), (-3, 3)), ((-3, 3), (-3, -3)), ((-3, -3), (3, -3)), ((3, -3), (3, 3))):
        for z0 in (0.5, 5.6, 11.1, 16.6):
            n = 10
            for i in range(n):
                t = i / n
                x = a[0] + (b[0] - a[0]) * t; y = a[1] + (b[1] - a[1]) * t
                z = z0 + 5.0 * t
                m.box('Metal', x - 0.05, x + 0.05, y - 0.05, y + 0.05, z, z + 0.55)
    m.cyl('Metal', 0, 0, 0, zt + 1, 0.3, seg=8)                     # cano central
    m.box('Metal', -4.6, 4.6, -4.6, 4.6, zt, zt + 0.25)              # passarela
    m.cyl('Metal', 0, 0, zt + 0.25, zt + 1.3, R + 0.5, seg=24, cap=False)  # guarda-corpo (aro)
    m.cyl('Tank', 0, 0, zt + 0.25, zt + 6.5, R, seg=32)
    m.cone('Tank', 0, 0, zt + 6.5, zt + 9.0, R + 0.15, seg=32)
    m.cyl('Metal', 0, 0, zt + 9.0, zt + 9.6, 0.25, seg=8)
    m.export(name)

def barricade(name):
    """cavalete de obra listrado + placa ROAD CLOSED"""
    reset()
    m = Mesh()
    for y in (-1.1, 1.1):
        for x in (-0.3, 0.3):
            m.box('Frame', x - 0.04, x + 0.04, y - 0.04, y + 0.04, 0, 1.1)
    m.box('Awning', -0.03, 0.03, -1.3, 1.3, 0.85, 1.1)
    m.box('Awning', -0.03, 0.03, -1.3, 1.3, 0.45, 0.65)
    m.box('SignBand', 0.03, 0.06, -0.7, 0.7, 1.15, 1.75)
    m.box('Frame', -0.02, 0.03, -0.05, 0.05, 1.0, 1.75)
    t = text_obj('ROAD\nCLOSED', 0.2, FONT_SANS, extrude=0.01)
    t.rotation_euler = (math.radians(90), 0, math.radians(90))
    bpy.context.view_layer.update()
    t.location = (0.065, 0, 1.45)
    bpy.context.view_layer.update()
    m.add_object('Letters', t)
    m.export(name)

# ---------------------------------------------------------------- catalogo
B = [
    # nome, largura, andares, semente, extras
    ('SM_MS_B076_2a', 7.6, 2, 11, dict(cornice='bracket', entry='left')),
    ('SM_MS_B076_2b', 7.6, 2, 12, dict(cornice='stepped', entry='right', shop='boarded')),
    ('SM_MS_B076_3a', 7.6, 3, 13, dict(cornice='bracket', entry='right')),
    ('SM_MS_B076_4a', 7.6, 4, 14, dict(cornice='simple', entry='left', parapet=1.0)),
    ('SM_MS_B114_2a', 11.4, 2, 21, dict(cornice='stepped', entry='center', lit_shop=True)),
    ('SM_MS_B114_3a', 11.4, 3, 22, dict(cornice='bracket', entry='center')),
    ('SM_MS_B114_3b', 11.4, 3, 23, dict(cornice='simple', entry='left', shop='boarded')),
    ('SM_MS_B114_4a', 11.4, 4, 24, dict(cornice='bracket', entry='right', parapet=1.6)),
    ('SM_MS_B152_2a', 15.2, 2, 31, dict(cornice='bracket', entry='center')),
    ('SM_MS_B152_3a', 15.2, 3, 32, dict(cornice='stepped', entry='right')),
    ('SM_MS_B152_4a', 15.2, 4, 33, dict(cornice='bracket', entry='center', parapet=1.8)),
    # esquinas (janelas na lateral; o UE espelha quando precisa)
    ('SM_MS_C114_3a', 11.4, 3, 41, dict(cornice='bracket', entry='right', side_windows='+y', D=14.0)),
    ('SM_MS_C152_2a', 15.2, 2, 42, dict(cornice='stepped', entry='left', side_windows='+y', D=14.0)),
    ('SM_MS_C152_4a', 15.2, 4, 43, dict(cornice='bracket', entry='center', side_windows='+y', D=16.0, parapet=1.6)),
]
SIGNS = [   # texto pintado na faixa do letreiro (larguras cabem nos lotes)
    ('SM_MS_Sign_Pharmacy', 'PHARMACY', 9.0), ('SM_MS_Sign_Hardware', 'HARDWARE', 9.0),
    ('SM_MS_Sign_Barber', 'BARBER SHOP', 6.0), ('SM_MS_Sign_Bakery', 'BAKERY', 6.0),
    ('SM_MS_Sign_Pawn', 'PAWN & LOAN', 6.0), ('SM_MS_Sign_ShoeRepair', 'SHOE REPAIR', 6.0),
    ('SM_MS_Sign_FiveDime', '5 & 10', 9.0), ('SM_MS_Sign_TVRepair', 'TV & RADIO REPAIR', 9.0),
    ('SM_MS_Sign_Florist', 'FLORIST', 6.0), ('SM_MS_Sign_Tailor', 'TAILOR', 6.0),
    ('SM_MS_Sign_Furniture', 'FURNITURE', 13.0), ('SM_MS_Sign_Bank', 'FIRST NATIONAL BANK', 13.0),
    ('SM_MS_Sign_Hotel', 'HOTEL', 9.0), ('SM_MS_Sign_Insurance', 'INSURANCE', 9.0),
    ('SM_MS_Sign_Records', 'RECORDS', 6.0), ('SM_MS_Sign_Diner', 'DINER', 9.0),
]

def main():
    for (n, W, F, s, kw) in B:
        commercial(n, W, F, s, **kw)
    for (n, t, w) in SIGNS:
        sign_band_text(n, t, w)
    neon_sign('SM_MS_Neon_Diner', 'DINER', h=0.7)
    neon_sign('SM_MS_Neon_Open', 'OPEN', h=0.35, box_pad=0.1)
    blade_sign('SM_MS_Blade_Hotel', 'HOTEL', letter_h=0.8)
    blade_sign('SM_MS_Blade_State', 'STATE', letter_h=0.9)
    blade_sign('SM_MS_Blade_Pawn', 'PAWN', letter_h=0.5, neon=False, arm=0.35)
    blade_sign('SM_MS_Blade_Bar', 'BAR', letter_h=0.55, arm=0.35)
    for w in (6.7, 10.5, 14.3):
        awning('SM_MS_Awning_%03d' % int(w * 10), w)
    for f in (3, 4, 5):
        fire_escape('SM_MS_FireEscape_%d' % f, f)
    hotel('SM_MS_Hotel')
    theater('SM_MS_Theater')
    water_tower('SM_MS_WaterTower')
    barricade('SM_MS_Barricade')

main()
