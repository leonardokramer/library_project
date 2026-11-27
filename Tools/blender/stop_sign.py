"""Placa de STOP (octogono vermelho, letras brancas, poste). Frente para +X. Origem no pe do poste.
Uso: blender -b -P stop_sign.py -- <pasta_saida>
"""
import bpy, bmesh, sys, os, math
out = sys.argv[sys.argv.index('--') + 1]
os.makedirs(out, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)

def mat(n):
    return bpy.data.materials.get(n) or bpy.data.materials.new(n)

def obj(name, bm, m):
    me = bpy.data.meshes.new(name); bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(o); o.data.materials.append(mat(m)); return o

H, R = 2.15, 0.38
bm = bmesh.new()
bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=R, radius2=R, depth=0.012,
                      matrix=__import__('mathutils').Matrix.Translation((0.03, 0, H)) @ __import__('mathutils').Matrix.Rotation(math.radians(90), 4, 'Y') @ __import__('mathutils').Matrix.Rotation(math.radians(22.5), 4, 'Z'))
plate = obj('Plate', bm, 'M_StopRed')
bm = bmesh.new()
bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=R * 0.9, radius2=R * 0.9, depth=0.004,
                      matrix=__import__('mathutils').Matrix.Translation((0.038, 0, H)) @ __import__('mathutils').Matrix.Rotation(math.radians(90), 4, 'Y') @ __import__('mathutils').Matrix.Rotation(math.radians(22.5), 4, 'Z'))
border = obj('Inner', bm, 'M_StopRed')
bm = bmesh.new()
bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=0.03, radius2=0.03, depth=H + 0.2,
                      matrix=__import__('mathutils').Matrix.Translation((0, 0, (H + 0.2) / 2)))
pole = obj('Pole', bm, 'M_Metal')
bpy.ops.object.text_add(location=(0, 0, 0))
t = bpy.context.object
t.data.body = 'STOP'; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'
t.data.size = 0.24; t.data.extrude = 0.003
t.rotation_euler = (math.radians(90), 0, math.radians(90))
t.location = (0.042, 0, H)
bpy.ops.object.convert(target='MESH')
t.data.materials.clear(); t.data.materials.append(mat('M_StopWhite'))
objs = [plate, border, pole, t]
bpy.ops.object.select_all(action='DESELECT')
for o in objs:
    bpy.context.view_layer.objects.active = o; o.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.cube_project(cube_size=0.5); bpy.ops.object.mode_set(mode='OBJECT'); o.select_set(False)
for o in objs: o.select_set(True)
bpy.context.view_layer.objects.active = plate
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
bpy.ops.object.join()
bpy.ops.export_scene.fbx(filepath=os.path.join(out, 'SM_StopSign.fbx'), use_selection=True,
                         apply_scale_options='FBX_SCALE_UNITS', mesh_smooth_type='FACE')
print('DONE')
