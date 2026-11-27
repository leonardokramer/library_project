"""Gera as pecas da fachada da livraria (cornija, pilastra, faixa do letreiro, letras, toldo,
caixa de devolucao de livros) e exporta FBX.
Uso: blender -b -P library_facade.py -- <pasta_saida>
Unidades: metros. Origem de cada peca = face da parede (X=0), centro da fachada (Y=0), chao (Z=0),
exceto pilastra (origem no pe) e caixa de devolucao (origem no chao, centro).
+X sai da parede para a rua. Texto corre para +Y (lido de quem esta na rua).
"""
import bpy, bmesh, sys, os, math

out = sys.argv[sys.argv.index('--') + 1]
os.makedirs(out, exist_ok=True)

def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def mat(name, color):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    return m

def box(bm, x0, x1, y0, y1, z0, z1):
    vs = [bm.verts.new(v) for v in [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
                                    (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]]
    for f in [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]:
        bm.faces.new([vs[i] for i in f])

def extrude_profile(bm, prof, y0, y1, cap=True):
    """prof: lista (x, z) no sentido anti-horario visto de +Y. Extruda de y0 a y1."""
    a = [bm.verts.new((x, y0, z)) for x, z in prof]
    b = [bm.verts.new((x, y1, z)) for x, z in prof]
    n = len(prof)
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new([a[i], a[j], b[j], b[i]])
    if cap:
        bm.faces.new(list(reversed(a)))
        bm.faces.new(b)

def obj_from_bm(name, bm, material):
    me = bpy.data.meshes.new(name)
    bm.normal_update()
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    o.data.materials.append(material)
    return o

def uv_and_export(objs, fname):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:
        o.select_set(True)
        bpy.context.view_layer.objects.active = o
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.cube_project(cube_size=1.0)
        bpy.ops.object.mode_set(mode='OBJECT')
    for o in objs:
        o.select_set(True)
    if len(objs) > 1:
        bpy.context.view_layer.objects.active = objs[0]
        bpy.ops.object.join()
    bpy.ops.export_scene.fbx(filepath=os.path.join(out, fname + '.fbx'), use_selection=True,
                             apply_scale_options='FBX_SCALE_UNITS', mesh_smooth_type='FACE',
                             axis_forward='-Z', axis_up='Y', bake_space_transform=False)

TRIM = (0.80, 0.77, 0.68)
BAND = (0.06, 0.13, 0.10)
BRASS = (0.65, 0.50, 0.22)
CANVAS = (0.10, 0.20, 0.16)
METAL = (0.08, 0.08, 0.08)
BLUE = (0.07, 0.15, 0.27)

HALF = 4.70   # meia largura da fachada com as quinas

# ---------- cornija + friso + denticulos ----------
reset()
m = mat('M_Trim', TRIM)
bm = bmesh.new()
prof = [(0.0, 8.00), (0.06, 8.00), (0.06, 8.08), (0.12, 8.12), (0.16, 8.20), (0.24, 8.30),
        (0.36, 8.36), (0.40, 8.40), (0.40, 8.52), (0.0, 8.52)]
extrude_profile(bm, prof, -HALF - 0.40, HALF + 0.40)
box(bm, 0.0, 0.03, -HALF, HALF, 7.40, 8.00)             # friso
box(bm, 0.0, 0.05, -HALF, HALF, 7.34, 7.40)             # filete de baixo
y = -HALF + 0.05
while y < HALF - 0.08:
    box(bm, 0.0, 0.09, y, y + 0.07, 7.92, 8.00)         # denticulos
    y += 0.16
# parapeito acima da cornija (esconde o teto)
box(bm, -0.30, 0.06, -HALF, HALF, 8.52, 8.95)
box(bm, -0.30, 0.10, -HALF - 0.04, HALF + 0.04, 8.95, 9.02)
o = obj_from_bm('SM_Lib_Cornice', bm, m)
uv_and_export([o], 'SM_Lib_Cornice')

# ---------- pilastra (uma; usar nas duas quinas) ----------
reset()
m = mat('M_Trim', TRIM)
bm = bmesh.new()
W = 0.42
box(bm, 0.0, 0.08, -W / 2, W / 2, 0.10, 7.34)            # fuste
box(bm, 0.0, 0.13, -W / 2 - 0.03, W / 2 + 0.03, 0.10, 0.55)   # plinto
box(bm, 0.0, 0.11, -W / 2 - 0.02, W / 2 + 0.02, 0.55, 0.60)
box(bm, 0.0, 0.12, -W / 2 - 0.03, W / 2 + 0.03, 3.05, 3.12)   # capitel do terreo (alinha com a faixa)
box(bm, 0.0, 0.12, -W / 2 - 0.03, W / 2 + 0.03, 7.22, 7.34)   # capitel de cima
o = obj_from_bm('SM_Lib_Pilaster', bm, m)
uv_and_export([o], 'SM_Lib_Pilaster')

# ---------- faixa do letreiro ----------
reset()
mb = mat('M_Band', BAND); mt = mat('M_Trim', TRIM)
bm = bmesh.new()
box(bm, 0.0, 0.10, -4.25, 4.25, 3.14, 3.60)
o1 = obj_from_bm('Band', bm, mb)
bm = bmesh.new()
box(bm, 0.0, 0.15, -4.29, 4.29, 3.60, 3.67)              # capa
box(bm, 0.0, 0.13, -4.27, 4.27, 3.10, 3.14)              # filete
o2 = obj_from_bm('BandTrim', bm, mt)
uv_and_export([o1, o2], 'SM_Lib_SignBand')

# ---------- letras ----------
reset()
mbr = mat('M_Brass', BRASS)
bpy.ops.object.text_add(location=(0, 0, 0))
t = bpy.context.object
t.data.body = 'LANTERN  &  LETTERS'   # nome da loja (placa da porta do Stationer)
t.data.align_x = 'CENTER'
t.data.align_y = 'CENTER'
t.data.size = 0.33
t.data.extrude = 0.015
t.data.space_character = 1.12
# texto no plano YZ, virado para +X, correndo para +Y
t.rotation_euler = (math.radians(90), 0, math.radians(90))
t.location = (0.115, 0.0, 3.375)
bpy.ops.object.convert(target='MESH')
t.name = 'SM_Lib_SignLetters'
t.data.materials.clear(); t.data.materials.append(mbr)
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
uv_and_export([t], 'SM_Lib_SignLetters')

# ---------- toldo (sobre a vitrine e a porta) ----------
reset()
mc = mat('M_Canvas', CANVAS); mm = mat('M_Metal', METAL)
Y0, Y1 = -4.30, 4.18
Z0, OUT, DROP = 3.06, 1.10, 0.42
bm = bmesh.new()
# lona inclinada com espessura pequena
prof = [(0.0, Z0), (OUT, Z0 - DROP), (OUT, Z0 - DROP - 0.02), (0.0, Z0 - 0.02)]
extrude_profile(bm, prof, Y0, Y1)
# sanefa com recortes (bandeirolas)
nflap = 34
w = (Y1 - Y0) / nflap
for i in range(nflap):
    ya, yb = Y0 + i * w, Y0 + (i + 1) * w
    zb = Z0 - DROP - 0.22
    v = [bm.verts.new(p) for p in [(OUT, ya, Z0 - DROP), (OUT, yb, Z0 - DROP), (OUT, yb, zb + 0.05),
                                     (OUT, (ya + yb) / 2, zb), (OUT, ya, zb + 0.05)]]
    bm.faces.new(v)
    v2 = [bm.verts.new((p.co.x + 0.01, p.co.y, p.co.z)) for p in v]
    bm.faces.new(list(reversed(v2)))
# laterais triangulares
for yy in (Y0, Y1):
    v = [bm.verts.new(p) for p in [(0.0, yy, Z0), (OUT, yy, Z0 - DROP), (OUT, yy, Z0 - DROP - 0.22), (0.0, yy, Z0 - 0.30)]]
    bm.faces.new(v)
o1 = obj_from_bm('Canvas', bm, mc)
bm = bmesh.new()
for yy in (Y0 + 0.02, 0.0, Y1 - 0.02):
    # bracos de ferro
    steps = 10
    for k in range(steps):
        x0 = OUT * k / steps; x1 = OUT * (k + 1) / steps
        z0 = Z0 - 0.05 - DROP * k / steps; z1 = Z0 - 0.05 - DROP * (k + 1) / steps
        box(bm, x0, x1, yy - 0.012, yy + 0.012, z1 - 0.012, z0 + 0.012)
box(bm, OUT - 0.03, OUT, Y0, Y1, Z0 - DROP - 0.06, Z0 - DROP - 0.03)   # barra da frente
o2 = obj_from_bm('Frame', bm, mm)
uv_and_export([o1, o2], 'SM_Lib_Awning')

# ---------- caixa de devolucao de livros ----------
reset()
mbl = mat('M_BoxPaint', BLUE); mm = mat('M_Metal', METAL)
bm = bmesh.new()
D, Wd = 0.62, 0.78
box(bm, -D / 2, D / 2, -Wd / 2, Wd / 2, 0.18, 1.05)          # corpo
prof = [(-D / 2, 1.05), (D / 2, 1.05), (D / 2, 1.13), (-D / 2, 1.30)]   # tampa curva simplificada
prof = [(-D / 2 - 0.02, 1.05), (D / 2 + 0.02, 1.05), (D / 2 + 0.02, 1.12), (0.15, 1.24), (-0.10, 1.30), (-D / 2 - 0.02, 1.30)]
extrude_profile(bm, prof, -Wd / 2 - 0.02, Wd / 2 + 0.02)
o1 = obj_from_bm('Body', bm, mbl)
bm = bmesh.new()
for sx in (-1, 1):
    for sy in (-1, 1):
        box(bm, sx * D / 2 - 0.03, sx * D / 2 + 0.03, sy * Wd / 2 - 0.03, sy * Wd / 2 + 0.03, 0.0, 0.20)  # pes
box(bm, D / 2 - 0.01, D / 2 + 0.09, -0.24, 0.24, 0.86, 0.98)     # boca da devolucao (frente = +X)
box(bm, D / 2 + 0.05, D / 2 + 0.10, -0.20, 0.20, 0.97, 1.00)     # aba
box(bm, D / 2, D / 2 + 0.01, -0.22, 0.22, 0.55, 0.75)           # placa
o2 = obj_from_bm('Metal', bm, mm)
uv_and_export([o1, o2], 'SM_BookReturn')

print('DONE', out)

