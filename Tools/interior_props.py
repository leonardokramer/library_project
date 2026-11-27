"""Carrinho de devolucao e capacho da entrada (L_Library, pasta Props/Entrance, rotulos 'Prop_Entrance_').
Tambem reimporta as letras do letreiro. Rodar: py "<caminho>/interior_props.py" [noimport]
"""
import unreal, os, sys, traceback
LOG = r'C:\Users\krame\OneDrive\Documentos\Unreal Projects\library_project\Saved\interior_props.log'
FBX = r'C:\Users\krame\OneDrive\Documentos\Unreal Projects\library_project\Saved\TownFBX3'
MESH = '/Game/Library/Meshes/Town'
MAT = '/Game/Library/Materials/Town'
MEL = unreal.MaterialEditingLibrary

def log(*a):
    with open(LOG, 'a') as f:
        f.write(' '.join(str(x) for x in a) + '\n')

def paint(name, color, rough, dirt):
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
        tasks = []
        for f in sorted(os.listdir(FBX)):
            t = unreal.AssetImportTask(); t.filename = os.path.join(FBX, f); t.destination_path = MESH
            t.automated = True; t.replace_existing = True; t.save = True; tasks.append(t)
        unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    wood = None
    for a in eas.get_all_level_actors():
        if a.get_actor_label() == 'Bookshelf_04':
            wood = a.static_mesh_component.get_material(0)
    log('wood', wood.get_path_name() if wood else None)
    mats = {'M_CartWood': wood, 'M_Metal': unreal.load_asset(MAT + '/MI_Town_Metal'),
            'M_DoorMat': paint('MI_Town_DoorMat', (0.055, 0.042, 0.03), 0.95, 0.6),
            'M_Brass': unreal.load_asset(MAT + '/MI_Town_Brass')}
    for n in ('SM_ReturnCart', 'SM_DoorMat', 'SM_Lib_SignLetters'):
        sm = unreal.load_asset(MESH + '/' + n)
        for i, s in enumerate(sm.static_materials):
            for k, v in mats.items():
                if str(s.material_slot_name).startswith(k) and v:
                    sm.set_material(i, v)
        unreal.EditorAssetLibrary.save_asset(MESH + '/' + n, False)
        log(n, sm.get_bounding_box())
    les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    les.set_current_level_by_name('L_Library')
    for a in eas.get_all_level_actors():
        if a.get_actor_label().startswith('Prop_Entrance_'):
            eas.destroy_actor(a)
    def put(n, loc, yaw, label):
        a = eas.spawn_actor_from_object(unreal.load_asset(MESH + '/' + n), unreal.Vector(*loc), unreal.Rotator(roll=0, pitch=0, yaw=yaw))
        a.set_actor_label('Prop_Entrance_' + label); a.set_folder_path('Props/Entrance')
        a.static_mesh_component.set_editor_property('can_ever_affect_navigation', False)
        return a
    put('SM_ReturnCart', (955, -70, 10), 0, 'ReturnCart')
    m = put('SM_DoorMat', (978, 207, 10.2), 0, 'DoorMat')
    m.static_mesh_component.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
    unreal.EditorLoadingAndSavingUtils.save_packages([p for p in list(unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()) + list(unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()) if p.get_name().startswith('/Game/Library')], True)  # so o que e nosso (nunca Stationer/pacotes)
    log('done')

try:
    run()
except Exception:
    log(traceback.format_exc())

