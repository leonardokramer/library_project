"""Bundles of pages opening out of slits in the monster's skin, plus small peeling skin flaps (Blender, headless).

  1. In Unreal, export the body: py "Tools/ue_export_body.py" <MonsterBody.fbx>  (see that file)
  2. blender -b --python Tools/blender/monster_flaps.py -- <MonsterBody.fbx> <out_folder> [seed]
     Face: export SKM_MH_Monster_FaceMesh the same way and run with mode "face":
     blender -b --python Tools/blender/monster_flaps.py -- <MonsterFace.fbx> <out_folder> 5 face
     -> SKM_MonsterFacePages.fbx, skeleton /Game/MetaHumans/Common/Face/Face_Archetype_Skeleton, follows the Face component.
  3. Import <out_folder>/SKM_MonsterPages.fbx as a SkeletalMesh with the skeleton
     /Game/MetaHumans/Common/Female/Medium/NormalWeight/Body/metahuman_base_skel and make the component follow the body
     (SetLeaderPoseComponent). Slots: Page (inner yellowed pages), Slit (dark cut), Flap (skin-coloured paper).

The pieces sit on the real skin (ray cast from outside toward the bone) and copy the skin weights of the body
(nearest face, interpolated), so they bend with the body instead of floating.
Blender coordinates of the imported body: metres, +X = monster's left, -Y = front, +Z = up.
"""
import math, random, sys
import bpy, bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree

argv = sys.argv[sys.argv.index('--') + 1:]
SRC, OUT = argv[0], argv[1]
SEED = int(argv[2]) if len(argv) > 2 else 3
MODE = argv[3] if len(argv) > 3 else 'body'
NAME = 'SKM_MonsterFacePages' if MODE == 'face' else 'SKM_MonsterPages'
rnd = random.Random(SEED)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=SRC, use_anim=False, ignore_leaf_bones=True, automatic_bone_orientation=False)
arm = [o for o in bpy.data.objects if o.type == 'ARMATURE'][0]
body = [o for o in bpy.data.objects if o.type == 'MESH'][0]
dg = bpy.context.evaluated_depsgraph_get()
bm_body = bmesh.new()
bm_body.from_mesh(body.data)
bm_body.transform(body.matrix_world)
if MODE == 'face':   # the face mesh also holds eyes, teeth, eyelashes, eye shells: keep only the skin
    # (material names come shuffled from the FBX: the skin is the section with by far the most faces)
    import collections
    cnt = collections.Counter(f.material_index for f in bm_body.faces)
    skin = {cnt.most_common(1)[0][0]}
    bmesh.ops.delete(bm_body, geom=[f for f in bm_body.faces if f.material_index not in skin], context='FACES')
bvh = BVHTree.FromBMesh(bm_body)


NEXT = {'upperarm_l': 'lowerarm_l', 'upperarm_r': 'lowerarm_r', 'lowerarm_l': 'hand_l', 'lowerarm_r': 'hand_r',
        'thigh_l': 'calf_l', 'spine_01': 'spine_02', 'thigh_r': 'calf_r', 'calf_l': 'foot_l', 'calf_r': 'foot_r', 'spine_02': 'spine_03',
        'spine_03': 'spine_04', 'spine_04': 'spine_05', 'spine_05': 'neck_01', 'clavicle_l': 'upperarm_l',
        'clavicle_r': 'upperarm_r', 'neck_01': 'neck_02', 'pelvis': 'spine_02'}


def bone_pts(name):
    """Joint of the bone and joint of the next bone in the chain (the FBX import tails are not the next joint)."""
    h = arm.matrix_world @ arm.data.bones[name].head_local
    t = arm.matrix_world @ arm.data.bones[NEXT[name]].head_local
    return h, t


def surface(bone, direction, t=0.5):
    h, tl = bone_pts(bone)
    m = h.lerp(tl, t)
    d = Vector(direction).normalized()
    origin = m + d * 0.35
    hit, nrm, idx, dist = bvh.ray_cast(origin, (m - origin).normalized(), 0.6)
    if hit is None:
        return None
    if nrm.dot(d) < 0:
        nrm = -nrm
    axis = (tl - h).normalized()
    return hit, nrm.normalized(), axis


verts, faces, uvs, mats = [], [], [], []
SLOTS = ['Page', 'Slit', 'Flap']


def quad_grid(pts, uv, slot):
    n, m = len(pts), len(pts[0])
    base = len(verts)
    for i in range(n):
        for j in range(m):
            verts.append(pts[i][j])
    for i in range(n - 1):
        for j in range(m - 1):
            a = base + i * m + j
            faces.append((a, a + m, a + m + 1, a + 1))
            uvs.append([uv[i][j], uv[i + 1][j], uv[i + 1][j + 1], uv[i][j + 1]])
            mats.append(SLOTS.index(slot))


def bundle(p, N, A, width, length, count, spread=(15, 165)):
    """The skin splits open along A at p (normal N): lens-shaped dark gash, the stacked page edges inside,
    the skin-paper lips peeling back on both sides, and loose pages fanning out of it."""
    B = N.cross(A).normalized()
    A = B.cross(N).normalized()
    gap = width * 0.16                       # half-opening of the gash at its middle

    def half_open(s):                        # lens profile along the gash, s in [-1, 1]
        return gap * max(0.0, 1 - s * s) ** 0.7

    # dark floor of the gash (slightly sunk)
    pts, uv = [], []
    for i in range(9):
        s = i / 8 * 2 - 1
        g = half_open(s) * 1.05
        row = [p + A * (s * width / 2) + B * (k * g) - N * 0.003 for k in (-1, 0, 1)]
        pts.append(row); uv.append([(0, i / 8), (0.5, i / 8), (1, i / 8)])
    quad_grid(pts, uv, 'Slit')
    # stacked page edges seen inside the cut (thin strips, parallel to the cut, at increasing depth)
    layers = max(5, int(width / 0.008))
    for l in range(layers):
        off = (l / (layers - 1) * 2 - 1) * 0.8
        depth = 0.002 + 0.002 * rnd.random()
        pts, uv = [], []
        for i in range(9):
            s = i / 8 * 2 - 1
            g = half_open(s)
            c = p + A * (s * width / 2 * 0.92) + B * (off * g) - N * depth
            pts.append([c - N * 0.0012, c + N * 0.0005])
            uv.append([(i / 8, l / layers), (i / 8, l / layers + 0.02)])
        quad_grid(pts, uv, 'Page')
    # lips: the skin-paper on both sides peels back
    for side in (-1, 1):
        lift = math.radians(rnd.uniform(25, 55))
        lw = width * rnd.uniform(0.18, 0.3)
        tear = [rnd.uniform(-0.4, 0.1) * lw for _ in range(9)]
        pts, uv = [], []
        for i in range(9):
            s = i / 8 * 2 - 1
            g = half_open(s)
            row, ru = [], []
            for j in range(4):
                q = j / 3
                d = (lw * (1 - abs(s) ** 2) + tear[i]) * q
                ang = lift * q
                pos = p + A * (s * width / 2) + B * (side * (g + d * math.cos(ang))) + N * (0.0007 + d * math.sin(ang))
                row.append(pos); ru.append((i / 8, q))
            pts.append(row); uv.append(ru)
        if side < 0:
            pts = [r[::-1] for r in pts]; uv = [r[::-1] for r in uv]
        quad_grid(pts, uv, 'Flap')
    # loose pages fanning out of the gash
    phis = sorted(rnd.uniform(*spread) for _ in range(count))
    for phi in phis:
        ph = math.radians(phi)
        D = B * math.cos(ph) + N * math.sin(ph)
        side = B * (-math.sin(ph)) + N * math.cos(ph)
        L = length * rnd.uniform(0.45, 1.0)
        wv = width * rnd.uniform(0.45, 0.85)
        off = rnd.uniform(-0.2, 0.2) * width
        curl = math.radians(rnd.uniform(-40, 40))
        tear = [rnd.uniform(-0.35, 0.0) * L for _ in range(5)]
        pts, uv = [], []
        for i in range(5):                      # along the gash
            s = off + (i / 4 - 0.5) * wv
            row, ru = [], []
            for j in range(5):                  # out of the gash
                q = j / 4
                d = (L + tear[i]) * q
                pos = p + A * s - N * 0.004 + D * d + side * (math.sin(curl) * d * q * 0.6)
                row.append(pos)
                ru.append((s / 0.12 + 0.5, d / 0.12))
            pts.append(row); uv.append(ru)
        quad_grid(pts, uv, 'Page')


def flap(p, N, size):
    """A corner of skin-paper peeling off."""
    A = N.cross(Vector((rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-1, 1)))).normalized()
    B = N.cross(A).normalized()
    lift = math.radians(rnd.uniform(15, 40))
    tear = [rnd.uniform(-0.3, 0.0) * size for _ in range(4)]
    pts, uv = [], []
    for i in range(4):
        s = (i / 3 - 0.5) * size
        row, ru = [], []
        for j in range(4):
            q = j / 3
            d = (size * 0.8 + tear[i]) * q
            ang = lift * q * q
            pos = p + A * s + N * 0.0008 + B * (d * math.cos(ang)) + N * (d * math.sin(ang))
            row.append(pos)
            ru.append((s / 0.1 + 0.5, d / 0.1))
        pts.append(row); uv.append(ru)
    quad_grid(pts, uv, 'Flap')


# (bone, outward direction in Blender space, slit 'along' bone or 'across', width m, length m, count, t along bone)
SITES = [
    ('upperarm_l', (1, 0.1, 0.4), 'along', 0.09, 0.07, 12, 0.25),     # left shoulder
    ('upperarm_r', (-0.5, 1, 0.1), 'along', 0.08, 0.06, 10, 0.55),    # back of right arm
    ('upperarm_r', (-1, -0.4, 0.3), 'along', 0.06, 0.05, 8, 0.2),     # right shoulder, front
    ('lowerarm_l', (0.4, 1, 0.3), 'along', 0.07, 0.05, 9, 0.45),      # back of left forearm
    ('lowerarm_r', (-1, -0.3, 0.1), 'along', 0.065, 0.05, 8, 0.6),    # outer right forearm
    ('lowerarm_l', (0.2, -1, 0), 'along', 0.05, 0.04, 6, 0.75),       # inside of left wrist
    ('spine_03', (1.0, -1, 0), 'across', 0.1, 0.075, 13, 0.5),        # left ribs, front side
    ('spine_02', (-1.0, -1, 0), 'across', 0.07, 0.05, 9, 0.6),        # right belly
    ('spine_02', (-0.6, 1, 0), 'across', 0.09, 0.065, 11, 0.5),       # lower back, right
    ('spine_04', (0.6, 1, 0), 'along', 0.08, 0.06, 10, 0.5),          # back, left shoulder blade
    ('spine_05', (0.15, 1, 0.15), 'along', 0.1, 0.08, 14, 0.4),       # upper back
    ('spine_05', (0.6, -1, 0.2), 'across', 0.06, 0.05, 8, 0.3),       # (front is the face mesh: lands on the back)
    ('spine_04', (-1.2, -1, 0), 'across', 0.07, 0.05, 9, 0.5),        # right chest
    ('pelvis', (1, 0.3, -0.25), 'across', 0.07, 0.055, 9, 0.5),       # left hip
    ('thigh_l', (0.35, -1, 0), 'along', 0.1, 0.07, 12, 0.35),         # front of left thigh
    ('thigh_r', (-1, 0.5, 0), 'along', 0.09, 0.065, 11, 0.6),         # outer back right thigh
    ('thigh_r', (0, -1, 0), 'along', 0.06, 0.045, 7, 0.85),           # above the right knee
    ('calf_r', (0, 1, 0), 'along', 0.09, 0.065, 11, 0.3),             # back of right calf
    ('calf_l', (1, -0.5, 0), 'along', 0.07, 0.05, 8, 0.6),            # outer left shin
    ('calf_l', (-0.3, 1, 0), 'along', 0.06, 0.045, 7, 0.25),          # back of left calf
    # --- big openings (the body splitting open)
    ('spine_04', (1.0, -1, 0.1), 'across', 0.16, 0.1, 20, 0.3),       # big one across the left chest
    ('spine_03', (-0.3, 1, 0), 'along', 0.18, 0.11, 22, 0.5),         # big one down the back, right of the spine
    ('spine_01', (0.4, -1, 0), 'across', 0.13, 0.08, 16, 0.5),        # belly
    ('thigh_r', (0.2, -1, 0), 'along', 0.15, 0.09, 18, 0.3),          # front of the right thigh
    ('thigh_l', (0.2, 1, 0), 'along', 0.13, 0.08, 15, 0.45),          # back of the left thigh
    # --- more small ones
    ('upperarm_l', (0.2, -1, 0), 'along', 0.06, 0.05, 8, 0.6),        # front of the left arm
    ('upperarm_l', (0.3, 1, 0), 'along', 0.05, 0.04, 6, 0.8),         # back of the left elbow
    ('lowerarm_r', (0.0, 1, 0.3), 'along', 0.05, 0.04, 7, 0.35),      # back of the right forearm
    ('lowerarm_r', (0.0, -1, 0), 'along', 0.045, 0.035, 6, 0.8),      # inside of the right wrist
    ('spine_02', (1.2, 1, 0), 'along', 0.06, 0.045, 8, 0.5),          # left flank, back
    ('pelvis', (-1, 0.5, -0.2), 'across', 0.06, 0.045, 8, 0.4),       # right hip
    ('calf_r', (-1, -0.3, 0), 'along', 0.06, 0.045, 7, 0.6),          # outer right shin
    ('calf_l', (0.3, -1, 0), 'along', 0.05, 0.04, 6, 0.4),            # left shin, front
    ('thigh_l', (1, 0, 0), 'along', 0.06, 0.05, 8, 0.75),             # outer left knee
    ('spine_05', (-0.6, 1, 0.2), 'along', 0.07, 0.055, 9, 0.6),       # right shoulder blade
]
placed = []


def surface_at(point, direction):
    d = Vector(direction).normalized()
    origin = point + d * 0.2
    hit, nrm, idx, dist = bvh.ray_cast(origin, -d, 0.35)
    if hit is None:
        return None
    if nrm.dot(d) < 0:
        nrm = -nrm
    return hit, nrm.normalized()


# face: (bone, offset from the bone in m, outward direction, gash axis, width, length, count)
FACE_SITES = [
    ('FACIAL_L_LipCorner', (0.012, 0.004, 0.0), (0.5, -1, 0), (1, 0.6, 0.15), 0.045, 0.018, 6),   # smile torn, left
    ('FACIAL_R_LipCorner', (-0.012, 0.004, 0.0), (-0.5, -1, 0), (-1, 0.6, 0.15), 0.04, 0.016, 5),  # smile torn, right
    # (a gash on the top of the skull with a tuft of pages was removed: looked like a punk haircut)
    ('head', (0.05, 0.05, 0.12), (0.8, 0.5, 0.6), (0.3, -0.4, 1), 0.06, 0.045, 8),                 # back left of the skull
    ('FACIAL_L_CheekInner', (0.025, 0.0, -0.01), (0.7, -1, 0), (0.2, 0.3, 1), 0.035, 0.022, 6),   # left cheek
    ('FACIAL_C_Forehead', (-0.04, 0.01, 0.015), (-0.6, -1, 0.5), (0.3, 0, 1), 0.035, 0.022, 5),   # right temple
    ('FACIAL_R_Eye', (0.0, 0.0, -0.022), (0, -1, -0.2), (1, 0, 0), 0.028, 0.014, 5),              # under the right eye
    ('neck_01', (0.05, 0.0, 0.07), (1, -0.2, 0), (0, 0.2, 1), 0.05, 0.035, 7),                    # left side of the neck
]
if MODE == 'face':
    SITES = []
    for bone, off, dirv, axis, w, L, n in FACE_SITES:
        b = arm.data.bones.get(bone)
        if b is None:
            print('NOBONE', bone); continue
        r = surface_at(arm.matrix_world @ b.head_local + Vector(off), dirv)
        if r is None:
            print('MISS', bone); continue
        p, N = r
        bundle(p, N, Vector(axis).normalized(), w, L, n, spread=(20, 160))
        placed.append(p)
        print('site', bone, tuple(round(x, 3) for x in p))
for bone, dirv, mode, w, L, n, t in SITES:
    r = surface(bone, dirv, t)
    if r is None:
        print('MISS', bone)
        continue
    p, N, axis = r
    A = axis if mode == 'along' else N.cross(axis)
    bundle(p, N, A, w, L, n)
    placed.append(p)
    print('site', bone, tuple(round(x, 3) for x in p))

# scattered peeling flaps on the skin (area-weighted random faces; no hands, feet or groin)
tris = [f for f in bm_body.faces]
areas = [f.calc_area() for f in tris]
tot = sum(areas)
count = 0
tries = 0
eyes_mouth = []
if MODE == 'face':
    for n in ('FACIAL_L_Eye', 'FACIAL_R_Eye', 'FACIAL_L_LipCorner', 'FACIAL_R_LipCorner', 'FACIAL_C_MouthUpper'):
        b = arm.data.bones.get(n)
        if b:
            eyes_mouth.append(arm.matrix_world @ b.head_local)
NFLAPS = 10 if MODE == 'face' else 24
while count < NFLAPS and tries < 5000:
    tries += 1
    x = rnd.uniform(0, tot)
    acc = 0
    for f, a in zip(tris, areas):
        acc += a
        if acc >= x:
            break
    c = f.calc_center_median()
    if MODE == 'face':
        if any((c - q).length < 0.035 for q in eyes_mouth):
            continue
    elif c.z < 0.12 or abs(c.x) > 0.42 or (c.z < 0.95 and c.z > 0.78 and abs(c.x) < 0.07):
        continue
    if any((c - q).length < (0.04 if MODE == 'face' else 0.08) for q in placed):
        continue
    flap(c, f.normal.normalized(), rnd.uniform(0.01, 0.02) if MODE == 'face' else rnd.uniform(0.015, 0.035))
    placed.append(c)
    count += 1
print('flaps', count)

me = bpy.data.meshes.new(NAME)
me.from_pydata([tuple(v) for v in verts], [], faces)
uvl = me.uv_layers.new(name='UVMap')
for poly in me.polygons:
    poly.material_index = mats[poly.index]
    poly.use_smooth = True
    for li, loop in enumerate(poly.loop_indices):
        uvl.data[loop].uv = uvs[poly.index][li]
for s in SLOTS:
    me.materials.append(bpy.data.materials.new(s))
ob = bpy.data.objects.new(NAME, me)
bpy.context.scene.collection.objects.link(ob)

# skin weights from the body (nearest face, interpolated)
bpy.context.view_layer.objects.active = ob
for o in bpy.data.objects:
    o.select_set(False)
ob.select_set(True)
mod = ob.modifiers.new('wt', 'DATA_TRANSFER')
mod.object = body
mod.use_object_transform = True
mod.use_vert_data = True
mod.data_types_verts = {'VGROUP_WEIGHTS'}
mod.vert_mapping = 'POLYINTERP_NEAREST'
mod.layers_vgroup_select_src = 'ALL'
mod.layers_vgroup_select_dst = 'NAME'
bpy.ops.object.datalayout_transfer(modifier='wt')
bpy.ops.object.modifier_apply(modifier='wt')
bpy.ops.object.vertex_group_limit_total(limit=8)
bpy.ops.object.vertex_group_normalize_all(lock_active=False)

# parent to the armature with an Armature modifier (world transform kept)
mw = ob.matrix_world.copy()
ob.parent = arm
ob.matrix_world = mw
am = ob.modifiers.new('Armature', 'ARMATURE')
am.object = arm

# export only the armature + the pages mesh. The FBX root must be the bone "root" (as in metahuman_base_skel):
# drop the Empty that the Unreal FBX import creates above the armature (keeping its 0.01 scale baked into the
# armature object). Blender turns the joint "root" into the armature OBJECT (it is not a bone), so the object is named
# "root" and exported as the root bone (armature_nodetype 'ROOT').
# A wrong root makes Unreal offer to REGENERATE the shared skeleton (happened on 2026-11-26; never accept that).
if arm.parent:
    mw = arm.matrix_world.copy()
    arm.parent = None
    arm.matrix_world = mw
arm.name = 'root'
for o in bpy.data.objects:
    o.select_set(False)
ob.select_set(True)
arm.select_set(True)
bpy.ops.export_scene.fbx(filepath=OUT + '/' + NAME + '.fbx', use_selection=True, object_types={'ARMATURE', 'MESH'},
                         add_leaf_bones=False, bake_anim=False, use_armature_deform_only=False, mesh_smooth_type='FACE',
                         apply_unit_scale=True, apply_scale_options='FBX_SCALE_NONE', armature_nodetype='ROOT')
print('exported verts', len(me.vertices), 'faces', len(me.polygons))
