"""Main Street densa (docs/TOWN_ART_PASS.md, "Main Street"): importa as pecas do Blender
(Tools/blender/main_street.py -> Saved/TownFBX_MS), cria os materiais e monta as fileiras de predios,
as pontas em T (hotel ao norte, cinema ao sul), as ruas transversais, os marcos e os letreiros.
L_Library_Street, rotulos 'MS_'. Idempotente.  Rodar: py "<caminho>/town_mainstreet.py" [noimport] [nomat]
"""
import unreal, sys, os, random, traceback, math
LOG = r'C:\Users\krame\OneDrive\Documentos\Unreal Projects\library_project\Saved\town_mainstreet.log'
FBX = r'C:\Users\krame\OneDrive\Documentos\Unreal Projects\library_project\Saved\TownFBX_MS'
MESH_DIR = '/Game/Library/Meshes/Town/MainStreet'
MAT_DIR = '/Game/Library/Materials/Town'
MEL = unreal.MaterialEditingLibrary
MASTER = '/Game/MERIDIAN/VOL21_55ElmStreet/Materials/Masters/MM_DEKO_MERDIAN_Master_01a'
BRICK_TX = '/Game/MERIDIAN/VOL21_55ElmStreet/Textures/Unique/TX_Brick_13a_'
ARGS = sys.argv[1:] if len(sys.argv) > 1 else []

WEST_X, EAST_X, Z0 = 1048, 2480, 10

def log(*a):
    with open(LOG, 'a') as f:
        f.write(' '.join(str(x) for x in a) + '\n')

def asset(path, cls, factory):
    if unreal.EditorAssetLibrary.does_asset_exist(path):
        return unreal.load_asset(path)
    d, n = path.rsplit('/', 1)
    return unreal.AssetToolsHelpers.get_asset_tools().create_asset(n, d, cls, factory)

def mi(name, parent, scal=None, vec=None, tex=None):
    m = asset(MAT_DIR + '/' + name, unreal.MaterialInstanceConstant, unreal.MaterialInstanceConstantFactoryNew())
    m.set_editor_property('parent', unreal.load_asset(parent) if isinstance(parent, str) else parent)
    for k, v in (scal or {}).items():
        MEL.set_material_instance_scalar_parameter_value(m, k, v)
    for k, v in (vec or {}).items():
        MEL.set_material_instance_vector_parameter_value(m, k, unreal.LinearColor(*v))
    for k, v in (tex or {}).items():
        MEL.set_material_instance_texture_parameter_value(m, k, unreal.load_asset(v))
    unreal.EditorAssetLibrary.save_asset(MAT_DIR + '/' + name, False)
    return m

def paint(name, color, rough=0.85, dirt=0.5, metal=0.0):
    return mi(name, MAT_DIR + '/M_Town_Paint', {'Roughness': rough, 'DirtAmount': dirt, 'Metallic': metal}, {'Color': (*color, 1)})

def glow(name, color, inten, blink=0.0, speed=0.0):
    return mi(name, MAT_DIR + '/M_Town_Glow', {'Intensity': inten, 'BlinkAmount': blink, 'BlinkSpeed': speed}, {'Color': (*color, 1)})

def make_glass():
    """vidro escuro opaco (barato; reflete a nevoa)"""
    path = MAT_DIR + '/M_MS_GlassDark'
    if unreal.EditorAssetLibrary.does_asset_exist(path):
        return unreal.load_asset(path)
    m = asset(path, unreal.Material, unreal.MaterialFactoryNew())
    c = MEL.create_material_expression(m, unreal.MaterialExpressionConstant3Vector, -400, 0)
    c.set_editor_property('constant', unreal.LinearColor(0.012, 0.014, 0.016, 1))
    r = MEL.create_material_expression(m, unreal.MaterialExpressionConstant, -400, 150)
    r.set_editor_property('r', 0.08)
    s = MEL.create_material_expression(m, unreal.MaterialExpressionConstant, -400, 250)
    s.set_editor_property('r', 0.9)
    MEL.connect_material_property(c, '', unreal.MaterialProperty.MP_BASE_COLOR)
    MEL.connect_material_property(r, '', unreal.MaterialProperty.MP_ROUGHNESS)
    MEL.connect_material_property(s, '', unreal.MaterialProperty.MP_SPECULAR)
    MEL.recompile_material(m)
    unreal.EditorAssetLibrary.save_asset(path, False)
    return m

def make_neon():
    """emissivo que falha: liga/desliga em degraus aleatorios (Seed por instancia)"""
    path = MAT_DIR + '/M_MS_NeonFlicker'
    if unreal.EditorAssetLibrary.does_asset_exist(path):
        return unreal.load_asset(path)
    m = asset(path, unreal.Material, unreal.MaterialFactoryNew())
    m.set_editor_property('shading_model', unreal.MaterialShadingModel.MSM_UNLIT)
    cu = MEL.create_material_expression(m, unreal.MaterialExpressionCustom, -300, 0)
    ins = []
    for n in ('T', 'Speed', 'Seed', 'Off', 'Color', 'Intensity', 'Dim'):
        ci = unreal.CustomInput(); ci.set_editor_property('input_name', n); ins.append(ci)
    cu.set_editor_property('inputs', ins)
    cu.set_editor_property('output_type', unreal.CustomMaterialOutputType.CMOT_FLOAT3)
    cu.set_editor_property('code',
        'float k = floor(T * Speed);\n'
        'float r = frac(sin(k * 12.9898 + Seed * 78.233) * 43758.5453);\n'
        'float r2 = frac(sin(floor(T * Speed * 7.0) * 4.1414 + Seed) * 24634.6345);\n'
        'float on = r > Off ? 1.0 : Dim;\n'
        'on *= (r < Off + 0.08 && r2 > 0.5) ? 0.35 : 1.0;\n'
        'return Color * Intensity * on;')
    t = MEL.create_material_expression(m, unreal.MaterialExpressionTime, -700, -200)
    def sp(name, v, y):
        e = MEL.create_material_expression(m, unreal.MaterialExpressionScalarParameter, -700, y)
        e.set_editor_property('parameter_name', name); e.set_editor_property('default_value', v); return e
    col = MEL.create_material_expression(m, unreal.MaterialExpressionVectorParameter, -700, 300)
    col.set_editor_property('parameter_name', 'Color'); col.set_editor_property('default_value', unreal.LinearColor(1.0, 0.25, 0.15, 1))
    MEL.connect_material_expressions(t, '', cu, 'T')
    MEL.connect_material_expressions(sp('Speed', 6.0, -100), '', cu, 'Speed')
    MEL.connect_material_expressions(sp('Seed', 1.0, 0), '', cu, 'Seed')
    MEL.connect_material_expressions(sp('Off', 0.15, 100), '', cu, 'Off')
    MEL.connect_material_expressions(col, '', cu, 'Color')
    MEL.connect_material_expressions(sp('Intensity', 12.0, 400), '', cu, 'Intensity')
    MEL.connect_material_expressions(sp('Dim', 0.05, 500), '', cu, 'Dim')
    MEL.connect_material_property(cu, '', unreal.MaterialProperty.MP_EMISSIVE_COLOR)
    MEL.recompile_material(m)
    unreal.EditorAssetLibrary.save_asset(path, False)
    return m

def find_pack_mat(name):
    ar = unreal.AssetRegistryHelpers.get_asset_registry()
    for ad in ar.get_assets_by_path('/Game/MERIDIAN', recursive=True):
        if str(ad.asset_name) == name:
            return unreal.load_asset(str(ad.package_name))

M = {}
def materials():
    brick_tex = {'Albedo ': BRICK_TX + 'ALB', 'Normal': BRICK_TX + 'NRM', 'RMA': BRICK_TX + 'RMA', 'Height': BRICK_TX + 'H'}
    def brick(name, tint, desat=0.0, coord=1.0):
        return mi(name, MASTER, {'Texture Coord': coord, 'Albedo Desat': desat, 'Height Ratio Offset': 0.01},
                  {'Albedo Color Tint (Base)': (*tint, 1)}, brick_tex)
    M['brick'] = [
        brick('MI_MS_Brick_Red', (1.0, 0.82, 0.76)),
        brick('MI_MS_Brick_Brown', (0.62, 0.5, 0.42)),
        brick('MI_MS_Brick_Dark', (0.42, 0.37, 0.35)),
        brick('MI_MS_Brick_Ochre', (0.95, 0.78, 0.55), 0.5),
        brick('MI_MS_Brick_PaintCream', (1.0, 0.93, 0.78), 1.0),
        brick('MI_MS_Brick_PaintGreen', (0.48, 0.58, 0.5), 1.0),
        brick('MI_MS_Brick_PaintGrey', (0.62, 0.63, 0.66), 1.0),
        brick('MI_MS_Brick_PaintRust', (0.62, 0.32, 0.24), 0.8),
    ]
    M['trim'] = [paint('MI_MS_Trim_Cream', (0.55, 0.51, 0.43), 0.8, 0.7), paint('MI_MS_Trim_Stone', (0.40, 0.39, 0.37), 0.9, 0.6),
                 paint('MI_MS_Trim_Green', (0.06, 0.12, 0.09), 0.7, 0.6), paint('MI_MS_Trim_Oxblood', (0.20, 0.05, 0.04), 0.7, 0.6),
                 paint('MI_MS_Trim_Black', (0.035, 0.035, 0.035), 0.6, 0.5)]
    M['band'] = [paint('MI_MS_Band_Black', (0.02, 0.02, 0.02), 0.5, 0.4), paint('MI_MS_Band_Green', (0.03, 0.09, 0.05), 0.6, 0.5),
                 paint('MI_MS_Band_Maroon', (0.15, 0.03, 0.03), 0.6, 0.5), paint('MI_MS_Band_Cream', (0.5, 0.46, 0.38), 0.8, 0.7),
                 paint('MI_MS_Band_Navy', (0.02, 0.035, 0.08), 0.6, 0.5)]
    M['awning'] = [paint('MI_MS_Awning_Maroon', (0.22, 0.035, 0.035), 0.95, 0.9), paint('MI_MS_Awning_Green', (0.04, 0.12, 0.06), 0.95, 0.9),
                   paint('MI_MS_Awning_Navy', (0.03, 0.05, 0.12), 0.95, 0.9), paint('MI_MS_Awning_Tan', (0.38, 0.30, 0.2), 0.95, 0.9)]
    M['stone'] = paint('MI_MS_Stone', (0.36, 0.35, 0.33), 0.92, 0.7)
    M['frame'] = paint('MI_MS_Frame', (0.04, 0.04, 0.038), 0.55, 0.5, 0.3)
    M['interior'] = paint('MI_MS_Interior', (0.006, 0.006, 0.006), 1.0, 0.0)
    M['roof'] = paint('MI_MS_Roof', (0.05, 0.05, 0.05), 0.95, 0.6)
    M['letters'] = paint('MI_MS_Letters', (0.62, 0.5, 0.26), 0.45, 0.6, 0.7)
    M['letters_w'] = paint('MI_MS_LettersWhite', (0.55, 0.53, 0.48), 0.6, 0.7)
    M['tank'] = paint('MI_MS_Tank', (0.36, 0.39, 0.37), 0.8, 0.9, 0.2)
    M['metal'] = unreal.load_asset(MAT_DIR + '/MI_Town_Metal')
    M['glass'] = make_glass()
    M['winlit'] = [glow('MI_MS_WinLit_Warm', (1.0, 0.6, 0.28), 1.6), glow('MI_MS_WinLit_Dim', (0.9, 0.62, 0.38), 0.6),
                   glow('MI_MS_WinLit_TV', (0.45, 0.6, 1.0), 0.8, 0.5, 9.0)]
    M['shoplit'] = glow('MI_MS_ShopLit', (1.0, 0.66, 0.38), 0.15)
    M['bulb'] = glow('MI_MS_Bulb', (1.0, 0.7, 0.35), 6.0)
    neon = make_neon()
    M['neon_red'] = mi('MI_MS_Neon_Red', neon, {'Seed': 3.0, 'Off': 0.22, 'Speed': 5.0, 'Intensity': 14.0}, {'Color': (1.0, 0.12, 0.08, 1)})
    M['neon_blue'] = mi('MI_MS_Neon_Blue', neon, {'Seed': 7.0, 'Off': 0.12, 'Speed': 3.0, 'Intensity': 10.0}, {'Color': (0.2, 0.45, 1.0, 1)})
    M['neon_pink'] = mi('MI_MS_Neon_Pink', neon, {'Seed': 11.0, 'Off': 0.35, 'Speed': 8.0, 'Intensity': 12.0}, {'Color': (1.0, 0.2, 0.5, 1)})
    M['neon_dead'] = paint('MI_MS_NeonDead', (0.12, 0.1, 0.1), 0.3, 0.6)
    M['board'] = find_pack_mat('MI_Plywood_Wall_01a') or paint('MI_MS_Board', (0.3, 0.24, 0.16), 0.95, 0.8)
    M['signboard'] = paint('MI_MS_SignBoard', (0.62, 0.6, 0.55), 0.8, 0.6)
    M['interior_dim'] = [glow('MI_MS_InteriorDim', (1.0, 0.7, 0.42), 0.05), glow('MI_MS_InteriorDimCold', (0.55, 0.7, 1.0), 0.035)]
    M['beacon'] = glow('MI_MS_Beacon', (1.0, 0.05, 0.02), 30.0, 1.0, 2.2)
    M['marquee'] = glow('MI_MS_Marquee', (0.85, 0.9, 1.0), 0.9, 0.08, 0.7)   # quadro de letras do cinema, aceso e tremendo um pouco

DEFAULT_SLOTS = None
def default_slots():
    return {'Brick': M['brick'][0], 'Trim': M['trim'][0], 'Stone': M['stone'], 'Glass': M['glass'], 'WinLit': M['winlit'][0],
            'Board': M['board'], 'Frame': M['frame'], 'Interior': M['interior'], 'SignBand': M['band'][0], 'Roof': M['roof'],
            'Metal': M['metal'], 'Letters': M['letters'], 'Neon': M['neon_red'], 'Awning': M['awning'][0], 'Bulb': M['bulb'],
            'Tank': M['tank']}

def import_meshes():
    tasks = []
    for f in sorted(os.listdir(FBX)):
        if not f.endswith('.fbx'):
            continue
        t = unreal.AssetImportTask(); t.filename = os.path.join(FBX, f); t.destination_path = MESH_DIR
        t.automated = True; t.replace_existing = True; t.save = True
        o = unreal.FbxImportUI()
        o.set_editor_property('import_materials', False)
        o.set_editor_property('import_textures', False)
        o.static_mesh_import_data.set_editor_property('combine_meshes', True)
        o.static_mesh_import_data.set_editor_property('auto_generate_collision', False)
        t.options = o
        tasks.append(t)
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
    log('imported', len(tasks))

def setup_meshes():
    ds = default_slots()
    ar = unreal.AssetRegistryHelpers.get_asset_registry()
    for ad in ar.get_assets_by_path(MESH_DIR):
        if str(ad.asset_class_path.asset_name) != 'StaticMesh':
            continue
        sm = unreal.load_asset(str(ad.package_name))
        for i, s in enumerate(sm.static_materials):
            k = str(s.material_slot_name)
            for slot, mat in ds.items():
                if k == slot or k.startswith(slot + '_') or k.startswith(slot + '.'):
                    sm.set_material(i, mat)
        n = sm.get_name()
        # colisao: so os predios (caixa simples), placas/toldos sem colisao
        body = n.startswith(('SM_MS_B', 'SM_MS_C', 'SM_MS_Hotel', 'SM_MS_Theater', 'SM_MS_WaterTower'))
        unreal.EditorStaticMeshLibrary.remove_collisions(sm)
        if body:
            unreal.EditorStaticMeshLibrary.add_simple_collisions(sm, unreal.ScriptCollisionShapeType.BOX)
        unreal.EditorAssetLibrary.save_asset(str(ad.package_name), False)
    log('meshes set')

# ---------------------------------------------------------------- layout
W = {'B076': 760, 'B114': 1140, 'B152': 1520, 'C114': 1140, 'C152': 1520}
def width(name):
    return W[name.split('_')[2]]

# fileiras: (lado, y0, y1, [(malha, opcoes)])  opcoes: sign, awning, neon, blade, fe(escada de incendio: '+'/'-'), corner(lado do mundo +1/-1)
ROWS = [
    # ---- oeste (lado da livraria), fachada X 1048, frente +X; ruas em T nas pontas (cinema Y -5300, hotel Y 7100)
    ('W', -4500, -2125, [('SM_MS_C114_3a', dict(corner=-1, sign='SM_MS_Sign_Insurance', brick=6, band=4)),
                         ('SM_MS_B114_3a', dict(sign='SM_MS_Sign_Hardware', awning=1, brick=0, fe='+'))]),
    ('W', -1875, -700, [('SM_MS_B114_3b', dict(brick=4, band=3))]),
    ('W', 700, 3100, [('SM_MS_B076_4a', dict(sign='SM_MS_Sign_Barber', awning=2, brick=3, band=1)),
                      ('SM_MS_C152_4a', dict(corner=+1, sign='SM_MS_Sign_FiveDime', brick=0, band=2, awning=0, fe='-'))]),
    ('W', 4300, 6300, [('SM_MS_C114_3a', dict(corner=-1, sign='SM_MS_Sign_Florist', brick=5, band=1)),
                       ('SM_MS_B076_3a', dict(sign='SM_MS_Sign_Records', brick=7, band=0, neon_open=True))]),
    # ---- leste (em frente), fachada X 2480, frente -X
    ('E', -4500, -2125, [('SM_MS_C114_3a', dict(corner=-1, sign='SM_MS_Sign_Tailor', brick=3, band=0)),
                         ('SM_MS_B114_4a', dict(brick=1, fe='-'))]),
    ('E', -1875, -560, [('SM_MS_B114_4a', dict(brick=2, blade='SM_MS_Blade_Pawn', sign='SM_MS_Sign_Pawn', band=2, awning=3))]),
    ('E', -560, 560, [('SM_MS_B114_2a', dict(brick=4, band=0, diner=True, trim=2))]),
    ('E', 560, 3100, [('SM_MS_B076_3a', dict(brick=1, blade='SM_MS_Blade_Bar', band=2)),
                      ('SM_MS_C152_4a', dict(corner=+1, sign='SM_MS_Sign_Pharmacy', brick=6, band=1, awning=1, lit=True))]),
    ('E', 4300, 6300, [('SM_MS_C114_3a', dict(corner=-1, sign='SM_MS_Sign_TVRepair', brick=2, band=4)),
                       ('SM_MS_B076_2a', dict(brick=0, sign='SM_MS_Sign_Bakery', awning=0))]),
]
# predios soltos: (malha, (x, y), yaw, opcoes)  yaw: 0 frente +X, 180 frente -X, 90 frente +Y, -90 frente -Y
SOLO = [
    # ponta norte: hotel fechando a rua (rua transversal norte em Y 6300..7100, so para oeste)
    ('SM_MS_Hotel', (1760, 7100), -90, dict(brick=2, sign='SM_MS_Sign_Hotel', blade='SM_MS_Blade_Hotel', band=0, trim=1, lit=True)),
    ('SM_MS_B114_4a', (-420, 7100), -90, dict(brick=1)),
    ('SM_MS_B076_4a', (3950, 7100), -90, dict(brick=6, band=2)),
    # ponta sul: cinema fechando a rua (rua transversal sul em Y -5300..-4500)
    ('SM_MS_Theater', (1760, -5300), 90, dict(brick=1, blade='SM_MS_Blade_State')),
    ('SM_MS_B114_3b', (190, -5300), 90, dict(brick=7)),
    ('SM_MS_B152_2a', (3410, -5300), 90, dict(brick=3, band=1)),
    # Elm Street (frentes para a rua transversal)
    ('SM_MS_B152_2a', (-1150, 4300), -90, dict(brick=2, band=1)),
    ('SM_MS_B114_3b', (-1030, 3100), 90, dict(brick=6)),
    ('SM_MS_B152_3a', (-2440, 3100), 90, dict(brick=1, fe='+')),
    ('SM_MS_B114_4a', (4520, 3100), 90, dict(brick=3)),
    ('SM_MS_B076_2a', (5550, 3100), 90, dict(brick=4, band=2)),
    ('SM_MS_B152_3a', (6750, 3100), 90, dict(brick=7)),
]
LANDMARKS = [
    ('SM_MS_WaterTower', (-900, -3400), 20),
]

def run():
    open(LOG, 'w').close()
    materials()
    if 'noimport' not in ARGS:
        import_meshes()
    setup_meshes()
    world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
    les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    les.set_current_level_by_name('L_Library_Street')
    for a in eas.get_all_level_actors():
        lab = a.get_actor_label()
        if lab.startswith(('MS_', 'NB_', 'FN_')) or lab.startswith('ST_Lawn'):
            eas.destroy_actor(a)
    load = lambda n: unreal.load_asset(MESH_DIR + '/' + n)
    rnd = random.Random(1996)
    foot = []   # pegadas dos predios (para limpar arvores/entulho)

    def spawn(mesh, loc, yaw, scale=(1, 1, 1), label='x', folder='Town/MainStreet'):
        sm = load(mesh) if isinstance(mesh, str) else mesh
        a = eas.spawn_actor_from_object(sm, unreal.Vector(*loc), unreal.Rotator(roll=0, pitch=0, yaw=yaw))
        a.set_actor_scale3d(unreal.Vector(*scale))
        a.set_actor_label('MS_' + label); a.set_folder_path(folder)
        c = a.static_mesh_component
        c.set_editor_property('mobility', unreal.ComponentMobility.STATIC)
        return a

    def override(a, slot, mat):
        c = a.static_mesh_component
        for i, s in enumerate(c.get_material_slot_names()):
            if str(s) == slot or str(s).startswith(slot + '_'):
                c.set_material(i, mat)

    def dress(a, opt, sc=1.0):
        override(a, 'Brick', M['brick'][opt.get('brick', 0) % len(M['brick'])])
        override(a, 'Trim', M['trim'][opt.get('trim', rnd.randrange(len(M['trim'])))])
        override(a, 'SignBand', M['band'][opt.get('band', rnd.randrange(len(M['band'])))])
        if rnd.random() < 0.45:
            override(a, 'Interior', M['interior_dim'][rnd.randrange(2)])
        if opt.get('lit') or opt.get('diner'):
            override(a, 'WinLit', M['shoplit'])
        else:
            override(a, 'WinLit', M['winlit'][rnd.choice([0, 0, 1, 1, 2])])

    def building(mesh, fx, yc, front, opt, sx=1.0, label='B'):
        """front +1: fachada para +X (oeste da rua); -1: para -X (leste)"""
        yaw = 0 if front > 0 else 180
        mirror = 1
        if 'corner' in opt:
            # janelas laterais do modelo ficam no -Y local (UE); no mundo: -1*front
            mirror = 1 if (-front) == opt['corner'] else -1
        a = spawn(mesh, (fx, yc, Z0), yaw, (1, sx * mirror, 1), label)
        dress(a, opt)
        w = width(mesh) * sx
        d = 1600 if 'C' in mesh.split('_')[2] else 1200
        foot.append((min(fx, fx - front * d), max(fx, fx - front * d), yc - w / 2, yc + w / 2))
        def front_pt(dx, dy, dz):
            return (fx + front * dx, yc + dy, Z0 + dz)
        if opt.get('sign'):
            s = spawn(opt['sign'], front_pt(9, 0, 397), yaw, (1, 1, 1), label + 'Sign')
            override(s, 'Letters', M['letters'] if rnd.random() < 0.6 else M['letters_w'])
        if opt.get('awning') is not None and 'awning' in opt:
            aw = {760: 'SM_MS_Awning_067', 1140: 'SM_MS_Awning_105', 1520: 'SM_MS_Awning_143'}[width(mesh)]
            t = spawn(aw, front_pt(4, 0, 355), yaw, (1, sx, 1), label + 'Awning')
            override(t, 'Awning', M['awning'][opt['awning']])
        if opt.get('blade'):
            dy = (w / 2 - 80)
            b = spawn(opt['blade'], front_pt(0, dy if rnd.random() < 0.5 else -dy, 470), yaw, (1, 1, 1), label + 'Blade')
            override(b, 'Neon', M['neon_pink'] if 'Bar' in opt['blade'] else (M['neon_dead'] if 'Pawn' in opt['blade'] else M['neon_red']))
        if opt.get('diner'):
            n = spawn('SM_MS_Neon_Diner', front_pt(10, 0, 330), yaw, (1, 1, 1), label + 'Neon')
            override(n, 'Neon', M['neon_red'])
            o = spawn('SM_MS_Neon_Open', front_pt(-30, -w / 2 + 160, 150), yaw, (1, 1, 1), label + 'Open')
            override(o, 'Neon', M['neon_blue'])
        if opt.get('neon_open'):
            o = spawn('SM_MS_Neon_Open', front_pt(-30, w / 2 - 160, 150), yaw, (1, 1, 1), label + 'Open')
            override(o, 'Neon', M['neon_pink'])
        if opt.get('fe'):
            fl = int(mesh.split('_')[3][0])
            if fl >= 3:
                sgn = 1 if opt['fe'] == '+' else -1
                # escada na lateral (sai para +y local); no mundo o lado e sgn
                yy = yc + sgn * w / 2
                ysc = 1 if (sgn * front) > 0 else -1     # +y local -> mundo: front>0 => -Y... ajustado por espelho
                spawn('SM_MS_FireEscape_%d' % fl, (fx, yy, Z0), yaw, (1, -ysc, 1), label + 'FireEsc')
        return a

    n = 0
    for side, y0, y1, lots in ROWS:
        nat = sum(width(m) for m, o in lots)
        sx = (y1 - y0) / nat
        fx, front = (WEST_X, 1) if side == 'W' else (EAST_X, -1)
        y = y0
        for (mesh, opt) in lots:
            w = width(mesh) * sx
            building(mesh, fx, y + w / 2, front, opt, sx, '%s%d' % (side, n))
            y += w; n += 1
        log('row', side, y0, y1, 'scale %.3f' % sx)
    for (mesh, (x, y), yaw, opt) in SOLO:
        a = spawn(mesh, (x, y, Z0), yaw, (1, 1, 1), 'Solo%d' % n)
        dress(a, opt)
        fr = unreal.Vector(1, 0, 0)
        c, s = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
        def pt(dx, dy, dz, x=x, y=y, c=c, s=s):
            return (x + c * dx - s * dy, y + s * dx + c * dy, Z0 + dz)
        if mesh == 'SM_MS_Hotel':
            spawn(opt['sign'], pt(9, 0, 397), yaw, (1, 1, 1), 'HotelSign')
            b = spawn(opt['blade'], pt(0, 900, 520), yaw, (1, 1, 1), 'HotelBlade')
            override(b, 'Neon', M['neon_red'])
        elif mesh == 'SM_MS_Theater':
            b = spawn(opt['blade'], pt(0, -500, 560), yaw, (1, 1, 1), 'TheaterBlade')
            override(b, 'Neon', M['neon_dead'])
            override(a, 'SignBand', M['marquee'])
            override(a, 'Letters', M['frame'])
        elif opt.get('fe'):
            fl = int(mesh.split('_')[3][0])
            spawn('SM_MS_FireEscape_%d' % fl, pt(0, -width(mesh) / 2, 0), yaw, (1, 1, 1), 'FireEscSolo%d' % n)
        bb = a.get_actor_bounds(False)
        foot.append((bb[0].x - bb[1].x, bb[0].x + bb[1].x, bb[0].y - bb[1].y, bb[0].y + bb[1].y))
        n += 1
    for (mesh, (x, y), yaw) in LANDMARKS:
        a = spawn(mesh, (x, y, Z0 - 20), yaw, (1, 1, 1), 'Landmark%d' % n)
        a.static_mesh_component.set_cast_shadow(False)
        if mesh == 'SM_MS_WaterTower':
            # farol de aviso vermelho piscando no topo (a propria lampada e a luminaria; sem luz de verdade)
            b = spawn(unreal.load_asset('/Engine/BasicShapes/Sphere'), (x, y, Z0 - 20 + 3175), 0, (0.35, 0.35, 0.35), 'WaterTowerBeacon')
            b.static_mesh_component.set_material(0, M['beacon'])
            b.static_mesh_component.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
        n += 1
    # ruas transversais nas pontas (asfalto) e barricadas
    road = unreal.load_asset(MAT_DIR + '/MI_Town_Road')
    plane = unreal.load_asset('/Engine/BasicShapes/Plane')
    for (xc, yc, sx, lab) in ((-1300, 6700, 75.0, 'RoadNorth'), (1764, -4900, 120.0, 'RoadSouth')):
        a = spawn(plane, (xc, yc, -11.2), 0, (sx, 8.0, 1), lab)
        a.static_mesh_component.set_material(0, road)
    for (x, y, yaw) in ((-1600, 6700, 90), (3700, 6500, 90), (3700, 6900, 90), (-1800, -4900, 90), (5300, -4900, 90), (1350, -5050, 0), (2150, -5080, 10)):
        spawn('SM_MS_Barricade', (x, y, -11), yaw, (1, 1, 1), 'Barricade')
    # chao dos becos ao lado da livraria e cerca de tabua no fundo (refaz o que era NB_)
    concrete = unreal.load_asset(MAT_DIR + '/MI_Town_Ground')
    cube = unreal.load_asset('/Engine/BasicShapes/Cube')
    board = M['board']
    for yc, lab in ((575, 'AlleyN'), (-575, 'AlleyS'), (-2000, 'AlleySW'), (-2000, 'AlleySE')):
        east = lab.endswith('E')
        x0 = EAST_X if east else -150
        x1 = EAST_X + 1300 if east else WEST_X
        a = spawn(plane, ((x0 + x1) / 2, yc, 9), 0, ((x1 - x0) / 100, 2.6, 1), lab + 'Ground')
        a.static_mesh_component.set_material(0, concrete)
        fxb = x1 - 60 if east else -100
        f = spawn(cube, (fxb, yc, 170), 0, (0.08, 2.8, 3.2), lab + 'Fence')
        f.static_mesh_component.set_material(0, board)
    # limpa arvores e entulho que caem dentro dos predios
    def inside(p):
        return any(x0 + 5 <= p.x <= x1 - 5 and y0 <= p.y <= y1 for (x0, x1, y0, y1) in foot)   # sem margem: a calcada encosta na fachada
    killed = 0
    for a in eas.get_all_level_actors():
        lab = a.get_actor_label()
        if lab.startswith(('TL_', 'CL_', 'CAR_', 'PR_', 'WR_')) and inside(a.get_actor_location()):
            log('remove (inside building)', lab, a.get_actor_location())
            eas.destroy_actor(a); killed += 1
    log('removed', killed)
    les.set_current_level_by_name('L_Library')
    log('spawned', n, 'footprints', len(foot))
    unreal.EditorLoadingAndSavingUtils.save_packages([p for p in list(unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()) + list(unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()) if p.get_name().startswith('/Game/Library')], True)
    log('saved')

try:
    run()
except Exception:
    log(traceback.format_exc())
