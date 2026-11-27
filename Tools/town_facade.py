"""Importa as pecas da fachada (Saved/TownFBX), cria os materiais de pintura e coloca tudo
no subnivel L_Library_Street (rotulos 'FC_'). Idempotente. Rodar: py "<caminho>/town_facade.py" [noimport]
"""
import unreal, sys, traceback
LOG = r'C:\Users\krame\OneDrive\Documentos\Unreal Projects\library_project\Saved\town_facade.log'
FBX = r'C:\Users\krame\OneDrive\Documentos\Unreal Projects\library_project\Saved\TownFBX'
MESH_DIR = '/Game/Library/Meshes/Town'
MAT_DIR = '/Game/Library/Materials/Town'
MEL = unreal.MaterialEditingLibrary

def log(*a):
    with open(LOG, 'a') as f:
        f.write(' '.join(str(x) for x in a) + '\n')

def master():
    path = MAT_DIR + '/M_Town_Paint'
    if unreal.EditorAssetLibrary.does_asset_exist(path):
        return unreal.load_asset(path)
    tools = unreal.AssetToolsHelpers.get_asset_tools()
    m = tools.create_asset('M_Town_Paint', MAT_DIR, unreal.Material, unreal.MaterialFactoryNew())
    col = MEL.create_material_expression(m, unreal.MaterialExpressionVectorParameter, -900, -100)
    col.set_editor_property('parameter_name', 'Color')
    col.set_editor_property('default_value', unreal.LinearColor(0.5, 0.5, 0.5, 1))
    dirt = MEL.create_material_expression(m, unreal.MaterialExpressionVectorParameter, -900, 100)
    dirt.set_editor_property('parameter_name', 'Dirt')
    dirt.set_editor_property('default_value', unreal.LinearColor(0.18, 0.16, 0.13, 1))
    wp = MEL.create_material_expression(m, unreal.MaterialExpressionWorldPosition, -1300, 300)
    nz = MEL.create_material_expression(m, unreal.MaterialExpressionNoise, -1100, 300)
    nz.set_editor_property('scale', 0.02)
    nz.set_editor_property('levels', 4)
    nz.set_editor_property('output_min', 0.0)
    nz.set_editor_property('output_max', 1.0)
    MEL.connect_material_expressions(wp, '', nz, 'Position')
    amt = MEL.create_material_expression(m, unreal.MaterialExpressionScalarParameter, -1100, 500)
    amt.set_editor_property('parameter_name', 'DirtAmount')
    amt.set_editor_property('default_value', 0.35)
    mul = MEL.create_material_expression(m, unreal.MaterialExpressionMultiply, -800, 300)
    MEL.connect_material_expressions(nz, '', mul, 'A')
    MEL.connect_material_expressions(amt, '', mul, 'B')
    lerp = MEL.create_material_expression(m, unreal.MaterialExpressionLinearInterpolate, -500, 0)
    MEL.connect_material_expressions(col, '', lerp, 'A')
    MEL.connect_material_expressions(dirt, '', lerp, 'B')
    MEL.connect_material_expressions(mul, '', lerp, 'Alpha')
    MEL.connect_material_property(lerp, '', unreal.MaterialProperty.MP_BASE_COLOR)
    rough = MEL.create_material_expression(m, unreal.MaterialExpressionScalarParameter, -500, 250)
    rough.set_editor_property('parameter_name', 'Roughness')
    rough.set_editor_property('default_value', 0.8)
    MEL.connect_material_property(rough, '', unreal.MaterialProperty.MP_ROUGHNESS)
    met = MEL.create_material_expression(m, unreal.MaterialExpressionScalarParameter, -500, 400)
    met.set_editor_property('parameter_name', 'Metallic')
    met.set_editor_property('default_value', 0.0)
    MEL.connect_material_property(met, '', unreal.MaterialProperty.MP_METALLIC)
    MEL.recompile_material(m)
    unreal.EditorAssetLibrary.save_asset(path, False)
    return m

def paint(name, color, rough=0.8, metal=0.0, dirt=0.35):
    path = MAT_DIR + '/' + name
    if unreal.EditorAssetLibrary.does_asset_exist(path):
        mi = unreal.load_asset(path)
    else:
        tools = unreal.AssetToolsHelpers.get_asset_tools()
        mi = tools.create_asset(name, MAT_DIR, unreal.MaterialInstanceConstant, unreal.MaterialInstanceConstantFactoryNew())
    mi.set_editor_property('parent', master())
    MEL.set_material_instance_vector_parameter_value(mi, 'Color', unreal.LinearColor(*color, 1))
    MEL.set_material_instance_scalar_parameter_value(mi, 'Roughness', rough)
    MEL.set_material_instance_scalar_parameter_value(mi, 'Metallic', metal)
    MEL.set_material_instance_scalar_parameter_value(mi, 'DirtAmount', dirt)
    unreal.EditorAssetLibrary.save_asset(path, False)
    return mi

def import_all():
    import os
    tasks = []
    for f in sorted(os.listdir(FBX)):
        if not f.endswith('.fbx'):
            continue
        t = unreal.AssetImportTask()
        t.filename = os.path.join(FBX, f)
        t.destination_path = MESH_DIR
        t.automated = True
        t.replace_existing = True
        t.save = True
        tasks.append(t)
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
    for t in tasks:
        log('imported', t.filename, list(t.imported_object_paths))

def run():
    open(LOG, 'w').close()
    if 'noimport' not in sys.argv:
        import_all()
    mats = {
        'M_Trim': paint('MI_Town_Trim', (0.62, 0.58, 0.50), 0.85, 0, 0.45),
        'M_Band': paint('MI_Town_Band', (0.035, 0.075, 0.055), 0.55, 0, 0.30),
        'M_Brass': paint('MI_Town_Brass', (0.55, 0.40, 0.16), 0.45, 1.0, 0.50),
        'M_Canvas': paint('MI_Town_Canvas', (0.05, 0.11, 0.085), 0.95, 0, 0.55),
        'M_Metal': paint('MI_Town_Metal', (0.05, 0.05, 0.05), 0.6, 0.6, 0.30),
        'M_BoxPaint': paint('MI_Town_BookBox', (0.04, 0.09, 0.18), 0.6, 0.2, 0.45),
    }
    # aplica os materiais pelos nomes dos slots
    for n in ['SM_Lib_Cornice', 'SM_Lib_Pilaster', 'SM_Lib_SignBand', 'SM_Lib_SignLetters', 'SM_Lib_Awning', 'SM_BookReturn']:
        sm = unreal.load_asset(MESH_DIR + '/' + n)
        if not sm:
            log('missing', n); continue
        for i, s in enumerate(sm.static_materials):
            key = str(s.material_slot_name)
            for k, v in mats.items():
                if key.startswith(k):
                    sm.set_material(i, v)
        log(n, [str(s.material_slot_name) for s in sm.static_materials], sm.get_bounding_box())
        unreal.EditorAssetLibrary.save_asset(MESH_DIR + '/' + n, False)

    les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    les.set_current_level_by_name('L_Library_Street')
    for a in eas.get_all_level_actors():
        if a.get_actor_label().startswith('FC_'):
            eas.destroy_actor(a)
    def put(n, loc, yaw=0, label=None, scale=1.0):
        sm = unreal.load_asset(MESH_DIR + '/' + n)
        a = eas.spawn_actor_from_object(sm, unreal.Vector(*loc), unreal.Rotator(roll=0, pitch=0, yaw=yaw))
        a.set_actor_scale3d(unreal.Vector(scale, scale, scale))
        a.set_actor_label('FC_' + (label or n))
        a.set_folder_path('Town/Facade')
        return a
    WX = 1050
    put('SM_Lib_Cornice', (WX, 0, 0))
    put('SM_Lib_Pilaster', (WX, -450, 0), label='Pilaster_S')
    put('SM_Lib_Pilaster', (WX, 450, 0), label='Pilaster_N')
    put('SM_Lib_SignBand', (WX, 0, 0))
    put('SM_Lib_SignLetters', (WX, 0, 0))
    put('SM_Lib_Awning', (WX, 0, 0))
    les.set_current_level_by_name('L_Library')
    unreal.EditorLoadingAndSavingUtils.save_packages([p for p in list(unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()) + list(unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()) if p.get_name().startswith('/Game/Library')], True)  # so o que e nosso (nunca Stationer/pacotes)
    log('done')

try:
    run()
except Exception:
    log(traceback.format_exc())

