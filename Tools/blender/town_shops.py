"""Predios vizinhos simples (casca) para a rua da livraria. Exporta FBX.
Uso: blender -b -P town_shops.py -- <pasta_saida>
Metros. Frente em X=0 (+X = rua), centro em Y=0, chao Z=0, fundo em X=-D.
Lembrete: o Y sai espelhado no Unreal (Blender +Y = UE -Y); as pecas sao simetricas.
"""
import bpy, bmesh, sys, os

out = sys.argv[sys.argv.index('--') + 1]
os.makedirs(out, exist_ok=True)

def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def box(bm, x0, x1, y0, y1, z0, z1):
    vs = [bm.verts.new(v) for v in [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
                                    (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]]
    for f in [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]:
        bm.faces.new([vs[i] for i in f])

def part(name, matname, fill):
    bm = bmesh.new()
    fill(bm)
    me = bpy.data.meshes.new(name)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    m = bpy.data.materials.get(matname) or bpy.data.materials.new(matname)
    o.data.materials.append(m)
    return o

def export(objs, fname):
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
    bpy.ops.export_scene.fbx(filepath=os.path.join(out, fname + '.fbx'), use_selection=True,
                             apply_scale_options='FBX_SCALE_UNITS', mesh_smooth_type='FACE')

def shop(fname, W, D, H, two_floors=True, boarded=True):
    reset()
    hw = W / 2
    objs = []
    def walls(bm):
        t = 0.25
        box(bm, -0.02, 0.0, -hw, hw, 3.6, H)                # frente, parte de cima
        box(bm, -0.02, 0.0, -hw, -hw + 0.5, 0.0, 3.6)       # frente, pilares do terreo
        box(bm, -0.02, 0.0, hw - 0.5, hw, 0.0, 3.6)
        box(bm, -D, 0.0, -hw, -hw + t, 0.0, H)              # laterais
        box(bm, -D, 0.0, hw - t, hw, 0.0, H)
        box(bm, -D, -D + t, -hw, hw, 0.0, H)                # fundo
    objs.append(part('Walls', 'M_Siding', walls))
    def trim(bm):
        box(bm, 0.0, 0.30, -hw - 0.05, hw + 0.05, H - 0.35, H)        # cornija simples
        box(bm, 0.0, 0.12, -hw, hw, H - 0.55, H - 0.35)
        box(bm, 0.0, 0.10, -hw + 0.5, hw - 0.5, 3.45, 3.60)           # verga da vitrine
        box(bm, 0.0, 0.14, -hw + 0.5, hw - 0.5, 2.85, 2.95)           # faixa da placa
        box(bm, 0.0, 0.08, -hw + 0.5, hw - 0.5, 0.0, 0.45)            # rodape da vitrine
        if two_floors:
            n = 3
            for i in range(n):
                yc = -hw + W * (i + 0.5) / n
                box(bm, 0.0, 0.08, yc - 0.62, yc + 0.62, 4.15, 4.25)  # peitoril
                box(bm, 0.0, 0.06, yc - 0.62, yc - 0.52, 4.25, 6.05)  # batentes
                box(bm, 0.0, 0.06, yc + 0.52, yc + 0.62, 4.25, 6.05)
                box(bm, 0.0, 0.10, yc - 0.68, yc + 0.68, 6.05, 6.20)  # verga
        box(bm, -D, 0.25, -hw - 0.02, hw + 0.02, H, H + 0.05)          # tampa do teto
    objs.append(part('Trim', 'M_TrimN', trim))
    def glass(bm):
        if two_floors:
            n = 3
            for i in range(n):
                yc = -hw + W * (i + 0.5) / n
                box(bm, -0.05, 0.01, yc - 0.52, yc + 0.52, 4.25, 6.05)
        if not boarded:
            box(bm, -0.10, -0.02, -hw + 0.5, hw - 0.5, 0.45, 2.85)
    objs.append(part('Glass', 'M_Glass', glass)) if (two_floors or not boarded) else None
    def board(bm):
        if boarded:
            # vitrine coberta de compensado, placas de 1,2 m com frestas
            y = -hw + 0.5
            while y < hw - 0.55:
                y1 = min(y + 1.2, hw - 0.5)
                box(bm, 0.0, 0.03, y + 0.01, y1 - 0.01, 0.45, 2.85)
                y = y1
            box(bm, 0.0, 0.03, -hw + 0.5, hw - 0.5, 2.95, 3.45)        # placa da loja, sem texto
    objs.append(part('Board', 'M_Plywood', board)) if boarded else None
    objs = [o for o in objs if o]
    export(objs, fname)

shop('SM_Town_ShopNorth', 10.0, 12.0, 7.6, two_floors=True, boarded=True)
shop('SM_Town_ShopSouth', 11.0, 12.0, 4.6, two_floors=False, boarded=True)
print('DONE')
