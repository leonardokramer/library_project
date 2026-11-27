"""Carrinho de devolucao de livros, capacho da entrada e as letras do letreiro (LANTERN & LETTERS).
Uso: blender -b -P library_props.py -- <pasta_saida>
Metros; origem no chao, centro. Lembrete: Blender +Y sai como UE -Y.
"""
import bpy, bmesh, sys, os, math

out = sys.argv[sys.argv.index('--') + 1]
os.makedirs(out, exist_ok=True)

def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def box(bm, x0, x1, y0, y1, z0, z1):
    vs = [bm.verts.new(v) for v in [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
                                    (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]]
    for f in [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]:
        bm.faces.new([vs[i] for i in f])

def slab(bm, x0, x1, y0, y1, z, tilt, th=0.018):
    """prateleira inclinada em torno do eixo Y (sobe para +X)."""
    za = z; zb = z + (x1 - x0) * math.tan(math.radians(tilt))
    pts = [(x0, y0, za), (x1, y0, zb), (x1, y1, zb), (x0, y1, za)]
    vs = [bm.verts.new(p) for p in pts] + [bm.verts.new((p[0], p[1], p[2] + th)) for p in pts]
    for f in [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]:
        bm.faces.new([vs[i] for i in f])

def part(name, matname, fill):
    bm = bmesh.new(); fill(bm)
    me = bpy.data.meshes.new(name)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(o)
    o.data.materials.append(bpy.data.materials.get(matname) or bpy.data.materials.new(matname))
    return o

def export(objs, fname, cube=1.0):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:
        bpy.context.view_layer.objects.active = o; o.select_set(True)
        bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.cube_project(cube_size=cube); bpy.ops.object.mode_set(mode='OBJECT'); o.select_set(False)
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    if len(objs) > 1: bpy.ops.object.join()
    bpy.ops.export_scene.fbx(filepath=os.path.join(out, fname + '.fbx'), use_selection=True,
                             apply_scale_options='FBX_SCALE_UNITS', mesh_smooth_type='FACE')

# ---- carrinho de devolucao: 0,92 x 0,44 x 1,00 m, prateleiras dos dois lados em V ----
reset()
L, D, H = 0.92, 0.44, 1.00
hl, hd = L / 2, D / 2
def wood(bm):
    box(bm, -hd, hd, -hl, -hl + 0.025, 0.12, H)          # laterais (cabeceiras)
    box(bm, -hd, hd, hl - 0.025, hl, 0.12, H)
    box(bm, -hd, hd, -hl, hl, 0.12, 0.16)                # base
    box(bm, -0.012, 0.012, -hl, hl, 0.16, 0.92)          # divisoria central
    for z in (0.40, 0.68):                               # prateleiras inclinadas em V (lombadas para fora)
        slab(bm, -hd, -0.012, -hl + 0.025, hl - 0.025, z + 0.05, -12)
        slab(bm, 0.012, hd, -hl + 0.025, hl - 0.025, z, 12)
    box(bm, -hd - 0.01, hd + 0.01, -hl - 0.01, hl + 0.01, H, H + 0.03)   # tampo
    box(bm, -0.02, 0.02, -hl - 0.06, -hl - 0.03, 0.80, 0.84)             # puxador
    box(bm, -0.02, 0.02, -hl - 0.06, -hl - 0.01, 0.80, 0.84)
o1 = part('Wood', 'M_CartWood', wood)
def metal(bm):
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = sx * (hd - 0.05), sy * (hl - 0.06)
            box(bm, x - 0.035, x + 0.035, y - 0.012, y + 0.012, 0.0, 0.07)   # rodinha
            box(bm, x - 0.02, x + 0.02, y - 0.02, y + 0.02, 0.07, 0.12)      # garfo
o2 = part('Metal', 'M_Metal', metal)
export([o1, o2], 'SM_ReturnCart', 0.5)

# ---- capacho da entrada: 1,40 x 0,90 ----
reset()
def mat(bm):
    box(bm, -0.45, 0.45, -0.70, 0.70, 0.0, 0.012)
o = part('Mat', 'M_DoorMat', mat)
export([o], 'SM_DoorMat', 0.5)

# ---- letras do letreiro ----
reset()
bpy.ops.object.text_add(location=(0, 0, 0))
t = bpy.context.object
t.data.body = 'LANTERN  &  LETTERS'
t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'
t.data.size = 0.33; t.data.extrude = 0.015; t.data.space_character = 1.10
t.rotation_euler = (math.radians(90), 0, math.radians(90))
t.location = (0.115, 0.0, 3.375)
bpy.ops.object.convert(target='MESH')
t.name = 'SM_Lib_SignLetters'
t.data.materials.clear(); t.data.materials.append(bpy.data.materials.new('M_Brass'))
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
export([t], 'SM_Lib_SignLetters', 1.0)
print('DONE')
