"""Placas de STOP nas esquinas do cruzamento da Elm Street (L_Library_Street, rotulos 'SP_'). Idempotente.
Rodar: py "<caminho>/town_stop.py" [noimport]
"""
import unreal, os, sys, traceback
LOG = r'C:\Users\krame\OneDrive\Documentos\Unreal Projects\library_project\Saved\town_stop.log'
FBX = r'C:\Users\krame\OneDrive\Documentos\Unreal Projects\library_project\Saved\TownFBX5\SM_StopSign.fbx'
MESH = '/Game/Library/Meshes/Town'; MAT = '/Game/Library/Materials/Town'
MEL = unreal.MaterialEditingLibrary

def log(*a):
    with open(LOG, 'a') as f:
        f.write(' '.join(str(x) for x in a) + '\n')

def paint(name, color, rough=0.6, dirt=0.55):
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
        t = unreal.AssetImportTask(); t.filename = FBX; t.destination_path = MESH
        t.automated = True; t.replace_existing = True; t.save = True
        unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([t])
    mats = {'M_StopRed': paint('MI_Town_StopRed', (0.38, 0.03, 0.02)), 'M_StopWhite': unreal.load_asset(MAT + '/MI_Town_White'),
            'M_Metal': unreal.load_asset(MAT + '/MI_Town_Metal')}
    sm = unreal.load_asset(MESH + '/SM_StopSign')
    for i, s in enumerate(sm.static_materials):
        for k, v in mats.items():
            if str(s.material_slot_name).startswith(k) and v:
                sm.set_material(i, v)
    unreal.EditorAssetLibrary.save_asset(MESH + '/SM_StopSign', False)
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    les.set_current_level_by_name('L_Library_Street')
    for a in eas.get_all_level_actors():
        if a.get_actor_label().startswith('SP_'):
            eas.destroy_actor(a)
    for (x, y, yaw, tilt) in ((1310, 3170, -90, 4), (2215, 4230, 90, -3)):
        a = eas.spawn_actor_from_object(sm, unreal.Vector(x, y, 10), unreal.Rotator(roll=tilt, pitch=0, yaw=yaw))
        a.set_actor_label('SP_StopSign'); a.set_folder_path('Town/Cross')
        a.static_mesh_component.set_cast_shadow(False)
    les.set_current_level_by_name('L_Library')
    unreal.EditorLoadingAndSavingUtils.save_packages([p for p in list(unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()) + list(unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()) if p.get_name().startswith('/Game/Library')], True)
    log('done')

try:
    run()
except Exception:
    log(traceback.format_exc())
