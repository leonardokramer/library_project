"""Cercas velhas (Fences VOL.4) no L_Library_Street (rotulos 'FN_'): fundo dos becos e terrenos vazios ao sul.
Tira os cubos provisorios do fundo dos becos (NB_Alley*Fence). Idempotente. Rodar: py "<caminho>/town_fences.py"
"""
import unreal, traceback
LOG = r'C:\Users\krame\OneDrive\Documentos\Unreal Projects\library_project\Saved\town_fences.log'

def log(*a):
    with open(LOG, 'a') as f:
        f.write(' '.join(str(x) for x in a) + '\n')

def run():
    open(LOG, 'w').close()
    ar = unreal.AssetRegistryHelpers.get_asset_registry()
    FIND = {str(a.asset_name): str(a.package_name) for a in ar.get_assets_by_path('/Game/FENCES', recursive=True) if '/LP/' not in str(a.package_name)}
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    les.set_current_level_by_name('L_Library_Street')
    for a in eas.get_all_level_actors():
        lab = a.get_actor_label()
        if lab.startswith('FN_') or lab in ('NB_AlleyNFence', 'NB_AlleySFence'):
            eas.destroy_actor(a)
    def put(name, x, y, yaw, sx=1.0, label='Fence'):
        sm = unreal.load_asset(FIND[name]); b = sm.get_bounding_box()
        a = eas.spawn_actor_from_object(sm, unreal.Vector(x, y, 10 - b.min.z), unreal.Rotator(roll=0, pitch=0, yaw=yaw))
        a.set_actor_scale3d(unreal.Vector(sx, 1, 1)); a.set_actor_label('FN_' + label); a.set_folder_path('Town/Fences')
        a.static_mesh_component.set_cast_shadow(False)
        return a
    # fundo dos becos: tapume alto de tabuas (25a: 377 de comprimento em X, centrado) atravessando o beco (ao longo de Y)
    for yc in (575, -575):
        put('SM_Fence_Wooden_Old_NN_25a', -100, yc, 90, 285.0 / 377.0, 'AlleyBack')
    # terreno vazio ao sul da loja do sul, junto a calcada (X 1040), cerca baixa de 220 cm (26g: X -220..0)
    y = -1820
    i = 0
    while y > -3200:
        put('SM_Fence_Wooden_Old_NN_26g', 1040, y, -90 if i % 5 != 3 else -87, 1.0, 'LotSouth')
        y -= 220; i += 1
    # do outro lado da rua, ao sul do King Wash
    y = -2650
    while y > -3200:
        put('SM_Fence_Wooden_Old_NN_26g', 2490, y, 90, 1.0, 'LotSouthE')
        y -= 220
    les.set_current_level_by_name('L_Library')
    unreal.EditorLoadingAndSavingUtils.save_packages([p for p in list(unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()) + list(unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()) if p.get_name().startswith('/Game/Library')], True)
    log('done')

try:
    run()
except Exception:
    log(traceback.format_exc())
