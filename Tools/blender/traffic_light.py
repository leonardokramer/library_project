"""Semaforo pendurado (anos 80/90): caixa amarela com 3 lentes e visores, gancho no topo.
Uso: blender -b -P traffic_light.py -- <pasta_saida>
Metros. Origem no gancho (topo). Lentes viradas para +X e -X (dois lados).
"""
import bpy, bmesh, sys, os, math
out = sys.argv[sys.argv.index('--') + 1]
os.makedirs(out, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)

def box(bm, x0, x1, y0, y1, z0, z1):
    vs = [bm.verts.new(v) for v in [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
                                    (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]]
    for f in [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]:
        bm.faces.new([vs[i] for i in f])

def disc(bm, x, z, r, n=16, th=0.01, sgn=1):
    c0 = bm.verts.new((x, 0, z)); c1 = bm.verts.new((x + sgn * th, 0, z))
    ring0 = [bm.verts.new((x, r * math.cos(2 * math.pi * i / n), z + r * math.sin(2 * math.pi * i / n))) for i in range(n)]
    ring1 = [bm.verts.new((x + sgn * th, v.co.y, v.co.z)) for v in ring0]
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new([c1, ring1[i], ring1[j]])
        bm.faces.new([ring0[i], ring0[j], ring1[j], ring1[i]])

def part(name, mat, fill):
    bm = bmesh.new(); fill(bm)
    me = bpy.data.meshes.new(name); bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(o)
    o.data.materials.append(bpy.data.materials.get(mat) or bpy.data.materials.new(mat))
    return o

W, D, H = 0.32, 0.30, 0.98
zs = (-0.27, -0.57, -0.87)  # centros das lentes (abaixo do gancho)
def body(bm):
    box(bm, -D / 2, D / 2, -W / 2, W / 2, -1.04, -0.06)
    box(bm, -0.02, 0.02, -0.02, 0.02, -0.08, 0.0)       # gancho
    for s in (1, -1):
        for z in zs:   # visores
            box(bm, s * D / 2, s * (D / 2 + 0.16), -0.13, 0.13, z + 0.11, z + 0.13)
            box(bm, s * D / 2, s * (D / 2 + 0.13), -0.13, -0.11, z - 0.11, z + 0.13)
            box(bm, s * D / 2, s * (D / 2 + 0.13), 0.11, 0.13, z - 0.11, z + 0.13)
o1 = part('Body', 'M_TLBody', body)
lenses = []
for k, z in enumerate(zs):
    name = ('M_LensRed', 'M_LensAmber', 'M_LensGreen')[k]
    def fill(bm, z=z):
        for s in (1, -1):
            disc(bm, s * (D / 2 + 0.001), z, 0.105, sgn=s)
    lenses.append(part('Lens%d' % k, name, fill))
objs = [o1] + lenses
bpy.ops.object.select_all(action='DESELECT')
for o in objs:
    bpy.context.view_layer.objects.active = o; o.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.cube_project(cube_size=0.5); bpy.ops.object.mode_set(mode='OBJECT'); o.select_set(False)
for o in objs: o.select_set(True)
bpy.context.view_layer.objects.active = o1
bpy.ops.object.join()
bpy.ops.export_scene.fbx(filepath=os.path.join(out, 'SM_TrafficLight.fbx'), use_selection=True,
                         apply_scale_options='FBX_SCALE_UNITS', mesh_smooth_type='FACE')
print('DONE')
