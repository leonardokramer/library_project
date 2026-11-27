"""Importa os vizinhos (Saved/TownFBX2) e coloca no L_Library_Street (rotulos 'NB_'), com becos.
Rodar: py "<caminho>/town_shops_ue.py" [noimport]
"""
import unreal, sys, os, traceback
LOG = r'C:\Users\krame\OneDrive\Documentos\Unreal Projects\library_project\Saved\town_shops.log'
FBX = r'C:\Users\krame\OneDrive\Documentos\Unreal Projects\library_project\Saved\TownFBX2'
MESH_DIR = '/Game/Library/Meshes/Town'
MAT_DIR = '/Game/Library/Materials/Town'
KW = '/Game/MERIDIAN/VOL55_KingWashStrip/Materials/'
MEL = unreal.MaterialEditingLibrary

def log(*a):
    with open(LOG, 'a') as f:
        f.write(' '.join(str(x) for x in a) + '\n')

def find_mat(name):
    ar = unreal.AssetRegistryHelpers.get_asset_registry()
    for ad in ar.get_assets_by_path('/Game/MERIDIAN/VOL55_KingWashStrip/Materials', recursive=True):
        if str(ad.asset_name) == name:
            return unreal.load_asset(str(ad.package_name))
    for ad in ar.get_assets_by_path('/Game/REALISTIC_MATERIALS', recursive=True):
        if str(ad.asset_name) == name:
            return unreal.load_asset(str(ad.package_name))
    log('no mat', name)

def paint(name, color, rough=0.85, dirt=0.5):
    path = MAT_DIR + '/' + name
    if unreal.EditorAssetLibrary.does_asset_exist(path):
        mi = unreal.load_asset(path)
    else:
        mi = unreal.AssetToolsHelpers.get_asset_tools().create_asset(name, MAT_DIR, unreal.MaterialInstanceConstant, unreal.MaterialInstanceConstantFactoryNew())
    mi.set_editor_property('parent', unreal.load_asset(MAT_DIR + '/M_Town_Paint'))
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
            t = unreal.AssetImportTask(); t.filename = os.path.join(FBX, f); t.destination_path = MESH_DIR
            t.automated = True; t.replace_existing = True; t.save = True
            tasks.append(t)
        unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
    trim_dark = paint('MI_Town_TrimDark', (0.20, 0.18, 0.15), 0.85, 0.5)
    board = find_mat('MI_Board_Wall_01a'); siding = find_mat('MI_Grocery_Wall_01a'); plaster = find_mat('MI_LM_Plaster_Wall_01a')
    ply = find_mat('MI_Plywood_Wall_01a'); glass = find_mat('MI_Glass_01c')
    concrete = unreal.load_asset(MAT_DIR + '/MI_Town_Ground')
    base = {'M_TrimN': trim_dark, 'M_Plywood': ply, 'M_Glass': glass, 'M_Siding': siding}
    for n in ('SM_Town_ShopNorth', 'SM_Town_ShopSouth'):
        sm = unreal.load_asset(MESH_DIR + '/' + n)
        for i, s in enumerate(sm.static_materials):
            k = str(s.material_slot_name)
            for kk, v in base.items():
                if k.startswith(kk) and v:
                    sm.set_material(i, v)
        unreal.EditorAssetLibrary.save_asset(MESH_DIR + '/' + n, False)
        log(n, [str(s.material_slot_name) for s in sm.static_materials])

    les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    les.set_current_level_by_name('L_Library_Street')
    for a in eas.get_all_level_actors():
        if a.get_actor_label().startswith('NB_'):
            eas.destroy_actor(a)
    def put(obj, loc, yaw=0, scale=(1, 1, 1), label='x', mat=None, slot=0):
        a = eas.spawn_actor_from_object(obj, unreal.Vector(*loc), unreal.Rotator(roll=0, pitch=0, yaw=yaw))
        a.set_actor_scale3d(unreal.Vector(*scale)); a.set_actor_label('NB_' + label); a.set_folder_path('Town/Neighbors')
        if mat:
            a.static_mesh_component.set_material(slot, mat)
        return a
    north = put(unreal.load_asset(MESH_DIR + '/SM_Town_ShopNorth'), (1048, 1200, 10), label='ShopNorth')
    south = put(unreal.load_asset(MESH_DIR + '/SM_Town_ShopSouth'), (1048, -1250, 10), label='ShopSouth')
    sm = unreal.load_asset(MESH_DIR + '/SM_Town_ShopSouth')
    for i, s in enumerate(sm.static_materials):
        if str(s.material_slot_name).startswith('M_Siding') and plaster:
            south.static_mesh_component.set_material(i, plaster)
    plane = unreal.load_asset('/Engine/BasicShapes/Plane')
    cube = unreal.load_asset('/Engine/BasicShapes/Cube')
    # chao dos becos (X -150..1048) e cercas de tabua no fundo
    for yc, lab in ((575, 'AlleyN'), (-575, 'AlleyS')):
        put(plane, (450, yc, 9), scale=(12.0, 2.5, 1), label=lab + 'Ground', mat=concrete)
        put(cube, (-100, yc, 10 + 160), scale=(0.08, 2.8, 3.2), label=lab + 'Fence', mat=board)
    dump = [str(ad.package_name) for ad in unreal.AssetRegistryHelpers.get_asset_registry().get_assets_by_path('/Game/MERIDIAN/VOL55_KingWashStrip/Meshes/NN', recursive=True) if str(ad.asset_name) == 'SM_Dumpster_Large_NN_01a']
    if dump:
        d = unreal.load_asset(dump[0]); b = d.get_bounding_box()
        put(d, (600, 590, 10 - b.min.z), yaw=90, label='Dumpster')
    les.set_current_level_by_name('L_Library')
    unreal.EditorLoadingAndSavingUtils.save_packages([p for p in list(unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()) + list(unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()) if p.get_name().startswith('/Game/Library')], True)  # so o que e nosso (nunca Stationer/pacotes)
    log('done')

try:
    run()
except Exception:
    log(traceback.format_exc())



