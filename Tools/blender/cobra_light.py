"""Luminaria de rua classica (braco curvo + cabeca 'cobra' com lente acesa embaixo) para prender no poste.
Origem no ponto de fixacao no poste; o braco sai para +X. Lente (slot M_Lens) virada para baixo em x ~ 1.75 m.
Uso: blender -b -P cobra_light.py -- <pasta_saida>
"""
import bpy, bmesh, sys, os, math
out = sys.argv[sys.argv.index('--') + 1]
os.makedirs(out, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
import mathutils

def mat(n):
    return bpy.data.materials.get(n) or bpy.data.materials.new(n)

def obj(name, bm, m):
    me = bpy.data.meshes.new(name); bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(o); o.data.materials.append(mat(m)); return o

# braco: tubo curvo (segmentos de cilindro) subindo e saindo para +X
bm = bmesh.new()
pts = [(0.0, 0.0), (0.35, 0.18), (0.8, 0.30), (1.3, 0.33), (1.6, 0.30)]
for (x0, z0), (x1, z1) in zip(pts, pts[1:]):
    L = math.hypot(x1 - x0, z1 - z0); ang = math.atan2(z1 - z0, x1 - x0)
    M = mathutils.Matrix.Translation(((x0 + x1) / 2, 0, (z0 + z1) / 2)) @ mathutils.Matrix.Rotation(-ang + math.pi / 2, 4, 'Y')
    bmesh.ops.create_cone(bm, cap_ends=True, segments=10, radius1=0.035, radius2=0.035, depth=L + 0.02, matrix=M)
# abracadeira no poste
bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=0.06, radius2=0.06, depth=0.14, matrix=mathutils.Matrix.Translation((0, 0, 0)))
arm = obj('Arm', bm, 'M_Metal')
# cabeca: casco achatado (escala de um cubo chanfrado)
bm = bmesh.new()
bmesh.ops.create_cube(bm, size=1.0, matrix=mathutils.Matrix.Translation((1.78, 0, 0.27)) @ mathutils.Matrix.Diagonal((0.62, 0.30, 0.13, 1)))
for v in bm.verts:
    if v.co.x > 1.9:
        v.co.z -= 0.03; v.co.y *= 0.8
head = obj('Head', bm, 'M_Head')
# lente acesa embaixo
bm = bmesh.new()
bmesh.ops.create_cube(bm, size=1.0, matrix=mathutils.Matrix.Translation((1.80, 0, 0.195)) @ mathutils.Matrix.Diagonal((0.46, 0.22, 0.02, 1)))
lens = obj('Lens', bm, 'M_Lens')
objs = [arm, head, lens]
bpy.ops.object.select_all(action='DESELECT')
for o in objs:
    bpy.context.view_layer.objects.active = o; o.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.cube_project(cube_size=0.5); bpy.ops.object.mode_set(mode='OBJECT'); o.select_set(False)
for o in objs: o.select_set(True)
bpy.context.view_layer.objects.active = arm
bpy.ops.object.join()
bpy.ops.export_scene.fbx(filepath=os.path.join(out, 'SM_Town_CobraLight.fbx'), use_selection=True,
                         apply_scale_options='FBX_SCALE_UNITS', mesh_smooth_type='FACE')
print('DONE')
