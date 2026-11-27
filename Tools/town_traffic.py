"""Cruzamento ao norte: rua transversal (Y 3300..4100), dois postes com fio atravessado e
dois semaforos pendurados piscando ambar. No L_Library_Street, rotulos 'TR_'. Idempotente.
Rodar: py "<caminho>/town_traffic.py" [noimport]
"""
import unreal, os, sys, traceback
LOG = r'C:\Users\krame\OneDrive\Documentos\Unreal Projects\library_project\Saved\town_traffic.log'
FBX = r'C:\Users\krame\OneDrive\Documentos\Unreal Projects\library_project\Saved\TownFBX4'
MESH = '/Game/Library/Meshes/Town'
MAT = '/Game/Library/Materials/Town'
MEL = unreal.MaterialEditingLibrary
SAFE = lambda: unreal.EditorLoadingAndSavingUtils.save_packages([p for p in list(unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()) + list(unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()) if p.get_name().startswith('/Game/Library')], True)
CROSS_Y0, CROSS_Y1 = 3300, 4100
STREET_X0, STREET_X1 = 1364, 2164

def log(*a):
    with open(LOG, 'a') as f:
        f.write(' '.join(str(x) for x in a) + '\n')

def glow_master():
    path = MAT + '/M_Town_Glow'
    if unreal.EditorAssetLibrary.does_asset_exist(path):
        return unreal.load_asset(path)
    m = unreal.AssetToolsHelpers.get_asset_tools().create_asset('M_Town_Glow', MAT, unreal.Material, unreal.MaterialFactoryNew())
    def p(cls, x, y):
        return MEL.create_material_expression(m, cls, x, y)
    col = p(unreal.MaterialExpressionVectorParameter, -1200, 0); col.set_editor_property('parameter_name', 'Color')
    col.set_editor_property('default_value', unreal.LinearColor(1, 0.5, 0.05, 1))
    inten = p(unreal.MaterialExpressionScalarParameter, -1200, 200); inten.set_editor_property('parameter_name', 'Intensity'); inten.set_editor_property('default_value', 10.0)
    spd = p(unreal.MaterialExpressionScalarParameter, -1400, 400); spd.set_editor_property('parameter_name', 'BlinkSpeed'); spd.set_editor_property('default_value', 0.8)
    amt = p(unreal.MaterialExpressionScalarParameter, -1000, 600); amt.set_editor_property('parameter_name', 'BlinkAmount'); amt.set_editor_property('default_value', 0.0)
    tm = p(unreal.MaterialExpressionTime, -1400, 300)
    mul_t = p(unreal.MaterialExpressionMultiply, -1200, 350); MEL.connect_material_expressions(tm, '', mul_t, 'A'); MEL.connect_material_expressions(spd, '', mul_t, 'B')
    fr = p(unreal.MaterialExpressionFrac, -1050, 350); MEL.connect_material_expressions(mul_t, '', fr, '')
    rd = p(unreal.MaterialExpressionRound, -900, 350); MEL.connect_material_expressions(fr, '', rd, '')
    one = p(unreal.MaterialExpressionConstant, -900, 250); one.set_editor_property('r', 1.0)
    lp = p(unreal.MaterialExpressionLinearInterpolate, -700, 300)
    MEL.connect_material_expressions(one, '', lp, 'A'); MEL.connect_material_expressions(rd, '', lp, 'B'); MEL.connect_material_expressions(amt, '', lp, 'Alpha')
    m1 = p(unreal.MaterialExpressionMultiply, -800, 100); MEL.connect_material_expressions(col, '', m1, 'A'); MEL.connect_material_expressions(inten, '', m1, 'B')
    m2 = p(unreal.MaterialExpressionMultiply, -500, 150); MEL.connect_material_expressions(m1, '', m2, 'A'); MEL.connect_material_expressions(lp, '', m2, 'B')
    MEL.connect_material_property(m2, '', unreal.MaterialProperty.MP_EMISSIVE_COLOR)
    base = p(unreal.MaterialExpressionVectorParameter, -500, -150); base.set_editor_property('parameter_name', 'Base')
    base.set_editor_property('default_value', unreal.LinearColor(0.05, 0.04, 0.03, 1))
    MEL.connect_material_property(base, '', unreal.MaterialProperty.MP_BASE_COLOR)
    r = p(unreal.MaterialExpressionConstant, -500, -50); r.set_editor_property('r', 0.25)
    MEL.connect_material_property(r, '', unreal.MaterialProperty.MP_ROUGHNESS)
    MEL.recompile_material(m)
    unreal.EditorAssetLibrary.save_asset(path, False)
    return m

def glow(name, color, inten, blink):
    path = MAT + '/' + name
    mi = unreal.load_asset(path) if unreal.EditorAssetLibrary.does_asset_exist(path) else \
        unreal.AssetToolsHelpers.get_asset_tools().create_asset(name, MAT, unreal.MaterialInstanceConstant, unreal.MaterialInstanceConstantFactoryNew())
    mi.set_editor_property('parent', glow_master())
    MEL.set_material_instance_vector_parameter_value(mi, 'Color', unreal.LinearColor(*color, 1))
    MEL.set_material_instance_scalar_parameter_value(mi, 'Intensity', inten)
    MEL.set_material_instance_scalar_parameter_value(mi, 'BlinkAmount', blink)
    unreal.EditorAssetLibrary.save_asset(path, False)
    return mi

def paint(name, color, rough=0.7, dirt=0.5):
    path = MAT + '/' + name
    mi = unreal.load_asset(path) if unreal.EditorAssetLibrary.does_asset_exist(path) else \
        unreal.AssetToolsHelpers.get_asset_tools().create_asset(name, MAT, unreal.MaterialInstanceConstant, unreal.MaterialInstanceConstantFactoryNew())
    mi.set_editor_property('parent', unreal.load_asset(MAT + '/M_Town_Paint'))
    MEL.set_material_instance_vector_parameter_value(mi, 'Color', unreal.LinearColor(*color, 1))
    MEL.set_material_instance_scalar_parameter_value(mi, 'Roughness', rough)
    MEL.set_material_instance_scalar_parameter_value(mi, 'DirtAmount', dirt)
    unreal.EditorAssetLibrary.save_asset(path, False)
    return mi

def run():
    open(LOG, 'w').close()
    if 'noimport' not in sys.argv:
        t = unreal.AssetImportTask(); t.filename = os.path.join(FBX, 'SM_TrafficLight.fbx'); t.destination_path = MESH
        t.automated = True; t.replace_existing = True; t.save = True
        unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([t])
    mats = {'M_TLBody': paint('MI_Town_TLBody', (0.20, 0.19, 0.08), 0.6, 0.6),
            'M_LensRed': glow('MI_Town_LensRed', (1.0, 0.05, 0.02), 0.08, 0.0),
            'M_LensAmber': glow('MI_Town_LensAmber', (1.0, 0.45, 0.04), 14.0, 1.0),
            'M_LensGreen': glow('MI_Town_LensGreen', (0.1, 1.0, 0.5), 0.06, 0.0)}
    sm = unreal.load_asset(MESH + '/SM_TrafficLight')
    for i, s in enumerate(sm.static_materials):
        for k, v in mats.items():
            if str(s.material_slot_name).startswith(k):
                sm.set_material(i, v)
    unreal.EditorAssetLibrary.save_asset(MESH + '/SM_TrafficLight', False)

    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    les.set_current_level_by_name('L_Library_Street')
    for a in eas.get_all_level_actors():
        if a.get_actor_label().startswith('TR_'):
            eas.destroy_actor(a)
    road = unreal.load_asset(MAT + '/MI_Town_Road')
    yellow = unreal.load_asset(MAT + '/MI_Town_Yellow')
    plane = unreal.load_asset('/Engine/BasicShapes/Plane')
    def put(obj, loc, yaw=0, scale=(1, 1, 1), label='x', mat=None):
        a = eas.spawn_actor_from_object(obj, unreal.Vector(*loc), unreal.Rotator(roll=0, pitch=0, yaw=yaw))
        a.set_actor_scale3d(unreal.Vector(*scale)); a.set_actor_label('TR_' + label); a.set_folder_path('Town/Cross')
        if mat:
            a.static_mesh_component.set_material(0, mat)
        return a
    # rua transversal (corre em X), por cima do chao geral
    cy = (CROSS_Y0 + CROSS_Y1) / 2.0
    for x0 in range(-2400, 8000, 800):
        put(plane, (x0 + 400, cy, -10.9), 0, (8.0, (CROSS_Y1 - CROSS_Y0) / 100.0, 1), 'CrossRoad', road)
    put(plane, (2800, cy - 9, -10.5), 0, (60.0, 0.10, 1), 'CrossLine', yellow)
    put(plane, (2800, cy + 9, -10.5), 0, (60.0, 0.10, 1), 'CrossLine', yellow)
    # faixa de parada (branca gasta) antes do cruzamento, na rua principal
    white = paint('MI_Town_White', (0.55, 0.55, 0.52), 0.6, 0.7)
    put(plane, ((STREET_X0 + 1764) / 2.0, CROSS_Y0 - 60, -10.6), 0, (3.9, 0.35, 1), 'StopBar', white)
    # postes do fio atravessado (nos cantos sul do cruzamento)
    ar = unreal.AssetRegistryHelpers.get_asset_registry()
    pole_path = [str(x.package_name) for x in ar.get_assets_by_path('/Game/MERIDIAN/VOL55_KingWashStrip/Meshes/NN', recursive=True) if str(x.asset_name) == 'SM_Electric_Poles_Set_01a'][0]
    pole = unreal.load_asset(pole_path); b = pole.get_bounding_box()
    top = 10 + (b.max.z - b.min.z)
    pa = put(pole, (1300, CROSS_Y0 - 120, 10 - b.min.z), 90, label='SpanPoleW')
    pb = put(pole, (2230, CROSS_Y0 - 120, 10 - b.min.z), 90, label='SpanPoleE')
    wz = top - 90
    start = unreal.Vector(1300, CROSS_Y0 - 120, wz); end = unreal.Vector(2230, CROSS_Y0 - 120, wz)
    # fio de sustentacao ESTATICO (cilindro fino): o CableActor cede no jogo e deixava os semaforos no ar
    cyl = unreal.load_asset('/Engine/BasicShapes/Cylinder')
    metal = unreal.load_asset(MAT + '/MI_Town_Metal')
    span = (end - start).length()
    w = put(cyl, ((start.x + end.x) / 2, start.y, wz), 0, (0.022, 0.022, span / 100.0), 'SpanWire', metal)
    w.set_actor_rotation(unreal.Rotator(roll=0, pitch=90, yaw=0), False)
    w.static_mesh_component.set_cast_shadow(False)
    # dois semaforos pendurados (lentes viradas para quem vem pela rua principal: +-Y), com haste ate o fio
    for x in (1580, 1950):
        put(sm, (x, CROSS_Y0 - 120, wz - 22), 90, label='TrafficLight')
        h = put(cyl, (x, CROSS_Y0 - 120, wz - 11), 0, (0.03, 0.03, 0.22), 'Hanger', metal)
        h.static_mesh_component.set_cast_shadow(False)
    les.set_current_level_by_name('L_Library')
    SAFE()
    log('done')

try:
    run()
except Exception:
    log(traceback.format_exc())
